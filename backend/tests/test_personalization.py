"""Personalization feature tests.

Covers data model, library, API endpoints, AI prompt rendering, and
the legacy /theme proxy. Migration round-trip is asserted
structurally; the live ``alembic upgrade/downgrade`` cycle is run in
CI per the project verification script.
"""

import importlib.util
import pathlib
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import PersonalizationContext, load_personalization_context
from app.ai.prompts import TUTOR_SYSTEM, render_tutor_system
from app.content.personalization_library import (
    AFFIRMATION_TONES,
    ICONOGRAPHY_PACKS,
    INTEREST_TAGS,
    SOUND_PACKS,
    VIBES,
    VOICE_PERSONAS,
    expand_allowlist,
    get_interest_tag,
)
from app.models.governance import GovernanceEvent
from app.models.identity import Child, ChildPreferences, Household, PersonalizationPolicy

# ── Migration structural smoke ────────────────────────────────────


def test_migration_upgrade_downgrade_clean():
    """Structural smoke: the migration module declares both upgrade
    and downgrade callables and the revision metadata points at
    042. The real alembic round-trip is exercised by the CI
    verification script (``alembic upgrade head; downgrade -1;
    upgrade head``)."""
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    path = repo_root / "alembic" / "versions" / "043_personalization.py"
    spec = importlib.util.spec_from_file_location("_mig_043_personalization", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.revision == "043"
    assert mod.down_revision == "042"
    assert callable(mod.upgrade)
    assert callable(mod.downgrade)


# ── Library content shape ─────────────────────────────────────────


def test_library_content_counts():
    """The spec mandates specific counts so the frontend can rely on
    them. Bumping any number is a coordinated change."""
    assert len(VIBES) == 6
    assert len(INTEREST_TAGS) >= 40
    assert len(VOICE_PERSONAS) == 5
    assert len(ICONOGRAPHY_PACKS) == 5
    assert len(SOUND_PACKS) == 3
    assert len(AFFIRMATION_TONES) == 3


def test_expand_allowlist_sentinel():
    assert expand_allowlist(["*"], ["a", "b", "c"]) == {"a", "b", "c"}
    assert expand_allowlist(["a"], ["a", "b", "c"]) == {"a"}
    assert expand_allowlist([], ["a", "b", "c"]) == set()


# ── Library endpoint ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_library_endpoint_returns_full_library_for_household_with_no_policy(
    auth_client: AsyncClient,
):
    resp = await auth_client.get("/api/v1/personalization/library")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["vibes"]) == 6
    assert len(body["interest_tags"]) >= 40
    assert all(v["available"] is True for v in body["vibes"])
    assert all(t["available"] is True for t in body["interest_tags"])
    assert body["max_interest_tags_per_child"] == 5


@pytest.mark.asyncio
async def test_library_endpoint_respects_policy_when_set(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    household: Household,
):
    db_session.add(
        PersonalizationPolicy(
            household_id=household.id,
            allowed_vibes=["calm"],
        )
    )
    await db_session.flush()

    resp = await auth_client.get("/api/v1/personalization/library")
    assert resp.status_code == 200
    body = resp.json()
    vibe_availability = {v["id"]: v["available"] for v in body["vibes"]}
    assert vibe_availability["calm"] is True
    assert all(not avail for vid, avail in vibe_availability.items() if vid != "calm")


# ── Per-child profile ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_child_personalization_returns_defaults_when_unset(
    auth_client: AsyncClient,
    child: Child,
):
    resp = await auth_client.get(f"/api/v1/children/{child.id}/personalization")
    assert resp.status_code == 200
    body = resp.json()
    assert body["companion_name"] == ""
    assert body["companion_voice"] == ""
    assert body["vibe"] == "calm"
    assert body["iconography_pack"] == "default"
    assert body["sound_pack"] == "soft"
    assert body["affirmation_tone"] == "warm"
    assert body["interest_tags"] == []
    assert body["out_of_policy"] == []
    assert body["onboarded"] is False


@pytest.mark.asyncio
async def test_child_personalization_update_persists_and_returns_resolved_profile(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    child: Child,
):
    payload = {
        "companion_name": "Spark",
        "companion_voice": "default_warm",
        "vibe": "field",
        "iconography_pack": "field",
        "sound_pack": "soft",
        "affirmation_tone": "warm",
        "interest_tags": ["trains", "dinosaurs"],
        "onboarded": True,
    }
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json=payload,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["companion_name"] == "Spark"
    assert body["vibe"] == "field"
    assert sorted(body["interest_tags"]) == ["dinosaurs", "trains"]
    assert body["onboarded"] is True

    # Re-read to confirm persistence.
    resp = await auth_client.get(f"/api/v1/children/{child.id}/personalization")
    assert resp.status_code == 200
    body = resp.json()
    assert body["vibe"] == "field"

    # ChildPreferences row exists with the expected JSONB.
    result = await db_session.execute(select(ChildPreferences).where(ChildPreferences.child_id == child.id))
    prefs = result.scalar_one()
    assert prefs.personalization["vibe"] == "field"
    assert prefs.personalization["companion_name"] == "Spark"
    assert sorted(prefs.interests or []) == ["dinosaurs", "trains"]


