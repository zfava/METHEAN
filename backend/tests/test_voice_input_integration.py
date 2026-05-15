"""Integration tests for the transcribe endpoint."""

import pathlib
from unittest.mock import AsyncMock, patch

import pytest

from app.models.identity import PersonalizationPolicy
from app.services.whisper.base import TranscriptionResult

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "audio"


def _mock_openai_text(text: str, duration: float = 2.0):
    return patch(
        "app.api.transcribe.get_whisper_client",
        AsyncMock(
            return_value=type(
                "P",
                (),
                {
                    "name": "openai",
                    "transcribe": AsyncMock(
                        return_value=TranscriptionResult(
                            text=text,
                            duration_seconds=duration,
                            confidence=None,
                            language_detected="en",
                        )
                    ),
                },
            )()
        ),
    )


@pytest.mark.asyncio
async def test_transcribe_happy_path(auth_client, child):
    data = (FIXTURES / "hello_2s.webm").read_bytes()
    with _mock_openai_text("hello there"):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["text"] == "hello there"
    assert body["safety_intervention"] is False
    assert body["provider"] == "openai"
    assert body["remaining_minutes"] >= 0


@pytest.mark.asyncio
async def test_transcribe_403_when_disabled(auth_client, db_session, household, child):
    db_session.add(PersonalizationPolicy(household_id=household.id, voice_input_enabled=False))
    await db_session.flush()
    data = (FIXTURES / "hello_2s.webm").read_bytes()
    with _mock_openai_text("hi"):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    assert resp.status_code == 403
    assert resp.json()["detail"]["error"] == "voice_input_disabled"


@pytest.mark.asyncio
async def test_transcribe_429_when_cap_reached(auth_client, db_session, household, child):
    db_session.add(PersonalizationPolicy(household_id=household.id, voice_minutes_daily_cap=0))
    await db_session.flush()
    data = (FIXTURES / "hello_2s.webm").read_bytes()
    with _mock_openai_text("hi"):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    assert resp.status_code == 429
    body = resp.json()["detail"]
    assert body["error"] == "voice_cap_reached"
    assert body["cap_minutes"] == 0
    assert "resets_at" in body


@pytest.mark.asyncio
async def test_transcribe_rejects_empty(auth_client, child):
    resp = await auth_client.post(
        f"/api/v1/children/{child.id}/transcribe",
        files={"audio": ("audio.webm", b"", "audio/webm")},
    )
    assert resp.status_code == 422
    assert resp.json()["detail"]["error"] == "audio_invalid"


@pytest.mark.asyncio
async def test_transcribe_rejects_oversized(auth_client, child):
    big = b"\x1a\x45\xdf\xa3" + b"x" * (26 * 1024 * 1024)
    resp = await auth_client.post(
        f"/api/v1/children/{child.id}/transcribe",
        files={"audio": ("audio.webm", big, "audio/webm")},
    )
    assert resp.status_code == 413


@pytest.mark.asyncio
async def test_transcribe_silence_flag(auth_client, child):
    data = (FIXTURES / "silence_5s.webm").read_bytes()
    with _mock_openai_text("", duration=5.0):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_silent"] is True
    assert body["text"] == ""


@pytest.mark.asyncio
async def test_transcribe_safety_intervention(auth_client, child):
    data = (FIXTURES / "hello_2s.webm").read_bytes()
    with _mock_openai_text("i hate everything"):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["safety_intervention"] is True
    assert body["intervention_kind"] == "distress_signal"
    # Crucial: the transcript itself is NOT returned to the kid.
    assert body["text"] == ""


@pytest.mark.asyncio
async def test_transcribe_audio_handle_not_persisted(auth_client, db_session, child):
    """No row in voice_usage_daily should ever carry audio bytes."""
    from sqlalchemy import text as sql_text

    data = (FIXTURES / "hello_2s.webm").read_bytes()
    with _mock_openai_text("hi"):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    assert resp.status_code == 200
    # The schema has no BYTEA / Text / JSONB column for audio. Verify
    # via information_schema that no such column was sneakily added.
    result = await db_session.execute(
        sql_text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'voice_usage_daily'")
    )
    cols = {row[0]: row[1] for row in result.all()}
    assert "audio_bytes" not in cols
    assert "audio" not in cols
    # Counter column is the only numeric storage.
    assert cols.get("stt_seconds_used") == "integer"


@pytest.mark.asyncio
async def test_transcribe_metrics_emit_on_success(auth_client, child):
    from app.core.observability import get_metric_snapshot, reset_metrics_for_tests

    reset_metrics_for_tests()
    data = (FIXTURES / "hello_2s.webm").read_bytes()
    with _mock_openai_text("hello there"):
        await auth_client.post(
            f"/api/v1/children/{child.id}/transcribe",
            files={"audio": ("audio.webm", data, "audio/webm")},
        )
    snap = get_metric_snapshot()
    success_keys = [
        k for k in snap["counters"] if k[0] == "voice_transcription_total" and dict(k[1]).get("outcome") == "success"
    ]
    assert success_keys, "voice_transcription_total{outcome=success} not emitted"
