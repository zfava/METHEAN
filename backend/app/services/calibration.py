"""Evaluator Calibration Service.

Tracks evaluator prediction accuracy over time and computes per-child
calibration offsets to correct systematic bias in confidence scoring.
The calibration system is purely advisory — it never blocks the
evaluator pipeline.
"""

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration import CalibrationProfile, CalibrationSnapshot, EvaluatorPrediction
from app.models.enums import AlertSeverity, AlertStatus, AuditAction, GovernanceAction
from app.models.evidence import Alert
from app.models.operational import AuditLog

logger = logging.getLogger(__name__)

# Minimum predictions needed before recomputation produces non-zero offsets
MIN_PREDICTIONS_FOR_CALIBRATION = 50

# Maximum offset change per recomputation cycle
MAX_OFFSET_STEP = 0.05


def clamp_offset_change(current: float, new: float, max_step: float = MAX_OFFSET_STEP) -> float:
    """Limit offset change to max_step per recomputation cycle."""
    delta = new - current
    if abs(delta) > max_step:
        return current + (max_step if delta > 0 else -max_step)
    return new


async def record_prediction(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
    attempt_id: uuid.UUID,
    evaluator_confidence: float,
    fsrs_rating: int,
    predicted_retention_at: datetime | None = None,
    calibration_offset_applied: float = 0.0,
) -> EvaluatorPrediction:
    """Record a new evaluator prediction for later reconciliation.

    Called after the evaluator scores an attempt and FSRS rating is computed,
    but before the FSRS card is updated.
    """
    prediction = EvaluatorPrediction(
        household_id=household_id,
        child_id=child_id,
        node_id=node_id,
        attempt_id=attempt_id,
        predicted_confidence=evaluator_confidence,
        predicted_fsrs_rating=fsrs_rating,
        predicted_retention_at=predicted_retention_at,
        calibration_offset_applied=calibration_offset_applied,
    )
    db.add(prediction)

    db.add(AuditLog(
        household_id=household_id,
        action=AuditAction.create,
        resource_type="evaluator_prediction",
        resource_id=prediction.id,
        details={
            "child_id": str(child_id),
            "node_id": str(node_id),
            "confidence": evaluator_confidence,
            "fsrs_rating": fsrs_rating,
            "offset_applied": calibration_offset_applied,
        },
    ))

    await db.flush()
    return prediction


async def reconcile_outcome(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    node_id: uuid.UUID,
    new_fsrs_rating: int,
) -> EvaluatorPrediction | None:
    """Reconcile the most recent unreconciled prediction with the actual outcome.

    Called when a child attempts a node they have previously attempted,
    providing a ground-truth signal for calibration.

    Returns the reconciled prediction, or None if no unreconciled prediction exists.
    """
    result = await db.execute(
        select(EvaluatorPrediction)
        .where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.node_id == node_id,
            EvaluatorPrediction.actual_outcome.is_(None),
        )
        .order_by(EvaluatorPrediction.created_at.desc())
        .limit(1)
    )
    prediction = result.scalar_one_or_none()

    if prediction is None:
        return None

    now = datetime.now(UTC)
    prediction.actual_outcome = new_fsrs_rating
    prediction.outcome_recorded_at = now
    prediction.drift_score = abs(prediction.predicted_fsrs_rating - new_fsrs_rating)

    db.add(AuditLog(
        household_id=household_id,
        action=AuditAction.update,
        resource_type="evaluator_prediction",
        resource_id=prediction.id,
        details={
            "child_id": str(child_id),
            "node_id": str(node_id),
            "predicted": prediction.predicted_fsrs_rating,
            "actual": new_fsrs_rating,
            "drift": prediction.drift_score,
        },
    ))

    # Alert on high drift
    if prediction.drift_score >= 2.0:
        severity = AlertSeverity.action_required if prediction.drift_score >= 3.0 else AlertSeverity.warning
        db.add(Alert(
            household_id=household_id,
            child_id=child_id,
            severity=severity,
            status=AlertStatus.unread,
            title="Evaluator Calibration Drift",
            message=(
                f"Evaluator predicted rating {prediction.predicted_fsrs_rating} "
                f"but actual was {new_fsrs_rating} (drift: {prediction.drift_score:.1f}). "
                f"The evaluator may need recalibration."
            ),
            source="calibration_drift",
            metadata_={
                "node_id": str(node_id),
                "predicted": prediction.predicted_fsrs_rating,
                "actual": new_fsrs_rating,
                "drift": prediction.drift_score,
            },
        ))

    await db.flush()
    return prediction


