"""Fitness business logic: activity logging, benchmarks, and analytics.

Mirrors the state-update pattern used by the attempt workflow: writes a
log record, updates the per-node learner state, and emits a StateEvent
when mastery advances.
"""

import uuid
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from itertools import pairwise
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningEdge, LearningMap, LearningNode
from app.models.enums import EdgeRelation, MasteryLevel, StateEventType
from app.models.fitness import FitnessBenchmark, FitnessLog
from app.models.state import ChildNodeState
from app.services.state_engine import emit_state_event, get_or_create_node_state

# Units where a smaller number means a better performance.
_LOWER_IS_BETTER_UNITS = {"seconds", "minutes"}
# Order of mastery levels for "at least" comparisons.
_MASTERY_ORDER = {
    MasteryLevel.not_started: 0,
    MasteryLevel.emerging: 1,
    MasteryLevel.developing: 2,
    MasteryLevel.proficient: 3,
    MasteryLevel.mastered: 4,
}


def _is_lower_better(unit: str | None) -> bool:
    return (unit or "").lower() in _LOWER_IS_BETTER_UNITS


def _improvement_pct(first: float, latest: float, lower_is_better: bool) -> float:
    """Percentage improvement from the first recorded value to the latest."""
    if first == 0:
        return 0.0
    delta = (first - latest) if lower_is_better else (latest - first)
    return round((delta / abs(first)) * 100.0, 2)


def _trend_from_series(values: list[float], lower_is_better: bool) -> str:
    """Return improving/plateau/declining from the last 5 values in order."""
    tail = values[-5:]
    if len(tail) < 2:
        return "plateau"
    improvements = 0
    declines = 0
    for prev, curr in pairwise(tail):
        if curr == prev:
            continue
        is_better = (curr < prev) if lower_is_better else (curr > prev)
        if is_better:
            improvements += 1
        else:
            declines += 1
    if improvements > declines:
        return "improving"
    if declines > improvements:
        return "declining"
    return "plateau"


def _meets_threshold(
    measurement_value: float | None,
    threshold: float | None,
    comparator: str,
) -> bool:
    """Check a measurement against a numeric benchmark threshold."""
    if measurement_value is None or threshold is None:
        return False
    if comparator == "lte":
        return measurement_value <= threshold
    return measurement_value >= threshold


async def _all_prereqs_mastered(db: AsyncSession, child_id: uuid.UUID, node_id: uuid.UUID) -> bool:
    """True when every prerequisite edge points to a fully mastered node."""
    prereq_result = await db.execute(
        select(LearningEdge.from_node_id).where(
            LearningEdge.to_node_id == node_id,
            LearningEdge.relation == EdgeRelation.prerequisite,
        )
    )
    prereq_ids = list(prereq_result.scalars().all())
    if not prereq_ids:
        return True

    mastered_result = await db.execute(
        select(func.count(ChildNodeState.id)).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.node_id.in_(prereq_ids),
            ChildNodeState.mastery_level == MasteryLevel.mastered,
        )
    )
    mastered_count = mastered_result.scalar_one()
    return mastered_count == len(prereq_ids)


