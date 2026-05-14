"""Unit tests for the TTS prep, allowlist, and cache services."""

import pytest

from app.content.personalization_library import get_voice_persona
from app.models.tts_cache import TTSCache
from app.services.text_to_speech_prep import TTSPrepError, prep_for_tts
from app.services.tts.cache import insert as cache_insert
from app.services.tts.cache import lookup as cache_lookup
from app.services.tts.phrase_allowlist import (
    CACHEABLE_PHRASES,
    cache_key,
    is_cacheable,
    normalize_phrase,
)


# ── phrase_allowlist ───────────────────────────────────────────


def test_normalize_strips_case_punct_whitespace():
    assert normalize_phrase("  Good Thinking. ") == "good thinking"
    assert normalize_phrase("Good   thinking!") == "good thinking"


def test_is_cacheable_known_phrase():
    assert is_cacheable("Good Thinking") is True


def test_is_cacheable_unknown_phrase():
    assert is_cacheable("Hey Atlas, the answer is 12") is False


def test_cache_key_is_stable_across_typography():
    k1 = cache_key("Good thinking.", "nova", "openai")
    k2 = cache_key("  good   THINKING  ", "nova", "openai")
    assert k1 == k2


def test_allowlist_has_at_least_50_phrases():
    assert len(CACHEABLE_PHRASES) >= 50


# ── prep_for_tts ───────────────────────────────────────────────


def test_prep_rejects_empty():
    persona = get_voice_persona("default_warm")
    assert persona is not None
    with pytest.raises(TTSPrepError) as exc:
        prep_for_tts("", persona)
    assert exc.value.kind == "text_empty"


def test_prep_rejects_tag_like():
    persona = get_voice_persona("default_warm")
    assert persona is not None
    with pytest.raises(TTSPrepError) as exc:
        prep_for_tts("hello <break time='500ms'/> world", persona)
    assert exc.value.kind == "text_has_tags"


def test_prep_truncates_in_voice_mode():
    persona = get_voice_persona("default_warm")
    assert persona is not None
    long = "First sentence. Second sentence. Third sentence. Fourth sentence."
    prepped = prep_for_tts(long, persona, voice_mode=True)
    # At most 2 sentences. The prep keeps the first two.
    assert "Third" not in prepped.text
    assert "Fourth" not in prepped.text


def test_prep_applies_lexicon_methean():
    persona = get_voice_persona("default_warm")
    assert persona is not None
    prepped = prep_for_tts("Welcome to METHEAN", persona)
    assert "Meth-ee-an" in prepped.text


def test_prep_marks_cacheable_for_allowlisted_phrase():
    persona = get_voice_persona("default_warm")
    assert persona is not None
    prepped = prep_for_tts("Good thinking", persona)
    assert prepped.is_cacheable is True
    assert prepped.cache_key_value is not None


def test_prep_marks_not_cacheable_for_personalized():
    persona = get_voice_persona("default_warm")
    assert persona is not None
    prepped = prep_for_tts("Hey Sage, twelve is the answer", persona)
    assert prepped.is_cacheable is False
    assert prepped.cache_key_value is None


# ── tts cache ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_cache_roundtrip(db_session):
    key = cache_key("good thinking", "nova", "openai")
    audio = b"fake-mp3-bytes" * 100
    await cache_insert(
        db_session,
        cache_key_value=key,
        voice_id="nova",
        provider="openai",
        audio_bytes=audio,
        duration_seconds=1.2,
    )
    hit = await cache_lookup(db_session, cache_key_value=key)
    assert hit is not None
    bytes_out, duration = hit
    assert bytes_out == audio
    assert duration == pytest.approx(1.2, rel=1e-3)


@pytest.mark.asyncio
async def test_cache_lookup_miss_returns_none(db_session):
    res = await cache_lookup(db_session, cache_key_value="missing-key-deadbeef")
    assert res is None


# ── persona TTS fields populated ────────────────────────────────


def test_all_personas_have_tts_fields():
    for persona_id in ["default_warm", "default_bright", "default_steady", "default_playful", "default_gentle"]:
        p = get_voice_persona(persona_id)
        assert p is not None
        assert p.tts_voice_id, f"{persona_id} missing tts_voice_id"
        assert p.tts_provider in {"openai", "elevenlabs"}
        assert 0.5 <= p.speech_rate <= 1.5
        assert p.prosody_hints, f"{persona_id} missing prosody_hints"


# Keep model imported for IDE / test discovery.
_ = TTSCache
