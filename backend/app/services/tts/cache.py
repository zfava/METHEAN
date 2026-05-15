"""TTS cache service.

Lookup and insert audio bytes for cacheable phrases. The cache is
global; the gate is the phrase allowlist. ``evict_lru`` is called
by a scheduled task (not yet wired) when cache size exceeds the
configured cap.
"""

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tts_cache import TTSCache

logger = logging.getLogger("methean.voice.tts.cache")


async def lookup(db: AsyncSession, *, cache_key_value: str) -> tuple[bytes, float] | None:
    """Return ``(audio_bytes, duration_seconds)`` on hit, None on miss.

    On hit we bump ``access_count`` and ``last_accessed_at`` so the
    LRU eviction has accurate metadata.
    """
    result = await db.execute(select(TTSCache).where(TTSCache.text_hash == cache_key_value))
    row = result.scalar_one_or_none()
    if row is None:
        return None
    await db.execute(
        update(TTSCache)
        .where(TTSCache.id == row.id)
        .values(access_count=TTSCache.access_count + 1, last_accessed_at=row.created_at.__class__.now())
    )
    return bytes(row.audio_bytes), float(row.audio_duration_seconds)


async def insert(
    db: AsyncSession,
    *,
    cache_key_value: str,
    voice_id: str,
    provider: str,
    audio_bytes: bytes,
    duration_seconds: float,
) -> None:
    """Idempotent cache insert. UniqueConstraint guards against dupes."""
    entry = TTSCache(
        text_hash=cache_key_value,
        voice_id=voice_id,
        provider=provider,
        audio_bytes=audio_bytes,
        audio_duration_seconds=duration_seconds,
        byte_count=len(audio_bytes),
    )
    db.add(entry)
    try:
        await db.flush()
    except Exception:
        # Race: another request inserted first. Treat as success;
        # the row exists, our copy is redundant.
        await db.rollback()
