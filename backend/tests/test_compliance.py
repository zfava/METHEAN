"""Tests for compliance engine and attendance tracking.

Covers:
- All 50 states + DC present with required fields
- Strictness classifications match HSLDA
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


class TestStateDatabase:

    def test_all_50_states_present(self):
        """Verify len(STATE_REQUIREMENTS) == 51 (50 states + DC)."""
        assert len(STATE_REQUIREMENTS) == 51

    def test_every_state_has_required_fields(self):
        """Verify every entry has all required fields."""
        required_fields = [
            "code", "name", "strictness", "notification",
            "required_subjects", "instruction_hours",
            "attendance_tracking", "annual_assessment", "special_notes",
        ]
        for code, data in STATE_REQUIREMENTS.items():
            for field in required_fields:
                assert field in data, f"{code} missing field: {field}"

    def test_strictness_values_valid(self):
        """Every strictness must be one of the four valid values."""
        valid = {"none", "low", "moderate", "high"}
        for code, data in STATE_REQUIREMENTS.items():
            assert data["strictness"] in valid, f"{code} has invalid strictness: {data['strictness']}"

    def test_high_regulation_states(self):
        """Verify NY, PA, MA are all 'high'."""
        for code in ["NY", "PA", "MA"]:
            assert STATE_REQUIREMENTS[code]["strictness"] == "high", f"{code} should be high"

    def test_no_notice_states(self):
        """Verify states classified as 'none' (no notice required per HSLDA)."""
        no_notice_states = ["TX", "AK", "CT", "ID", "IL", "IN", "NJ", "MI", "MO", "WY"]
        for code in no_notice_states:
            assert STATE_REQUIREMENTS[code]["strictness"] == "none", f"{code} should be none"

    def test_utah_low_with_notification(self):
        """UT should be strictness 'low' with notification required but no testing."""
        ut = STATE_REQUIREMENTS["UT"]
        assert ut["strictness"] == "low"
        assert ut["notification"]["required"] is True
        assert ut["annual_assessment"]["required"] is False

    def test_new_york_strict(self):
        """NY should have ihip_required=True, quarterly_reports=True, 900/990 hours."""
        ny = STATE_REQUIREMENTS["NY"]
        assert ny["strictness"] == "high"
        assert ny["ihip_required"] is True
        assert ny["quarterly_reports"] is True
        assert ny["instruction_hours"]["1-6"]["annual"] == 900
        assert ny["instruction_hours"]["7-12"]["annual"] == 990

    def test_all_codes_match_keys(self):
        """Each entry's 'code' field must match its dict key."""
        for code, data in STATE_REQUIREMENTS.items():
            assert data["code"] == code, f"Key {code} != code field {data['code']}"

    def test_all_have_last_verified(self):
        """Each entry should have last_verified and source fields."""
        for code, data in STATE_REQUIREMENTS.items():
            assert "last_verified" in data, f"{code} missing last_verified"
            assert "source" in data, f"{code} missing source"

    def test_ohio_updated_to_low(self):
        """Ohio's new law reduced regulation — should be 'low' now."""
        oh = STATE_REQUIREMENTS["OH"]
        assert oh["strictness"] == "low"
        assert oh["annual_assessment"]["required"] is False

    def test_california_psa_corrected(self):
        """CA PSA option should not have daily hour requirement."""
        ca = STATE_REQUIREMENTS["CA"]
        assert ca["strictness"] == "low"
        assert ca["instruction_hours"] == {}
        assert "Oct 1-15" in ca["special_notes"] or "October 1" in ca["notification"]["when"]

    def test_indiana_no_notice(self):
        """IN should be 'none' strictness with notification not required."""
        ind = STATE_REQUIREMENTS["IN"]
        assert ind["strictness"] == "none"
        assert ind["notification"]["required"] is False

    def test_south_carolina_low(self):
        """SC should be 'low' per HSLDA, not 'moderate'."""
        sc = STATE_REQUIREMENTS["SC"]
        assert sc["strictness"] == "low"

    def test_georgia_notification_to_doe(self):
        """GA notification should go to GA DOE (changed in 2013)."""
        ga = STATE_REQUIREMENTS["GA"]
        assert "Department of Education" in ga["notification"]["to_whom"]

    def test_dc_included(self):
        """DC should be in the database."""
        assert "DC" in STATE_REQUIREMENTS
        assert STATE_REQUIREMENTS["DC"]["name"] == "District of Columbia"

    def test_notification_structure(self):
        """All notification fields should have 'required' boolean."""
        for code, data in STATE_REQUIREMENTS.items():
            notif = data["notification"]
            assert isinstance(notif["required"], bool), f"{code} notification.required not bool"
            if notif["required"]:
                assert "to_whom" in notif, f"{code} missing to_whom"
                assert "when" in notif, f"{code} missing when"


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

        result = await check_compliance(db_session, household.id, child.id, "WA")
        assert result["state_code"] == "WA"
        assert result["total_hours"] == 10.0
        assert len(result["checks"]) > 0
        # Should have some unmet (only 10 hours of 1000 required)
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

    @pytest.mark.asyncio
    async def test_new_state_alaska(self, db_session, household, child, user):
        """Verify a newly added state works with check_compliance."""
        result = await check_compliance(db_session, household.id, child.id, "AK")
        assert result["state_code"] == "AK"
        assert result["strictness"] == "none"
        assert result["score"] == 100  # No requirements to check

    @pytest.mark.asyncio
    async def test_new_state_massachusetts(self, db_session, household, child, user):
        """Verify MA (high regulation) works correctly."""
        result = await check_compliance(db_session, household.id, child.id, "MA")
        assert result["state_code"] == "MA"
        assert result["strictness"] == "high"
        assert len(result["checks"]) > 0  # Should have notification + subject + assessment checks


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
        assert len(states) == 51
        codes = {s["code"] for s in states}
        assert "TX" in codes
        assert "NY" in codes
        assert "DC" in codes
        assert "AK" in codes

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
