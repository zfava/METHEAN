"""Learner State Engine (System 2).

Manages ChildNodeState transitions, FSRS integration, cascade unblocking,
and state event emission. Every state change is immutable and auditable.
"""

import uuid
from datetime import UTC, datetime

from fsrs import Card as FSRSCardObj, Rating, Scheduler, State as FSRSState
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.curriculum import LearningEdge
from app.models.enums import (
    EdgeRelation,
    MasteryLevel,
    StateEventType,
)
from app.models.identity import Child
from app.models.state import ChildNodeState, FSRSCard, ReviewLog, StateEvent


def _get_scheduler(weights: list[float] | None = None) -> Scheduler:
    """Get FSRS Scheduler instance, optionally with personalized weights.

    The Scheduler constructor accepts `parameters` as a Sequence[float]
    (the 21 FSRS weights). When personalized weights are available from
    the child's optimization history, they are used instead of defaults.
    """
    if weights and len(weights) == 21:
        return Scheduler(parameters=weights)
    return Scheduler()


def confidence_to_rating(confidence: float) -> Rating:
    """Map evaluator confidence (0-1) to FSRS rating per Section 5.1.

    0.0 - 0.3  => Again (1)
    0.3 - 0.5  => Hard (2)
    0.5 - 0.8  => Good (3)
    0.8 - 1.0  => Easy (4)
    """
    if confidence < 0.3:
        return Rating.Again
    elif confidence < 0.5:
        return Rating.Hard
    elif confidence < 0.8:
        return Rating.Good
    else:
        return Rating.Easy


def _mastery_from_confidence(confidence: float, current: MasteryLevel) -> MasteryLevel:
    """Determine mastery level from confidence score."""
    if confidence >= settings.MASTERY_THRESHOLD:
        return MasteryLevel.mastered
    elif confidence >= 0.6:
        return MasteryLevel.proficient
    elif confidence >= 0.4:
        return MasteryLevel.developing
    elif confidence >= 0.2:
        return MasteryLevel.emerging
    else:
        if current == MasteryLevel.not_started:
            return MasteryLevel.emerging
        return current


async def get_or_create_node_state(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
) -> ChildNodeState:
    """Get existing ChildNodeState or create a new one."""
    result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
            ChildNodeState.node_id == node_id,
        )
    )
    state = result.scalar_one_or_none()
    if state:
        return state

    state = ChildNodeState(
        child_id=child_id,
        household_id=household_id,
        node_id=node_id,
        mastery_level=MasteryLevel.not_started,
    )
    db.add(state)
    await db.flush()
    return state


async def emit_state_event(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
    event_type: StateEventType,
    from_state: str,
    to_state: str,
    trigger: str,
    metadata: dict | None = None,
    created_by: uuid.UUID | None = None,
) -> StateEvent:
    """Append an immutable StateEvent."""
    event = StateEvent(
        child_id=child_id,
        household_id=household_id,
        node_id=node_id,
        event_type=event_type,
        from_state=from_state,
        to_state=to_state,
        trigger=trigger,
        metadata_=metadata or {},
        created_by=created_by,
    )
    db.add(event)
    await db.flush()
    return event


async def get_or_create_fsrs_card(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
) -> FSRSCard:
    """Get existing FSRSCard or create a new one."""
    result = await db.execute(
        select(FSRSCard).where(
            FSRSCard.child_id == child_id,
            FSRSCard.household_id == household_id,
            FSRSCard.node_id == node_id,
        )
    )
    card = result.scalar_one_or_none()
    if card:
        return card

    card = FSRSCard(
        child_id=child_id,
        household_id=household_id,
        node_id=node_id,
    )
    db.add(card)
    await db.flush()
    return card


def _db_card_to_fsrs(db_card: FSRSCard) -> FSRSCardObj:
    """Convert DB FSRSCard to py-fsrs Card for computation."""
    card = FSRSCardObj()
    if db_card.stability and db_card.stability > 0:
        card.stability = db_card.stability
    if db_card.difficulty and db_card.difficulty > 0:
        card.difficulty = db_card.difficulty
    card.state = FSRSState(db_card.state) if db_card.state else FSRSState.Learning
    if db_card.due:
        card.due = db_card.due
    if db_card.last_review:
        card.last_review = db_card.last_review
    return card


def _fsrs_card_to_db(fsrs_card: FSRSCardObj, db_card: FSRSCard) -> None:
    """Update DB FSRSCard from py-fsrs Card after review."""
    db_card.stability = fsrs_card.stability or 0.0
    db_card.difficulty = fsrs_card.difficulty or 0.0
    db_card.state = fsrs_card.state.value if hasattr(fsrs_card.state, 'value') else int(fsrs_card.state)
    db_card.due = fsrs_card.due
    db_card.last_review = fsrs_card.last_review
    # Compute scheduled_days from due and last_review
    if fsrs_card.due and fsrs_card.last_review:
        delta = (fsrs_card.due - fsrs_card.last_review).total_seconds() / 86400
        db_card.scheduled_days = max(0, int(delta))
    db_card.reps = (db_card.reps or 0) + 1


