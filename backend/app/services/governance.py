"""Governance Rules Engine.

Evaluates recommendations against all active household rules.
Enforces: approval_required, pace_limit, content_filter,
schedule_constraint, and ai_boundary rules.
"""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import GovernanceAction, RuleScope, RuleTier, RuleType
from app.models.governance import Activity, Attempt, GovernanceEvent, GovernanceRule
from app.models.operational import AIRun


# ══════════════════════════════════════════════════
# Data classes
# ══════════════════════════════════════════════════


@dataclass
class ActivityContext:
    """Everything needed to evaluate governance rules against an activity."""
    household_id: uuid.UUID
    child_id: uuid.UUID | None = None
    activity_type: str | None = None
    difficulty: int | None = None
    subject_id: uuid.UUID | None = None
    node_id: uuid.UUID | None = None
    scheduled_date: date | None = None
    scheduled_time: str | None = None
    estimated_minutes: int | None = None
    content_topics: list[str] | None = None
    ai_role: str | None = None


@dataclass
class RuleEvaluation:
    """Result of evaluating a single rule."""
    rule_id: uuid.UUID
    rule_name: str
    rule_type: str
    tier: str
    passed: bool
    action: str  # pass, auto_approve, require_review, block, warn
    reason: str


@dataclass
class GovernanceDecision:
    """Aggregate decision after evaluating all rules."""
    action: str  # auto_approve, require_review, block
    reason: str
    evaluations: list[RuleEvaluation] = field(default_factory=list)
    blocking_rules: list[RuleEvaluation] = field(default_factory=list)
    passed_rules: list[RuleEvaluation] = field(default_factory=list)
    constitutional_violations: list[RuleEvaluation] = field(default_factory=list)

    # Backward compatibility
    @property
    def rule_id(self) -> uuid.UUID | None:
        return self.blocking_rules[0].rule_id if self.blocking_rules else None

    @property
    def rule_name(self) -> str | None:
        return self.blocking_rules[0].rule_name if self.blocking_rules else None


# ══════════════════════════════════════════════════
# Per-type evaluators
# ══════════════════════════════════════════════════


def _eval_result(rule: GovernanceRule, passed: bool, action: str, reason: str) -> RuleEvaluation:
    tier = rule.tier.value if hasattr(rule.tier, "value") else str(rule.tier)
    return RuleEvaluation(
        rule_id=rule.id, rule_name=rule.name,
        rule_type=rule.rule_type.value if hasattr(rule.rule_type, "value") else str(rule.rule_type),
        tier=tier, passed=passed, action=action, reason=reason,
    )


async def _evaluate_approval(db: AsyncSession, rule: GovernanceRule, ctx: ActivityContext) -> RuleEvaluation:
    params = rule.parameters or {}
    action = params.get("action", "require_review")

    # Check activity type filter
    type_filter = params.get("activity_types", [])
    if type_filter and ctx.activity_type and ctx.activity_type not in type_filter:
        return _eval_result(rule, True, "pass", "Activity type not in filter")

    if ctx.difficulty is not None:
        max_diff = params.get("max_difficulty")
        min_diff = params.get("min_difficulty")
        if max_diff is not None and ctx.difficulty < max_diff:
            return _eval_result(rule, action == "auto_approve", action,
                f"Difficulty {ctx.difficulty} < threshold {max_diff}")
        if min_diff is not None and ctx.difficulty >= min_diff:
            return _eval_result(rule, action == "auto_approve", action,
                f"Difficulty {ctx.difficulty} >= threshold {min_diff}")

    if action == "always_review":
        return _eval_result(rule, False, "require_review", "All activities require review")

    return _eval_result(rule, True, "pass", "No difficulty match")


