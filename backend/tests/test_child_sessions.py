"""Tests for child-scoped (kid mode) sessions.

Covers migration 053 and the kid-mode boundary: scope claims on access
tokens, the ChildScopeMiddleware fail-closed allowlist, dependency
level enforcement (require_role, require_child_access), the
/auth/pin and /auth/child-session/enter|exit endpoints, PIN attempt
lockout, and governance event logging.
"""

import uuid
from datetime import UTC, datetime, timedelta

import jwt as pyjwt
import pytest
import pytest_asyncio
from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.core import cache as cache_module
from app.core.config import settings
from app.core.security import create_access_token
from app.models.curriculum import LearningNode
from app.models.enums import ActivityType, NodeType
from app.models.governance import Activity, GovernanceEvent, Plan, PlanWeek
from app.models.identity import Child, Household, User

PIN = "2468"
WRONG_PIN = "1357"
PASSWORD = "testpass123"  # matches the conftest user fixture


class _DictRedis:
    """Minimal dict-backed stand-in for the cache module's redis client.

    The real cache helpers are fail-open no-ops without a client, which
    would make the PIN lockout untestable; this gives them real storage.
    """

    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        self.store[key] = value

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)


@pytest_asyncio.fixture
async def pin_cache():
    fake = _DictRedis()
    cache_module.init_cache(fake)
    yield fake
    cache_module._redis = None


@pytest_asyncio.fixture
async def activity(db_session: AsyncSession, household: Household, child: Child, learning_map) -> Activity:
    """A real plan/week/activity for the bound child, for lesson-flow tests."""
    from datetime import date

    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title="Addition",
    )
    db_session.add(node)
    await db_session.flush()
    plan = Plan(household_id=household.id, child_id=child.id, name="Test Plan", status="active")
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
    a = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        title="Practice Addition",
        activity_type=ActivityType.practice,
        node_id=node.id,
        estimated_minutes=20,
    )
    db_session.add(a)
    await db_session.flush()
    return a


async def _enter(client: AsyncClient, child_id: uuid.UUID):
    return await client.post("/api/v1/auth/child-session/enter", json={"child_id": str(child_id)})


async def _set_pin(client: AsyncClient, pin: str = PIN, password: str = PASSWORD):
    return await client.post("/api/v1/auth/pin", json={"current_password": password, "new_pin": pin})


def _restore_parent_cookie(client: AsyncClient, user: User, household: Household) -> None:
    token = create_access_token(user.id, household.id, "owner")
    client.cookies.set("access_token", token)


# ── Enter: scope and household boundaries ───────────────────────────


@pytest.mark.asyncio
async def test_enter_requires_parent_scope_no_nesting(auth_client: AsyncClient, child: Child):
    first = await _enter(auth_client, child.id)
    assert first.status_code == 200
    # The client now holds the child-scoped cookie: a second enter must
    # be rejected (middleware allowlist, before the endpoint even runs).
    second = await _enter(auth_client, child.id)
    assert second.status_code == 403
    assert second.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_enter_rejects_child_from_other_household(auth_client: AsyncClient, db_session, household):
    other_household = Household(name="Other Family", timezone="UTC")
    db_session.add(other_household)
    await db_session.flush()
    other_child = Child(household_id=other_household.id, first_name="Stranger")
    db_session.add(other_child)
    await db_session.flush()

    response = await _enter(auth_client, other_child.id)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_enter_sets_kid_mode_cookie_and_child_scope(auth_client: AsyncClient, child: Child):
    response = await _enter(auth_client, child.id)
    assert response.status_code == 200
    data = response.json()
    assert data["scope"] == "child"
    assert data["child_id"] == str(child.id)
    assert data["expires_in"] <= 12 * 3600
    set_cookies = response.headers.get_list("set-cookie")
    assert any(c.startswith("kid_mode=1") for c in set_cookies)
    kid_mode_cookie = next(c for c in set_cookies if c.startswith("kid_mode=1"))
    assert "httponly" not in kid_mode_cookie.lower()
    access_cookie = next(c for c in set_cookies if c.startswith("access_token="))
    assert "httponly" in access_cookie.lower()


# ── Child token: allowed surface ────────────────────────────────────


