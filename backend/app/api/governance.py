# subscription_exempt: mixed file — AI/generation routes (plans/generate, tutor, cartographer, advisor-reports/generate) gated per-route
# See fix/methean6-08-subscription-gating for classification rationale.
"""Parent Governance + AI Integration API.

Plan generation, governance rules CRUD, plan approve/reject/lock,
tutor interaction, cartographer calibration, advisor reports,
AI inspection endpoints.
"""

import json
import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai, load_personalization_context
from app.ai.prompts import (
    ADVISOR_SYSTEM,
    CARTOGRAPHER_SYSTEM,
    TUTOR_SYSTEM,
    render_tutor_system,
)
from app.api.deps import (
    PaginationParams,
    get_current_user,
    get_db,
    require_active_subscription,
    require_child_access,
    require_permission,
    require_role,
)
from app.core.config import settings
from app.core.rate_limit import rate_limit_user
from app.models.curriculum import LearningMap, LearningNode
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AIRunStatus,
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
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


async def _get_plan_or_404(
    db: AsyncSession,
    plan_id: uuid.UUID,
    household_id: uuid.UUID,
) -> Plan:
    result = await db.execute(select(Plan).where(Plan.id == plan_id, Plan.household_id == household_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


async def _get_philosophical_profile(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> dict | None:
    from app.models.identity import Household

    result = await db.execute(select(Household).where(Household.id == household_id))
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


def _validate_rule_params(rule_type: str, params: dict) -> str | None:
    """Return error message if params are invalid for the rule type."""
    if rule_type == "pace_limit":
        v = params.get("max_daily_minutes")
        if v is not None and (not isinstance(v, (int, float)) or v < 0 or v > 1440):
            return "max_daily_minutes must be between 0 and 1440"
        w = params.get("max_weekly_minutes")
        if w is not None and (not isinstance(w, (int, float)) or w < 0 or w > 10080):
            return "max_weekly_minutes must be between 0 and 10080"
    elif rule_type == "schedule_constraint":
        days = params.get("allowed_days", [])
        valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        if days and any(d not in valid_days for d in days):
            return f"allowed_days must be from: {', '.join(sorted(valid_days))}"
    elif rule_type == "content_filter":
        if not params.get("topic"):
            return "content_filter rules require a 'topic' parameter"
        valid_stances = {"exclude", "present_alternative", "parent_led_only", "age_appropriate"}
        if params.get("stance") and params["stance"] not in valid_stances:
            return f"stance must be one of: {', '.join(sorted(valid_stances))}"
    elif rule_type == "ai_boundary":
        valid_transparency = {"full", "summary", "minimal"}
        if params.get("ai_transparency") and params["ai_transparency"] not in valid_transparency:
            return f"ai_transparency must be one of: {', '.join(sorted(valid_transparency))}"
    return None


@router.post("/governance-rules", response_model=GovernanceRuleResponse, status_code=201)
async def create_governance_rule(
    body: GovernanceRuleCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("rules.create")),
) -> GovernanceRuleResponse:
    from app.core.permissions import PERM_RULES_CONSTITUTIONAL, check_permission
    from app.models.enums import RuleTier

    # Validate parameters
    rule_type_str = body.rule_type.value if hasattr(body.rule_type, "value") else str(body.rule_type)
    param_err = _validate_rule_params(rule_type_str, body.parameters or {})
    if param_err:
        raise HTTPException(status_code=400, detail=param_err)

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
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        target_type,
        rule.id,
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

    if body.parameters is not None:
        rt = rule.rule_type.value if hasattr(rule.rule_type, "value") else str(rule.rule_type)
        param_err = _validate_rule_params(rt, body.parameters)
        if param_err:
            raise HTTPException(status_code=400, detail=param_err)

    is_constitutional = (
        (
            (rule.tier == RuleTier.constitutional)
            if hasattr(rule.tier, "value") is False
            else (
                rule.tier.value == "constitutional"
                if hasattr(rule.tier, "value")
                else str(rule.tier) == "constitutional"
            )
        )
        or (rule.tier == "constitutional")
        or (rule.tier == RuleTier.constitutional)
    )

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
        "name": rule.name,
        "description": rule.description,
        "parameters": rule.parameters,
        "priority": rule.priority,
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
        "name": rule.name,
        "description": rule.description,
        "parameters": rule.parameters,
        "priority": rule.priority,
        "is_active": rule.is_active,
    }

    await db.flush()
    await db.refresh(rule)

    target_type = "constitutional_rule_change" if is_constitutional else "governance_rule"
    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        target_type,
        rule.id,
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
        db,
        user.household_id,
        body.period_start,
        body.period_end,
        user.id,
    )

    # Log the export
    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.approve,
        "governance_report",
        user.household_id,
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
        items.append(
            {
                "rule_id": str(r.id),
                "rule_name": r.name,
                "trigger_type": tc.get("type"),
                "trigger_conditions": tc,
                "effective_from": r.effective_from.isoformat() if r.effective_from else None,
                "is_active": r.is_active,
            }
        )
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


