"""Parent Governance + AI Integration API.

Plan generation, governance rules CRUD, plan approve/reject/lock,
tutor interaction, cartographer calibration, advisor reports,
AI inspection endpoints.
"""

import json
import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import (
    ADVISOR_SYSTEM,
    CARTOGRAPHER_SYSTEM,
    TUTOR_SYSTEM,
)
from app.api.deps import PaginationParams, get_current_user, get_db, require_permission, require_role
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


async def _get_philosophical_profile(
    db: AsyncSession, household_id: uuid.UUID,
) -> dict | None:
    from app.models.identity import Household
    result = await db.execute(
        select(Household).where(Household.id == household_id)
    )
    h = result.scalar_one_or_none()
    return h.philosophical_profile if h else None


# ══════════════════════════════════════════════════
# Governance Rules CRUD
# ══════════════════════════════════════════════════

@router.get("/governance-rules")
async def list_governance_rules(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    base = select(GovernanceRule).where(GovernanceRule.household_id == user.household_id)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(GovernanceRule.priority.asc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [GovernanceRuleResponse.model_validate(r) for r in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.post("/governance-rules", response_model=GovernanceRuleResponse, status_code=201)
async def create_governance_rule(
    body: GovernanceRuleCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("rules.create")),
) -> GovernanceRuleResponse:
    from app.models.enums import RuleTier
    from app.core.permissions import check_permission, PERM_RULES_CONSTITUTIONAL

    # Constitutional rules require explicit confirmation AND the constitutional permission
    if body.tier == RuleTier.constitutional:
        if not await check_permission(db, user, PERM_RULES_CONSTITUTIONAL):
            raise HTTPException(status_code=403, detail="Missing permission: rules.constitutional")
        if not body.confirm_constitutional:
            raise HTTPException(
                status_code=400,
                detail="Constitutional rules are hard to change once created. "
                       "Set confirm_constitutional=true to confirm.",
            )

    rule = GovernanceRule(
        household_id=user.household_id,
        created_by=user.id,
        rule_type=body.rule_type,
        tier=body.tier,
        scope=body.scope,
        scope_id=body.scope_id,
        name=body.name,
        description=body.description,
        parameters=body.parameters,
        priority=body.priority,
        effective_from=body.effective_from,
        effective_until=body.effective_until,
        trigger_conditions=body.trigger_conditions or {},
    )
    db.add(rule)
    await db.flush()

    target_type = "constitutional_rule_change" if body.tier == RuleTier.constitutional else "governance_rule"
    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.modify, target_type, rule.id,
        reason="Constitutional rule created" if body.tier == RuleTier.constitutional else "Rule created",
    )

    return GovernanceRuleResponse.model_validate(rule)


@router.put("/governance-rules/{rule_id}", response_model=GovernanceRuleResponse)
async def update_governance_rule(
    rule_id: uuid.UUID,
    body: GovernanceRuleUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("rules.edit")),
) -> GovernanceRuleResponse:
    from app.models.enums import RuleTier

    result = await db.execute(
        select(GovernanceRule).where(
            GovernanceRule.id == rule_id,
            GovernanceRule.household_id == user.household_id,
        )
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    is_constitutional = (
        (rule.tier == RuleTier.constitutional)
        if hasattr(rule.tier, "value") is False
        else (rule.tier.value == "constitutional" if hasattr(rule.tier, "value") else str(rule.tier) == "constitutional")
    ) or (rule.tier == "constitutional") or (rule.tier == RuleTier.constitutional)

    if is_constitutional:
        if not body.confirm_constitutional:
            raise HTTPException(
                status_code=400,
                detail="This is a constitutional rule. Set confirm_constitutional=true to modify.",
            )
        if not body.reason or len(body.reason.strip()) < 20:
            raise HTTPException(
                status_code=400,
                detail="Constitutional rule changes require a reason of at least 20 characters.",
            )

    # Capture before state for diff
    before = {
        "name": rule.name, "description": rule.description,
        "parameters": rule.parameters, "priority": rule.priority,
        "is_active": rule.is_active,
    }

    if body.name is not None:
        rule.name = body.name
    if body.description is not None:
        rule.description = body.description
    if body.parameters is not None:
        rule.parameters = body.parameters
    if body.priority is not None:
        rule.priority = body.priority
    if body.is_active is not None:
        # Constitutional rules cannot be deleted, only deactivated — and that requires ceremony
        if is_constitutional and body.is_active is False:
            if not body.reason or len(body.reason.strip()) < 20:
                raise HTTPException(
                    status_code=400,
                    detail="Deactivating a constitutional rule requires a reason of at least 20 characters.",
                )
        rule.is_active = body.is_active

    after = {
        "name": rule.name, "description": rule.description,
        "parameters": rule.parameters, "priority": rule.priority,
        "is_active": rule.is_active,
    }

    await db.flush()
    await db.refresh(rule)

    target_type = "constitutional_rule_change" if is_constitutional else "governance_rule"
    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.modify, target_type, rule.id,
        reason=body.reason or "Rule updated",
        metadata={"before": before, "after": after} if is_constitutional else None,
    )

    return GovernanceRuleResponse.model_validate(rule)


