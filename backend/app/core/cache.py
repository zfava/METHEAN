"""Redis cache utilities for hot-path API responses.

Advisory: if Redis is down, all operations are no-ops (fail open).
"""

import json
import logging
from typing import Any

import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

_redis: aioredis.Redis | None = None


def init_cache(redis_client: aioredis.Redis) -> None:
    global _redis
    _redis = redis_client


async def cache_get(key: str) -> Any | None:
    """Get cached value. Returns None on miss or error."""
    if not _redis:
        return None
    try:
        data = await _redis.get(key)
        return json.loads(data) if data else None
    except Exception:
        logger.debug("Cache miss or error for key=%s", key)
        return None


async def cache_set(key: str, value: Any, ttl_seconds: int = 30) -> None:
    """Cache a value with TTL. No-op on error."""
    if not _redis:
        return
    try:
        await _redis.set(key, json.dumps(value, default=str), ex=ttl_seconds)
    except Exception:
        logger.debug("Cache set error for key=%s", key)


async def cache_delete(key: str) -> None:
    """Delete a cached key. No-op on error."""
    if not _redis:
        return
    try:
        await _redis.delete(key)
    except Exception:
        pass


async def cache_delete_pattern(pattern: str) -> None:
    """Delete all keys matching a glob pattern. Use sparingly."""
    if not _redis:
        return
    try:
        async for key in _redis.scan_iter(match=pattern):
            await _redis.delete(key)
    except Exception:
        pass
