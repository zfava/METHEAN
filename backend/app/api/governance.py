"""Parent Governance + AI Integration API.

Plan generation, governance rules CRUD, plan approve/reject/lock,
tutor interaction, cartographer calibration, advisor reports,
AI inspection endpoints.
"""

import json
import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import (
    ADVISOR_SYSTEM,
    CARTOGRAPHER_SYSTEM,
    TUTOR_SYSTEM,
)
from app.api.deps import get_current_user, get_db, require_role
from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode
from app.models.enums import (
    ActivityStatus,
    GovernanceAction,
    MasteryLevel,
    PlanStatus,
)
from app.models.evidence import AdvisorReport
from app.models.governance import Activity, GovernanceEvent, GovernanceRule, Plan, PlanWeek
from app.models.identity import Child, User
from app.models.operational import AIRun
from app.models.state import ChildNodeState
from app.schemas.governance import (
    ActivityApproveReject,
    ActivityInPlan,
    AdvisorReportResponse,
    AIRunResponse,
    CartographerCalibrateRequest,
    CartographerRecommendation,
    GovernanceEventResponse,
    GovernanceRuleCreate,
    GovernanceRuleResponse,
    GovernanceRuleUpdate,
    PlanDetailResponse,
    PlanGenerateRequest,
    PlanResponse,
    TutorMessageRequest,
    TutorMessageResponse,
)
from app.services.governance import (
    create_default_rules,
    log_governance_event,
)
from app.services.planner import generate_plan

router = APIRouter(tags=["governance"])


# ── Helpers ──

async def _get_child_or_404(
    db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID,
) -> Child:
    result = await db.execute(
        select(Child).where(Child.id == child_id, Child.household_id == household_id)
    )
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


