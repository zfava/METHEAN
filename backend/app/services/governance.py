"""Governance Rules Engine.

Evaluates recommendations against household rules to determine action:
auto_approve, require_review, or block.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import GovernanceAction, RuleScope, RuleTier, RuleType
from app.models.governance import GovernanceEvent, GovernanceRule


class GovernanceDecision:
    """Result of evaluating governance rules against a recommendation."""

    def __init__(
        self,
        action: str,  # "auto_approve", "require_review", "block"
        rule_id: uuid.UUID | None = None,
        rule_name: str | None = None,
        reason: str | None = None,
    ):
        self.action = action
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.reason = reason


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
            parameters={"max_daily_minutes": 240},
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
            parameters={"ai_transparency": "full", "ai_direct_action": False},
            priority=1,
        ),
    ]
    for rule in defaults:
        db.add(rule)
    await db.flush()
    return defaults


async def evaluate_activity(
    db: AsyncSession,
    household_id: uuid.UUID,
    difficulty: int | None = None,
    activity_type: str | None = None,
    node_id: uuid.UUID | None = None,
    subject_id: uuid.UUID | None = None,
) -> GovernanceDecision:
    """Evaluate an activity against governance rules.

    Returns the highest-priority matching decision.
    """
    # Get all active rules for household, ordered by priority
    result = await db.execute(
        select(GovernanceRule).where(
            GovernanceRule.household_id == household_id,
            GovernanceRule.is_active == True,  # noqa: E712
            GovernanceRule.rule_type == RuleType.approval_required,
        ).order_by(GovernanceRule.priority.asc())
    )
    rules = result.scalars().all()

    if not rules:
        # No rules = auto-approve
        return GovernanceDecision(action="auto_approve", reason="No governance rules defined")

    for rule in rules:
        params = rule.parameters or {}
        action = params.get("action", "require_review")

        # Check scope match
        if rule.scope == RuleScope.subject and rule.scope_id and subject_id:
            if rule.scope_id != subject_id:
                continue
        elif rule.scope == RuleScope.map and rule.scope_id and node_id:
            pass  # Map-scoped rules apply to all nodes in the map

        # Check difficulty conditions
        if difficulty is not None:
            max_diff = params.get("max_difficulty")
            min_diff = params.get("min_difficulty")

            if max_diff is not None and difficulty < max_diff:
                return GovernanceDecision(
                    action=action,
                    rule_id=rule.id,
                    rule_name=rule.name,
                    reason=f"Difficulty {difficulty} < threshold {max_diff}",
                )
            if min_diff is not None and difficulty >= min_diff:
                return GovernanceDecision(
                    action=action,
                    rule_id=rule.id,
                    rule_name=rule.name,
                    reason=f"Difficulty {difficulty} >= threshold {min_diff}",
                )

    # Default: require review
    return GovernanceDecision(action="require_review", reason="Default policy")


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
    return event
