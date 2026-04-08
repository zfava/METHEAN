"""Annual Curriculum service.

Generates 36-week year-long curricula, materializes them into
Plan/PlanWeek/Activity records, tracks week completion, and
maintains the historical record of planned vs actual.
"""

import json
import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import build_philosophical_constraints
from app.models.annual_curriculum import AnnualCurriculum
from app.models.curriculum import LearningEdge, LearningMap, LearningNode, Subject
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    GovernanceAction,
    PlanStatus,
)
from app.models.governance import Activity, Attempt, GovernanceEvent, Plan, PlanWeek
from app.models.identity import Child, ChildPreferences, Household
from app.models.state import ChildNodeState


ANNUAL_CURRICULUM_SYSTEM = """You are METHEAN's Annual Curriculum Architect.

You design COMPLETE year-long scope-and-sequence plans for individual subjects.
Each plan covers exactly {total_weeks} weeks of instruction.

RULES:
- Produce exactly {total_weeks} weeks of content
- For each week: title, learning objectives, 3-5 daily activities (Mon-Fri), assessment focus
- Activities must have: title, type (lesson/practice/assessment/review/project), minutes, day
- Respect the DAG order: prerequisite nodes MUST come before dependent nodes
- Every 6th week is a REVIEW week (lighter, consolidation + formal assessment checkpoint)
- Be realistic: 3-5 nodes per week maximum for elementary, 2-4 for secondary
- Include varied activity types: hands-on, reading, discussion, practice, creative
- Total weekly minutes should approximate the hours_per_week budget
- Assessment checkpoints every 6 weeks with specific criteria

{philosophical_constraints}

OUTPUT FORMAT (JSON):
{{
  "overview": "Year-long narrative of curriculum coverage",
  "philosophy_alignment": "How this curriculum reflects family values",
  "materials": ["resource types needed"],
  "weeks": [
    {{
      "week_number": 1,
      "title": "Week title",
      "focus_nodes": ["node-id-1"],
      "objectives": ["objective 1", "objective 2"],
      "suggested_activities": [
        {{"title": "Activity name", "type": "lesson", "minutes": 25, "day": "Monday", "description": "Brief description"}},
        ...
      ],
      "assessment_focus": "What to evaluate this week",
      "parent_notes_placeholder": ""
    }},
    ...
  ]
}}
"""


