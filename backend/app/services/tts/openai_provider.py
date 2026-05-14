"""OpenAI tts-1 streaming provider.

Streams MP3 chunks via the SDK's ``with_streaming_response`` path.
One retry on 5xx + timeout. Audio chunks are passed back to the
caller as raw bytes; the endpoint wraps them in SSE.
"""

import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Any

from app.core.config import settings
from app.services.tts.base import TTSError

logger = logging.getLogger("methean.voice.tts.openai")


class OpenAITTSProvider:
    name = "openai"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        timeout_seconds: float = 15.0,
        max_retries: int = 1,
    ) -> None:
        self._api_key = api_key or getattr(settings, "OPENAI_API_KEY", "") or getattr(settings, "AI_API_KEY", "")
        self._timeout = timeout_seconds
        self._max_retries = max_retries

    async def stream_speech(
        self,
        text: str,
        voice_id: str,
        *,
        speech_rate: float,
        request_id: str,
    ) -> AsyncIterator[bytes]:
        if not self._api_key:
            raise TTSError("OPENAI_API_KEY not configured", kind="auth", retryable=False, provider=self.name)

        attempts = self._max_retries + 1
        last_err: TTSError | None = None
        for attempt in range(attempts):
            try:
                async for chunk in self._call(text, voice_id, speech_rate, request_id):
                    yield chunk
                return
            except TTSError as err:
                last_err = err
                logger.warning(
                    "openai_tts_attempt_failed",
                    extra={"request_id": request_id, "attempt": attempt + 1, "kind": err.kind},
                )
                if not err.retryable or attempt + 1 >= attempts:
                    raise
                await asyncio.sleep(0.5)
        assert last_err is not None  # pragma: no cover
        raise last_err

    async def _call(
        self,
        text: str,
        voice_id: str,
        speech_rate: float,
        request_id: str,
    ) -> AsyncIterator[bytes]:
        try:
            from openai import APIError, APITimeoutError, AsyncOpenAI, AuthenticationError, RateLimitError
        except ImportError as e:  # pragma: no cover
            raise TTSError("openai SDK missing", kind="provider_5xx", retryable=False, provider=self.name) from e

        client = AsyncOpenAI(api_key=self._api_key, timeout=self._timeout)
        try:
            stream_ctx = client.audio.speech.with_streaming_response.create(  # type: ignore[attr-defined]
                model="tts-1",
                voice=voice_id,
                input=text,
                response_format="mp3",
                speed=speech_rate,
            )
        except APITimeoutError as e:
            raise TTSError("openai timeout", kind="timeout", retryable=True, provider=self.name) from e
        except AuthenticationError as e:
            raise TTSError("openai auth", kind="auth", retryable=False, provider=self.name) from e
        except RateLimitError as e:
            raise TTSError("openai rate limit", kind="provider_4xx", retryable=True, provider=self.name) from e
        except APIError as e:
            status_code = getattr(e, "status_code", 500) or 500
            kind: str = "provider_5xx" if status_code >= 500 else "provider_4xx"
            raise TTSError(
                f"openai api error: {status_code}",
                kind=kind,  # type: ignore[arg-type]
                retryable=status_code >= 500,
                provider=self.name,
            ) from e
        except Exception as e:  # pragma: no cover
            raise TTSError("openai unknown", kind="network", retryable=True, provider=self.name) from e

        async with stream_ctx as response:  # type: ignore[union-attr]
            async for chunk in response.iter_bytes(chunk_size=4096):
                if chunk:
                    yield chunk


_ = Any  # avoid unused-import warning under some linters
