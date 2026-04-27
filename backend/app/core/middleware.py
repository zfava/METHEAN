"""Error handling middleware, rate limiting, and CSRF protection (Section 11)."""

import secrets
import time
import uuid

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

logger = structlog.get_logger()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses.

    The Content-Security-Policy is environment-aware:

    * Production drops ``'unsafe-eval'`` and replaces ``'unsafe-inline'``
      on script-src with a per-request nonce, allows js.stripe.com for
      payments, and forces upgrade-insecure-requests.
    * Development keeps ``'unsafe-eval' 'unsafe-inline'`` so Next.js
      HMR and React DevTools work, plus ``ws:``/``wss:`` for the dev
      server.

    The header name is ``Content-Security-Policy-Report-Only`` until
    ``settings.CSP_ENFORCE`` flips to True. Each response also carries
    the chosen nonce as ``X-CSP-Nonce`` so the Next.js layout can
    stamp it onto its inline scripts.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        nonce = secrets.token_urlsafe(16)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["X-CSP-Nonce"] = nonce

        if settings.APP_ENV == "production":
            csp = (
                "default-src 'self'; "
                f"script-src 'self' 'nonce-{nonce}' https://js.stripe.com; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https://api.anthropic.com https://api.openai.com "
                "https://api.stripe.com https://api.resend.com; "
                "frame-src https://js.stripe.com; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "upgrade-insecure-requests"
            )
        else:
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-eval' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob:; "
                "font-src 'self'; "
                "connect-src 'self' ws: wss: https://api.anthropic.com https://api.openai.com "
                "https://api.stripe.com https://api.resend.com; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )

        if settings.CSP_ENFORCE:
            response.headers["Content-Security-Policy"] = csp
        else:
            response.headers["Content-Security-Policy-Report-Only"] = csp + "; report-uri /api/v1/csp-report"
        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global exception handler. Returns structured error JSON.
    Never leaks stack traces in production."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start = time.monotonic()

        try:
            response = await call_next(request)
            elapsed = round((time.monotonic() - start) * 1000, 1)

            if response.status_code >= 500:
                logger.error(
                    "request_error",
                    request_id=request_id,
                    path=request.url.path,
                    status=response.status_code,
                    elapsed_ms=elapsed,
                )

            return response

        except Exception as exc:
            elapsed = round((time.monotonic() - start) * 1000, 1)
            logger.exception(
                "unhandled_exception",
                request_id=request_id,
                path=request.url.path,
                elapsed_ms=elapsed,
                error=str(exc),
            )

            from app.core.config import settings

            detail = str(exc) if not settings.is_production else "Internal server error"

            return JSONResponse(
                status_code=500,
                content={
                    "code": "internal_error",
                    "message": "Internal server error",
                    "detail": detail,
                    "request_id": request_id,
                },
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Coarse-grained baseline limiter using the shared "default" policy.

    Per-endpoint, per-identity limits are layered on top via
    :mod:`app.core.rate_limit` dependency factories. This middleware
    only enforces the wide-net cap on requests per IP+endpoint and
    fails open on Redis exceptions so an outage doesn't take down
    the whole API. Auth and AI routes get their own fail-closed
    policies via dependencies.
    """

    def __init__(self, app: FastAPI, requests_per_minute: int = 60):
        super().__init__(app)
        # rpm kept for backwards compatibility with main.py wiring;
        # the canonical numbers live in
        # ``rate_limit.POLICIES["default"]``.
        self.rpm = requests_per_minute

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip health checks and static files
        if request.url.path in ("/health", "/health/ready", "/metrics"):
            return await call_next(request)

        # Skip in test environments. Playwright E2E runs all
        # registrations from localhost in parallel and would otherwise
        # saturate the default policy after the first few requests.
        if settings.APP_ENV == "test":
            return await call_next(request)

        from app.core.rate_limit import POLICIES, check_and_consume, client_ip

        policy = POLICIES["default"]
        key_values = {
            "ip": client_ip(request, settings.TRUSTED_PROXIES),
            "endpoint": request.url.path,
        }
        redis = getattr(request.app.state, "redis", None)
        if redis is None:
            # No Redis configured (e.g. test environment). Apply policy's
            # fail_open behavior. Closed-fail policies (login, AI, etc.)
            # cannot enforce without Redis — log once and fall through;
            # tests for those routes should mock the limiter directly.
            if not policy.fail_open:
                import logging

                logging.getLogger("methean.middleware.ratelimit").warning(
                    "Rate limit policy %s cannot enforce: redis unavailable", policy.name
                )
            # Allow the request either way to avoid breaking the
            # request pipeline.
            return await call_next(request)

        allowed, retry_after = await check_and_consume(redis, policy, key_values)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "code": "rate_limited",
                    "message": "Too many requests",
                    "detail": f"Rate limit: {policy.requests} requests per {policy.window_seconds}s",
                },
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)


# Paths exempt from CSRF checks (unauthenticated or initial auth flow)
_CSRF_EXEMPT_PATHS = {
    "/health",
    "/health/ready",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/billing/webhook",
    # Browsers post CSP violation reports without our CSRF cookie.
    "/api/v1/csp-report",
}

_STATE_CHANGING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class CSRFMiddleware(BaseHTTPMiddleware):
    """Double-submit cookie CSRF protection.

    On every response, sets a non-httponly csrf_token cookie.
    On state-changing requests, verifies X-CSRF-Token header matches
    the cookie value.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        csrf_cookie = request.cookies.get("csrf_token")

        # Check CSRF on state-changing methods for non-exempt paths
        if request.method in _STATE_CHANGING_METHODS:
            if request.url.path not in _CSRF_EXEMPT_PATHS:
                csrf_header = request.headers.get("x-csrf-token")
                if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "code": "csrf_failed",
                            "message": "CSRF validation failed",
                        },
                    )

        response = await call_next(request)

        # Set or refresh the csrf_token cookie on every response.
        # Not httponly so the frontend JS can read it.
        if not csrf_cookie:
            csrf_cookie = secrets.token_hex(32)
        response.set_cookie(
            key="csrf_token",
            value=csrf_cookie,
            httponly=False,
            samesite="lax",
            secure=settings.is_production,
            path="/",
        )

        return response