async def _evaluate_pace_limit(db: AsyncSession, rule: GovernanceRule, ctx: ActivityContext) -> RuleEvaluation:
    params = rule.parameters or {}
    max_daily = params.get("max_daily_minutes")
    enforce = params.get("enforce", "soft")

    if not max_daily or not ctx.child_id:
        return _eval_result(rule, True, "pass", "No daily limit or no child context")

    today = date.today()
    today_start = datetime(today.year, today.month, today.day, tzinfo=UTC)
    today_end = today_start + timedelta(days=1)

    actual_result = await db.execute(
        select(func.coalesce(func.sum(Attempt.duration_minutes), 0)).where(
            Attempt.child_id == ctx.child_id,
            Attempt.created_at >= today_start,
            Attempt.created_at < today_end,
        )
    )
    current_minutes = actual_result.scalar() or 0
    new_minutes = ctx.estimated_minutes or 0
    projected = current_minutes + new_minutes

    if projected > max_daily:
        action = "block" if enforce == "hard" else "warn"
        return _eval_result(rule, False, action,
            f"Daily limit: {current_minutes}m used + {new_minutes}m planned = {projected}m (limit: {max_daily}m)")

    # Check weekly limit
    max_weekly = params.get("max_weekly_minutes")
    if max_weekly:
        week_start = today - timedelta(days=today.weekday())
        week_start_dt = datetime(week_start.year, week_start.month, week_start.day, tzinfo=UTC)
        weekly_result = await db.execute(
            select(func.coalesce(func.sum(Attempt.duration_minutes), 0)).where(
                Attempt.child_id == ctx.child_id,
                Attempt.created_at >= week_start_dt,
                Attempt.created_at < today_end,
            )
        )
        weekly_minutes = weekly_result.scalar() or 0
        if weekly_minutes + new_minutes > max_weekly:
            action = "block" if enforce == "hard" else "warn"
            return _eval_result(rule, False, action,
                f"Weekly limit: {weekly_minutes}m used + {new_minutes}m = {weekly_minutes + new_minutes}m (limit: {max_weekly}m)")

    return _eval_result(rule, True, "pass", f"Within limits ({current_minutes}m/{max_daily}m daily)")


async def _evaluate_content_filter(db: AsyncSession, rule: GovernanceRule, ctx: ActivityContext) -> RuleEvaluation:
    params = rule.parameters or {}
    topic = (params.get("topic") or "").lower()
    stance = params.get("stance", "exclude")

    if not topic or not ctx.content_topics:
        return _eval_result(rule, True, "pass", "No topic match")

    matched = any(topic in t.lower() for t in ctx.content_topics)
    if not matched:
        return _eval_result(rule, True, "pass", f"No match for '{topic}'")

    action_map = {
        "exclude": "block",
        "present_alternative": "warn",
        "parent_led_only": "require_review",
        "age_appropriate": "warn",
    }
    notes = params.get("notes", "")
    return _eval_result(rule, False, action_map.get(stance, "require_review"),
        f"Content filter: '{topic}' ({stance.replace('_', ' ')}){'. ' + notes if notes else ''}")


async def _evaluate_schedule(db: AsyncSession, rule: GovernanceRule, ctx: ActivityContext) -> RuleEvaluation:
    params = rule.parameters or {}
    enforce = params.get("enforce", "soft")

    if not ctx.scheduled_date:
        return _eval_result(rule, True, "pass", "No scheduled date to check")

    # Check allowed days
    allowed = params.get("allowed_days", [])
    if allowed:
        day_name = ctx.scheduled_date.strftime("%A").lower()
        if day_name not in [d.lower() for d in allowed]:
            action = "block" if enforce == "hard" else "warn"
            return _eval_result(rule, False, action,
                f"Schedule: {day_name.capitalize()} is not in allowed days ({', '.join(allowed)})")

    # Check blackout dates
    blackout = params.get("no_learning_dates", [])
    if ctx.scheduled_date.isoformat() in blackout:
        return _eval_result(rule, False, "block",
            f"Schedule: {ctx.scheduled_date.isoformat()} is a blackout date")

    return _eval_result(rule, True, "pass", "Within schedule")


