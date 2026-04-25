"""Evaluator Calibration API endpoints."""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_child_access
from app.models.calibration import CalibrationProfile, EvaluatorPrediction
from app.models.enums import GovernanceAction
from app.models.governance import GovernanceEvent
from app.models.identity import Child, User

router = APIRouter(tags=["calibration"])


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


# ── GET /children/{child_id}/calibration ──


@router.get("/children/{child_id}/calibration")
async def get_calibration_profile(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Returns the CalibrationProfile for a child."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(CalibrationProfile).where(
            CalibrationProfile.child_id == child_id,
            CalibrationProfile.household_id == user.household_id,
        )
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        # Count total predictions to show progress toward threshold
        count_result = await db.execute(
            select(func.count())
            .select_from(EvaluatorPrediction)
            .where(
                EvaluatorPrediction.child_id == child_id,
                EvaluatorPrediction.actual_outcome.isnot(None),
            )
        )
        reconciled_count = count_result.scalar() or 0
        return {
            "profile": None,
            "reconciled_predictions": reconciled_count,
            "threshold": 50,
            "message": f"{50 - reconciled_count} more reconciled reviews needed for calibration data.",
        }

    return {
        "profile": {
            "id": str(profile.id),
            "child_id": str(profile.child_id),
            "total_predictions": profile.total_predictions,
            "reconciled_predictions": profile.reconciled_predictions,
            "mean_drift": profile.mean_drift,
            "directional_bias": profile.directional_bias,
            "confidence_band_accuracy": profile.confidence_band_accuracy,
            "subject_drift_map": profile.subject_drift_map,
            "recalibration_offset": profile.recalibration_offset,
            "offset_active": profile.offset_active,
            "parent_override_offset": profile.parent_override_offset,
            "last_computed_at": profile.last_computed_at.isoformat() if profile.last_computed_at else None,
        },
        "threshold": 50,
    }


# ── GET /children/{child_id}/calibration/predictions ──


@router.get("/children/{child_id}/calibration/predictions")
async def list_predictions(
    child_id: uuid.UUID,
    reconciled_only: bool = Query(False),
    min_drift: float | None = Query(None, ge=0),
    subject: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Paginated list of evaluator predictions for a child."""
    await _get_child_or_404(db, child_id, user.household_id)

    query = select(EvaluatorPrediction).where(
        EvaluatorPrediction.child_id == child_id,
        EvaluatorPrediction.household_id == user.household_id,
    )

    if reconciled_only:
        query = query.where(EvaluatorPrediction.actual_outcome.isnot(None))
    if min_drift is not None:
        query = query.where(EvaluatorPrediction.drift_score >= min_drift)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Fetch page
    query = query.order_by(EvaluatorPrediction.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    predictions = result.scalars().all()

    items = []
    for p in predictions:
        items.append(
            {
                "id": str(p.id),
                "node_id": str(p.node_id),
                "attempt_id": str(p.attempt_id),
                "predicted_confidence": p.predicted_confidence,
                "predicted_fsrs_rating": p.predicted_fsrs_rating,
                "actual_outcome": p.actual_outcome,
                "drift_score": p.drift_score,
                "calibration_offset_applied": p.calibration_offset_applied,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "outcome_recorded_at": p.outcome_recorded_at.isoformat() if p.outcome_recorded_at else None,
            }
        )

    return {"items": items, "total": total}


# ── PATCH /children/{child_id}/calibration/offset ──


class OffsetUpdateRequest(BaseModel):
    offset_active: bool | None = None
    parent_override_offset: float | None = Field(None, ge=-0.15, le=0.15)


@router.patch("/children/{child_id}/calibration/offset")
async def update_calibration_offset(
    child_id: uuid.UUID,
    body: OffsetUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    """Toggle offset active/inactive or set a parent override offset."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(CalibrationProfile).where(
            CalibrationProfile.child_id == child_id,
            CalibrationProfile.household_id == user.household_id,
        )
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = CalibrationProfile(
            child_id=child_id,
            household_id=user.household_id,
        )
        db.add(profile)
        await db.flush()

    changes = {}
    if body.offset_active is not None:
        profile.offset_active = body.offset_active
        changes["offset_active"] = body.offset_active
    if body.parent_override_offset is not None:
        clamped = max(-0.15, min(0.15, body.parent_override_offset))
        profile.parent_override_offset = clamped
        changes["parent_override_offset"] = clamped
    elif body.parent_override_offset is None and "parent_override_offset" in (body.model_fields_set or set()):
        # Explicitly set to null — clear the override
        profile.parent_override_offset = None
        changes["parent_override_offset"] = None

    # Emit governance event
    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="calibration_profile",
            target_id=profile.id,
            reason=f"Calibration offset updated: {changes}",
        )
    )

    await db.flush()
    await db.commit()

    return {"status": "updated", "changes": changes}


# ── GET /children/{child_id}/calibration/drift-history ──


