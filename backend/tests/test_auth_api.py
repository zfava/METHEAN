"""Tests for auth API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "methean"


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "securepass123",
            "display_name": "New User",
            "household_name": "New Family",
            "timezone": "America/Chicago",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "newuser@test.com"
    assert data["user"]["display_name"] == "New User"
    assert data["user"]["role"] == "owner"
    assert "access_token" in data

    # Check cookies set
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "email": "duplicate@test.com",
        "password": "securepass123",
        "display_name": "User One",
        "household_name": "Family One",
    }
    response1 = await client.post("/api/v1/auth/register", json=payload)
    assert response1.status_code == 201

    response2 = await client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "logintest@test.com",
            "password": "securepass123",
            "display_name": "Login User",
            "household_name": "Login Family",
        },
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "logintest@test.com", "password": "securepass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrongpass@test.com",
            "password": "securepass123",
            "display_name": "Wrong Pass",
            "household_name": "Wrong Family",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpass@test.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authenticated(client: AsyncClient):
    # Register to get token
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "metest@test.com",
            "password": "securepass123",
            "display_name": "Me User",
            "household_name": "Me Family",
        },
    )
    token = reg_response.json()["access_token"]

    # Use cookie to access /me
    client.cookies.set("access_token", token)
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "metest@test.com"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "logouttest@test.com",
            "password": "securepass123",
            "display_name": "Logout User",
            "household_name": "Logout Family",
        },
    )
    # Set cookies from registration
    client.cookies.set("access_token", reg_response.json()["access_token"])
    if "refresh_token" in reg_response.cookies:
        client.cookies.set("refresh_token", reg_response.cookies["refresh_token"])

    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "short@test.com",
            "password": "short",
            "display_name": "Short",
            "household_name": "Short Family",
        },
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_refresh_token_reuse_revokes_all_tokens(client: AsyncClient):
    """When a refresh token is replayed after rotation, ALL of the user's
    refresh tokens must be revoked — including the legitimately issued new one.

    Flow:
    1. Register -> get refresh_token_A
    2. Call /refresh with token_A -> get refresh_token_B (token_A rotated out)
    3. Replay token_A (the OLD one) -> 401 "Token reuse detected"
    4. Try token_B (the NEW one) -> also 401, proving all tokens were killed
    """
    # 1. Register
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "reuse@test.com",
            "password": "securepass123",
            "display_name": "Reuse Tester",
            "household_name": "Reuse Family",
        },
    )
    assert reg.status_code == 201
    token_a = reg.cookies.get("refresh_token")
    assert token_a is not None, "Registration must set refresh_token cookie"

    # 2. Normal refresh: rotate token_A -> token_B
    client.cookies.set("refresh_token", token_a)
    refresh1 = await client.post("/api/v1/auth/refresh")
    assert refresh1.status_code == 200, f"First refresh should succeed: {refresh1.text}"
    token_b = refresh1.cookies.get("refresh_token")
    assert token_b is not None, "Refresh must set a new refresh_token cookie"
    assert token_b != token_a, "Rotated token must differ from original"

    # 3. Replay old token_A — this is the reuse attack
    client.cookies.set("refresh_token", token_a)
    reuse_resp = await client.post("/api/v1/auth/refresh")
    assert reuse_resp.status_code == 401, "Replayed old token must be rejected"
    assert "reuse" in reuse_resp.json()["detail"].lower()

    # 4. Try the legitimate token_B — it should ALSO be revoked now
    client.cookies.set("refresh_token", token_b)
    after_reuse = await client.post("/api/v1/auth/refresh")
    assert after_reuse.status_code == 401, (
        "After reuse detection, even the newest token must be revoked"
    )
