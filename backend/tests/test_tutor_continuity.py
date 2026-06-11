"""Tests for tutor continuity: parent-governed tutor memory.

Covers migration 057 and the full pipeline: extraction gating by
policy, routing (standard proposes, autonomous applies under the
grant, off never runs), the structural privacy validator, caps,
decisions and revocation, context injection, governance events on
every transition, chain validity after a full lifecycle, access
control, and the single-writer guard.
"""

import re
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.governance import GovernanceEvent
from app.models.identity import Household, User
from app.models.intelligence import TutorProfileEntry
from app.services.governance import set_ai_role_policy
from app.services.tutor_profile import (
    MAX_ACTIVE_ENTRIES,
    MAX_PENDING_PROPOSALS,
    TutorProfileStateError,
    TutorProfileValidationError,
    decide_entry,
    extract_and_route_proposals,
    get_active_entries_block,
    revoke_entry,
    route_proposal,
    validate_entry,
)

PASSWORD = "testpass123"

GOOD_PROPOSAL = {
    "category": "explanation_style",
    "content": "Concrete visual examples before abstract rules work well for this learner",
    "confidence": 0.8,
}


async def _set_policy(db, household, user, autonomy: str) -> None:
    await set_ai_role_policy(db, household.id, user.id, "tutor", autonomy)


