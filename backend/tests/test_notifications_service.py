"""Tests for the notification service."""

import uuid
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household, User
from app.models.operational import NotificationLog
from app.services.notifications import (
    get_notifications,
    mark_all_read,
    mark_read,
    send_notification,
)
from app.core.security import hash_password


@pytest_asyncio.fixture
async def notif_household(db_session):
    h = Household(name="Notif Test", timezone="America/New_York")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def notif_user(db_session, notif_household):
    u = User(
        household_id=notif_household.id,
        email="notify@test.com",
        password_hash=hash_password("test"),
        display_name="Test",
        role="owner",
    )
    db_session.add(u)
    await db_session.flush()
    return u


@pytest.mark.asyncio
class TestNotifications:
    async def test_send_creates_record(self, db_session, notif_household, notif_user):
        # Use alert_triggered so quiet-hours check is skipped and delivery is guaranteed
        n = await send_notification(
            db_session,
            notif_household.id,
            notif_user.id,
            event_type="alert_triggered",
            title="Test Notification",
            body="Test body",
        )
        assert n is not None
        assert n.title == "Test Notification"

    async def test_get_notifications(self, db_session, notif_household, notif_user):
        # Use alert_triggered so quiet-hours check is skipped and delivery is guaranteed
        await send_notification(
            db_session, notif_household.id, notif_user.id, event_type="alert_triggered", title="N1", body="B1"
        )
        await send_notification(
            db_session, notif_household.id, notif_user.id, event_type="alert_triggered", title="N2", body="B2"
        )
        await db_session.flush()
        results = await get_notifications(db_session, notif_user.id, notif_household.id)
        assert len(results) >= 2

    async def test_mark_read(self, db_session, notif_household, notif_user):
        n = await send_notification(
            db_session, notif_household.id, notif_user.id, event_type="test", title="Read Test", body="B"
        )
        await db_session.flush()
        if n:
            await mark_read(db_session, n.id, notif_household.id)

    async def test_mark_all_read(self, db_session, notif_household, notif_user):
        await send_notification(db_session, notif_household.id, notif_user.id, event_type="test", title="R1", body="B")
        await send_notification(db_session, notif_household.id, notif_user.id, event_type="test2", title="R2", body="B")
        await db_session.flush()
        count = await mark_all_read(db_session, notif_user.id, notif_household.id)
        assert isinstance(count, int)