@pytest.mark.asyncio
async def test_child_personalization_update_rejects_unknown_vibe_with_400(
    auth_client: AsyncClient,
    child: Child,
):
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={"vibe": "nightmare_mode"},
    )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["field"] == "vibe"
    assert detail["value"] == "nightmare_mode"
    assert detail["reason"] == "unknown library entry"


@pytest.mark.asyncio
async def test_child_personalization_update_rejects_disallowed_vibe_with_403(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    household: Household,
    child: Child,
):
    db_session.add(PersonalizationPolicy(household_id=household.id, allowed_vibes=["calm"]))
    await db_session.flush()
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={"vibe": "bold"},
    )
    assert resp.status_code == 403
    detail = resp.json()["detail"]
    assert detail["field"] == "vibe"
    assert detail["value"] == "bold"
    assert detail["reason"] == "outside policy"
    assert "calm" in detail["allowed"]


@pytest.mark.asyncio
async def test_child_personalization_update_rejects_too_many_interests(
    auth_client: AsyncClient,
    child: Child,
):
    # Default policy caps at 5; 6 must fail with 400.
    sample_ids = [t.id for t in INTEREST_TAGS[:6]]
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={"interest_tags": sample_ids},
    )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["field"] == "interest_tags"
    assert detail["max"] == 5
    assert detail["reason"] == "too many interest tags"


@pytest.mark.asyncio
async def test_child_personalization_update_with_review_required_stores_pending_not_active(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    household: Household,
    child: Child,
):
    db_session.add(
        PersonalizationPolicy(
            household_id=household.id,
            companion_name_requires_review=True,
        )
    )
    await db_session.flush()

    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={"companion_name": "Cinder"},
    )
    assert resp.status_code == 200
    body = resp.json()
    # Active companion_name must NOT be updated.
    assert body["companion_name"] == ""

    # Pending value should be on the JSONB blob.
    result = await db_session.execute(select(ChildPreferences).where(ChildPreferences.child_id == child.id))
    prefs = result.scalar_one()
    assert prefs.personalization.get("companion_name_pending") == "Cinder"
    assert prefs.personalization.get("companion_name") in (None, "")

    # An audit event should exist with the pending value.
    result = await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.target_type == "personalization"))
    events = result.scalars().all()
    assert any(
        e.reason == "companion_name_pending_review"
        and e.metadata_
        and e.metadata_.get("pending_companion_name") == "Cinder"
        for e in events
    )


# ── Policy endpoints ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_policy_update_requires_guardian(
    observer_client: AsyncClient,
):
    resp = await observer_client.put(
        "/api/v1/personalization/policy",
        json={"max_interest_tags_per_child": 3},
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_policy_update_writes_audit_log(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    household: Household,
):
    resp = await auth_client.put(
        "/api/v1/personalization/policy",
        json={"allowed_vibes": ["calm", "field"], "max_interest_tags_per_child": 7},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert sorted(body["allowed_vibes"]) == ["calm", "field"]
    assert body["max_interest_tags_per_child"] == 7

    result = await db_session.execute(
        select(GovernanceEvent).where(
            GovernanceEvent.target_type == "personalization",
            GovernanceEvent.target_id == household.id,
        )
    )
    events = result.scalars().all()
    assert any(e.reason == "personalization_policy_updated" for e in events)
    # The diff metadata should reflect what changed.
    diffs = [e.metadata_ or {} for e in events if e.reason == "personalization_policy_updated"]
    assert any("diff" in d for d in diffs)


@pytest.mark.asyncio
async def test_policy_update_rejects_unknown_id_with_400(
    auth_client: AsyncClient,
):
    resp = await auth_client.put(
        "/api/v1/personalization/policy",
        json={"allowed_vibes": ["calm", "bogus_vibe"]},
    )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["field"] == "allowed_vibes"
    assert detail["value"] == "bogus_vibe"


# ── out_of_policy flagging ────────────────────────────────────────


@pytest.mark.asyncio
async def test_out_of_policy_flag_appears_when_tightening_after_selection(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    household: Household,
    child: Child,
):
    # 1. Kid picks "bold" while policy is wide open.
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={"vibe": "bold"},
    )
    assert resp.status_code == 200
    assert resp.json()["out_of_policy"] == []

    # 2. Parent tightens the policy to disallow "bold".
    policy = PersonalizationPolicy(household_id=household.id, allowed_vibes=["calm"])
    db_session.add(policy)
    await db_session.flush()

    # 3. The next read flags vibe as out_of_policy.
    resp = await auth_client.get(f"/api/v1/children/{child.id}/personalization")
    body = resp.json()
    assert body["vibe"] == "bold"
    assert "vibe" in body["out_of_policy"]


# ── Legacy theme proxy ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_legacy_theme_route_proxies_to_personalization(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    child: Child,
):
    # Set vibe via the new API.
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={"vibe": "orbit"},
    )
    assert resp.status_code == 200

    # Legacy GET reads the mapped background.
    resp = await auth_client.get(f"/api/v1/children/{child.id}/theme")
    assert resp.status_code == 200
    assert resp.json()["background"] == "ocean"

    # Legacy PUT writes back through the proxy.
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/theme",
        json={"background": "forest", "avatar": "fox", "font_size": "large"},
    )
    assert resp.status_code == 200
    assert resp.json()["background"] == "forest"
    assert resp.json()["avatar"] == "fox"

    # The new personalization endpoint should now reflect vibe=field
    # (reverse-mapped) and legacy_theme should NOT leak into the
    # public profile shape.
    resp = await auth_client.get(f"/api/v1/children/{child.id}/personalization")
    body = resp.json()
    assert body["vibe"] == "field"
    assert "legacy_theme" not in body


