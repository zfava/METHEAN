"""Tests for the full governance rule evaluation engine.

Covers all 5 rule types, constitutional violations, aggregate decisions,
and the evaluation hierarchy (constitutional > block > review > warn > pass).
"""

from datetime import UTC, date, datetime, timedelta

import pytest

from app.models.enums import (
    ActivityType,
    AttemptStatus,
    PlanStatus,
    RuleScope,
    RuleTier,
    RuleType,
)
from app.models.governance import Activity, Attempt, GovernanceRule, Plan, PlanWeek
from app.models.operational import AIRun
from app.services.governance import (
    ActivityContext,
    GovernanceDecision,
    evaluate_activity,
)


class TestPaceLimit:
    @pytest.mark.asyncio
    async def test_blocks_when_exceeded_hard(self, db_session, household, child, user):
        """Hard pace_limit blocks when daily minutes exceeded."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.pace_limit,
                scope=RuleScope.household,
                name="60m limit",
                parameters={"max_daily_minutes": 60, "enforce": "hard"},
            )
        )
        # Log 50m of attempts today
        plan = Plan(
            household_id=household.id, child_id=child.id, created_by=user.id, name="T", status=PlanStatus.active
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id, household_id=household.id, week_number=1, start_date=date.today(), end_date=date.today()
        )
        db_session.add(week)
        await db_session.flush()
        act = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="T",
            governance_approved=True,
        )
        db_session.add(act)
        await db_session.flush()
        db_session.add(
            Attempt(
                activity_id=act.id,
                household_id=household.id,
                child_id=child.id,
                status=AttemptStatus.completed,
                duration_minutes=50,
                created_at=datetime.now(UTC),
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, child_id=child.id, estimated_minutes=20)
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert "70m" in decision.reason  # 50 + 20 = 70

    @pytest.mark.asyncio
    async def test_warns_when_exceeded_soft(self, db_session, household, child, user):
        """Soft pace_limit warns instead of blocking."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.pace_limit,
                scope=RuleScope.household,
                name="60m soft",
                parameters={"max_daily_minutes": 60, "enforce": "soft"},
            )
        )
        plan = Plan(
            household_id=household.id, child_id=child.id, created_by=user.id, name="T", status=PlanStatus.active
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id, household_id=household.id, week_number=1, start_date=date.today(), end_date=date.today()
        )
        db_session.add(week)
        await db_session.flush()
        act = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="T",
            governance_approved=True,
        )
        db_session.add(act)
        await db_session.flush()
        db_session.add(
            Attempt(
                activity_id=act.id,
                household_id=household.id,
                child_id=child.id,
                status=AttemptStatus.completed,
                duration_minutes=50,
                created_at=datetime.now(UTC),
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, child_id=child.id, estimated_minutes=20)
        decision = await evaluate_activity(db_session, context=ctx)
        # Soft enforced = warn, which is auto_approve with warning
        assert decision.action == "auto_approve"
        assert "warnings" in decision.reason.lower() or "warn" in decision.blocking_rules[0].action


class TestContentFilter:
    @pytest.mark.asyncio
    async def test_excludes_matching_topic(self, db_session, household, user):
        """Content filter with 'exclude' blocks matching topic."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.content_filter,
                scope=RuleScope.household,
                name="No evolution",
                parameters={"topic": "evolution", "stance": "exclude"},
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, content_topics=["evolutionary biology"])
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert "evolution" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_passes_non_matching_topic(self, db_session, household, user):
        """Content filter passes when topic doesn't match."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.content_filter,
                scope=RuleScope.household,
                name="No evolution",
                parameters={"topic": "evolution", "stance": "exclude"},
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, content_topics=["mathematics"])
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "auto_approve"


class TestScheduleConstraint:
    @pytest.mark.asyncio
    async def test_blocks_weekend(self, db_session, household, user):
        """Schedule constraint blocks activities on non-allowed days."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.schedule_constraint,
                scope=RuleScope.household,
                name="Weekdays only",
                parameters={
                    "allowed_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                    "enforce": "hard",
                },
            )
        )
        await db_session.flush()

        # Find next Saturday
        today = date.today()
        days_until_sat = (5 - today.weekday()) % 7
        if days_until_sat == 0:
            days_until_sat = 7
        saturday = today + timedelta(days=days_until_sat)

        ctx = ActivityContext(household_id=household.id, scheduled_date=saturday)
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert "not in allowed days" in decision.reason.lower()

    @pytest.mark.asyncio
    async def test_blackout_date(self, db_session, household, user):
        """Schedule constraint blocks blackout dates."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.schedule_constraint,
                scope=RuleScope.household,
                name="Holidays",
                parameters={
                    "no_learning_dates": ["2026-12-25"],
                    "enforce": "hard",
                },
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, scheduled_date=date(2026, 12, 25))
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert "blackout" in decision.reason.lower()


