"""Attempt workflow: connects System 1 (Curriculum) and System 2 (State).

Orchestrates: start attempt -> submit -> evaluate -> update FSRS ->
update state -> emit events -> cascade unblock.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ActivityStatus, AttemptStatus
from app.models.governance import Activity, Attempt
from app.services.evaluator import mock_evaluator
from app.services.state_engine import process_review
from app.services import intelligence
from app.services import achievements as achievements_svc


async def start_attempt(
    db: AsyncSession,
    activity_id: uuid.UUID,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> Attempt:
    """Create a new attempt for an activity."""
    # Verify activity exists and belongs to household
    result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id,
            Activity.household_id == household_id,
        )
    )
    activity = result.scalar_one_or_none()
    if not activity:
        raise ValueError("Activity not found")

    # Update activity status if needed
    if activity.status == ActivityStatus.scheduled:
        activity.status = ActivityStatus.in_progress

    attempt = Attempt(
        activity_id=activity_id,
        household_id=household_id,
        child_id=child_id,
        status=AttemptStatus.started,
    )
    db.add(attempt)
    await db.flush()
    return attempt


async def submit_attempt(
    db: AsyncSession,
    attempt_id: uuid.UUID,
    household_id: uuid.UUID,
    duration_minutes: int | None = None,
    score: float | None = None,
    confidence: float | None = None,
    feedback: dict | None = None,
    user_id: uuid.UUID | None = None,
) -> dict:
    """Submit an attempt, triggering the evaluation pipeline.

    Returns dict with attempt, state update results, etc.
    """
    # Get the attempt
    result = await db.execute(
        select(Attempt).where(
            Attempt.id == attempt_id,
            Attempt.household_id == household_id,
        )
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise ValueError("Attempt not found")

    if attempt.status != AttemptStatus.started:
        raise ValueError(f"Attempt is already {attempt.status.value if hasattr(attempt.status, 'value') else attempt.status}")

    # Complete the attempt
    now = datetime.now(UTC)
    attempt.status = AttemptStatus.completed
    attempt.completed_at = now
    attempt.duration_minutes = duration_minutes
    attempt.score = score
    attempt.feedback = feedback or {}

    # Get the activity to find the linked node
    activity_result = await db.execute(
        select(Activity).where(Activity.id == attempt.activity_id)
    )
    activity = activity_result.scalar_one()

    # Update activity status
    activity.status = ActivityStatus.completed

    await db.flush()

    # If no node linked, we can't update state
    if not activity.node_id:
        return {
            "attempt": attempt,
            "mastery_level": None,
            "previous_mastery": None,
            "fsrs_due": None,
            "fsrs_rating": None,
            "state_event_id": None,
            "nodes_unblocked": [],
        }

    # Evaluate: use provided confidence or run mock evaluator
    if confidence is None:
        confidence = mock_evaluator.evaluate(score=score)

    # Process through state engine (FSRS + state transition + cascade)
    review_result = await process_review(
        db,
        child_id=attempt.child_id,
        household_id=household_id,
        node_id=activity.node_id,
        confidence=confidence,
        duration_minutes=duration_minutes,
        created_by=user_id,
    )

    # Record intelligence observations (non-blocking)
    try:
        hour = now.hour
        time_of_day = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
        subject = activity.subject_area or activity.title or ""

        await intelligence.record_attempt_engagement(
            db, attempt.child_id, household_id,
            duration_minutes=duration_minutes or 0,
            activity_type=activity.activity_type.value if hasattr(activity.activity_type, "value") else str(activity.activity_type),
            time_of_day=time_of_day,
            completed=True,
            estimated_minutes=activity.estimated_minutes,
        )

        # Record evaluation insight if we have feedback data
        if feedback:
            await intelligence.record_evaluation_insight(
                db, attempt.child_id, household_id,
                evaluation_result=feedback,
                activity_title=activity.title or "",
                subject=subject,
            )

        # Record mastery transition if level changed
        prev = review_result.get("previous_mastery")
        curr = review_result.get("mastery_level")
        if prev and curr and prev != curr:
            await intelligence.record_mastery_transition(
                db, attempt.child_id, household_id,
                subject=subject,
                from_level=prev,
                to_level=curr,
                node_title=activity.title or "",
            )
    except Exception:
        pass  # Intelligence recording is non-blocking

    # Check achievements and update streak
    new_achievements = []
    try:
        await achievements_svc.update_streak(db, attempt.child_id, household_id)
        ctx = {
            "subject": activity.subject_area or activity.title or "",
            "new_level": review_result.get("mastery_level"),
            "old_level": review_result.get("previous_mastery"),
            "node_id": str(activity.node_id) if activity.node_id else None,
        }
        new_achievements = await achievements_svc.check_achievements(
            db, attempt.child_id, household_id,
            trigger_event="mastery_change" if ctx["new_level"] != ctx["old_level"] else "activity_complete",
            context=ctx,
        )
    except Exception:
        pass  # Achievement checking is non-blocking

    return {
        "attempt": attempt,
        **review_result,
        "new_achievements": [{"title": a.title, "icon": a.icon} for a in new_achievements],
    }
