"""Per-household entitlement gate for native-curriculum generation/materialization.

The native-library curriculum generation/materialization path (the
"Approve and Create" / generate-year-plan endpoints that fire the NATIVE
provider when API keys are blank) is gated behind a per-household boolean
entitlement, ``Household.native_curriculum_access``, default OFF and
server-enforced.

These tests prove:
- the entitlement defaults FALSE on a freshly created household;
- the capabilities endpoint (``GET /household/settings``) reflects the value;
- an UNENTITLED household gets 403 on both gated routes, with NO side effects
  (no draft generated, no materialization);
- an ENTITLED household reaches the existing native path unchanged (generate
  then approve materializes real weeks).

The gate is at the route handler, not the client: the unentitled 403 holds
against a direct API call.
"""

import uuid

from sqlalchemy import func, select

from app.core.config import settings
from app.models.annual_curriculum import AnnualCurriculum
from app.models.governance import Activity, Plan, PlanWeek
from app.services.annual_curriculum import generate_annual_curriculum


def _force_native_path(monkeypatch) -> None:
    """Blank keys + mock disabled => the generator routes through the NATIVE
    provider, exactly as the existing native-generation tests configure it."""
    monkeypatch.setattr(settings, "AI_API_KEY", "")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)


# ── Default OFF ──────────────────────────────────────────────────────────


async def test_entitlement_defaults_false_on_fresh_household(household):
    """A freshly created household has the entitlement OFF (dark by default)."""
    assert household.native_curriculum_access is False


# ── Capabilities endpoint reflects the value ─────────────────────────────


async def test_capabilities_endpoint_reflects_unentitled(auth_client):
    resp = await auth_client.get("/api/v1/household/settings")
    assert resp.status_code == 200
    assert resp.json()["native_curriculum_access"] is False


async def test_capabilities_endpoint_reflects_entitled(auth_client, household, db_session):
    household.native_curriculum_access = True
    await db_session.commit()
    resp = await auth_client.get("/api/v1/household/settings")
    assert resp.status_code == 200
    assert resp.json()["native_curriculum_access"] is True


# ── UNENTITLED: 403 with no side effects on the GENERATE route ───────────


async def test_unentitled_generate_route_returns_403_no_side_effects(auth_client, household, child, db_session):
    assert household.native_curriculum_access is False

    resp = await auth_client.post(
        f"/api/v1/children/{child.id}/curricula/generate",
        json={"subject_name": "Mathematics", "academic_year": "2026-2027", "total_weeks": 6},
    )
    assert resp.status_code == 403
    assert resp.json()["detail"]["error"] == "native_curriculum_access_required"

    # No draft curriculum was written: the gate ran before any generation.
    count = await db_session.scalar(
        select(func.count()).select_from(AnnualCurriculum).where(AnnualCurriculum.household_id == household.id)
    )
    assert count == 0


# ── UNENTITLED: 403 with no materialization on the APPROVE route ─────────


async def test_unentitled_approve_route_returns_403_no_materialization(
    auth_client, household, child, user, db_session, monkeypatch
):
    """A draft exists (created at the service layer, which is not gated), but the
    unentitled household cannot materialize it through the API: 403 and zero
    Plan/PlanWeek rows."""
    _force_native_path(monkeypatch)
    curriculum = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Mathematics",
        academic_year="2026-2027",
        total_weeks=6,
        content_tier="foundational",
    )
    await db_session.commit()
    assert household.native_curriculum_access is False

    resp = await auth_client.post(f"/api/v1/curricula/{curriculum.id}/approve")
    assert resp.status_code == 403
    assert resp.json()["detail"]["error"] == "native_curriculum_access_required"

    # NOT materialized: the gate ran before approve_annual_curriculum.
    plan_count = await db_session.scalar(
        select(func.count()).select_from(Plan).where(Plan.annual_curriculum_id == curriculum.id)
    )
    assert plan_count == 0

    refreshed = await db_session.get(AnnualCurriculum, curriculum.id)
    assert refreshed is not None
    assert refreshed.status != "approved"


async def test_unentitled_approve_route_403_holds_against_direct_api_call(auth_client, household, child):
    """Even with a crafted (nonexistent) curriculum id, the entitlement gate
    fires first: the unentitled household never reaches the handler body."""
    assert household.native_curriculum_access is False
    resp = await auth_client.post(f"/api/v1/curricula/{uuid.uuid4()}/approve")
    assert resp.status_code == 403
    assert resp.json()["detail"]["error"] == "native_curriculum_access_required"


# ── ENTITLED: native path works unchanged ────────────────────────────────


async def test_entitled_generate_and_approve_materializes(auth_client, household, child, db_session, monkeypatch):
    """An entitled household reaches the existing native path: generate returns a
    draft and approve materializes real weeks (no behavior change)."""
    _force_native_path(monkeypatch)
    household.native_curriculum_access = True
    await db_session.commit()

    gen = await auth_client.post(
        f"/api/v1/children/{child.id}/curricula/generate",
        json={"subject_name": "Mathematics", "academic_year": "2026-2027", "total_weeks": 6},
    )
    assert gen.status_code == 201, gen.text
    curriculum_id = uuid.UUID(gen.json()["id"])

    appr = await auth_client.post(f"/api/v1/curricula/{curriculum_id}/approve")
    assert appr.status_code == 200, appr.text
    # Approval ran and recorded a timestamp; the real materialization proof is
    # the Plan/PlanWeek/Activity rows below.
    assert appr.json()["approved_at"] not in (None, "None")

    plan = (await db_session.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum_id))).scalar_one()
    week_count = await db_session.scalar(select(func.count()).select_from(PlanWeek).where(PlanWeek.plan_id == plan.id))
    activity_count = await db_session.scalar(
        select(func.count())
        .select_from(Activity)
        .join(PlanWeek, Activity.plan_week_id == PlanWeek.id)
        .where(PlanWeek.plan_id == plan.id)
    )
    assert week_count == 6
    assert activity_count > 0


# ── The gate is a per-household dial, not a permanent role ────────────────


async def test_entitlement_is_a_flippable_household_field(household, db_session):
    """Flipping the entitlement is a one-boolean data write on the household row,
    requiring no code change: off -> on -> off round-trips on the same column."""
    assert household.native_curriculum_access is False
    household.native_curriculum_access = True
    await db_session.commit()
    refreshed = await db_session.get(type(household), household.id)
    assert refreshed.native_curriculum_access is True
    refreshed.native_curriculum_access = False
    await db_session.commit()
    again = await db_session.get(type(household), household.id)
    assert again.native_curriculum_access is False