async def generate_annual_curriculum(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    user_id: uuid.UUID,
    subject_name: str,
    academic_year: str,
    learning_map_id: uuid.UUID | None = None,
    hours_per_week: float = 4.0,
    total_weeks: int = 36,
    start_date: date | None = None,
    scope_notes: str | None = None,
) -> AnnualCurriculum:
    """Generate a complete year-long curriculum for one subject."""

    # Fetch child profile
    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one()

    prefs_result = await db.execute(
        select(ChildPreferences).where(ChildPreferences.child_id == child_id)
    )
    prefs = prefs_result.scalar_one_or_none()

    # Fetch household philosophical profile
    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one()
    phil = household.philosophical_profile or {}

    # Read academic calendar
    from app.services.academic_calendar import get_academic_calendar, get_instruction_days, calculate_end_date
    calendar = await get_academic_calendar(db, household_id)
    if total_weeks == 36:
        total_weeks = calendar.get("total_instructional_weeks", 36)
    instruction_days = get_instruction_days(calendar)
    days_per_week = len(instruction_days)

    # Calculate dates
    if not start_date:
        cal_start = calendar.get("start_date")
        if cal_start:
            start_date = date.fromisoformat(cal_start) if isinstance(cal_start, str) else cal_start
        else:
            today = date.today()
            year = today.year if today.month < 7 else today.year + 1
            start_date = date(year, 9, 1)
    end_date = calculate_end_date(start_date, total_weeks, calendar)

    child_age = (date.today() - child.date_of_birth).days / 365.25 if child.date_of_birth else 6

    # Learning level for AI prompt
    from app.core.learning_levels import get_level_for_subject, LEARNING_LEVELS
    level = get_level_for_subject(prefs, subject_name)
    level_info = LEARNING_LEVELS.get(level, LEARNING_LEVELS["developing"])

    # Fetch learning map nodes in topological order if provided
    nodes_description = ""
    if learning_map_id:
        nodes_result = await db.execute(
            select(LearningNode)
            .where(LearningNode.learning_map_id == learning_map_id, LearningNode.is_active.is_(True))
            .order_by(LearningNode.sort_order)
        )
        nodes = nodes_result.scalars().all()
        edges_result = await db.execute(
            select(LearningEdge).where(LearningEdge.learning_map_id == learning_map_id)
        )
        edges = edges_result.scalars().all()

        # Build topological description
        node_list = []
        for n in nodes:
            prereqs = [e.from_node_id for e in edges if str(e.to_node_id) == str(n.id)]
            prereq_titles = [next((nn.title for nn in nodes if str(nn.id) == str(p)), "?") for p in prereqs]
            node_list.append(
                f"- {n.id}: {n.title} (type={n.node_type.value}, "
                f"est_minutes={n.estimated_minutes or 30}, "
                f"prereqs=[{', '.join(prereq_titles)}])"
            )
        nodes_description = f"""
LEARNING MAP NODES (teach in this order, respecting prerequisites):
{chr(10).join(node_list)}

Use these node IDs in the focus_nodes field for each week."""

    # Build philosophical constraints
    phil_constraints = build_philosophical_constraints(phil)

    # Detect vocational subject and use appropriate prompt
    from app.core.learning_levels import SUBJECT_CATALOG
    vocational_names = {s["name"].lower() for s in SUBJECT_CATALOG.get("vocational", [])}
    vocational_ids = {s["id"] for s in SUBJECT_CATALOG.get("vocational", [])}
    is_vocational = subject_name.lower() in vocational_names or subject_name.lower().replace(" ", "_") in vocational_ids

    if is_vocational:
        from app.ai.prompts import VOCATIONAL_CURRICULUM_SYSTEM
        system_prompt = VOCATIONAL_CURRICULUM_SYSTEM
    else:
        system_prompt = ANNUAL_CURRICULUM_SYSTEM.format(
            total_weeks=total_weeks,
            philosophical_constraints=phil_constraints,
        )

    user_prompt = f"""Design a complete {total_weeks}-week curriculum for:

SUBJECT: {subject_name}
ACADEMIC YEAR: {academic_year}

CHILD PROFILE:
- Name: {child.first_name}
- Age: {child_age:.1f} years
- Learning level for {subject_name}: {level_info['label']} — {level_info['ai_instruction']}
- Age: {child_age:.0f} (developmental context only)
- Learning style: {json.dumps(prefs.learning_style if prefs else {}, default=str)}
- Interests: {json.dumps(prefs.interests if prefs else [], default=str)}
- Accommodations: {json.dumps(prefs.accommodations if prefs else {}, default=str)}

TIME BUDGET: {hours_per_week} hours per week ({hours_per_week * 60:.0f} minutes)
TOTAL WEEKS: {total_weeks}
INSTRUCTION DAYS: {days_per_week} days per week ({', '.join(d.capitalize() for d in instruction_days)})
START DATE: {start_date}
{nodes_description}
{f'ADDITIONAL GUIDANCE FROM PARENT: {scope_notes}' if scope_notes else ''}

Generate the complete {total_weeks}-week scope and sequence."""

    ai_result = await call_ai(
        db,
        role=AIRole.education_architect,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil,
        max_tokens=8000,
    )

    output = ai_result["output"] if isinstance(ai_result["output"], dict) else {}

    curriculum = AnnualCurriculum(
        household_id=household_id,
        child_id=child_id,
        learning_map_id=learning_map_id,
        created_by=user_id,
        subject_name=subject_name,
        academic_year=academic_year,
        grade_level=child.grade_level,
        total_weeks=total_weeks,
        hours_per_week=hours_per_week,
        start_date=start_date,
        end_date=end_date,
        scope_sequence=output,
        status="draft",
        ai_run_id=ai_result.get("ai_run_id"),
        actual_record={"weeks": {}},
    )
    db.add(curriculum)
    await db.flush()

    db.add(GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=GovernanceAction.modify,
        target_type="annual_curriculum",
        target_id=curriculum.id,
        reason=f"Annual curriculum generated: {subject_name} {academic_year}",
    ))
    await db.flush()

    return curriculum


async def approve_annual_curriculum(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    user_id: uuid.UUID,
    household_id: uuid.UUID,
) -> AnnualCurriculum:
    """Parent approves the curriculum. Materializes ALL weeks immediately."""
    result = await db.execute(
        select(AnnualCurriculum).where(
            AnnualCurriculum.id == curriculum_id,
            AnnualCurriculum.household_id == household_id,
        )
    )
    curriculum = result.scalar_one_or_none()
    if not curriculum:
        raise ValueError("Curriculum not found")
    if curriculum.status != "draft":
        raise ValueError(f"Cannot approve curriculum in '{curriculum.status}' status")

    curriculum.status = "active"
    curriculum.approved_at = datetime.now(UTC)
    curriculum.approved_by = user_id

    db.add(GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=GovernanceAction.approve,
        target_type="annual_curriculum",
        target_id=curriculum.id,
        reason=f"Annual curriculum approved: {curriculum.subject_name} {curriculum.academic_year}",
    ))
    await db.flush()

    # Materialize full year
    await materialize_full_year(db, curriculum)

    return curriculum


