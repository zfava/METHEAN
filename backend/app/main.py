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
from app.api.auth import router as auth_router
from app.api.curriculum import router as curriculum_router
from app.api.state import router as state_router
from app.api.governance import router as governance_router

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

# CORS
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


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "methean"}
