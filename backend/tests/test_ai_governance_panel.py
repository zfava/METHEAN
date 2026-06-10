"""Tests for the per-role AI autonomy policy and governance panel.

Covers migration 056: policy defaults, legal and illegal transitions,
grant and revoke events on the hash chain, gateway enforcement of off
(including the education_architect native carve-out), the status
endpoint's key hygiene, spend aggregation, and access control.
"""

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select

from app.ai.gateway import AIRole, AIRoleDisabledError, call_ai
from app.core import cache as cache_module
from app.core.security import create_access_token, hash_password
from app.models.enums import AIRunStatus
from app.models.governance import GovernanceEvent, HouseholdAIRoleSetting
from app.models.identity import Household, User
from app.models.operational import AIRun
from app.services.governance import (
    ALLOWED_AUTONOMY,
    get_active_autonomy_grant,
    get_ai_role_policy,
    set_ai_role_policy,
)

PASSWORD = "testpass123"


class _DictRedis:
    """Dict-backed stand-in so the policy cache actually caches."""

    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        self.store[key] = value

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)


@pytest_asyncio.fixture
async def policy_cache():
    fake = _DictRedis()
    cache_module.init_cache(fake)
    yield fake
    cache_module._redis = None


# ── Defaults and transitions ────────────────────────────────────────


@pytest.mark.asyncio
async def test_default_state_all_roles_standard(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/governance/ai-settings")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["roles"]) == 8
    for role in data["roles"]:
        assert role["autonomy"] == "standard"
        assert role["description"]
        assert "off" in role["allowed"] and "standard" in role["allowed"]
    tutor = next(r for r in data["roles"] if r["role"] == "tutor")
    assert tutor["allowed"] == ["off", "standard", "autonomous"]
    assert set(data["autonomy_levels"].keys()) == {"off", "standard", "autonomous"}


@pytest.mark.asyncio
async def test_put_toggles_persist_and_log_events(auth_client: AsyncClient, db_session, household):
    response = await auth_client.put(
        "/api/v1/governance/ai-settings", json={"role": "planner", "autonomy": "off"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"role": "planner", "autonomy": "off", "old_autonomy": "standard"}

    settings_response = await auth_client.get("/api/v1/governance/ai-settings")
    planner = next(r for r in settings_response.json()["roles"] if r["role"] == "planner")
    assert planner["autonomy"] == "off"
    assert planner["updated_at"] is not None

    events = (
        await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.household_id == household.id,
                GovernanceEvent.target_type == "ai_role_policy_changed",
            )
        )
    ).scalars().all()
    assert len(events) == 1
    assert events[0].metadata_["role"] == "planner"
    assert events[0].metadata_["old"] == "standard"
    assert events[0].metadata_["new"] == "off"
    assert events[0].event_hash, "policy events must ride the hash chain"

    back = await auth_client.put(
        "/api/v1/governance/ai-settings", json={"role": "planner", "autonomy": "standard"}
    )
    assert back.status_code == 200


@pytest.mark.asyncio
async def test_cache_invalidation_on_write(db_session, household, user, policy_cache):
    assert await get_ai_role_policy(db_session, household.id, "tutor") == "standard"
    assert policy_cache.store, "first read must populate the cache"

    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")
    # Second read reflects the write immediately (key was invalidated).
    assert await get_ai_role_policy(db_session, household.id, "tutor") == "off"


@pytest.mark.asyncio
async def test_autonomous_grant_and_revoke_events(auth_client: AsyncClient, db_session, household):
    granted = await auth_client.put(
        "/api/v1/governance/ai-settings", json={"role": "tutor", "autonomy": "autonomous"}
    )
    assert granted.status_code == 200, granted.text

    grant_events = (
        await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.household_id == household.id,
                GovernanceEvent.target_type == "ai_autonomy_granted",
            )
        )
    ).scalars().all()
    assert len(grant_events) == 1
    assert grant_events[0].metadata_["role"] == "tutor"
    assert grant_events[0].metadata_["scope"], "grant must carry plain-language scope text"
    assert grant_events[0].event_hash

    active = await get_active_autonomy_grant(db_session, household.id, "tutor")
    assert active == grant_events[0].event_hash

    revoked = await auth_client.put(
        "/api/v1/governance/ai-settings", json={"role": "tutor", "autonomy": "standard"}
    )
    assert revoked.status_code == 200
    revoke_events = (
        await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.household_id == household.id,
                GovernanceEvent.target_type == "ai_autonomy_revoked",
            )
        )
    ).scalars().all()
    assert len(revoke_events) == 1
    assert await get_active_autonomy_grant(db_session, household.id, "tutor") is None


