"""Tests for governance rule tiers (constitutional vs policy).

Covers:
- Constitutional rules require confirmation to create
- Constitutional rule changes are logged with full diff
- Constitutional rules cannot be deleted (only deactivated)
- Deactivation requires a reason of >= 20 characters
- Policy rules work normally
"""

import uuid

import pytest
from sqlalchemy import select

from app.models.governance import GovernanceEvent


class TestConstitutionalRules:
    @pytest.mark.asyncio
    async def test_constitutional_requires_confirmation(self, auth_client, db_session, household, user):
        """Creating a constitutional rule without confirm_constitutional=true should fail."""
        resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Test Constitutional",
                "parameters": {},
            },
        )
        assert resp.status_code == 400
        assert "confirm_constitutional" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_constitutional_created_with_confirmation(self, auth_client, db_session, household, user):
        resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Test Constitutional",
                "parameters": {},
                "confirm_constitutional": True,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["tier"] == "constitutional"
        assert data["name"] == "Test Constitutional"

    @pytest.mark.asyncio
    async def test_constitutional_creation_logged(self, auth_client, db_session, household, user):
        await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Logged Constitutional",
                "parameters": {},
                "confirm_constitutional": True,
            },
        )
        result = await db_session.execute(
            select(GovernanceEvent).where(GovernanceEvent.target_type == "constitutional_rule_change")
        )
        event = result.scalars().first()
        assert event is not None
        assert "Constitutional rule created" in event.reason

    @pytest.mark.asyncio
    async def test_constitutional_update_requires_reason(self, auth_client, db_session, household, user):
        # Create the rule first
        create_resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Update Test",
                "parameters": {},
                "confirm_constitutional": True,
            },
        )
        rule_id = create_resp.json()["id"]

        # Try to update without confirmation
        resp = await auth_client.put(
            f"/api/v1/governance-rules/{rule_id}",
            json={
                "name": "Updated Name",
            },
        )
        assert resp.status_code == 400
        assert "confirm_constitutional" in resp.json()["detail"]

        # Try with confirmation but short reason
        resp2 = await auth_client.put(
            f"/api/v1/governance-rules/{rule_id}",
            json={
                "name": "Updated Name",
                "confirm_constitutional": True,
                "reason": "too short",
            },
        )
        assert resp2.status_code == 400
        assert "20 characters" in resp2.json()["detail"]

    @pytest.mark.asyncio
    async def test_constitutional_update_with_ceremony(self, auth_client, db_session, household, user):
        create_resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Ceremony Test",
                "parameters": {"level": 1},
                "confirm_constitutional": True,
            },
        )
        rule_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/governance-rules/{rule_id}",
            json={
                "name": "Ceremony Test Updated",
                "parameters": {"level": 2},
                "confirm_constitutional": True,
                "reason": "Updating because the family's needs have changed after six months of use.",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Ceremony Test Updated"

        # Verify governance event logged with diff
        result = await db_session.execute(
            select(GovernanceEvent)
            .where(
                GovernanceEvent.target_type == "constitutional_rule_change",
                GovernanceEvent.target_id == uuid.UUID(rule_id),
            )
            .order_by(GovernanceEvent.created_at.desc())
        )
        events = result.scalars().all()
        update_event = next(
            (e for e in events if "changed" in (e.reason or "").lower() or "Updating" in (e.reason or "")),
            events[0] if events else None,
        )
        assert update_event is not None
        assert update_event.metadata_ is not None
        assert "before" in update_event.metadata_
        assert "after" in update_event.metadata_

    @pytest.mark.asyncio
    async def test_constitutional_cannot_be_deleted(self, auth_client, db_session, household, user):
        create_resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Undeletable",
                "parameters": {},
                "confirm_constitutional": True,
            },
        )
        rule_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/governance-rules/{rule_id}")
        assert resp.status_code == 400
        assert "cannot be deleted" in resp.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_constitutional_deactivation_requires_reason(self, auth_client, db_session, household, user):
        create_resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "ai_boundary",
                "tier": "constitutional",
                "name": "Deactivate Test",
                "parameters": {},
                "confirm_constitutional": True,
            },
        )
        rule_id = create_resp.json()["id"]

        # Deactivate without reason
        resp = await auth_client.put(
            f"/api/v1/governance-rules/{rule_id}",
            json={
                "is_active": False,
                "confirm_constitutional": True,
            },
        )
        assert resp.status_code == 400
        assert "reason" in resp.json()["detail"].lower()

        # Deactivate with proper reason
        resp2 = await auth_client.put(
            f"/api/v1/governance-rules/{rule_id}",
            json={
                "is_active": False,
                "confirm_constitutional": True,
                "reason": "Temporarily deactivating while we reassess our educational approach for the semester.",
            },
        )
        assert resp2.status_code == 200
        assert resp2.json()["is_active"] is False


class TestPolicyRulesUnchanged:
    @pytest.mark.asyncio
    async def test_policy_rule_normal_crud(self, auth_client, db_session, household, user):
        # Create without confirmation
        resp = await auth_client.post(
            "/api/v1/governance-rules",
            json={
                "rule_type": "pace_limit",
                "name": "Policy Rule",
                "parameters": {"max_daily_minutes": 120},
            },
        )
        assert resp.status_code == 201
        assert resp.json()["tier"] == "policy"
        rule_id = resp.json()["id"]

        # Update without ceremony
        resp2 = await auth_client.put(
            f"/api/v1/governance-rules/{rule_id}",
            json={
                "name": "Updated Policy",
            },
        )
        assert resp2.status_code == 200

        # Delete works
        resp3 = await auth_client.delete(f"/api/v1/governance-rules/{rule_id}")
        assert resp3.status_code == 200

    @pytest.mark.asyncio
    async def test_default_rules_include_constitutional(self, auth_client, db_session, household, user):
        resp = await auth_client.post("/api/v1/governance-rules/defaults")
        assert resp.status_code == 201
        rules = resp.json()
        constitutional = [r for r in rules if r["tier"] == "constitutional"]
        assert len(constitutional) == 1
        assert constitutional[0]["name"] == "AI oversight guarantee"