@router.delete("/governance-rules/{rule_id}")
async def delete_governance_rule(
    rule_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("rules.edit")),
) -> dict:
    from app.models.enums import RuleTier

    result = await db.execute(
        select(GovernanceRule).where(
            GovernanceRule.id == rule_id,
            GovernanceRule.household_id == user.household_id,
        )
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    is_constitutional = rule.tier == RuleTier.constitutional or rule.tier == "constitutional"
    if is_constitutional:
        raise HTTPException(
            status_code=400,
            detail="Constitutional rules cannot be deleted. Use PUT to deactivate with a reason.",
        )

    await db.delete(rule)
    await db.flush()
    return {"deleted": True}


# ══════════════════════════════════════════════════
# Governance Reports
# ══════════════════════════════════════════════════

class ReportRequest(BaseModel):
    period_start: date
    period_end: date

class AttestRequest(BaseModel):
    report_id: str
    attestation_text: str = Field(min_length=10)


@router.post("/governance/report")
async def generate_report(
    body: ReportRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("export.data")),
) -> dict:
    """Generate a comprehensive governance report for the period."""
    from app.services.governance_report import generate_governance_report

    report = await generate_governance_report(
        db, user.household_id, body.period_start, body.period_end, user.id,
    )

    # Log the export
    await log_governance_event(
        db, user.household_id, user.id,
        GovernanceAction.approve, "governance_report", user.household_id,
        reason=f"Governance report generated for {body.period_start} to {body.period_end}",
    )

    return report


@router.post("/governance/report/attest")
async def attest_report(
    body: AttestRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner")),
) -> dict:
    """Parent's digital signature on a governance report.

    Creates an immutable governance event as attestation. This is the
    authoritative document — not any AI summary.
    """
    event = GovernanceEvent(
        household_id=user.household_id,
        user_id=user.id,
        action=GovernanceAction.approve,
        target_type="governance_report_attestation",
        target_id=user.household_id,
        reason=body.attestation_text,
        metadata_={
            "report_id": body.report_id,
            "attested_by": user.display_name,
            "attested_at": datetime.now(UTC).isoformat(),
        },
    )
    db.add(event)
    await db.flush()

    return {
        "attestation_id": str(event.id),
        "report_id": body.report_id,
        "attested_by": user.display_name,
        "attested_at": event.created_at.isoformat() if event.created_at else None,
    }


@router.get("/governance/rules/upcoming")
async def upcoming_triggers(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict]:
    """Rules with future trigger conditions that haven't fired yet."""
    result = await db.execute(
        select(GovernanceRule).where(
            GovernanceRule.household_id == user.household_id,
            GovernanceRule.trigger_conditions.isnot(None),
        )
    )
    items = []
    for r in result.scalars().all():
        tc = r.trigger_conditions or {}
        if not tc.get("type") or tc.get("triggered_at"):
            continue
        items.append({
            "rule_id": str(r.id),
            "rule_name": r.name,
            "trigger_type": tc.get("type"),
            "trigger_conditions": tc,
            "effective_from": r.effective_from.isoformat() if r.effective_from else None,
            "is_active": r.is_active,
        })
    return items