async def _evaluate_ai_boundary(db: AsyncSession, rule: GovernanceRule, ctx: ActivityContext) -> RuleEvaluation:
    params = rule.parameters or {}

    # Check AI role
    if ctx.ai_role:
        allowed = params.get("allowed_roles", [])
        if allowed and ctx.ai_role not in allowed:
            return _eval_result(rule, False, "block",
                f"AI boundary: role '{ctx.ai_role}' not in allowed roles ({', '.join(allowed)})")

    # Check rate limit
    max_calls = params.get("max_ai_calls_per_day")
    if max_calls:
        today = date.today()
        today_start = datetime(today.year, today.month, today.day, tzinfo=UTC)
        count_result = await db.execute(
            select(func.count(AIRun.id)).where(
                AIRun.household_id == ctx.household_id,
                AIRun.created_at >= today_start,
            )
        )
        current_count = count_result.scalar() or 0
        if current_count >= max_calls:
            return _eval_result(rule, False, "block",
                f"AI boundary: {current_count}/{max_calls} daily AI calls used")

    # Check human review requirement
    if params.get("require_human_review", False):
        return _eval_result(rule, False, "require_review",
            "AI boundary: all AI actions require human review")

    # Check ai_direct_action (if False, AI can't act without review)
    if params.get("ai_direct_action") is False and ctx.ai_role:
        return _eval_result(rule, False, "require_review",
            "AI boundary: AI cannot act without parent review")

    return _eval_result(rule, True, "pass", "Within AI boundaries")


# ══════════════════════════════════════════════════
# Main evaluator
# ══════════════════════════════════════════════════


_EVALUATORS = {
    RuleType.approval_required: _evaluate_approval,
    RuleType.pace_limit: _evaluate_pace_limit,
    RuleType.content_filter: _evaluate_content_filter,
    RuleType.schedule_constraint: _evaluate_schedule,
    RuleType.ai_boundary: _evaluate_ai_boundary,
}


async def evaluate_activity(
    db: AsyncSession,
    household_id: uuid.UUID | None = None,
    difficulty: int | None = None,
    activity_type: str | None = None,
    node_id: uuid.UUID | None = None,
    subject_id: uuid.UUID | None = None,
    # New: accept ActivityContext directly
    context: ActivityContext | None = None,
    **kwargs,
) -> GovernanceDecision:
    """Evaluate an activity against ALL active governance rules.

    Accepts either individual parameters (backward compatible) or an
    ActivityContext object. Returns a GovernanceDecision with full
    evaluation details for every rule checked.
    """
    # Build context from individual args if not provided
    if context is None:
        context = ActivityContext(
            household_id=household_id or kwargs.get("household_id", uuid.UUID(int=0)),
            child_id=kwargs.get("child_id"),
            activity_type=activity_type,
            difficulty=difficulty,
            subject_id=subject_id,
            node_id=node_id,
            scheduled_date=kwargs.get("scheduled_date"),
            estimated_minutes=kwargs.get("estimated_minutes"),
            content_topics=kwargs.get("content_topics"),
            ai_role=kwargs.get("ai_role"),
        )

    today = date.today()

    # Get ALL active rules for household
    result = await db.execute(
        select(GovernanceRule).where(
            GovernanceRule.household_id == context.household_id,
            GovernanceRule.is_active.is_(True),
        ).order_by(GovernanceRule.priority.asc())
    )
    all_rules = result.scalars().all()

    # Filter by effective date window
    active_rules = []
    for r in all_rules:
        if r.effective_from and r.effective_from > today:
            continue
        if r.effective_until and r.effective_until < today:
            continue
        active_rules.append(r)

    if not active_rules:
        return GovernanceDecision(
            action="auto_approve",
            reason="No governance rules defined",
        )

    # Evaluate every rule
    evaluations: list[RuleEvaluation] = []
    for rule in active_rules:
        evaluator = _EVALUATORS.get(rule.rule_type)
        if evaluator:
            ev = await evaluator(db, rule, context)
            evaluations.append(ev)

    blocking = [e for e in evaluations if not e.passed]
    passed = [e for e in evaluations if e.passed]
    constitutional_violations = [e for e in blocking if e.tier == "constitutional"]

    # Constitutional violations always block
    if constitutional_violations:
        return GovernanceDecision(
            action="block",
            reason=f"Constitutional rule violated: {constitutional_violations[0].reason}",
            evaluations=evaluations,
            blocking_rules=blocking,
            passed_rules=passed,
            constitutional_violations=constitutional_violations,
        )

    # Any "block" action blocks
    blocks = [e for e in blocking if e.action == "block"]
    if blocks:
        return GovernanceDecision(
            action="block",
            reason=blocks[0].reason,
            evaluations=evaluations,
            blocking_rules=blocking,
            passed_rules=passed,
            constitutional_violations=[],
        )

    # Any "require_review" sends to queue
    reviews = [e for e in blocking if e.action == "require_review"]
    if reviews:
        return GovernanceDecision(
            action="require_review",
            reason=reviews[0].reason,
            evaluations=evaluations,
            blocking_rules=blocking,
            passed_rules=passed,
            constitutional_violations=[],
        )

    # Warnings pass through but are noted
    warns = [e for e in blocking if e.action == "warn"]
    if warns:
        return GovernanceDecision(
            action="auto_approve",
            reason="Approved with warnings: " + "; ".join(w.reason for w in warns),
            evaluations=evaluations,
            blocking_rules=warns,
            passed_rules=passed,
            constitutional_violations=[],
        )

    # All clear
    return GovernanceDecision(
        action="auto_approve",
        reason="All rules passed",
        evaluations=evaluations,
        blocking_rules=[],
        passed_rules=passed,
        constitutional_violations=[],
    )