async def log_fitness_activity(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    logged_at: datetime,
    duration_minutes: int,
    measurement_type: str,
    measurement_value: float | None = None,
    measurement_unit: str | None = None,
    sets: int | None = None,
    reps: int | None = None,
    weight_lbs: float | None = None,
    distance_value: float | None = None,
    heart_rate_avg: int | None = None,
    notes: str | None = None,
    logged_by: uuid.UUID | None = None,
) -> dict:
    """Record a fitness practice, update node state, and advance mastery if earned."""
    log = FitnessLog(
        household_id=household_id,
        child_id=child_id,
        node_id=node_id,
        logged_at=logged_at,
        duration_minutes=duration_minutes,
        measurement_type=measurement_type,
        measurement_value=measurement_value,
        measurement_unit=measurement_unit,
        sets=sets,
        reps=reps,
        weight_lbs=weight_lbs,
        distance_value=distance_value,
        heart_rate_avg=heart_rate_avg,
        notes=notes,
        logged_by=logged_by,
    )
    db.add(log)

    state = await get_or_create_node_state(db, child_id, household_id, node_id)
    state.time_spent_minutes = (state.time_spent_minutes or 0) + duration_minutes
    state.attempts_count = (state.attempts_count or 0) + 1
    state.last_activity_at = logged_at

    node_result = await db.execute(select(LearningNode).where(LearningNode.id == node_id))
    node = node_result.scalar_one_or_none()

    mastery_advanced = False
    previous_mastery = state.mastery_level
    state_event_id: uuid.UUID | None = None

    if node is not None:
        content = node.content or {}
        benchmark_criteria = content.get("benchmark_criteria")
        if benchmark_criteria:
            threshold = content.get("benchmark_threshold")
            assessment_type = content.get("assessment_type")
            unit = content.get("measurement_unit") or measurement_unit
            default_comparator = "lte" if _is_lower_better(unit) else "gte"
            comparator = content.get("benchmark_comparator", default_comparator)

            if threshold is not None:
                threshold_met = _meets_threshold(measurement_value, float(threshold), comparator)
            elif assessment_type in ("pass_fail", "observed"):
                # No numeric threshold; successful logging is the signal.
                threshold_met = True
            else:
                threshold_met = False

            already_proficient = _MASTERY_ORDER.get(state.mastery_level, 0) >= _MASTERY_ORDER[MasteryLevel.proficient]
            if threshold_met and not already_proficient and await _all_prereqs_mastered(db, child_id, node_id):
                state.mastery_level = MasteryLevel.proficient
                mastery_advanced = True
                event = await emit_state_event(
                    db,
                    child_id=child_id,
                    household_id=household_id,
                    node_id=node_id,
                    event_type=StateEventType.mastery_change,
                    from_state=previous_mastery.value if hasattr(previous_mastery, "value") else str(previous_mastery),
                    to_state=MasteryLevel.proficient.value,
                    trigger="fitness_log",
                    metadata={
                        "measurement_type": measurement_type,
                        "measurement_value": measurement_value,
                        "measurement_unit": measurement_unit,
                        "threshold": threshold,
                        "comparator": comparator,
                    },
                    created_by=logged_by,
                )
                state_event_id = event.id

    await db.flush()

    return {
        "id": log.id,
        "household_id": log.household_id,
        "child_id": log.child_id,
        "node_id": log.node_id,
        "logged_at": log.logged_at,
        "duration_minutes": log.duration_minutes,
        "measurement_type": log.measurement_type,
        "measurement_value": log.measurement_value,
        "measurement_unit": log.measurement_unit,
        "sets": log.sets,
        "reps": log.reps,
        "weight_lbs": log.weight_lbs,
        "distance_value": log.distance_value,
        "heart_rate_avg": log.heart_rate_avg,
        "notes": log.notes,
        "logged_by": log.logged_by,
        "mastery_advanced": mastery_advanced,
        "previous_mastery": previous_mastery.value if hasattr(previous_mastery, "value") else str(previous_mastery),
        "current_mastery": state.mastery_level.value
        if hasattr(state.mastery_level, "value")
        else str(state.mastery_level),
        "state_event_id": state_event_id,
    }


async def record_benchmark(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    benchmark_name: str,
    value: float,
    unit: str,
    tier: str | None = None,
    measured_at: datetime | None = None,
    notes: str | None = None,
) -> dict:
    """Persist a benchmark and return it with improvement/PB metadata."""
    measured_at = measured_at or datetime.now(UTC)

    prior_result = await db.execute(
        select(FitnessBenchmark)
        .where(
            FitnessBenchmark.child_id == child_id,
            FitnessBenchmark.household_id == household_id,
            FitnessBenchmark.benchmark_name == benchmark_name,
        )
        .order_by(FitnessBenchmark.measured_at.asc())
    )
    prior = list(prior_result.scalars().all())

    lower_is_better = _is_lower_better(unit)
    if prior:
        first_value = prior[0].value
        if lower_is_better:
            personal_best = value < min(b.value for b in prior)
        else:
            personal_best = value > max(b.value for b in prior)
        improvement_pct = _improvement_pct(first_value, value, lower_is_better)
    else:
        first_value = value
        personal_best = True
        improvement_pct = 0.0

    benchmark = FitnessBenchmark(
        household_id=household_id,
        child_id=child_id,
        benchmark_name=benchmark_name,
        measured_at=measured_at,
        value=value,
        unit=unit,
        tier=tier,
        notes=notes,
    )
    db.add(benchmark)
    await db.flush()

    return {
        "id": benchmark.id,
        "household_id": benchmark.household_id,
        "child_id": benchmark.child_id,
        "benchmark_name": benchmark.benchmark_name,
        "measured_at": benchmark.measured_at,
        "value": benchmark.value,
        "unit": benchmark.unit,
        "tier": benchmark.tier,
        "percentile": benchmark.percentile,
        "notes": benchmark.notes,
        "first_value": first_value,
        "improvement_pct": improvement_pct,
        "personal_best": personal_best,
        "history_count": len(prior) + 1,
    }


