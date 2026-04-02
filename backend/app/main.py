"""FastAPI application factory with lifespan handler."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import redis.asyncio as aioredis
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.core.logging import setup_logging
from app.core.middleware import ErrorHandlerMiddleware, RateLimitMiddleware
from app.api.auth import router as auth_router
from app.api.curriculum import router as curriculum_router
from app.api.state import router as state_router
from app.api.governance import router as governance_router
from app.api.operations import router as operations_router

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()

    # Initialize Redis
    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    app.state.redis = redis
    logger.info("redis_connected", url=settings.REDIS_URL)

    logger.info("app_started", env=settings.APP_ENV)
    yield

    # Shutdown
    await redis.aclose()
    await engine.dispose()
    logger.info("app_shutdown")


app = FastAPI(
    title="METHEAN",
    description="Learning governance operating system for homeschool families",
    version="0.1.0",
    lifespan=lifespan,
)

# Middleware (order matters: outermost first)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(curriculum_router, prefix="/api/v1")
app.include_router(state_router, prefix="/api/v1")
app.include_router(governance_router, prefix="/api/v1")
app.include_router(operations_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict:
    """Basic health check — API is alive."""
    return {"status": "ok", "service": "methean"}


@app.get("/health/ready")
async def health_ready() -> dict:
    """Readiness probe — DB + Redis connected."""
    checks = {"api": "ok"}

    # Check DB
    try:
        from sqlalchemy import text
        from app.core.database import engine as db_engine
        async with db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"

    # Check Redis
    try:
        redis = app.state.redis
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "degraded", "checks": checks}