async def apply_calibration_offset(
    db: AsyncSession,
    raw_confidence: float,
    child_id: uuid.UUID,
) -> float:
    """Apply per-child calibration offset to raw evaluator confidence.

    CRITICAL: If this method errors for ANY reason, returns raw_confidence
    unchanged. Calibration is advisory, never blocking.
    """
    try:
        result = await db.execute(
            select(CalibrationProfile).where(
                CalibrationProfile.child_id == child_id,
            )
        )
        profile = result.scalar_one_or_none()

        if profile is None or not profile.offset_active:
            return raw_confidence

        offset = (
            profile.parent_override_offset
            if profile.parent_override_offset is not None
            else profile.recalibration_offset
        )

        adjusted = raw_confidence + offset
        return max(0.0, min(1.0, adjusted))
    except Exception:
        logger.exception("Calibration offset lookup failed for child %s — using raw confidence", child_id)
        return raw_confidence


async def recompute_profile(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> CalibrationProfile:
    """Recompute calibration profile for a child from all reconciled predictions.

    Requires MIN_PREDICTIONS_FOR_CALIBRATION (50) reconciled predictions
    to produce non-zero metrics. Below that threshold, all metrics are zeroed.
    """
    from app.models.curriculum import LearningNode

    now = datetime.now(UTC)

    # Count total and reconciled predictions
    total_count_result = await db.execute(
        select(func.count()).select_from(EvaluatorPrediction).where(
            EvaluatorPrediction.child_id == child_id,
        )
    )
    total_predictions = total_count_result.scalar() or 0

    reconciled_result = await db.execute(
        select(EvaluatorPrediction).where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.actual_outcome.isnot(None),
        )
    )
    reconciled = reconciled_result.scalars().all()
    reconciled_count = len(reconciled)

    # Get or create profile
    profile_result = await db.execute(
        select(CalibrationProfile).where(CalibrationProfile.child_id == child_id)
    )
    profile = profile_result.scalar_one_or_none()

    if profile is None:
        profile = CalibrationProfile(
            child_id=child_id,
            household_id=household_id,
        )
        db.add(profile)
        await db.flush()

    profile.total_predictions = total_predictions
    profile.reconciled_predictions = reconciled_count

    if reconciled_count < MIN_PREDICTIONS_FOR_CALIBRATION:
        # Not enough data — zero everything
        profile.mean_drift = 0.0
        profile.directional_bias = 0.0
        profile.confidence_band_accuracy = {}
        profile.subject_drift_map = {}
        profile.recalibration_offset = 0.0
        profile.last_computed_at = now
        await db.flush()
        return profile

    # 1. mean_drift
    drift_scores = [p.drift_score for p in reconciled if p.drift_score is not None]
    profile.mean_drift = sum(drift_scores) / len(drift_scores) if drift_scores else 0.0

    # 2. directional_bias: positive = evaluator too generous
    biases = [p.predicted_fsrs_rating - p.actual_outcome for p in reconciled]
    profile.directional_bias = sum(biases) / len(biases) if biases else 0.0

    # 3. confidence_band_accuracy
    bands = {
        "0.00-0.30": {"total": 0, "hits": 0},
        "0.31-0.55": {"total": 0, "hits": 0},
        "0.56-0.80": {"total": 0, "hits": 0},
        "0.81-1.00": {"total": 0, "hits": 0},
    }
    for p in reconciled:
        conf = p.predicted_confidence
        if conf <= 0.30:
            band_key = "0.00-0.30"
            expected_rating = 1  # Again
        elif conf <= 0.55:
            band_key = "0.31-0.55"
            expected_rating = 2  # Hard
        elif conf <= 0.80:
            band_key = "0.56-0.80"
            expected_rating = 3  # Good
        else:
            band_key = "0.81-1.00"
            expected_rating = 4  # Easy
        bands[band_key]["total"] += 1
        if p.actual_outcome == expected_rating:
            bands[band_key]["hits"] += 1

    profile.confidence_band_accuracy = {
        k: {
            "total": v["total"],
            "hit_rate": round(v["hits"] / v["total"], 3) if v["total"] > 0 else 0.0,
        }
        for k, v in bands.items()
    }

    # 4. subject_drift_map — join with nodes to get subject info
    node_ids = list({p.node_id for p in reconciled})
    node_result = await db.execute(
        select(LearningNode.id, LearningNode.title).where(
            LearningNode.id.in_(node_ids)
        )
    )
    node_titles = {row[0]: row[1] for row in node_result.all()}

    # Group predictions by subject (using node title as proxy since nodes don't have subject_name)
    # We'll use a simpler approach: group by node and report per-node drift
    subject_groups: dict[str, list[EvaluatorPrediction]] = {}
    for p in reconciled:
        # Use node title as subject key (nodes belong to subject-specific maps)
        title = node_titles.get(p.node_id, "unknown")
        subject_groups.setdefault(title, []).append(p)

    profile.subject_drift_map = {}
    for subj, preds in subject_groups.items():
        drifts = [p.drift_score for p in preds if p.drift_score is not None]
        biases_subj = [p.predicted_fsrs_rating - p.actual_outcome for p in preds]
        profile.subject_drift_map[subj] = {
            "mean_drift": round(sum(drifts) / len(drifts), 3) if drifts else 0.0,
            "count": len(preds),
            "bias": round(sum(biases_subj) / len(biases_subj), 3) if biases_subj else 0.0,
        }

    # 5. recalibration_offset with rate limiter
    previous_offset = profile.recalibration_offset
    if profile.parent_override_offset is not None:
        # Parent override takes precedence — no rate limiting
        target_offset = max(-0.15, min(0.15, profile.parent_override_offset))
    elif abs(profile.directional_bias) > 0.3:
        raw_offset = -profile.directional_bias * 0.3
        target_offset = max(-0.15, min(0.15, raw_offset))
    else:
        target_offset = 0.0

    # Apply rate limiter: max 0.05 change per recomputation
    rate_limited = clamp_offset_change(previous_offset, target_offset)
    if rate_limited != target_offset:
        logger.warning(
            "Calibration rate limiter activated for child %s: "
            "target=%.4f, applied=%.4f (clamped from %.4f)",
            child_id, target_offset, rate_limited, previous_offset,
        )
    profile.recalibration_offset = rate_limited

    profile.last_computed_at = now

    # 6. Save CalibrationSnapshot for historical tracking
    db.add(CalibrationSnapshot(
        household_id=household_id,
        child_id=child_id,
        mean_drift=profile.mean_drift,
        directional_bias=profile.directional_bias,
        recalibration_offset=profile.recalibration_offset,
        reconciled_count=reconciled_count,
        confidence_band_accuracy=profile.confidence_band_accuracy,
        subject_drift_map=profile.subject_drift_map,
        computed_at=now,
    ))

    # Emit audit and governance events
    db.add(AuditLog(
        household_id=household_id,
        action=AuditAction.update,
        resource_type="calibration_profile",
        resource_id=profile.id,
        details={
            "child_id": str(child_id),
            "mean_drift": profile.mean_drift,
            "directional_bias": profile.directional_bias,
            "offset": profile.recalibration_offset,
            "previous_offset": previous_offset,
            "target_offset": target_offset,
            "rate_limited": rate_limited != target_offset,
            "reconciled_count": reconciled_count,
        },
    ))

    from app.models.governance import GovernanceEvent
    db.add(GovernanceEvent(
        household_id=household_id,
        user_id=None,
        action=GovernanceAction.modify,
        target_type="calibration_profile",
        target_id=profile.id,
        reason=f"Calibration profile recomputed: mean_drift={profile.mean_drift:.3f}, bias={profile.directional_bias:.3f}, offset={profile.recalibration_offset:.3f}",
    ))

    await db.flush()
    return profile


