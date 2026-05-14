"""TTS provider protocol."""

from collections.abc import AsyncIterator
from typing import Literal, Protocol


class TTSError(Exception):
    """Provider-side failure surfaced to the caller."""

    def __init__(
        self,
        message: str,
        *,
        kind: Literal["network", "timeout", "provider_5xx", "provider_4xx", "auth", "malformed_response"],
        retryable: bool,
        provider: str,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.retryable = retryable
        self.provider = provider


class TTSClient(Protocol):
    """Provider-agnostic text-to-speech client.

    ``stream_speech`` yields raw MP3 chunks. The endpoint base64-
    encodes each chunk into a server-sent event so the browser's
    streaming player can decode incrementally.
    """

    name: str

    async def stream_speech(
        self,
        text: str,
        voice_id: str,
        *,
        speech_rate: float,
        request_id: str,
    ) -> AsyncIterator[bytes]: ...