async def _get_plan_or_404(
    db: AsyncSession, plan_id: uuid.UUID, household_id: uuid.UUID,
) -> Plan:
    result = await db.execute(
        select(Plan).where(Plan.id == plan_id, Plan.household_id == household_id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


# ══════════════════════════════════════════════════
# Governance Rules CRUD
# ══════════════════════════════════════════════════

@router.get("/governance-rules", response_model=list[GovernanceRuleResponse])
async def list_governance_rules(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[GovernanceRuleResponse]:
    result = await db.execute(
        select(GovernanceRule)
        .where(GovernanceRule.household_id == user.household_id)
        .order_by(GovernanceRule.priority.asc())
    )
    return [GovernanceRuleResponse.model_validate(r) for r in result.scalars().all()]


@router.post("/governance-rules", response_model=GovernanceRuleResponse, status_code=201)
async def create_governance_rule(
    body: GovernanceRuleCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> GovernanceRuleResponse:
    rule = GovernanceRule(
        household_id=user.household_id,
        created_by=user.id,
        rule_type=body.rule_type,
        scope=body.scope,
        scope_id=body.scope_id,
        name=body.name,
        description=body.description,
        parameters=body.parameters,
        priority=body.priority,
    )
    db.add(rule)
    await db.flush()

    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.modify, "governance_rule", rule.id,
        reason="Rule created",
    )

    return GovernanceRuleResponse.model_validate(rule)


@router.put("/governance-rules/{rule_id}", response_model=GovernanceRuleResponse)
async def update_governance_rule(
    rule_id: uuid.UUID,
    body: GovernanceRuleUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> GovernanceRuleResponse:
    result = await db.execute(
        select(GovernanceRule).where(
            GovernanceRule.id == rule_id,
            GovernanceRule.household_id == user.household_id,
        )
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    if body.name is not None:
        rule.name = body.name
    if body.description is not None:
        rule.description = body.description
    if body.parameters is not None:
        rule.parameters = body.parameters
    if body.priority is not None:
        rule.priority = body.priority
    if body.is_active is not None:
        rule.is_active = body.is_active

    await db.flush()
    await db.refresh(rule)

    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.modify, "governance_rule", rule.id,
        reason="Rule updated",
    )

    return GovernanceRuleResponse.model_validate(rule)


@router.post("/governance-rules/defaults", response_model=list[GovernanceRuleResponse], status_code=201)
async def initialize_default_rules(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> list[GovernanceRuleResponse]:
    rules = await create_default_rules(db, user.household_id, user.id)
    return [GovernanceRuleResponse.model_validate(r) for r in rules]


# ══════════════════════════════════════════════════
# Plan Generation + Management
# ══════════════════════════════════════════════════

@router.post("/children/{child_id}/plans/generate", response_model=PlanResponse, status_code=201)
async def generate_plan_endpoint(
    child_id: uuid.UUID,
    body: PlanGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> PlanResponse:
    child = await _get_child_or_404(db, child_id, user.household_id)

    result = await generate_plan(
        db, child_id, user.household_id, user.id,
        week_start=body.week_start,
        daily_minutes=body.daily_minutes,
    )

    plan_result = await db.execute(select(Plan).where(Plan.id == result["plan_id"]))
    plan = plan_result.scalar_one()
    return PlanResponse.model_validate(plan)


@router.get("/children/{child_id}/plans", response_model=list[PlanResponse])
async def list_plans(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[PlanResponse]:
    child = await _get_child_or_404(db, child_id, user.household_id)
    result = await db.execute(
        select(Plan)
        .where(Plan.child_id == child_id, Plan.household_id == user.household_id)
        .order_by(Plan.created_at.desc())
    )
    return [PlanResponse.model_validate(p) for p in result.scalars().all()]


@router.get("/plans/{plan_id}", response_model=PlanDetailResponse)
async def get_plan_detail(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PlanDetailResponse:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)

    # Get activities through weeks
    weeks_result = await db.execute(
        select(PlanWeek).where(PlanWeek.plan_id == plan_id)
    )
    weeks = weeks_result.scalars().all()
    week_ids = [w.id for w in weeks]

    activities = []
    if week_ids:
        act_result = await db.execute(
            select(Activity)
            .where(Activity.plan_week_id.in_(week_ids))
            .order_by(Activity.sort_order)
        )
        activities = [ActivityInPlan.model_validate(a) for a in act_result.scalars().all()]

    return PlanDetailResponse(
        id=plan.id,
        household_id=plan.household_id,
        child_id=plan.child_id,
        name=plan.name,
        description=plan.description,
        status=plan.status,
        start_date=plan.start_date,
        end_date=plan.end_date,
        ai_generated=plan.ai_generated,
        ai_run_id=plan.ai_run_id,
        created_at=plan.created_at,
        activities=activities,
    )


@router.put("/plans/{plan_id}/activities/{activity_id}/approve")
async def approve_activity(
    plan_id: uuid.UUID,
    activity_id: uuid.UUID,
    body: ActivityApproveReject | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> dict:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)
    if plan.status == PlanStatus.archived:
        raise HTTPException(status_code=409, detail="Plan is archived")

    result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id,
            Activity.household_id == user.household_id,
        )
    )
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.status = ActivityStatus.scheduled

    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.approve, "activity", activity_id,
        reason=body.reason if body else "Parent approved",
    )

    return {"activity_id": str(activity_id), "status": "approved"}


@router.put("/plans/{plan_id}/activities/{activity_id}/reject")
async def reject_activity(
    plan_id: uuid.UUID,
    activity_id: uuid.UUID,
    body: ActivityApproveReject,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> dict:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)
    if plan.status == PlanStatus.archived:
        raise HTTPException(status_code=409, detail="Plan is archived")

    result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id,
            Activity.household_id == user.household_id,
        )
    )
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.status = ActivityStatus.cancelled

    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.reject, "activity", activity_id,
        reason=body.reason or "Parent rejected",
    )

    return {"activity_id": str(activity_id), "status": "rejected"}


@router.put("/plans/{plan_id}/lock")
async def lock_plan(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> dict:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)
    plan.status = PlanStatus.active
    await db.flush()

    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.approve, "plan", plan_id,
        reason="Plan locked/activated",
    )

    return {"plan_id": str(plan_id), "status": "active"}


@router.put("/plans/{plan_id}/unlock")
async def unlock_plan(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> dict:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)
    if plan.status == PlanStatus.archived:
        raise HTTPException(status_code=409, detail="Cannot unlock archived plan")
    plan.status = PlanStatus.draft
    await db.flush()
    return {"plan_id": str(plan_id), "status": "draft"}


# ══════════════════════════════════════════════════
# Tutor
# ══════════════════════════════════════════════════

