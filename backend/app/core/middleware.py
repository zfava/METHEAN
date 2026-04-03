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
    """Redis-backed rate limiter. Returns 429 with Retry-After header."""

    def __init__(self, app: FastAPI, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip health checks and static files
        if request.url.path in ("/health", "/health/ready", "/metrics"):
            return await call_next(request)

        # Get client identifier (IP or user from token)
        client_ip = request.client.host if request.client else "unknown"
        window_key = f"ratelimit:{client_ip}:{int(time.time()) // 60}"

        try:
            redis = request.app.state.redis
            count = await redis.incr(window_key)
            if count == 1:
                await redis.expire(window_key, 60)

            if count > self.rpm:
                return JSONResponse(
                    status_code=429,
                    content={
                        "code": "rate_limited",
                        "message": "Too many requests",
                        "detail": f"Rate limit: {self.rpm} requests per minute",
                    },
                    headers={"Retry-After": "60"},
                )
        except Exception:
            # If Redis is down, allow the request (fail open)
            pass

        return await call_next(request)


# Paths exempt from CSRF checks (unauthenticated or initial auth flow)
_CSRF_EXEMPT_PATHS = {
    "/health",
    "/health/ready",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
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
