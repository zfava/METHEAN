"""Every governance event must ride the hash chain.

Before migration 055, twenty code paths constructed GovernanceEvent
rows directly, bypassing the migration 052 hash chain and breaking
verification for any household that used them. These tests pin the
repair: a source-level guard against new direct constructions, plus
end-to-end checks that the previously-offending surfaces now produce
hashed, verifiable chains.
"""

import re
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.models.curriculum import LearningNode
from app.models.enums import NodeType
from app.models.governance import GovernanceEvent

APP_DIR = Path(__file__).resolve().parents[1] / "app"

# The only modules allowed to construct GovernanceEvent directly: the
# model definition and the chain-aware logger itself.
_ALLOWED = {"app/models/governance.py", "app/services/governance.py"}


def test_no_direct_governance_event_constructions():
    """Source guard: every event goes through log_governance_event."""
    pattern = re.compile(r"(?<!Evidence)\bGovernanceEvent\(")
    offenders = []
    for path in APP_DIR.rglob("*.py"):
        rel = path.relative_to(APP_DIR.parent).as_posix()
        if rel in _ALLOWED:
            continue
        if pattern.search(path.read_text()):
            offenders.append(rel)
    assert offenders == [], (
        "Direct GovernanceEvent constructions bypass the hash chain "
        f"(use log_governance_event): {offenders}"
    )


async def _assert_chain_verified(auth_client: AsyncClient, expected_min_events: int) -> None:
    response = await auth_client.get("/api/v1/chain/verify")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["valid"] is True, data
    assert data["checked"] >= expected_min_events


@pytest.mark.asyncio
async def test_mastery_override_event_is_hashed_and_chain_verifies(
    auth_client: AsyncClient, db_session, household, child, learning_map
):
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title="Addition",
    )
    db_session.add(node)
    await db_session.flush()

    response = await auth_client.post(
        f"/api/v1/children/{child.id}/nodes/{node.id}/mastery-override",
        json={"target_level": "mastered", "reason": "Demonstrated in person"},
    )
    assert response.status_code == 200, response.text

    events = (
        await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.household_id == household.id))
    ).scalars().all()
    assert events, "override must log a governance event"
    assert all(e.event_hash for e in events), "every event must carry a chain hash"
    await _assert_chain_verified(auth_client, expected_min_events=1)


@pytest.mark.asyncio
async def test_assessment_with_judgment_events_are_hashed_and_chain_verifies(
    auth_client: AsyncClient, db_session, household, child, learning_map
):
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title="Narration",
    )
    db_session.add(node)
    await db_session.flush()

    response = await auth_client.post(
        f"/api/v1/children/{child.id}/assessments",
        json={
            "node_id": str(node.id),
            "assessment_type": "observation",
            "title": "Observed narration",
            "mastery_judgment": "proficient",
        },
    )
    assert response.status_code == 201, response.text

    events = (
        await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.household_id == household.id))
    ).scalars().all()
    assert events, "assessment with judgment must log a governance event"
    assert all(e.event_hash for e in events)
    await _assert_chain_verified(auth_client, expected_min_events=1)


@pytest.mark.asyncio
async def test_philosophy_update_event_is_hashed(auth_client: AsyncClient, db_session, household):
    response = await auth_client.put(
        "/api/v1/household/philosophy",
        json={"primary_philosophy": "classical"},
    )
    assert response.status_code == 200, response.text
    events = (
        await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.household_id == household.id))
    ).scalars().all()
    assert events and all(e.event_hash for e in events)
    await _assert_chain_verified(auth_client, expected_min_events=1)


@pytest.mark.asyncio
async def test_attestation_event_is_hashed(auth_client: AsyncClient, db_session, household):
    response = await auth_client.post(
        "/api/v1/governance/report/attest",
        json={"report_id": str(uuid.uuid4()), "attestation_text": "I attest this record is accurate"},
    )
    assert response.status_code == 200, response.text
    events = (
        await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.household_id == household.id))
    ).scalars().all()
    assert events and all(e.event_hash for e in events)
    await _assert_chain_verified(auth_client, expected_min_events=1)
