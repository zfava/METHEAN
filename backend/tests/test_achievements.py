"""Tests for the achievement system."""

import uuid
from datetime import date, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Child, Household
from app.models.achievements import Achievement, Streak
from app.models.governance import Activity, Attempt
from app.models.enums import AttemptStatus, ActivityStatus
from app.services.achievements import (
    check_achievements,
    update_streak,
    get_achievements,
    get_streak,
    get_all_definitions,
    ACHIEVEMENT_DEFS,
)


@pytest_asyncio.fixture
async def ach_household(db_session: AsyncSession) -> Household:
    h = Household(name="Achievement Test Family")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def ach_child(db_session: AsyncSession, ach_household: Household) -> Child:
    c = Child(household_id=ach_household.id, first_name="Emma", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def ach_child_b(db_session: AsyncSession, ach_household: Household) -> Child:
    c = Child(household_id=ach_household.id, first_name="Lucas", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


async def _create_completed_attempt(db, child, household, subject=None):
    """Helper: create a completed attempt."""
    act = Activity(
        household_id=household.id,
        title="Test Activity",
        activity_type="lesson",
        status=ActivityStatus.completed,
        subject_area=subject,
    )
    db.add(act)
    await db.flush()
    attempt = Attempt(
        activity_id=act.id,
        household_id=household.id,
        child_id=child.id,
        status=AttemptStatus.completed,
    )
    db.add(attempt)
    await db.flush()
    return attempt


@pytest.mark.asyncio
async def test_check_achievements_first_steps(db_session, ach_child, ach_household):
    """Completing first activity earns 'First Steps'."""
    await _create_completed_attempt(db_session, ach_child, ach_household)
    earned = await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")
    titles = [a.title for a in earned]
    assert "First Steps" in titles


@pytest.mark.asyncio
async def test_check_achievements_no_duplicate(db_session, ach_child, ach_household):
    """'First Steps' is only earned once."""
    await _create_completed_attempt(db_session, ach_child, ach_household)
    earned1 = await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")
    assert any(a.title == "First Steps" for a in earned1)

    await _create_completed_attempt(db_session, ach_child, ach_household)
    earned2 = await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")
    assert not any(a.title == "First Steps" for a in earned2)


@pytest.mark.asyncio
async def test_streak_update_consecutive_days(db_session, ach_child, ach_household):
    """3 consecutive days of activity gives streak of 3."""
    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    assert streak.current_streak == 1

    # Simulate next day
    streak.last_activity_date = date.today() - timedelta(days=1)
    await db_session.flush()
    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    assert streak.current_streak == 2

    streak.last_activity_date = date.today() - timedelta(days=1)
    await db_session.flush()
    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    assert streak.current_streak == 3


@pytest.mark.asyncio
async def test_streak_reset_gap(db_session, ach_child, ach_household):
    """Skipping a day resets streak to 1."""
    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    streak.current_streak = 5
    streak.last_activity_date = date.today() - timedelta(days=3)  # Gap
    await db_session.flush()

    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    assert streak.current_streak == 1


@pytest.mark.asyncio
async def test_streak_longest_preserved(db_session, ach_child, ach_household):
    """Longest streak is preserved after a break."""
    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    streak.current_streak = 5
    streak.longest_streak = 5
    streak.last_activity_date = date.today() - timedelta(days=3)
    await db_session.flush()

    streak = await update_streak(db_session, ach_child.id, ach_household.id)
    assert streak.current_streak == 1
    assert streak.longest_streak == 5


@pytest.mark.asyncio
async def test_subject_star_earned_on_first_mastery(db_session, ach_child, ach_household):
    """Mastering first node in a subject earns Subject Star."""
    await _create_completed_attempt(db_session, ach_child, ach_household, subject="math")
    earned = await check_achievements(
        db_session, ach_child.id, ach_household.id, "mastery_change",
        context={"new_level": "mastered", "old_level": "developing", "subject": "Math"},
    )
    titles = [a.title for a in earned]
    assert any("Subject Star" in t for t in titles)


@pytest.mark.asyncio
async def test_century_club_at_100(db_session, ach_child, ach_household):
    """100 completed attempts earns Century Club."""
    for _ in range(100):
        await _create_completed_attempt(db_session, ach_child, ach_household)
    earned = await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")
    titles = [a.title for a in earned]
    assert "Century Club" in titles


@pytest.mark.asyncio
async def test_explorer_five_subjects(db_session, ach_child, ach_household):
    """Activities in 5 subjects earns Explorer."""
    for subj in ["math", "science", "history", "reading", "art"]:
        act = Activity(
            household_id=ach_household.id, title=f"{subj} activity",
            activity_type="lesson", status=ActivityStatus.completed, subject_area=subj,
        )
        db_session.add(act)
    await db_session.flush()
    await _create_completed_attempt(db_session, ach_child, ach_household)

    earned = await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")
    titles = [a.title for a in earned]
    assert "Explorer" in titles


@pytest.mark.asyncio
async def test_get_achievements_returns_earned_and_definitions(db_session, ach_child, ach_household):
    """get_achievements returns list, get_all_definitions returns all defs."""
    await _create_completed_attempt(db_session, ach_child, ach_household)
    await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")

    earned = await get_achievements(db_session, ach_child.id)
    assert len(earned) >= 1
    assert "title" in earned[0]

    defs = get_all_definitions()
    assert len(defs) == len(ACHIEVEMENT_DEFS)


@pytest.mark.asyncio
async def test_achievement_has_correct_fields():
    """Every definition has required fields."""
    for d in get_all_definitions():
        assert "type" in d
        assert "title" in d
        assert "description" in d
        assert "icon" in d
        assert "category" in d


@pytest.mark.asyncio
async def test_achievements_scoped_to_child(db_session, ach_child, ach_child_b, ach_household):
    """Child A's achievements don't appear for child B."""
    await _create_completed_attempt(db_session, ach_child, ach_household)
    await check_achievements(db_session, ach_child.id, ach_household.id, "activity_complete")

    child_a_earned = await get_achievements(db_session, ach_child.id)
    child_b_earned = await get_achievements(db_session, ach_child_b.id)
    assert len(child_a_earned) >= 1
    assert len(child_b_earned) == 0


@pytest.mark.asyncio
async def test_comeback_kid_earned(db_session, ach_child, ach_household):
    """Re-mastering after decay earns Comeback Kid."""
    await _create_completed_attempt(db_session, ach_child, ach_household)
    earned = await check_achievements(
        db_session, ach_child.id, ach_household.id, "mastery_change",
        context={"new_level": "mastered", "old_level": "emerging", "subject": "math"},
    )
    titles = [a.title for a in earned]
    assert "Comeback Kid" in titles


@pytest.mark.asyncio
async def test_get_streak_empty(db_session, ach_child, ach_household):
    """Streak for child with no activity returns zeros."""
    s = await get_streak(db_session, ach_child.id, ach_household.id)
    assert s["current_streak"] == 0
    assert s["longest_streak"] == 0
