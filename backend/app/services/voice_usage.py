"""Per-child daily voice-usage counter service.

The transcribe endpoint debits seconds atomically via
INSERT ... ON CONFLICT DO UPDATE on the unique
``(child_id, usage_date)`` constraint. No SELECT-then-UPDATE; the
upsert is the only concurrency-safe path that holds under the
asyncio.gather(...) tests in test_voice_input_unit.py.

Daily rollover: requests use the household's timezone if known,
falling back to UTC. The runbook (``docs/runbooks/voice-input.md``)
documents that crossing midnight mid-request debits the day the
request started on, since the date is computed once at debit time.
"""

import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import PersonalizationPolicy, VoiceUsageDaily


@dataclass(frozen=True)
class UsageSnapshot:
    seconds_used: int
    cap_seconds: int

    @property
    def remaining_seconds(self) -> int:
        return max(0, self.cap_seconds - self.seconds_used)

    @property
    def cap_breached(self) -> bool:
        return self.seconds_used >= self.cap_seconds


def _today_in_tz(tz_name: str | None) -> date:
    """Resolve "today" against the household timezone, defaulting UTC."""
    if tz_name:
        try:
            return datetime.now(ZoneInfo(tz_name)).date()
        except Exception:
            pass
    return datetime.now(UTC).date()


async def get_remaining_seconds(
    db: AsyncSession,
    *,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    policy: PersonalizationPolicy | None,
    tz: str | None = None,
) -> UsageSnapshot:
    """Return today's usage snapshot without modifying any row."""
    cap_seconds = (policy.voice_minutes_daily_cap if policy is not None else 60) * 60
    today = _today_in_tz(tz)
    result = await db.execute(
        select(VoiceUsageDaily).where(
            VoiceUsageDaily.child_id == child_id,
            VoiceUsageDaily.usage_date == today,
        )
    )
    row = result.scalar_one_or_none()
    used = int(row.stt_seconds_used) if row is not None else 0
    return UsageSnapshot(seconds_used=used, cap_seconds=cap_seconds)


async def debit_seconds(
    db: AsyncSession,
    *,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    seconds: float,
    policy: PersonalizationPolicy | None,
    tz: str | None = None,
) -> tuple[int, bool]:
    """Atomically increment the day counter. Returns ``(new_total, cap_breached)``.

    The upsert resolves to ``new_total = old + ceil(seconds)``. Two
    concurrent callers in the same second each get a correct
    ``new_total`` because PostgreSQL serializes the ON CONFLICT path.
    """
    cap_seconds = (policy.voice_minutes_daily_cap if policy is not None else 60) * 60
    today = _today_in_tz(tz)
    debit = max(0, round(seconds))

    stmt = (
        pg_insert(VoiceUsageDaily)
        .values(
            child_id=child_id,
            household_id=household_id,
            usage_date=today,
            stt_seconds_used=debit,
        )
        .on_conflict_do_update(
            constraint="uq_voice_usage_daily_child_date",
            set_={
                "stt_seconds_used": VoiceUsageDaily.stt_seconds_used + debit,
            },
        )
        .returning(VoiceUsageDaily.stt_seconds_used)
    )
    result = await db.execute(stmt)
    new_total = int(result.scalar_one())
    return new_total, new_total >= cap_seconds


# ── Voice-output (TTS) counter ────────────────────────────────────


async def get_remaining_tts_seconds(
    db: AsyncSession,
    *,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    policy: PersonalizationPolicy | None,
    tz: str | None = None,
) -> UsageSnapshot:
    """Output counter snapshot, mirroring ``get_remaining_seconds`` but
    for the TTS cap."""
    cap_seconds = (policy.voice_output_minutes_daily_cap if policy is not None else 120) * 60
    today = _today_in_tz(tz)
    result = await db.execute(
        select(VoiceUsageDaily).where(
            VoiceUsageDaily.child_id == child_id,
            VoiceUsageDaily.usage_date == today,
        )
    )
    row = result.scalar_one_or_none()
    used = int(row.tts_seconds_used) if row is not None else 0
    return UsageSnapshot(seconds_used=used, cap_seconds=cap_seconds)


async def debit_tts_seconds(
    db: AsyncSession,
    *,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    seconds: float,
    policy: PersonalizationPolicy | None,
    tz: str | None = None,
) -> tuple[int, bool]:
    """Atomically increment the day's TTS counter."""
    cap_seconds = (policy.voice_output_minutes_daily_cap if policy is not None else 120) * 60
    today = _today_in_tz(tz)
    debit = max(0, round(seconds))

    stmt = (
        pg_insert(VoiceUsageDaily)
        .values(
            child_id=child_id,
            household_id=household_id,
            usage_date=today,
            tts_seconds_used=debit,
        )
        .on_conflict_do_update(
            constraint="uq_voice_usage_daily_child_date",
            set_={
                "tts_seconds_used": VoiceUsageDaily.tts_seconds_used + debit,
            },
        )
        .returning(VoiceUsageDaily.tts_seconds_used)
    )
    result = await db.execute(stmt)
    new_total = int(result.scalar_one())
    return new_total, new_total >= cap_seconds
