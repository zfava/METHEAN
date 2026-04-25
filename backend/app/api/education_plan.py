"""Education Plan API — multi-year educational blueprints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_active_subscription, require_child_access, require_permission
from app.models.education_plan import EducationPlan
from app.models.identity import Child, User
from app.services.education_architect import (
    approve_education_plan,
    generate_education_plan,
    generate_year_curricula,
)

router = APIRouter(tags=["education-plan"], dependencies=[Depends(require_active_subscription)])


class GeneratePlanRequest(BaseModel):
    goals: dict = Field(default_factory=dict)
    baseline_assessment: dict = Field(default_factory=dict)
    time_budget_hours_per_week: int = Field(default=25, ge=5, le=60)


class UpdatePlanRequest(BaseModel):
    name: str | None = None
    year_plans: dict | None = None
    goals: dict | None = None


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


@router.post("/children/{child_id}/education-plan/generate", status_code=201)
async def generate_plan_endpoint(
    child_id: uuid.UUID,
    body: GeneratePlanRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("plans.generate")),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)

    plan = await generate_education_plan(
        db,
        user.household_id,
        child_id,
        user.id,
        goals=body.goals,
        baseline_assessment=body.baseline_assessment,
        time_budget_hours_per_week=body.time_budget_hours_per_week,
    )

    return {
        "id": str(plan.id),
        "name": plan.name,
        "status": plan.status,
        "year_plans": plan.year_plans,
        "goals": plan.goals,
        "baseline_assessment": plan.baseline_assessment,
        "ai_run_id": str(plan.ai_run_id) if plan.ai_run_id else None,
        "created_at": plan.created_at.isoformat() if plan.created_at else None,
    }


@router.get("/children/{child_id}/education-plan")
async def get_plan(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(EducationPlan).where(
            EducationPlan.child_id == child_id,
            EducationPlan.household_id == user.household_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="No education plan exists for this child")

    return {
        "id": str(plan.id),
        "name": plan.name,
        "status": plan.status,
        "year_plans": plan.year_plans,
        "goals": plan.goals,
        "baseline_assessment": plan.baseline_assessment,
        "ai_run_id": str(plan.ai_run_id) if plan.ai_run_id else None,
        "approved_at": plan.approved_at.isoformat() if plan.approved_at else None,
        "created_at": plan.created_at.isoformat() if plan.created_at else None,
    }


@router.put("/children/{child_id}/education-plan")
async def update_plan(
    child_id: uuid.UUID,
    body: UpdatePlanRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("plans.generate")),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(EducationPlan).where(
            EducationPlan.child_id == child_id,
            EducationPlan.household_id == user.household_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="No education plan exists")

    if body.name is not None:
        plan.name = body.name
    if body.year_plans is not None:
        plan.year_plans = body.year_plans
    if body.goals is not None:
        plan.goals = body.goals

    await db.flush()
    return {"id": str(plan.id), "name": plan.name, "status": plan.status, "updated": True}


@router.post("/children/{child_id}/education-plan/approve")
async def approve_plan_endpoint(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("approve.activities")),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(EducationPlan).where(
            EducationPlan.child_id == child_id,
            EducationPlan.household_id == user.household_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="No education plan exists")

    try:
        plan = await approve_education_plan(db, plan.id, user.id, user.household_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": str(plan.id),
        "status": plan.status,
        "approved_at": plan.approved_at.isoformat() if plan.approved_at else None,
    }


@router.post("/children/{child_id}/education-plan/years/{year_key}/generate-curricula")
async def generate_curricula_endpoint(
    child_id: uuid.UUID,
    year_key: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("plans.generate")),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)

    result = await db.execute(
        select(EducationPlan).where(
            EducationPlan.child_id == child_id,
            EducationPlan.household_id == user.household_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="No education plan exists")

    try:
        proposals = await generate_year_curricula(
            db,
            plan.id,
            year_key,
            user.id,
            user.household_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"year_key": year_key, "proposals": proposals}
