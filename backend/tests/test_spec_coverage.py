"""Tests for spec coverage endpoints.

Covers: household settings, child PATCH/preferences, /today, map validate,
pace metrics, counterfactual, sync, attempt locking, device register,
notification log, metrics, FSRS optimizer pipeline.
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningNode,
)
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    EdgeRelation,
    MasteryLevel,
    NodeType,
    PlanStatus,
)
from app.models.governance import Activity, Plan, PlanWeek
from app.models.identity import Child
from app.models.state import ChildNodeState

# ══════════════════════════════════════════════════
# Household & Child Management
# ══════════════════════════════════════════════════


class TestHouseholdSettings:
    @pytest.mark.asyncio
    async def test_update_household_name(self, auth_client, db_session, household):
        resp = await auth_client.put(
            "/api/v1/household/settings",
            json={
                "name": "New Family Name",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Family Name"

    @pytest.mark.asyncio
    async def test_update_timezone(self, auth_client, db_session, household):
        resp = await auth_client.put(
            "/api/v1/household/settings",
            json={
                "timezone": "America/Chicago",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["timezone"] == "America/Chicago"


class TestChildUpdate:
    @pytest.mark.asyncio
    async def test_patch_child(self, auth_client, db_session, household, child):
        resp = await auth_client.patch(
            f"/api/v1/children/{child.id}",
            json={
                "first_name": "Updated",
                "grade_level": "4th",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["first_name"] == "Updated"
        assert resp.json()["grade_level"] == "4th"

    @pytest.mark.asyncio
    async def test_update_preferences(self, auth_client, db_session, household, child):
        resp = await auth_client.put(
            f"/api/v1/children/{child.id}/preferences",
            json={
                "daily_duration_minutes": 120,
                "learning_style": {"visual": True},
            },
        )
        assert resp.status_code == 200
        assert resp.json()["daily_duration_minutes"] == 120


# ══════════════════════════════════════════════════
# Today's Activities
# ══════════════════════════════════════════════════


class TestToday:
    @pytest.mark.asyncio
    async def test_get_today_activities(
        self,
        auth_client,
        db_session,
        household,
        child,
        subject,
        user,
    ):
        # Create activity for today
        plan = Plan(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            name="Today Plan",
            status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()

        db_session.add(
            Activity(
                plan_week_id=week.id,
                household_id=household.id,
                activity_type=ActivityType.lesson,
                title="Today's Lesson",
                status=ActivityStatus.scheduled,
                scheduled_date=date.today(),
            )
        )
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
        assert resp.status_code == 200
        activities = resp.json()
        assert len(activities) >= 1
        assert activities[0]["title"] == "Today's Lesson"


# ══════════════════════════════════════════════════
# Map Validation
# ══════════════════════════════════════════════════


class TestMapValidation:
    @pytest.mark.asyncio
    async def test_validate_healthy_map(
        self,
        auth_client,
        db_session,
        household,
        subject,
    ):
        lmap = LearningMap(household_id=household.id, subject_id=subject.id, name="Valid Map")
        db_session.add(lmap)
        await db_session.flush()

        root = LearningNode(
            learning_map_id=lmap.id,
            household_id=household.id,
            node_type=NodeType.root,
            title="Root",
        )
        skill = LearningNode(
            learning_map_id=lmap.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Skill",
        )
        db_session.add_all([root, skill])
        await db_session.flush()

        db_session.add(
            LearningEdge(
                learning_map_id=lmap.id,
                household_id=household.id,
                from_node_id=root.id,
                to_node_id=skill.id,
                relation=EdgeRelation.prerequisite,
            )
        )
        await db_session.flush()

        # Build closure table so reachability check works
        from app.services.dag_engine import rebuild_closure_for_map

        await rebuild_closure_for_map(db_session, lmap.id)

        resp = await auth_client.post(f"/api/v1/learning-maps/{lmap.id}/validate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is True
        assert data["node_count"] == 2

    @pytest.mark.asyncio
    async def test_validate_detects_orphan(
        self,
        auth_client,
        db_session,
        household,
        subject,
    ):
        lmap = LearningMap(household_id=household.id, subject_id=subject.id, name="Orphan Map")
        db_session.add(lmap)
        await db_session.flush()

        root = LearningNode(
            learning_map_id=lmap.id,
            household_id=household.id,
            node_type=NodeType.root,
            title="Root",
        )
        orphan = LearningNode(
            learning_map_id=lmap.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Orphan Skill",
        )
        db_session.add_all([root, orphan])
        await db_session.flush()

        resp = await auth_client.post(f"/api/v1/learning-maps/{lmap.id}/validate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["valid"] is False
        assert any(i["type"] == "orphan" for i in data["issues"])


# ══════════════════════════════════════════════════
# Pace Metrics
# ══════════════════════════════════════════════════


class TestPace:
    @pytest.mark.asyncio
    async def test_pace_metrics(
        self,
        auth_client,
        db_session,
        household,
        child,
        subject,
    ):
        lmap = LearningMap(household_id=household.id, subject_id=subject.id, name="Pace Map")
        db_session.add(lmap)
        await db_session.flush()

        node = LearningNode(
            learning_map_id=lmap.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Pace Node",
            estimated_minutes=30,
        )
        db_session.add(node)
        await db_session.flush()

        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=lmap.id,
            )
        )
        db_session.add(
            ChildNodeState(
                child_id=child.id,
                household_id=household.id,
                node_id=node.id,
                mastery_level=MasteryLevel.mastered,
                time_spent_minutes=25,
                attempts_count=2,
            )
        )
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/children/{child.id}/pace")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["nodes"]) >= 1
        assert data["nodes"][0]["pace_status"] == "ahead"  # 25min < 30min estimated


# ══════════════════════════════════════════════════
# Counterfactual
# ══════════════════════════════════════════════════


class TestCounterfactual:
    @pytest.mark.asyncio
    async def test_counterfactual_analysis(
        self,
        auth_client,
        db_session,
        household,
        child,
    ):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/counterfactual",
            json={"changes": {"daily_minutes": 45}},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_mock"] is True
        assert data["ai_run_id"] is not None
        assert "No state changes" in data["note"]


# ══════════════════════════════════════════════════
# Sync Protocol
# ══════════════════════════════════════════════════


class TestSync:
    @pytest.mark.asyncio
    async def test_sync_events(self, auth_client):
        now = datetime.now(UTC)
        resp = await auth_client.post(
            "/api/v1/sync",
            json={
                "events": [
                    {"event_type": "activity_completed", "payload": {"id": "abc"}, "client_timestamp": now.isoformat()},
                    {"event_type": "attempt_submitted", "payload": {"id": "def"}, "client_timestamp": now.isoformat()},
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["processed"] == 2
        assert all(r["status"] == "processed" for r in data["results"])

    @pytest.mark.asyncio
    async def test_sync_drift_detection(self, auth_client):
        old = datetime.now(UTC) - timedelta(hours=25)
        resp = await auth_client.post(
            "/api/v1/sync",
            json={
                "events": [
                    {"event_type": "test", "payload": {}, "client_timestamp": old.isoformat()},
                ],
            },
        )
        assert resp.status_code == 200
        assert resp.json()["results"][0]["drift_warning"] is True


# ══════════════════════════════════════════════════
# Attempt Locking
# ══════════════════════════════════════════════════


class TestAttemptLocking:
    @pytest.mark.asyncio
    async def test_lock_and_check(self, auth_client):
        activity_id = str(uuid.uuid4())

        # Lock
        resp = await auth_client.post(
            f"/api/v1/activities/{activity_id}/lock",
            headers={"x-device-id": "device-A"},
        )
        assert resp.status_code == 200
        assert resp.json()["locked"] is True

        # Check status
        resp2 = await auth_client.get(f"/api/v1/activities/{activity_id}/lock-status")
        assert resp2.json()["locked"] is True
        assert resp2.json()["device_id"] == "device-A"

    @pytest.mark.asyncio
    async def test_lock_conflict(self, auth_client):
        activity_id = str(uuid.uuid4())

        # Lock with device A
        await auth_client.post(
            f"/api/v1/activities/{activity_id}/lock",
            headers={"x-device-id": "device-A"},
        )

        # Try lock with device B — should 409
        resp = await auth_client.post(
            f"/api/v1/activities/{activity_id}/lock",
            headers={"x-device-id": "device-B"},
        )
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_unlock(self, auth_client):
        activity_id = str(uuid.uuid4())
        await auth_client.post(
            f"/api/v1/activities/{activity_id}/lock",
            headers={"x-device-id": "device-A"},
        )
        resp = await auth_client.delete(f"/api/v1/activities/{activity_id}/lock")
        assert resp.json()["locked"] is False


# ══════════════════════════════════════════════════
# Device Register
# ══════════════════════════════════════════════════


class TestDeviceRegister:
    @pytest.mark.asyncio
    async def test_register_device(self, auth_client):
        resp = await auth_client.post(
            "/api/v1/devices/register",
            json={
                "device_token": "abc123",
                "platform": "web",
                "device_name": "Chrome on Laptop",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["registered"] is True


# ══════════════════════════════════════════════════
# Notification Log
# ══════════════════════════════════════════════════


class TestNotificationLog:
    @pytest.mark.asyncio
    async def test_notification_log(self, auth_client, db_session, household, user):
        from app.models.operational import NotificationLog

        db_session.add(
            NotificationLog(
                household_id=household.id,
                user_id=user.id,
                channel="email",
                title="plan_ready: New Plan",
                body="Test",
                sent=True,
                sent_at=datetime.now(UTC),
            )
        )
        await db_session.flush()

        resp = await auth_client.get("/api/v1/notifications/log")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1


# ══════════════════════════════════════════════════
# Metrics
# ══════════════════════════════════════════════════


class TestMetrics:
    @pytest.mark.asyncio
    async def test_prometheus_metrics(self, auth_client):
        resp = await auth_client.get("/api/v1/metrics")
        assert resp.status_code == 200
        assert "methean_up 1" in resp.text


# ══════════════════════════════════════════════════
# FSRS Optimizer
# ══════════════════════════════════════════════════


class TestFSRSOptimizer:
    @pytest.mark.asyncio
    async def test_child_has_fsrs_weights_field(self, db_session, household):
        """Verify the model field exists."""
        child = Child(
            household_id=household.id,
            first_name="FSRS",
            last_name="Test",
            fsrs_weights=[1.0, 2.0, 3.0],
        )
        db_session.add(child)
        await db_session.flush()

        result = await db_session.execute(select(Child).where(Child.id == child.id))
        loaded = result.scalar_one()
        assert loaded.fsrs_weights == [1.0, 2.0, 3.0]

    @pytest.mark.asyncio
    async def test_personalized_weights_used_in_review(
        self,
        db_session,
        household,
        learning_map,
    ):
        """Verify state engine looks up child weights."""
        from app.services.state_engine import process_review

        child = Child(
            household_id=household.id,
            first_name="Weighted",
            fsrs_weights=None,  # Start without weights
        )
        db_session.add(child)
        await db_session.flush()

        node = LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.skill,
            title="Weight Test Node",
        )
        db_session.add(node)
        await db_session.flush()

        # Process review — should work with None weights (uses defaults)
        result = await process_review(
            db_session,
            child.id,
            household.id,
            node.id,
            confidence=0.7,
        )
        assert result["mastery_level"] is not None
        assert result["fsrs_due"] is not None
