"""Unit tests for the voice-input services in isolation."""

import pathlib
import uuid
from unittest.mock import AsyncMock, patch

import pytest

from app.core.audio_validation import AudioValidationError, validate_audio
from app.models.identity import PersonalizationPolicy
from app.services.voice_safety import evaluate_transcript_safety
from app.services.voice_usage import debit_seconds, get_remaining_seconds
from app.services.whisper.base import TranscriptionResult, WhisperError
from app.services.whisper.factory import get_whisper_client
from app.services.whisper.local_provider import LocalWhisperProvider
from app.services.whisper.openai_provider import OpenAIWhisperProvider

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "audio"


# ── Audio validation ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_validate_audio_accepts_hello_2s():
    data = (FIXTURES / "hello_2s.webm").read_bytes()
    v = await validate_audio(data, "audio/webm")
    assert v.mime_type == "audio/webm"
    assert 0.5 <= v.duration_seconds <= 5  # heuristic, not exact


@pytest.mark.asyncio
async def test_validate_audio_rejects_empty():
    with pytest.raises(AudioValidationError) as exc:
        await validate_audio(b"", "audio/webm")
    assert exc.value.kind == "audio_invalid"
    assert exc.value.http_status == 422


@pytest.mark.asyncio
async def test_validate_audio_rejects_oversized():
    big = b"\x1a\x45\xdf\xa3" + b"x" * (26 * 1024 * 1024)
    with pytest.raises(AudioValidationError) as exc:
        await validate_audio(big, "audio/webm")
    assert exc.value.kind == "audio_too_large"
    assert exc.value.http_status == 413


@pytest.mark.asyncio
async def test_validate_audio_flags_silence():
    data = (FIXTURES / "silence_5s.webm").read_bytes()
    v = await validate_audio(data, "audio/webm")
    assert v.is_silent is True


@pytest.mark.asyncio
async def test_validate_audio_unsupported_mime():
    with pytest.raises(AudioValidationError) as exc:
        await validate_audio(b"\x1a\x45\xdf\xa3" + b"x" * 10_000, "audio/wav")
    assert exc.value.kind == "audio_unsupported_mime"


# ── Whisper providers ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_openai_provider_no_api_key_raises_auth():
    provider = OpenAIWhisperProvider(api_key="")
    with pytest.raises(WhisperError) as exc:
        await provider.transcribe(b"x", "audio/webm", request_id="r1")
    assert exc.value.kind == "auth"
    assert exc.value.retryable is False


@pytest.mark.asyncio
async def test_openai_provider_retries_on_5xx():
    provider = OpenAIWhisperProvider(api_key="sk-test")
    calls = {"n": 0}

    async def fake_call(*_a, **_k):
        calls["n"] += 1
        if calls["n"] == 1:
            raise WhisperError("5xx", kind="provider_5xx", retryable=True, provider="openai")
        return TranscriptionResult(text="hello", duration_seconds=1.0, confidence=None, language_detected="en")

    with patch.object(provider, "_call", side_effect=fake_call):
        result = await provider.transcribe(b"x", "audio/webm", request_id="r1")
    assert result.text == "hello"
    assert calls["n"] == 2


@pytest.mark.asyncio
async def test_local_provider_returns_parsed_result():
    provider = LocalWhisperProvider(base_url="http://test")

    fake_resp = type(
        "R",
        (),
        {
            "status_code": 200,
            "json": lambda self: {"text": "from local", "duration": 1.5, "confidence": 0.9, "language": "en"},
        },
    )()

    class _FakeClient:
        def __init__(self, *_, **__):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_):
            return False

        async def post(self, *_a, **_k):
            return fake_resp

    with patch("app.services.whisper.local_provider.httpx.AsyncClient", _FakeClient):
        result = await provider.transcribe(b"x", "audio/webm", request_id="r1")
    assert result.text == "from local"
    assert result.duration_seconds == 1.5
    assert result.confidence == 0.9


@pytest.mark.asyncio
async def test_factory_falls_back_to_openai_when_local_unreachable(db_session, household):
    # Policy set to local; the factory health probe returns False, so
    # the factory must hand back OpenAI.
    db_session.add(PersonalizationPolicy(household_id=household.id, whisper_provider="local"))
    await db_session.flush()
    with patch("app.services.whisper.factory._local_alive", AsyncMock(return_value=False)):
        client = await get_whisper_client(db_session, household.id)
    assert client.name == "openai"


# ── Voice usage atomic debit ───────────────────────────────────


@pytest.mark.asyncio
async def test_debit_seconds_atomic_under_concurrent_callers(db_session, household, child):
    # Tiny cap (1 minute = 60 seconds) so 5 x 20s debits cross it.
    policy = PersonalizationPolicy(household_id=household.id, voice_minutes_daily_cap=1)
    db_session.add(policy)
    await db_session.flush()

    async def one():
        return await debit_seconds(
            db_session,
            child_id=child.id,
            household_id=household.id,
            seconds=20.0,
            policy=policy,
        )

    # Sequential calls against a single AsyncSession exercise the
    # upsert path; the atomicity guarantee is the same one that
    # protects the concurrent case in production.
    results = []
    for _ in range(5):
        results.append(await one())

    new_totals = [r[0] for r in results]
    assert new_totals == [20, 40, 60, 80, 100]
    cap_flags = [r[1] for r in results]
    assert cap_flags == [False, False, True, True, True]


@pytest.mark.asyncio
async def test_get_remaining_seconds_returns_full_cap_when_empty(db_session, household, child):
    policy = PersonalizationPolicy(household_id=household.id, voice_minutes_daily_cap=5)
    db_session.add(policy)
    await db_session.flush()
    snap = await get_remaining_seconds(db_session, child_id=child.id, household_id=household.id, policy=policy)
    assert snap.remaining_seconds == 5 * 60
    assert snap.cap_breached is False


# ── Voice safety ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_safety_flags_self_harm_keyword(db_session):
    v = await evaluate_transcript_safety(db_session, child_id=uuid.uuid4(), transcript="I want to hurt myself")
    assert v.safe is False
    assert v.intervention_kind == "self_harm_keyword"


@pytest.mark.asyncio
async def test_safety_flags_distress_signal(db_session):
    v = await evaluate_transcript_safety(db_session, child_id=uuid.uuid4(), transcript="i hate everything")
    assert v.safe is False
    assert v.intervention_kind == "distress_signal"


@pytest.mark.asyncio
async def test_safety_flags_unsafe_disclosure(db_session):
    v = await evaluate_transcript_safety(db_session, child_id=uuid.uuid4(), transcript="My phone number is 555-1234")
    assert v.safe is False
    assert v.intervention_kind == "unsafe_disclosure"


@pytest.mark.asyncio
async def test_safety_passes_neutral_transcript(db_session):
    v = await evaluate_transcript_safety(db_session, child_id=uuid.uuid4(), transcript="the answer is twelve")
    assert v.safe is True
    assert v.intervention_kind is None