async def process_review(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
    confidence: float,
    duration_minutes: int | None = None,
    created_by: uuid.UUID | None = None,
) -> dict:
    """Process an attempt review: update FSRS card, node state, emit events.

    Returns dict with: mastery_level, previous_mastery, fsrs_due, fsrs_rating,
    state_event_id, nodes_unblocked.
    """
    now = datetime.now(UTC)
    rating = confidence_to_rating(confidence)

    # 1. Get or create FSRS card
    db_card = await get_or_create_fsrs_card(db, child_id, household_id, node_id)

    # 2. Run FSRS review (use personalized weights if available)
    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child_obj = child_result.scalar_one_or_none()
    weights = child_obj.fsrs_weights if child_obj else None
    scheduler = _get_scheduler(weights)
    fsrs_card = _db_card_to_fsrs(db_card)
    updated_card, review_log_entry = scheduler.review_card(fsrs_card, rating, now)

    # 3. Update DB card
    _fsrs_card_to_db(updated_card, db_card)
    db_card.last_review = now
    await db.flush()

    # 4. Append ReviewLog
    scheduled_days = db_card.scheduled_days or 0
    review_log = ReviewLog(
        card_id=db_card.id,
        child_id=child_id,
        household_id=household_id,
        rating=rating.value,
        scheduled_days=scheduled_days,
        elapsed_days=db_card.elapsed_days or 0,
        review_duration_ms=(duration_minutes * 60 * 1000) if duration_minutes else None,
    )
    db.add(review_log)

    # 5. Update ChildNodeState
    node_state = await get_or_create_node_state(db, child_id, household_id, node_id)
    previous_mastery = node_state.mastery_level
    new_mastery = _mastery_from_confidence(confidence, previous_mastery)

    node_state.mastery_level = new_mastery
    node_state.attempts_count += 1
    node_state.last_activity_at = now
    if duration_minutes:
        node_state.time_spent_minutes += duration_minutes

    # 6. Emit StateEvent
    event_type = StateEventType.review_completed
    if new_mastery != previous_mastery:
        event_type = StateEventType.mastery_change

    state_event = await emit_state_event(
        db, child_id, household_id, node_id,
        event_type=event_type,
        from_state=previous_mastery.value if hasattr(previous_mastery, 'value') else str(previous_mastery),
        to_state=new_mastery.value if hasattr(new_mastery, 'value') else str(new_mastery),
        trigger="attempt",
        metadata={
            "confidence": confidence,
            "rating": rating.value,
            "fsrs_stability": updated_card.stability,
            "fsrs_due": updated_card.due.isoformat() if updated_card.due else None,
        },
        created_by=created_by,
    )

    await db.flush()

    # 7. Cascade unblock if node just mastered
    nodes_unblocked: list[uuid.UUID] = []
    if new_mastery == MasteryLevel.mastered and previous_mastery != MasteryLevel.mastered:
        nodes_unblocked = await _cascade_unblock(
            db, child_id, household_id, node_id
        )

    return {
        "mastery_level": new_mastery,
        "previous_mastery": previous_mastery,
        "fsrs_due": updated_card.due,
        "fsrs_rating": rating.value,
        "state_event_id": state_event.id,
        "nodes_unblocked": nodes_unblocked,
    }


async def _cascade_unblock(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    mastered_node_id: uuid.UUID,
) -> list[uuid.UUID]:
    """Check if mastering a node unblocks any downstream nodes."""
    edges_result = await db.execute(
        select(LearningEdge).where(
            LearningEdge.from_node_id == mastered_node_id,
            LearningEdge.relation == EdgeRelation.prerequisite,
        )
    )
    downstream_edges = edges_result.scalars().all()

    unblocked = []
    for edge in downstream_edges:
        downstream_id = edge.to_node_id

        prereq_result = await db.execute(
            select(LearningEdge.from_node_id).where(
                LearningEdge.to_node_id == downstream_id,
                LearningEdge.relation == EdgeRelation.prerequisite,
            )
        )
        all_prereq_ids = list(prereq_result.scalars().all())
        if not all_prereq_ids:
            continue

        mastered_result = await db.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child_id,
                ChildNodeState.node_id.in_(all_prereq_ids),
                ChildNodeState.mastery_level == MasteryLevel.mastered,
            )
        )
        mastered_count = len(mastered_result.scalars().all())

        if mastered_count == len(all_prereq_ids):
            downstream_state = await get_or_create_node_state(
                db, child_id, household_id, downstream_id
            )
            if downstream_state.mastery_level == MasteryLevel.not_started:
                await emit_state_event(
                    db, child_id, household_id, downstream_id,
                    event_type=StateEventType.node_unlocked,
                    from_state="blocked",
                    to_state="not_started",
                    trigger="prerequisite_met",
                    metadata={"mastered_prerequisite": str(mastered_node_id)},
                )
                unblocked.append(downstream_id)

    return unblocked


def compute_retrievability(fsrs_card: FSRSCard, now: datetime | None = None) -> float | None:
    """Compute current retrievability for an FSRS card.

    Uses the FSRS power-law forgetting formula:
    R = (1 + elapsed / (9 * stability))^(-1)
    """
    if not fsrs_card.last_review or not fsrs_card.stability or fsrs_card.stability <= 0:
        return None

    now = now or datetime.now(UTC)
    elapsed = (now - fsrs_card.last_review).total_seconds() / 86400

    if elapsed <= 0:
        return 1.0

    retrievability = (1 + elapsed / (9 * fsrs_card.stability)) ** (-1)
    return max(0.0, min(1.0, retrievability))