# ── Routing matrix ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_standard_routes_to_proposed(db_session, household, user, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    assert entry is not None
    assert entry.status == "proposed"
    assert entry.grant_event_hash is None

    events = (
        (
            await db_session.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.household_id == household.id,
                    GovernanceEvent.target_type == "tutor_profile_proposed",
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(events) == 1
    assert events[0].event_hash, "proposal events ride the hash chain"


@pytest.mark.asyncio
async def test_autonomous_applies_with_grant_hash(db_session, household, user, child):
    await _set_policy(db_session, household, user, "autonomous")
    from app.services.governance import get_active_autonomy_grant

    grant_hash = await get_active_autonomy_grant(db_session, household.id, "tutor")
    assert grant_hash

    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    assert entry is not None
    assert entry.status == "active"
    assert entry.grant_event_hash == grant_hash
    assert entry.decided_by is None, "autonomous application has no per-item human decider"

    events = (
        (
            await db_session.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.household_id == household.id,
                    GovernanceEvent.target_type == "tutor_profile_applied_autonomously",
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(events) == 1
    assert events[0].metadata_["grant_event_hash"] == grant_hash


@pytest.mark.asyncio
async def test_off_runs_no_extraction_no_calls(db_session, household, user, child):
    await _set_policy(db_session, household, user, "off")
    with patch("app.ai.gateway.call_ai", new_callable=AsyncMock) as spy:
        created = await extract_and_route_proposals(
            db_session, household.id, child.id, "Child asked: help\nTutor replied: sure"
        )
    spy.assert_not_called()
    assert created == []
    rows = (
        (await db_session.execute(select(TutorProfileEntry).where(TutorProfileEntry.child_id == child.id)))
        .scalars()
        .all()
    )
    assert rows == []


@pytest.mark.asyncio
async def test_grant_race_drops_never_applies(db_session, household, user, child):
    """Policy says autonomous but the grant was revoked moments ago:
    the proposal is dropped, never applied."""
    await _set_policy(db_session, household, user, "autonomous")
    with patch(
        "app.services.tutor_profile.get_active_autonomy_grant",
        new_callable=AsyncMock,
        return_value=None,
    ):
        entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    assert entry is None
    rows = (
        (await db_session.execute(select(TutorProfileEntry).where(TutorProfileEntry.child_id == child.id)))
        .scalars()
        .all()
    )
    assert rows == []


@pytest.mark.asyncio
async def test_unreadable_policy_drops(db_session, household, child):
    with patch(
        "app.services.tutor_profile.get_ai_role_policy",
        new_callable=AsyncMock,
        side_effect=RuntimeError("cache and db both down"),
    ):
        entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    assert entry is None


# ── Decisions and revocation ────────────────────────────────────────


@pytest.mark.asyncio
async def test_approve_and_reject_transitions(db_session, household, user, child):
    first = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    second = await route_proposal(
        db_session,
        household.id,
        child.id,
        {"category": "pacing", "content": "Short five minute bursts keep momentum high"},
    )

    approved = await decide_entry(db_session, household.id, child.id, first.id, "approve", user.id)
    assert approved.status == "active"
    assert approved.decided_by == user.id
    assert approved.decided_at is not None

    rejected = await decide_entry(db_session, household.id, child.id, second.id, "reject", user.id)
    assert rejected.status == "rejected"

    types = {
        row[0]
        for row in (
            await db_session.execute(
                select(GovernanceEvent.target_type).where(GovernanceEvent.household_id == household.id)
            )
        ).all()
    }
    assert "tutor_profile_approved" in types
    assert "tutor_profile_rejected" in types

    # Decided entries are immutable to further decisions.
    with pytest.raises(TutorProfileStateError):
        await decide_entry(db_session, household.id, child.id, first.id, "reject", user.id)


@pytest.mark.asyncio
async def test_revoke_only_on_active(db_session, household, user, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    with pytest.raises(TutorProfileStateError):
        await revoke_entry(db_session, household.id, child.id, entry.id, user.id)

    await decide_entry(db_session, household.id, child.id, entry.id, "approve", user.id)
    revoked = await revoke_entry(db_session, household.id, child.id, entry.id, user.id)
    assert revoked.status == "revoked"

    events = (
        (
            await db_session.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.household_id == household.id,
                    GovernanceEvent.target_type == "tutor_profile_entry_revoked",
                )
            )
        )
        .scalars()
        .all()
    )
    assert len(events) == 1


# ── Caps ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_pending_cap_drops_sixth_proposal(db_session, household, user, child):
    for i in range(MAX_PENDING_PROPOSALS):
        entry = await route_proposal(
            db_session,
            household.id,
            child.id,
            {"category": "interest", "content": f"Linking practice to space exploration works well, variant {i}"},
        )
        assert entry is not None
    dropped = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    assert dropped is None
    count = len(
        (
            await db_session.execute(
                select(TutorProfileEntry).where(
                    TutorProfileEntry.child_id == child.id, TutorProfileEntry.status == "proposed"
                )
            )
        )
        .scalars()
        .all()
    )
    assert count == MAX_PENDING_PROPOSALS


@pytest.mark.asyncio
async def test_active_cap_drops_thirteenth_entry(db_session, household, user, child):
    await _set_policy(db_session, household, user, "autonomous")
    for i in range(MAX_ACTIVE_ENTRIES):
        entry = await route_proposal(
            db_session,
            household.id,
            child.id,
            {"category": "motivation", "content": f"Progress streak callouts keep energy up, variant {i}"},
        )
        assert entry is not None, f"entry {i} should land under cap"
    dropped = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    assert dropped is None
    count = len(
        (
            await db_session.execute(
                select(TutorProfileEntry).where(
                    TutorProfileEntry.child_id == child.id, TutorProfileEntry.status == "active"
                )
            )
        )
        .scalars()
        .all()
    )
    assert count == MAX_ACTIVE_ENTRIES


# ── Validator ───────────────────────────────────────────────────────


def test_validator_rejects_quoted_speech():
    with pytest.raises(TutorProfileValidationError, match="quotation"):
        validate_entry("other", 'Responds well when told "you are so close"')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content",
    [
        "Shows signs of ADHD during long sessions",
        "Likely dyslexia, prefers audio",
        "Works best with therapy style check-ins",
        "Possible attention deficit pattern observed",
    ],
)
async def test_validator_rejects_clinical_terms(content):
    with pytest.raises(TutorProfileValidationError, match="clinical"):
        validate_entry("other", content)


def test_validator_rejects_overlong_and_accepts_clean():
    with pytest.raises(TutorProfileValidationError, match="300"):
        validate_entry("pacing", "x" * 301)
    # A clean strategy entry passes.
    validate_entry("explanation_style", "Number lines before equations help this learner ground the concept")


# ── Injection ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_only_active_entries_injected(db_session, household, user, child):
    proposed = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    to_reject = await route_proposal(
        db_session, household.id, child.id, {"category": "pacing", "content": "Slow warmups help"}
    )
    to_revoke = await route_proposal(
        db_session, household.id, child.id, {"category": "interest", "content": "Dinosaur examples spark engagement"}
    )
    approved = await route_proposal(
        db_session,
        household.id,
        child.id,
        {"category": "motivation", "content": "Celebrating small wins keeps momentum"},
    )
    await decide_entry(db_session, household.id, child.id, to_reject.id, "reject", user.id)
    await decide_entry(db_session, household.id, child.id, to_revoke.id, "approve", user.id)
    await revoke_entry(db_session, household.id, child.id, to_revoke.id, user.id)
    await decide_entry(db_session, household.id, child.id, approved.id, "approve", user.id)

    block = await get_active_entries_block(db_session, household.id, child.id)
    assert "What works for this learner".upper() in block.upper()
    assert "Celebrating small wins" in block
    assert "Concrete visual examples" not in block, "proposed entries never inject"
    assert "Slow warmups" not in block, "rejected entries never inject"
    assert "Dinosaur examples" not in block, "revoked entries never inject"

    # And through the real context assembly seam:
    from app.services.context_assembly import assemble_context

    assembled = await assemble_context(db_session, role="tutor", child_id=child.id, household_id=household.id)
    assert "Celebrating small wins" in assembled["context_text"]


@pytest.mark.asyncio
async def test_policy_off_injects_nothing(db_session, household, user, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    await decide_entry(db_session, household.id, child.id, entry.id, "approve", user.id)
    await _set_policy(db_session, household, user, "off")
    block = await get_active_entries_block(db_session, household.id, child.id)
    assert block == ""


# ── Extraction robustness ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_malformed_extraction_json_discarded(db_session, household, user, child):
    with patch(
        "app.ai.gateway.call_ai",
        new_callable=AsyncMock,
        return_value={"output": "not json at all {", "ai_run_id": str(uuid.uuid4())},
    ):
        created = await extract_and_route_proposals(db_session, household.id, child.id, "exchange")
    assert created == []


@pytest.mark.asyncio
async def test_extraction_routes_well_formed_proposals(db_session, household, user, child):
    payload = {
        "proposals": [
            {"category": "pacing", "content": "Short bursts with movement breaks work well", "confidence": 0.9},
            {"category": "bogus_category", "content": "should be dropped by validator", "confidence": 0.9},
        ]
    }
    with patch(
        "app.ai.gateway.call_ai",
        new_callable=AsyncMock,
        return_value={"output": payload, "ai_run_id": str(uuid.uuid4())},
    ):
        created = await extract_and_route_proposals(db_session, household.id, child.id, "exchange")
    assert len(created) == 1
    assert created[0].category == "pacing"
    assert created[0].status == "proposed"


# ── Chain integrity across a full lifecycle ─────────────────────────


@pytest.mark.asyncio
async def test_chain_valid_after_full_lifecycle(auth_client: AsyncClient, db_session, household, user, child):
    proposed = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    await decide_entry(db_session, household.id, child.id, proposed.id, "approve", user.id)
    await revoke_entry(db_session, household.id, child.id, proposed.id, user.id)
    await _set_policy(db_session, household, user, "autonomous")
    auto = await route_proposal(
        db_session, household.id, child.id, {"category": "interest", "content": "Music references keep focus high"}
    )
    assert auto is not None and auto.status == "active"

    response = await auth_client.get("/api/v1/chain/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["checked"] >= 6


# ── Endpoints and access control ────────────────────────────────────


@pytest.mark.asyncio
async def test_get_endpoint_groups_by_status(auth_client: AsyncClient, db_session, household, user, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    response = await auth_client.get(f"/api/v1/children/{child.id}/tutor-profile")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["proposed"]) == 1
    assert data["proposed"][0]["id"] == str(entry.id)
    assert data["active"] == [] and data["rejected"] == [] and data["revoked"] == []


@pytest.mark.asyncio
async def test_decide_and_revoke_endpoints(auth_client: AsyncClient, db_session, household, user, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    approved = await auth_client.post(
        f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/decide", json={"action": "approve"}
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "active"

    repeat = await auth_client.post(
        f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/decide", json={"action": "reject"}
    )
    assert repeat.status_code == 409

    revoked = await auth_client.post(f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/revoke")
    assert revoked.status_code == 200
    assert revoked.json()["status"] == "revoked"

    twice = await auth_client.post(f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/revoke")
    assert twice.status_code == 409


@pytest.mark.asyncio
async def test_household_isolation(client: AsyncClient, db_session, household, user, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))

    other = Household(name="Other Family", timezone="UTC")
    db_session.add(other)
    await db_session.flush()
    from app.core.database import set_tenant

    await set_tenant(db_session, other.id)
    other_user = User(
        household_id=other.id,
        email="other-tutor@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Other",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(other_user.id, other.id, "owner"))

    read = await client.get(f"/api/v1/children/{child.id}/tutor-profile")
    assert read.status_code == 404
    decide = await client.post(
        f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/decide", json={"action": "approve"}
    )
    assert decide.status_code == 404


@pytest.mark.asyncio
async def test_child_scope_denied_on_all_endpoints(auth_client: AsyncClient, db_session, household, child):
    entry = await route_proposal(db_session, household.id, child.id, dict(GOOD_PROPOSAL))
    enter = await auth_client.post("/api/v1/auth/child-session/enter", json={"child_id": str(child.id)})
    assert enter.status_code == 200
    for method, path in (
        ("GET", f"/api/v1/children/{child.id}/tutor-profile"),
        ("POST", f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/decide"),
        ("POST", f"/api/v1/children/{child.id}/tutor-profile/{entry.id}/revoke"),
    ):
        response = await auth_client.request(method, path, json={"action": "approve"} if "decide" in path else None)
        assert response.status_code == 403, path
        assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_unverified_email_denied(client: AsyncClient, db_session, household, child):
    unverified = User(
        household_id=household.id,
        email="unverified-tutor@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Unverified",
        role="owner",
        email_verified=False,
    )
    db_session.add(unverified)
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(unverified.id, household.id, "owner"))
    response = await client.get(f"/api/v1/children/{child.id}/tutor-profile")
    assert response.status_code == 403
    assert response.json() == {"detail": "email_not_verified"}


# ── Single-writer guard ─────────────────────────────────────────────


def test_no_code_outside_service_writes_tutor_profile_entries():
    """Mirrors the GovernanceEvent single-writer guard: only the model
    definition and services/tutor_profile.py may construct
    TutorProfileEntry."""
    app_dir = Path(__file__).resolve().parents[1] / "app"
    allowed = {"app/models/intelligence.py", "app/services/tutor_profile.py"}
    pattern = re.compile(r"\bTutorProfileEntry\(")
    offenders = []
    for path in app_dir.rglob("*.py"):
        rel = path.relative_to(app_dir.parent).as_posix()
        if rel in allowed:
            continue
        if pattern.search(path.read_text()):
            offenders.append(rel)
    assert offenders == [], f"TutorProfileEntry must only be written through services/tutor_profile.py: {offenders}"
