"""Governance Rules Engine.

Evaluates recommendations against all active household rules.
Enforces: approval_required, pace_limit, content_filter,
schedule_constraint, and ai_boundary rules.
"""

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta

import structlog
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import GovernanceAction, RuleScope, RuleTier, RuleType
from app.models.governance import Attempt, GovernanceEvent, GovernanceRule
from app.models.identity import Household
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
    # When True, the auto_approve came from the self_governed fast path.
    # Callers use this to tag the GovernanceEvent metadata with
    # source="self_governed_autonomy" so the audit trail is distinguishable
    # from parent approvals.
    self_governed_auto_approve: bool = False
    autonomy_level: str | None = None

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
        rule_id=rule.id,
        rule_name=rule.name,
        rule_type=rule.rule_type.value if hasattr(rule.rule_type, "value") else str(rule.rule_type),
        tier=tier,
        passed=passed,
        action=action,
        reason=reason,
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
            return _eval_result(
                rule, action == "auto_approve", action, f"Difficulty {ctx.difficulty} < threshold {max_diff}"
            )
        if min_diff is not None and ctx.difficulty >= min_diff:
            return _eval_result(
                rule, action == "auto_approve", action, f"Difficulty {ctx.difficulty} >= threshold {min_diff}"
            )

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
        return _eval_result(
            rule,
            False,
            action,
            f"Daily limit: {current_minutes}m used + {new_minutes}m planned = {projected}m (limit: {max_daily}m)",
        )

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
            return _eval_result(
                rule,
                False,
                action,
                f"Weekly limit: {weekly_minutes}m used + {new_minutes}m = {weekly_minutes + new_minutes}m (limit: {max_weekly}m)",
            )

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
    return _eval_result(
        rule,
        False,
        action_map.get(stance, "require_review"),
        f"Content filter: '{topic}' ({stance.replace('_', ' ')}){'. ' + notes if notes else ''}",
    )


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
            return _eval_result(
                rule, False, action, f"Schedule: {day_name.capitalize()} is not in allowed days ({', '.join(allowed)})"
            )

    # Check blackout dates
    blackout = params.get("no_learning_dates", [])
    if ctx.scheduled_date.isoformat() in blackout:
        return _eval_result(rule, False, "block", f"Schedule: {ctx.scheduled_date.isoformat()} is a blackout date")

    return _eval_result(rule, True, "pass", "Within schedule")


