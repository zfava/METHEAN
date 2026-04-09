"""Plan Generation Service.

Wires Planner AI through governance gateway to create weekly learning plans.
"""

import json
import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import PLANNER_SYSTEM
from app.models.curriculum import ChildMapEnrollment, LearningNode
from app.models.identity import Child
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    GovernanceAction,
    MasteryLevel,
    PlanStatus,
)
from app.models.governance import Activity, Plan, PlanWeek
from app.models.state import ChildNodeState, FSRSCard
from app.services.governance import evaluate_activity, log_governance_event


async def generate_plan(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    user_id: uuid.UUID,
    week_start: date,
    daily_minutes: int = 120,
) -> dict:
    """Generate a weekly plan via AI Planner + governance evaluation.

    Returns dict with plan_id, activities, governance_decisions.
    """
    # Read academic calendar
    from app.services.academic_calendar import (
        get_academic_calendar, get_instruction_days, is_break_date,
        get_week_end_for_start,
    )
    from app.core.learning_levels import get_daily_minutes_for_child
    from sqlalchemy.orm import selectinload
    calendar = await get_academic_calendar(db, household_id)
    instruction_days = get_instruction_days(calendar)
    num_days = len(instruction_days)
    week_end = get_week_end_for_start(week_start, calendar)

    # Check if this week is a break
    if is_break_date(calendar, week_start):
        return {"plan_id": None, "message": "This week is a scheduled break.", "activities": []}

    # Use calendar-aware daily minutes if default
    if daily_minutes == 120:
        child_r = await db.execute(
            select(Child).options(selectinload(Child.preferences)).where(Child.id == child_id)
        )
        child_obj = child_r.scalar_one_or_none()
        if child_obj:
            daily_minutes = get_daily_minutes_for_child(child_obj, calendar)

    # Gather child context for AI
    context = await _build_planner_context(
        db, child_id, household_id, daily_minutes,
    )

    # Inject governance intelligence
    try:
        from app.services.governance_intelligence import get_planning_adjustments
        gov_adjustments = await get_planning_adjustments(db, household_id)
        if gov_adjustments:
            context["governance_intelligence"] = gov_adjustments
    except Exception:
        pass

    day_labels = ", ".join([d.capitalize() for d in instruction_days])

    user_prompt = f"""Generate a weekly learning plan for this child.

Week: {week_start.isoformat()} to {week_end.isoformat()}
Daily time budget: {daily_minutes} minutes
Instruction days: {day_labels} ({num_days} days)

Child's current state:
{json.dumps(context, indent=2, default=str)}

Create activities spread across {num_days} days ({day_labels}).
Prioritize nodes that are due for review, then available nodes."""

    # Fetch household philosophical profile for AI constraints
    from app.models.identity import Household
    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household_obj = h_result.scalar_one_or_none()
    phil_profile = household_obj.philosophical_profile if household_obj else None

    # Call AI through governance gateway
    ai_result = await call_ai(
        db,
        role=AIRole.planner,
        system_prompt=PLANNER_SYSTEM,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil_profile,
    )

    ai_output = ai_result["output"]
    ai_activities = ai_output.get("activities", []) if isinstance(ai_output, dict) else []

    # Create Plan
    plan = Plan(
        household_id=household_id,
        child_id=child_id,
        created_by=user_id,
        name=f"Week of {week_start.isoformat()}",
        description=ai_output.get("rationale", "") if isinstance(ai_output, dict) else "",
        status=PlanStatus.draft,
        start_date=week_start,
        end_date=week_end,
        ai_generated=True,
        ai_run_id=ai_result["ai_run_id"],
    )
    db.add(plan)
    await db.flush()

    # Create PlanWeek
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household_id,
        week_number=1,
        start_date=week_start,
        end_date=week_end,
    )
    db.add(week)
    await db.flush()

    # Create activities and evaluate each through governance
    governance_decisions = []
    for i, act_data in enumerate(ai_activities):
        # Map activity type
        act_type = _map_activity_type(act_data.get("activity_type", "lesson"))
        difficulty = act_data.get("difficulty", 3)

        # Calculate scheduled date from day number
        scheduled_day = act_data.get("scheduled_day", (i % 5) + 1)
        scheduled_date = week_start + timedelta(days=scheduled_day - 1)

        # Resolve node_id
        node_id = None
        node_id_str = act_data.get("node_id")
        if node_id_str and node_id_str != "null":
            try:
                node_id = uuid.UUID(node_id_str)
            except (ValueError, AttributeError):
                pass

        # Evaluate through governance rules
        decision = await evaluate_activity(
            db, household_id, difficulty=difficulty, activity_type=act_type.value,
            node_id=node_id,
        )

        # Blocked activities are not created at all
        if decision.action == "block":
            await log_governance_event(
                db, household_id, user_id=user_id,
                action=GovernanceAction.reject,
                target_type="activity_proposal",
                target_id=uuid.uuid4(),  # no activity created
                reason=decision.reason,
                metadata={
                    "rule_id": str(decision.rule_id) if decision.rule_id else None,
                    "title": act_data.get("title", f"Activity {i+1}"),
                    "blocked": True,
                },
            )
            governance_decisions.append({
                "activity_id": None,
                "title": act_data.get("title", f"Activity {i+1}"),
                "action": "block",
                "reason": decision.reason,
            })
            continue

        activity = Activity(
            plan_week_id=week.id,
            household_id=household_id,
            node_id=node_id,
            activity_type=act_type,
            title=act_data.get("title", f"Activity {i+1}"),
            description=act_data.get("rationale", ""),
            instructions={"difficulty": difficulty, "ai_rationale": act_data.get("rationale", "")},
            estimated_minutes=act_data.get("estimated_minutes", 30),
            status=ActivityStatus.scheduled,
            scheduled_date=scheduled_date,
            sort_order=i,
            governance_approved=decision.action == "auto_approve",
        )
        db.add(activity)
        await db.flush()

        gov_action = GovernanceAction.approve if decision.action == "auto_approve" else GovernanceAction.defer

        await log_governance_event(
            db, household_id, user_id=user_id,
            action=gov_action,
            target_type="activity",
            target_id=activity.id,
            reason=decision.reason,
            metadata={
                "rule_id": str(decision.rule_id) if decision.rule_id else None,
                "rule_name": decision.rule_name,
                "difficulty": difficulty,
                "is_auto": True,
            },
        )

        governance_decisions.append({
            "activity_id": activity.id,
            "title": activity.title,
            "action": decision.action,
            "reason": decision.reason,
        })

    await db.flush()

    return {
        "plan_id": plan.id,
        "plan_name": plan.name,
        "ai_run_id": ai_result["ai_run_id"],
        "is_mock": ai_result["is_mock"],
        "activities_count": len(ai_activities),
        "governance_decisions": governance_decisions,
    }


