"""Regression tests for ``GET /children/{child_id}/today`` (METHEAN-6-06).

The legacy handler scoped activities only to ``household_id``, so
sibling activities leaked into every response. These tests prove the
current handler joins Activity → PlanWeek → Plan and filters on the
target child's ``Plan.child_id``.
"""

from datetime import date, timedelta

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ActivityStatus, ActivityType, PlanStatus
from app.models.governance import Activity, Plan, PlanWeek
from app.models.identity import Child, Household


async def _make_plan_with_activity(
    db_session: AsyncSession,
    *,
    household_id,
    child_id,
    title: str,
    scheduled_date: date,
    status: ActivityStatus = ActivityStatus.scheduled,
) -> Activity:
    """Drop a Plan + PlanWeek + Activity row owned by ``child_id``."""
    plan = Plan(
        household_id=household_id,
        child_id=child_id,
        name=f"Plan for {title}",
        status=PlanStatus.active,
    )
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household_id,
        week_number=1,
        start_date=scheduled_date,
        end_date=scheduled_date + timedelta(days=6),
    )
    db_session.add(week)
    await db_session.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household_id,
        activity_type=ActivityType.lesson,
        title=title,
        status=status,
        scheduled_date=scheduled_date,
    )
    db_session.add(activity)
    await db_session.flush()
    return activity


@pytest_asyncio.fixture
async def sibling(db_session: AsyncSession, household: Household) -> Child:
    """A second child in the same household — the bug source."""
    c = Child(household_id=household.id, first_name="Sibling", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


# ══════════════════════════════════════════════════════════════════════
# Spec tests
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_today_returns_only_target_child_activities(auth_client, db_session, household, child, sibling):
    today = date.today()
    await _make_plan_with_activity(
        db_session,
        household_id=household.id,
        child_id=child.id,
        title="Math for Target",
        scheduled_date=today,
    )
    await _make_plan_with_activity(
        db_session,
        household_id=household.id,
        child_id=sibling.id,
        title="Reading for Sibling",
        scheduled_date=today,
    )

    resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
    assert resp.status_code == 200, resp.text
    titles = [a["title"] for a in resp.json()]
    assert "Math for Target" in titles
    assert "Reading for Sibling" not in titles
    assert len(titles) == 1


@pytest.mark.asyncio
async def test_today_returns_empty_for_child_with_no_activities_today(
    auth_client, db_session, household, child, sibling
):
    """Sibling has activities today; the target child does not."""
    today = date.today()
    await _make_plan_with_activity(
        db_session,
        household_id=household.id,
        child_id=sibling.id,
        title="Sibling Only",
        scheduled_date=today,
    )

    resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_today_excludes_completed_and_cancelled_activities(auth_client, db_session, household, child):
    """Only ``scheduled`` and ``in_progress`` are returned."""
    today = date.today()
    for title, status in [
        ("Scheduled Math", ActivityStatus.scheduled),
        ("In Progress Math", ActivityStatus.in_progress),
        ("Completed Math", ActivityStatus.completed),
        ("Cancelled Math", ActivityStatus.cancelled),
    ]:
        await _make_plan_with_activity(
            db_session,
            household_id=household.id,
            child_id=child.id,
            title=title,
            scheduled_date=today,
            status=status,
        )

    resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
    assert resp.status_code == 200, resp.text
    titles = sorted(a["title"] for a in resp.json())
    assert titles == ["In Progress Math", "Scheduled Math"]


@pytest.mark.asyncio
async def test_today_respects_target_date_query_param(auth_client, db_session, household, child):
    today = date.today()
    future = today + timedelta(days=3)
    await _make_plan_with_activity(
        db_session,
        household_id=household.id,
        child_id=child.id,
        title="Today Activity",
        scheduled_date=today,
    )
    await _make_plan_with_activity(
        db_session,
        household_id=household.id,
        child_id=child.id,
        title="Future Activity",
        scheduled_date=future,
    )

    resp = await auth_client.get(
        f"/api/v1/children/{child.id}/today",
        params={"date": future.isoformat()},
    )
    assert resp.status_code == 200, resp.text
    titles = [a["title"] for a in resp.json()]
    assert titles == ["Future Activity"]


@pytest.mark.asyncio
async def test_today_uses_plan_join_not_household_only(auth_client, db_session, household, child, sibling):
    """Pre-fix sentinel: with both children seeded, a household-only
    filter would return every row. The join MUST trim the result to
    the target child.
    """
    today = date.today()
    for i in range(3):
        await _make_plan_with_activity(
            db_session,
            household_id=household.id,
            child_id=sibling.id,
            title=f"Sibling Activity {i}",
            scheduled_date=today,
        )
    await _make_plan_with_activity(
        db_session,
        household_id=household.id,
        child_id=child.id,
        title="Only Mine",
        scheduled_date=today,
    )

    resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1, (
        f"Expected exactly 1 activity for the target child, got {len(items)}. "
        "Regression: handler is leaking sibling activities."
    )
    assert items[0]["title"] == "Only Mine"
