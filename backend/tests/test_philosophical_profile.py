"""Tests for household philosophical profile.

Covers:
- CRUD: create, read, update the profile
- Prompt injection: profile constraints appear in AI run input_data
- Content boundary enforcement: exclusion instructions in prompt
- Validation: invalid philosophy/stance values rejected
"""

import pytest
from sqlalchemy import select

from app.ai.prompts import build_philosophical_constraints
from app.models.operational import AIRun

# ══════════════════════════════════════════════════
# build_philosophical_constraints unit tests
# ══════════════════════════════════════════════════


class TestBuildConstraints:
    def test_empty_profile_returns_empty(self):
        assert build_philosophical_constraints(None) == ""
        assert build_philosophical_constraints({}) == ""

    def test_educational_philosophy(self):
        result = build_philosophical_constraints(
            {
                "educational_philosophy": "classical",
                "philosophy_description": "We follow the trivium",
            }
        )
        assert "Classical education" in result
        assert "trivium" in result.lower()

    def test_content_exclusion(self):
        result = build_philosophical_constraints(
            {
                "content_boundaries": [
                    {"topic": "astrology", "stance": "exclude", "notes": "Not evidence-based"},
                ],
            }
        )
        assert "CONTENT EXCLUSION" in result
        assert "astrology" in result
        assert "Not evidence-based" in result

    def test_present_alternative(self):
        result = build_philosophical_constraints(
            {
                "content_boundaries": [
                    {
                        "topic": "evolution",
                        "stance": "present_alternative",
                        "notes": "Present young-earth creationism alongside",
                    },
                ],
            }
        )
        assert "ALTERNATIVE PERSPECTIVES" in result
        assert "evolution" in result
        assert "multiple perspectives" in result.lower()

    def test_parent_led_topic(self):
        result = build_philosophical_constraints(
            {
                "content_boundaries": [
                    {"topic": "sexuality_education", "stance": "parent_led_only", "notes": ""},
                ],
            }
        )
        assert "PARENT-LED TOPIC" in result

    def test_autonomy_preview_all(self):
        result = build_philosophical_constraints(
            {
                "ai_autonomy_level": "preview_all",
            }
        )
        assert "FLAG EVERY" in result

    def test_pedagogical_preferences(self):
        result = build_philosophical_constraints(
            {
                "pedagogical_preferences": {
                    "socratic_method": True,
                    "memorization_valued": True,
                    "standardized_testing": False,
                    "competitive_grading": False,
                },
            }
        )
        assert "Socratic" in result
        assert "memorization" in result.lower()
        assert "standardized test" in result.lower()
        assert "competitive grading" in result.lower()

    def test_custom_constraints(self):
        result = build_philosophical_constraints(
            {
                "custom_constraints": [
                    "All history content should include primary sources",
                    "Latin roots in vocabulary across all subjects",
                ],
            }
        )
        assert "primary sources" in result
        assert "Latin roots" in result

    def test_religious_framework(self):
        result = build_philosophical_constraints(
            {
                "religious_framework": "christian",
                "religious_notes": "Reformed Protestant tradition",
            }
        )
        assert "christian" in result
        assert "Reformed Protestant" in result

    def test_secular_framework_omitted(self):
        result = build_philosophical_constraints(
            {
                "religious_framework": "secular",
            }
        )
        # Secular should not add religious constraint lines
        assert "Religious framework" not in result

    def test_self_governed_constraints_use_second_person(self):
        """Self-governed mode uses self-defined language and drops parent wording."""
        profile = {
            "educational_philosophy": "classical",
            "philosophy_description": "I want trivium-style depth",
            "content_boundaries": [
                {"topic": "gambling", "stance": "parent_led_only", "notes": ""},
            ],
            "ai_autonomy_level": "preview_all",
        }
        result = build_philosophical_constraints(profile, governance_mode="self_governed")
        assert "self-defined" in result
        assert "set by parent" not in result
        # parent-led topic label must swap to governor-led in self mode
        assert "GOVERNOR-LED TOPIC" in result
        assert "PARENT-LED TOPIC" not in result
        # The constraint text itself addresses the learner as "you"
        assert "you has explicitly assigned" in result
        # The AI autonomy line uses "governor" for any non-parent mode
        assert "for governor review" in result
        assert "for parent review" not in result

    def test_parent_governed_constraints_unchanged(self):
        """Default parent_governed mode matches existing behavior."""
        profile = {
            "educational_philosophy": "classical",
            "content_boundaries": [
                {"topic": "gambling", "stance": "parent_led_only", "notes": ""},
            ],
            "ai_autonomy_level": "preview_all",
        }
        # Explicit mode
        result_explicit = build_philosophical_constraints(profile, governance_mode="parent_governed")
        # Implicit default must produce the same string
        result_default = build_philosophical_constraints(profile)
        assert result_explicit == result_default
        assert "set by parent" in result_explicit
        assert "PARENT-LED TOPIC" in result_explicit
        assert "for parent review" in result_explicit

    def test_institution_governed_uses_institutional_language(self):
        profile = {
            "educational_philosophy": "traditional",
            "content_boundaries": [
                {"topic": "gambling", "stance": "parent_led_only", "notes": ""},
            ],
            "ai_autonomy_level": "approve_difficult",
        }
        result = build_philosophical_constraints(profile, governance_mode="institution_governed")
        assert "set by administration" in result
        assert "set by parent" not in result
        assert "GOVERNOR-LED TOPIC" in result
        assert "the institution has explicitly assigned" in result
        assert "for governor review" in result

    def test_mentor_governed_uses_mentor_language(self):
        profile = {
            "educational_philosophy": "traditional",
            "content_boundaries": [
                {"topic": "gambling", "stance": "parent_led_only", "notes": ""},
            ],
            "ai_autonomy_level": "approve_difficult",
        }
        result = build_philosophical_constraints(profile, governance_mode="mentor_governed")
        assert "set by mentor" in result
        assert "set by parent" not in result
        assert "GOVERNOR-LED TOPIC" in result
        assert "your mentor has explicitly assigned" in result
        assert "for governor review" in result