async def run_calibration_health_check(db: AsyncSession) -> dict:
    """System-level health check across all calibration profiles.

    Emits alerts for:
    - Individual children with mean_drift > 2.0 and 100+ predictions
    - System-wide average drift > 1.5
    """
    result = await db.execute(select(CalibrationProfile))
    profiles = result.scalars().all()

    if not profiles:
        return {"profiles_checked": 0, "alerts_created": 0}

    alerts_created = 0

    # Per-child critical drift check
    for p in profiles:
        if p.mean_drift > 2.0 and p.reconciled_predictions >= 100:
            db.add(Alert(
                household_id=p.household_id,
                child_id=p.child_id,
                severity=AlertSeverity.action_required,
                status=AlertStatus.unread,
                title="Critical Calibration Drift",
                message=(
                    f"Evaluator calibration drift is critically high "
                    f"(mean_drift={p.mean_drift:.2f}) after {p.reconciled_predictions} "
                    f"reconciled predictions. Consider reviewing evaluator configuration."
                ),
                source="calibration_health_check",
                metadata_={
                    "mean_drift": p.mean_drift,
                    "reconciled_predictions": p.reconciled_predictions,
                    "directional_bias": p.directional_bias,
                },
            ))
            alerts_created += 1

    # System-wide average drift check
    drifts = [p.mean_drift for p in profiles if p.reconciled_predictions >= MIN_PREDICTIONS_FOR_CALIBRATION]
    if drifts:
        avg_drift = sum(drifts) / len(drifts)
        if avg_drift > 1.5:
            # Use the first profile's household for the system alert
            db.add(Alert(
                household_id=profiles[0].household_id,
                severity=AlertSeverity.action_required,
                status=AlertStatus.unread,
                title="System-Wide Calibration Drift",
                message=(
                    f"Average calibration drift across {len(drifts)} children "
                    f"is {avg_drift:.2f}, exceeding the 1.5 threshold. "
                    f"The evaluator may have a systemic accuracy issue."
                ),
                source="calibration_health_check",
                metadata_={
                    "average_drift": avg_drift,
                    "children_count": len(drifts),
                },
            ))
            alerts_created += 1

    logger.info(
        "Calibration health check: %d profiles checked, avg_drift=%.3f, %d alerts",
        len(profiles),
        sum(drifts) / len(drifts) if drifts else 0.0,
        alerts_created,
    )

    await db.flush()
    return {"profiles_checked": len(profiles), "alerts_created": alerts_created}


