"""Learner Intelligence API — read, observe, override."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import Child, User
from app.models.intelligence import LearnerIntelligence
from app.services.intelligence import get_intelligence_context

router = APIRouter(tags=["intelligence"])


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


class AddObservationRequest(BaseModel):
    observation: str


class OverrideRequest(BaseModel):
    field: str  # e.g. "subject_patterns.math.strengths"
    value: object  # The replacement value


@router.get("/children/{child_id}/intelligence")
async def get_intelligence(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Returns the full intelligence profile for a child."""
    await _get_child_or_404(db, child_id, user.household_id)
    context = await get_intelligence_context(db, child_id, user.household_id)
    if not context:
        return {"profile": None, "message": "No intelligence data yet. It builds as your child completes activities."}

    # Also return the raw profile for full transparency
    result = await db.execute(
        select(LearnerIntelligence).where(
            LearnerIntelligence.child_id == child_id,
            LearnerIntelligence.household_id == user.household_id,
        )
    )
    profile = result.scalar_one_or_none()

    return {
        "summary": context,
        "raw": {
            "learning_style_observations": profile.learning_style_observations if profile else [],
            "subject_patterns": profile.subject_patterns if profile else {},
            "engagement_patterns": profile.engagement_patterns if profile else {},
            "tutor_interaction_analysis": profile.tutor_interaction_analysis if profile else {},
            "pace_trends": profile.pace_trends if profile else {},
            "parent_observations": profile.parent_observations if profile else [],
            "governance_learned_preferences": profile.governance_learned_preferences if profile else {},
            "observation_count": profile.observation_count if profile else 0,
            "last_updated_at": profile.last_updated_at.isoformat() if profile and profile.last_updated_at else None,
        },
    }


@router.put("/children/{child_id}/intelligence/observations")
async def add_observation(
    child_id: uuid.UUID,
    body: AddObservationRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Parent adds a manual observation. Parent's word is law."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
    profile = result.scalar_one_or_none()

    if not profile:
        profile = LearnerIntelligence(
            child_id=child_id,
            household_id=user.household_id,
        )
        db.add(profile)
        await db.flush()

    observations = list(profile.parent_observations or [])
    observations.append(
        {
            "observation": body.observation.strip(),
            "created_at": datetime.now(UTC).isoformat(),
            "created_by": str(user.id),
        }
    )
    profile.parent_observations = observations
    profile.last_updated_at = datetime.now(UTC)
    await db.flush()
    await db.commit()

    return {"status": "added", "count": len(observations)}


@router.delete("/children/{child_id}/intelligence/observations/{index}")
async def remove_observation(
    child_id: uuid.UUID,
    index: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Parent removes a specific observation by index."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="No intelligence profile found")

    observations = list(profile.parent_observations or [])
    if index < 0 or index >= len(observations):
        raise HTTPException(status_code=400, detail="Invalid observation index")

    observations.pop(index)
    profile.parent_observations = observations
    profile.last_updated_at = datetime.now(UTC)
    await db.flush()
    await db.commit()

    return {"status": "removed", "count": len(observations)}


@router.put("/children/{child_id}/intelligence/override")
async def override_intelligence(
    child_id: uuid.UUID,
    body: OverrideRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Parent overrides any AI-accumulated observation. Parent governs."""
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="No intelligence profile found")

    # Parse dotted field path and set value
    parts = body.field.split(".")
    allowed_top = {
        "learning_style_observations",
        "subject_patterns",
        "engagement_patterns",
        "tutor_interaction_analysis",
        "pace_trends",
        "governance_learned_preferences",
    }
    if parts[0] not in allowed_top:
        raise HTTPException(
            status_code=400, detail=f"Cannot override field '{parts[0]}'. Allowed: {', '.join(allowed_top)}"
        )

    if len(parts) == 1:
        setattr(profile, parts[0], body.value)
    else:
        container = getattr(profile, parts[0])
        if not isinstance(container, dict):
            raise HTTPException(status_code=400, detail=f"Field '{parts[0]}' is not a dict, cannot use dotted path")
        container = dict(container)  # Ensure mutable copy
        current = container
        for part in parts[1:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = body.value
        setattr(profile, parts[0], container)

    profile.last_updated_at = datetime.now(UTC)
    await db.flush()
    await db.commit()

    return {"status": "overridden", "field": body.field}


@router.get("/household/governance-intelligence")
async def get_governance_intelligence(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Returns governance pattern analysis for the current household."""
    from app.services.governance_intelligence import analyze_governance_patterns

    return await analyze_governance_patterns(db, user.household_id)


@router.get("/children/{child_id}/achievements")
async def list_achievements(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """List earned achievements and all possible definitions."""
    await _get_child_or_404(db, child_id, user.household_id)
    from app.services.achievements import get_achievements, get_all_definitions

    earned = await get_achievements(db, child_id)
    return {"earned": earned, "definitions": get_all_definitions()}


@router.get("/children/{child_id}/streak")
async def get_child_streak(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get current streak info for a child."""
    await _get_child_or_404(db, child_id, user.household_id)
    from app.services.achievements import get_streak

    return await get_streak(db, child_id, user.household_id)
