"""Tests for the attempt workflow pipeline — the heartbeat of METHEAN."""

import uuid
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy import func, select

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import ActivityStatus, ActivityType, AttemptStatus, NodeType
from app.models.governance import Activity, Plan, PlanWeek
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, StateEvent
from app.services.attempt_workflow import save_attempt_progress, start_attempt, submit_attempt


@pytest_asyncio.fixture
async def aw_household(db_session):
    h = Household(name="Workflow Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def aw_child(db_session, aw_household):
    c = Child(household_id=aw_household.id, first_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def aw_node(db_session, aw_household):
    s = Subject(household_id=aw_household.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    m = LearningMap(household_id=aw_household.id, subject_id=s.id, name="Map")
    db_session.add(m)
    await db_session.flush()
    n = LearningNode(learning_map_id=m.id, household_id=aw_household.id, node_type=NodeType.concept, title="Addition")
    db_session.add(n)
    await db_session.flush()
    return n


@pytest_asyncio.fixture
async def aw_activity(db_session, aw_household, aw_node):
    c = Child(household_id=aw_household.id, first_name="PlanChild")
    db_session.add(c)
    await db_session.flush()
    plan = Plan(household_id=aw_household.id, child_id=c.id, name="Test Plan", status="active")
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=aw_household.id,
        week_number=1,
        start_date=date(2026, 1, 5),
        end_date=date(2026, 1, 11),
    )
    db_session.add(week)
    await db_session.flush()
    a = Activity(
        plan_week_id=week.id,
        household_id=aw_household.id,
        title="Practice",
        activity_type=ActivityType.practice,
        node_id=aw_node.id,
        estimated_minutes=20,
    )
    db_session.add(a)
    await db_session.flush()
    return a


@pytest.mark.asyncio
class TestStartAttempt:
    async def test_creates_record(self, db_session, aw_household, aw_child, aw_activity):
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        assert att.id is not None
        assert att.status == AttemptStatus.started
        assert att.activity_id == aw_activity.id

    async def test_activity_not_found_raises(self, db_session, aw_household, aw_child):
        with pytest.raises(ValueError, match="Activity not found"):
            await start_attempt(db_session, uuid.uuid4(), aw_child.id, aw_household.id)

    async def test_updates_activity_status(self, db_session, aw_household, aw_child, aw_activity):
        assert aw_activity.status == ActivityStatus.scheduled
        await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        assert aw_activity.status == ActivityStatus.in_progress


@pytest.mark.asyncio
class TestSubmitAttempt:
    async def test_completes_attempt(self, db_session, aw_household, aw_child, aw_activity):
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        result = await submit_attempt(db_session, att.id, aw_household.id, confidence=0.7, duration_minutes=15)
        assert result["attempt"].status == AttemptStatus.completed
        assert result["attempt"].completed_at is not None

    async def test_already_completed_raises(self, db_session, aw_household, aw_child, aw_activity):
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        await submit_attempt(db_session, att.id, aw_household.id, confidence=0.7)
        with pytest.raises(ValueError, match="already"):
            await submit_attempt(db_session, att.id, aw_household.id, confidence=0.7)

    async def test_triggers_state_review(self, db_session, aw_household, aw_child, aw_activity):
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        result = await submit_attempt(db_session, att.id, aw_household.id, confidence=0.7)
        assert result["mastery_level"] is not None
        assert result["fsrs_rating"] is not None

    async def test_no_node_returns_null_mastery(self, db_session, aw_household, aw_child):
        plan = Plan(household_id=aw_household.id, child_id=aw_child.id, name="P", status="active")
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=aw_household.id,
            week_number=1,
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 11),
        )
        db_session.add(week)
        await db_session.flush()
        a = Activity(
            plan_week_id=week.id,
            household_id=aw_household.id,
            title="No Node",
            activity_type=ActivityType.lesson,
            node_id=None,
        )
        db_session.add(a)
        await db_session.flush()
        att = await start_attempt(db_session, a.id, aw_child.id, aw_household.id)
        result = await submit_attempt(db_session, att.id, aw_household.id, confidence=0.8)
        assert result["mastery_level"] is None


@pytest.mark.asyncio
class TestSaveAttemptProgress:
    async def test_persists_draft_without_completing(self, db_session, aw_household, aw_child, aw_activity):
        """Saving progress stores draft notes, keeps the attempt started, and runs no pipeline."""
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)

        saved = await save_attempt_progress(
            db_session,
            att.id,
            aw_household.id,
            notes="Built the model frame, painted two sides.",
        )

        assert saved.feedback["draft_notes"] == "Built the model frame, painted two sides."
        assert "draft_saved_at" in saved.feedback
        assert saved.status == AttemptStatus.started
        assert saved.completed_at is None
        assert saved.score is None

        # No StateEvent emitted and no mastery transition recorded.
        event_count = await db_session.scalar(
            select(func.count()).select_from(StateEvent).where(StateEvent.household_id == aw_household.id)
        )
        assert event_count == 0
        state_count = await db_session.scalar(
            select(func.count()).select_from(ChildNodeState).where(ChildNodeState.child_id == aw_child.id)
        )
        assert state_count == 0

    async def test_merges_into_existing_feedback(self, db_session, aw_household, aw_child, aw_activity):
        """Saving progress merges draft notes without dropping prior feedback keys."""
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        att.feedback = {"responses": [{"prompt": "Q1", "response": "A1"}]}
        await db_session.flush()

        saved = await save_attempt_progress(db_session, att.id, aw_household.id, notes="First draft")
        assert saved.feedback["responses"] == [{"prompt": "Q1", "response": "A1"}]
        assert saved.feedback["draft_notes"] == "First draft"

        # A second save overwrites the draft but still preserves the prior key.
        saved = await save_attempt_progress(db_session, att.id, aw_household.id, notes="Second draft")
        assert saved.feedback["responses"] == [{"prompt": "Q1", "response": "A1"}]
        assert saved.feedback["draft_notes"] == "Second draft"

    async def test_missing_attempt_raises(self, db_session, aw_household):
        with pytest.raises(ValueError, match="Attempt not found"):
            await save_attempt_progress(db_session, uuid.uuid4(), aw_household.id, notes="x")

    async def test_cross_household_attempt_raises(self, db_session, aw_household, aw_child, aw_activity):
        """An attempt from another household is not reachable and raises ValueError."""
        att = await start_attempt(db_session, aw_activity.id, aw_child.id, aw_household.id)
        other = Household(name="Other Household")
        db_session.add(other)
        await db_session.flush()
        with pytest.raises(ValueError, match="Attempt not found"):
            await save_attempt_progress(db_session, att.id, other.id, notes="x")
