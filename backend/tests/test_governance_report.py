"""Tests for governance report generation and attestation.

Covers:
- Report includes all sections
- Attestation creates immutable governance event
- AI acceptance rate calculation
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.enums import GovernanceAction
from app.models.governance import GovernanceEvent


class TestGovernanceReport:

    @pytest.mark.asyncio
    async def test_report_includes_all_sections(
        self, auth_client, db_session, household, user,
    ):
        today = date.today()
        resp = await auth_client.post("/api/v1/governance/report", json={
            "period_start": (today - timedelta(days=30)).isoformat(),
            "period_end": today.isoformat(),
        })
        assert resp.status_code == 200
        report = resp.json()

        # Verify all sections present
        assert "executive_summary" in report
        assert "governance_decisions" in report
        assert "ai_oversight" in report
        assert "rule_changes" in report
        assert "constitutional_actions" in report
        assert "overrides" in report
        assert "learning_progress" in report
        assert "compliance_metrics" in report
        assert "parent_attestation" in report
        assert "period" in report
        assert "household" in report

    @pytest.mark.asyncio
    async def test_report_attestation_creates_event(
        self, auth_client, db_session, household, user,
    ):
        resp = await auth_client.post("/api/v1/governance/report/attest", json={
            "report_id": "test-report-123",
            "attestation_text": "I confirm this report is accurate and complete for the period.",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["report_id"] == "test-report-123"

        # Verify governance event exists
        result = await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.target_type == "governance_report_attestation",
            )
        )
        event = result.scalar_one()
        assert "accurate and complete" in event.reason
        assert event.metadata_["report_id"] == "test-report-123"

    @pytest.mark.asyncio
    async def test_ai_acceptance_rate(
        self, auth_client, db_session, household, user,
    ):
        """Create 10 events (7 approve, 3 reject), verify 70% rate."""
        target = uuid.uuid4()
        for i in range(7):
            db_session.add(GovernanceEvent(
                household_id=household.id, user_id=user.id,
                action=GovernanceAction.approve,
                target_type="activity", target_id=target,
                reason=f"Approved {i}",
            ))
        for i in range(3):
            db_session.add(GovernanceEvent(
                household_id=household.id, user_id=user.id,
                action=GovernanceAction.reject,
                target_type="activity", target_id=target,
                reason=f"Rejected {i}",
            ))
        await db_session.flush()

        today = date.today()
        resp = await auth_client.post("/api/v1/governance/report", json={
            "period_start": (today - timedelta(days=1)).isoformat(),
            "period_end": (today + timedelta(days=1)).isoformat(),
        })
        assert resp.status_code == 200
        report = resp.json()
        assert report["executive_summary"]["ai_acceptance_rate_pct"] == 70.0

    @pytest.mark.asyncio
    async def test_attestation_requires_min_length(
        self, auth_client, db_session, household, user,
    ):
        resp = await auth_client.post("/api/v1/governance/report/attest", json={
            "report_id": "x",
            "attestation_text": "short",
        })
        assert resp.status_code == 422  # Pydantic validation: min 10 chars