@pytest.mark.asyncio
async def test_child_token_allowed_on_dashboard(auth_client: AsyncClient, child: Child):
    assert (await _enter(auth_client, child.id)).status_code == 200
    response = await auth_client.get(f"/api/v1/children/{child.id}/dashboard")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_child_token_allowed_on_learn_context(auth_client: AsyncClient, child: Child, activity: Activity):
    assert (await _enter(auth_client, child.id)).status_code == 200
    response = await auth_client.get(f"/api/v1/activities/{activity.id}/learn?child_id={child.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_child_token_completes_attempt_flow_without_403(
    auth_client: AsyncClient, child: Child, activity: Activity
):
    """A child token can run the full attempt flow: start, save
    progress, submit. Not a single 403 anywhere in the loop."""
    assert (await _enter(auth_client, child.id)).status_code == 200

    start = await auth_client.post(
        f"/api/v1/activities/{activity.id}/attempts",
        json={"child_id": str(child.id)},
    )
    assert start.status_code == 201, start.text
    attempt_id = start.json()["id"]

    progress = await auth_client.post(
        f"/api/v1/attempts/{attempt_id}/progress",
        json={"notes": "halfway there"},
    )
    assert progress.status_code == 200, progress.text

    submit = await auth_client.put(
        f"/api/v1/attempts/{attempt_id}/submit",
        json={"confidence": 0.8, "duration_minutes": 15, "score": 0.9},
    )
    assert submit.status_code == 200, submit.text


# ── Child token: denied surface (fail closed) ───────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path",
    [
        ("GET", "/api/v1/governance/queue"),
        ("GET", "/api/v1/billing/status"),
        ("GET", "/api/v1/compliance/dashboard"),
        ("GET", "/api/v1/auth/household/invites"),
        ("POST", "/api/v1/auth/pin"),
    ],
)
async def test_child_token_denied_on_parent_surfaces(auth_client: AsyncClient, child: Child, method: str, path: str):
    assert (await _enter(auth_client, child.id)).status_code == 200
    response = await auth_client.request(method, path, json={} if method == "POST" else None)
    assert response.status_code == 403, f"{path} returned {response.status_code}"
    assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_child_token_mismatched_child_id_denied(auth_client: AsyncClient, child: Child, second_child: Child):
    assert (await _enter(auth_client, child.id)).status_code == 200
    response = await auth_client.get(f"/api/v1/children/{second_child.id}/dashboard")
    assert response.status_code == 403
    assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_child_token_denied_on_unlisted_child_path(auth_client: AsyncClient, child: Child):
    """Even paths for the bound child are denied unless allowlisted:
    the allowlist is fail-closed, not child-id based."""
    assert (await _enter(auth_client, child.id)).status_code == 200
    response = await auth_client.get(f"/api/v1/children/{child.id}/state")
    assert response.status_code == 403
    assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_require_role_fails_under_child_scope(user: User):
    user.token_scope = "child"
    user.token_child_id = uuid.uuid4()
    checker = require_role("owner", "co_parent")
    with pytest.raises(HTTPException) as exc:
        await checker(user=user)
    assert exc.value.status_code == 403
    assert exc.value.detail == "child_session_forbidden"


# ── Exit: PIN, password, lockout ────────────────────────────────────


@pytest.mark.asyncio
async def test_exit_with_correct_pin_restores_parent_scope(auth_client: AsyncClient, child: Child, pin_cache):
    assert (await _set_pin(auth_client)).status_code == 200
    assert (await _enter(auth_client, child.id)).status_code == 200
    # Sanity: parent surface is blocked while in kid mode.
    assert (await auth_client.get("/api/v1/governance/queue")).status_code == 403

    response = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": PIN})
    assert response.status_code == 200
    assert response.json()["scope"] == "parent"

    after = await auth_client.get("/api/v1/governance/queue")
    assert after.status_code == 200


@pytest.mark.asyncio
async def test_exit_with_wrong_pin_fails(auth_client: AsyncClient, child: Child, pin_cache):
    assert (await _set_pin(auth_client)).status_code == 200
    assert (await _enter(auth_client, child.id)).status_code == 200
    response = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": WRONG_PIN})
    assert response.status_code == 401
    # Still in kid mode.
    assert (await auth_client.get("/api/v1/governance/queue")).status_code == 403


@pytest.mark.asyncio
async def test_pin_lockout_rejects_correct_pin_password_still_works(auth_client: AsyncClient, child: Child, pin_cache):
    assert (await _set_pin(auth_client)).status_code == 200
    assert (await _enter(auth_client, child.id)).status_code == 200

    for _ in range(5):
        failed = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": WRONG_PIN})
        assert failed.status_code == 401

    # The PIN path is now locked: even the correct PIN is rejected.
    locked = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": PIN})
    assert locked.status_code == 403
    assert locked.json()["detail"] == "pin_locked_use_password"

    # The full password still exits.
    response = await auth_client.post("/api/v1/auth/child-session/exit", json={"password": PASSWORD})
    assert response.status_code == 200
    assert response.json()["scope"] == "parent"


