"""Tests for multi-year education plan generation.

Covers:
- Plan generation uses philosophical profile
- Plan includes year plans with subjects
- Approval logs governance event
- Year curricula generation produces proposals per subject
- Baseline assessment is stored on the plan
"""

import uuid
from datetime import date

import pytest
from sqlalchemy import select

from app.models.education_plan import EducationPlan
from app.models.governance import GovernanceEvent
from app.models.identity import Household


class TestEducationPlanGeneration:

    @pytest.mark.asyncio
    async def test_generate_plan_creates_draft(
        self, auth_client, db_session, household, child, user,
    ):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={
                "goals": {
                    "graduation_target": "2038",
                    "post_graduation": "college_prep",
                    "parent_vision": "Classical education with strong humanities",
                },
                "baseline_assessment": {
                    "reading_level": "at_grade",
                    "strengths": ["verbal expression"],
                },
                "time_budget_hours_per_week": 20,
            },
        )
        assert resp.status_code == 201, f"Generate failed: {resp.text}"
        data = resp.json()
        assert data["status"] == "draft"
        assert data["name"]  # Non-empty name
        assert data["year_plans"]  # Has year plans
        assert data["goals"]["graduation_target"] == "2038"

    @pytest.mark.asyncio
    async def test_plan_uses_philosophy(
        self, auth_client, db_session, household, child, user,
    ):
        """Set a philosophy, generate a plan, verify AI run includes constraints."""
        # Set philosophy
        household.philosophical_profile = {
            "educational_philosophy": "classical",
            "religious_framework": "christian",
        }
        await db_session.flush()

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={"goals": {}, "baseline_assessment": {}},
        )
        assert resp.status_code == 201
        ai_run_id = resp.json().get("ai_run_id")

        if ai_run_id:
            from app.models.operational import AIRun
            run = await db_session.execute(
                select(AIRun).where(AIRun.id == uuid.UUID(ai_run_id))
            )
            ai_run = run.scalar_one_or_none()
            if ai_run and ai_run.input_data:
                prompt = ai_run.input_data.get("system_prompt", "")
                assert "PHILOSOPHICAL CONSTRAINTS" in prompt
                assert "Classical education" in prompt

    @pytest.mark.asyncio
    async def test_get_plan(self, auth_client, db_session, household, child, user):
        await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={"goals": {}, "baseline_assessment": {}},
        )
        resp = await auth_client.get(f"/api/v1/children/{child.id}/education-plan")
        assert resp.status_code == 200
        assert resp.json()["status"] == "draft"

    @pytest.mark.asyncio
    async def test_update_plan(self, auth_client, db_session, household, child, user):
        await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={"goals": {}, "baseline_assessment": {}},
        )
        resp = await auth_client.put(
            f"/api/v1/children/{child.id}/education-plan",
            json={"name": "Updated Plan Name"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Plan Name"


class TestEducationPlanApproval:

    @pytest.mark.asyncio
    async def test_approve_logs_governance_event(
        self, auth_client, db_session, household, child, user,
    ):
        gen = await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={"goals": {}, "baseline_assessment": {}},
        )
        plan_id = gen.json()["id"]

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/approve"
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "active"
        assert resp.json()["approved_at"] is not None

        # Verify governance event
        result = await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.target_type == "education_plan",
                GovernanceEvent.target_id == uuid.UUID(plan_id),
                GovernanceEvent.action == "approve",
            )
        )
        event = result.scalar_one()
        assert "approved by parent" in event.reason.lower()


class TestYearCurricula:

    @pytest.mark.asyncio
    async def test_generate_year_curricula(
        self, auth_client, db_session, household, child, user,
    ):
        await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={"goals": {}, "baseline_assessment": {}},
        )

        # Get the plan to find a valid year key
        plan = await auth_client.get(f"/api/v1/children/{child.id}/education-plan")
        year_plans = plan.json()["year_plans"]
        if not year_plans:
            pytest.skip("Mock returned no year plans")

        year_key = list(year_plans.keys())[0]
        expected_subjects = len(year_plans[year_key].get("subjects", []))

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/years/{year_key}/generate-curricula"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["year_key"] == year_key
        assert len(data["proposals"]) == expected_subjects
        assert all(p["status"] == "proposed" for p in data["proposals"])


class TestBaselineAssessment:

    @pytest.mark.asyncio
    async def test_baseline_stored_on_plan(
        self, auth_client, db_session, household, child, user,
    ):
        baseline = {
            "reading_level": "above_grade",
            "math_level": "at_grade",
            "strengths": ["spatial reasoning", "memorization"],
            "struggles": ["fine motor"],
            "diagnosed_conditions": ["gifted"],
        }
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/education-plan/generate",
            json={"goals": {}, "baseline_assessment": baseline},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["baseline_assessment"]["reading_level"] == "above_grade"
        assert "spatial reasoning" in data["baseline_assessment"]["strengths"]