async def _evaluate_ai_boundary(db: AsyncSession, rule: GovernanceRule, ctx: ActivityContext) -> RuleEvaluation:
    params = rule.parameters or {}

    # Check AI role
    if ctx.ai_role:
        allowed = params.get("allowed_roles", [])
        if allowed and ctx.ai_role not in allowed:
            return _eval_result(
                rule, False, "block", f"AI boundary: role '{ctx.ai_role}' not in allowed roles ({', '.join(allowed)})"
            )

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
            return _eval_result(rule, False, "block", f"AI boundary: {current_count}/{max_calls} daily AI calls used")

    # Check human review requirement
    if params.get("require_human_review", False):
        return _eval_result(rule, False, "require_review", "AI boundary: all AI actions require human review")

    # Check ai_direct_action (if False, AI can't act without review)
    if params.get("ai_direct_action") is False and ctx.ai_role:
        return _eval_result(rule, False, "require_review", "AI boundary: AI cannot act without parent review")

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

    # Load the household so we can honor governance_mode and the
    # ai_autonomy_level declared in its philosophical_profile.
    household_row = await db.get(Household, context.household_id) if context.household_id else None
    governance_mode = (
        getattr(household_row, "governance_mode", "parent_governed") if household_row is not None else "parent_governed"
    )
    autonomy = "preview_all"
    if household_row is not None:
        autonomy = (household_row.philosophical_profile or {}).get("ai_autonomy_level", "preview_all")

    # Self-governed fast path
    if governance_mode == "self_governed":
        if autonomy == "full_autonomy":
            # Auto-approve outright. No rule evaluation, no queue.
            return GovernanceDecision(
                action="auto_approve",
                reason="Self-governed, full autonomy",
                self_governed_auto_approve=True,
                autonomy_level=autonomy,
            )
        # trust_within_rules falls through to normal rule evaluation.
        # approve_difficult and preview_all also fall through unchanged.

    # Get ALL active rules for household
    result = await db.execute(
        select(GovernanceRule)
        .where(
            GovernanceRule.household_id == context.household_id,
            GovernanceRule.is_active.is_(True),
        )
        .order_by(GovernanceRule.priority.asc())
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

    self_governed_trust = governance_mode == "self_governed" and autonomy == "trust_within_rules"

    if not active_rules:
        return GovernanceDecision(
            action="auto_approve",
            reason="Self-governed, trust within rules" if self_governed_trust else "No governance rules defined",
            self_governed_auto_approve=self_governed_trust,
            autonomy_level=autonomy if self_governed_trust else None,
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
        try:
            from app.core.metrics import governance_decisions

            governance_decisions.labels(action="require_review").inc()
        except Exception:
            pass
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
    try:
        from app.core.metrics import governance_decisions

        governance_decisions.labels(action="auto_approve").inc()
    except Exception:
        pass
    return GovernanceDecision(
        action="auto_approve",
        reason=("Self-governed, trust within rules" if self_governed_trust else "All rules passed"),
        evaluations=evaluations,
        blocking_rules=[],
        passed_rules=passed,
        constitutional_violations=[],
        self_governed_auto_approve=self_governed_trust,
        autonomy_level=autonomy if self_governed_trust else None,
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


# ══════════════════════════════════════════════════
# Hash chain (append-only audit, migration 052)
# ══════════════════════════════════════════════════

logger = structlog.get_logger()

GENESIS_SENTINEL = "GENESIS"

# The exact GovernanceEvent columns covered by the hash, in canonical
# payload form. The surrogate id is excluded: it is generated at flush
# time and carries no audit meaning; everything a parent audits is here.
GOVERNANCE_HASH_FIELDS = (
    "household_id",
    "user_id",
    "action",
    "target_type",
    "target_id",
    "reason",
    "metadata",
    "created_at",
)


def build_governance_hash_payload(
    *,
    household_id: uuid.UUID | str,
    user_id: uuid.UUID | str | None,
    action: GovernanceAction | str,
    target_type: str,
    target_id: uuid.UUID | str,
    reason: str | None,
    metadata: dict | None,
    created_at: datetime | str,
) -> dict:
    """Build the canonical dict hashed for a GovernanceEvent.

    Every value is normalized to a JSON-stable form (str for UUIDs,
    enum value for the action, isoformat for the timestamp) so the
    same row always serializes to the same bytes, whether the inputs
    come from the ORM, from raw migration rows, or from API output.
    """
    return {
        "household_id": str(household_id),
        "user_id": str(user_id) if user_id is not None else None,
        "action": action.value if isinstance(action, GovernanceAction) else str(action),
        "target_type": target_type,
        "target_id": str(target_id),
        "reason": reason,
        "metadata": metadata or {},
        "created_at": created_at.isoformat() if isinstance(created_at, datetime) else str(created_at),
    }


def compute_event_hash(payload: dict, prev_hash: str | None) -> str:
    """Compute the SHA-256 chain hash for one event.

    Serialization is canonical: sorted keys, no whitespace, default=str
    for any stray non-JSON values. The previous event's hash (or the
    GENESIS sentinel for the first event in a household) is prepended
    so each hash commits to the entire history before it.
    """
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(((prev_hash or GENESIS_SENTINEL) + serialized).encode("utf-8")).hexdigest()


def verify_chain(events: list[dict]) -> dict:
    """Verify a household's hash chain. Pure function, no I/O.

    Each dict must carry the canonical payload fields plus the stored
    event_hash and prev_event_hash, already ordered by (created_at, id).
    Fails closed: a missing or null stored hash is a break, not a skip.
    Returns {"valid": bool, "checked": int, "first_break_index": int | None}.
    """
    prev_hash: str | None = None
    for index, event in enumerate(events):
        if event.get("prev_event_hash") != prev_hash:
            return {"valid": False, "checked": index + 1, "first_break_index": index}
        payload = {f: event.get(f) for f in GOVERNANCE_HASH_FIELDS}
        expected = compute_event_hash(payload, prev_hash)
        if event.get("event_hash") != expected:
            return {"valid": False, "checked": index + 1, "first_break_index": index}
        prev_hash = expected
    return {"valid": True, "checked": len(events), "first_break_index": None}


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
    """Log an immutable governance event, chained to the household's last event."""
    # Serialize concurrent appends per household so two transactions can
    # never both read the same head and fork the chain. The advisory
    # lock is transaction-scoped and released automatically on
    # commit/rollback. This is the only raw SQL outside migrations.
    if db.bind is not None and db.bind.dialect.name == "postgresql":
        await db.execute(
            text("SELECT pg_advisory_xact_lock(hashtext(:hid))"),
            {"hid": str(household_id)},
        )

    head_result = await db.execute(
        select(GovernanceEvent.event_hash)
        .where(GovernanceEvent.household_id == household_id)
        .order_by(GovernanceEvent.created_at.desc(), GovernanceEvent.id.desc())
        .limit(1)
    )
    prev_hash = head_result.scalar_one_or_none()

    # created_at is set client-side (not left to the server default)
    # because the hash must commit to it before the row is inserted:
    # the append-only triggers forbid writing the hash in a second pass.
    created_at = datetime.now(UTC)
    event_metadata = metadata or {}
    payload = build_governance_hash_payload(
        household_id=household_id,
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        metadata=event_metadata,
        created_at=created_at,
    )
    event_hash = compute_event_hash(payload, prev_hash)

    event = GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        metadata_=event_metadata,
        created_at=created_at,
        event_hash=event_hash,
        prev_event_hash=prev_hash,
    )
    db.add(event)
    await db.flush()
    logger.debug(
        "governance_event_chained",
        household_id=str(household_id),
        event_id=str(event.id),
        event_hash=event_hash,
        prev_event_hash=prev_hash,
    )

    # Record governance pattern for intelligence layer
    try:
        from app.services.intelligence import record_governance_pattern

        meta = metadata or {}
        await record_governance_pattern(
            db,
            household_id,
            action=action.value if hasattr(action, "value") else str(action),
            activity_type=meta.get("activity_type"),
            difficulty=meta.get("difficulty"),
        )
    except Exception:
        pass  # Intelligence recording is non-blocking

    return event


# ══════════════════════════════════════════════════
# AI role autonomy policy (migration 056)
# ══════════════════════════════════════════════════

AI_AUTONOMY_OFF = "off"
AI_AUTONOMY_STANDARD = "standard"
AI_AUTONOMY_AUTONOMOUS = "autonomous"

# Which autonomy values each role may take. Widening a role's allowed
# set is a deliberate product decision with legal and parental weight,
# not a config change: it means defining the role's named write
# actions, their governance events, and their revocation story first.
# Only the tutor is autonomy-capable today (the tutor profile system
# consumes the grant).
ALLOWED_AUTONOMY: dict[str, tuple[str, ...]] = {
    "planner": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
    "tutor": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD, AI_AUTONOMY_AUTONOMOUS),
    "evaluator": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
    "advisor": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
    "cartographer": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
    "education_architect": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
    "content_architect": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
    "curriculum_mapper": (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD),
}

# One line per role, written for a skeptical parent.
AI_ROLE_DESCRIPTIONS: dict[str, str] = {
    "planner": "Drafts weekly activity plans for your approval. It proposes; you approve every plan before your child sees it.",
    "tutor": "Talks your child through their work with guiding questions. It coaches; it never just hands over answers.",
    "evaluator": "Reads completed work and suggests a mastery judgment. Your approval settings decide what actually counts.",
    "advisor": "Writes you periodic progress summaries and suggestions. It reports to you, never to your child.",
    "cartographer": "Suggests how skills connect and what could come next on the learning map. Nothing moves without your approval.",
    "education_architect": "Drafts long-range education plans and annual curricula for your review. Your curriculum itself runs natively, with or without AI.",
    "content_architect": "Drafts lesson content and practice material inside the curriculum you already approved.",
    "curriculum_mapper": "Reads curriculum materials you provide and maps them into METHEAN for your review.",
}

# One line per autonomy level, same audience.
AI_AUTONOMY_DESCRIPTIONS: dict[str, str] = {
    AI_AUTONOMY_OFF: "This role makes no AI calls at all. The features it powers show a friendly unavailable state instead.",
    AI_AUTONOMY_STANDARD: "The AI advises. Anything it wants to change about your child's record waits for your approval. This is the default.",
    AI_AUTONOMY_AUTONOMOUS: "A standing grant: this role may apply its specific, named actions without per-item approval. Every action is recorded against this grant in the sealed family record, and one tap revokes it.",
}

# Plain-language scope text recorded inside every grant event. The
# grant event's hash is the standing reference that future autonomous
# writes cite.
AI_AUTONOMY_GRANT_SCOPE: dict[str, str] = {
    "tutor": (
        "Allows the AI tutor to apply its specific, named tutor adjustments "
        "for your child without per-item approval. Every action under this "
        "grant is recorded in the sealed family record, cites this grant, "
        "and the grant is revocable in one tap."
    ),
}

_AI_POLICY_CACHE_TTL_SECONDS = 30


def _ai_policy_cache_key(household_id: uuid.UUID, role: str) -> str:
    return f"ai_policy:{household_id}:{role}"


async def get_ai_role_policy(db: AsyncSession, household_id: uuid.UUID, role: str) -> str:
    """Effective autonomy for one role. Absent row means standard.

    Cached briefly (mirroring the governance queue cache pattern) so
    the gateway does not add a query to every AI call; writes
    invalidate the key.
    """
    from app.core.cache import cache_get, cache_set

    key = _ai_policy_cache_key(household_id, role)
    cached = await cache_get(key)
    if cached in (AI_AUTONOMY_OFF, AI_AUTONOMY_STANDARD, AI_AUTONOMY_AUTONOMOUS):
        return cached

    from app.models.governance import HouseholdAIRoleSetting

    result = await db.execute(
        select(HouseholdAIRoleSetting.autonomy).where(
            HouseholdAIRoleSetting.household_id == household_id,
            HouseholdAIRoleSetting.role == role,
        )
    )
    autonomy = result.scalar_one_or_none() or AI_AUTONOMY_STANDARD
    await cache_set(key, autonomy, ttl_seconds=_AI_POLICY_CACHE_TTL_SECONDS)
    return autonomy


async def get_all_ai_role_settings(db: AsyncSession, household_id: uuid.UUID) -> list[dict]:
    """All eight roles with effective autonomy and change metadata."""
    from app.models.governance import HouseholdAIRoleSetting

    result = await db.execute(select(HouseholdAIRoleSetting).where(HouseholdAIRoleSetting.household_id == household_id))
    rows = {row.role: row for row in result.scalars().all()}

    settings_list = []
    for role, allowed in ALLOWED_AUTONOMY.items():
        row = rows.get(role)
        settings_list.append(
            {
                "role": role,
                "autonomy": row.autonomy if row else AI_AUTONOMY_STANDARD,
                "allowed": list(allowed),
                "description": AI_ROLE_DESCRIPTIONS[role],
                "updated_at": row.updated_at.isoformat() if row and row.updated_at else None,
                "updated_by": str(row.updated_by) if row and row.updated_by else None,
            }
        )
    return settings_list


async def set_ai_role_policy(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID,
    role: str,
    autonomy: str,
) -> dict:
    """Upsert one role's autonomy policy and log the governance events.

    Raises ValueError for unknown roles or disallowed autonomy values
    (the endpoint surfaces these as 422). Every change logs
    ai_role_policy_changed; transitions into and out of autonomous
    additionally log ai_autonomy_granted / ai_autonomy_revoked because
    a standing grant carries legal and parental weight beyond a normal
    setting change.
    """
    allowed = ALLOWED_AUTONOMY.get(role)
    if allowed is None:
        raise ValueError(f"Unknown AI role '{role}'")
    if autonomy not in allowed:
        raise ValueError(f"Autonomy '{autonomy}' is not available for the {role} role. Allowed: {', '.join(allowed)}")

    from app.core.cache import cache_delete
    from app.models.governance import HouseholdAIRoleSetting

    result = await db.execute(
        select(HouseholdAIRoleSetting).where(
            HouseholdAIRoleSetting.household_id == household_id,
            HouseholdAIRoleSetting.role == role,
        )
    )
    row = result.scalar_one_or_none()
    old_autonomy = row.autonomy if row else AI_AUTONOMY_STANDARD

    if row is None:
        row = HouseholdAIRoleSetting(
            household_id=household_id,
            role=role,
            autonomy=autonomy,
            updated_by=user_id,
        )
        db.add(row)
    else:
        row.autonomy = autonomy
        row.updated_by = user_id
    await db.flush()
    await cache_delete(_ai_policy_cache_key(household_id, role))

    if autonomy != old_autonomy:
        await log_governance_event(
            db,
            household_id,
            user_id,
            GovernanceAction.modify,
            "ai_role_policy_changed",
            row.id,
            reason=f"AI policy for {role}: {old_autonomy} to {autonomy}",
            metadata={"role": role, "old": old_autonomy, "new": autonomy},
        )
        if autonomy == AI_AUTONOMY_AUTONOMOUS:
            await log_governance_event(
                db,
                household_id,
                user_id,
                GovernanceAction.approve,
                "ai_autonomy_granted",
                row.id,
                reason=AI_AUTONOMY_GRANT_SCOPE.get(role, f"Standing autonomy grant for the {role} role"),
                metadata={"role": role, "granted_by": str(user_id), "scope": AI_AUTONOMY_GRANT_SCOPE.get(role)},
            )
        elif old_autonomy == AI_AUTONOMY_AUTONOMOUS:
            await log_governance_event(
                db,
                household_id,
                user_id,
                GovernanceAction.modify,
                "ai_autonomy_revoked",
                row.id,
                reason=f"Standing autonomy grant for the {role} role revoked",
                metadata={"role": role, "revoked_by": str(user_id)},
            )
        logger.info(
            "ai_role_policy_changed",
            household_id=str(household_id),
            role=role,
            old=old_autonomy,
            new=autonomy,
            user_id=str(user_id),
        )

    return {
        "role": role,
        "autonomy": autonomy,
        "old_autonomy": old_autonomy,
    }


async def get_active_autonomy_grant(db: AsyncSession, household_id: uuid.UUID, role: str) -> str | None:
    """The hash of the standing grant event currently in force, or None.

    Future autonomous writes cite this hash so every action under a
    grant is traceable to the parent decision that authorized it.
    """
    result = await db.execute(
        select(GovernanceEvent)
        .where(
            GovernanceEvent.household_id == household_id,
            GovernanceEvent.target_type.in_(["ai_autonomy_granted", "ai_autonomy_revoked"]),
            GovernanceEvent.metadata_["role"].astext == role,
        )
        .order_by(GovernanceEvent.created_at.desc(), GovernanceEvent.id.desc())
        .limit(1)
    )
    latest = result.scalar_one_or_none()
    if latest is None or latest.target_type != "ai_autonomy_granted":
        return None
    return latest.event_hash
