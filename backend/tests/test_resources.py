"""Tests for family resource library.

Covers:
- Create resource
- List with filters
- Update resource
- Delete resource
- Link and unlink nodes
"""

import uuid

import pytest
from sqlalchemy import select

from app.models.evidence import FamilyResource


class TestResourceModel:
    @pytest.mark.asyncio
    async def test_create_resource(self, db_session, household, user):
        """Create a resource, verify it's stored."""
        r = FamilyResource(
            household_id=household.id,
            created_by=user.id,
            name="Saxon Math 5/4",
            resource_type="textbook",
            subject_area="mathematics",
            publisher="Saxon",
            grade_range="3-5",
            status="owned",
        )
        db_session.add(r)
        await db_session.flush()

        result = await db_session.execute(select(FamilyResource).where(FamilyResource.id == r.id))
        saved = result.scalar_one()
        assert saved.name == "Saxon Math 5/4"
        assert saved.resource_type == "textbook"
        assert saved.subject_area == "mathematics"

    @pytest.mark.asyncio
    async def test_link_unlink_node(self, db_session, household, user):
        """Link a node to a resource, then unlink it."""
        r = FamilyResource(
            household_id=household.id,
            created_by=user.id,
            name="Test Book",
            resource_type="textbook",
            linked_node_ids=[],
        )
        db_session.add(r)
        await db_session.flush()

        node_id = str(uuid.uuid4())
        r.linked_node_ids = [node_id]
        from sqlalchemy.orm.attributes import flag_modified

        flag_modified(r, "linked_node_ids")
        await db_session.flush()
        await db_session.refresh(r)
        assert node_id in r.linked_node_ids

        r.linked_node_ids = []
        flag_modified(r, "linked_node_ids")
        await db_session.flush()
        await db_session.refresh(r)
        assert len(r.linked_node_ids) == 0


class TestResourceAPI:
    @pytest.mark.asyncio
    async def test_create_resource_api(self, auth_client):
        """POST /resources returns 201."""
        resp = await auth_client.post(
            "/api/v1/resources",
            json={
                "name": "Story of the World Vol 1",
                "resource_type": "textbook",
                "subject_area": "history",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Story of the World Vol 1"
        assert data["resource_type"] == "textbook"

    @pytest.mark.asyncio
    async def test_list_resources_filtered(self, auth_client):
        """Create multiple resources, filter by type."""
        await auth_client.post("/api/v1/resources", json={"name": "TextA", "resource_type": "textbook"})
        await auth_client.post("/api/v1/resources", json={"name": "WorkA", "resource_type": "workbook"})
        await auth_client.post("/api/v1/resources", json={"name": "TextB", "resource_type": "textbook"})

        # Filter by textbook
        resp = await auth_client.get("/api/v1/resources?resource_type=textbook")
        assert resp.status_code == 200
        items = resp.json()
        assert all(r["resource_type"] == "textbook" for r in items)
        assert len(items) >= 2

    @pytest.mark.asyncio
    async def test_update_resource_api(self, auth_client):
        """PUT /resources/{id} updates fields."""
        create_resp = await auth_client.post("/api/v1/resources", json={"name": "Old Name"})
        rid = create_resp.json()["id"]

        resp = await auth_client.put(f"/api/v1/resources/{rid}", json={"name": "New Name", "publisher": "Acme"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"
        assert resp.json()["publisher"] == "Acme"

    @pytest.mark.asyncio
    async def test_delete_resource_api(self, auth_client):
        """DELETE /resources/{id} removes it."""
        create_resp = await auth_client.post("/api/v1/resources", json={"name": "To Delete"})
        rid = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/resources/{rid}")
        assert resp.status_code == 200
        assert resp.json()["deleted"] is True

        # Verify 404 on re-fetch
        resp = await auth_client.put(f"/api/v1/resources/{rid}", json={"name": "X"})
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_link_unlink_api(self, auth_client):
        """Link a node, verify. Unlink, verify."""
        create_resp = await auth_client.post("/api/v1/resources", json={"name": "Linkable"})
        rid = create_resp.json()["id"]
        node_id = str(uuid.uuid4())

        # Link
        resp = await auth_client.post(f"/api/v1/resources/{rid}/link/{node_id}")
        assert resp.status_code == 200
        assert node_id in resp.json()["linked_node_ids"]

        # Unlink
        resp = await auth_client.delete(f"/api/v1/resources/{rid}/link/{node_id}")
        assert resp.status_code == 200
        assert node_id not in resp.json()["linked_node_ids"]