@router.post(
    "/children/{child_id}/plans/generate",
    response_model=PlanResponse,
    status_code=201,
    dependencies=[Depends(require_active_subscription)],
)
async def generate_plan_endpoint(
    child_id: uuid.UUID,
    body: PlanGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("plans.generate")),
    _child: Child = Depends(require_child_access("write")),
) -> PlanResponse:
    await _get_child_or_404(db, child_id, user.household_id)

    result = await generate_plan(
        db,
        child_id,
        user.household_id,
        user.id,
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
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    base = select(Plan).where(Plan.child_id == child_id, Plan.household_id == user.household_id)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(base.order_by(Plan.created_at.desc()).offset(pagination.skip).limit(pagination.limit))
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
    weeks_result = await db.execute(select(PlanWeek).where(PlanWeek.plan_id == plan_id))
    weeks = weeks_result.scalars().all()
    week_ids = [w.id for w in weeks]

    activities = []
    if week_ids:
        act_result = await db.execute(
            select(Activity).where(Activity.plan_week_id.in_(week_ids)).order_by(Activity.sort_order)
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
        db,
        user.household_id,
        user.id,
        GovernanceAction.approve,
        "activity",
        activity_id,
        reason=body.reason if body else "Parent approved",
        metadata={"source": "manual"},
    )

    # Invalidate governance queue cache
    from app.core.cache import cache_delete_pattern

    await cache_delete_pattern(f"gov_queue:{user.household_id}:*")

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
        db,
        user.household_id,
        user.id,
        GovernanceAction.reject,
        "activity",
        activity_id,
        reason=body.reason or "Parent rejected",
        metadata={"source": "manual"},
    )

    from app.core.cache import cache_delete_pattern

    await cache_delete_pattern(f"gov_queue:{user.household_id}:*")

    return {"activity_id": str(activity_id), "status": "rejected"}


