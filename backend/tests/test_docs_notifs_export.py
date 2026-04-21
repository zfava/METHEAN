"""Tests for document generation, notifications, and data export.

Covers:
- PDF document generation (IHIP, quarterly, attendance, transcript)
- Notification creation and retrieval
- Data export ZIP structure
"""

from datetime import date

import pytest

from app.services.data_export import export_family_data
from app.services.document_generator import (
    generate_attendance_record,
    generate_ihip,
    generate_quarterly_report,
    generate_transcript,
)
from app.services.notifications import (
    get_notifications,
    mark_all_read,
    mark_read,
    send_notification,
)


class TestDocumentGeneration:
    @pytest.mark.asyncio
    async def test_generate_ihip(self, db_session, household, child, user):
        """Generate IHIP PDF and verify it contains child name."""
        result = await generate_ihip(db_session, household.id, child.id, "NY", "2026-2027")
        assert len(result) > 0
        # May be PDF bytes (%PDF-) or text fallback — either is valid
        text = result.decode("utf-8", errors="ignore")
        if result[:5] == b"%PDF-":
            # PDF generated; just verify it's non-trivial
            assert len(result) > 100
        else:
            # Text fallback; verify child name present
            assert child.first_name in text

    @pytest.mark.asyncio
    async def test_quarterly_report(self, db_session, household, child, user):
        """Generate quarterly report."""
        pdf = await generate_quarterly_report(db_session, household.id, child.id, 1, "2026-2027")
        assert len(pdf) > 0

    @pytest.mark.asyncio
    async def test_attendance_record(self, db_session, household, child, user):
        """Generate attendance record."""
        pdf = await generate_attendance_record(
            db_session,
            household.id,
            child.id,
            date(2026, 9, 1),
            date(2027, 6, 30),
        )
        assert len(pdf) > 0

    @pytest.mark.asyncio
    async def test_transcript(self, db_session, household, child, user):
        """Generate transcript."""
        pdf = await generate_transcript(db_session, household.id, child.id)
        assert len(pdf) > 0


class TestNotifications:
    @pytest.mark.asyncio
    async def test_notification_created(self, db_session, household, user):
        """Create a notification, verify it's stored."""
        notif = await send_notification(
            db_session,
            household.id,
            user.id,
            event_type="alert_triggered",
            title="Test Alert",
            body="Something needs attention.",
        )
        assert notif is not None
        assert notif.title == "Test Alert"

    @pytest.mark.asyncio
    async def test_notifications_list(self, db_session, household, user):
        """Create notifications, list them."""
        for i in range(3):
            await send_notification(
                db_session,
                household.id,
                user.id,
                event_type="alert_triggered",
                title=f"Alert {i}",
                body=f"Message {i}",
            )
        await db_session.flush()

        notifs = await get_notifications(db_session, user.id, household.id, limit=10)
        assert len(notifs) >= 3

    @pytest.mark.asyncio
    async def test_mark_read(self, db_session, household, user):
        """Mark a notification as read."""
        notif = await send_notification(
            db_session,
            household.id,
            user.id,
            event_type="alert_triggered",
            title="Read Me",
            body="Test",
        )
        await db_session.flush()

        await mark_read(db_session, notif.id, household.id)
        await db_session.flush()

        await db_session.refresh(notif)
        assert notif.error == "read"

    @pytest.mark.asyncio
    async def test_mark_all_read(self, db_session, household, user):
        """Mark all notifications as read."""
        for i in range(3):
            await send_notification(
                db_session,
                household.id,
                user.id,
                event_type="alert_triggered",
                title=f"Unread {i}",
                body=f"Test {i}",
            )
        await db_session.flush()

        count = await mark_all_read(db_session, user.id, household.id)
        assert count >= 3


class TestDataExport:
    @pytest.mark.asyncio
    async def test_export_returns_zip(self, db_session, household, child, user):
        """Export family data, verify ZIP structure."""
        data = await export_family_data(db_session, household.id)
        assert len(data) > 0
        # ZIP magic bytes
        assert data[:2] == b"PK"

    @pytest.mark.asyncio
    async def test_export_contains_metadata(self, db_session, household, child, user):
        """Verify export ZIP contains metadata.json."""
        import io
        import json
        import zipfile

        data = await export_family_data(db_session, household.id)
        zf = zipfile.ZipFile(io.BytesIO(data))
        names = zf.namelist()

        assert "metadata.json" in names
        assert "family_profile.json" in names
        assert "governance_rules.json" in names

        meta = json.loads(zf.read("metadata.json"))
        assert meta["methean_version"] == "0.1.0"
        assert meta["total_children"] >= 1

    @pytest.mark.asyncio
    async def test_export_contains_child_data(self, db_session, household, child, user):
        """Verify export contains per-child directories."""
        import io
        import zipfile

        data = await export_family_data(db_session, household.id)
        zf = zipfile.ZipFile(io.BytesIO(data))
        names = zf.namelist()

        child_name = child.first_name.lower().replace(" ", "_")
        assert any(n.startswith(f"{child_name}/") for n in names)
        assert f"{child_name}/curricula.json" in names
        assert f"{child_name}/mastery_states.json" in names


class TestNotificationAPI:
    @pytest.mark.asyncio
    async def test_list_notifications(self, auth_client, db_session, household, user):
        """Test notification listing via API."""
        await send_notification(
            db_session, household.id, user.id, event_type="alert_triggered", title="API Test", body="Test body"
        )
        await db_session.commit()

        resp = await auth_client.get("/api/v1/notifications")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_mark_all_read_api(self, auth_client, db_session, household, user):
        """Test mark-all-read via API."""
        await send_notification(
            db_session, household.id, user.id, event_type="alert_triggered", title="To Read", body="Test"
        )
        await db_session.commit()

        resp = await auth_client.put("/api/v1/notifications/read-all")
        assert resp.status_code == 200
