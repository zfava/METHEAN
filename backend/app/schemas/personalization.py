"""Pydantic v2 schemas for the personalization API.

Validation against the personalization library happens at the API
layer rather than the schema layer so that adding a new library entry
does not require a schema redeploy. Schemas only enforce shape and
basic length/range constraints.
"""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

# ── Per-child profile ─────────────────────────────────────────────


class ChildPersonalizationRead(BaseModel):
    child_id: UUID
    companion_name: str
    companion_voice: str
    vibe: str
    iconography_pack: str
    sound_pack: str
    affirmation_tone: str
    interest_tags: list[str]
    out_of_policy: list[str]
    onboarded: bool


class ChildPersonalizationUpdate(BaseModel):
    companion_name: str | None = Field(default=None, min_length=1, max_length=30)
    companion_voice: str | None = None
    vibe: str | None = None
    iconography_pack: str | None = None
    sound_pack: str | None = None
    affirmation_tone: str | None = None
    interest_tags: list[str] | None = None
    onboarded: bool | None = None


# ── Household policy ──────────────────────────────────────────────


class PersonalizationPolicyRead(BaseModel):
    allowed_vibes: list[str]
    allowed_interest_tags: list[str]
    allowed_voice_personas: list[str]
    allowed_iconography_packs: list[str]
    allowed_sound_packs: list[str]
    allowed_affirmation_tones: list[str]
    companion_name_requires_review: bool
    max_interest_tags_per_child: int
    # Voice-input governance (migration 044).
    voice_input_enabled: bool = True
    voice_minutes_daily_cap: int = 60
    whisper_provider: Literal["openai", "local"] = "openai"
    # Voice-output governance (migration 045).
    voice_output_enabled: bool = True
    voice_output_minutes_daily_cap: int = 120
    tts_provider: Literal["openai", "elevenlabs"] = "openai"


class PersonalizationPolicyUpdate(BaseModel):
    """Partial-update payload.

    Each list field may be ``["*"]`` (sentinel for "all from the
    library") or an explicit list of valid library IDs. Unknown IDs
    are rejected at the API layer with 400.
    """

    allowed_vibes: list[str] | None = None
    allowed_interest_tags: list[str] | None = None
    allowed_voice_personas: list[str] | None = None
    allowed_iconography_packs: list[str] | None = None
    allowed_sound_packs: list[str] | None = None
    allowed_affirmation_tones: list[str] | None = None
    companion_name_requires_review: bool | None = None
    max_interest_tags_per_child: int | None = Field(default=None, ge=1, le=15)
    # Voice-input governance (migration 044).
    voice_input_enabled: bool | None = None
    voice_minutes_daily_cap: int | None = Field(default=None, ge=0, le=480)
    whisper_provider: Literal["openai", "local"] | None = None
    # Voice-output governance (migration 045).
    voice_output_enabled: bool | None = None
    voice_output_minutes_daily_cap: int | None = Field(default=None, ge=0, le=600)
    tts_provider: Literal["openai", "elevenlabs"] | None = None


# ── Library views ─────────────────────────────────────────────────


class VibeEntry(BaseModel):
    id: str
    label: str
    description: str
    tokens: dict[str, str]
    available: bool


class InterestTagEntry(BaseModel):
    id: str
    label: str
    category: str
    icon_keyword: str
    available: bool


class VoicePersonaEntry(BaseModel):
    id: str
    label: str
    default_companion_name: str
    tone_summary: str
    available: bool


class IconographyPackEntry(BaseModel):
    id: str
    label: str
    description: str
    icons: dict[str, str]
    available: bool


class SoundPackEntry(BaseModel):
    id: str
    label: str
    description: str
    cues: dict[str, str | None]
    available: bool


class AffirmationToneEntry(BaseModel):
    id: str
    label: str
    tone_summary: str
    available: bool


class PersonalizationLibraryRead(BaseModel):
    vibes: list[VibeEntry]
    interest_tags: list[InterestTagEntry]
    voice_personas: list[VoicePersonaEntry]
    iconography_packs: list[IconographyPackEntry]
    sound_packs: list[SoundPackEntry]
    affirmation_tones: list[AffirmationToneEntry]
    max_interest_tags_per_child: int
