"""Tests for the developmental voice register.

Covers per-tier derivation from the child's content tier (subject scoped),
the absolute per-child parent override and its governance events, the
fail-closed fallback to the youngest register, injection into the tutor
context (present with the right guidance, gated only by the role being
off, present even with zero memory entries), tier_band stamping on new
entries, tier-lag retirement through the existing retire_entry pipeline,
the relationship_memory write rejection, and access control.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.learning_levels import VALID_LEVELS
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.governance import GovernanceEvent
from app.models.identity import ChildPreferences
from app.models.intelligence import ChildTutorPreferences, TutorProfileEntry
from app.services.governance import set_ai_role_policy
from app.services.learning_context import build_register_block
from app.services.tutor_efficacy import (
    EVT_RETIREMENT_PROPOSED,
    decide_retirement,
    maybe_propose_tier_lag_retirement,
)
from app.services.tutor_profile import route_proposal
from app.services.tutor_register import (
    FALLBACK_TIER,
    REGISTER_GUIDANCE,
    current_tier_for_child,
    resolve_register,
    tier_lag,
)

TIERS = ("foundational", "developing", "intermediate", "advanced", "mastery")


async def _prefs(db, household, child, levels: dict) -> ChildPreferences:
    p = ChildPreferences(child_id=child.id, household_id=household.id, subject_levels=levels)
    db.add(p)
    await db.flush()
    return p


async def _node(db, household, subject_name: str) -> LearningNode:
    s = Subject(household_id=household.id, name=subject_name)
    db.add(s)
    await db.flush()
    m = LearningMap(household_id=household.id, subject_id=s.id, name=f"{subject_name} Map")
    db.add(m)
    await db.flush()
    n = LearningNode(learning_map_id=m.id, household_id=household.id, node_type=NodeType.concept, title="Topic")
    db.add(n)
    await db.flush()
    return n


async def _active_entry(
    db, household, child, *, tier_band: str | None, content="Concrete blocks help"
) -> TutorProfileEntry:
    e = TutorProfileEntry(
        household_id=household.id,
        child_id=child.id,
        category="pacing",
        content=content,
        status="active",
        tier_band=tier_band,
    )
    db.add(e)
    await db.flush()
    return e


# ── 1. Derivation per tier ──────────────────────────────────────────────


@pytest.mark.parametrize("tier", TIERS)
@pytest.mark.asyncio
async def test_derivation_per_tier(db_session, household, child, tier):
    await _prefs(db_session, household, child, {"mathematics": tier})
    rt, guidance, source = await resolve_register(db_session, child.id, "Mathematics")
    assert rt == tier
    assert guidance == REGISTER_GUIDANCE[tier]
    assert source == "derived"


@pytest.mark.asyncio
async def test_subject_scoped_when_tiers_differ(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "advanced", "latin": "foundational"})
    math_tier, _, _ = await resolve_register(db_session, child.id, "Mathematics")
    latin_tier, _, _ = await resolve_register(db_session, child.id, "Latin")
    assert math_tier == "advanced"
    assert latin_tier == "foundational"


# ── 2. Override is absolute ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_override_beats_derivation(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "foundational"})
    db_session.add(ChildTutorPreferences(household_id=household.id, child_id=child.id, register_override="mastery"))
    await db_session.flush()
    rt, guidance, source = await resolve_register(db_session, child.id, "Mathematics")
    assert rt == "mastery"
    assert guidance == REGISTER_GUIDANCE["mastery"]
    assert source == "override"


# ── 3. Fail closed to the youngest ───────────────────────────────────────


@pytest.mark.asyncio
async def test_unresolvable_falls_back_foundational_no_subject(db_session, household, child):
    rt, guidance, source = await resolve_register(db_session, child.id, None)
    assert rt == FALLBACK_TIER == "foundational"
    assert guidance == REGISTER_GUIDANCE["foundational"]
    assert source == "derived"


@pytest.mark.asyncio
async def test_unresolvable_falls_back_foundational_no_prefs(db_session, household, child):
    # Subject named but the child has no tier data: still youngest.
    rt, _, _ = await resolve_register(db_session, child.id, "Mathematics")
    assert rt == "foundational"


# ── 4. Injection into tutor context ──────────────────────────────────────


@pytest.mark.asyncio
async def test_register_block_uses_subject_tier(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate"})
    node = await _node(db_session, household, "Mathematics")
    block = await build_register_block(db_session, household.id, child.id, "tutor", node_id=node.id)
    assert "TUTOR VOICE REGISTER" in block
    assert "Stage: Intermediate" in block
    assert REGISTER_GUIDANCE["intermediate"] in block


@pytest.mark.asyncio
async def test_register_absent_when_role_off(db_session, household, user, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate"})
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")
    block = await build_register_block(db_session, household.id, child.id, "tutor", node_id=None)
    assert block == ""


@pytest.mark.asyncio
async def test_register_absent_for_non_tutor_role(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate"})
    block = await build_register_block(db_session, household.id, child.id, "evaluator", node_id=None)
    assert block == ""


@pytest.mark.asyncio
async def test_register_present_even_with_zero_entries(db_session, household, child):
    # No tutor profile entries exist; the register is presentation, not
    # memory, so it still appears (youngest fallback when no node).
    block = await build_register_block(db_session, household.id, child.id, "tutor", node_id=None)
    assert "TUTOR VOICE REGISTER" in block
    assert REGISTER_GUIDANCE["foundational"] in block


@pytest.mark.asyncio
async def test_override_changes_assembled_context(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate"})
    node = await _node(db_session, household, "Mathematics")
    before = await build_register_block(db_session, household.id, child.id, "tutor", node_id=node.id)
    assert "Stage: Intermediate" in before
    db_session.add(
        ChildTutorPreferences(household_id=household.id, child_id=child.id, register_override="foundational")
    )
    await db_session.flush()
    after = await build_register_block(db_session, household.id, child.id, "tutor", node_id=node.id)
    assert "Stage: Foundational" in after


# ── 5. tier_band stamping ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_new_proposal_stamped_with_tier_band(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate", "latin": "developing"})
    entry = await route_proposal(
        db_session, household.id, child.id, {"category": "pacing", "content": "Short bursts keep momentum"}
    )
    assert entry is not None
    # Furthest reach across subjects.
    assert entry.tier_band == "intermediate"


@pytest.mark.asyncio
async def test_tier_band_none_without_tier_data(db_session, household, child):
    entry = await route_proposal(
        db_session, household.id, child.id, {"category": "pacing", "content": "Short bursts keep momentum"}
    )
    assert entry is not None
    assert entry.tier_band is None


# ── 6. Tier-lag retirement ───────────────────────────────────────────────


async def _retirement_reason(db, entry_id) -> str | None:
    ev = (
        (
            await db.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.target_id == entry_id,
                    GovernanceEvent.target_type == EVT_RETIREMENT_PROPOSED,
                )
            )
        )
        .scalars()
        .all()
    )
    return ev[-1].reason if ev else None


@pytest.mark.asyncio
async def test_tier_lag_two_tiers_proposes_once_with_both_stages(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate"})
    entry = await _active_entry(db_session, household, child, tier_band="foundational")

    routed = await maybe_propose_tier_lag_retirement(db_session, entry)
    assert routed is not None
    reason = await _retirement_reason(db_session, entry.id)
    assert reason is not None
    assert "Foundational" in reason and "Intermediate" in reason

    # Exactly one: a second attempt sees the pending proposal and stops.
    again = await maybe_propose_tier_lag_retirement(db_session, entry)
    assert again is None


@pytest.mark.asyncio
async def test_one_tier_lag_does_not_trigger(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate"})
    entry = await _active_entry(db_session, household, child, tier_band="developing")
    routed = await maybe_propose_tier_lag_retirement(db_session, entry)
    assert routed is None


@pytest.mark.asyncio
async def test_tier_lag_lifetime_cap_honored(db_session, household, user, child):
    await _prefs(db_session, household, child, {"mathematics": "advanced"})
    entry = await _active_entry(db_session, household, child, tier_band="foundational")

    first = await maybe_propose_tier_lag_retirement(db_session, entry)
    assert first is not None
    await decide_retirement(db_session, household.id, child.id, entry.id, "reject", user.id)

    second = await maybe_propose_tier_lag_retirement(db_session, entry)
    assert second is not None, "a second proposal is allowed after a rejection"
    await decide_retirement(db_session, household.id, child.id, entry.id, "reject", user.id)

    third = await maybe_propose_tier_lag_retirement(db_session, entry)
    assert third is None, "lifetime cap of two is honored"


def test_tier_lag_helper_distance():
    assert tier_lag("intermediate", "foundational") == 2
    assert tier_lag("developing", "intermediate") == -1
    assert tier_lag("mastery", None) is None


# ── 7. Preferences API ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_returns_derived_per_subject(auth_client: AsyncClient, db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "advanced", "latin": "foundational"})
    resp = await auth_client.get(f"/api/v1/children/{child.id}/tutor-register")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["derived_by_subject"]["mathematics"] == "advanced"
    assert body["derived_by_subject"]["latin"] == "foundational"
    assert body["register_override"] is None
    assert body["relationship_memory"] == "off"
    assert body["effective_tier"] == "advanced"
    assert body["source"] == "derived"


@pytest.mark.asyncio
async def test_put_override_set_and_clear_log_events(auth_client: AsyncClient, db_session, household, user, child):
    await _prefs(db_session, household, child, {"mathematics": "foundational"})

    set_resp = await auth_client.put(
        f"/api/v1/children/{child.id}/tutor-register", json={"register_override": "advanced"}
    )
    assert set_resp.status_code == 200, set_resp.text
    assert set_resp.json()["register_override"] == "advanced"
    assert set_resp.json()["effective_tier"] == "advanced"
    assert set_resp.json()["source"] == "override"

    clear_resp = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"register_override": None})
    assert clear_resp.status_code == 200
    assert clear_resp.json()["register_override"] is None
    assert clear_resp.json()["source"] == "derived"

    types = {
        row[0]
        for row in (
            await db_session.execute(
                select(GovernanceEvent.target_type).where(GovernanceEvent.household_id == household.id)
            )
        ).all()
    }
    assert "tutor_register_override_set" in types
    assert "tutor_register_override_cleared" in types


@pytest.mark.asyncio
async def test_invalid_override_rejected(auth_client: AsyncClient, child):
    resp = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"register_override": "genius"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_relationship_memory_write_rejected(auth_client: AsyncClient, child):
    resp = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "on"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_relationship_memory_column_defaults_off(auth_client: AsyncClient, db_session, household, child):
    await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"register_override": "intermediate"})
    ctp = (
        await db_session.execute(select(ChildTutorPreferences).where(ChildTutorPreferences.child_id == child.id))
    ).scalar_one()
    assert ctp.relationship_memory == "off"


@pytest.mark.asyncio
async def test_chain_valid_after_override_lifecycle(auth_client: AsyncClient, child):
    await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"register_override": "intermediate"})
    await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"register_override": None})
    resp = await auth_client.get("/api/v1/chain/verify")
    assert resp.status_code == 200
    assert resp.json()["valid"] is True


# ── 8. Access control ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_child_scope_denied(client: AsyncClient, household, user, child):
    from app.core.security import create_access_token

    token = create_access_token(user.id, household.id, "owner", scope="child", child_id=child.id)
    client.cookies.set("access_token", token)
    resp = await client.get(f"/api/v1/children/{child.id}/tutor-register")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_household_isolation(client: AsyncClient, db_session, household, child):
    from app.core.database import set_tenant
    from app.core.security import create_access_token, hash_password
    from app.models.identity import Household, User

    other = Household(name="Other Family", subscription_status="trialing")
    db_session.add(other)
    await db_session.flush()
    await set_tenant(db_session, other.id)
    other_user = User(
        household_id=other.id,
        email="other-register@test.com",
        password_hash=hash_password("testpass123"),
        display_name="Other Parent",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()

    token = create_access_token(other_user.id, other.id, "owner")
    client.cookies.set("access_token", token)
    resp = await client.get(f"/api/v1/children/{child.id}/tutor-register")
    assert resp.status_code == 404


# ── 9. current_tier_for_child helper ─────────────────────────────────────


@pytest.mark.asyncio
async def test_current_tier_is_furthest_reach(db_session, household, child):
    await _prefs(db_session, household, child, {"mathematics": "intermediate", "latin": "developing"})
    assert await current_tier_for_child(db_session, child.id) == "intermediate"
    assert await current_tier_for_child(db_session, child.id, "Latin") == "developing"
    assert await current_tier_for_child(db_session, child.id) in VALID_LEVELS
