"""Tests for vocational curriculum, certification tracking, and mentors."""

import uuid
from datetime import date

import pytest


class TestVocationalNodeTypes:

    @pytest.mark.asyncio
    async def test_all_node_types_accepted(self, auth_client, db_session, household, user, subject, learning_map):
        """All 9 node types can be created."""
        for nt in ["root", "milestone", "concept", "skill", "safety", "knowledge", "technique", "project", "certification_prep"]:
            resp = await auth_client.post(f"/api/v1/learning-maps/{learning_map.id}/nodes", json={
                "node_type": nt, "title": f"Test {nt}", "estimated_minutes": 30,
            })
            assert resp.status_code == 201, f"Failed to create {nt} node"


class TestAssessmentTypes:

    @pytest.mark.asyncio
    async def test_assessment_types_include_vocational(self, auth_client):
        """GET /assessment-types returns both academic and vocational."""
        resp = await auth_client.get("/api/v1/assessment-types")
        assert resp.status_code == 200
        data = resp.json()
        assert "practical_demo" in data["vocational"]
        assert "weld_inspection" in data["vocational"]
        assert "parent_observation" in data["academic"]


class TestCertificationTracking:

    @pytest.mark.asyncio
    async def test_certification_crud(self, auth_client, db_session, household, child):
        """Create, list, and update a certification."""
        resp = await auth_client.post(f"/api/v1/children/{child.id}/certifications", json={
            "name": "AWS Certified Welder", "subject": "welding",
            "target_date": "2027-06-01",
            "requirements": [{"name": "Shop Safety", "met": False}, {"name": "Flat Position", "met": False}],
        })
        assert resp.status_code == 201
        cert_id = resp.json()["id"]

        resp = await auth_client.get(f"/api/v1/children/{child.id}/certifications")
        assert len(resp.json()) >= 1

        resp = await auth_client.put(f"/api/v1/children/{child.id}/certifications/{cert_id}", json={
            "status": "in_progress",
            "requirements": [{"name": "Shop Safety", "met": True, "date_met": "2026-09-15"}, {"name": "Flat Position", "met": False}],
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_certification_duplicate_rejected(self, auth_client, db_session, household, child):
        """Duplicate certifications rejected."""
        await auth_client.post(f"/api/v1/children/{child.id}/certifications", json={
            "name": "Test Cert Dup", "subject": "welding",
        })
        resp = await auth_client.post(f"/api/v1/children/{child.id}/certifications", json={
            "name": "Test Cert Dup", "subject": "welding",
        })
        assert resp.status_code == 409


class TestMentors:

    @pytest.mark.asyncio
    async def test_mentor_crud(self, auth_client):
        """Add and remove a mentor."""
        resp = await auth_client.post("/api/v1/household/mentors", json={
            "name": "Mike Johnson", "trade": "Welding", "availability": "Saturdays 9-12",
        })
        assert resp.status_code == 201
        mentor_id = resp.json()["id"]

        resp = await auth_client.get("/api/v1/household/mentors")
        assert resp.status_code == 200
        assert any(m["id"] == mentor_id for m in resp.json())

        resp = await auth_client.delete(f"/api/v1/household/mentors/{mentor_id}")
        assert resp.status_code == 200


class TestManualVocationalActivity:

    @pytest.mark.asyncio
    async def test_vocational_fields_accepted(self, auth_client, db_session, household, child):
        """Manual activities accept vocational fields."""
        resp = await auth_client.post("/api/v1/activities", json={
            "child_id": str(child.id),
            "title": "MIG Flat Position Practice",
            "activity_type": "lesson",
            "scheduled_date": "2026-10-15",
            "estimated_minutes": 60,
            "subject_area": "Welding",
            "tools_required": ["MIG welder", "Welding helmet"],
            "materials": [{"item": "Mild steel plate", "quantity": "2", "estimated_cost": 8.0}],
            "safety_notes": "Ensure ventilation. Wear long sleeves.",
        })
        assert resp.status_code == 201
