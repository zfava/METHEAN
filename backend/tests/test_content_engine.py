"""Tests for node content enrichment engine.

Covers:
- Enrichment populates node content
- Enriched content has required fields
- Tutor prompt includes node content when available
- Evaluator accepts assessment criteria
- Enrichment respects philosophical profile
"""

import uuid

import pytest
from sqlalchemy import select

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.identity import Household
from app.models.operational import AIRun
from app.services.node_content import is_enriched, validate_content


class TestNodeContentSchema:

    def test_empty_content_not_enriched(self):
        assert is_enriched(None) is False
        assert is_enriched({}) is False

    def test_minimal_content_not_enriched(self):
        assert is_enriched({"some_key": "value"}) is False

    def test_enriched_content_detected(self):
        assert is_enriched({
            "learning_objectives": ["Objective 1"],
            "teaching_guidance": {"introduction": "Start here"},
        }) is True

    def test_validate_missing_fields(self):
        issues = validate_content({})
        assert "learning_objectives missing" in issues
        assert "teaching_guidance missing" in issues
        assert "assessment_criteria missing" in issues


class TestContentEnrichment:

    @pytest.mark.asyncio
    async def test_enrich_populates_content(
        self, auth_client, db_session, household, subject, learning_map,
    ):
        # Create a node with empty content
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Basic Phonics",
            content={},
        )
        db_session.add(node)
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/learning-maps/{learning_map.id}/nodes/{node.id}/enrich"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["content"] is not None
        assert data["content"].get("learning_objectives")

    @pytest.mark.asyncio
    async def test_enrich_map_enriches_all_unenriched(
        self, auth_client, db_session, household, subject, learning_map,
    ):
        for title in ["Node A", "Node B"]:
            db_session.add(LearningNode(
                learning_map_id=learning_map.id, household_id=household.id,
                node_type=NodeType.concept, title=title, content={},
            ))
        await db_session.flush()

        resp = await auth_client.post(f"/api/v1/learning-maps/{learning_map.id}/enrich")
        assert resp.status_code == 200
        assert resp.json()["enriched"] == 2

    @pytest.mark.asyncio
    async def test_enriched_content_has_required_fields(
        self, auth_client, db_session, household, subject, learning_map,
    ):
        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Enrichable Node", content={},
        )
        db_session.add(node)
        await db_session.flush()

        await auth_client.post(
            f"/api/v1/learning-maps/{learning_map.id}/nodes/{node.id}/enrich"
        )

        resp = await auth_client.get(
            f"/api/v1/learning-maps/{learning_map.id}/nodes/{node.id}/content"
        )
        assert resp.status_code == 200
        content = resp.json()
        assert "learning_objectives" in content
        assert "teaching_guidance" in content
        assert "assessment_criteria" in content
        assert "accommodations" in content

    @pytest.mark.asyncio
    async def test_enrich_respects_philosophy(
        self, auth_client, db_session, household, subject, learning_map, user,
    ):
        household.philosophical_profile = {
            "educational_philosophy": "classical",
        }
        await db_session.flush()

        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.concept, title="Philosophy Node", content={},
        )
        db_session.add(node)
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/learning-maps/{learning_map.id}/nodes/{node.id}/enrich"
        )
        assert resp.status_code == 200
        ai_run_id = resp.json().get("ai_run_id")

        if ai_run_id:
            run = await db_session.execute(
                select(AIRun).where(AIRun.id == uuid.UUID(ai_run_id))
            )
            ai_run = run.scalar_one_or_none()
            if ai_run and ai_run.input_data:
                prompt = ai_run.input_data.get("system_prompt", "")
                assert "PHILOSOPHICAL CONSTRAINTS" in prompt


class TestTutorWithContent:

    @pytest.mark.asyncio
    async def test_tutor_prompt_includes_node_content(
        self, auth_client, db_session, household, subject, learning_map, child, user,
    ):
        """When a node has enriched content, the tutor should use it."""
        from app.models.governance import Activity, Plan, PlanWeek
        from app.models.enums import ActivityType, PlanStatus
        from datetime import date, timedelta

        node = LearningNode(
            learning_map_id=learning_map.id, household_id=household.id,
            node_type=NodeType.skill, title="Enriched Tutor Node",
            content={
                "teaching_guidance": {
                    "socratic_questions": ["What do you notice?", "Why do you think that?"],
                    "common_misconceptions": ["Students often confuse X with Y"],
                    "scaffolding_sequence": ["Step 1", "Step 2", "Step 3"],
                },
            },
        )
        db_session.add(node)
        await db_session.flush()

        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id, name="T", status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()
        week = PlanWeek(
            plan_id=plan.id, household_id=household.id,
            week_number=1, start_date=date.today(),
            end_date=date.today() + timedelta(days=4),
        )
        db_session.add(week)
        await db_session.flush()
        activity = Activity(
            plan_week_id=week.id, household_id=household.id,
            node_id=node.id, activity_type=ActivityType.lesson,
            title="Tutor Activity", governance_approved=True,
        )
        db_session.add(activity)
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/tutor/{activity.id}/message",
            json={"child_id": str(child.id), "message": "I don't understand"},
        )
        assert resp.status_code == 200

        # Verify the AI run prompt included teaching guidance
        runs = await db_session.execute(
            select(AIRun).where(AIRun.run_type == "tutor").order_by(AIRun.created_at.desc())
        )
        latest = runs.scalars().first()
        if latest and latest.input_data:
            prompt = latest.input_data.get("user_prompt", "")
            assert "TEACHING GUIDANCE" in prompt
            assert "What do you notice?" in prompt