# ══════════════════════════════════════════════════
# Default rules + logging
# ══════════════════════════════════════════════════


async def create_default_rules(
    db: AsyncSession,
    household_id: uuid.UUID,
    created_by: uuid.UUID,
) -> list[GovernanceRule]:
    """Create default governance rules for a new household."""
    defaults = [
        GovernanceRule(
            household_id=household_id,
            created_by=created_by,
            rule_type=RuleType.approval_required,
            scope=RuleScope.household,
            name="Auto-approve easy activities",
            description="Activities with difficulty < 3 are auto-approved",
            parameters={"max_difficulty": 3, "action": "auto_approve"},
            priority=10,
        ),
        GovernanceRule(
            household_id=household_id,
            created_by=created_by,
            rule_type=RuleType.approval_required,
            scope=RuleScope.household,
            name="Review difficult activities",
            description="Activities with difficulty >= 3 require parent review",
            parameters={"min_difficulty": 3, "action": "require_review"},
            priority=20,
        ),
        GovernanceRule(
            household_id=household_id,
            created_by=created_by,
            rule_type=RuleType.pace_limit,
            scope=RuleScope.household,
            name="Daily time limit",
            description="Maximum daily learning time",
            parameters={"max_daily_minutes": 240, "enforce": "soft"},
            priority=5,
        ),
        GovernanceRule(
            household_id=household_id,
            created_by=created_by,
            rule_type=RuleType.ai_boundary,
            tier=RuleTier.constitutional,
            scope=RuleScope.household,
            name="AI oversight guarantee",
            description="All AI-generated content and recommendations are logged with full input/output for parent inspection. AI cannot modify child state without governance approval.",
            parameters={"ai_transparency": "full", "ai_direct_action": False, "require_human_review": False},
            priority=1,
        ),
    ]
    for rule in defaults:
        db.add(rule)
    await db.flush()
    return defaults


async def log_governance_event(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID | None,
    action: GovernanceAction,
    target_type: str,
    target_id: uuid.UUID,
    reason: str | None = None,
    metadata: dict | None = None,
) -> GovernanceEvent:
    """Log an immutable governance event."""
    event = GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        metadata_=metadata or {},
    )
    db.add(event)
    await db.flush()

    # Record governance pattern for intelligence layer
    try:
        from app.services.intelligence import record_governance_pattern
        meta = metadata or {}
        await record_governance_pattern(
            db, household_id,
            action=action.value if hasattr(action, "value") else str(action),
            activity_type=meta.get("activity_type"),
            difficulty=meta.get("difficulty"),
        )
    except Exception:
        pass  # Intelligence recording is non-blocking

    return event