async def compute_temporal_drift(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> dict:
    """Compute weekly drift trends with linear regression.

    Returns: weekly_buckets, trend, trend_slope.
    """
    from datetime import timedelta

    result = await db.execute(
        select(EvaluatorPrediction).where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.household_id == household_id,
            EvaluatorPrediction.actual_outcome.isnot(None),
        ).order_by(EvaluatorPrediction.created_at)
    )
    predictions = result.scalars().all()

    if len(predictions) < 10:
        return {"weekly_buckets": [], "trend": "insufficient_data", "trend_slope": 0.0}

    # Group by ISO week
    weekly: dict[str, list[EvaluatorPrediction]] = {}
    for p in predictions:
        if p.created_at is None:
            continue
        week_start = p.created_at.date() - timedelta(days=p.created_at.weekday())
        key = week_start.isoformat()
        weekly.setdefault(key, []).append(p)

    buckets = []
    for week_key in sorted(weekly.keys()):
        preds = weekly[week_key]
        drifts = [p.drift_score for p in preds if p.drift_score is not None]
        biases = [p.predicted_fsrs_rating - p.actual_outcome for p in preds]
        buckets.append({
            "week": week_key,
            "mean_drift": round(sum(drifts) / len(drifts), 3) if drifts else 0.0,
            "count": len(preds),
            "bias": round(sum(biases) / len(biases), 3) if biases else 0.0,
        })

    # Linear regression on weekly mean_drift
    if len(buckets) < 2:
        return {"weekly_buckets": buckets, "trend": "insufficient_data", "trend_slope": 0.0}

    n = len(buckets)
    x_vals = list(range(n))
    y_vals = [b["mean_drift"] for b in buckets]
    x_mean = sum(x_vals) / n
    y_mean = sum(y_vals) / n
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)
    slope = numerator / denominator if denominator != 0 else 0.0

    if slope < -0.05:
        trend = "improving"
    elif slope > 0.05:
        trend = "worsening"
    else:
        trend = "stable"

    return {
        "weekly_buckets": buckets,
        "trend": trend,
        "trend_slope": round(slope, 4),
    }