@router.post("/tutor/{activity_id}/message", response_model=TutorMessageResponse)
async def tutor_message(
    activity_id: uuid.UUID,
    body: TutorMessageRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TutorMessageResponse:
    """Send a message to the tutor and get a response."""
    # Verify activity
    act_result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id,
            Activity.household_id == user.household_id,
        )
    )
    activity = act_result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Build context
    node_title = "General"
    if activity.node_id:
        node_result = await db.execute(
            select(LearningNode).where(LearningNode.id == activity.node_id)
        )
        node = node_result.scalar_one_or_none()
        if node:
            node_title = node.title

    user_prompt = f"""Activity: {activity.title}
Learning Topic: {node_title}

Child says: {body.message}

Respond using the Socratic method. Guide the child toward understanding without giving the answer."""

    result = await call_ai(
        db,
        role=AIRole.tutor,
        system_prompt=TUTOR_SYSTEM,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
    )

    output = result["output"]
    return TutorMessageResponse(
        message=output.get("message", "Could you tell me more about your thinking?"),
        hints=output.get("hints", []),
        encouragement=output.get("encouragement", True),
        ai_run_id=result["ai_run_id"],
    )


# ══════════════════════════════════════════════════
# Cartographer
# ══════════════════════════════════════════════════

@router.post(
    "/children/{child_id}/cartographer/calibrate",
    response_model=CartographerRecommendation,
)
async def cartographer_calibrate(
    child_id: uuid.UUID,
    body: CartographerCalibrateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> CartographerRecommendation:
    child = await _get_child_or_404(db, child_id, user.household_id)

    # Get map info
    map_result = await db.execute(
        select(LearningMap).where(
            LearningMap.id == body.learning_map_id,
            LearningMap.household_id == user.household_id,
        )
    )
    lmap = map_result.scalar_one_or_none()
    if not lmap:
        raise HTTPException(status_code=404, detail="Learning map not found")

    # Get nodes
    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id == lmap.id,
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    nodes = nodes_result.scalars().all()

    user_prompt = f"""Calibrate this learning map for a child.

Map: {lmap.name}
Child: {child.first_name}
Parent Goals: {body.parent_goals}
Notes: {body.notes}

Current nodes:
{json.dumps([{"id": str(n.id), "title": n.title, "type": n.node_type.value if hasattr(n.node_type, 'value') else str(n.node_type)} for n in nodes], indent=2)}

Provide calibration recommendations."""

    result = await call_ai(
        db,
        role=AIRole.cartographer,
        system_prompt=CARTOGRAPHER_SYSTEM,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
    )

    output = result["output"]
    return CartographerRecommendation(
        ai_run_id=result["ai_run_id"],
        difficulty_adjustments=output.get("difficulty_adjustments", []),
        suggested_additions=output.get("suggested_additions", []),
        suggested_removals=output.get("suggested_removals", []),
        estimated_weeks=output.get("estimated_weeks", 12),
        rationale=output.get("rationale", ""),
    )


# ══════════════════════════════════════════════════
# Advisor Reports
# ══════════════════════════════════════════════════

@router.post("/children/{child_id}/advisor-reports/generate", response_model=AdvisorReportResponse, status_code=201)
async def generate_advisor_report(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
) -> AdvisorReportResponse:
    child = await _get_child_or_404(db, child_id, user.household_id)

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Get child's state summary
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == user.household_id,
        )
    )
    states = states_result.scalars().all()
    mastered = sum(1 for s in states if s.mastery_level == MasteryLevel.mastered)
    in_progress = sum(1 for s in states if s.mastery_level not in (MasteryLevel.mastered, MasteryLevel.not_started))

    user_prompt = f"""Generate a weekly progress report.

Child: {child.first_name}
Period: {week_start.isoformat()} to {week_end.isoformat()}

State Summary:
- Total nodes with state: {len(states)}
- Mastered: {mastered}
- In progress: {in_progress}
- Total attempts: {sum(s.attempts_count for s in states)}
- Total time: {sum(s.time_spent_minutes for s in states)} minutes

Provide an encouraging, honest assessment."""

    result = await call_ai(
        db,
        role=AIRole.advisor,
        system_prompt=ADVISOR_SYSTEM,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
    )

    output = result["output"]
    report = AdvisorReport(
        household_id=user.household_id,
        child_id=child_id,
        ai_run_id=result["ai_run_id"],
        report_type="weekly",
        period_start=week_start,
        period_end=week_end,
        content=output if isinstance(output, dict) else {"raw": output},
        recommendations=output.get("recommended_focus", []) if isinstance(output, dict) else [],
    )
    db.add(report)
    await db.flush()

    return AdvisorReportResponse.model_validate(report)


