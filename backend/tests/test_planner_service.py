"""Tests for the planner service."""

import pytest
import pytest_asyncio

from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.identity import Child, Household


@pytest_asyncio.fixture
async def plan_household(db_session):
    h = Household(name="Planner Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def plan_child(db_session, plan_household):
    c = Child(household_id=plan_household.id, first_name="Planner")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def plan_map(db_session, plan_household):
    s = Subject(household_id=plan_household.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    m = LearningMap(household_id=plan_household.id, subject_id=s.id, name="Map")
    db_session.add(m)
    await db_session.flush()
    for i in range(5):
        db_session.add(
            LearningNode(
                learning_map_id=m.id,
                household_id=plan_household.id,
                node_type=NodeType.concept,
                title=f"Node {i}",
                sort_order=i,
            )
        )
    await db_session.flush()
    return m


@pytest.mark.asyncio
class TestPlannerContext:
    async def test_build_context_returns_dict(self, db_session, plan_child, plan_household, plan_map):
        """_build_planner_context should return a dict."""
        # Enroll child
        db_session.add(
            ChildMapEnrollment(
                child_id=plan_child.id,
                household_id=plan_household.id,
                learning_map_id=plan_map.id,
                is_active=True,
            )
        )
        await db_session.flush()
        from app.services.planner import _build_planner_context

        ctx = await _build_planner_context(db_session, plan_child.id, plan_household.id, 120)
        assert isinstance(ctx, dict)
        assert "daily_minutes" in ctx
        assert "nodes" in ctx

    async def test_empty_enrollment_returns_empty_nodes(self, db_session, plan_child, plan_household):
        """No enrollments → empty nodes list."""
        from app.services.planner import _build_planner_context

        ctx = await _build_planner_context(db_session, plan_child.id, plan_household.id, 120)
        assert ctx["nodes"] == []

    async def test_context_includes_daily_minutes(self, db_session, plan_child, plan_household):
        from app.services.planner import _build_planner_context

        ctx = await _build_planner_context(db_session, plan_child.id, plan_household.id, 90)
        assert ctx["daily_minutes"] == 90
