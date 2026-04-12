"""Wellbeing Anomaly Detection Engine.

Detects when a child's performance drops across multiple subjects
simultaneously. Every design decision errs on the side of caution.

# PARENT-ONLY: This service's output must never reach child-facing endpoints.
"""

import logging
import math
import uuid
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration import EvaluatorPrediction
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import AnomalyStatus, AnomalyType, SensitivityLevel
from app.models.governance import Activity, Attempt
from app.models.identity import Child
from app.models.intelligence import LearnerIntelligence
from app.models.state import ChildNodeState
from app.models.wellbeing import WellbeingAnomaly, WellbeingConfig

logger = logging.getLogger(__name__)

# Active statuses for deduplication
ACTIVE_STATUSES = {AnomalyStatus.detected, AnomalyStatus.notified, AnomalyStatus.acknowledged}
DEDUP_WINDOW_DAYS = 14
MIN_BASELINE_DAYS = 30
MIN_DATA_POINTS_PER_SUBJECT = 20


# ═══════════════════════════════════════════
# Threshold Management
# ═══════════════════════════════════════════


def get_effective_threshold(
    config: WellbeingConfig | None,
    anomaly_type: str,
    default_sd: float = 1.5,
) -> float:
    """Get the effective SD threshold accounting for sensitivity, custom, and self-calibration."""
    if config is None:
        return default_sd

    sens = config.sensitivity_level
    sens_val = sens.value if hasattr(sens, "value") else str(sens)
    base = {"conservative": 2.0, "balanced": 1.5, "sensitive": 1.0}.get(sens_val, 1.5)

    custom = (config.custom_thresholds or {}).get(anomaly_type, {})
    if isinstance(custom, dict) and "sd_threshold" in custom:
        base = custom["sd_threshold"]

    adjustment = (config.threshold_adjustments or {}).get(anomaly_type, 0.0)
    return base + adjustment


# ═══════════════════════════════════════════
# Baseline & Window Computation
# ═══════════════════════════════════════════


async def _get_subject_for_node(db: AsyncSession, node_id: uuid.UUID) -> str | None:
    result = await db.execute(
        select(Subject.name)
        .join(LearningMap, Subject.id == LearningMap.subject_id)
        .join(LearningNode, LearningMap.id == LearningNode.learning_map_id)
        .where(LearningNode.id == node_id)
    )
    row = result.one_or_none()
    return row[0] if row else None


