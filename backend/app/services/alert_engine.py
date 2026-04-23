"""Alert Engine (Section 3.5 / System 4).

Detects: stalls, regressions, patterns, prerequisite decay.
Runs as daily Celery task + triggered inline on state changes.
"""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode
from app.models.enums import AlertSeverity, AlertStatus, MasteryLevel
from app.models.evidence import Alert
from app.models.fitness import FitnessBenchmark, FitnessLog
from app.models.identity import Child
from app.models.state import ChildNodeState, StateEvent

_FITNESS_MAP_NAME_PREFIX = "Physical Fitness"
# Tiers 1-3 are Foundations, Development, Intermediate. Overtraining detection
# only applies to these younger/less-conditioned progression tiers.
_OVERTRAINING_TIER_NAMES = (
    "Physical Fitness: Foundations",
    "Physical Fitness: Development",
    "Physical Fitness: Intermediate",
)
# Units where a smaller number means a better performance.
_LOWER_IS_BETTER_UNITS = {"seconds", "minutes"}


async def _child_name(db: AsyncSession, child_id: uuid.UUID) -> str:
    result = await db.execute(select(Child.first_name).where(Child.id == child_id))
    first = result.scalar_one_or_none()
    return first or "Your child"


async def _has_unresolved_alert(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    source: str,
    *,
    since: datetime | None = None,
) -> bool:
    """True if an unresolved alert with the same source already exists."""
    stmt = select(Alert.id).where(
        Alert.household_id == household_id,
        Alert.child_id == child_id,
        Alert.source == source,
        Alert.status.in_([AlertStatus.unread, AlertStatus.read]),
    )
    if since is not None:
        stmt = stmt.where(Alert.created_at >= since)
    result = await db.execute(stmt.limit(1))
    return result.scalar_one_or_none() is not None