@router.post("/governance-rules/defaults", response_model=list[GovernanceRuleResponse], status_code=201)
async def initialize_default_rules(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("manage.users")),
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
    user: User = Depends(require_permission("plans.generate")),
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


@router.get("/children/{child_id}/plans")
async def list_plans(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    child = await _get_child_or_404(db, child_id, user.household_id)
    base = select(Plan).where(Plan.child_id == child_id, Plan.household_id == user.household_id)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(Plan.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [PlanResponse.model_validate(p) for p in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


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
    user: User = Depends(require_permission("approve.activities")),
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

    now = datetime.now(UTC)
    activity.status = ActivityStatus.scheduled
    activity.governance_approved = True
    activity.governance_reviewed_by = user.id
    activity.governance_reviewed_at = now

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
    user: User = Depends(require_permission("rules.edit")),
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

    now = datetime.now(UTC)
    activity.status = ActivityStatus.cancelled
    activity.governance_reviewed_by = user.id
    activity.governance_reviewed_at = now

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
    user: User = Depends(require_permission("rules.edit")),
) -> dict:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)

    # Verify all non-cancelled activities are governance-approved
    weeks_result = await db.execute(
        select(PlanWeek).where(PlanWeek.plan_id == plan_id)
    )
    week_ids = [w.id for w in weeks_result.scalars().all()]

    if week_ids:
        unapproved_result = await db.execute(
            select(Activity).where(
                Activity.plan_week_id.in_(week_ids),
                Activity.governance_approved == False,  # noqa: E712
                Activity.status != ActivityStatus.cancelled,
            )
        )
        unapproved = unapproved_result.scalars().all()
        if unapproved:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Cannot lock plan with unapproved activities",
                    "unapproved_activity_ids": [str(a.id) for a in unapproved],
                },
            )

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
    user: User = Depends(require_permission("export.data")),
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

    # Build context with node content if available
    node_title = "General"
    content_guidance = ""
    if activity.node_id:
        node_result = await db.execute(
            select(LearningNode).where(LearningNode.id == activity.node_id)
        )
        node = node_result.scalar_one_or_none()
        if node:
            node_title = node.title
            if node.content and node.content.get("teaching_guidance"):
                tg = node.content["teaching_guidance"]
                parts = []
                if tg.get("socratic_questions"):
                    parts.append(f"Key questions to ask: {', '.join(tg['socratic_questions'][:3])}")
                if tg.get("common_misconceptions"):
                    parts.append(f"Watch for misconceptions: {', '.join(tg['common_misconceptions'][:2])}")
                if tg.get("scaffolding_sequence"):
                    parts.append(f"Scaffolding: {' -> '.join(tg['scaffolding_sequence'][:3])}")
                if parts:
                    content_guidance = "\n\nTEACHING GUIDANCE:\n" + "\n".join(f"- {p}" for p in parts)

    user_prompt = f"""Activity: {activity.title}
Learning Topic: {node_title}
{content_guidance}

Child says: {body.message}

Respond using the Socratic method. Guide the child toward understanding without giving the answer."""

    phil = await _get_philosophical_profile(db, user.household_id)
    result = await call_ai(
        db,
        role=AIRole.tutor,
        system_prompt=TUTOR_SYSTEM,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
        philosophical_profile=phil,
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
    user: User = Depends(require_permission("approve.activities")),
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

    phil = await _get_philosophical_profile(db, user.household_id)
    result = await call_ai(
        db,
        role=AIRole.cartographer,
        system_prompt=CARTOGRAPHER_SYSTEM,
        user_prompt=user_prompt,
        philosophical_profile=phil,
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
    user: User = Depends(require_permission("approve.activities")),
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

    phil = await _get_philosophical_profile(db, user.household_id)
    result = await call_ai(
        db,
        role=AIRole.advisor,
        system_prompt=ADVISOR_SYSTEM,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
        philosophical_profile=phil,
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


@router.get("/children/{child_id}/advisor-reports")
async def list_advisor_reports(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    child = await _get_child_or_404(db, child_id, user.household_id)
    base = select(AdvisorReport).where(
        AdvisorReport.child_id == child_id, AdvisorReport.household_id == user.household_id,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(AdvisorReport.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [AdvisorReportResponse.model_validate(r) for r in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


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

@router.get("/ai-runs")
async def list_ai_runs(
    child_id: uuid.UUID | None = Query(default=None),
    role: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    base = select(AIRun).where(AIRun.household_id == user.household_id)
    if role:
        base = base.where(AIRun.run_type == role)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(AIRun.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [AIRunResponse.model_validate(r) for r in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


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


@router.get("/governance-events")
async def list_governance_events(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    base = select(GovernanceEvent).where(GovernanceEvent.household_id == user.household_id)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(GovernanceEvent.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [GovernanceEventResponse.model_validate(e) for e in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


# ══════════════════════════════════════════════════
# Approval Queue
# ══════════════════════════════════════════════════

@router.get("/governance/queue")
async def governance_queue(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    """All activities pending governance approval across all children."""
    from app.models.identity import Child

    base = select(Activity).where(
        Activity.household_id == user.household_id,
        Activity.governance_approved == False,  # noqa: E712
        Activity.status != ActivityStatus.cancelled,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0

    result = await db.execute(
        base.order_by(Activity.created_at.desc())
        .offset(pagination.skip).limit(pagination.limit)
    )
    activities = result.scalars().all()

    # Resolve child names and plan names in batch
    plan_week_ids = list({a.plan_week_id for a in activities})
    child_ids: set[uuid.UUID] = set()
    week_to_plan: dict[uuid.UUID, uuid.UUID] = {}

    if plan_week_ids:
        weeks_result = await db.execute(
            select(PlanWeek).where(PlanWeek.id.in_(plan_week_ids))
        )
        for w in weeks_result.scalars().all():
            week_to_plan[w.id] = w.plan_id

    plan_ids = list(set(week_to_plan.values()))
    plan_names: dict[uuid.UUID, tuple[str, uuid.UUID]] = {}
    if plan_ids:
        plans_result = await db.execute(
            select(Plan).where(Plan.id.in_(plan_ids))
        )
        for p in plans_result.scalars().all():
            plan_names[p.id] = (p.name, p.child_id)
            child_ids.add(p.child_id)

    child_names: dict[uuid.UUID, str] = {}
    if child_ids:
        children_result = await db.execute(
            select(Child).where(Child.id.in_(list(child_ids)))
        )
        for c in children_result.scalars().all():
            child_names[c.id] = f"{c.first_name} {c.last_name or ''}".strip()

    items = []
    for a in activities:
        plan_id = week_to_plan.get(a.plan_week_id)
        plan_info = plan_names.get(plan_id) if plan_id else None
        plan_name = plan_info[0] if plan_info else "Unknown"
        a_child_id = plan_info[1] if plan_info else None
        child_name = child_names.get(a_child_id) if a_child_id else "Unknown"
        instructions = a.instructions or {}

        items.append({
            "activity_id": str(a.id),
            "title": a.title,
            "activity_type": a.activity_type.value if hasattr(a.activity_type, "value") else str(a.activity_type),
            "estimated_minutes": a.estimated_minutes,
            "difficulty": instructions.get("difficulty"),
            "ai_rationale": instructions.get("ai_rationale", ""),
            "scheduled_date": a.scheduled_date.isoformat() if a.scheduled_date else None,
            "child_name": child_name,
            "child_id": str(a_child_id) if a_child_id else None,
            "plan_name": plan_name,
            "plan_id": str(plan_id) if plan_id else None,
        })

    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }
