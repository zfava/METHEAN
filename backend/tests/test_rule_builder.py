"""Tests for governance rule builder API validation.

Covers:
- Create rule via API
- Constitutional requires confirmation
- Content filter validates topic
- Update rule parameters
- Delete policy rule
- Delete constitutional rule rejected
"""

import uuid
from datetime import date

import pytest
from sqlalchemy import select

from app.models.enums import RuleType, RuleTier, RuleScope
from app.models.governance import GovernanceRule


class TestRuleBuilderAPI:

    @pytest.mark.asyncio
    async def test_create_pace_limit_rule(self, auth_client):
        """POST a pace_limit rule, verify 201."""
        resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "pace_limit",
            "tier": "policy",
            "scope": "household",
            "name": "4 hours max",
            "parameters": {"max_daily_minutes": 240, "max_weekly_minutes": 1200, "enforce": "soft"},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "4 hours max"
        assert data["rule_type"] == "pace_limit"

    @pytest.mark.asyncio
    async def test_create_constitutional_requires_confirmation(self, auth_client):
        """POST constitutional without confirm, verify 400."""
        resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "approval_required",
            "tier": "constitutional",
            "scope": "household",
            "name": "All activities reviewed",
            "parameters": {"action": "always_review"},
        })
        assert resp.status_code == 400
        assert "confirm_constitutional" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_content_filter_validates_topic(self, auth_client):
        """POST content_filter without topic, verify 400."""
        resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "content_filter",
            "tier": "policy",
            "scope": "household",
            "name": "Missing topic",
            "parameters": {"stance": "exclude"},
        })
        assert resp.status_code == 400
        assert "topic" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_pace_limit_validates_range(self, auth_client):
        """POST pace_limit with out-of-range minutes, verify 400."""
        resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "pace_limit",
            "tier": "policy",
            "scope": "household",
            "name": "Invalid",
            "parameters": {"max_daily_minutes": 9999},
        })
        assert resp.status_code == 400
        assert "max_daily_minutes" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_update_rule_parameters(self, auth_client):
        """PUT with new parameters, verify updated."""
        create_resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "pace_limit",
            "tier": "policy",
            "scope": "household",
            "name": "To update",
            "parameters": {"max_daily_minutes": 120},
        })
        assert create_resp.status_code == 201
        rule_id = create_resp.json()["id"]

        resp = await auth_client.put(f"/api/v1/governance-rules/{rule_id}", json={
            "parameters": {"max_daily_minutes": 180},
        })
        assert resp.status_code == 200
        assert resp.json()["parameters"]["max_daily_minutes"] == 180

    @pytest.mark.asyncio
    async def test_delete_policy_rule(self, auth_client):
        """DELETE policy rule, verify 200."""
        create_resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "pace_limit",
            "tier": "policy",
            "scope": "household",
            "name": "To delete",
            "parameters": {"max_daily_minutes": 60},
        })
        rule_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/governance-rules/{rule_id}")
        assert resp.status_code == 200
        assert resp.json()["deleted"] is True

    @pytest.mark.asyncio
    async def test_delete_constitutional_rejected(self, auth_client):
        """DELETE constitutional rule, verify 400."""
        create_resp = await auth_client.post("/api/v1/governance-rules", json={
            "rule_type": "approval_required",
            "tier": "constitutional",
            "scope": "household",
            "name": "Cannot delete",
            "parameters": {"action": "always_review"},
            "confirm_constitutional": True,
        })
        assert create_resp.status_code == 201
        rule_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/governance-rules/{rule_id}")
        assert resp.status_code == 400
        assert "cannot be deleted" in resp.json()["detail"].lower()
