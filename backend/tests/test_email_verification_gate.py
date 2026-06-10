"""Tests for the router-level email verification gate.

Unverified accounts must be locked out of every child-data surface
(403 email_not_verified) while keeping the verify, billing, and exit
paths open. Verified accounts are unaffected.
"""

import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.core.security import create_access_token, hash_password
from app.models.identity import Household, User

PASSWORD = "testpass123"


@pytest_asyncio.fixture
async def unverified_client(client: AsyncClient, db_session, household: Household) -> AsyncClient:
    user = User(
        household_id=household.id,
        email="unverified@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Unverified Parent",
        role="owner",
        email_verified=False,
    )
    db_session.add(user)
    await db_session.flush()
    token = create_access_token(user.id, household.id, "owner")
    client.cookies.set("access_token", token)
    return client


# ── Gated surfaces: 403 with the exact stable token ─────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path,body",
    [
        ("POST", "/api/v1/children", {"first_name": "Blocked"}),
        ("GET", "/api/v1/learning-maps", None),
        ("GET", f"/api/v1/activities/{uuid.uuid4()}/learn", None),
        ("GET", "/api/v1/governance/queue", None),
        ("GET", "/api/v1/children", None),
    ],
)
async def test_unverified_user_blocked_on_child_data_surfaces(
    unverified_client: AsyncClient, method: str, path: str, body
):
    response = await unverified_client.request(method, path, json=body)
    assert response.status_code == 403, f"{path} returned {response.status_code}"
    assert response.json() == {"detail": "email_not_verified"}


# ── Ungated surfaces: verify, pay, or leave ─────────────────────────


@pytest.mark.asyncio
async def test_unverified_user_can_resend_verification(unverified_client: AsyncClient):
    response = await unverified_client.post("/api/v1/auth/resend-verification", json={})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unverified_user_can_hit_billing(unverified_client: AsyncClient):
    response = await unverified_client.get("/api/v1/billing/status")
    assert response.status_code != 403


@pytest.mark.asyncio
async def test_unverified_user_can_logout(unverified_client: AsyncClient):
    response = await unverified_client.post("/api/v1/auth/logout", json={})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unverified_user_can_export_data(unverified_client: AsyncClient):
    response = await unverified_client.post("/api/v1/household/export", json={})
    assert response.status_code != 403


# ── Verified accounts unaffected ────────────────────────────────────


@pytest.mark.asyncio
async def test_verified_user_passes_the_gate(auth_client: AsyncClient):
    created = await auth_client.post("/api/v1/children", json={"first_name": "Allowed"})
    assert created.status_code == 201
    queue = await auth_client.get("/api/v1/governance/queue")
    assert queue.status_code == 200


# ── Registration behavior around the gate ───────────────────────────


@pytest.mark.asyncio
async def test_register_without_email_provider_is_verified(client: AsyncClient):
    """With no email provider configured (dev/CI), the verification
    email can never arrive, so registration auto-verifies outside
    production and the new account can use the product immediately."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "no-provider@test.com",
            "password": "securepass123",
            "display_name": "Dev User",
            "household_name": "Dev Family",
        },
    )
    assert response.status_code == 201
    created = await client.post("/api/v1/children", json={"first_name": "DevKid"})
    assert created.status_code == 201


@pytest.mark.asyncio
async def test_register_with_email_provider_requires_verification(client: AsyncClient, monkeypatch):
    """With a provider configured, fresh registrations stay unverified
    and the gate holds until the emailed token is redeemed."""
    from unittest.mock import AsyncMock, patch

    from app.core.config import settings

    monkeypatch.setattr(settings, "RESEND_API_KEY", "re_test_key")
    with patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "must-verify@test.com",
                "password": "securepass123",
                "display_name": "Strict User",
                "household_name": "Strict Family",
            },
        )
    assert response.status_code == 201
    blocked = await client.post("/api/v1/children", json={"first_name": "BlockedKid"})
    assert blocked.status_code == 403
    assert blocked.json() == {"detail": "email_not_verified"}
