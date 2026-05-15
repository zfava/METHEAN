"""TTS provider factory.

Mirrors the whisper factory pattern: picks per-household by policy
and falls back to OpenAI when the requested provider is unusable
(e.g., ElevenLabs selected but no API key configured).
"""

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.identity import PersonalizationPolicy
from app.services.tts.base import TTSClient
from app.services.tts.elevenlabs_provider import ElevenLabsTTSProvider
from app.services.tts.openai_provider import OpenAITTSProvider

logger = logging.getLogger("methean.voice.tts.factory")


async def get_tts_client(db: AsyncSession, household_id: uuid.UUID) -> TTSClient:
    result = await db.execute(select(PersonalizationPolicy).where(PersonalizationPolicy.household_id == household_id))
    policy = result.scalar_one_or_none()
    choice = (policy.tts_provider if policy is not None else "openai") or "openai"

    if choice == "elevenlabs":
        api_key = getattr(settings, "ELEVENLABS_API_KEY", "")
        if api_key:
            return ElevenLabsTTSProvider(api_key=api_key)
        logger.info(
            "elevenlabs_not_configured_fallback_to_openai",
            extra={"household_id": str(household_id)},
        )
    return OpenAITTSProvider()
