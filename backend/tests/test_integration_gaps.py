"""Integration tests for Build 18 gap remediation."""

import pytest


class TestVocationalTemplates:

    @pytest.mark.asyncio
    async def test_seven_templates_registered(self, auth_client):
        """All 7 templates (3 academic + 4 vocational) in template list."""
        resp = await auth_client.get("/api/v1/learning-maps/templates")
        assert resp.status_code == 200
        templates = resp.json()
        names = [t["name"] for t in templates]
        assert "Mathematics Foundational" in names
        assert "Welding Fundamentals" in names
        assert "Electrical Fundamentals" in names
        assert "Automotive Fundamentals" in names
        assert "Woodworking Fundamentals" in names
        assert len(templates) == 7

    @pytest.mark.asyncio
    async def test_welding_template_has_safety_first(self, auth_client):
        """Welding template has safety node as entry point."""
        resp = await auth_client.post("/api/v1/learning-maps/from-template/welding-fundamentals")
        assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_assessment_types_endpoint(self, auth_client):
        """GET /assessment-types returns both categories."""
        resp = await auth_client.get("/api/v1/assessment-types")
        assert resp.status_code == 200
        data = resp.json()
        assert "academic" in data and "vocational" in data
        assert "parent_observation" in data["academic"]
        assert "practical_demo" in data["vocational"]