# ── render_tutor_system ───────────────────────────────────────────


def test_render_tutor_system_with_empty_context_falls_back_gracefully():
    out = render_tutor_system(PersonalizationContext())
    assert "your learning companion" in out
    # The Socratic-tutor mission anchor must always render.
    assert "METHEAN Socratic Tutor" in out


def test_render_tutor_system_with_full_context_contains_companion_and_interests():
    trains = get_interest_tag("trains")
    dinos = get_interest_tag("dinosaurs")
    assert trains is not None and dinos is not None
    ctx = PersonalizationContext(
        companion_name="Sparky",
        companion_voice_tone="Calm, encouraging.",
        affirmation_tone="Warm, focused on effort.",
        interests=[trains, dinos],
    )
    out = render_tutor_system(ctx)
    assert "Sparky" in out
    assert "Calm, encouraging." in out
    assert "Warm, focused on effort." in out
    assert "trains" in out.lower()
    assert "dinosaur" in out.lower() or "paleontology" in out.lower()


def test_render_tutor_system_preserves_existing_rules():
    """All key Socratic-tutor rules must survive personalization."""
    out = render_tutor_system(PersonalizationContext(companion_name="Sage"))
    must_contain = [
        "NEVER give the answer directly",
        "Ask ONE guiding question at a time",
        "SCAFFOLD",
        "CELEBRATE effort and thinking",
        "Match language to developmental level",
        "OUTPUT FORMAT",
    ]
    for phrase in must_contain:
        assert phrase in out, f"Personalization stripped rule: {phrase!r}"
    # Also confirm the original constant is unchanged so legacy
    # imports of TUTOR_SYSTEM still see the full unmodified prompt.
    for phrase in must_contain:
        assert phrase in TUTOR_SYSTEM


# ── Gateway helper ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_load_personalization_context_resolves_library_entries(
    auth_client: AsyncClient,
    db_session: AsyncSession,
    child: Child,
):
    await auth_client.put(
        f"/api/v1/children/{child.id}/personalization",
        json={
            "companion_name": "Bo",
            "companion_voice": "default_steady",
            "affirmation_tone": "direct",
            "interest_tags": ["coding"],
        },
    )
    ctx = await load_personalization_context(db_session, child.id)
    assert ctx.companion_name == "Bo"
    assert "Measured" in ctx.companion_voice_tone
    assert "Brief" in ctx.affirmation_tone
    assert any(t.id == "coding" for t in ctx.interests)


@pytest.mark.asyncio
async def test_load_personalization_context_handles_missing_row(
    db_session: AsyncSession,
):
    # No preferences row written. Helper must degrade to empty values.
    fake_id = uuid.uuid4()
    ctx = await load_personalization_context(db_session, fake_id)
    assert ctx.companion_name == ""
    assert ctx.companion_voice_tone == ""
    assert ctx.affirmation_tone == ""
    assert ctx.interests == []


# ── Schema-level checks ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_personalization_column_exists_in_child_preferences(
    db_session: AsyncSession,
):
    result = await db_session.execute(
        text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'child_preferences' AND column_name = 'personalization'"
        )
    )
    assert result.scalar_one_or_none() == "personalization"


@pytest.mark.asyncio
async def test_personalization_policy_table_has_rls_enabled(
    db_session: AsyncSession,
):
    result = await db_session.execute(
        text("SELECT rowsecurity FROM pg_tables WHERE tablename = 'personalization_policy'")
    )
    enabled = result.scalar_one_or_none()
    assert enabled is True
