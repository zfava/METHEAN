"""Tests for temporal governance triggers.

Covers:
- Age threshold activates rule when child reaches specified age
- Mastery milestone activates rule when child completes map
- Effective date window: future rules not enforced today
- Triggers fire only once (idempotent)
"""

import uuid
from datetime import date, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import (
    GovernanceAction,
    MasteryLevel,
    NodeType,
    RuleScope,
    RuleTier,
    RuleType,
)
from app.models.governance import GovernanceEvent, GovernanceRule
from app.models.identity import Child
from app.models.state import ChildNodeState
from app.services.governance import evaluate_activity


class TestAgeThresholdTrigger:
    @pytest.mark.asyncio
    async def test_age_triggers_rule_activation(self, db_session, household, user):
        """Rule with age_threshold trigger fires when child reaches the age."""
        from app.tasks.temporal_rules import evaluate_temporal_triggers

        # Child who turned 8 today
        child = Child(
            household_id=household.id,
            first_name="AgeTest",
            date_of_birth=date.today() - timedelta(days=8 * 366),  # Safely past 8th birthday
        )
        db_session.add(child)
        await db_session.flush()

        # Rule starts inactive, trigger should activate it
        rule = GovernanceRule(
            household_id=household.id,
            created_by=user.id,
            rule_type=RuleType.ai_boundary,
            scope=RuleScope.household,
            name="Increase autonomy at 8",
            parameters={"ai_autonomy_level": "approve_difficult"},
            is_active=False,
            trigger_conditions={
                "type": "age_threshold",
                "child_id": str(child.id),
                "age_years": 8,
                "action": "activate",
            },
        )
        db_session.add(rule)
        await db_session.commit()

        from app.core.config import settings as cfg

        test_url = cfg.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"
        eng = create_async_engine(test_url, poolclass=NullPool)
        sf = async_sessionmaker(eng, class_=AsyncSession, expire_on_commit=False)

        result = await evaluate_temporal_triggers(session_factory=sf)
        assert result["triggers_fired"] >= 1

        # Verify rule is now active
        async with sf() as check_db:
            r = await check_db.execute(select(GovernanceRule).where(GovernanceRule.id == rule.id))
            updated = r.scalar_one()
            assert updated.is_active is True
            assert updated.trigger_conditions.get("triggered_at") is not None

            # Verify governance event logged
            ev = await check_db.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.target_type == "temporal_trigger",
                    GovernanceEvent.target_id == rule.id,
                )
            )
            event = ev.scalar_one()
            assert "AgeTest turned 8" in event.reason

        await eng.dispose()


class TestMasteryMilestoneTrigger:
    @pytest.mark.asyncio
    async def test_mastery_triggers_rule(self, db_session, household, user, subject, learning_map):
        """Rule fires when child reaches 100% mastery on a map."""
        from app.tasks.temporal_rules import evaluate_temporal_triggers

        child = Child(household_id=household.id, first_name="MasteryTest")
        db_session.add(child)
        await db_session.flush()

        # Create 2 nodes in the map
        for title in ["Node A", "Node B"]:
            node = LearningNode(
                learning_map_id=learning_map.id,
                household_id=household.id,
                node_type=NodeType.skill,
                title=title,
            )
            db_session.add(node)
            await db_session.flush()
            # Master both
            db_session.add(
                ChildNodeState(
                    child_id=child.id,
                    household_id=household.id,
                    node_id=node.id,
                    mastery_level=MasteryLevel.mastered,
                )
            )

        rule = GovernanceRule(
            household_id=household.id,
            created_by=user.id,
            rule_type=RuleType.approval_required,
            scope=RuleScope.household,
            name="Unlock next level",
            parameters={},
            is_active=False,
            trigger_conditions={
                "type": "mastery_milestone",
                "child_id": str(child.id),
                "map_id": str(learning_map.id),
                "mastery_percentage": 100,
                "action": "activate",
            },
        )
        db_session.add(rule)
        await db_session.commit()

        from app.core.config import settings as cfg

        test_url = cfg.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"
        eng = create_async_engine(test_url, poolclass=NullPool)
        sf = async_sessionmaker(eng, class_=AsyncSession, expire_on_commit=False)

        result = await evaluate_temporal_triggers(session_factory=sf)
        assert result["triggers_fired"] >= 1

        async with sf() as check_db:
            r = await check_db.execute(select(GovernanceRule).where(GovernanceRule.id == rule.id))
            assert r.scalar_one().is_active is True

        await eng.dispose()


class TestEffectiveDateWindow:
    @pytest.mark.asyncio
    async def test_future_rule_not_enforced(self, db_session, household, user):
        """A rule with effective_from=tomorrow should not be applied today."""
        tomorrow = date.today() + timedelta(days=1)
        rule = GovernanceRule(
            household_id=household.id,
            created_by=user.id,
            rule_type=RuleType.approval_required,
            scope=RuleScope.household,
            name="Future rule",
            parameters={"min_difficulty": 1, "action": "block"},
            priority=1,
            effective_from=tomorrow,
        )
        db_session.add(rule)
        await db_session.flush()

        # This rule should NOT block because it's not yet effective
        decision = await evaluate_activity(db_session, household.id, difficulty=5)
        # Without any other blocking rule, should auto-approve
        assert decision.action != "block"

    @pytest.mark.asyncio
    async def test_expired_rule_not_enforced(self, db_session, household, user):
        """A rule with effective_until=yesterday should not be applied."""
        yesterday = date.today() - timedelta(days=1)
        rule = GovernanceRule(
            household_id=household.id,
            created_by=user.id,
            rule_type=RuleType.approval_required,
            scope=RuleScope.household,
            name="Expired rule",
            parameters={"min_difficulty": 1, "action": "block"},
            priority=1,
            effective_until=yesterday,
        )
        db_session.add(rule)
        await db_session.flush()

        decision = await evaluate_activity(db_session, household.id, difficulty=5)
        assert decision.action != "block"


class TestTriggerIdempotency:
    @pytest.mark.asyncio
    async def test_trigger_fires_only_once(self, db_session, household, user):
        """Running the temporal task twice should only create one event."""
        from app.tasks.temporal_rules import evaluate_temporal_triggers

        rule = GovernanceRule(
            household_id=household.id,
            created_by=user.id,
            rule_type=RuleType.ai_boundary,
            scope=RuleScope.household,
            name="Idempotent trigger",
            parameters={},
            is_active=False,
            trigger_conditions={
                "type": "date_scheduled",
                "date": date.today().isoformat(),
                "action": "activate",
            },
        )
        db_session.add(rule)
        await db_session.commit()

        from app.core.config import settings as cfg

        test_url = cfg.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"
        eng = create_async_engine(test_url, poolclass=NullPool)
        sf = async_sessionmaker(eng, class_=AsyncSession, expire_on_commit=False)

        r1 = await evaluate_temporal_triggers(session_factory=sf)
        r2 = await evaluate_temporal_triggers(session_factory=sf)

        assert r1["triggers_fired"] >= 1
        assert r2["triggers_fired"] == 0  # Already triggered

        # Only one governance event
        async with sf() as check_db:
            ev = await check_db.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.target_type == "temporal_trigger",
                    GovernanceEvent.target_id == rule.id,
                )
            )
            events = ev.scalars().all()
            assert len(events) == 1

        await eng.dispose()