@router.put("/activities/{activity_id}/reschedule")
async def reschedule_activity(
    activity_id: uuid.UUID,
    body: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Move an activity to a different day."""
    result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id,
            Activity.household_id == user.household_id,
        )
    )
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    from datetime import date as date_type

    old_date = activity.scheduled_date
    new_date_str = body.get("new_date")
    if not new_date_str:
        raise HTTPException(status_code=400, detail="new_date required")
    new_date = date_type.fromisoformat(new_date_str)
    activity.scheduled_date = new_date

    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        "activity",
        activity_id,
        reason=f"Rescheduled from {old_date} to {new_date}",
    )

    return {"activity_id": str(activity_id), "scheduled_date": str(new_date)}


class ManualActivityCreate(BaseModel):
    child_id: uuid.UUID
    title: str
    activity_type: str = "lesson"
    scheduled_date: date
    estimated_minutes: int = 30
    description: str | None = None
    subject_area: str | None = None
    node_id: uuid.UUID | None = None
    tools_required: list[str] | None = None
    materials: list[dict] | None = None
    safety_notes: str | None = None
    workspace: str | None = None


@router.post("/activities", status_code=201)
async def create_manual_activity(
    body: ManualActivityCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Create a manually scheduled activity (not AI-generated)."""
    from app.models.identity import Child

    child_r = await db.execute(select(Child).where(Child.id == body.child_id, Child.household_id == user.household_id))
    child = child_r.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    # Find or create plan for this week
    week_start = body.scheduled_date - timedelta(days=body.scheduled_date.weekday())
    week_end = week_start + timedelta(days=4)

    plan_r = await db.execute(
        select(Plan)
        .where(
            Plan.child_id == body.child_id,
            Plan.household_id == user.household_id,
            Plan.start_date <= body.scheduled_date,
            Plan.end_date >= body.scheduled_date,
        )
        .limit(1)
    )
    plan = plan_r.scalar_one_or_none()
    if not plan:
        plan = Plan(
            household_id=user.household_id,
            child_id=body.child_id,
            created_by=user.id,
            name=f"Week of {week_start}",
            status=PlanStatus.active,
            start_date=week_start,
            end_date=week_end,
        )
        db.add(plan)
        await db.flush()

    # Find or create plan_week
    pw_r = await db.execute(
        select(PlanWeek)
        .where(
            PlanWeek.plan_id == plan.id,
            PlanWeek.start_date <= body.scheduled_date,
            PlanWeek.end_date >= body.scheduled_date,
        )
        .limit(1)
    )
    pw = pw_r.scalar_one_or_none()
    if not pw:
        pw = PlanWeek(
            plan_id=plan.id, household_id=user.household_id, week_number=1, start_date=week_start, end_date=week_end
        )
        db.add(pw)
        await db.flush()

    activity = Activity(
        plan_week_id=pw.id,
        household_id=user.household_id,
        node_id=body.node_id,
        activity_type=ActivityType(body.activity_type),
        title=body.title,
        description=body.description,
        instructions={
            **({"subject_area": body.subject_area} if body.subject_area else {}),
            **({"tools_required": body.tools_required} if body.tools_required else {}),
            **({"materials": body.materials} if body.materials else {}),
            **({"safety_notes": body.safety_notes} if body.safety_notes else {}),
            **({"workspace": body.workspace} if body.workspace else {}),
        },
        estimated_minutes=body.estimated_minutes,
        status=ActivityStatus.scheduled,
        scheduled_date=body.scheduled_date,
        governance_approved=True,
        governance_reviewed_by=user.id,
        governance_reviewed_at=datetime.now(UTC),
    )
    db.add(activity)
    await db.flush()

    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.approve,
        "activity",
        activity.id,
        reason="Manually created by parent",
        metadata={"source": "manual"},
    )
    await db.commit()
    return {"id": str(activity.id), "title": activity.title, "scheduled_date": str(body.scheduled_date)}


class TimeLogCreate(BaseModel):
    date_val: date = Field(alias="date")
    minutes: int = Field(ge=1, le=1440)
    subject_area: str
    description: str | None = None

    model_config = {"populate_by_name": True}


@router.post("/children/{child_id}/time-log", status_code=201)
async def log_manual_time(
    child_id: uuid.UUID,
    body: TimeLogCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    """Log manual learning time for compliance tracking."""
    from app.models.evidence import ReadingLogEntry
    from app.models.identity import Child

    child_r = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == user.household_id))
    child = child_r.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    entry = ReadingLogEntry(
        household_id=user.household_id,
        child_id=child_id,
        created_by=user.id,
        book_title=body.subject_area,
        book_author=body.description or "",
        genre="manual_time",
        subject_area=body.subject_area,
        status="completed",
        minutes_spent=body.minutes,
        started_date=body.date_val,
        completed_date=body.date_val,
    )
    db.add(entry)
    await db.commit()
    return {"id": str(entry.id), "minutes": body.minutes, "subject": body.subject_area}


@router.put("/plans/{plan_id}/lock")
async def lock_plan(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("rules.edit")),
) -> dict:
    plan = await _get_plan_or_404(db, plan_id, user.household_id)

    # Verify all non-cancelled activities are governance-approved
    weeks_result = await db.execute(select(PlanWeek).where(PlanWeek.plan_id == plan_id))
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
        db,
        user.household_id,
        user.id,
        GovernanceAction.approve,
        "plan",
        plan_id,
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


