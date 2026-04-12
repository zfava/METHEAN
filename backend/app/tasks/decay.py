"""Nightly decay batch job (Section 5.4).

For every active FSRSCard where due < now():
- Compute retrievability using FSRS formula
- If retrievability < threshold, transition mastered -> in_progress
- Emit StateEvent with trigger='decay'

Must be idempotent (safe to run twice).
"""

import asyncio
import time
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.enums import MasteryLevel, StateEventType
from app.models.state import ChildNodeState, FSRSCard, StateEvent
from app.services.state_engine import compute_retrievability, emit_state_event


async def run_decay_batch(
    session_factory: async_sessionmaker | None = None,
) -> dict:
    """Run the decay batch job. Returns stats dict.

    Can be called directly (for testing) or via Celery task.
    """
    start_time = time.monotonic()
    now = datetime.now(UTC)

    # Create engine if not provided (Celery context)
    if session_factory is None:
        engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    cards_checked = 0
    cards_decayed = 0

    async with session_factory() as db:
        # Batch fetch overdue FSRS cards that are linked to mastered nodes
        # Join with ChildNodeState to only check mastered nodes
        offset = 0
        batch_size = settings.DECAY_BATCH_SIZE

        while True:
            result = await db.execute(
                select(FSRSCard)
                .where(
                    FSRSCard.due < now,
                    FSRSCard.stability > 0,
                    FSRSCard.last_review.isnot(None),
                )
                .offset(offset)
                .limit(batch_size)
            )
            cards = result.scalars().all()

            if not cards:
                break

            for card in cards:
                cards_checked += 1

                # Check if this node is currently mastered
                state_result = await db.execute(
                    select(ChildNodeState).where(
                        ChildNodeState.child_id == card.child_id,
                        ChildNodeState.household_id == card.household_id,
                        ChildNodeState.node_id == card.node_id,
                        ChildNodeState.mastery_level == MasteryLevel.mastered,
                    )
                )
                node_state = state_result.scalar_one_or_none()

                if not node_state:
                    continue  # Not mastered, skip

                # Compute retrievability
                retrievability = compute_retrievability(card, now)
                if retrievability is None:
                    continue

                if retrievability < settings.DECAY_RETRIEVABILITY_THRESHOLD:
                    # Check idempotency: don't decay if already decayed in this run
                    # (look for a recent decay event for this node)
                    recent_decay = await db.execute(
                        select(StateEvent.id)
                        .where(
                            StateEvent.child_id == card.child_id,
                            StateEvent.node_id == card.node_id,
                            StateEvent.event_type == StateEventType.mastery_change,
                            StateEvent.trigger == "decay",
                            StateEvent.to_state == MasteryLevel.proficient.value,
                            StateEvent.created_at > now.replace(hour=0, minute=0, second=0),
                        )
                        .limit(1)
                    )
                    if recent_decay.scalar_one_or_none():
                        continue  # Already decayed today

                    # Transition: mastered -> proficient
                    node_state.mastery_level = MasteryLevel.proficient

                    await emit_state_event(
                        db,
                        card.child_id,
                        card.household_id,
                        card.node_id,
                        event_type=StateEventType.mastery_change,
                        from_state=MasteryLevel.mastered.value,
                        to_state=MasteryLevel.proficient.value,
                        trigger="decay",
                        metadata={
                            "retrievability": round(retrievability, 4),
                            "threshold": settings.DECAY_RETRIEVABILITY_THRESHOLD,
                            "fsrs_stability": card.stability,
                            "days_overdue": (now - card.due).total_seconds() / 86400 if card.due else 0,
                        },
                    )
                    cards_decayed += 1

            offset += batch_size
            await db.flush()

        await db.commit()

    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    return {
        "cards_checked": cards_checked,
        "cards_decayed": cards_decayed,
        "duration_ms": elapsed_ms,
    }


def run_decay_sync() -> dict:
    """Synchronous wrapper for Celery."""
    return asyncio.run(run_decay_batch())