def _map_activity_type(type_str: str) -> ActivityType:
    """Map AI-generated type string to ActivityType enum."""
    mapping = {
        "lesson": ActivityType.lesson,
        "practice": ActivityType.practice,
        "assessment": ActivityType.assessment,
        "review": ActivityType.review,
        "project": ActivityType.project,
        "field_trip": ActivityType.field_trip,
    }
    return mapping.get(type_str.lower(), ActivityType.lesson)


async def _build_planner_context(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    daily_minutes: int,
) -> dict:
    """Build context data for the planner AI."""
    # Get enrolled maps
    enrollments = await db.execute(
        select(ChildMapEnrollment.learning_map_id).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.household_id == household_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    map_ids = list(enrollments.scalars().all())

    # Get nodes with states
    nodes = []
    if map_ids:
        node_result = await db.execute(
            select(LearningNode).where(
                LearningNode.learning_map_id.in_(map_ids),
                LearningNode.is_active == True,  # noqa: E712
            )
        )
        all_nodes = node_result.scalars().all()
        node_ids = [n.id for n in all_nodes]

        # Get states
        state_result = await db.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child_id,
                ChildNodeState.node_id.in_(node_ids),
            )
        ) if node_ids else None
        states = {s.node_id: s for s in (state_result.scalars().all() if state_result else [])}

        # Get FSRS cards for due dates
        card_result = await db.execute(
            select(FSRSCard).where(
                FSRSCard.child_id == child_id,
                FSRSCard.node_id.in_(node_ids),
            )
        ) if node_ids else None
        cards = {c.node_id: c for c in (card_result.scalars().all() if card_result else [])}

        for node in all_nodes:
            state = states.get(node.id)
            card = cards.get(node.id)
            mastery = state.mastery_level.value if state and hasattr(state.mastery_level, 'value') else (
                str(state.mastery_level) if state else "not_started"
            )
            nodes.append({
                "node_id": str(node.id),
                "title": node.title,
                "type": node.node_type.value if hasattr(node.node_type, 'value') else str(node.node_type),
                "mastery": mastery,
                "due": card.due.isoformat() if card and card.due else None,
                "estimated_minutes": node.estimated_minutes,
            })

    # Inject learner intelligence context
    from app.services.intelligence import get_intelligence_context
    try:
        intel = await get_intelligence_context(db, child_id, household_id)
    except Exception:
        intel = {}

    return {
        "daily_minutes": daily_minutes,
        "nodes": nodes,
        "learner_intelligence": intel,
    }
