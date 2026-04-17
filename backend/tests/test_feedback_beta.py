"""Tests for the beta feedback API.

Covers:
- Submit feedback via POST /feedback
- List own feedback via GET /feedback
- Get feedback detail via GET /feedback/{id}
- Validation of rating bounds, empty message, invalid feedback_type
- Auth required on all endpoints
- A user cannot fetch another user's feedback by ID
"""

import uuid

import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.evidence import BetaFeedback
from app.models.identity import Household, User


class TestBetaFeedbackAPI:
    @pytest.mark.asyncio
    async def test_submit_feedback(self, auth_client, db_session, user):
        """Submit feedback returns 201 and stores it."""
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={
                "feedback_type": "bug",
                "page_context": "/dashboard",
                "rating": 4,
                "message": "The mastery chart flickers on mobile.",
            },
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["feedback_type"] == "bug"
        assert data["page_context"] == "/dashboard"
        assert data["rating"] == 4
        assert data["message"] == "The mastery chart flickers on mobile."
        assert data["status"] == "new"
        assert "id" in data

        # Verify persisted
        result = await db_session.execute(select(BetaFeedback).where(BetaFeedback.user_id == user.id))
        fb = result.scalar_one()
        assert fb.message == "The mastery chart flickers on mobile."
        assert fb.household_id == user.household_id

    @pytest.mark.asyncio
    async def test_submit_minimal_feedback(self, auth_client):
        """Message alone is sufficient; feedback_type defaults to 'general'."""
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={"message": "Love this so far."},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["feedback_type"] == "general"
        assert data["rating"] is None
        assert data["page_context"] is None

    @pytest.mark.asyncio
    async def test_submit_rejects_empty_message(self, auth_client):
        """Empty message must be rejected by validation."""
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={"message": ""},
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_submit_rejects_invalid_rating(self, auth_client):
        """Rating outside 1-5 is rejected."""
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={"message": "ok", "rating": 9},
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_submit_rejects_invalid_type(self, auth_client):
        """Unknown feedback_type is rejected."""
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={"message": "ok", "feedback_type": "spam"},
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_list_own_feedback(self, auth_client):
        """List returns only the current user's feedback, newest first."""
        for i, msg in enumerate(["first", "second", "third"]):
            resp = await auth_client.post(
                "/api/v1/feedback",
                json={"message": msg, "feedback_type": "feature_request"},
            )
            assert resp.status_code == 201

        resp = await auth_client.get("/api/v1/feedback")
        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 3
        # Newest first
        assert items[0]["message"] == "third"
        assert items[2]["message"] == "first"
        for item in items:
            assert item["status"] == "new"
            assert item["feedback_type"] == "feature_request"

    @pytest.mark.asyncio
    async def test_get_feedback_detail(self, auth_client):
        """GET /feedback/{id} returns the submission."""
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={"message": "detail test", "feedback_type": "usability"},
        )
        fid = resp.json()["id"]

        resp = await auth_client.get(f"/api/v1/feedback/{fid}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == fid
        assert data["message"] == "detail test"
        assert data["feedback_type"] == "usability"

    @pytest.mark.asyncio
    async def test_get_feedback_not_found(self, auth_client):
        """Unknown ID returns 404."""
        resp = await auth_client.get(f"/api/v1/feedback/{uuid.uuid4()}")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_auth_required_submit(self, client):
        """Submission without auth returns 401."""
        resp = await client.post("/api/v1/feedback", json={"message": "hi"})
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_auth_required_list(self, client):
        """Listing without auth returns 401."""
        resp = await client.get("/api/v1/feedback")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_cannot_read_other_users_feedback(self, auth_client, client, db_session, user):
        """A second user in a different household cannot fetch another user's feedback by ID."""
        # Submit as the original user
        resp = await auth_client.post(
            "/api/v1/feedback",
            json={"message": "private to user A"},
        )
        fid = resp.json()["id"]

        # Create a second household + user
        other_hh = Household(name="Other Family", timezone="UTC")
        db_session.add(other_hh)
        await db_session.flush()
        other_user = User(
            household_id=other_hh.id,
            email="other@test.com",
            password_hash=hash_password("testpass123"),
            display_name="Other",
            role="owner",
        )
        db_session.add(other_user)
        await db_session.flush()

        other_token = create_access_token(other_user.id, other_hh.id, "owner")
        client.cookies.set("access_token", other_token)

        resp = await client.get(f"/api/v1/feedback/{fid}")
        assert resp.status_code == 404