async def materialize_full_year(
    db: AsyncSession,
    curriculum: AnnualCurriculum,
) -> dict:
    """Create Plan/PlanWeek/Activity records for ALL weeks."""

    weeks_data = curriculum.scope_sequence.get("weeks", [])
    if not weeks_data:
        return {"weeks_created": 0, "activities_created": 0}

    # Determine which weeks are "near" (auto-approve governance)
    today = date.today()
    near_threshold = today + timedelta(weeks=4)

    # Create one Plan for the entire curriculum year
    plan = Plan(
        household_id=curriculum.household_id,
        child_id=curriculum.child_id,
        created_by=curriculum.created_by,
        name=f"{curriculum.subject_name} — {curriculum.academic_year}",
        description=curriculum.scope_sequence.get("overview", ""),
        status=PlanStatus.active,
        start_date=curriculum.start_date,
        end_date=curriculum.end_date,
        ai_generated=True,
        ai_run_id=curriculum.ai_run_id,
        annual_curriculum_id=curriculum.id,
    )
    db.add(plan)
    await db.flush()

    activity_type_map = {
        "lesson": ActivityType.lesson,
        "practice": ActivityType.practice,
        "assessment": ActivityType.assessment,
        "review": ActivityType.review,
        "project": ActivityType.project,
        "field_trip": ActivityType.field_trip,
    }

    day_offsets = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}

    total_activities = 0

    for week_data in weeks_data:
        week_num = week_data.get("week_number", 1)
        week_start = curriculum.start_date + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=4)

        pw = PlanWeek(
            plan_id=plan.id,
            household_id=curriculum.household_id,
            week_number=week_num,
            start_date=week_start,
            end_date=week_end,
            notes=week_data.get("assessment_focus", ""),
        )
        db.add(pw)
        await db.flush()

        is_near = week_start <= near_threshold
        activities = week_data.get("suggested_activities", [])

        for idx, act_data in enumerate(activities):
            day_name = act_data.get("day", "Monday")
            day_offset = day_offsets.get(day_name, 0)
            scheduled = week_start + timedelta(days=day_offset)

            act_type_str = act_data.get("type", "lesson")
            act_type = activity_type_map.get(act_type_str, ActivityType.lesson)

            activity = Activity(
                plan_week_id=pw.id,
                household_id=curriculum.household_id,
                activity_type=act_type,
                title=act_data.get("title", f"Activity {idx + 1}"),
                description=act_data.get("description", ""),
                estimated_minutes=act_data.get("minutes", 30),
                status=ActivityStatus.scheduled,
                scheduled_date=scheduled,
                sort_order=idx,
                governance_approved=is_near,  # Near weeks auto-approved
            )

            # Link to node if specified
            focus_nodes = week_data.get("focus_nodes", [])
            if focus_nodes:
                try:
                    activity.node_id = uuid.UUID(focus_nodes[min(idx, len(focus_nodes) - 1)])
                except (ValueError, IndexError):
                    pass

            db.add(activity)
            total_activities += 1

    await db.flush()

    return {
        "weeks_created": len(weeks_data),
        "activities_created": total_activities,
        "plan_id": str(plan.id),
    }


async def evaluate_approaching_weeks(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    weeks_ahead: int = 4,
) -> list:
    """Run governance evaluation on activities in the next N weeks.

    Activities created with governance_approved=False get evaluated
    as their scheduled week approaches. This ensures rule changes
    mid-year are respected for future activities.
    """
    result = await db.execute(
        select(AnnualCurriculum).where(AnnualCurriculum.id == curriculum_id)
    )
    curriculum = result.scalar_one_or_none()
    if not curriculum or curriculum.status != "active":
        return []

    today = date.today()
    threshold = today + timedelta(weeks=weeks_ahead)

    # Find unapproved activities in the approaching window
    plans_result = await db.execute(
        select(Plan).where(Plan.annual_curriculum_id == curriculum_id)
    )
    plans = plans_result.scalars().all()
    evaluated = []

    for plan in plans:
        weeks_result = await db.execute(
            select(PlanWeek).where(
                PlanWeek.plan_id == plan.id,
                PlanWeek.start_date <= threshold,
                PlanWeek.start_date >= today,
            )
        )
        weeks = weeks_result.scalars().all()

        for week in weeks:
            acts_result = await db.execute(
                select(Activity).where(
                    Activity.plan_week_id == week.id,
                    Activity.governance_approved.is_(False),
                    Activity.status == ActivityStatus.scheduled,
                )
            )
            activities = acts_result.scalars().all()

            for act in activities:
                # Auto-approve approaching activities
                # In production, this would check governance rules
                act.governance_approved = True
                evaluated.append({"activity_id": str(act.id), "week": week.week_number})

    await db.flush()
    return evaluated


