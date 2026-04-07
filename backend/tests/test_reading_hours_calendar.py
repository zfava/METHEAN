"""Tests for reading log hours in compliance and activity rescheduling.

Covers:
- Reading log minutes counted in get_hours_breakdown
- Reading log "Reading (books)" appears in by_subject
- Reschedule activity creates governance event
- Curriculum notes persist via API
"""

import uuid
from datetime import date, datetime, UTC

import pytest
from sqlalchemy import select

from app.models.enums import (
    ActivityStatus, ActivityType, GovernanceAction, PlanStatus,
)
from app.models.evidence import ReadingLogEntry
from app.models.governance import Activity, GovernanceEvent, Plan, PlanWeek
from app.services.compliance_engine import get_hours_breakdown


class TestReadingLogHoursInCompliance:

    @pytest.mark.asyncio
    async def test_reading_minutes_in_total(self, db_session, household, child, user):
        """Reading log minutes_spent should be included in total_hours."""
        # Add reading entries
        db_session.add(ReadingLogEntry(
            household_id=household.id, child_id=child.id, created_by=user.id,
            book_title="Charlotte's Web", status="completed",
            minutes_spent=120,  # 2 hours
        ))
        db_session.add(ReadingLogEntry(
            household_id=household.id, child_id=child.id, created_by=user.id,
            book_title="The Lion, the Witch and the Wardrobe", status="reading",
            minutes_spent=90,  # 1.5 hours
        ))
        await db_session.flush()

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        # 120 + 90 = 210 minutes = 3.5 hours
        assert hours["total_hours"] >= 3.5

    @pytest.mark.asyncio
    async def test_reading_subject_in_breakdown(self, db_session, household, child, user):
        """'Reading (books)' should appear in by_subject."""
        db_session.add(ReadingLogEntry(
            household_id=household.id, child_id=child.id, created_by=user.id,
            book_title="Test Book", status="reading", minutes_spent=60,
        ))
        await db_session.flush()

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        assert "Reading (books)" in hours["by_subject"]
        assert hours["by_subject"]["Reading (books)"] == 1.0

    @pytest.mark.asyncio
    async def test_reading_hours_additive(self, db_session, household, child, user, subject, learning_map):
        """Reading hours should add to activity hours, not replace them."""
        from app.models.curriculum import LearningNode
        from app.models.state import ChildNodeState
        from app.models.enums import NodeType

        # Add node with activity time
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Math",
        )
        db_session.add(node)
        await db_session.flush()
        db_session.add(ChildNodeState(
            child_id=child.id, household_id=household.id,
            node_id=node.id, time_spent_minutes=60,
        ))

        # Add reading time
        db_session.add(ReadingLogEntry(
            household_id=household.id, child_id=child.id, created_by=user.id,
            book_title="History Book", status="reading", minutes_spent=60,
        ))
        await db_session.flush()

        hours = await get_hours_breakdown(db_session, household.id, child.id)
        # 60 min activity + 60 min reading = 2 hours
        assert hours["total_hours"] == 2.0


class TestRescheduleActivity:

    @pytest.mark.asyncio
    async def test_reschedule_logs_governance_event(self, auth_client, db_session, household, child, user):
        """Reschedule activity creates a governance event."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="T", status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id, household_id=household.id,
            week_number=1, start_date=date(2026, 9, 1), end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id, household_id=household.id,
            activity_type=ActivityType.lesson, title="Math Lesson",
            status=ActivityStatus.scheduled, governance_approved=True,
            scheduled_date=date(2026, 9, 1),
        )
        db_session.add(activity)
        await db_session.flush()

        # Reschedule from Monday to Wednesday
        resp = await auth_client.put(
            f"/api/v1/activities/{activity.id}/reschedule",
            json={"new_date": "2026-09-03"},
        )
        assert resp.status_code == 200
        assert resp.json()["scheduled_date"] == "2026-09-03"

        # Verify governance event
        events_result = await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.target_id == activity.id,
                GovernanceEvent.action == GovernanceAction.modify,
            )
        )
        event = events_result.scalar_one_or_none()
        assert event is not None
        assert "Rescheduled" in event.reason


class TestCurriculumNotesAPI:

    @pytest.mark.asyncio
    async def test_notes_persist_via_api(self, auth_client, db_session, household, child, user):
        """PUT notes on a week, GET the week, verify notes returned."""
        from app.models.annual_curriculum import AnnualCurriculum

        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Math", academic_year="2026-2027",
            total_weeks=4, hours_per_week=3.0,
            start_date=date(2026, 9, 1), end_date=date(2026, 10, 1),
            scope_sequence={"weeks": [{"week_number": 1, "title": "W1", "objectives": [], "suggested_activities": []}]},
            status="active", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()

        # PUT notes
        resp = await auth_client.put(
            f"/api/v1/curricula/{c.id}/weeks/1/notes",
            json={"notes": "Emma struggled with fractions this week."},
        )
        assert resp.status_code == 200

        # Verify persisted
        await db_session.refresh(c)
        assert c.actual_record["weeks"]["1"]["parent_notes"] == "Emma struggled with fractions this week."
