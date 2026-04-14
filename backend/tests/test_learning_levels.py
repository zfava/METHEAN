"""Tests for learning levels, subject catalog, and preferences."""

import pytest
from app.core.learning_levels import (
    LEARNING_LEVELS,
    VALID_LEVELS,
    SUBJECT_CATALOG,
    get_level_for_subject,
    get_daily_minutes_for_child,
    build_level_context,
)


class TestLearningLevelsModule:
    def test_five_levels_defined(self):
        assert len(LEARNING_LEVELS) == 5
        assert set(LEARNING_LEVELS.keys()) == {"foundational", "developing", "intermediate", "advanced", "mastery"}

    def test_valid_levels_set(self):
        assert VALID_LEVELS == {"foundational", "developing", "intermediate", "advanced", "mastery"}

    def test_catalog_has_academic_and_vocational(self):
        assert len(SUBJECT_CATALOG["academic"]) >= 15
        assert len(SUBJECT_CATALOG["vocational"]) >= 10

    def test_get_level_default(self):
        assert get_level_for_subject(None, "Mathematics") == "developing"

    def test_get_level_from_prefs(self):
        class FakePrefs:
            subject_levels = {"mathematics": "advanced", "latin": "foundational"}

        assert get_level_for_subject(FakePrefs(), "Mathematics") == "advanced"
        assert get_level_for_subject(FakePrefs(), "Latin") == "foundational"
        assert get_level_for_subject(FakePrefs(), "Science") == "developing"

    def test_daily_minutes_fallback(self):
        class FakeChild:
            preferences = None

        assert get_daily_minutes_for_child(FakeChild()) == 120

    def test_daily_minutes_from_prefs(self):
        class FakePrefs:
            daily_duration_minutes = 180

        class FakeChild:
            preferences = FakePrefs()

        assert get_daily_minutes_for_child(FakeChild()) == 180

    def test_build_level_context(self):
        class FakePrefs:
            subject_levels = {"mathematics": "advanced"}

        ctx = build_level_context(FakePrefs(), ["Mathematics", "Latin"])
        assert "Advanced" in ctx
        assert "Developing" in ctx  # Latin defaults to developing


class TestSubjectCatalogAPI:
    @pytest.mark.asyncio
    async def test_catalog_returns_all_categories(self, auth_client):
        resp = await auth_client.get("/api/v1/subjects/catalog")
        assert resp.status_code == 200
        data = resp.json()
        assert "academic" in data
        assert "vocational" in data
        assert "custom" in data
        assert "levels" in data
        assert len(data["academic"]) >= 15
        assert len(data["vocational"]) >= 10

    @pytest.mark.asyncio
    async def test_custom_subject_creation(self, auth_client):
        resp = await auth_client.post(
            "/api/v1/subjects/custom",
            json={
                "name": "Beekeeping",
                "category": "life_skills",
                "description": "Hive management",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["name"] == "Beekeeping"

    @pytest.mark.asyncio
    async def test_duplicate_custom_rejected(self, auth_client):
        await auth_client.post("/api/v1/subjects/custom", json={"name": "Beekeeping2"})
        resp = await auth_client.post("/api/v1/subjects/custom", json={"name": "Beekeeping2"})
        assert resp.status_code == 409


class TestPreferencesAPI:
    @pytest.mark.asyncio
    async def test_set_subject_levels(self, auth_client, db_session, household, child):
        resp = await auth_client.put(
            f"/api/v1/children/{child.id}/preferences",
            json={
                "subject_levels": {"mathematics": "advanced", "latin": "foundational"},
            },
        )
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_invalid_level_rejected(self, auth_client, db_session, household, child):
        resp = await auth_client.put(
            f"/api/v1/children/{child.id}/preferences",
            json={
                "subject_levels": {"mathematics": "super_genius"},
            },
        )
        assert resp.status_code == 400
        assert "super_genius" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_child_without_grade(self, auth_client):
        resp = await auth_client.post(
            "/api/v1/children",
            json={
                "first_name": "Test",
            },
        )
        assert resp.status_code == 201
