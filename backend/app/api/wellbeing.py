"""Wellbeing Anomaly API — parent-only anomaly management and configuration.

# PARENT-ONLY: These endpoints must NEVER be accessible from child auth.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.enums import (
    AnomalyStatus,
    AuditAction,
    GovernanceAction,
)
from app.models.governance import GovernanceEvent
from app.models.identity import Child, User
from app.models.operational import AuditLog
from app.models.wellbeing import WellbeingAnomaly, WellbeingConfig

router = APIRouter(tags=["wellbeing"])


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


# ── GET /children/{child_id}/wellbeing/anomalies ──


@router.get("/children/{child_id}/wellbeing/anomalies")
async def list_anomalies(
    child_id: uuid.UUID,
    status: str | None = Query(None),
    anomaly_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Paginated list of wellbeing anomalies for a child. PARENT-ONLY."""
    await _get_child_or_404(db, child_id, user.household_id)

    query = select(WellbeingAnomaly).where(
        WellbeingAnomaly.child_id == child_id,
        WellbeingAnomaly.household_id == user.household_id,
    )
    if status:
        query = query.where(WellbeingAnomaly.status == status)
    if anomaly_type:
        query = query.where(WellbeingAnomaly.anomaly_type == anomaly_type)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(WellbeingAnomaly.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    anomalies = result.scalars().all()

    return {
        "items": [_serialize(a) for a in anomalies],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


# ── GET /children/{child_id}/wellbeing/anomalies/{anomaly_id} ──


@router.get("/children/{child_id}/wellbeing/anomalies/{anomaly_id}")
async def get_anomaly(
    child_id: uuid.UUID,
    anomaly_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Single anomaly with full evidence. PARENT-ONLY."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(WellbeingAnomaly).where(
            WellbeingAnomaly.id == anomaly_id,
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.household_id == user.household_id,
        )
    )
    anomaly = result.scalar_one_or_none()
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly not found")

    data = _serialize(anomaly)
    data["evidence_json"] = anomaly.evidence_json
    return data


# ── PATCH /children/{child_id}/wellbeing/anomalies/{anomaly_id}/status ──


class StatusUpdate(BaseModel):
    status: str
    parent_response: str | None = None


@router.patch("/children/{child_id}/wellbeing/anomalies/{anomaly_id}/status")
async def update_anomaly_status(
    child_id: uuid.UUID,
    anomaly_id: uuid.UUID,
    body: StatusUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Update anomaly status. PARENT-ONLY."""
    await _get_child_or_404(db, child_id, user.household_id)

    valid = {"acknowledged", "dismissed", "resolved"}
    if body.status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {', '.join(valid)}")

    result = await db.execute(
        select(WellbeingAnomaly).where(
            WellbeingAnomaly.id == anomaly_id,
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.household_id == user.household_id,
        )
    )
    anomaly = result.scalar_one_or_none()
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly not found")

    prev_status = anomaly.status.value if hasattr(anomaly.status, "value") else str(anomaly.status)
    atype = anomaly.anomaly_type.value if hasattr(anomaly.anomaly_type, "value") else str(anomaly.anomaly_type)

    if body.status == "dismissed":
        from app.services.wellbeing_detection import record_dismissal

        await record_dismissal(db, anomaly_id, user.household_id, body.parent_response)
    else:
        anomaly.status = body.status
        if body.parent_response:
            anomaly.parent_response = body.parent_response

    action_map = {
        "acknowledged": "wellbeing_anomaly_acknowledged",
        "dismissed": "wellbeing_anomaly_dismissed",
        "resolved": "wellbeing_anomaly_resolved",
    }

    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="wellbeing_anomaly",
            target_id=anomaly.id,
            reason=f"{action_map[body.status]}: {atype}",
            metadata_={
                "action": action_map[body.status],
                "anomaly_type": atype,
                "previous_status": prev_status,
                "new_status": body.status,
                "child_id": str(child_id),
            },
        )
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.update,
            resource_type="wellbeing_anomaly",
            resource_id=anomaly.id,
            details={"action": action_map[body.status], "previous_status": prev_status},
        )
    )

    await db.flush()
    await db.commit()
    return {"status": body.status, "anomaly_id": str(anomaly_id)}


# ── GET /children/{child_id}/wellbeing/config ──


@router.get("/children/{child_id}/wellbeing/config")
async def get_config(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Returns wellbeing config or defaults. PARENT-ONLY."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(WellbeingConfig).where(
            WellbeingConfig.child_id == child_id,
            WellbeingConfig.household_id == user.household_id,
        )
    )
    config = result.scalar_one_or_none()

    if config is None:
        return {
            "enabled": True,
            "sensitivity_level": "balanced",
            "custom_thresholds": {},
            "threshold_adjustments": {},
            "total_false_positives": 0,
            "is_default": True,
        }

    return {
        "enabled": config.enabled,
        "sensitivity_level": config.sensitivity_level.value
        if hasattr(config.sensitivity_level, "value")
        else str(config.sensitivity_level),
        "custom_thresholds": config.custom_thresholds,
        "threshold_adjustments": config.threshold_adjustments,
        "total_false_positives": config.total_false_positives,
        "is_default": False,
    }


# ── PATCH /children/{child_id}/wellbeing/config ──


class ConfigUpdate(BaseModel):
    enabled: bool | None = None
    sensitivity_level: str | None = None
    custom_thresholds: dict | None = None


@router.patch("/children/{child_id}/wellbeing/config")
async def update_config(
    child_id: uuid.UUID,
    body: ConfigUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Update wellbeing config. Merges custom_thresholds. PARENT-ONLY."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(WellbeingConfig).where(
            WellbeingConfig.child_id == child_id,
            WellbeingConfig.household_id == user.household_id,
        )
    )
    config = result.scalar_one_or_none()

    if config is None:
        config = WellbeingConfig(child_id=child_id, household_id=user.household_id)
        db.add(config)
        await db.flush()

    changes = {}

    if body.enabled is not None:
        config.enabled = body.enabled
        changes["enabled"] = body.enabled

    if body.sensitivity_level is not None:
        valid_levels = {"conservative", "balanced", "sensitive"}
        if body.sensitivity_level not in valid_levels:
            raise HTTPException(status_code=400, detail=f"Must be one of: {', '.join(valid_levels)}")
        config.sensitivity_level = body.sensitivity_level
        changes["sensitivity_level"] = body.sensitivity_level

    if body.custom_thresholds is not None:
        current = dict(config.custom_thresholds or {})
        for key, updates in body.custom_thresholds.items():
            if not isinstance(updates, dict):
                raise HTTPException(status_code=400, detail=f"Thresholds for '{key}' must be an object")
            existing = current.get(key, {})
            existing.update(updates)
            current[key] = existing
        config.custom_thresholds = current
        changes["custom_thresholds"] = body.custom_thresholds

    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="wellbeing_config",
            target_id=config.id,
            reason=f"wellbeing_config_updated: {list(changes.keys())}",
            metadata_={"changes": changes, "child_id": str(child_id)},
        )
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.update,
            resource_type="wellbeing_config",
            resource_id=config.id,
            details=changes,
        )
    )

    await db.flush()
    await db.commit()
    return {"status": "updated", "changes": changes}


# ── GET /children/{child_id}/wellbeing/summary ──


@router.get("/children/{child_id}/wellbeing/summary")
async def get_summary(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Aggregate wellbeing summary. PARENT-ONLY."""
    await _get_child_or_404(db, child_id, user.household_id)

    active_statuses = [AnomalyStatus.detected.value, AnomalyStatus.notified.value, AnomalyStatus.acknowledged.value]

    # Active count
    total_active_r = await db.execute(
        select(func.count())
        .select_from(WellbeingAnomaly)
        .where(
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.household_id == user.household_id,
            WellbeingAnomaly.status.in_(active_statuses),
        )
    )
    total_active = total_active_r.scalar() or 0

    # By type
    type_r = await db.execute(
        select(WellbeingAnomaly.anomaly_type, func.count())
        .where(
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.household_id == user.household_id,
            WellbeingAnomaly.status.in_(active_statuses),
        )
        .group_by(WellbeingAnomaly.anomaly_type)
    )
    by_type = {r[0].value if hasattr(r[0], "value") else str(r[0]): r[1] for r in type_r.all()}

    # By status
    status_r = await db.execute(
        select(WellbeingAnomaly.status, func.count())
        .where(
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.household_id == user.household_id,
            WellbeingAnomaly.status.in_(active_statuses),
        )
        .group_by(WellbeingAnomaly.status)
    )
    by_status = {r[0].value if hasattr(r[0], "value") else str(r[0]): r[1] for r in status_r.all()}

    # Resolved and dismissed totals
    resolved_r = await db.execute(
        select(func.count())
        .select_from(WellbeingAnomaly)
        .where(
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.status == AnomalyStatus.resolved.value,
        )
    )
    dismissed_r = await db.execute(
        select(func.count())
        .select_from(WellbeingAnomaly)
        .where(
            WellbeingAnomaly.child_id == child_id,
            WellbeingAnomaly.status == AnomalyStatus.dismissed.value,
        )
    )

    # Config
    config_r = await db.execute(select(WellbeingConfig).where(WellbeingConfig.child_id == child_id))
    config = config_r.scalar_one_or_none()

    return {
        "total_active": total_active,
        "by_type": by_type,
        "by_status": by_status,
        "total_resolved": resolved_r.scalar() or 0,
        "total_dismissed": dismissed_r.scalar() or 0,
        "sensitivity_level": (
            config.sensitivity_level.value if config and hasattr(config.sensitivity_level, "value") else "balanced"
        ),
        "enabled": config.enabled if config else True,
        "threshold_adjustments": config.threshold_adjustments if config else {},
    }


# ── Serialization ──


def _serialize(a: WellbeingAnomaly) -> dict:
    return {
        "id": str(a.id),
        "anomaly_type": a.anomaly_type.value if hasattr(a.anomaly_type, "value") else str(a.anomaly_type),
        "severity": a.severity,
        "affected_subjects": a.affected_subjects or [],
        "parent_message": a.parent_message,
        "status": a.status.value if hasattr(a.status, "value") else str(a.status),
        "sensitivity_level": a.sensitivity_level.value
        if hasattr(a.sensitivity_level, "value")
        else str(a.sensitivity_level),
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "false_positive": a.false_positive,
        "parent_response": a.parent_response,
    }
