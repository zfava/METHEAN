"""Tests for compliance engine and attendance tracking.

Covers:
- Compliance check identifies met and unmet requirements
- Hours calculated from child node states
- Attendance counts school days from attempts
- Texas minimal requirements (strictness=none)
- New York strict requirements
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import AttemptStatus, MasteryLevel, NodeType, ActivityType, ActivityStatus, PlanStatus
from app.models.governance import Activity, Attempt, Plan, PlanWeek
from app.models.state import ChildNodeState
from app.services.compliance_engine import STATE_REQUIREMENTS, check_compliance, get_hours_breakdown
from app.services.attendance import get_attendance_record


class TestComplianceCheck:

    @pytest.mark.asyncio
    async def test_compliance_identifies_met_and_unmet(
        self, db_session, household, child, subject, learning_map, user,
    ):
        """Create a node with hours, check compliance for a state with hour requirements."""
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Reading Node",
        )
        db_session.add(node)
        await db_session.flush()
        db_session.add(ChildNodeState(
            child_id=child.id, household_id=household.id,
            node_id=node.id, mastery_level=MasteryLevel.developing,
            time_spent_minutes=600,  # 10 hours
        ))
        await db_session.flush()

        result = await check_compliance(db_session, household.id, child.id, "OH")
        assert result["state_code"] == "OH"
        assert result["total_hours"] == 10.0
        assert len(result["checks"]) > 0
        # Should have some unmet (only 10 hours of 900 required)
        statuses = {c["status"] for c in result["checks"]}
        assert "not_met" in statuses or "at_risk" in statuses or "on_track" in statuses

    @pytest.mark.asyncio
    async def test_texas_minimal(self, db_session, household, child, user):
        """Texas has no hour, testing, or reporting requirements."""
        result = await check_compliance(db_session, household.id, child.id, "TX")
        assert result["state_code"] == "TX"
        assert result["strictness"] == "none"
        # Texas requires no notification, no testing — mainly subject checks
        assert result["score"] >= 0

    @pytest.mark.asyncio
    async def test_unknown_state(self, db_session, household, child, user):
        result = await check_compliance(db_session, household.id, child.id, "XX")
        assert "error" in result


class TestHoursBreakdown:

    @pytest.mark.asyncio
    async def test_hours_from_node_states(
        self, db_session, household, child, subject, learning_map,
    ):
        for title, mins in [("Math Node", 120), ("Reading Node", 90)]:
            node = LearningNode(
                learning_map_id=learning_map.id, household_id=household.id,
                node_type=NodeType.skill, title=title,
            )
            db_session.add(node)
            await db_session.flush()
            db_session.add(ChildNodeState(
                child_id=child.id, household_id=household.id,
                node_id=node.id, time_spent_minutes=mins,
            ))
        await db_session.flush()

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        assert hours["total_hours"] == 3.5  # (120 + 90) / 60


class TestAttendance:

    @pytest.mark.asyncio
    async def test_attendance_counts_school_days(
        self, db_session, household, child, user, subject, learning_map,
    ):
        """Create attempts on specific dates, verify school days counted."""
        # Need an activity to link attempts to
        plan = Plan(household_id=household.id, child_id=child.id,
                     created_by=user.id, name="T", status=PlanStatus.active)
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(plan_id=plan.id, household_id=household.id,
                        week_number=1, start_date=date(2026, 1, 5), end_date=date(2026, 1, 9))
        db_session.add(week)
        await db_session.flush()
        activity = Activity(plan_week_id=week.id, household_id=household.id,
                            activity_type=ActivityType.lesson, title="Test",
                            status=ActivityStatus.completed, governance_approved=True)
        db_session.add(activity)
        await db_session.flush()

        # Create attempts on 3 different days
        for day_offset in [0, 1, 3]:  # Mon, Tue, Thu
            db_session.add(Attempt(
                activity_id=activity.id, household_id=household.id,
                child_id=child.id, status=AttemptStatus.completed,
                completed_at=datetime(2026, 1, 5 + day_offset, 10, 0, tzinfo=UTC),
                duration_minutes=60,
            ))
        await db_session.flush()

        record = await get_attendance_record(
            db_session, household.id, child.id,
            date(2026, 1, 5), date(2026, 1, 9),
        )
        assert record["total_school_days"] == 3

    @pytest.mark.asyncio
    async def test_attendance_has_monthly_summary(
        self, db_session, household, child, user,
    ):
        record = await get_attendance_record(
            db_session, household.id, child.id,
            date(2026, 1, 1), date(2026, 1, 31),
        )
        assert "monthly_summary" in record
        assert "daily_log" in record
        assert len(record["daily_log"]) == 31


class TestComplianceAPI:

    @pytest.mark.asyncio
    async def test_list_states(self, auth_client):
        resp = await auth_client.get("/api/v1/compliance/states")
        assert resp.status_code == 200
        states = resp.json()
        assert len(states) == 20
        codes = {s["code"] for s in states}
        assert "TX" in codes
        assert "NY" in codes

    @pytest.mark.asyncio
    async def test_state_detail(self, auth_client):
        resp = await auth_client.get("/api/v1/compliance/states/NY")
        assert resp.status_code == 200
        assert resp.json()["name"] == "New York"
        assert resp.json()["strictness"] == "high"

    @pytest.mark.asyncio
    async def test_compliance_check_api(self, auth_client, db_session, household, child):
        resp = await auth_client.get(
            f"/api/v1/children/{child.id}/compliance/check",
            params={"state": "TX"},
        )
        assert resp.status_code == 200
        assert resp.json()["state_code"] == "TX"