# ══════════════════════════════════════════════════
# API CRUD Tests
# ══════════════════════════════════════════════════


class TestPhilosophicalProfileAPI:
    @pytest.mark.asyncio
    async def test_set_and_get_profile(self, auth_client, db_session, household, user):
        profile = {
            "educational_philosophy": "classical",
            "philosophy_description": "Trivium-based, great books",
            "religious_framework": "christian",
            "content_boundaries": [
                {"topic": "evolution", "stance": "present_alternative", "notes": ""},
            ],
            "ai_autonomy_level": "approve_difficult",
            "pedagogical_preferences": {"socratic_method": True},
            "custom_constraints": ["Include primary sources in history"],
        }
        resp = await auth_client.put("/api/v1/household/philosophy", json=profile)
        assert resp.status_code == 200
        data = resp.json()
        assert data["educational_philosophy"] == "classical"

        # Read it back
        get_resp = await auth_client.get("/api/v1/household/philosophy")
        assert get_resp.status_code == 200
        assert get_resp.json()["educational_philosophy"] == "classical"
        assert len(get_resp.json()["content_boundaries"]) == 1

    @pytest.mark.asyncio
    async def test_update_profile(self, auth_client, db_session, household, user):
        await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "educational_philosophy": "montessori",
            },
        )
        resp = await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "educational_philosophy": "charlotte_mason",
                "ai_autonomy_level": "preview_all",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["educational_philosophy"] == "charlotte_mason"

    @pytest.mark.asyncio
    async def test_invalid_philosophy_rejected(self, auth_client, db_session, household, user):
        resp = await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "educational_philosophy": "not_a_real_philosophy",
            },
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_invalid_stance_rejected(self, auth_client, db_session, household, user):
        resp = await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "content_boundaries": [
                    {"topic": "math", "stance": "invalid_stance", "notes": ""},
                ],
            },
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_invalid_autonomy_rejected(self, auth_client, db_session, household, user):
        resp = await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "ai_autonomy_level": "not_a_level",
            },
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_governance_event_logged(self, auth_client, db_session, household, user):
        from app.models.governance import GovernanceEvent

        await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "educational_philosophy": "eclectic",
            },
        )
        result = await db_session.execute(
            select(GovernanceEvent).where(GovernanceEvent.target_type == "philosophical_profile")
        )
        event = result.scalar_one()
        assert event.reason == "Philosophical profile updated"


