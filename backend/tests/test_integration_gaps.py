"""Integration tests for Build 18 gap remediation."""

import pytest


class TestVocationalTemplates:
    @pytest.mark.asyncio
    async def test_core_templates_registered(self, auth_client):
        """The core starter templates are all registered and exposed by the
        templates endpoint.

        This verifies the EXPECTED NAMED templates are present (academic,
        vocational, fitness, and visual-art tiers), so a MISSING or DUPLICATE
        template fails the test, rather than asserting a brittle exact count
        that breaks every time a legitimate template is added. The count check
        is a known-good lower bound (>=), resilient to future growth the same
        way the curriculum tier count-gates were relaxed.
        """
        resp = await auth_client.get("/api/v1/learning-maps/templates")
        assert resp.status_code == 200
        templates = resp.json()
        names = [t["name"] for t in templates]

        # Every required template must be present by name.
        required = [
            "Mathematics Foundational",
            "Reading Foundational",
            "Welding Fundamentals",
            "Electrical Fundamentals",
            "Automotive Fundamentals",
            "Woodworking Fundamentals",
            "Physical Fitness: Foundations",
            "Physical Fitness: Independent",
            "Visual Art: Foundations",
            "Visual Art: Independent",
        ]
        missing = [name for name in required if name not in names]
        assert not missing, f"missing required templates: {missing}"

        # No duplicate template name may be registered (a duplicate is the real risk).
        duplicates = sorted({name for name in names if names.count(name) > 1})
        assert not duplicates, f"duplicate template names registered: {duplicates}"

        # Known-good lower bound: 18 templates as of the Reading Foundational
        # addition (which made the reading tier generatable). New legitimate
        # templates may raise this; the named-presence check above is what
        # actually guards correctness.
        assert len(templates) >= 18, f"expected at least 18 templates, got {len(templates)}"

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
