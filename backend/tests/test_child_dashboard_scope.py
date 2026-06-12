"""The kid surface shows a child only their own day.

The verification harness (PR 58) flagged that child_dashboard.py's
today query filtered by household only, so in a multi-child household
each child's dashboard listed every sibling's same-day activities.
The fix joins Activity -> PlanWeek -> Plan and filters Plan.child_id,
the same scoping /children/{id}/today (spec_coverage.py) has always
used. Activity.plan_week_id is non-nullable, so the inner join drops
nothing: there is no plan-less, household-level activity concept.

The leak surface is the kid-mode session, so the assertions run with
child-scoped tokens, exactly as the kid surface calls the endpoint.
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.models.enums import ActivityStatus, ActivityType, PlanStatus
from app.models.governance import Activity, Plan, PlanWeek
from app.models.identity import Household, User


async def _seed_today_activity(
    db: AsyncSession, household: Household, user: User, child_id: uuid.UUID, title: str
) -> Activity:
    """One approved activity scheduled today for one child, through the
    real Plan -> PlanWeek -> Activity shape."""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    plan = Plan(
        household_id=household.id,
        child_id=child_id,
        created_by=user.id,
        name=f"Week of {week_start}",
        status=PlanStatus.active,
        start_date=week_start,
        end_date=week_start + timedelta(days=4),
    )
    db.add(plan)
    await db.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=week_start,
        end_date=week_start + timedelta(days=4),
    )
    db.add(week)
    await db.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        activity_type=ActivityType.practice,
        title=title,
        status=ActivityStatus.scheduled,
        scheduled_date=today,
        governance_approved=True,
        governance_reviewed_by=user.id,
        governance_reviewed_at=datetime.now(UTC),
    )
    db.add(activity)
    await db.flush()
    return activity


def _kid_cookie(client, user: User, household: Household, child_id: uuid.UUID) -> None:
    token = create_access_token(user.id, household.id, "owner", scope="child", child_id=child_id)
    client.cookies.set("access_token", token)


@pytest.mark.asyncio
async def test_each_child_sees_only_their_own_today(client, db_session, household, user, child, second_child):
    """Two children, one same-day activity each: each kid-mode session's
    dashboard lists exactly its own activity, never the sibling's."""
    await _seed_today_activity(db_session, household, user, child.id, "Alpha's addition")
    await _seed_today_activity(db_session, household, user, second_child.id, "Beta's biology")

    _kid_cookie(client, user, household, child.id)
    resp = await client.get(f"/api/v1/children/{child.id}/dashboard")
    assert resp.status_code == 200, resp.text
    titles = [a["title"] for a in resp.json()["today"]["activities"]]
    assert "Alpha's addition" in titles
    assert "Beta's biology" not in titles, "sibling activity leaked onto this child's kid surface"

    _kid_cookie(client, user, household, second_child.id)
    resp = await client.get(f"/api/v1/children/{second_child.id}/dashboard")
    assert resp.status_code == 200, resp.text
    titles = [a["title"] for a in resp.json()["today"]["activities"]]
    assert "Beta's biology" in titles
    assert "Alpha's addition" not in titles


@pytest.mark.asyncio
async def test_child_scoped_token_cannot_read_siblings_dashboard(
    client, db_session, household, user, child, second_child
):
    """The bound-child guard already rejects cross-child reads; pin it
    here because this file is where the sibling boundary is tested."""
    await _seed_today_activity(db_session, household, user, second_child.id, "Beta's biology")
    _kid_cookie(client, user, household, child.id)
    resp = await client.get(f"/api/v1/children/{second_child.id}/dashboard")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_parent_session_sees_the_scoped_today_too(auth_client, db_session, household, user, child, second_child):
    """The same scoping holds for parent-session reads of the kid
    dashboard: the response is about THIS child, not the household."""
    await _seed_today_activity(db_session, household, user, child.id, "Alpha's addition")
    await _seed_today_activity(db_session, household, user, second_child.id, "Beta's biology")

    resp = await auth_client.get(f"/api/v1/children/{child.id}/dashboard")
    assert resp.status_code == 200, resp.text
    titles = [a["title"] for a in resp.json()["today"]["activities"]]
    assert titles == ["Alpha's addition"]
