"""Error handling middleware and rate limiting (Section 11)."""

import time
import uuid

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

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