@router.get("/children/{child_id}/calibration/drift-history")
async def get_drift_history(
    child_id: uuid.UUID,
    weeks: int = Query(12, ge=1, le=52),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Time series of mean drift grouped by week."""
    await _get_child_or_404(db, child_id, user.household_id)

    cutoff = datetime.now(UTC) - timedelta(weeks=weeks)

    result = await db.execute(
        select(EvaluatorPrediction)
        .where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.household_id == user.household_id,
            EvaluatorPrediction.actual_outcome.isnot(None),
            EvaluatorPrediction.outcome_recorded_at >= cutoff,
        )
        .order_by(EvaluatorPrediction.outcome_recorded_at)
    )
    predictions = result.scalars().all()

    # Group by week
    weekly: dict[str, list[float]] = {}
    for p in predictions:
        if p.drift_score is None or p.outcome_recorded_at is None:
            continue
        # ISO week start (Monday)
        week_start = p.outcome_recorded_at.date()
        week_start = week_start - timedelta(days=week_start.weekday())
        key = week_start.isoformat()
        weekly.setdefault(key, []).append(p.drift_score)

    series = []
    for week_key in sorted(weekly.keys()):
        drifts = weekly[week_key]
        series.append(
            {
                "week": week_key,
                "mean_drift": round(sum(drifts) / len(drifts), 3),
                "count": len(drifts),
            }
        )

    return {"series": series, "weeks_requested": weeks}


# ── GET /children/{child_id}/calibration/temporal-drift ──


@router.get("/children/{child_id}/calibration/temporal-drift")
async def get_temporal_drift(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Temporal drift analysis with trend detection."""
    await _get_child_or_404(db, child_id, user.household_id)
    from app.services.calibration import compute_temporal_drift

    return await compute_temporal_drift(db, child_id, user.household_id)


# ── GET /children/{child_id}/calibration/confidence-distribution ──


@router.get("/children/{child_id}/calibration/confidence-distribution")
async def get_confidence_distribution(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Confidence score distribution histogram."""
    await _get_child_or_404(db, child_id, user.household_id)
    from app.services.calibration import compute_confidence_distribution

    return await compute_confidence_distribution(db, child_id, user.household_id)


# ── GET /children/{child_id}/calibration/subject-detail ──


@router.get("/children/{child_id}/calibration/subject-detail")
async def get_subject_detail(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Per-subject calibration detail with recommendations."""
    await _get_child_or_404(db, child_id, user.household_id)
    from app.services.calibration import compute_subject_calibration_detail

    subjects = await compute_subject_calibration_detail(db, child_id, user.household_id)
    return {"subjects": subjects}


# ── GET /children/{child_id}/calibration/export ──


@router.get("/children/{child_id}/calibration/export")
async def export_calibration_data(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Full calibration data export for a child. Parent's data."""
    await _get_child_or_404(db, child_id, user.household_id)

    from app.models.calibration import CalibrationSnapshot

    # Profile
    profile_result = await db.execute(
        select(CalibrationProfile).where(
            CalibrationProfile.child_id == child_id,
            CalibrationProfile.household_id == user.household_id,
        )
    )
    profile = profile_result.scalar_one_or_none()

    # Snapshots
    snap_result = await db.execute(
        select(CalibrationSnapshot)
        .where(
            CalibrationSnapshot.child_id == child_id,
            CalibrationSnapshot.household_id == user.household_id,
        )
        .order_by(CalibrationSnapshot.computed_at.desc())
    )
    snapshots = snap_result.scalars().all()

    # All predictions with outcomes
    pred_result = await db.execute(
        select(EvaluatorPrediction)
        .where(
            EvaluatorPrediction.child_id == child_id,
            EvaluatorPrediction.household_id == user.household_id,
        )
        .order_by(EvaluatorPrediction.created_at.desc())
    )
    predictions = pred_result.scalars().all()

    return {
        "child_id": str(child_id),
        "exported_at": datetime.now(UTC).isoformat(),
        "profile": {
            "total_predictions": profile.total_predictions,
            "reconciled_predictions": profile.reconciled_predictions,
            "mean_drift": profile.mean_drift,
            "directional_bias": profile.directional_bias,
            "recalibration_offset": profile.recalibration_offset,
            "offset_active": profile.offset_active,
            "parent_override_offset": profile.parent_override_offset,
            "confidence_band_accuracy": profile.confidence_band_accuracy,
            "subject_drift_map": profile.subject_drift_map,
            "last_computed_at": profile.last_computed_at.isoformat() if profile.last_computed_at else None,
        }
        if profile
        else None,
        "snapshots": [
            {
                "computed_at": s.computed_at.isoformat() if s.computed_at else None,
                "mean_drift": s.mean_drift,
                "directional_bias": s.directional_bias,
                "recalibration_offset": s.recalibration_offset,
                "reconciled_count": s.reconciled_count,
                "confidence_band_accuracy": s.confidence_band_accuracy,
                "subject_drift_map": s.subject_drift_map,
            }
            for s in snapshots
        ],
        "predictions": [
            {
                "id": str(p.id),
                "node_id": str(p.node_id),
                "attempt_id": str(p.attempt_id),
                "predicted_confidence": p.predicted_confidence,
                "predicted_fsrs_rating": p.predicted_fsrs_rating,
                "actual_outcome": p.actual_outcome,
                "drift_score": p.drift_score,
                "calibration_offset_applied": p.calibration_offset_applied,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "outcome_recorded_at": p.outcome_recorded_at.isoformat() if p.outcome_recorded_at else None,
            }
            for p in predictions
        ],
    }