# ══════════════════════════════════════════════════
# AI Prompt Injection Tests
# ══════════════════════════════════════════════════


class TestPhilosophyInAIPrompts:
    @pytest.mark.asyncio
    async def test_profile_injected_into_planner(
        self,
        auth_client,
        db_session,
        household,
        subject,
        child,
        user,
    ):
        """Set a profile, generate a plan, verify constraints in AI run input."""
        from app.models.curriculum import ChildMapEnrollment, LearningMap

        # Set philosophical profile
        await auth_client.put(
            "/api/v1/household/philosophy",
            json={
                "educational_philosophy": "classical",
                "content_boundaries": [
                    {"topic": "astrology", "stance": "exclude", "notes": "Not evidence-based"},
                ],
                "custom_constraints": ["Always include primary sources"],
            },
        )

        # Create a map and enroll child so planner has context
        lmap = LearningMap(
            household_id=household.id,
            subject_id=subject.id,
            name="Philosophy Test Map",
        )
        db_session.add(lmap)
        await db_session.flush()
        db_session.add(
            ChildMapEnrollment(
                child_id=child.id,
                household_id=household.id,
                learning_map_id=lmap.id,
            )
        )
        await db_session.flush()

        # Initialize governance rules
        from app.services.governance import create_default_rules

        await create_default_rules(db_session, household.id, user.id)

        # Generate a plan (triggers AI call with profile)
        from datetime import date

        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/plans/generate",
            json={"week_start": date.today().isoformat()},
        )
        assert resp.status_code == 201
        plan_data = resp.json()
        ai_run_id = plan_data.get("ai_run_id")

        # Check that the AI run's system_prompt contains the constraints
        if ai_run_id:
            run_result = await db_session.execute(select(AIRun).where(AIRun.id == ai_run_id))
            ai_run = run_result.scalar_one_or_none()
            if ai_run and ai_run.input_data:
                system_prompt = ai_run.input_data.get("system_prompt", "")
                assert "PHILOSOPHICAL CONSTRAINTS" in system_prompt
                assert "Classical education" in system_prompt
                assert "astrology" in system_prompt
                assert "primary sources" in system_prompt

    @pytest.mark.asyncio
    async def test_content_boundary_in_prompt(self, db_session, household, user):
        """Verify content boundary exclusion appears correctly."""
        from app.ai.gateway import AIRole, call_ai

        # Set profile on household
        household.philosophical_profile = {
            "content_boundaries": [
                {"topic": "violent_content", "stance": "exclude", "notes": "Age-inappropriate"},
            ],
        }
        await db_session.flush()

        result = await call_ai(
            db_session,
            role=AIRole.planner,
            system_prompt="Test prompt",
            user_prompt="Test",
            household_id=household.id,
            triggered_by=user.id,
            philosophical_profile=household.philosophical_profile,
        )

        # Check the AI run recorded the augmented prompt
        run_result = await db_session.execute(select(AIRun).where(AIRun.id == result["ai_run_id"]))
        ai_run = run_result.scalar_one()
        system_prompt = ai_run.input_data.get("system_prompt", "")
        assert "CONTENT EXCLUSION" in system_prompt
        assert "violent_content" in system_prompt
        assert "Age-inappropriate" in system_prompt
