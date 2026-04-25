"""Learner Style Vector API — read, override, bound."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_active_subscription, require_child_access
from app.models.enums import AuditAction, GovernanceAction
from app.models.governance import GovernanceEvent
from app.models.identity import Child, User
from app.models.intelligence import LearnerIntelligence
from app.models.operational import AuditLog
from app.models.style_vector import LearnerStyleVector

router = APIRouter(tags=["style-vector"], dependencies=[Depends(require_active_subscription)])

# Valid dimensions with their value ranges
VALID_DIMENSIONS: dict[str, dict[str, Any]] = {
    "optimal_session_minutes": {"type": "int", "min": 10, "max": 60},
    "socratic_responsiveness": {"type": "float", "min": 0.0, "max": 1.0},
    "frustration_threshold": {"type": "float", "min": 0.0, "max": 1.0},
    "recovery_rate": {"type": "float", "min": 0.0, "max": 1.0},
    "time_of_day_peak": {"type": "int", "min": 0, "max": 23},
    "modality_preference": {"type": "str", "values": ["visual", "auditory", "kinesthetic", "reading_writing", "mixed"]},
    "pacing_preference": {"type": "float", "min": -1.0, "max": 1.0},
    "independence_level": {"type": "float", "min": 0.0, "max": 1.0},
    "attention_pattern": {"type": "str", "values": ["sustained", "burst", "variable"]},
}


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


def _validate_dimension(dimension: str) -> None:
    if dimension not in VALID_DIMENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid dimension '{dimension}'. Valid: {', '.join(VALID_DIMENSIONS.keys())}",
        )


def _validate_value(dimension: str, value: Any) -> None:
    spec = VALID_DIMENSIONS[dimension]
    if spec["type"] == "str":
        if value not in spec["values"]:
            raise HTTPException(status_code=400, detail=f"Value must be one of: {spec['values']}")
    elif spec["type"] == "int" or spec["type"] == "float":
        if not isinstance(value, (int, float)) or value < spec["min"] or value > spec["max"]:
            raise HTTPException(status_code=400, detail=f"Value must be {spec['min']}-{spec['max']}")


def _serialize_vector(v: LearnerStyleVector) -> dict:
    return {
        "id": str(v.id),
        "child_id": str(v.child_id),
        "optimal_session_minutes": v.optimal_session_minutes,
        "socratic_responsiveness": v.socratic_responsiveness,
        "frustration_threshold": v.frustration_threshold,
        "recovery_rate": v.recovery_rate,
        "time_of_day_peak": v.time_of_day_peak,
        "subject_affinity_map": v.subject_affinity_map,
        "modality_preference": v.modality_preference,
        "pacing_preference": v.pacing_preference,
        "independence_level": v.independence_level,
        "attention_pattern": v.attention_pattern,
        "data_points_count": v.data_points_count,
        "dimensions_active": v.dimensions_active,
        "parent_overrides": v.parent_overrides,
        "parent_bounds": v.parent_bounds,
        "last_computed_at": v.last_computed_at.isoformat() if v.last_computed_at else None,
    }


# ── GET /children/{child_id}/style-vector ──


@router.get("/children/{child_id}/style-vector")
async def get_style_vector(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Returns the full LearnerStyleVector for a child."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(LearnerStyleVector).where(
            LearnerStyleVector.child_id == child_id,
            LearnerStyleVector.household_id == user.household_id,
        )
    )
    vector = result.scalar_one_or_none()

    if vector is None:
        # Check how much data exists
        intel_result = await db.execute(
            select(LearnerIntelligence.observation_count).where(
                LearnerIntelligence.child_id == child_id,
            )
        )
        row = intel_result.one_or_none()
        obs_count = row[0] if row else 0
        return {
            "vector": None,
            "observation_count": obs_count,
            "threshold": 20,
            "message": f"{max(0, 20 - obs_count)} more observations needed before style analysis activates.",
        }

    return {"vector": _serialize_vector(vector)}


# ── PATCH /children/{child_id}/style-vector/overrides ──


class OverrideRequest(BaseModel):
    dimension: str
    value: Any = None
    locked: bool = True


@router.patch("/children/{child_id}/style-vector/overrides")
async def set_style_override(
    child_id: uuid.UUID,
    body: OverrideRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    """Lock or unlock a parent override on a style dimension."""
    await _get_child_or_404(db, child_id, user.household_id)
    _validate_dimension(body.dimension)

    # Get or create vector
    result = await db.execute(
        select(LearnerStyleVector).where(
            LearnerStyleVector.child_id == child_id,
            LearnerStyleVector.household_id == user.household_id,
        )
    )
    vector = result.scalar_one_or_none()
    if vector is None:
        vector = LearnerStyleVector(child_id=child_id, household_id=user.household_id)
        db.add(vector)
        await db.flush()

    overrides = dict(vector.parent_overrides or {})
    old_value = overrides.get(body.dimension)

    if body.locked:
        if body.value is None:
            raise HTTPException(status_code=400, detail="Value required when locking a dimension")
        _validate_value(body.dimension, body.value)
        overrides[body.dimension] = {"value": body.value, "locked": True}
        action = "style_override_set"
    else:
        overrides.pop(body.dimension, None)
        action = "style_override_removed"

    vector.parent_overrides = overrides

    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="learner_style_vector",
            target_id=vector.id,
            reason=f"{action}: {body.dimension}",
            metadata_={
                "action": action,
                "dimension": body.dimension,
                "old_value": old_value,
                "new_value": overrides.get(body.dimension),
                "child_id": str(child_id),
            },
        )
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.update,
            resource_type="learner_style_vector",
            resource_id=vector.id,
            details={"action": action, "dimension": body.dimension},
        )
    )

    await db.flush()
    await db.commit()
    return {"status": action, "dimension": body.dimension, "overrides": overrides}


# ── PATCH /children/{child_id}/style-vector/bounds ──


class BoundsRequest(BaseModel):
    dimension: str
    min: float | int | None = None
    max: float | int | None = None


@router.patch("/children/{child_id}/style-vector/bounds")
async def set_style_bounds(
    child_id: uuid.UUID,
    body: BoundsRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    """Set or remove parent bounds on a style dimension."""
    await _get_child_or_404(db, child_id, user.household_id)
    _validate_dimension(body.dimension)

    spec = VALID_DIMENSIONS[body.dimension]
    if spec["type"] == "str":
        raise HTTPException(status_code=400, detail="Bounds not applicable to string dimensions")

    # Get or create vector
    result = await db.execute(
        select(LearnerStyleVector).where(
            LearnerStyleVector.child_id == child_id,
            LearnerStyleVector.household_id == user.household_id,
        )
    )
    vector = result.scalar_one_or_none()
    if vector is None:
        vector = LearnerStyleVector(child_id=child_id, household_id=user.household_id)
        db.add(vector)
        await db.flush()

    bounds = dict(vector.parent_bounds or {})
    old_bounds = bounds.get(body.dimension)

    if body.min is None and body.max is None:
        # Remove bounds
        bounds.pop(body.dimension, None)
        action = "style_bound_removed"
    else:
        # Validate range
        new_bound: dict[str, float | int] = {}
        if body.min is not None:
            if body.min < spec["min"] or body.min > spec["max"]:
                raise HTTPException(status_code=400, detail=f"min must be {spec['min']}-{spec['max']}")
            new_bound["min"] = body.min
        if body.max is not None:
            if body.max < spec["min"] or body.max > spec["max"]:
                raise HTTPException(status_code=400, detail=f"max must be {spec['min']}-{spec['max']}")
            new_bound["max"] = body.max
        if body.min is not None and body.max is not None and body.min > body.max:
            raise HTTPException(status_code=400, detail="min cannot exceed max")
        bounds[body.dimension] = new_bound
        action = "style_bound_set"

    vector.parent_bounds = bounds

    db.add(
        GovernanceEvent(
            household_id=user.household_id,
            user_id=user.id,
            action=GovernanceAction.modify,
            target_type="learner_style_vector",
            target_id=vector.id,
            reason=f"{action}: {body.dimension}",
            metadata_={
                "action": action,
                "dimension": body.dimension,
                "old_bounds": old_bounds,
                "new_bounds": bounds.get(body.dimension),
                "child_id": str(child_id),
            },
        )
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.update,
            resource_type="learner_style_vector",
            resource_id=vector.id,
            details={"action": action, "dimension": body.dimension},
        )
    )

    await db.flush()
    await db.commit()
    return {"status": action, "dimension": body.dimension, "bounds": bounds}


# ── GET /children/{child_id}/style-vector/history ──


@router.get("/children/{child_id}/style-vector/history")
async def get_style_vector_history(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Returns the current vector state with timestamp as a history entry.

    Can be expanded later to return multiple snapshots.
    """
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(LearnerStyleVector).where(
            LearnerStyleVector.child_id == child_id,
            LearnerStyleVector.household_id == user.household_id,
        )
    )
    vector = result.scalar_one_or_none()

    if vector is None:
        return {"entries": [], "total": 0}

    return {
        "entries": [_serialize_vector(vector)],
        "total": 1,
    }