async def compute_confidence_distribution(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> dict:
    """Compute histogram of predicted confidence values.

    Returns: histogram (10 bands), mean, std_dev, skew, compression_warning.
    """
    import math

    result = await db.execute(
        select(EvaluatorPrediction.predicted_confidence).where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.household_id == household_id,
        )
    )
    confidences = [row[0] for row in result.all()]

    if len(confidences) < 5:
        return {
            "histogram": [],
            "mean": 0.0,
            "std_dev": 0.0,
            "skew": 0.0,
            "compression_warning": False,
            "total": len(confidences),
        }

    # Build histogram: 10 bands of 0.1 width
    bands = [{"band": f"{i/10:.1f}-{(i+1)/10:.1f}", "count": 0} for i in range(10)]
    for c in confidences:
        idx = min(int(c * 10), 9)
        bands[idx]["count"] += 1

    n = len(confidences)
    mean = sum(confidences) / n
    variance = sum((c - mean) ** 2 for c in confidences) / n
    std_dev = math.sqrt(variance)

    # Skewness (Fisher's)
    if std_dev > 0 and n >= 3:
        skew = (sum((c - mean) ** 3 for c in confidences) / n) / (std_dev ** 3)
    else:
        skew = 0.0

    compression_warning = std_dev < 0.1

    if compression_warning:
        # Emit alert about evaluator not discriminating
        db.add(Alert(
            household_id=household_id,
            child_id=child_id,
            severity=AlertSeverity.warning,
            status=AlertStatus.unread,
            title="Evaluator Confidence Compression",
            message=(
                f"Evaluator confidence scores have very low variance "
                f"(std_dev={std_dev:.3f}). The evaluator may not be effectively "
                f"discriminating between different quality levels."
            ),
            source="calibration_confidence_compression",
            metadata_={
                "std_dev": std_dev,
                "mean": mean,
                "total_predictions": n,
            },
        ))
        await db.flush()

    return {
        "histogram": bands,
        "mean": round(mean, 3),
        "std_dev": round(std_dev, 3),
        "skew": round(skew, 3),
        "compression_warning": compression_warning,
        "total": n,
    }


async def compute_subject_calibration_detail(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> list[dict]:
    """Per-subject calibration detail with recommendations.

    Joins predictions with learning nodes to group by subject/node title.
    """
    from app.models.curriculum import LearningNode

    result = await db.execute(
        select(EvaluatorPrediction).where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.household_id == household_id,
            EvaluatorPrediction.actual_outcome.isnot(None),
        )
    )
    predictions = result.scalars().all()

    if not predictions:
        return []

    # Get node titles
    node_ids = list({p.node_id for p in predictions})
    node_result = await db.execute(
        select(LearningNode.id, LearningNode.title).where(LearningNode.id.in_(node_ids))
    )
    node_titles = {row[0]: row[1] for row in node_result.all()}

    # Group by node title
    groups: dict[str, list[EvaluatorPrediction]] = {}
    for p in predictions:
        title = node_titles.get(p.node_id, "Unknown")
        groups.setdefault(title, []).append(p)

    details = []
    for subject, preds in sorted(groups.items()):
        count = len(preds)
        drifts = [p.drift_score for p in preds if p.drift_score is not None]
        biases = [p.predicted_fsrs_rating - p.actual_outcome for p in preds]

        mean_drift = sum(drifts) / len(drifts) if drifts else 0.0
        bias = sum(biases) / len(biases) if biases else 0.0

        if count < 10:
            action = "insufficient_data"
            recommendation = f"Need {10 - count} more reconciled predictions for analysis."
        elif mean_drift < 0.5:
            action = "well_calibrated"
            recommendation = "Evaluator is accurately calibrated for this topic."
        elif mean_drift < 1.0:
            action = "offset_active"
            if bias > 0:
                recommendation = "Evaluator is slightly generous. Auto-offset is correcting."
            else:
                recommendation = "Evaluator is slightly harsh. Auto-offset is correcting."
        else:
            action = "review_recommended"
            direction = "generous" if bias > 0 else "harsh"
            recommendation = (
                f"Evaluator is significantly too {direction} for this topic "
                f"(mean drift: {mean_drift:.1f}). Review evaluation criteria."
            )

        details.append({
            "subject": subject,
            "mean_drift": round(mean_drift, 3),
            "directional_bias": round(bias, 3),
            "reconciled_count": count,
            "action": action,
            "recommendation": recommendation,
        })

    return details