@pytest.mark.asyncio
async def test_exit_with_password_when_no_pin_set(auth_client: AsyncClient, child: Child, pin_cache):
    assert (await _enter(auth_client, child.id)).status_code == 200
    pin_only = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": PIN})
    assert pin_only.status_code == 400
    assert pin_only.json()["detail"] == "pin_not_set"

    response = await auth_client.post("/api/v1/auth/child-session/exit", json={"password": PASSWORD})
    assert response.status_code == 200
    assert response.json()["scope"] == "parent"


@pytest.mark.asyncio
async def test_kid_mode_cookie_set_on_enter_cleared_on_exit(auth_client: AsyncClient, child: Child, pin_cache):
    enter = await _enter(auth_client, child.id)
    assert any(c.startswith("kid_mode=1") for c in enter.headers.get_list("set-cookie"))

    exit_response = await auth_client.post("/api/v1/auth/child-session/exit", json={"password": PASSWORD})
    assert exit_response.status_code == 200
    cleared = [c for c in exit_response.headers.get_list("set-cookie") if c.startswith("kid_mode=")]
    assert cleared, "exit must clear the kid_mode cookie"
    assert 'kid_mode="";' in cleared[0] or "kid_mode=;" in cleared[0] or "Max-Age=0" in cleared[0]


# ── PIN management ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_set_pin_requires_correct_current_password(auth_client: AsyncClient):
    response = await _set_pin(auth_client, password="not-the-password")
    assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.parametrize("bad_pin", ["abc", "12", "123456789", "12a4", ""])
async def test_set_pin_validates_format(auth_client: AsyncClient, bad_pin: str):
    response = await _set_pin(auth_client, pin=bad_pin)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_set_pin_reports_via_me_and_requires_parent_scope(
    auth_client: AsyncClient, child: Child, user: User, household: Household
):
    before = await auth_client.get("/api/v1/auth/me")
    assert before.json()["has_parent_pin"] is False
    assert (await _set_pin(auth_client)).status_code == 200
    after = await auth_client.get("/api/v1/auth/me")
    assert after.json()["has_parent_pin"] is True

    # Under child scope the same call is denied (hard deny + scope check).
    assert (await _enter(auth_client, child.id)).status_code == 200
    denied = await _set_pin(auth_client)
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_pin_value_never_appears_in_logs(auth_client: AsyncClient, child: Child, pin_cache, caplog, capfd):
    secret_pin = "86421357"
    with caplog.at_level("DEBUG"):
        assert (
            await auth_client.post(
                "/api/v1/auth/pin",
                json={"current_password": PASSWORD, "new_pin": secret_pin},
            )
        ).status_code == 200
        assert (await _enter(auth_client, child.id)).status_code == 200
        wrong = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": "99999999"})
        assert wrong.status_code == 401
        ok = await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": secret_pin})
        assert ok.status_code == 200

    captured = capfd.readouterr()
    log_text = caplog.text + captured.out + captured.err
    assert secret_pin not in log_text
    assert "99999999" not in log_text


# ── Backward compatibility ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_legacy_token_without_scope_decodes_as_parent(client: AsyncClient, user: User, household: Household):
    now = datetime.now(UTC)
    legacy_payload = {
        "sub": str(user.id),
        "hid": str(household.id),
        "role": "owner",
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=15),
        # No scope claim: minted before this change.
    }
    legacy_token = pyjwt.encode(legacy_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    client.cookies.set("access_token", legacy_token)

    me = await client.get("/api/v1/auth/me")
    assert me.status_code == 200
    queue = await client.get("/api/v1/governance/queue")
    assert queue.status_code == 200


@pytest.mark.asyncio
async def test_child_token_keeps_parent_sub(auth_client: AsyncClient, child: Child, user: User):
    response = await _enter(auth_client, child.id)
    payload = pyjwt.decode(
        response.json()["access_token"],
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    assert payload["sub"] == str(user.id)
    assert payload["scope"] == "child"
    assert payload["child_id"] == str(child.id)


# ── Governance events ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_governance_events_logged_for_pin_enter_exit(
    auth_client: AsyncClient, db_session, household: Household, child: Child, pin_cache
):
    assert (await _set_pin(auth_client)).status_code == 200
    assert (await _enter(auth_client, child.id)).status_code == 200
    assert (await auth_client.post("/api/v1/auth/child-session/exit", json={"pin": PIN})).status_code == 200

    result = await db_session.execute(
        select(GovernanceEvent.target_type).where(GovernanceEvent.household_id == household.id)
    )
    target_types = {row[0] for row in result.all()}
    assert "parent_pin_changed" in target_types
    assert "child_session_entered" in target_types
    assert "child_session_exited" in target_types
