"""Tests for Celery email tasks."""

from datetime import date
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household, User, Child
from app.models.governance import Activity
from app.models.enums import ActivityStatus
from app.core.security import hash_password


@pytest_asyncio.fixture
async def task_household(db_session: AsyncSession) -> Household:
    h = Household(name="Task Test Family", timezone="America/New_York")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def task_user(db_session: AsyncSession, task_household: Household) -> User:
    u = User(
        household_id=task_household.id,
        email="tasks@test.com",
        password_hash=hash_password("testpass"),
        display_name="Task Parent",
        role="owner",
        notification_preferences={
            "email_daily_summary": True,
            "email_milestones": True,
            "email_governance_alerts": True,
            "email_weekly_digest": True,
            "email_compliance_warnings": True,
        },
    )
    db_session.add(u)
    await db_session.flush()
    return u


@pytest_asyncio.fixture
async def task_child(db_session: AsyncSession, task_household: Household) -> Child:
    c = Child(household_id=task_household.id, first_name="TaskChild")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest.mark.asyncio
@patch("app.services.notifications._is_quiet_hours", return_value=False)
@patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True)
async def test_notification_sends_email_for_high_priority(mock_email, mock_quiet, db_session, task_household, task_user):
    """High-priority notifications trigger email delivery."""
    from app.services.notifications import send_notification
    await send_notification(
        db_session, task_household.id, task_user.id,
        event_type="node_mastered",
        title="Emma mastered Fractions",
        body="Celebration!",
        timezone=task_household.timezone,
    )
    mock_email.assert_called_once()
    assert mock_email.call_args[0][0] == "tasks@test.com"


@pytest.mark.asyncio
@patch("app.services.notifications._is_quiet_hours", return_value=False)
@patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True)
async def test_notification_respects_preferences(mock_email, mock_quiet, db_session, task_household, task_user):
    """Disabled preference prevents email."""
    task_user.notification_preferences = {"email_milestones": False}
    await db_session.flush()

    from app.services.notifications import send_notification
    await send_notification(
        db_session, task_household.id, task_user.id,
        event_type="node_mastered",
        title="Emma mastered something",
        body="Body",
        timezone=task_household.timezone,
    )
    mock_email.assert_not_called()


@pytest.mark.asyncio
@patch("app.services.notifications._is_quiet_hours", return_value=False)
@patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True)
async def test_notification_governance_alert_sends_email(mock_email, mock_quiet, db_session, task_household, task_user):
    """Governance alerts trigger email."""
    from app.services.notifications import send_notification
    await send_notification(
        db_session, task_household.id, task_user.id,
        event_type="review_needed",
        title="Review needed",
        body="An activity needs your review.",
        timezone=task_household.timezone,
    )
    mock_email.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.notifications._is_quiet_hours", return_value=False)
@patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True)
async def test_notification_low_priority_no_email(mock_email, mock_quiet, db_session, task_household, task_user):
    """Low-priority notifications don't trigger email."""
    from app.services.notifications import send_notification
    await send_notification(
        db_session, task_household.id, task_user.id,
        event_type="plan_ready",
        title="Plan ready",
        body="Your plan is ready.",
        timezone=task_household.timezone,
    )
    mock_email.assert_not_called()
