"""Education Architect service.

Generates complete multi-year educational blueprints through the AI
governance gateway, stores them as EducationPlan records, and bridges
approved plans to concrete learning map generation.
"""

import json
import uuid
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import EDUCATION_ARCHITECT_SYSTEM
from app.models.education_plan import EducationPlan
from app.models.enums import GovernanceAction
from app.models.governance import GovernanceEvent
from app.models.identity import Child, ChildPreferences, Household


async def generate_education_plan(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    user_id: uuid.UUID,
    goals: dict,
    baseline_assessment: dict,
    time_budget_hours_per_week: int = 25,
) -> EducationPlan:
    """Generate a complete multi-year education plan."""

    # Fetch child
    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one()

    # Fetch preferences
    prefs_result = await db.execute(
        select(ChildPreferences).where(ChildPreferences.child_id == child_id)
    )
    prefs = prefs_result.scalar_one_or_none()

    # Fetch household philosophical profile
    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one()
    phil = household.philosophical_profile or {}

    # Calculate years to graduation
    child_age = (date.today() - child.date_of_birth).days / 365.25 if child.date_of_birth else 6
    grad_target = goals.get("graduation_target", str(date.today().year + int(18 - child_age)))
    years_remaining = max(1, int(grad_target) - date.today().year)

    # Build prompt
    user_prompt = f"""Design a complete {years_remaining}-year education plan for this child.

CHILD PROFILE:
- Name: {child.first_name}
- Age: {child_age:.1f} years
- Grade: {child.grade_level or 'K'}
- Strengths: {json.dumps(baseline_assessment.get('strengths', []))}
- Struggles: {json.dumps(baseline_assessment.get('struggles', []))}
- Diagnosed conditions: {json.dumps(baseline_assessment.get('diagnosed_conditions', []))}
- Prior education: {baseline_assessment.get('prior_education', 'homeschool')}
- Reading level: {baseline_assessment.get('reading_level', 'at_grade')}
- Math level: {baseline_assessment.get('math_level', 'at_grade')}

FAMILY PHILOSOPHY:
{json.dumps(phil, indent=2, default=str)}

GOALS:
- Graduation target: {grad_target}
- Post-graduation path: {goals.get('post_graduation', 'undecided')}
- College prep level: {goals.get('college_prep_level', 'standard')}
- Target skills: {json.dumps(goals.get('target_skills', []))}
- Parent's vision: {goals.get('parent_vision', '')}

TIME BUDGET: {time_budget_hours_per_week} hours per week

Generate year plans from {date.today().year}-{date.today().year + 1} through {int(grad_target) - 1}-{grad_target}.
Limit to the next {min(years_remaining, 5)} years for now (the plan can be extended later)."""

    # Call AI through governance gateway
    ai_result = await call_ai(
        db,
        role=AIRole.education_architect,
        system_prompt=EDUCATION_ARCHITECT_SYSTEM,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil,
    )

    output = ai_result["output"]
    year_plans = output.get("year_plans", {}) if isinstance(output, dict) else {}
    plan_name = output.get("plan_name", f"{child.first_name}'s Education Plan") if isinstance(output, dict) else f"{child.first_name}'s Education Plan"

    # Delete any existing draft plan for this child
    existing = await db.execute(
        select(EducationPlan).where(
            EducationPlan.child_id == child_id,
            EducationPlan.status == "draft",
        )
    )
    for old in existing.scalars().all():
        await db.delete(old)

    plan = EducationPlan(
        household_id=household_id,
        child_id=child_id,
        created_by=user_id,
        name=plan_name,
        status="draft",
        year_plans=year_plans,
        goals=goals,
        baseline_assessment=baseline_assessment,
        ai_run_id=ai_result["ai_run_id"],
    )
    db.add(plan)
    await db.flush()

    # Log governance event
    db.add(GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=GovernanceAction.modify,
        target_type="education_plan",
        target_id=plan.id,
        reason=f"Education plan generated for {child.first_name}",
    ))
    await db.flush()

    return plan


async def approve_education_plan(
    db: AsyncSession,
    plan_id: uuid.UUID,
    user_id: uuid.UUID,
    household_id: uuid.UUID,
) -> EducationPlan:
    """Parent approves the education plan. Status -> active."""
    result = await db.execute(
        select(EducationPlan).where(
            EducationPlan.id == plan_id,
            EducationPlan.household_id == household_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise ValueError("Plan not found")

    plan.status = "active"
    plan.approved_at = datetime.now(UTC)
    plan.approved_by = user_id

    db.add(GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=GovernanceAction.approve,
        target_type="education_plan",
        target_id=plan.id,
        reason="Education plan approved by parent",
    ))
    await db.flush()
    return plan


async def generate_year_curricula(
    db: AsyncSession,
    plan_id: uuid.UUID,
    year_key: str,
    user_id: uuid.UUID,
    household_id: uuid.UUID,
) -> list[dict]:
    """For an approved plan year, generate curriculum proposals per subject.

    Returns a list of proposals (subject name + recommended map structure)
    for parent review. The actual learning maps are created when the parent
    approves individual proposals.
    """
    result = await db.execute(
        select(EducationPlan).where(
            EducationPlan.id == plan_id,
            EducationPlan.household_id == household_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise ValueError("Plan not found")

    year_data = plan.year_plans.get(year_key, {})
    subjects = year_data.get("subjects", [])

    proposals = []
    for subj in subjects:
        proposals.append({
            "subject": subj.get("subject", "Unknown"),
            "priority": subj.get("priority", "core"),
            "hours_per_week": subj.get("hours_per_week", 3),
            "description": subj.get("description", ""),
            "approach": subj.get("approach", ""),
            "status": "proposed",
            "year_key": year_key,
        })

    return proposals
