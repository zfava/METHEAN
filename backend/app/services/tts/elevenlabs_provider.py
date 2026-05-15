"""ElevenLabs Turbo v2 TTS provider (stub, feature-flagged).

When ``ELEVENLABS_API_KEY`` is configured, the household policy
can switch to ``tts_provider="elevenlabs"`` and route through this
provider. Until then, calling ``stream_speech`` raises a
``TTSError`` with ``kind="auth"`` so the endpoint falls back to
OpenAI (handled by the factory).

This file documents the contract; the full streaming integration
lands when premium households exist.
"""

from collections.abc import AsyncIterator

from app.core.config import settings
from app.services.tts.base import TTSError


class ElevenLabsTTSProvider:
    name = "elevenlabs"

    def __init__(self, *, api_key: str | None = None) -> None:
        self._api_key = api_key or getattr(settings, "ELEVENLABS_API_KEY", "")

    async def stream_speech(
        self,
        text: str,
        voice_id: str,
        *,
        speech_rate: float,
        request_id: str,
    ) -> AsyncIterator[bytes]:
        if not self._api_key:
            raise TTSError(
                "ELEVENLABS_API_KEY not configured",
                kind="auth",
                retryable=False,
                provider=self.name,
            )
        # Pretend stream interface so the type-checker is happy on
        # paths that never execute (no household has elevenlabs
        # enabled in v2).
        if False:  # pragma: no cover
            yield b""
        raise TTSError(
            "ElevenLabs provider not implemented",
            kind="provider_5xx",
            retryable=False,
            provider=self.name,
        )
