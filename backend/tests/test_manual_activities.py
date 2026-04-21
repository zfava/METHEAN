"""Tests for manual activities, time logging, and password change."""

import pytest


class TestManualActivity:
    @pytest.mark.asyncio
    async def test_create_manual_activity(self, auth_client, db_session, household, child):
        """POST /activities creates a manual activity."""
        resp = await auth_client.post(
            "/api/v1/activities",
            json={
                "child_id": str(child.id),
                "title": "Piano lesson",
                "activity_type": "lesson",
                "scheduled_date": "2026-09-15",
                "estimated_minutes": 30,
                "subject_area": "Music",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Piano lesson"
        assert data["scheduled_date"] == "2026-09-15"

    @pytest.mark.asyncio
    async def test_manual_activity_auto_approved(self, auth_client, db_session, household, child):
        """Manual activities are auto-approved (governance_approved=True)."""
        resp = await auth_client.post(
            "/api/v1/activities",
            json={
                "child_id": str(child.id),
                "title": "Library trip",
                "activity_type": "field_trip",
                "scheduled_date": "2026-09-15",
            },
        )
        assert resp.status_code == 201
        # Activity should not appear in the approval queue
        queue_resp = await auth_client.get("/api/v1/governance/queue")
        assert queue_resp.status_code == 200
        queue_items = queue_resp.json().get("items", [])
        manual_in_queue = [i for i in queue_items if i["title"] == "Library trip"]
        assert len(manual_in_queue) == 0


class TestTimeLogging:
    @pytest.mark.asyncio
    async def test_log_time(self, auth_client, db_session, household, child):
        """POST /children/{id}/time-log creates a time entry."""
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/time-log",
            json={
                "date": "2026-09-15",
                "minutes": 45,
                "subject_area": "Music",
                "description": "Piano practice",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["minutes"] == 45
        assert data["subject"] == "Music"


class TestPasswordChange:
    @pytest.mark.asyncio
    async def test_change_password_success(self, auth_client, db_session, user):
        """PUT /auth/password with correct current password succeeds."""
        resp = await auth_client.put(
            "/api/v1/auth/password",
            json={
                "current_password": "testpass123",
                "new_password": "newpassword123",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    @pytest.mark.asyncio
    async def test_change_password_wrong_current(self, auth_client, db_session, user):
        """PUT /auth/password with wrong current password returns 400."""
        resp = await auth_client.put(
            "/api/v1/auth/password",
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
            },
        )
        assert resp.status_code == 400
        assert "incorrect" in resp.json()["detail"].lower()