async def detect_stalls(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> list[Alert]:
    """Detect nodes in_progress for too long without mastery improvement."""
    cutoff = datetime.now(UTC) - timedelta(days=14)  # 2 weeks default

    in_progress_levels = [
        MasteryLevel.emerging,
        MasteryLevel.developing,
        MasteryLevel.proficient,
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
            select(Alert.id)
            .where(
                Alert.household_id == household_id,
                Alert.child_id == state.child_id,
                Alert.source == "stall_detection",
                Alert.status.in_([AlertStatus.unread, AlertStatus.read]),
                Alert.metadata_["node_id"].as_string() == str(state.node_id),
            )
            .limit(1)
        )
        if existing.scalar_one_or_none():
            continue

        # Get node title
        node_result = await db.execute(select(LearningNode.title).where(LearningNode.id == state.node_id))
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

    node_result = await db.execute(select(LearningNode.title).where(LearningNode.id == node_id))
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
        select(StateEvent)
        .where(
            StateEvent.child_id == child_id,
            StateEvent.node_id == node_id,
        )
        .order_by(StateEvent.created_at.desc())
        .limit(3)
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

    node_result = await db.execute(select(LearningNode.title).where(LearningNode.id == node_id))
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


# ══════════════════════════════════════════════════
# Fitness-specific detectors
# ══════════════════════════════════════════════════


async def detect_fitness_stall(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> list[Alert]:
    """Info alert for each child with a PE enrollment but no logs in the past 14 days."""
    cutoff = datetime.now(UTC) - timedelta(days=14)

    # Children with an active enrollment in a Physical Fitness learning map.
    enrolled_result = await db.execute(
        select(ChildMapEnrollment.child_id)
        .join(LearningMap, LearningMap.id == ChildMapEnrollment.learning_map_id)
        .where(
            ChildMapEnrollment.household_id == household_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
            LearningMap.name.ilike(f"{_FITNESS_MAP_NAME_PREFIX}%"),
        )
        .distinct()
    )
    candidate_ids = list(enrolled_result.scalars().all())
    if not candidate_ids:
        return []

    alerts: list[Alert] = []
    for child_id in candidate_ids:
        recent = await db.execute(
            select(func.count(FitnessLog.id)).where(
                FitnessLog.household_id == household_id,
                FitnessLog.child_id == child_id,
                FitnessLog.logged_at >= cutoff,
            )
        )
        if (recent.scalar_one() or 0) > 0:
            continue
        if await _has_unresolved_alert(db, household_id, child_id, "fitness_stall_detection"):
            continue

        name = await _child_name(db, child_id)
        alert = Alert(
            household_id=household_id,
            child_id=child_id,
            severity=AlertSeverity.info,
            status=AlertStatus.unread,
            title="No recent physical activity",
            message=f"No physical activity logged for {name} in the past two weeks.",
            source="fitness_stall_detection",
            metadata_={"days_since_last_log": 14},
        )
        db.add(alert)
        alerts.append(alert)

    await db.flush()
    return alerts


async def detect_fitness_regression(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    benchmark_name: str,
) -> Alert | None:
    """Warning alert when the last 3 benchmarks each regress vs the previous."""
    result = await db.execute(
        select(FitnessBenchmark)
        .where(
            FitnessBenchmark.household_id == household_id,
            FitnessBenchmark.child_id == child_id,
            FitnessBenchmark.benchmark_name == benchmark_name,
        )
        .order_by(FitnessBenchmark.measured_at.desc())
        .limit(3)
    )
    recent = list(result.scalars().all())
    if len(recent) < 3:
        return None

    # Put in chronological order: oldest → newest.
    recent.reverse()
    unit = recent[-1].unit
    lower_is_better = (unit or "").lower() in _LOWER_IS_BETTER_UNITS
    deltas = [recent[i].value - recent[i - 1].value for i in range(1, 3)]
    if lower_is_better:
        is_declining = all(d > 0 for d in deltas)  # time increased → worse
    else:
        is_declining = all(d < 0 for d in deltas)  # count decreased → worse
    if not is_declining:
        return None

    if await _has_unresolved_alert(db, household_id, child_id, f"fitness_regression:{benchmark_name}"):
        return None

    name = await _child_name(db, child_id)
    alert = Alert(
        household_id=household_id,
        child_id=child_id,
        severity=AlertSeverity.warning,
        status=AlertStatus.unread,
        title=f"Regression: {benchmark_name}",
        message=f"{name}'s {benchmark_name} has declined over the last three assessments.",
        source=f"fitness_regression:{benchmark_name}",
        metadata_={
            "benchmark_name": benchmark_name,
            "values": [r.value for r in recent],
            "unit": unit,
        },
    )
    db.add(alert)
    await db.flush()
    return alert


async def detect_fitness_overtraining(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> Alert | None:
    """Info alert when a Tier 1-3 child logs >6 long sessions in a single calendar week."""
    # Gate by tier: only Foundations, Development, Intermediate.
    tier_enrolled = await db.execute(
        select(func.count(ChildMapEnrollment.id))
        .join(LearningMap, LearningMap.id == ChildMapEnrollment.learning_map_id)
        .where(
            ChildMapEnrollment.household_id == household_id,
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
            LearningMap.name.in_(_OVERTRAINING_TIER_NAMES),
        )
    )
    if (tier_enrolled.scalar_one() or 0) == 0:
        return None

    now = datetime.now(UTC)
    week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    long_sessions = await db.execute(
        select(func.count(FitnessLog.id)).where(
            FitnessLog.household_id == household_id,
            FitnessLog.child_id == child_id,
            FitnessLog.logged_at >= week_start,
            FitnessLog.duration_minutes > 30,
        )
    )
    count = long_sessions.scalar_one() or 0
    if count <= 6:
        return None

    if await _has_unresolved_alert(
        db,
        household_id,
        child_id,
        "fitness_overtraining_detection",
        since=week_start,
    ):
        return None

    name = await _child_name(db, child_id)
    alert = Alert(
        household_id=household_id,
        child_id=child_id,
        severity=AlertSeverity.info,
        status=AlertStatus.unread,
        title="High training volume",
        message=f"High training volume detected for {name} this week. Consider adding a rest day.",
        source="fitness_overtraining_detection",
        metadata_={"sessions_over_30_min": count, "week_start": week_start.isoformat()},
    )
    db.add(alert)
    await db.flush()
    return alert
