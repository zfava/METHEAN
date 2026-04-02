"""Alert Engine (Section 3.5 / System 4).

Detects: stalls, regressions, patterns, prerequisite decay.
Runs as daily Celery task + triggered inline on state changes.
"""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AlertSeverity, AlertStatus, MasteryLevel
from app.models.evidence import Alert
from app.models.state import ChildNodeState, FSRSCard, ReviewLog, StateEvent
from app.models.curriculum import LearningEdge, LearningNode
from app.models.enums import EdgeRelation


async def detect_stalls(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> list[Alert]:
    """Detect nodes in_progress for too long without mastery improvement."""
    cutoff = datetime.now(UTC) - timedelta(days=14)  # 2 weeks default

    in_progress_levels = [
        MasteryLevel.emerging, MasteryLevel.developing, MasteryLevel.proficient,
    ]

    result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.household_id == household_id,
            ChildNodeState.mastery_level.in_(in_progress_levels),
            ChildNodeState.last_activity_at < cutoff,
            ChildNodeState.last_activity_at.isnot(None),
        )
    )
    stalled = result.scalars().all()

    alerts = []
    for state in stalled:
        # Check no existing active stall alert for this node
        existing = await db.execute(
            select(Alert.id).where(
                Alert.household_id == household_id,
                Alert.child_id == state.child_id,
                Alert.source == "stall_detection",
                Alert.status.in_([AlertStatus.unread, AlertStatus.read]),
                Alert.metadata_["node_id"].as_string() == str(state.node_id),
            ).limit(1)
        )
        if existing.scalar_one_or_none():
            continue

        # Get node title
        node_result = await db.execute(
            select(LearningNode.title).where(LearningNode.id == state.node_id)
        )
        title = node_result.scalar_one_or_none() or "Unknown"

        days_stalled = (datetime.now(UTC) - state.last_activity_at).days if state.last_activity_at else 0

        alert = Alert(
            household_id=household_id,
            child_id=state.child_id,
            severity=AlertSeverity.warning,
            status=AlertStatus.unread,
            title=f"Stalled: {title}",
            message=f"No activity on '{title}' for {days_stalled} days at {state.mastery_level.value if hasattr(state.mastery_level, 'value') else state.mastery_level} level.",
            source="stall_detection",
            metadata_={"node_id": str(state.node_id), "days_stalled": days_stalled},
        )
        db.add(alert)
        alerts.append(alert)

    await db.flush()
    return alerts


async def detect_regression(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
    from_mastery: str,
    to_mastery: str,
) -> Alert | None:
    """Create alert when mastered -> lower state (decay)."""
    if from_mastery != "mastered":
        return None

    node_result = await db.execute(
        select(LearningNode.title).where(LearningNode.id == node_id)
    )
    title = node_result.scalar_one_or_none() or "Unknown"

    alert = Alert(
        household_id=household_id,
        child_id=child_id,
        severity=AlertSeverity.warning,
        status=AlertStatus.unread,
        title=f"Regression: {title}",
        message=f"'{title}' dropped from mastered to {to_mastery}. Review recommended.",
        source="regression_detection",
        metadata_={"node_id": str(node_id), "from": from_mastery, "to": to_mastery},
    )
    db.add(alert)
    await db.flush()
    return alert


async def detect_pattern_failure(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
) -> Alert | None:
    """Detect 3+ consecutive low-quality attempts on same node."""
    result = await db.execute(
        select(StateEvent).where(
            StateEvent.child_id == child_id,
            StateEvent.node_id == node_id,
        ).order_by(StateEvent.created_at.desc()).limit(3)
    )
    events = result.scalars().all()

    if len(events) < 3:
        return None

    # Check if last 3 attempts had low confidence
    low_count = 0
    for evt in events:
        meta = evt.metadata_ or {}
        confidence = meta.get("confidence", 1.0)
        if confidence < 0.5:
            low_count += 1

    if low_count < 3:
        return None

    node_result = await db.execute(
        select(LearningNode.title).where(LearningNode.id == node_id)
    )
    title = node_result.scalar_one_or_none() or "Unknown"

    alert = Alert(
        household_id=household_id,
        child_id=child_id,
        severity=AlertSeverity.action_required,
        status=AlertStatus.unread,
        title=f"Struggling: {title}",
        message=f"3 consecutive low-quality attempts on '{title}'. Consider adjusting approach or reviewing prerequisites.",
        source="pattern_detection",
        metadata_={"node_id": str(node_id), "consecutive_low": low_count},
    )
    db.add(alert)
    await db.flush()
    return alert
