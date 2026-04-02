"""Weekly snapshot capture and alert detection tasks."""

import asyncio
import time
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.curriculum import ChildMapEnrollment, LearningNode
from app.models.enums import MasteryLevel
from app.models.evidence import WeeklySnapshot
from app.models.identity import Child
from app.models.state import ChildNodeState


async def capture_weekly_snapshots(
    session_factory: async_sessionmaker | None = None,
) -> dict:
    """Capture weekly snapshot for every active child enrollment."""
    start = time.monotonic()

    if session_factory is None:
        engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    snapshots_created = 0

    async with session_factory() as db:
        # Get all active children
        children_result = await db.execute(select(Child).where(Child.is_active == True))  # noqa: E712
        children = children_result.scalars().all()

        for child in children:
            # Check if snapshot already exists for this week
            existing = await db.execute(
                select(WeeklySnapshot.id).where(
                    WeeklySnapshot.child_id == child.id,
                    WeeklySnapshot.week_start == week_start,
                ).limit(1)
            )
            if existing.scalar_one_or_none():
                continue

            # Get states
            states_result = await db.execute(
                select(ChildNodeState).where(
                    ChildNodeState.child_id == child.id,
                    ChildNodeState.household_id == child.household_id,
                )
            )
            states = states_result.scalars().all()

            mastered = sum(1 for s in states if s.mastery_level == MasteryLevel.mastered)
            in_progress = sum(1 for s in states if s.mastery_level not in (
                MasteryLevel.mastered, MasteryLevel.not_started
            ))
            total_minutes = sum(s.time_spent_minutes or 0 for s in states)
            total_attempts = sum(s.attempts_count or 0 for s in states)

            snapshot = WeeklySnapshot(
                household_id=child.household_id,
                child_id=child.id,
                week_start=week_start,
                week_end=week_end,
                total_minutes=total_minutes,
                activities_completed=total_attempts,
                nodes_mastered=mastered,
                nodes_progressed=in_progress,
                summary={
                    "total_states": len(states),
                    "mastered": mastered,
                    "in_progress": in_progress,
                },
            )
            db.add(snapshot)
            snapshots_created += 1

        await db.commit()

    elapsed_ms = int((time.monotonic() - start) * 1000)
    return {"snapshots_created": snapshots_created, "duration_ms": elapsed_ms}


def run_snapshots_sync() -> dict:
    return asyncio.run(capture_weekly_snapshots())
