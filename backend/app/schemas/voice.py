"""Pydantic schemas for the voice API.

Voice input (STT) lands in migration 044; voice output (TTS) extends
this module in migration 045.
"""

from typing import Literal

from pydantic import BaseModel, Field


class TranscribeResponse(BaseModel):
    """Successful transcription envelope.

    ``text`` is empty when the response is a safety intervention; the
    caller surfaces a wellbeing UI instead of writing the transcript
    into the kid's textarea.
    """

    text: str
    duration_seconds: float
    remaining_minutes: int
    is_silent: bool = False
    safety_intervention: bool = False
    intervention_kind: str | None = None
    suggested_response: str | None = None
    provider: Literal["openai", "local"]


class VoiceCapErrorDetail(BaseModel):
    """Structured 429 body for cap-reached responses."""

    error: Literal["voice_cap_reached"] = "voice_cap_reached"
    minutes_used: int = Field(ge=0)
    cap_minutes: int = Field(ge=0)
    resets_at: str  # ISO-8601 midnight in the household's tz (or UTC)