async def _compute_metrics(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    start_date: datetime,
    end_date: datetime,
) -> dict | None:
    """Compute per-subject metrics for a date range.

    Returns dict with "subjects" map and metadata, or None if insufficient data.
    """
    # Get attempts in the window joined with activity/node/subject
    result = await db.execute(
        select(Attempt, Activity.node_id, Activity.estimated_minutes).join(
            Activity, Attempt.activity_id == Activity.id
        ).where(
            Attempt.child_id == child_id,
            Attempt.household_id == household_id,
            Attempt.created_at >= start_date,
            Attempt.created_at <= end_date,
        )
    )
    rows = result.all()

    if not rows:
        return None

    # Resolve subjects for each node
    node_subjects: dict[uuid.UUID, str] = {}
    for attempt, node_id, est_min in rows:
        if node_id and node_id not in node_subjects:
            subj = await _get_subject_for_node(db, node_id)
            if subj:
                node_subjects[node_id] = subj

    # Group attempts by subject
    subject_attempts: dict[str, list[dict]] = defaultdict(list)
    for attempt, node_id, est_min in rows:
        subj = node_subjects.get(node_id, "Unknown") if node_id else "Unknown"
        if subj == "Unknown":
            continue

        status_val = attempt.status.value if hasattr(attempt.status, "value") else str(attempt.status)

        # Effort quality: completion * duration ratio
        completed = status_val == "completed"
        dur = attempt.duration_minutes or 0
        expected = est_min or 30
        duration_ratio = min(1.0, dur / max(expected, 1)) if dur > 0 else 0.0
        effort = (1.0 if completed else 0.3) * max(0.3, duration_ratio)

        subject_attempts[subj].append({
            "completed": completed,
            "effort": effort,
            "node_id": str(node_id) if node_id else None,
        })

    # Get evaluator confidence per subject
    pred_result = await db.execute(
        select(EvaluatorPrediction).where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.household_id == household_id,
            EvaluatorPrediction.created_at >= start_date,
            EvaluatorPrediction.created_at <= end_date,
        )
    )
    preds = pred_result.scalars().all()

    subject_confidences: dict[str, list[float]] = defaultdict(list)
    for p in preds:
        subj = node_subjects.get(p.node_id)
        if subj:
            subject_confidences[subj].append(p.predicted_confidence)

    # Get frustration data from intelligence
    intel_result = await db.execute(
        select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id)
    )
    intel = intel_result.scalar_one_or_none()

    # Build per-subject metrics
    subjects: dict[str, dict] = {}
    total_points = 0

    for subj, attempts in subject_attempts.items():
        n = len(attempts)
        if n < 3:  # Need at least 3 data points for a window
            continue

        efforts = [a["effort"] for a in attempts]
        effort_mean = sum(efforts) / n
        effort_var = sum((e - effort_mean) ** 2 for e in efforts) / max(n - 1, 1)
        effort_std = math.sqrt(effort_var) if effort_var > 0 else 0.1

        completed_count = sum(1 for a in attempts if a["completed"])
        completion_rate = completed_count / n
        # Compute std for completion as binomial approximation
        completion_std = math.sqrt(completion_rate * (1 - completion_rate) / max(n, 1)) if n > 1 else 0.1

        confs = subject_confidences.get(subj, [])
        if confs:
            conf_mean = sum(confs) / len(confs)
            conf_var = sum((c - conf_mean) ** 2 for c in confs) / max(len(confs) - 1, 1)
            conf_std = math.sqrt(conf_var) if conf_var > 0 else 0.1
        else:
            conf_mean = 0.0
            conf_std = 0.1

        # Frustration from intelligence patterns
        frustration_freq = 0.0
        frustration_std = 0.1
        if intel and intel.subject_patterns:
            sp = intel.subject_patterns.get(subj, {})
            struggles = sp.get("struggles", [])
            frustration_freq = len(struggles) / max(n, 1)

        subjects[subj] = {
            "effort_quality_mean": round(effort_mean, 3),
            "effort_quality_std": round(max(effort_std, 0.05), 3),
            "frustration_frequency": round(frustration_freq, 3),
            "frustration_std": round(frustration_std, 3),
            "evaluator_confidence_mean": round(conf_mean, 3),
            "evaluator_confidence_std": round(max(conf_std, 0.05), 3),
            "session_completion_rate": round(completion_rate, 3),
            "completion_std": round(max(completion_std, 0.05), 3),
            "data_points": n,
        }
        total_points += n

    if not subjects:
        return None

    return {
        "subjects": subjects,
        "overall_data_points": total_points,
        "baseline_start": start_date.date().isoformat(),
        "baseline_end": end_date.date().isoformat(),
    }