@router.post(
    "/tutor/{activity_id}/message",
    response_model=TutorMessageResponse,
    dependencies=[
        Depends(require_active_subscription),
        Depends(rate_limit_user("tutor_message")),
    ],
)
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
        node_result = await db.execute(select(LearningNode).where(LearningNode.id == activity.node_id))
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

    # Build conversation context from history
    conversation_context = ""
    if body.conversation_history:
        recent = body.conversation_history[-10:]  # Last 10 messages max
        lines = []
        for msg in recent:
            role_label = "Child" if msg.get("role") == "child" else "Tutor"
            lines.append(f"{role_label}: {msg.get('text', '')}")
        conversation_context = "\n\nCONVERSATION SO FAR:\n" + "\n".join(lines)

    user_prompt = f"""Activity: {activity.title}
Learning Topic: {node_title}
{content_guidance}
{conversation_context}

Child's latest message: {body.message}

Continue the Socratic dialogue. Reference what was discussed earlier if relevant. Guide toward understanding without giving answers."""

    # Assemble context via centralized service (advisory, never blocking)
    assembled_ctx = ""
    try:
        from app.services.context_assembly import assemble_context

        if body.child_id:
            assembled = await assemble_context(
                db,
                role="tutor",
                child_id=body.child_id,
                household_id=user.household_id,
                activity_id=activity_id,
                node_id=activity.node_id,
            )
            assembled_ctx = assembled["context_text"]
            if assembled_ctx:
                user_prompt += f"\n\n{assembled_ctx}"
    except Exception:
        pass

    phil = await _get_philosophical_profile(db, user.household_id)
    # Load personalization once per request so prompt assembly stays
    # synchronous; render_tutor_system never hits the DB itself.
    pctx = await load_personalization_context(db, body.child_id) if body.child_id else None
    tutor_system = render_tutor_system(pctx, voice_mode=body.voice_mode) if pctx is not None else TUTOR_SYSTEM
    result = await call_ai(
        db,
        role=AIRole.tutor,
        system_prompt=tutor_system,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
        philosophical_profile=phil,
        assembled_context=assembled_ctx,
    )

    output = result["output"]

    # Record tutor interaction for style vector computation (advisory)
    try:
        from app.services.intelligence import record_tutor_interaction

        child_id = body.child_id
        if child_id:
            history_len = len(body.conversation_history or [])
            hints_in_response = len(output.get("hints", []))
            await record_tutor_interaction(
                db,
                child_id,
                user.household_id,
                subject=node_title or activity.title or "general",
                messages_count=history_len + 1,  # includes current message
                hints_used=hints_in_response,
                self_corrections=0,  # tracked client-side if available
            )
    except Exception:
        pass  # Intelligence recording is advisory, never blocking

    response_message = output.get("message", "Could you tell me more about your thinking?")
    if body.voice_mode:
        from app.services.sentence_truncate import truncate_to_sentences

        response_message = truncate_to_sentences(response_message, max_sentences=2)
    return TutorMessageResponse(
        message=response_message,
        hints=output.get("hints", []),
        encouragement=output.get("encouragement", True),
        ai_run_id=result["ai_run_id"],
    )


