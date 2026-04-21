"""Tests for activity feedback and reading log.

Covers:
- Create feedback on activity, retrieve it
- Recent feedback for a child
- Create reading entry, update progress, complete
- Reading stats calculation
"""

from datetime import date

import pytest
from sqlalchemy import select

from app.models.enums import ActivityStatus, ActivityType, PlanStatus
from app.models.evidence import ActivityFeedback, ReadingLogEntry
from app.models.governance import Activity, Plan, PlanWeek


class TestActivityFeedback:
    @pytest.mark.asyncio
    async def test_create_and_retrieve_feedback(self, db_session, household, child, user):
        """Parent posts feedback, verify it's retrievable."""
        plan = Plan(
            household_id=household.id, child_id=child.id, created_by=user.id, name="T", status=PlanStatus.active
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="Roman History",
            status=ActivityStatus.completed,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        fb = ActivityFeedback(
            household_id=household.id,
            activity_id=activity.id,
            child_id=child.id,
            author_id=user.id,
            message="Your narration was excellent! Try to include dates next time.",
            feedback_type="praise",
        )
        db_session.add(fb)
        await db_session.flush()

        result = await db_session.execute(select(ActivityFeedback).where(ActivityFeedback.activity_id == activity.id))
        feedbacks = result.scalars().all()
        assert len(feedbacks) == 1
        assert "narration was excellent" in feedbacks[0].message
        assert feedbacks[0].feedback_type == "praise"

    @pytest.mark.asyncio
    async def test_recent_feedback_for_child(self, db_session, household, child, user):
        """Multiple feedbacks across activities, retrieved by child."""
        plan = Plan(
            household_id=household.id, child_id=child.id, created_by=user.id, name="T", status=PlanStatus.active
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()

        for title in ["Math", "Reading", "Science"]:
            act = Activity(
                plan_week_id=week.id,
                household_id=household.id,
                activity_type=ActivityType.lesson,
                title=title,
                status=ActivityStatus.completed,
                governance_approved=True,
            )
            db_session.add(act)
            await db_session.flush()
            db_session.add(
                ActivityFeedback(
                    household_id=household.id,
                    activity_id=act.id,
                    child_id=child.id,
                    author_id=user.id,
                    message=f"Good work on {title}!",
                )
            )
        await db_session.flush()

        result = await db_session.execute(
            select(ActivityFeedback)
            .where(ActivityFeedback.child_id == child.id)
            .order_by(ActivityFeedback.created_at.desc())
        )
        all_fb = result.scalars().all()
        assert len(all_fb) == 3


class TestReadingLog:
    @pytest.mark.asyncio
    async def test_create_reading_entry(self, db_session, household, child, user):
        """Add a book, verify it appears."""
        entry = ReadingLogEntry(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            book_title="Charlotte's Web",
            book_author="E.B. White",
            genre="fiction",
            subject_area="literature",
            status="reading",
            pages_total=184,
            pages_read=50,
            started_date=date(2026, 9, 1),
        )
        db_session.add(entry)
        await db_session.flush()

        result = await db_session.execute(select(ReadingLogEntry).where(ReadingLogEntry.child_id == child.id))
        entries = result.scalars().all()
        assert len(entries) == 1
        assert entries[0].book_title == "Charlotte's Web"
        assert entries[0].pages_read == 50

    @pytest.mark.asyncio
    async def test_update_reading_progress(self, db_session, household, child, user):
        """Update pages_read, verify progress changes."""
        entry = ReadingLogEntry(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            book_title="Test Book",
            status="reading",
            pages_total=100,
            pages_read=25,
        )
        db_session.add(entry)
        await db_session.flush()

        entry.pages_read = 75
        entry.narration = "The hero found the treasure."
        await db_session.flush()

        await db_session.refresh(entry)
        assert entry.pages_read == 75
        assert entry.narration == "The hero found the treasure."

    @pytest.mark.asyncio
    async def test_complete_book(self, db_session, household, child, user):
        """Mark complete, verify completed_date set."""
        entry = ReadingLogEntry(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            book_title="Finished Book",
            status="reading",
            pages_total=200,
            pages_read=200,
        )
        db_session.add(entry)
        await db_session.flush()

        entry.status = "completed"
        entry.completed_date = date.today()
        entry.child_rating = 4
        await db_session.flush()

        await db_session.refresh(entry)
        assert entry.status == "completed"
        assert entry.completed_date == date.today()
        assert entry.child_rating == 4

    @pytest.mark.asyncio
    async def test_reading_stats(self, db_session, household, child, user):
        """Add multiple books, verify stats."""
        for title, genre, status, pages in [
            ("Book A", "fiction", "completed", 150),
            ("Book B", "nonfiction", "completed", 200),
            ("Book C", "fiction", "reading", 100),
            ("Book D", "poetry", "to_read", None),
        ]:
            db_session.add(
                ReadingLogEntry(
                    household_id=household.id,
                    child_id=child.id,
                    created_by=user.id,
                    book_title=title,
                    genre=genre,
                    status=status,
                    pages_total=pages,
                    pages_read=pages if status == "completed" else (50 if status == "reading" else 0),
                    minutes_spent=120 if status == "completed" else (30 if status == "reading" else 0),
                )
            )
        await db_session.flush()

        result = await db_session.execute(select(ReadingLogEntry).where(ReadingLogEntry.child_id == child.id))
        entries = result.scalars().all()
        assert len(entries) == 4

        total = len(entries)
        completed = sum(1 for e in entries if e.status == "completed")
        pages = sum(e.pages_read or 0 for e in entries)

        assert total == 4
        assert completed == 2
        assert pages == 400  # 150 + 200 + 50 + 0


class TestFeedbackAPI:
    @pytest.mark.asyncio
    async def test_feedback_api_create_and_list(self, auth_client, db_session, household, child, user):
        """Test feedback creation and listing via API."""
        plan = Plan(
            household_id=household.id, child_id=child.id, created_by=user.id, name="T", status=PlanStatus.active
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id,
            household_id=household.id,
            week_number=1,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 5),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id,
            household_id=household.id,
            activity_type=ActivityType.lesson,
            title="Test",
            status=ActivityStatus.completed,
            governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Create feedback
        resp = await auth_client.post(
            f"/api/v1/activities/{activity.id}/feedback",
            json={"message": "Great work!", "child_id": str(child.id)},
        )
        assert resp.status_code == 201

        # List feedback
        resp = await auth_client.get(f"/api/v1/activities/{activity.id}/feedback")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["message"] == "Great work!"


class TestReadingLogAPI:
    @pytest.mark.asyncio
    async def test_reading_log_crud(self, auth_client, db_session, household, child):
        """Test reading log creation and listing via API."""
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/reading-log",
            json={"book_title": "Test Book", "genre": "fiction", "pages_total": 100},
        )
        assert resp.status_code == 201
        entry_id = resp.json()["id"]

        # List
        resp = await auth_client.get(f"/api/v1/children/{child.id}/reading-log")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # Stats
        resp = await auth_client.get(f"/api/v1/children/{child.id}/reading-log/stats")
        assert resp.status_code == 200
        assert resp.json()["total_books"] == 1