async def compute_child_baselines(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> dict | None:
    """Compute 90-day rolling baselines. Returns None if < 30 days of data."""
    now = datetime.now(UTC)
    start = now - timedelta(days=90)

    metrics = await _compute_metrics(db, child_id, household_id, start, now)
    if metrics is None:
        return None

    # Filter subjects with insufficient data
    filtered = {
        s: m for s, m in metrics["subjects"].items()
        if m["data_points"] >= MIN_DATA_POINTS_PER_SUBJECT
    }

    if not filtered:
        return None

    metrics["subjects"] = filtered
    return metrics


async def compute_recent_window(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    window_days: int = 14,
) -> dict | None:
    """Compute metrics for the recent window."""
    now = datetime.now(UTC)
    start = now - timedelta(days=window_days)
    return await _compute_metrics(db, child_id, household_id, start, now)


# ═══════════════════════════════════════════
# Detection Algorithms
# ═══════════════════════════════════════════


def _detect_broad_disengagement(
    baselines: dict,
    recent: dict,
    config: WellbeingConfig | None,
    child_name: str,
) -> WellbeingAnomaly | None:
    """Effort quality drops across 3+ subjects."""
    threshold = get_effective_threshold(config, "broad_disengagement")
    affected = []
    evidence = {}

    for subj, baseline in baselines["subjects"].items():
        recent_subj = recent["subjects"].get(subj)
        if not recent_subj:
            continue

        bl_mean = baseline["effort_quality_mean"]
        bl_std = baseline["effort_quality_std"]
        recent_mean = recent_subj["effort_quality_mean"]

        if bl_std > 0:
            deviation = (bl_mean - recent_mean) / bl_std
            if deviation >= threshold:
                affected.append(subj)
                evidence[subj] = {
                    "baseline_mean": bl_mean,
                    "recent_mean": recent_mean,
                    "deviation_sd": round(deviation, 2),
                }

    min_subjects = 3
    if config and config.custom_thresholds:
        ct = config.custom_thresholds.get("broad_disengagement", {})
        if isinstance(ct, dict):
            min_subjects = ct.get("min_subjects", 3)

    if len(affected) < min_subjects:
        return None

    severity = sum(evidence[s]["deviation_sd"] for s in affected) / len(affected)
    sens = config.sensitivity_level if config else SensitivityLevel.balanced

    return WellbeingAnomaly(
        anomaly_type=AnomalyType.broad_disengagement,
        severity=round(severity, 2),
        affected_subjects=affected,
        evidence_json=evidence,
        parent_message=(
            f"We've noticed a change in {child_name}'s engagement across several "
            f"subjects this week. This sometimes reflects factors outside the "
            f"curriculum. You know your child best."
        ),
        sensitivity_level=sens,
    )


def _detect_frustration_spike(
    baselines: dict,
    recent: dict,
    config: WellbeingConfig | None,
    child_name: str,
) -> WellbeingAnomaly | None:
    """Frustration frequency doubles across 2+ subjects."""
    affected = []
    evidence = {}

    for subj, baseline in baselines["subjects"].items():
        recent_subj = recent["subjects"].get(subj)
        if not recent_subj:
            continue

        bl_freq = baseline["frustration_frequency"]
        recent_freq = recent_subj["frustration_frequency"]

        if bl_freq > 0 and recent_freq > bl_freq * 2:
            affected.append(subj)
            evidence[subj] = {
                "baseline_frequency": bl_freq,
                "recent_frequency": recent_freq,
                "ratio": round(recent_freq / max(bl_freq, 0.001), 2),
            }
        elif bl_freq == 0 and recent_freq > 0.3:
            affected.append(subj)
            evidence[subj] = {
                "baseline_frequency": 0,
                "recent_frequency": recent_freq,
                "ratio": float("inf"),
            }

    if len(affected) < 2:
        return None

    severity = sum(
        evidence[s].get("ratio", 2.0) if evidence[s].get("ratio") != float("inf") else 3.0
        for s in affected
    ) / len(affected)
    sens = config.sensitivity_level if config else SensitivityLevel.balanced

    return WellbeingAnomaly(
        anomaly_type=AnomalyType.frustration_spike,
        severity=round(min(severity, 5.0), 2),
        affected_subjects=affected,
        evidence_json=evidence,
        parent_message=(
            f"{child_name} has shown increased difficulty across multiple areas "
            f"recently. This may be a temporary phase, or it may indicate the "
            f"current workload needs adjustment."
        ),
        sensitivity_level=sens,
    )


async def _detect_performance_cliff(
    db: AsyncSession,
    baselines: dict,
    recent: dict,
    config: WellbeingConfig | None,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    child_name: str,
) -> WellbeingAnomaly | None:
    """Confidence drops > threshold SD across 3+ subjects in < 7 days."""
    threshold = get_effective_threshold(config, "performance_cliff")

    # Compute 7-day window for cliff detection
    recent_7 = await compute_recent_window(db, child_id, household_id, window_days=7)
    if not recent_7 or not recent_7["subjects"]:
        return None

    affected = []
    evidence = {}

    for subj, baseline in baselines["subjects"].items():
        recent_7_subj = recent_7["subjects"].get(subj)
        recent_14_subj = recent["subjects"].get(subj)
        if not recent_7_subj:
            continue

        bl_mean = baseline["evaluator_confidence_mean"]
        bl_std = baseline["evaluator_confidence_std"]
        r7_mean = recent_7_subj.get("evaluator_confidence_mean", bl_mean)
        r14_mean = recent_14_subj.get("evaluator_confidence_mean", bl_mean) if recent_14_subj else bl_mean

        if bl_std > 0:
            deviation_7 = (bl_mean - r7_mean) / bl_std
            deviation_14 = (bl_mean - r14_mean) / bl_std

            # Cliff = 7-day drop is sharper than 14-day (recent, sudden)
            if deviation_7 >= threshold and deviation_7 > deviation_14 * 0.8:
                affected.append(subj)
                evidence[subj] = {
                    "baseline_confidence": bl_mean,
                    "7day_confidence": r7_mean,
                    "14day_confidence": r14_mean,
                    "deviation_7d_sd": round(deviation_7, 2),
                    "deviation_14d_sd": round(deviation_14, 2),
                }

    if len(affected) < 3:
        return None

    severity = sum(evidence[s]["deviation_7d_sd"] for s in affected) / len(affected)
    sens = config.sensitivity_level if config else SensitivityLevel.balanced

    return WellbeingAnomaly(
        anomaly_type=AnomalyType.performance_cliff,
        severity=round(severity, 2),
        affected_subjects=affected,
        evidence_json=evidence,
        parent_message=(
            f"{child_name}'s performance has shifted noticeably in a short period "
            f"across several subjects. Sudden broad changes sometimes reflect "
            f"factors we can't see in the data."
        ),
        sensitivity_level=sens,
    )


async def _detect_session_avoidance(
    db: AsyncSession,
    baselines: dict,
    config: WellbeingConfig | None,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    child_name: str,
) -> WellbeingAnomaly | None:
    """Completion rate below 50% across all subjects for 5+ consecutive days."""
    now = datetime.now(UTC)

    # Check last 7 days of scheduled activities
    result = await db.execute(
        select(Activity.scheduled_date, Attempt.status).outerjoin(
            Attempt, and_(
                Attempt.activity_id == Activity.id,
                Attempt.child_id == child_id,
            )
        ).where(
            Activity.household_id == household_id,
            Activity.scheduled_date >= (now - timedelta(days=7)).date(),
            Activity.scheduled_date <= now.date(),
        ).order_by(Activity.scheduled_date)
    )
    rows = result.all()

    if not rows:
        return None

    # Group by day
    day_stats: dict[date, dict] = defaultdict(lambda: {"scheduled": 0, "completed": 0})
    for sched_date, attempt_status in rows:
        if sched_date is None:
            continue
        day_stats[sched_date]["scheduled"] += 1
        if attempt_status:
            status_val = attempt_status.value if hasattr(attempt_status, "value") else str(attempt_status)
            if status_val == "completed":
                day_stats[sched_date]["completed"] += 1

    # Find consecutive days with < 50% completion
    consecutive_low = 0
    low_days = []
    for day in sorted(day_stats.keys()):
        stats = day_stats[day]
        if stats["scheduled"] == 0:
            continue
        rate = stats["completed"] / stats["scheduled"]
        if rate < 0.5:
            consecutive_low += 1
            low_days.append(str(day))
        else:
            consecutive_low = 0

    if consecutive_low < 5:
        return None

    sens = config.sensitivity_level if config else SensitivityLevel.balanced

    return WellbeingAnomaly(
        anomaly_type=AnomalyType.session_avoidance,
        severity=round(consecutive_low / 5.0, 2),
        affected_subjects=list(baselines["subjects"].keys()),
        evidence_json={
            "consecutive_low_days": consecutive_low,
            "low_days": low_days[-7:],
            "day_stats": {str(d): s for d, s in sorted(day_stats.items())},
        },
        parent_message=(
            f"{child_name} has been completing fewer sessions than usual across "
            f"all subjects. This is worth a conversation. The curriculum can wait; "
            f"your child's wellbeing cannot."
        ),
        sensitivity_level=sens,
    )


# ═══════════════════════════════════════════
# Deduplication
# ═══════════════════════════════════════════


async def _anomaly_exists_recent(
    db: AsyncSession,
    child_id: uuid.UUID,
    anomaly_type: AnomalyType,
) -> bool:
    """Check if an active anomaly of this type exists within the dedup window."""
    cutoff = datetime.now(UTC) - timedelta(days=DEDUP_WINDOW_DAYS)
    result = await db.execute(
        select(func.count()).select_from(WellbeingAnomaly).where(
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.anomaly_type == anomaly_type,
            WellbeingAnomaly.status.in_([s.value for s in ACTIVE_STATUSES]),
            WellbeingAnomaly.created_at >= cutoff,
        )
    )
    return (result.scalar() or 0) > 0


# ═══════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════


async def run_wellbeing_detection(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> list[WellbeingAnomaly]:
    """Run all four detection algorithms for one child.

    Returns list of newly created anomalies (may be empty).
    """
    # 1. Fetch config
    config_result = await db.execute(
        select(WellbeingConfig).where(WellbeingConfig.child_id == child_id)
    )
    config = config_result.scalar_one_or_none()

    if config and not config.enabled:
        return []

    # Get child name
    child_result = await db.execute(select(Child.first_name).where(Child.id == child_id))
    child_row = child_result.one_or_none()
    child_name = child_row[0] if child_row else "Your child"

    # 2. Compute baselines
    baselines = await compute_child_baselines(db, child_id, household_id)
    if baselines is None:
        return []

    # 3. Compute recent window
    recent = await compute_recent_window(db, child_id, household_id)
    if recent is None or not recent["subjects"]:
        return []

    # 4. Run all algorithms
    new_anomalies: list[WellbeingAnomaly] = []

    detectors = [
        ("broad_disengagement", lambda: _detect_broad_disengagement(baselines, recent, config, child_name)),
        ("frustration_spike", lambda: _detect_frustration_spike(baselines, recent, config, child_name)),
        ("performance_cliff", lambda: _detect_performance_cliff(db, baselines, recent, config, child_id, household_id, child_name)),
        ("session_avoidance", lambda: _detect_session_avoidance(db, baselines, config, child_id, household_id, child_name)),
    ]

    for name, detector in detectors:
        try:
            result = await detector() if asyncio_iscoroutine(detector) else detector()
            if hasattr(result, "__await__"):
                result = await result
            if result is None:
                continue

            # Deduplication
            atype = AnomalyType(name)
            if await _anomaly_exists_recent(db, child_id, atype):
                continue

            result.child_id = child_id
            result.household_id = household_id
            db.add(result)
            new_anomalies.append(result)

            # Audit log
            try:
                from app.models.enums import AuditAction
                from app.models.operational import AuditLog
                db.add(AuditLog(
                    household_id=household_id,
                    action=AuditAction.create,
                    resource_type="wellbeing_anomaly",
                    resource_id=result.id,
                    details={
                        "anomaly_type": name,
                        "severity": result.severity,
                        "affected_subjects": result.affected_subjects,
                    },
                ))
            except Exception:
                pass

        except Exception:
            logger.exception("Wellbeing detector '%s' failed for child %s", name, child_id)

    if new_anomalies:
        await db.flush()

    return new_anomalies


def asyncio_iscoroutine(fn):
    """Check if calling fn() would return a coroutine."""
    import asyncio
    import inspect
    return inspect.iscoroutinefunction(fn)
