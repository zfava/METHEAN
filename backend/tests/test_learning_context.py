"""Tests for learning context endpoint and service.

Covers:
- Learn endpoint returns structured lesson content
- Learn endpoint generates content for unenriched nodes
- Attempt stores responses and self_reflection in feedback
- Tutor messages are contextual to the activity
"""

import uuid
from datetime import UTC, date, datetime

import pytest
from sqlalchemy import select

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AttemptStatus,
    MasteryLevel,
    NodeType,
    PlanStatus,
)
from app.models.governance import Activity, Attempt, Plan, PlanWeek
from app.services.learning_context import get_activity_learning_context


class TestLearningContext:

    @pytest.mark.asyncio
    async def test_learn_returns_lesson_content(
        self, db_session, household, child, user, subject, learning_map,
    ):
        """Call learning context for an activity with enriched node, verify content returned."""
        # Create an enriched node
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Double-Digit Addition",
            content={
                "learning_objectives": ["Add two-digit numbers", "Carry over tens"],
                "teaching_guidance": {
                    "introduction": "Today we learn to add bigger numbers!",
                    "practice_activities": ["Solve 23 + 45", "Solve 37 + 18"],
                    "common_misconceptions": ["Forgetting to carry the ten"],
                    "scaffolding_sequence": ["Start with no carrying", "Introduce carrying"],
                    "socratic_questions": ["What happens when digits add to more than 9?"],
                    "real_world_connections": ["Adding prices at the store"],
                },
                "assessment_criteria": {
                    "mastery_indicators": ["Correctly adds with carrying"],
                    "sample_assessment_prompts": ["What is 48 + 35?"],
                    "assessment_methods": ["written work"],
                },
                "resource_guidance": {"required": ["pencil", "paper"], "recommended": ["base-10 blocks"]},
                "time_estimates": {"first_exposure": 30, "practice_session": 20},
            },
        )
        db_session.add(node)
        await db_session.flush()

        # Create plan/week/activity linked to node
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            node_id=node.id, activity_type=ActivityType.lesson,
            title="Double-Digit Addition Lesson",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Get learning context
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id,
        )

        assert ctx["activity"]["title"] == "Double-Digit Addition Lesson"
        assert ctx["activity"]["activity_type"] == "lesson"
        assert ctx["tutor_available"] is True

        # Lesson content
        assert "Today we learn" in ctx["lesson"]["introduction"]
        assert len(ctx["lesson"]["objectives"]) == 2
        assert len(ctx["lesson"]["steps"]) > 0
        assert any(s["type"] == "read" for s in ctx["lesson"]["steps"])
        assert len(ctx["lesson"]["practice_prompts"]) > 0
        assert "pencil" in ctx["lesson"]["resources_needed"]
        assert "store" in ctx["lesson"]["real_world_connection"]

        # Assessment
        assert len(ctx["assessment"]["prompts"]) > 0
        assert "carrying" in ctx["assessment"]["mastery_criteria"]

    @pytest.mark.asyncio
    async def test_learn_with_unenriched_node(
        self, db_session, household, child, user, subject, learning_map,
    ):
        """Activity with unenriched node still returns basic structure."""
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Fractions",
            content={},  # Not enriched
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            node_id=node.id, activity_type=ActivityType.practice,
            title="Fractions Practice",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id,
        )

        # Fallback content should be generated from node title
        assert ctx["activity"]["title"] == "Fractions Practice"
        assert ctx["activity"]["activity_type"] == "practice"
        assert "Fractions" in ctx["lesson"]["introduction"]
        assert len(ctx["lesson"]["objectives"]) >= 2
        assert len(ctx["lesson"]["steps"]) > 0
        assert len(ctx["assessment"]["prompts"]) > 0
        assert "Fractions" in ctx["assessment"]["prompts"][0]

    @pytest.mark.asyncio
    async def test_learn_no_tutor_for_assessment(
        self, db_session, household, child, user, subject, learning_map,
    ):
        """Assessment activities should not have tutor available."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            activity_type=ActivityType.assessment,
            title="Weekly Assessment",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id,
        )
        assert ctx["tutor_available"] is False

    @pytest.mark.asyncio
    async def test_previous_attempts_returned(
        self, db_session, household, child, user, subject, learning_map,
    ):
        """Previous attempts for the same activity are returned."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            activity_type=ActivityType.lesson, title="Test",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Add a previous attempt
        db_session.add(Attempt(
            activity_id=activity.id, household_id=household.id,
            child_id=child.id, status=AttemptStatus.completed,
            completed_at=datetime.now(UTC), duration_minutes=20, score=0.8,
        ))
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id,
        )
        assert len(ctx["previous_attempts"]) == 1
        assert ctx["previous_attempts"][0]["duration_minutes"] == 20


