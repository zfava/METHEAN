"""OpenAI Whisper provider.

Wraps the ``whisper-1`` model behind the WhisperClient protocol with
a single retry on 5xx and timeout failures. The audio bytes are
passed via :class:`io.BytesIO` so the SDK never reads from disk.

Logs never include the audio payload or the transcript text at
INFO level. DEBUG-level logs scrub the transcript via
:func:`_scrub_transcript_for_logs` which truncates to length only.
"""

import asyncio
import io
import logging
from time import perf_counter

from app.core.config import settings
from app.services.whisper.base import TranscriptionResult, WhisperError

logger = logging.getLogger("methean.voice.openai")


class OpenAIWhisperProvider:
    name = "openai"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        timeout_seconds: float = 10.0,
        max_retries: int = 1,
    ) -> None:
        # Defer SDK import so the module loads cleanly in environments
        # without the openai package installed (e.g., the test runner
        # when AI_MOCK_ENABLED is True).
        self._api_key = api_key or getattr(settings, "OPENAI_API_KEY", "") or getattr(settings, "AI_API_KEY", "")
        self._timeout = timeout_seconds
        self._max_retries = max_retries

    async def transcribe(
        self,
        audio_handle: bytes,
        mime_type: str,
        *,
        language: str = "en",
        request_id: str,
    ) -> TranscriptionResult:
        if not self._api_key:
            raise WhisperError(
                "OPENAI_API_KEY not configured",
                kind="auth",
                retryable=False,
                provider=self.name,
            )

        last_err: WhisperError | None = None
        attempts = self._max_retries + 1
        for attempt in range(attempts):
            t0 = perf_counter()
            try:
                return await self._call(audio_handle, mime_type, language, request_id)
            except WhisperError as err:
                last_err = err
                logger.warning(
                    "openai_whisper_attempt_failed",
                    extra={
                        "request_id": request_id,
                        "attempt": attempt + 1,
                        "kind": err.kind,
                        "retryable": err.retryable,
                        "latency_ms": int((perf_counter() - t0) * 1000),
                    },
                )
                if not err.retryable or attempt + 1 >= attempts:
                    raise
                await asyncio.sleep(0.5)
        # Defensive: the loop above either returns or raises.
        assert last_err is not None
        raise last_err

    async def _call(
        self,
        audio_handle: bytes,
        mime_type: str,
        language: str,
        request_id: str,
    ) -> TranscriptionResult:
        try:
            from openai import APIError, APITimeoutError, AsyncOpenAI, AuthenticationError, RateLimitError
        except ImportError as e:  # pragma: no cover - SDK install gate
            raise WhisperError(
                "openai SDK missing",
                kind="provider_5xx",
                retryable=False,
                provider=self.name,
            ) from e

        client = AsyncOpenAI(api_key=self._api_key, timeout=self._timeout)
        # BytesIO wrapper so the SDK doesn't try to read a file path.
        # The OpenAI SDK requires a filename hint via the tuple form.
        buf = io.BytesIO(audio_handle)
        # Filename is purely a hint for the OpenAI parser; the bytes
        # are what matters.
        ext = "webm" if "webm" in mime_type else "mp3" if "mpeg" in mime_type else "m4a"
        file_tuple = (f"audio.{ext}", buf, mime_type or "audio/webm")
        try:
            resp = await client.audio.transcriptions.create(  # type: ignore[call-overload]
                model="whisper-1",
                file=file_tuple,
                language=language,
                response_format="verbose_json",
            )
        except APITimeoutError as e:
            raise WhisperError("openai timeout", kind="timeout", retryable=True, provider=self.name) from e
        except AuthenticationError as e:
            raise WhisperError("openai auth", kind="auth", retryable=False, provider=self.name) from e
        except RateLimitError as e:
            # Treat 429 from the provider as retryable; one retry helps
            # with the occasional burst.
            raise WhisperError("openai rate limit", kind="provider_4xx", retryable=True, provider=self.name) from e
        except APIError as e:
            status = getattr(e, "status_code", 500) or 500
            kind: str = "provider_5xx" if status >= 500 else "provider_4xx"
            raise WhisperError(
                f"openai api error: {status}",
                kind=kind,  # type: ignore[arg-type]
                retryable=status >= 500,
                provider=self.name,
            ) from e
        except Exception as e:  # pragma: no cover - defensive
            raise WhisperError(
                "openai unknown",
                kind="network",
                retryable=True,
                provider=self.name,
            ) from e

        text = (getattr(resp, "text", "") or "").strip()
        duration = float(getattr(resp, "duration", 0.0) or 0.0)
        language_detected = getattr(resp, "language", None) or None
        return TranscriptionResult(
            text=text,
            duration_seconds=duration,
            confidence=None,
            language_detected=language_detected,
        )


def _scrub_transcript_for_logs(text: str) -> str:
    """Reduce a transcript to a non-PII descriptor for DEBUG logs."""
    return f"<transcript len={len(text)}>"