class TestAIBoundary:
    @pytest.mark.asyncio
    async def test_blocks_disallowed_role(self, db_session, household, user):
        """AI boundary blocks roles not in allowed list."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.ai_boundary,
                scope=RuleScope.household,
                name="Limited roles",
                parameters={"allowed_roles": ["planner", "tutor"]},
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, ai_role="evaluator")
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert "evaluator" in decision.reason

    @pytest.mark.asyncio
    async def test_rate_limit(self, db_session, household, user):
        """AI boundary blocks when daily call limit exceeded."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.ai_boundary,
                scope=RuleScope.household,
                name="Rate limit",
                parameters={"max_ai_calls_per_day": 5},
            )
        )
        # Create 5 AI runs today
        for _ in range(5):
            db_session.add(
                AIRun(
                    household_id=household.id,
                    triggered_by=user.id,
                    run_type="planner",
                    status="completed",
                    input_data={},
                    output_data={},
                    created_at=datetime.now(UTC),
                )
            )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, ai_role="planner")
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert "5/5" in decision.reason


class TestConstitutionalViolation:
    @pytest.mark.asyncio
    async def test_always_blocks(self, db_session, household, user):
        """Constitutional violations always block regardless of other rules."""
        # Add a passing policy rule
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.approval_required,
                scope=RuleScope.household,
                name="Auto approve",
                parameters={"max_difficulty": 10, "action": "auto_approve"},
            )
        )
        # Add a constitutional ai_boundary that blocks
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.ai_boundary,
                tier=RuleTier.constitutional,
                scope=RuleScope.household,
                name="Constitutional AI limit",
                parameters={"allowed_roles": ["planner"]},
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, difficulty=1, ai_role="evaluator")
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"
        assert len(decision.constitutional_violations) > 0
        assert "Constitutional rule violated" in decision.reason


class TestAggregateDecision:
    @pytest.mark.asyncio
    async def test_hierarchy_block_beats_review(self, db_session, household, user):
        """Block overrides require_review in aggregate."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.approval_required,
                scope=RuleScope.household,
                name="Review",
                parameters={"min_difficulty": 1, "action": "require_review"},
            )
        )
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.content_filter,
                scope=RuleScope.household,
                name="Block topic",
                parameters={"topic": "violence", "stance": "exclude"},
            )
        )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, difficulty=5, content_topics=["violence"])
        decision = await evaluate_activity(db_session, context=ctx)
        assert decision.action == "block"

    @pytest.mark.asyncio
    async def test_all_rules_evaluated(self, db_session, household, user):
        """Create one of each type. Verify all 5 appear in evaluations."""
        for rt in [
            RuleType.approval_required,
            RuleType.pace_limit,
            RuleType.content_filter,
            RuleType.schedule_constraint,
            RuleType.ai_boundary,
        ]:
            params = (
                {"max_difficulty": 5, "action": "auto_approve"}
                if rt == RuleType.approval_required
                else {"max_daily_minutes": 999}
                if rt == RuleType.pace_limit
                else {"topic": "nothing_matches", "stance": "exclude"}
                if rt == RuleType.content_filter
                else {"allowed_days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
                if rt == RuleType.schedule_constraint
                else {"ai_transparency": "full"}
            )
            db_session.add(
                GovernanceRule(
                    household_id=household.id,
                    created_by=user.id,
                    rule_type=rt,
                    scope=RuleScope.household,
                    name=f"Test {rt.value}",
                    parameters=params,
                )
            )
        await db_session.flush()

        ctx = ActivityContext(household_id=household.id, difficulty=2, scheduled_date=date.today())
        decision = await evaluate_activity(db_session, context=ctx)

        eval_types = {e.rule_type for e in decision.evaluations}
        assert "approval_required" in eval_types
        assert "pace_limit" in eval_types
        assert "content_filter" in eval_types
        assert "schedule_constraint" in eval_types
        assert "ai_boundary" in eval_types
        assert len(decision.evaluations) == 5


class TestBackwardCompat:
    @pytest.mark.asyncio
    async def test_old_style_call_works(self, db_session, household, user):
        """Calling with individual args (old style) still works."""
        db_session.add(
            GovernanceRule(
                household_id=household.id,
                created_by=user.id,
                rule_type=RuleType.approval_required,
                scope=RuleScope.household,
                name="Review hard",
                parameters={"min_difficulty": 3, "action": "require_review"},
            )
        )
        await db_session.flush()

        decision = await evaluate_activity(db_session, household.id, difficulty=5)
        assert decision.action in ("require_review", "block", "auto_approve")
        assert isinstance(decision, GovernanceDecision)
