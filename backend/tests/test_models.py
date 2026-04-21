"""Tests for database models."""

from datetime import date

import pytest
from sqlalchemy import select

from app.models.curriculum import (
    LearningEdge,
    LearningMap,
    LearningNode,
    Subject,
)
from app.models.enums import (
    ActivityType,
    AuditAction,
    EdgeRelation,
    NodeType,
    PlanStatus,
    RuleScope,
    RuleType,
    StateEventType,
    UserRole,
)
from app.models.governance import Activity, GovernanceRule, Plan, PlanWeek
from app.models.identity import Child, ChildPreferences, Household, User
from app.models.operational import AuditLog
from app.models.state import StateEvent


@pytest.mark.asyncio
async def test_household_creation(db_session):
    h = Household(name="Smith Family")
    db_session.add(h)
    await db_session.flush()

    result = await db_session.execute(select(Household).where(Household.id == h.id))
    loaded = result.scalar_one()
    assert loaded.name == "Smith Family"
    assert loaded.timezone == "America/New_York"
    assert loaded.id is not None


@pytest.mark.asyncio
async def test_user_creation(db_session, household):
    u = User(
        household_id=household.id,
        email="test@example.com",
        password_hash="hashed",
        display_name="Test User",
        role=UserRole.owner,
    )
    db_session.add(u)
    await db_session.flush()

    result = await db_session.execute(select(User).where(User.id == u.id))
    loaded = result.scalar_one()
    assert loaded.email == "test@example.com"
    assert loaded.role == UserRole.owner
    assert loaded.household_id == household.id
    assert loaded.is_active is True


@pytest.mark.asyncio
async def test_child_with_preferences(db_session, household):
    child = Child(
        household_id=household.id,
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date(2015, 6, 15),
        grade_level="3rd",
    )
    db_session.add(child)
    await db_session.flush()

    prefs = ChildPreferences(
        child_id=child.id,
        household_id=household.id,
        learning_style={"visual": True, "kinesthetic": True},
        interests=["science", "art"],
        daily_duration_minutes=180,
    )
    db_session.add(prefs)
    await db_session.flush()

    result = await db_session.execute(select(Child).where(Child.id == child.id))
    loaded = result.scalar_one()
    assert loaded.first_name == "Alice"
    assert loaded.grade_level == "3rd"


@pytest.mark.asyncio
async def test_curriculum_dag(db_session, household):
    subject = Subject(household_id=household.id, name="Mathematics")
    db_session.add(subject)
    await db_session.flush()

    lmap = LearningMap(
        household_id=household.id,
        subject_id=subject.id,
        name="Elementary Math",
    )
    db_session.add(lmap)
    await db_session.flush()

    node_a = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title="Addition",
    )
    node_b = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title="Multiplication",
    )
    db_session.add_all([node_a, node_b])
    await db_session.flush()

    edge = LearningEdge(
        learning_map_id=lmap.id,
        household_id=household.id,
        from_node_id=node_a.id,
        to_node_id=node_b.id,
        relation=EdgeRelation.prerequisite,
    )
    db_session.add(edge)
    await db_session.flush()

    result = await db_session.execute(select(LearningEdge).where(LearningEdge.learning_map_id == lmap.id))
    loaded_edge = result.scalar_one()
    assert loaded_edge.from_node_id == node_a.id
    assert loaded_edge.to_node_id == node_b.id
    assert loaded_edge.relation == EdgeRelation.prerequisite


@pytest.mark.asyncio
async def test_state_events_append_only(db_session, household):
    child = Child(household_id=household.id, first_name="Bob")
    db_session.add(child)
    await db_session.flush()

    subject = Subject(household_id=household.id, name="Science")
    db_session.add(subject)
    await db_session.flush()

    lmap = LearningMap(household_id=household.id, subject_id=subject.id, name="Biology")
    db_session.add(lmap)
    await db_session.flush()

    node = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title="Cell Biology",
    )
    db_session.add(node)
    await db_session.flush()

    # Create state event
    event = StateEvent(
        child_id=child.id,
        household_id=household.id,
        node_id=node.id,
        event_type=StateEventType.mastery_change,
        from_state="not_started",
        to_state="emerging",
        trigger="review_completed",
    )
    db_session.add(event)
    await db_session.flush()

    result = await db_session.execute(select(StateEvent).where(StateEvent.child_id == child.id))
    loaded = result.scalar_one()
    assert loaded.event_type == StateEventType.mastery_change
    assert loaded.to_state == "emerging"


@pytest.mark.asyncio
async def test_governance_rule(db_session, household, user):
    rule = GovernanceRule(
        household_id=household.id,
        created_by=user.id,
        rule_type=RuleType.pace_limit,
        scope=RuleScope.household,
        name="Max 4 hours daily",
        parameters={"max_daily_minutes": 240},
    )
    db_session.add(rule)
    await db_session.flush()

    result = await db_session.execute(select(GovernanceRule).where(GovernanceRule.household_id == household.id))
    loaded = result.scalar_one()
    assert loaded.rule_type == RuleType.pace_limit
    assert loaded.parameters["max_daily_minutes"] == 240


@pytest.mark.asyncio
async def test_plan_with_activities(db_session, household, user):
    child = Child(household_id=household.id, first_name="Charlie")
    db_session.add(child)
    await db_session.flush()

    plan = Plan(
        household_id=household.id,
        child_id=child.id,
        created_by=user.id,
        name="Spring Semester",
        status=PlanStatus.draft,
        start_date=date(2026, 1, 6),
        end_date=date(2026, 5, 29),
    )
    db_session.add(plan)
    await db_session.flush()

    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 1, 6),
        end_date=date(2026, 1, 10),
    )
    db_session.add(week)
    await db_session.flush()

    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        activity_type=ActivityType.lesson,
        title="Intro to Fractions",
        estimated_minutes=45,
        scheduled_date=date(2026, 1, 6),
    )
    db_session.add(activity)
    await db_session.flush()

    result = await db_session.execute(select(Activity).where(Activity.plan_week_id == week.id))
    loaded = result.scalar_one()
    assert loaded.title == "Intro to Fractions"
    assert loaded.activity_type == ActivityType.lesson


@pytest.mark.asyncio
async def test_audit_log(db_session, household, user):
    log = AuditLog(
        household_id=household.id,
        user_id=user.id,
        action=AuditAction.login,
        resource_type="session",
        ip_address="127.0.0.1",
    )
    db_session.add(log)
    await db_session.flush()

    result = await db_session.execute(select(AuditLog).where(AuditLog.user_id == user.id))
    loaded = result.scalar_one()
    assert loaded.action == AuditAction.login