@pytest.mark.asyncio
async def test_autonomous_on_non_tutor_role_is_422(auth_client: AsyncClient, db_session, household):
    response = await auth_client.put(
        "/api/v1/governance/ai-settings", json={"role": "planner", "autonomy": "autonomous"}
    )
    assert response.status_code == 422
    assert "planner" in response.json()["detail"]

    rows = (
        await db_session.execute(
            select(HouseholdAIRoleSetting).where(HouseholdAIRoleSetting.household_id == household.id)
        )
    ).scalars().all()
    assert rows == [], "rejected transition must not write a row"
    events = (
        await db_session.execute(
            select(GovernanceEvent).where(GovernanceEvent.household_id == household.id)
        )
    ).scalars().all()
    assert events == [], "rejected transition must not log an event"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {"role": "not_a_role", "autonomy": "standard"},
        {"role": "tutor", "autonomy": "supercharged"},
    ],
)
async def test_invalid_role_or_autonomy_is_422(auth_client: AsyncClient, body):
    response = await auth_client.put("/api/v1/governance/ai-settings", json=body)
    assert response.status_code == 422


def test_allowed_autonomy_covers_all_roles_and_never_defaults_autonomous():
    assert set(ALLOWED_AUTONOMY.keys()) == {r.value for r in AIRole}
    for role, allowed in ALLOWED_AUTONOMY.items():
        assert allowed[0] != "autonomous" and "standard" in allowed, role


# ── Gateway enforcement ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_role_off_blocks_provider_calls(db_session, household, user):
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")

    with patch("app.ai.gateway._call_mock") as mock_provider:
        with pytest.raises(AIRoleDisabledError) as exc:
            await call_ai(
                db_session,
                AIRole.tutor,
                "system",
                "user prompt",
                household.id,
                triggered_by=user.id,
            )
        mock_provider.assert_not_called()
    assert exc.value.role == "tutor"

    runs = (
        await db_session.execute(
            select(AIRun).where(AIRun.household_id == household.id, AIRun.run_type == "tutor")
        )
    ).scalars().all()
    assert len(runs) == 1
    assert runs[0].status == AIRunStatus.failed
    assert "parent policy" in runs[0].error_message


@pytest.mark.asyncio
@pytest.mark.parametrize("autonomy", ["standard", "autonomous"])
async def test_standard_and_autonomous_identical_at_gateway(
    db_session, household, user, autonomy
):
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", autonomy)
    result = await call_ai(
        db_session,
        AIRole.tutor,
        "system",
        "What is 2+2?",
        household.id,
        triggered_by=user.id,
        expected_json=False,
    )
    # The mock provider answered: the policy did not block the call.
    assert result["provider"] == "mock"
    assert result["output"]


@pytest.mark.asyncio
async def test_education_architect_off_keeps_native_curriculum_path(db_session, household, user):
    """The carve-out: native is curriculum, not AI advice. With the
    role off, the same call path the annual curriculum service uses
    still reaches the native provider (and never the LLM/mock ones)."""
    await set_ai_role_policy(db_session, household.id, user.id, "education_architect", "off")

    native_payload = {"weeks": {"1": {"summary": "native content"}}}
    with (
        patch(
            "app.services.native_curriculum_generator.build_native_response",
            new_callable=AsyncMock,
            return_value=native_payload,
        ) as native,
        patch("app.ai.gateway._call_mock") as mock_provider,
    ):
        result = await call_ai(
            db_session,
            AIRole.education_architect,
            "system",
            "generate annual curriculum",
            household.id,
            triggered_by=user.id,
        )
    native.assert_awaited_once()
    mock_provider.assert_not_called()
    assert result["provider"] == "native"
    assert result["output"] == native_payload


# ── Status endpoint ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_ai_status_never_leaks_key_material(auth_client: AsyncClient, monkeypatch):
    from app.core.config import settings as app_settings

    fake_key = "sk-ant-fake1234567890secret"
    monkeypatch.setattr(app_settings, "AI_API_KEY", fake_key)

    response = await auth_client.get("/api/v1/governance/ai-status")
    assert response.status_code == 200, response.text
    body = response.text
    assert fake_key not in body
    assert fake_key[:10] not in body
    data = response.json()
    assert data["providers"]["anthropic"]["configured"] is True
    assert data["providers"]["native"]["configured"] is True
    assert "native" in data["chain_order"]


