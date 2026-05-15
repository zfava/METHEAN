"""Voice-input transcribe endpoint.

Audio bytes pass through memory only. The handle variable name is
``audio_handle`` (not ``audio_data`` or ``audio_bytes``) to signal
that it is a transient handle, not durable storage. It is dropped
immediately after the provider call returns; no audio appears in
logs or in any persisted column.

Order of operations (do not reorder without updating
``docs/runbooks/voice-input.md``):

1. Load policy. Reject with 403 if ``voice_input_enabled`` is false.
2. Read + validate audio (size, container, duration, silence).
3. Pre-debit cap check. 429 if no remaining seconds.
4. Resolve provider via factory (cloud or local with fallback).
5. Transcribe. 503 on provider failure after retry.
6. Atomic debit of actual duration. May cross the cap; we still
   return the transcript for THIS request and the next request 429s.
7. Safety check on transcript. May flip ``safety_intervention=true``.
8. Emit metrics. Return.
"""

import logging
import uuid
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_child_access
from app.core.audio_validation import AudioValidationError, validate_audio
from app.core.observability import (
    observe_safety_intervention,
    observe_transcription,
)
from app.models.identity import Child, PersonalizationPolicy
from app.schemas.voice import TranscribeResponse
from app.services.voice_safety import evaluate_transcript_safety
from app.services.voice_usage import debit_seconds, get_remaining_seconds
from app.services.whisper import WhisperError, get_whisper_client

router = APIRouter(tags=["voice"])

logger = logging.getLogger("methean.voice.transcribe")


@router.post(
    "/children/{child_id}/transcribe",
    response_model=TranscribeResponse,
    responses={
        403: {"description": "voice_input_disabled"},
        413: {"description": "audio_too_large"},
        415: {"description": "audio_unsupported_mime"},
        422: {"description": "audio_invalid | audio_too_long | audio_too_short"},
        429: {"description": "voice_cap_reached"},
        503: {"description": "provider_unavailable"},
    },
)
async def transcribe(
    child_id: uuid.UUID,
    request: Request,
    audio: UploadFile = File(...),
    child: Child = Depends(require_child_access("write")),
    db: AsyncSession = Depends(get_db),
) -> TranscribeResponse:
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

    # 1. Policy.
    result = await db.execute(
        select(PersonalizationPolicy).where(PersonalizationPolicy.household_id == child.household_id)
    )
    policy = result.scalar_one_or_none()
    voice_enabled = policy.voice_input_enabled if policy is not None else True
    if not voice_enabled:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"error": "voice_input_disabled"})

    # 2. Read + validate. audio_handle is a TRANSIENT bytes handle.
    audio_handle: bytes | None = await audio.read()
    try:
        validated = await validate_audio(audio_handle or b"", audio.content_type or "")
    except AudioValidationError as e:
        raise HTTPException(e.http_status, detail={"error": e.kind}) from None

    # 3. Pre-debit cap.
    snapshot = await get_remaining_seconds(db, child_id=child.id, household_id=child.household_id, policy=policy)
    if snapshot.remaining_seconds <= 0:
        cap_minutes = policy.voice_minutes_daily_cap if policy is not None else 60
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "voice_cap_reached",
                "minutes_used": snapshot.seconds_used // 60,
                "cap_minutes": cap_minutes,
                "resets_at": _iso_next_midnight_utc(),
            },
        )

    # 4. Resolve provider.
    client = await get_whisper_client(db, child.household_id)

    # 5. Transcribe.
    t0 = perf_counter()
    try:
        result_obj = await client.transcribe(
            audio_handle or b"",
            validated.mime_type,
            request_id=request_id,
        )
    except WhisperError as e:
        observe_transcription(
            provider=client.name,
            outcome="error",
            duration_seconds=validated.duration_seconds,
            latency_ms=(perf_counter() - t0) * 1000,
        )
        logger.error(
            "transcribe_provider_failed",
            extra={"provider": client.name, "kind": e.kind, "request_id": request_id},
        )
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "provider_unavailable"},
        ) from None
    finally:
        # Drop the audio handle explicitly. No persistence, no logging,
        # no further references after this point.
        audio_handle = None

    latency_ms = (perf_counter() - t0) * 1000

    # 6. Atomic debit. The debit may push past the cap; we still
    # return the current transcript, and the next request 429s.
    new_total, cap_breached = await debit_seconds(
        db,
        child_id=child.id,
        household_id=child.household_id,
        seconds=validated.duration_seconds,
        policy=policy,
    )

    # 7. Safety check.
    verdict = await evaluate_transcript_safety(db, child_id=child.id, transcript=result_obj.text)
    outcome = "safety_flag" if not verdict.safe else "success"

    # 8. Metrics.
    observe_transcription(
        provider=client.name,
        outcome=outcome,
        duration_seconds=validated.duration_seconds,
        latency_ms=latency_ms,
    )
    if verdict.intervention_kind:
        observe_safety_intervention(intervention_kind=verdict.intervention_kind)

    cap_minutes = policy.voice_minutes_daily_cap if policy is not None else 60
    remaining_minutes = max(0, (cap_minutes * 60 - new_total) // 60)

    logger.info(
        "transcribe_ok",
        extra={
            "provider": client.name,
            "latency_ms": int(latency_ms),
            "duration_seconds": round(validated.duration_seconds, 2),
            "request_id": request_id,
            "outcome": outcome,
            "cap_breached": cap_breached,
        },
    )

    return TranscribeResponse(
        text=result_obj.text if verdict.safe else "",
        duration_seconds=validated.duration_seconds,
        remaining_minutes=remaining_minutes,
        is_silent=validated.is_silent,
        safety_intervention=not verdict.safe,
        intervention_kind=verdict.intervention_kind,
        suggested_response=verdict.suggested_response,
        provider=client.name,  # type: ignore[arg-type]
    )


def _iso_next_midnight_utc() -> str:
    now = datetime.now(UTC)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return tomorrow.isoformat()


# Public surface for tests + the router import path.
__all__: list[str] = ["router"]


# Convenience helper for type-checking conformance.
_ = Any  # avoid unused-import warnings in some linters