class TestAttemptFeedback:

    @pytest.mark.asyncio
    async def test_attempt_stores_responses_in_feedback(
        self, db_session, household, child, user, subject, learning_map,
    ):
        """Submit attempt with responses and self_reflection, verify stored in feedback."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            activity_type=ActivityType.lesson, title="Test",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        attempt = Attempt(
            activity_id=activity.id, household_id=household.id,
            child_id=child.id, status=AttemptStatus.started,
            feedback={
                "responses": [
                    {"prompt": "What is 3+4?", "response": "7"},
                    {"prompt": "Spell 'cat'", "response": "c-a-t"},
                ],
                "self_reflection": "I thought the math was easy but spelling was harder.",
            },
        )
        db_session.add(attempt)
        await db_session.flush()

        # Verify feedback stored
        result = await db_session.execute(
            select(Attempt).where(Attempt.id == attempt.id)
        )
        saved = result.scalar_one()
        assert len(saved.feedback["responses"]) == 2
        assert saved.feedback["responses"][0]["prompt"] == "What is 3+4?"
        assert saved.feedback["responses"][0]["response"] == "7"
        assert "spelling was harder" in saved.feedback["self_reflection"]


class TestLearningContextAPI:

    @pytest.mark.asyncio
    async def test_learn_endpoint(self, auth_client, db_session, household, child, user, subject, learning_map):
        """Test the /activities/{id}/learn API endpoint."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            activity_type=ActivityType.lesson, title="API Test Lesson",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        resp = await auth_client.get(f"/api/v1/activities/{activity.id}/learn")
        assert resp.status_code == 200
        data = resp.json()
        assert data["activity"]["title"] == "API Test Lesson"
        assert data["activity"]["activity_type"] == "lesson"
        assert "lesson" in data
        assert "assessment" in data
        assert data["tutor_available"] is True


class TestTutorConversationHistory:

    @pytest.mark.asyncio
    async def test_tutor_with_history(self, auth_client, db_session, household, child, user, subject, learning_map):
        """Send a tutor message with conversation history, verify it's accepted."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            activity_type=ActivityType.lesson, title="Addition",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Send with conversation history
        resp = await auth_client.post(
            f"/api/v1/tutor/{activity.id}/message",
            json={
                "message": "Why?",
                "conversation_history": [
                    {"role": "child", "text": "What is 3 + 4?"},
                    {"role": "tutor", "text": "What do you think happens when you add 3 and 4?"},
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data

    @pytest.mark.asyncio
    async def test_tutor_without_history(self, auth_client, db_session, household, child, user, subject, learning_map):
        """Send a tutor message without history (backward compatible)."""
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="Math", status=PlanStatus.active,
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
            activity_type=ActivityType.lesson, title="Addition",
            status=ActivityStatus.scheduled, governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        # Send without history (no conversation_history field)
        resp = await auth_client.post(
            f"/api/v1/tutor/{activity.id}/message",
            json={"message": "What is 3 + 4?"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
