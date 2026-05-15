"""Whisper provider factory.

Picks per-household based on ``PersonalizationPolicy.whisper_provider``.
Falls back to openai if the household selected ``local`` but the
local service is unreachable on health-check; the swap is logged.
"""

import logging
import uuid

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.identity import PersonalizationPolicy
from app.services.whisper.base import WhisperClient
from app.services.whisper.local_provider import LocalWhisperProvider
from app.services.whisper.openai_provider import OpenAIWhisperProvider

logger = logging.getLogger("methean.voice.factory")


async def _local_alive(timeout_seconds: float = 1.0) -> bool:
    """Cheap liveness probe used as the fallback signal."""
    base = getattr(settings, "LOCAL_WHISPER_URL", "")
    if not base:
        return False
    url = f"{base.rstrip('/')}/health"
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            resp = await client.get(url)
        return resp.status_code < 500
    except Exception:
        return False


async def get_whisper_client(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> WhisperClient:
    """Resolve the provider for the household, with cloud fallback."""
    result = await db.execute(select(PersonalizationPolicy).where(PersonalizationPolicy.household_id == household_id))
    policy = result.scalar_one_or_none()
    choice = (policy.whisper_provider if policy is not None else "openai") or "openai"

    if choice == "local":
        if await _local_alive():
            return LocalWhisperProvider()
        logger.warning(
            "local_whisper_unreachable_fallback_to_openai",
            extra={"household_id": str(household_id)},
        )
    return OpenAIWhisperProvider()
