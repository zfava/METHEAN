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

from app.models.calibration import CalibrationProfile, EvaluatorPrediction
from app.models.enums import AlertSeverity, AlertStatus, AuditAction, GovernanceAction
from app.models.evidence import Alert
from app.models.operational import AuditLog

logger = logging.getLogger(__name__)

# Minimum predictions needed before recomputation produces non-zero offsets
MIN_PREDICTIONS_FOR_CALIBRATION = 50


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

    # 5. recalibration_offset
    if profile.parent_override_offset is not None:
        # Parent override takes precedence
        profile.recalibration_offset = max(-0.15, min(0.15, profile.parent_override_offset))
    elif abs(profile.directional_bias) > 0.3:
        raw_offset = -profile.directional_bias * 0.3
        profile.recalibration_offset = max(-0.15, min(0.15, raw_offset))
    else:
        profile.recalibration_offset = 0.0

    profile.last_computed_at = now

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