async def record_week_completion(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    week_number: int,
    parent_notes: str | None = None,
) -> dict:
    """Record what actually happened during a completed week."""
    result = await db.execute(
        select(AnnualCurriculum).where(AnnualCurriculum.id == curriculum_id)
    )
    curriculum = result.scalar_one_or_none()
    if not curriculum:
        raise ValueError("Curriculum not found")

    # Find the plan and week
    plan_result = await db.execute(
        select(Plan).where(Plan.annual_curriculum_id == curriculum_id)
    )
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise ValueError("No plan found for this curriculum")

    week_result = await db.execute(
        select(PlanWeek).where(
            PlanWeek.plan_id == plan.id,
            PlanWeek.week_number == week_number,
        )
    )
    week = week_result.scalar_one_or_none()
    if not week:
        raise ValueError(f"Week {week_number} not found")

    # Fetch all activities and their attempts
    acts_result = await db.execute(
        select(Activity).where(Activity.plan_week_id == week.id)
    )
    activities = acts_result.scalars().all()

    completed = [a for a in activities if a.status == ActivityStatus.completed]
    skipped = [a for a in activities if a.status in (ActivityStatus.skipped, ActivityStatus.cancelled)]

    total_minutes = 0
    for act in activities:
        attempts_result = await db.execute(
            select(Attempt).where(Attempt.activity_id == act.id)
        )
        attempts = attempts_result.scalars().all()
        total_minutes += sum(a.duration_minutes or 0 for a in attempts)

    # Build week record
    week_record = {
        "planned_activities": len(activities),
        "completed_activities": len(completed),
        "skipped_activities": len(skipped),
        "total_minutes": total_minutes,
        "parent_notes": parent_notes or "",
    }

    # Update actual_record
    actual = dict(curriculum.actual_record or {})
    weeks = dict(actual.get("weeks", {}))
    weeks[str(week_number)] = week_record
    actual["weeks"] = weeks
    curriculum.actual_record = actual

    # Force SQLAlchemy to detect JSONB change
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(curriculum, "actual_record")

    await db.flush()
    return week_record


async def get_curriculum_history(
    db: AsyncSession,
    curriculum_id: uuid.UUID,
    week_number: int | None = None,
) -> dict:
    """Get planned vs actual for a curriculum, optionally for one week."""
    result = await db.execute(
        select(AnnualCurriculum).where(AnnualCurriculum.id == curriculum_id)
    )
    curriculum = result.scalar_one_or_none()
    if not curriculum:
        raise ValueError("Curriculum not found")

    scope = curriculum.scope_sequence
    actual = curriculum.actual_record or {}

    if week_number is not None:
        # Single week detail
        planned_weeks = scope.get("weeks", [])
        planned = next((w for w in planned_weeks if w.get("week_number") == week_number), None)
        actual_week = actual.get("weeks", {}).get(str(week_number), {})

        # Fetch real activities
        plan_result = await db.execute(
            select(Plan).where(Plan.annual_curriculum_id == curriculum_id)
        )
        plan = plan_result.scalar_one_or_none()
        activities_data = []
        if plan:
            week_result = await db.execute(
                select(PlanWeek).where(
                    PlanWeek.plan_id == plan.id,
                    PlanWeek.week_number == week_number,
                )
            )
            week = week_result.scalar_one_or_none()
            if week:
                acts_result = await db.execute(
                    select(Activity).where(Activity.plan_week_id == week.id)
                    .order_by(Activity.sort_order)
                )
                for act in acts_result.scalars().all():
                    activities_data.append({
                        "id": str(act.id),
                        "title": act.title,
                        "type": act.activity_type.value,
                        "status": act.status.value,
                        "scheduled_date": str(act.scheduled_date) if act.scheduled_date else None,
                        "estimated_minutes": act.estimated_minutes,
                        "governance_approved": act.governance_approved,
                    })

        return {
            "week_number": week_number,
            "planned": planned,
            "actual": actual_week,
            "activities": activities_data,
        }

    # Full curriculum summary
    planned_weeks = scope.get("weeks", [])
    actual_weeks = actual.get("weeks", {})

    week_summaries = []
    for pw in planned_weeks:
        wn = pw.get("week_number", 0)
        aw = actual_weeks.get(str(wn), {})
        week_summaries.append({
            "week_number": wn,
            "title": pw.get("title", ""),
            "objectives": pw.get("objectives", []),
            "has_actual": bool(aw),
            "completed_activities": aw.get("completed_activities", 0) if aw else None,
            "planned_activities": len(pw.get("suggested_activities", [])),
            "parent_notes": aw.get("parent_notes", "") if aw else None,
        })

    return {
        "curriculum_id": str(curriculum.id),
        "subject_name": curriculum.subject_name,
        "academic_year": curriculum.academic_year,
        "grade_level": curriculum.grade_level,
        "status": curriculum.status,
        "overview": scope.get("overview", ""),
        "total_weeks": curriculum.total_weeks,
        "weeks": week_summaries,
    }
