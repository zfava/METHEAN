"""Whisper provider protocol.

The contract is provider-agnostic so we can route a household to
OpenAI's cloud or a local faster-whisper service without the
transcribe endpoint having to know which one ran.
"""

from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class TranscriptionResult:
    """One transcription, regardless of provider."""

    text: str
    duration_seconds: float
    confidence: float | None
    language_detected: str | None


class WhisperError(Exception):
    """Provider-side failure surfaced to the caller.

    ``kind`` is a stable string the API layer maps to HTTP status
    and the operator-facing log. ``retryable`` lets the caller
    decide whether to back off and try again.
    """

    def __init__(
        self,
        message: str,
        *,
        kind: Literal["network", "timeout", "provider_5xx", "provider_4xx", "malformed_response", "auth"],
        retryable: bool,
        provider: str,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.retryable = retryable
        self.provider = provider


class WhisperClient(Protocol):
    """Provider-agnostic transcription client."""

    name: str

    async def transcribe(
        self,
        audio_handle: bytes,
        mime_type: str,
        *,
        language: str = "en",
        request_id: str,
    ) -> TranscriptionResult:
        """Transcribe ``audio_handle`` and return a result.

        ``audio_handle`` is a transient bytes object held in memory
        only. Providers MUST NOT write it to disk, log it, or include
        it in error responses.
        """
        ...
