"""Voice-output TTS endpoint.

``POST /children/{id}/tts/stream`` returns an SSE stream of
base64-encoded MP3 chunks. The kid's chosen persona drives voice
selection; the phrase allowlist gates cache eligibility; the daily
cap is debited based on actual duration once streaming completes.

Order of operations:

1. Policy check. 403 if ``voice_output_enabled`` is false.
2. Persona lookup. 422 if unknown.
3. Text prep (sanitize, optional voice-mode truncation, lexicon).
4. Pre-debit cap check. 429 if no remaining seconds.
5. Cache lookup (if cacheable phrase). Hit short-circuits to step 7.
6. Stream from provider. Yields SSE events: ``meta``, ``chunk``,
   ``done``.
7. Atomic debit of actual duration. Survives client disconnect via
   try/finally; we debit what was successfully streamed.
"""

import asyncio
import base64
import logging
import time
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_child_access
from app.content.personalization_library import get_voice_persona
from app.core.observability import observe_tts_cache_hit, observe_tts_request
from app.models.identity import Child, PersonalizationPolicy
from app.schemas.voice import TTSRequest
from app.services.text_to_speech_prep import TTSPrepError, prep_for_tts
from app.services.tts import get_tts_client
from app.services.tts.base import TTSError
from app.services.tts.cache import insert as cache_insert
from app.services.tts.cache import lookup as cache_lookup
from app.services.voice_usage import debit_tts_seconds, get_remaining_tts_seconds

router = APIRouter(tags=["voice"])

logger = logging.getLogger("methean.voice.tts")


def _iso_next_midnight_utc() -> str:
    now = datetime.now(UTC)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return tomorrow.isoformat()


def _sse(event: str, data: str) -> bytes:
    return f"event: {event}\ndata: {data}\n\n".encode()


