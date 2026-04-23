"""Physical-education hours flow from fitness_service into the compliance breakdown.

log_fitness_activity writes a FitnessLog AND bumps child_node_state.time_spent_minutes
for the target node. get_hours_breakdown aggregates child_node_states grouped by the
subject attached to the node's learning_map. Together, fitness log duration should
show up under the learning map's subject name in by_subject — with no special-case
code in compliance_engine.
"""

from datetime import UTC, datetime

import pytest
import pytest_asyncio

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.services.compliance_engine import get_hours_breakdown
from app.services.fitness_service import log_fitness_activity


@pytest_asyncio.fixture
async def pe_subject(db_session, household) -> Subject:
    s = Subject(household_id=household.id, name="Physical Fitness")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def pe_map(db_session, household, pe_subject) -> LearningMap:
    lm = LearningMap(
        household_id=household.id,
        subject_id=pe_subject.id,
        name="Physical Fitness: Foundations",
    )
    db_session.add(lm)
    await db_session.flush()
    return lm


@pytest_asyncio.fixture
async def pe_node(db_session, household, pe_map) -> LearningNode:
    node = LearningNode(
        learning_map_id=pe_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title="Two-Foot Jump",
        content={
            "description": "Jump forward from two feet.",
            "benchmark_criteria": "Land 8 of 10.",
            "assessment_type": "counted",
            "measurement_unit": "repetitions",
            "suggested_frequency": 4,
        },
    )
    db_session.add(node)
    await db_session.flush()
    return node


class TestFitnessHoursFlowThroughCompliance:
    @pytest.mark.asyncio
    async def test_fitness_log_minutes_appear_in_total_hours(self, db_session, household, child, user, pe_node):
        """A 45-minute fitness log bumps get_hours_breakdown total by 0.75 hours."""
        before = await get_hours_breakdown(db_session, household.id, child.id)
        before_total = before["total_hours"]

        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=45,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )

        after = await get_hours_breakdown(db_session, household.id, child.id)
        # 45 minutes = 0.75 hours
        assert after["total_hours"] == pytest.approx(before_total + 0.75, abs=0.01)

    @pytest.mark.asyncio
    async def test_fitness_log_lands_in_pe_subject_bucket(self, db_session, household, child, user, pe_node):
        """Logged minutes show up under the learning_map's subject name."""
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=60,
            measurement_type="counted",
            measurement_value=15,
            measurement_unit="repetitions",
            logged_by=user.id,
        )

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        assert "Physical Fitness" in hours["by_subject"], (
            f"Expected 'Physical Fitness' in {list(hours['by_subject'].keys())}"
        )
        assert hours["by_subject"]["Physical Fitness"] == pytest.approx(1.0, abs=0.05)

    @pytest.mark.asyncio
    async def test_multiple_fitness_logs_accumulate(self, db_session, household, child, user, pe_node):
        """Three 20-minute sessions = 60 minutes = 1.0 hours under Physical Fitness."""
        now = datetime.now(UTC)
        for _ in range(3):
            await log_fitness_activity(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=pe_node.id,
                logged_at=now,
                duration_minutes=20,
                measurement_type="counted",
                measurement_value=12,
                measurement_unit="repetitions",
                logged_by=user.id,
            )

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        assert hours["by_subject"]["Physical Fitness"] == pytest.approx(1.0, abs=0.05)

    @pytest.mark.asyncio
    async def test_pe_hours_additive_to_academic_hours(
        self,
        db_session,
        household,
        child,
        user,
        subject,
        learning_map,
        pe_node,
    ):
        """PE minutes add to — not replace — existing academic subject hours."""
        # Academic node: 60 minutes logged via ChildNodeState directly.
        from app.models.state import ChildNodeState

        math_node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Addition",
        )
        db_session.add(math_node)
        await db_session.flush()
        db_session.add(
            ChildNodeState(
                child_id=child.id,
                household_id=household.id,
                node_id=math_node.id,
                time_spent_minutes=60,
            )
        )
        await db_session.flush()

        # 30 minutes of fitness on the PE node.
        await log_fitness_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=pe_node.id,
            logged_at=datetime.now(UTC),
            duration_minutes=30,
            measurement_type="counted",
            measurement_value=10,
            measurement_unit="repetitions",
            logged_by=user.id,
        )

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        # 60 min math + 30 min PE = 1.5 hours total
        assert hours["total_hours"] == pytest.approx(1.5, abs=0.05)
        # Both subjects represented in breakdown.
        assert hours["by_subject"]["Mathematics"] == pytest.approx(1.0, abs=0.05)
        assert hours["by_subject"]["Physical Fitness"] == pytest.approx(0.5, abs=0.05)