@router.post(
    "/tutor/{activity_id}/stream",
    dependencies=[
        Depends(require_active_subscription),
        Depends(rate_limit_user("tutor_message")),
    ],
)
async def tutor_stream(
    activity_id: uuid.UUID,
    body: TutorMessageRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Stream tutor response token-by-token via Server-Sent Events."""
    import asyncio

    from starlette.responses import StreamingResponse

    from app.ai.gateway import stream_claude
    from app.ai.prompts import build_philosophical_constraints

    # Verify activity
    act_result = await db.execute(
        select(Activity).where(Activity.id == activity_id, Activity.household_id == user.household_id)
    )
    activity = act_result.scalar_one_or_none()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Build context (same as non-streaming)
    node_title = "General"
    content_guidance = ""
    if activity.node_id:
        node_result = await db.execute(select(LearningNode).where(LearningNode.id == activity.node_id))
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

    conversation_context = ""
    if body.conversation_history:
        recent = body.conversation_history[-10:]
        lines = []
        for msg in recent:
            role_label = "Child" if msg.get("role") == "child" else "Tutor"
            lines.append(f"{role_label}: {msg.get('text', '')}")
        conversation_context = "\n\nCONVERSATION SO FAR:\n" + "\n".join(lines)

    user_prompt = f"""Activity: {activity.title}
Learning Topic: {node_title}
{content_guidance}
{conversation_context}

Child's latest message: {body.message}

Respond in plain text as the Socratic tutor. Do NOT use JSON. Just speak naturally to the child. If you want to include a hint, put it on its own line starting with "HINT:" at the very end of your response."""

    # Assemble context (advisory)
    try:
        from app.services.context_assembly import assemble_context

        if body.child_id:
            assembled = await assemble_context(
                db,
                role="tutor",
                child_id=body.child_id,
                household_id=user.household_id,
                activity_id=activity_id,
                node_id=activity.node_id,
            )
            if assembled.get("context_text"):
                user_prompt += f"\n\n{assembled['context_text']}"
    except Exception:
        pass

    phil = await _get_philosophical_profile(db, user.household_id)
    pctx = await load_personalization_context(db, body.child_id) if body.child_id else None
    system = render_tutor_system(pctx, voice_mode=body.voice_mode) if pctx is not None else TUTOR_SYSTEM
    constraints = build_philosophical_constraints(phil)
    if constraints:
        system = system + "\n" + constraints

    # Mock fallback
    if not settings.AI_API_KEY or settings.AI_MOCK_ENABLED:
        mock_text = (
            "That's a great start! Can you tell me more about how you arrived at that answer? What steps did you take?"
        )

        async def mock_stream():
            words = mock_text.split(" ")
            for i, word in enumerate(words):
                chunk = word if i == 0 else " " + word
                yield f"data: {json.dumps({'type': 'token', 'text': chunk})}\n\n"
                await asyncio.sleep(0.05)
            yield f"data: {json.dumps({'type': 'done', 'hints': ['Think about the relationship between the parts'], 'ai_run_id': str(uuid.uuid4())})}\n\n"

        return StreamingResponse(
            mock_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    # Log AIRun
    ai_run = AIRun(
        household_id=user.household_id,
        triggered_by=user.id,
        run_type="tutor",
        status=AIRunStatus.completed,
        started_at=datetime.now(UTC),
        input_log={"system_prompt": system[:500], "user_prompt": user_prompt[:500]},
    )
    db.add(ai_run)
    await db.flush()
    run_id = ai_run.id
    full_text: list[str] = []

    # Resolve the household's AI tier so stream_claude uses the right model.
    from app.models.identity import Household as _Household

    hh_row = (await db.execute(select(_Household).where(_Household.id == user.household_id))).scalar_one_or_none()
    tier = (hh_row.settings or {}).get("ai_tier", "opus") if hh_row else "opus"
    stream_tier_models = {
        "opus": settings.AI_PRIMARY_MODEL,
        "sonnet": settings.AI_STANDARD_MODEL,
        "haiku": settings.AI_LIGHT_MODEL,
    }
    stream_model = stream_tier_models.get(tier, settings.AI_PRIMARY_MODEL)

    async def event_generator():
        async for event_type, data in stream_claude(system, user_prompt, settings.AI_MAX_TOKENS, model=stream_model):
            if event_type == "token":
                full_text.append(data)
                yield f"data: {json.dumps({'type': 'token', 'text': data})}\n\n"
            elif event_type == "done":
                accumulated = "".join(full_text)
                hints: list[str] = []
                if "HINT:" in accumulated:
                    parts = accumulated.rsplit("HINT:", 1)
                    hints = [parts[1].strip()]
                yield f"data: {json.dumps({'type': 'done', 'hints': hints, 'ai_run_id': str(run_id)})}\n\n"
                try:
                    ai_run.output_log = {"message": accumulated[:1000], "hints": hints}
                    ai_run.completed_at = datetime.now(UTC)
                    ai_run.model_used = data.get("model", "")
                    ai_run.input_tokens = data.get("input_tokens", 0)
                    ai_run.output_tokens = data.get("output_tokens", 0)
                    await db.commit()
                except Exception:
                    pass
                try:
                    from app.services.intelligence import record_tutor_interaction

                    if body.child_id:
                        await record_tutor_interaction(
                            db,
                            body.child_id,
                            user.household_id,
                            subject=node_title or activity.title or "general",
                            messages_count=len(body.conversation_history or []) + 1,
                            hints_used=len(hints),
                            self_corrections=0,
                        )
                except Exception:
                    pass
            elif event_type == "error":
                yield f"data: {json.dumps({'type': 'error', 'message': 'I had trouble thinking. Try again in a moment.'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ══════════════════════════════════════════════════
# Cartographer
# ══════════════════════════════════════════════════


@router.post(
    "/children/{child_id}/cartographer/calibrate",
    response_model=CartographerRecommendation,
    dependencies=[Depends(require_active_subscription)],
)
async def cartographer_calibrate(
    child_id: uuid.UUID,
    body: CartographerCalibrateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("approve.activities")),
    _child: Child = Depends(require_child_access("write")),
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
{json.dumps([{"id": str(n.id), "title": n.title, "type": n.node_type.value if hasattr(n.node_type, "value") else str(n.node_type)} for n in nodes], indent=2)}

Provide calibration recommendations."""

    # Assemble context via centralized service (advisory, never blocking)
    assembled_ctx = ""
    try:
        from app.services.context_assembly import assemble_context

        assembled = await assemble_context(
            db,
            role="cartographer",
            child_id=child_id,
            household_id=user.household_id,
        )
        assembled_ctx = assembled["context_text"]
        if assembled_ctx:
            user_prompt += f"\n\n{assembled_ctx}"
    except Exception:
        pass

    phil = await _get_philosophical_profile(db, user.household_id)
    result = await call_ai(
        db,
        role=AIRole.cartographer,
        system_prompt=CARTOGRAPHER_SYSTEM,
        user_prompt=user_prompt,
        philosophical_profile=phil,
        household_id=user.household_id,
        triggered_by=user.id,
        assembled_context=assembled_ctx,
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


@router.post(
    "/children/{child_id}/advisor-reports/generate",
    response_model=AdvisorReportResponse,
    status_code=201,
    dependencies=[Depends(require_active_subscription)],
)
async def generate_advisor_report(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("approve.activities")),
    _child: Child = Depends(require_child_access("write")),
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

    # Assemble context via centralized service (advisory, never blocking)
    assembled_ctx = ""
    try:
        from app.services.context_assembly import assemble_context

        assembled = await assemble_context(
            db,
            role="advisor",
            child_id=child_id,
            household_id=user.household_id,
        )
        assembled_ctx = assembled["context_text"]
        if assembled_ctx:
            user_prompt += f"\n\n{assembled_ctx}"
    except Exception:
        pass

    phil = await _get_philosophical_profile(db, user.household_id)
    result = await call_ai(
        db,
        role=AIRole.advisor,
        system_prompt=ADVISOR_SYSTEM,
        user_prompt=user_prompt,
        household_id=user.household_id,
        triggered_by=user.id,
        philosophical_profile=phil,
        assembled_context=assembled_ctx,
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
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    base = select(AdvisorReport).where(
        AdvisorReport.child_id == child_id,
        AdvisorReport.household_id == user.household_id,
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
    result = await db.execute(base.order_by(AIRun.created_at.desc()).offset(pagination.skip).limit(pagination.limit))
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


@router.get("/ai-runs/{run_id}/context-detail")
async def get_ai_run_context_detail(
    run_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Returns structured context breakdown for an AIRun.

    Parses the assembled_context from input_data and returns source-level detail.
    For legacy runs without assembled context, returns the raw input_data.
    """
    result = await db.execute(select(AIRun).where(AIRun.id == run_id, AIRun.household_id == user.household_id))
    ai_run = result.scalar_one_or_none()
    if not ai_run:
        raise HTTPException(status_code=404, detail="AI run not found")

    input_data = ai_run.input_data or {}
    role = input_data.get("role", ai_run.run_type)
    assembled_context = input_data.get("assembled_context", "")

    if not assembled_context:
        # Legacy run without context assembly
        return {
            "role": role,
            "legacy": True,
            "token_budget": 0,
            "tokens_used": 0,
            "sources": [],
            "sources_excluded": [],
            "context_text": "",
            "raw_input": input_data,
        }

    # Parse context into source blocks by looking for section headers
    from app.services.context_assembly import ROLE_PROFILES, estimate_tokens

    profile = ROLE_PROFILES.get(role)
    budget = profile.total_token_budget if profile else 0

    tokens_used = estimate_tokens(assembled_context)

    # Build source list from the profile (we know which sources could have contributed)
    sources = []
    sources_excluded = []
    if profile:
        # Split context by double-newlines to estimate per-source tokens
        blocks = [b.strip() for b in assembled_context.split("\n\n") if b.strip()]
        block_tokens = [estimate_tokens(b) for b in blocks]

        # Match blocks to profile sources by order (best effort)
        [s.name for s in profile.sources]
        for i, source in enumerate(profile.sources):
            if i < len(blocks):
                sources.append(
                    {
                        "name": source.name,
                        "tokens": block_tokens[i] if i < len(block_tokens) else 0,
                        "required": source.required,
                        "truncated": "[...truncated]" in blocks[i] if i < len(blocks) else False,
                    }
                )
            else:
                sources_excluded.append(source.name)

    return {
        "role": role,
        "legacy": False,
        "token_budget": budget,
        "tokens_used": tokens_used,
        "sources": sources,
        "sources_excluded": sources_excluded,
        "context_text": assembled_context,
    }


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
        run_result = await db.execute(select(AIRun).where(AIRun.id == plan.ai_run_id))
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
        acts_result = await db.execute(select(Activity).where(Activity.plan_week_id.in_(week_ids)))
        activities = acts_result.scalars().all()

        for act in activities:
            events_result = await db.execute(
                select(GovernanceEvent)
                .where(
                    GovernanceEvent.target_type == "activity",
                    GovernanceEvent.target_id == act.id,
                )
                .order_by(GovernanceEvent.created_at.asc())
            )
            events = events_result.scalars().all()

            activity_decisions.append(
                {
                    "activity_id": str(act.id),
                    "title": act.title,
                    "status": act.status.value if hasattr(act.status, "value") else str(act.status),
                    "instructions": act.instructions,
                    "governance_events": [
                        {
                            "action": e.action.value if hasattr(e.action, "value") else str(e.action),
                            "reason": e.reason,
                            "metadata": e.metadata_,
                            "created_at": e.created_at.isoformat() if e.created_at else None,
                        }
                        for e in events
                    ],
                }
            )

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
    from app.core.cache import cache_get, cache_set
    from app.models.identity import Child

    cache_key = f"gov_queue:{user.household_id}:{pagination.skip}:{pagination.limit}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    base = select(Activity).where(
        Activity.household_id == user.household_id,
        Activity.governance_approved == False,  # noqa: E712
        Activity.status != ActivityStatus.cancelled,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0

    result = await db.execute(base.order_by(Activity.created_at.desc()).offset(pagination.skip).limit(pagination.limit))
    activities = result.scalars().all()

    # Resolve child names and plan names in batch
    plan_week_ids = list({a.plan_week_id for a in activities})
    child_ids: set[uuid.UUID] = set()
    week_to_plan: dict[uuid.UUID, uuid.UUID] = {}

    if plan_week_ids:
        weeks_result = await db.execute(select(PlanWeek).where(PlanWeek.id.in_(plan_week_ids)))
        for w in weeks_result.scalars().all():
            week_to_plan[w.id] = w.plan_id

    plan_ids = list(set(week_to_plan.values()))
    plan_names: dict[uuid.UUID, tuple[str, uuid.UUID]] = {}
    if plan_ids:
        plans_result = await db.execute(select(Plan).where(Plan.id.in_(plan_ids)))
        for p in plans_result.scalars().all():
            plan_names[p.id] = (p.name, p.child_id)
            child_ids.add(p.child_id)

    child_names: dict[uuid.UUID, str] = {}
    if child_ids:
        children_result = await db.execute(select(Child).where(Child.id.in_(list(child_ids))))
        for c in children_result.scalars().all():
            child_names[c.id] = f"{c.first_name} {c.last_name or ''}".strip()

    # Fetch governance evaluations for pending activities
    activity_ids = [a.id for a in activities]
    gov_evals: dict[uuid.UUID, dict] = {}
    if activity_ids:
        for aid in activity_ids:
            ev_result = await db.execute(
                select(GovernanceEvent)
                .where(
                    GovernanceEvent.target_id == aid,
                    GovernanceEvent.household_id == user.household_id,
                )
                .order_by(GovernanceEvent.created_at.desc())
                .limit(1)
            )
            ev = ev_result.scalar_one_or_none()
            if ev and ev.metadata_:
                gov_evals[aid] = ev.metadata_

    items = []
    for a in activities:
        plan_id = week_to_plan.get(a.plan_week_id)
        plan_info = plan_names.get(plan_id) if plan_id else None
        plan_name = plan_info[0] if plan_info else "Unknown"
        a_child_id = plan_info[1] if plan_info else None
        child_name = child_names.get(a_child_id) if a_child_id else "Unknown"
        instructions = a.instructions or {}

        items.append(
            {
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
                "governance_evaluation": gov_evals.get(a.id, {}),
            }
        )

    response = {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }
    await cache_set(cache_key, response, ttl_seconds=15)
    return response