@pytest.mark.asyncio
async def test_spend_aggregates_match_seeded_runs(auth_client: AsyncClient, db_session, household, user):
    from app.ai.cost_controls import estimate_cost_cents

    for tokens_in, tokens_out in ((1000, 500), (2000, 1000)):
        db_session.add(
            AIRun(
                household_id=household.id,
                triggered_by=user.id,
                run_type="planner",
                status=AIRunStatus.completed,
                input_tokens=tokens_in,
                output_tokens=tokens_out,
                started_at=datetime.now(UTC),
            )
        )
    await db_session.flush()

    response = await auth_client.get("/api/v1/governance/ai-status")
    data = response.json()
    planner = next(r for r in data["last_30_days"] if r["role"] == "planner")
    assert planner["calls"] == 2
    assert planner["input_tokens"] == 3000
    assert planner["output_tokens"] == 1500
    assert planner["estimated_cost_cents"] == estimate_cost_cents("claude-sonnet-4-20250514", 3000, 1500)
    assert data["today"]["tokens"] == 4500
    assert data["today"]["calls"] == 2


# ── Access control ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_household_isolation(client: AsyncClient, db_session, household, user, policy_cache):
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")

    other = Household(name="Other Family", timezone="UTC")
    db_session.add(other)
    await db_session.flush()
    from app.core.database import set_tenant

    await set_tenant(db_session, other.id)
    other_user = User(
        household_id=other.id,
        email="other-ai@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Other",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(other_user.id, other.id, "owner"))

    settings_response = await client.get("/api/v1/governance/ai-settings")
    assert settings_response.status_code == 200
    tutor = next(r for r in settings_response.json()["roles"] if r["role"] == "tutor")
    assert tutor["autonomy"] == "standard", "household A's policy must not leak into B"

    status_response = await client.get("/api/v1/governance/ai-status")
    assert status_response.status_code == 200
    assert status_response.json()["today"]["calls"] == 0


@pytest.mark.asyncio
async def test_child_scope_denied_on_all_three(auth_client: AsyncClient, child):
    enter = await auth_client.post("/api/v1/auth/child-session/enter", json={"child_id": str(child.id)})
    assert enter.status_code == 200
    for method, path, body in (
        ("GET", "/api/v1/governance/ai-settings", None),
        ("PUT", "/api/v1/governance/ai-settings", {"role": "tutor", "autonomy": "off"}),
        ("GET", "/api/v1/governance/ai-status", None),
    ):
        response = await auth_client.request(method, path, json=body)
        assert response.status_code == 403, path
        assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_unverified_email_denied(client: AsyncClient, db_session, household):
    unverified = User(
        household_id=household.id,
        email="unverified-ai@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Unverified",
        role="owner",
        email_verified=False,
    )
    db_session.add(unverified)
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(unverified.id, household.id, "owner"))

    response = await client.get("/api/v1/governance/ai-settings")
    assert response.status_code == 403
    assert response.json() == {"detail": "email_not_verified"}


@pytest.mark.asyncio
async def test_observer_cannot_change_policy(observer_client: AsyncClient):
    response = await observer_client.put(
        "/api/v1/governance/ai-settings", json={"role": "tutor", "autonomy": "off"}
    )
    assert response.status_code == 403


# ── Child-surface degradation ───────────────────────────────────────


@pytest.mark.asyncio
async def test_tutor_stream_off_returns_kind_message(
    auth_client: AsyncClient, db_session, household, user, child, learning_map
):
    from datetime import date

    from app.models.curriculum import LearningNode
    from app.models.enums import ActivityType, NodeType
    from app.models.governance import Activity, Plan, PlanWeek

    node = LearningNode(
        learning_map_id=learning_map.id, household_id=household.id, node_type=NodeType.concept, title="Math"
    )
    db_session.add(node)
    await db_session.flush()
    plan = Plan(household_id=household.id, child_id=child.id, name="P", status="active")
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 6, 8),
        end_date=date(2026, 6, 14),
    )
    db_session.add(week)
    await db_session.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        title="Practice",
        activity_type=ActivityType.practice,
        node_id=node.id,
    )
    db_session.add(activity)
    await db_session.flush()

    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")

    response = await auth_client.post(
        f"/api/v1/tutor/{activity.id}/stream",
        json={"child_id": str(child.id), "message": "help me", "conversation_history": []},
    )
    assert response.status_code == 200
    assert "ask your parent" in response.text.lower()
    assert "error" in response.text