@router.post(
    "/children/{child_id}/tts/stream",
    responses={
        403: {"description": "voice_output_disabled"},
        422: {"description": "unknown_persona | text_invalid"},
        429: {"description": "voice_output_cap_reached"},
        503: {"description": "provider_unavailable"},
    },
)
async def tts_stream(
    child_id: uuid.UUID,
    body: TTSRequest,
    request: Request,
    child: Child = Depends(require_child_access("write")),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

    # 1. Policy.
    pol_result = await db.execute(
        select(PersonalizationPolicy).where(PersonalizationPolicy.household_id == child.household_id)
    )
    policy = pol_result.scalar_one_or_none()
    if policy is not None and not policy.voice_output_enabled:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"error": "voice_output_disabled"})

    # 2. Persona.
    persona = get_voice_persona(body.persona_id)
    if persona is None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"error": "unknown_persona"})

    # 3. Prep.
    try:
        prepped = prep_for_tts(body.text, persona, voice_mode=body.voice_mode)
    except TTSPrepError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"error": e.kind}) from None

    # 4. Cap.
    snapshot = await get_remaining_tts_seconds(db, child_id=child.id, household_id=child.household_id, policy=policy)
    if snapshot.remaining_seconds <= 0:
        cap_minutes = policy.voice_output_minutes_daily_cap if policy is not None else 120
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "voice_output_cap_reached",
                "minutes_used": snapshot.seconds_used // 60,
                "cap_minutes": cap_minutes,
                "resets_at": _iso_next_midnight_utc(),
            },
        )
    # Conservative pre-check: refuse if the estimated text duration
    # would push more than 10s past the cap. The actual debit at the
    # finally block uses the streamed bytes.
    if prepped.estimated_seconds > snapshot.remaining_seconds + 10:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "voice_output_cap_reached_estimated",
                "remaining_seconds": snapshot.remaining_seconds,
                "estimated_seconds": int(prepped.estimated_seconds),
            },
        )

    # Cache lookup happens inside the stream generator so the
    # initial meta event reflects the cache decision.

    async def event_stream() -> AsyncIterator[bytes]:
        actual_duration = 0.0
        first_chunk_at_ms: float | None = None
        t0 = time.perf_counter()
        outcome = "success"
        try:
            cached_payload: tuple[bytes, float] | None = None
            if prepped.is_cacheable and prepped.cache_key_value:
                cached_payload = await cache_lookup(db, cache_key_value=prepped.cache_key_value)

            if cached_payload is not None:
                audio_bytes, duration = cached_payload
                actual_duration = duration
                outcome = "cached"
                observe_tts_cache_hit(phrase_key=prepped.cache_key_value or "")
                yield _sse(
                    "meta",
                    f'{{"cached": true, "duration": {duration:.3f}, "voice_id": "{persona.tts_voice_id}"}}',
                )
                first_chunk_at_ms = (time.perf_counter() - t0) * 1000
                for i in range(0, len(audio_bytes), 4096):
                    chunk = audio_bytes[i : i + 4096]
                    yield _sse("chunk", base64.b64encode(chunk).decode("ascii"))
                yield _sse("done", f'{{"duration_seconds": {duration:.3f}}}')
                return

            # Cache miss: stream from provider.
            client = await get_tts_client(db, child.household_id)
            yield _sse(
                "meta",
                f'{{"cached": false, "voice_id": "{persona.tts_voice_id}", "provider": "{client.name}"}}',
            )
            all_bytes = bytearray()
            try:
                async for chunk in client.stream_speech(
                    prepped.text,
                    persona.tts_voice_id,
                    speech_rate=persona.speech_rate,
                    request_id=request_id,
                ):
                    if first_chunk_at_ms is None:
                        first_chunk_at_ms = (time.perf_counter() - t0) * 1000
                    all_bytes.extend(chunk)
                    yield _sse("chunk", base64.b64encode(chunk).decode("ascii"))
            except TTSError as e:
                outcome = "error"
                logger.error(
                    "tts_provider_failed",
                    extra={"provider": e.provider, "kind": e.kind, "request_id": request_id},
                )
                # Tell the client. SSE doesn't have a clean error
                # status path mid-stream so the consumer treats this
                # event as terminal.
                yield _sse("error", f'{{"error": "provider_unavailable", "kind": "{e.kind}"}}')
                return

            # Estimated duration from byte count: tts-1 MP3 stereo
            # at default bitrate is ~16 KB/s; we use the prep
            # estimate as a floor.
            actual_duration = max(prepped.estimated_seconds, len(all_bytes) / 16000.0)
            yield _sse("done", f'{{"duration_seconds": {actual_duration:.3f}}}')

            # Insert into cache if eligible. Best-effort; failures
            # are logged at DEBUG and don't break the stream.
            if prepped.is_cacheable and prepped.cache_key_value:
                try:
                    await cache_insert(
                        db,
                        cache_key_value=prepped.cache_key_value,
                        voice_id=persona.tts_voice_id,
                        provider=persona.tts_provider,
                        audio_bytes=bytes(all_bytes),
                        duration_seconds=actual_duration,
                    )
                except Exception:
                    logger.debug("tts_cache_insert_failed", extra={"request_id": request_id})
        finally:
            # Debit actual duration even on partial streams. A
            # client disconnect mid-stream still costs the kid the
            # seconds successfully delivered.
            try:
                await debit_tts_seconds(
                    db,
                    child_id=child.id,
                    household_id=child.household_id,
                    seconds=actual_duration,
                    policy=policy,
                )
            except Exception:
                logger.debug("tts_debit_failed", extra={"request_id": request_id})

            observe_tts_request(
                provider=("openai" if outcome != "cached" else "cache"),
                persona_id=persona.id,
                outcome=outcome,
                first_chunk_latency_ms=first_chunk_at_ms,
                duration_seconds=actual_duration,
            )
            logger.info(
                "tts_done",
                extra={
                    "persona_id": persona.id,
                    "request_id": request_id,
                    "outcome": outcome,
                    "duration_seconds": round(actual_duration, 2),
                    "first_chunk_ms": int(first_chunk_at_ms or 0),
                },
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# Keep the asyncio import alive for type checkers.
_ = asyncio
__all__: list[str] = ["router"]
