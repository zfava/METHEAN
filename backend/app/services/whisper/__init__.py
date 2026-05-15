"""Whisper STT provider abstraction.

Two implementations:

- :mod:`app.services.whisper.openai_provider` calls OpenAI's hosted
  ``whisper-1`` API.
- :mod:`app.services.whisper.local_provider` calls a self-hosted
  faster-whisper service (Mac mini cluster) exposing the same
  request/response shape.

The factory picks per-household based on
``PersonalizationPolicy.whisper_provider``.
"""

from app.services.whisper.base import (
    TranscriptionResult,
    WhisperClient,
    WhisperError,
)
from app.services.whisper.factory import get_whisper_client

__all__ = [
    "TranscriptionResult",
    "WhisperClient",
    "WhisperError",
    "get_whisper_client",
]