async def get_progress_summary(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
) -> dict:
    """Aggregate benchmarks, fitness hours, and mastery for a child."""
    now = datetime.now(UTC)
    week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Benchmarks grouped by name.
    bench_result = await db.execute(
        select(FitnessBenchmark)
        .where(
            FitnessBenchmark.child_id == child_id,
            FitnessBenchmark.household_id == household_id,
        )
        .order_by(FitnessBenchmark.benchmark_name.asc(), FitnessBenchmark.measured_at.asc())
    )
    by_name: dict[str, list[FitnessBenchmark]] = defaultdict(list)
    for row in bench_result.scalars().all():
        by_name[row.benchmark_name].append(row)

    benchmarks_summary: list[dict[str, Any]] = []
    for name, rows in by_name.items():
        values = [r.value for r in rows]
        unit = rows[-1].unit
        lower_is_better = _is_lower_better(unit)
        first_value = values[0]
        latest_value = values[-1]
        best_value = min(values) if lower_is_better else max(values)
        benchmarks_summary.append(
            {
                "benchmark_name": name,
                "unit": unit,
                "first_value": first_value,
                "latest_value": latest_value,
                "personal_best": best_value,
                "improvement_pct": _improvement_pct(first_value, latest_value, lower_is_better),
                "trend": _trend_from_series(values, lower_is_better),
                "data_point_count": len(values),
            }
        )

    # Fitness hours across three windows.
    def _sum_minutes(since: datetime | None) -> Any:
        q = select(func.coalesce(func.sum(FitnessLog.duration_minutes), 0)).where(
            FitnessLog.child_id == child_id,
            FitnessLog.household_id == household_id,
        )
        if since is not None:
            q = q.where(FitnessLog.logged_at >= since)
        return q

    all_time = (await db.execute(_sum_minutes(None))).scalar_one() or 0
    this_month = (await db.execute(_sum_minutes(month_start))).scalar_one() or 0
    this_week = (await db.execute(_sum_minutes(week_start))).scalar_one() or 0

    # Node mastery within fitness learning maps for this child.
    node_scope = (
        select(ChildNodeState.mastery_level)
        .join(LearningNode, LearningNode.id == ChildNodeState.node_id)
        .join(LearningMap, LearningMap.id == LearningNode.learning_map_id)
        .where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
            LearningMap.name.ilike("Physical Fitness%"),
        )
    )
    node_rows = (await db.execute(node_scope)).scalars().all()
    mastery_proficient_or_better = sum(
        1 for m in node_rows if _MASTERY_ORDER.get(m, 0) >= _MASTERY_ORDER[MasteryLevel.proficient]
    )

    return {
        "benchmarks": benchmarks_summary,
        "fitness_hours": {
            "all_time": round(all_time / 60.0, 2),
            "this_month": round(this_month / 60.0, 2),
            "this_week": round(this_week / 60.0, 2),
        },
        "nodes": {
            "mastered": mastery_proficient_or_better,
            "total": len(node_rows),
        },
    }


async def get_detailed_stats(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    period_start: datetime,
    period_end: datetime,
) -> dict:
    """Return weekly minutes breakdown and strength/endurance/flexibility series."""
    logs_result = await db.execute(
        select(FitnessLog)
        .where(
            FitnessLog.child_id == child_id,
            FitnessLog.household_id == household_id,
            FitnessLog.logged_at >= period_start,
            FitnessLog.logged_at <= period_end,
        )
        .order_by(FitnessLog.logged_at.asc())
    )
    logs = list(logs_result.scalars().all())

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly: dict[str, int] = {d: 0 for d in day_names}
    for log in logs:
        weekly[day_names[log.logged_at.weekday()]] += log.duration_minutes or 0

    strength: list[dict[str, Any]] = []
    endurance: list[dict[str, Any]] = []
    flexibility: list[dict[str, Any]] = []

    for log in logs:
        day = log.logged_at.date()
        if log.measurement_type == "weight_reps" and log.weight_lbs is not None and log.reps is not None:
            strength.append(
                {
                    "date": day,
                    "node_id": log.node_id,
                    "weight_lbs": log.weight_lbs,
                    "reps": log.reps,
                    "estimated_1rm": round(log.weight_lbs * (1 + log.reps / 30.0), 2),
                }
            )
        elif log.measurement_type == "timed" and log.distance_value is not None and log.measurement_value is not None:
            time_seconds = (
                log.measurement_value * 60.0
                if (log.measurement_unit or "").lower() == "minutes"
                else log.measurement_value
            )
            endurance.append(
                {
                    "date": day,
                    "node_id": log.node_id,
                    "time_seconds": round(time_seconds, 2),
                    "distance_value": log.distance_value,
                    "distance_unit": log.measurement_unit,
                }
            )
        if (log.measurement_unit or "").lower() == "inches" and log.measurement_value is not None:
            flexibility.append(
                {
                    "date": day,
                    "node_id": log.node_id,
                    "inches": log.measurement_value,
                }
            )

    return {
        "period_start": period_start,
        "period_end": period_end,
        "weekly_minutes": weekly,
        "strength": strength,
        "endurance": endurance,
        "flexibility": flexibility,
    }
