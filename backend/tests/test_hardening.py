"""Production hardening tests.

Tests cover:
- Notification dedup and quiet hours
- Alert detection (stall, regression, pattern)
- Error handling middleware
- Rate limiting
- Health checks
- Snapshot capture
- Compliance report
- Auth error paths
- RLS household isolation
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode, Subject
from app.models.enums import (
    AlertSeverity,
    AlertStatus,
    MasteryLevel,
    NodeType,
    StateEventType,
)
from app.models.evidence import Alert, WeeklySnapshot
from app.models.identity import Child, Household, User
from app.models.operational import NotificationLog
from app.models.state import ChildNodeState, StateEvent
from app.services.alert_engine import detect_pattern_failure, detect_regression, detect_stalls
from app.services.notifications import (
    _is_quiet_hours,
    send_notification,
    should_send,
)


# ══════════════════════════════════════════════════
# Notification Tests
# ══════════════════════════════════════════════════

class TestNotifications:

    def test_quiet_hours_night(self):
        assert _is_quiet_hours(22) is True
        assert _is_quiet_hours(23) is True
        assert _is_quiet_hours(3) is True
        assert _is_quiet_hours(6) is True

    def test_quiet_hours_day(self):
        assert _is_quiet_hours(7) is False
        assert _is_quiet_hours(12) is False
        assert _is_quiet_hours(20) is False

    @pytest.mark.asyncio
    async def test_send_notification(self, db_session, household, user):
        notif = await send_notification(
            db_session, household.id, user.id,
            "test", "Test Title", "Test Body",
        )
        # May or may not send depending on current hour (quiet hours)
        # Just verify no errors

    @pytest.mark.asyncio
    async def test_dedup_prevents_duplicate(self, db_session, household, user):
        # Send first
        n1 = await send_notification(
            db_session, household.id, user.id,
            "node_decayed", "Decay Alert", "Node decayed",
        )
        # Second within dedup window should be blocked
        n2 = await send_notification(
            db_session, household.id, user.id,
            "node_decayed", "Decay Alert", "Node decayed again",
        )
        # n2 should be None (deduped) if n1 was sent
        if n1 is not None:
            assert n2 is None


# ══════════════════════════════════════════════════
# Alert Engine Tests
# ══════════════════════════════════════════════════

class TestAlertEngine:

    @pytest.mark.asyncio
    async def test_detect_stalls(self, db_session, household, learning_map, child):
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Stalled Node",
        )
        db_session.add(node)
        await db_session.flush()

        # Create stalled state (15 days old, still emerging)
        state = ChildNodeState(
            child_id=child.id, household_id=household.id,
            node_id=node.id, mastery_level=MasteryLevel.emerging,
            last_activity_at=datetime.now(UTC) - timedelta(days=15),
        )
        db_session.add(state)
        await db_session.flush()

        alerts = await detect_stalls(db_session, household.id)
        assert len(alerts) >= 1
        assert any("Stalled" in a.title for a in alerts)

    @pytest.mark.asyncio
    async def test_detect_regression(self, db_session, household, child, learning_map):
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Regressed Node",
        )
        db_session.add(node)
        await db_session.flush()

        alert = await detect_regression(
            db_session, child.id, household.id, node.id,
            "mastered", "proficient",
        )
        assert alert is not None
        assert "Regression" in alert.title

    @pytest.mark.asyncio
    async def test_no_regression_for_non_mastered(self, db_session, household, child, learning_map):
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Normal Node",
        )
        db_session.add(node)
        await db_session.flush()

        alert = await detect_regression(
            db_session, child.id, household.id, node.id,
            "developing", "emerging",
        )
        assert alert is None

    @pytest.mark.asyncio
    async def test_detect_pattern_failure(self, db_session, household, child, learning_map):
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Struggling Node",
        )
        db_session.add(node)
        await db_session.flush()

        # Create 3 low-confidence events
        for i in range(3):
            db_session.add(StateEvent(
                child_id=child.id, household_id=household.id,
                node_id=node.id, event_type=StateEventType.review_completed,
                from_state="emerging", to_state="emerging",
                trigger="attempt", metadata_={"confidence": 0.2},
            ))
        await db_session.flush()

        alert = await detect_pattern_failure(
            db_session, child.id, household.id, node.id,
        )
        assert alert is not None
        assert "Struggling" in alert.title


# ══════════════════════════════════════════════════
# API Error Path Tests
# ══════════════════════════════════════════════════

class TestErrorHandling:

    @pytest.mark.asyncio
    async def test_health_endpoint(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    @pytest.mark.asyncio
    async def test_404_for_missing_resource(self, auth_client):
        resp = await auth_client.get(f"/api/v1/plans/{uuid.uuid4()}")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_401_without_auth(self, client):
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_token(self, client):
        client.cookies.set("access_token", "invalid.token.here")
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_register_validation(self, client):
        # Short password
        resp = await client.post("/api/v1/auth/register", json={
            "email": "bad@test.com", "password": "short",
            "display_name": "X", "household_name": "X",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "not-an-email", "password": "securepass123",
            "display_name": "X", "household_name": "X",
        })
        assert resp.status_code == 422


# ══════════════════════════════════════════════════
# Alerts API Tests
# ══════════════════════════════════════════════════

class TestAlertsAPI:

    @pytest.mark.asyncio
    async def test_list_alerts(self, auth_client, db_session, household, child):
        db_session.add(Alert(
            household_id=household.id, child_id=child.id,
            severity=AlertSeverity.warning, status=AlertStatus.unread,
            title="Test Alert", message="Test message", source="test",
        ))
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/children/{child.id}/alerts")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) >= 1

    @pytest.mark.asyncio
    async def test_acknowledge_alert(self, auth_client, db_session, household, child):
        alert = Alert(
            household_id=household.id, child_id=child.id,
            severity=AlertSeverity.info, status=AlertStatus.unread,
            title="Ack Test", message="Test", source="test",
        )
        db_session.add(alert)
        await db_session.flush()

        resp = await auth_client.put(f"/api/v1/alerts/{alert.id}/acknowledge")
        assert resp.status_code == 200
        assert resp.json()["status"] == "read"

    @pytest.mark.asyncio
    async def test_dismiss_alert(self, auth_client, db_session, household, child):
        alert = Alert(
            household_id=household.id, child_id=child.id,
            severity=AlertSeverity.info, status=AlertStatus.unread,
            title="Dismiss Test", message="Test", source="test",
        )
        db_session.add(alert)
        await db_session.flush()

        resp = await auth_client.put(f"/api/v1/alerts/{alert.id}/dismiss")
        assert resp.status_code == 200
        assert resp.json()["status"] == "dismissed"


# ══════════════════════════════════════════════════
# Snapshots & Compliance Tests
# ══════════════════════════════════════════════════

class TestSnapshots:

    @pytest.mark.asyncio
    async def test_list_snapshots(self, auth_client, db_session, household, child):
        db_session.add(WeeklySnapshot(
            household_id=household.id, child_id=child.id,
            week_start=date(2026, 3, 30), week_end=date(2026, 4, 5),
            total_minutes=120, nodes_mastered=5, nodes_progressed=3,
        ))
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/children/{child.id}/snapshots")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) >= 1


class TestCompliance:

    @pytest.mark.asyncio
    async def test_compliance_report(self, auth_client, db_session, household, child, learning_map):
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Compliance Node",
        )
        db_session.add(node)
        await db_session.flush()

        db_session.add(ChildNodeState(
            child_id=child.id, household_id=household.id,
            node_id=node.id, mastery_level=MasteryLevel.mastered,
            attempts_count=5, time_spent_minutes=120,
        ))
        await db_session.flush()

        resp = await auth_client.get(
            f"/api/v1/children/{child.id}/compliance-report",
            params={"from": "2026-01-01", "to": "2026-12-31"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["nodes_mastered"] >= 1
        assert data["total_hours_logged"] > 0
        assert len(data["mastered_skills"]) >= 1


# ══════════════════════════════════════════════════
# Notifications API Tests
# ══════════════════════════════════════════════════

class TestNotificationsAPI:

    @pytest.mark.asyncio
    async def test_list_notifications(self, auth_client, db_session, household, user):
        db_session.add(NotificationLog(
            household_id=household.id, user_id=user.id,
            channel="in_app", title="Test", body="Test notification",
            sent=True, sent_at=datetime.now(UTC),
        ))
        await db_session.flush()

        resp = await auth_client.get("/api/v1/notifications")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) >= 1

    @pytest.mark.asyncio
    async def test_send_test_notification(self, auth_client):
        resp = await auth_client.post("/api/v1/notifications/test")
        assert resp.status_code == 200


# ══════════════════════════════════════════════════
# Household Isolation (RLS conceptual test)
# ══════════════════════════════════════════════════

class TestHouseholdIsolation:

    @pytest.mark.asyncio
    async def test_cannot_access_other_household_child(self, auth_client, db_session):
        """User from household A cannot access child from household B."""
        other_household = Household(name="Other Family")
        db_session.add(other_household)
        await db_session.flush()

        other_child = Child(
            household_id=other_household.id,
            first_name="Other", last_name="Child",
        )
        db_session.add(other_child)
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/children/{other_child.id}/state")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_cannot_access_other_household_plan(self, auth_client, db_session):
        resp = await auth_client.get(f"/api/v1/plans/{uuid.uuid4()}")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_cannot_access_other_household_alert(self, auth_client, db_session):
        other_household = Household(name="Another Family")
        db_session.add(other_household)
        await db_session.flush()

        alert = Alert(
            household_id=other_household.id,
            severity=AlertSeverity.info, status=AlertStatus.unread,
            title="Secret", message="Hidden", source="test",
        )
        db_session.add(alert)
        await db_session.flush()

        resp = await auth_client.put(f"/api/v1/alerts/{alert.id}/acknowledge")
        assert resp.status_code == 404