@router.get("/children/{child_id}/advisor-reports", response_model=list[AdvisorReportResponse])
async def list_advisor_reports(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[AdvisorReportResponse]:
    child = await _get_child_or_404(db, child_id, user.household_id)
    result = await db.execute(
        select(AdvisorReport)
        .where(AdvisorReport.child_id == child_id, AdvisorReport.household_id == user.household_id)
        .order_by(AdvisorReport.created_at.desc())
    )
    return [AdvisorReportResponse.model_validate(r) for r in result.scalars().all()]


@router.get("/advisor-reports/{report_id}", response_model=AdvisorReportResponse)
async def get_advisor_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AdvisorReportResponse:
    result = await db.execute(
        select(AdvisorReport).where(
            AdvisorReport.id == report_id,
            AdvisorReport.household_id == user.household_id,
        )
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return AdvisorReportResponse.model_validate(report)


# ══════════════════════════════════════════════════
# AI Inspection Endpoints
# ══════════════════════════════════════════════════

@router.get("/ai-runs", response_model=list[AIRunResponse])
async def list_ai_runs(
    child_id: uuid.UUID | None = Query(default=None),
    role: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[AIRunResponse]:
    query = select(AIRun).where(AIRun.household_id == user.household_id)
    if role:
        query = query.where(AIRun.run_type == role)
    query = query.order_by(AIRun.created_at.desc()).limit(50)

    result = await db.execute(query)
    return [AIRunResponse.model_validate(r) for r in result.scalars().all()]


@router.get("/ai-runs/{run_id}", response_model=AIRunResponse)
async def get_ai_run(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AIRunResponse:
    result = await db.execute(
        select(AIRun).where(
            AIRun.id == run_id,
            AIRun.household_id == user.household_id,
        )
    )
    ai_run = result.scalar_one_or_none()
    if not ai_run:
        raise HTTPException(status_code=404, detail="AI run not found")
    return AIRunResponse.model_validate(ai_run)


@router.get("/plans/{plan_id}/decision-trace")
async def get_decision_trace(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get the AI rationale and governance decisions for each activity in a plan."""
    plan = await _get_plan_or_404(db, plan_id, user.household_id)

    # Get AI run
    ai_run_data = None
    if plan.ai_run_id:
        run_result = await db.execute(
            select(AIRun).where(AIRun.id == plan.ai_run_id)
        )
        ai_run = run_result.scalar_one_or_none()
        if ai_run:
            ai_run_data = {
                "model_used": ai_run.model_used,
                "input_data": ai_run.input_data,
                "output_data": ai_run.output_data,
            }

    # Get governance events for activities in this plan
    weeks_result = await db.execute(select(PlanWeek).where(PlanWeek.plan_id == plan_id))
    week_ids = [w.id for w in weeks_result.scalars().all()]

    activity_decisions = []
    if week_ids:
        acts_result = await db.execute(
            select(Activity).where(Activity.plan_week_id.in_(week_ids))
        )
        activities = acts_result.scalars().all()

        for act in activities:
            events_result = await db.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.target_type == "activity",
                    GovernanceEvent.target_id == act.id,
                ).order_by(GovernanceEvent.created_at.asc())
            )
            events = events_result.scalars().all()

            activity_decisions.append({
                "activity_id": str(act.id),
                "title": act.title,
                "status": act.status.value if hasattr(act.status, 'value') else str(act.status),
                "instructions": act.instructions,
                "governance_events": [
                    {
                        "action": e.action.value if hasattr(e.action, 'value') else str(e.action),
                        "reason": e.reason,
                        "metadata": e.metadata_,
                        "created_at": e.created_at.isoformat() if e.created_at else None,
                    }
                    for e in events
                ],
            })

    return {
        "plan_id": str(plan_id),
        "ai_run": ai_run_data,
        "activity_decisions": activity_decisions,
    }


@router.get("/governance-events", response_model=list[GovernanceEventResponse])
async def list_governance_events(
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[GovernanceEventResponse]:
    result = await db.execute(
        select(GovernanceEvent)
        .where(GovernanceEvent.household_id == user.household_id)
        .order_by(GovernanceEvent.created_at.desc())
        .limit(limit)
    )
    return [GovernanceEventResponse.model_validate(e) for e in result.scalars().all()]
