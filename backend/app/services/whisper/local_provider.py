"""Local faster-whisper provider.

POSTs the audio bytes as ``multipart/form-data`` to a self-hosted
faster-whisper service exposing ``POST /transcribe`` with the
response shape ``{"text", "duration", "confidence", "language"}``.

The service runs on the homestead Mac mini cluster. Deployment is
documented in ``docs/runbooks/local-whisper-deployment.md``.
"""

import asyncio
import logging
from time import perf_counter

import httpx

from app.core.config import settings
from app.services.whisper.base import TranscriptionResult, WhisperError

logger = logging.getLogger("methean.voice.local")


class LocalWhisperProvider:
    name = "local"

    def __init__(
        self,
        *,
        base_url: str | None = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 1,
    ) -> None:
        self._base_url = base_url or getattr(settings, "LOCAL_WHISPER_URL", "") or "http://localhost:9000"
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
        url = f"{self._base_url.rstrip('/')}/transcribe"
        attempts = self._max_retries + 1
        last_err: WhisperError | None = None

        for attempt in range(attempts):
            t0 = perf_counter()
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    files = {"audio": ("audio.webm", audio_handle, mime_type or "audio/webm")}
                    data = {"language": language, "request_id": request_id}
                    resp = await client.post(url, files=files, data=data)
                if resp.status_code >= 500:
                    raise WhisperError(
                        f"local 5xx {resp.status_code}",
                        kind="provider_5xx",
                        retryable=True,
                        provider=self.name,
                    )
                if resp.status_code >= 400:
                    raise WhisperError(
                        f"local 4xx {resp.status_code}",
                        kind="provider_4xx",
                        retryable=False,
                        provider=self.name,
                    )
                body = resp.json()
                return TranscriptionResult(
                    text=str(body.get("text", "")).strip(),
                    duration_seconds=float(body.get("duration", 0.0)),
                    confidence=(float(body["confidence"]) if "confidence" in body else None),
                    language_detected=body.get("language"),
                )
            except httpx.TimeoutException as e:
                last_err = WhisperError(
                    "local timeout",
                    kind="timeout",
                    retryable=True,
                    provider=self.name,
                )
                logger.warning(
                    "local_whisper_timeout",
                    extra={
                        "request_id": request_id,
                        "attempt": attempt + 1,
                        "latency_ms": int((perf_counter() - t0) * 1000),
                    },
                )
                if attempt + 1 >= attempts:
                    raise last_err from e
                await asyncio.sleep(0.5)
            except httpx.HTTPError as e:
                last_err = WhisperError("local network", kind="network", retryable=True, provider=self.name)
                if attempt + 1 >= attempts:
                    raise last_err from e
                await asyncio.sleep(0.5)
            except WhisperError as err:
                last_err = err
                if not err.retryable or attempt + 1 >= attempts:
                    raise
                await asyncio.sleep(0.5)
            except Exception as e:  # pragma: no cover
                raise WhisperError(
                    "local unknown", kind="malformed_response", retryable=False, provider=self.name
                ) from e

        assert last_err is not None  # pragma: no cover
        raise last_err
