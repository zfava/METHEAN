"""Tests for auth API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.models.identity import Child, Household, User


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
    #    Clear cookies first to avoid httpx merging old and new values
    client.cookies.delete("refresh_token")
    client.cookies.set("refresh_token", token_a)
    reuse_resp = await client.post("/api/v1/auth/refresh")
    assert reuse_resp.status_code == 401, "Replayed old token must be rejected"
    assert "reuse" in reuse_resp.json()["detail"].lower()

    # 4. Try the legitimate token_B — it should ALSO be revoked now
    client.cookies.delete("refresh_token")
    client.cookies.set("refresh_token", token_b)
    after_reuse = await client.post("/api/v1/auth/refresh")
    assert after_reuse.status_code == 401, "After reuse detection, even the newest token must be revoked"


@pytest.mark.asyncio
async def test_register_self_learner(client: AsyncClient, db_session):
    """Self-directed registration creates a linked Child record and flips the household."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "self@test.com",
            "password": "testpass123",
            "display_name": "Solo Learner",
            "household_name": "My Learning",
            "is_self_learner": True,
        },
    )
    assert response.status_code == 201, response.text

    user_row = (await db_session.execute(select(User).where(User.email == "self@test.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == user_row.household_id))).scalar_one()
    child = (await db_session.execute(select(Child).where(Child.household_id == household.id))).scalar_one()

    assert household.governance_mode == "self_governed"
    assert household.organization_type == "self_directed"
    assert user_row.is_self_learner is True
    assert user_row.linked_child_id is not None
    assert user_row.linked_child_id == child.id
    assert child.first_name == "Solo"


@pytest.mark.asyncio
async def test_register_normal_user_still_works(client: AsyncClient, db_session):
    """Omitting is_self_learner leaves the household in parent_governed mode."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "parent@test.com",
            "password": "testpass123",
            "display_name": "Normal Parent",
            "household_name": "Normal Family",
        },
    )
    assert response.status_code == 201, response.text

    user_row = (await db_session.execute(select(User).where(User.email == "parent@test.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == user_row.household_id))).scalar_one()

    assert household.governance_mode == "parent_governed"
    assert user_row.is_self_learner is False
    assert user_row.linked_child_id is None

    # No Child should have been auto-created
    children = (await db_session.execute(select(Child).where(Child.household_id == household.id))).scalars().all()
    assert children == []


# ══════════════════════════════════════════════════
# Institutional registration and invites
# ══════════════════════════════════════════════════


async def _register_inst_admin(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/v1/auth/register-institution",
        json={
            "organization_name": "Test University",
            "organization_type": "university",
            "admin_email": "admin@uni.example.com",
            "admin_password": "testpass123",
            "admin_display_name": "Dean Smith",
        },
    )
    assert resp.status_code == 201, resp.text
    token = resp.cookies.get("access_token") or resp.json()["access_token"]
    client.cookies.set("access_token", token)
    return token


@pytest.mark.asyncio
async def test_register_institution(client: AsyncClient, db_session):
    await _register_inst_admin(client)

    admin = (await db_session.execute(select(User).where(User.email == "admin@uni.example.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == admin.household_id))).scalar_one()

    assert household.governance_mode == "institution_governed"
    assert household.organization_type == "university"
    assert household.name == "Test University"
    assert admin.institutional_role == "department_admin"
    assert admin.role.value == "owner"


@pytest.mark.asyncio
async def test_invite_instructor(client: AsyncClient, db_session):
    await _register_inst_admin(client)

    resp = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "prof@uni.example.com",
            "display_name": "Prof Jones",
            "institutional_role": "instructor",
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["institutional_role"] == "instructor"

    instructor = (await db_session.execute(select(User).where(User.email == "prof@uni.example.com"))).scalar_one()
    assert instructor.institutional_role == "instructor"
    assert instructor.role.value == "co_parent"

    # Co-parent grants include approve.activities per CO_PARENT_PERMISSIONS
    from app.models.identity import UserPermission

    perms = (
        (await db_session.execute(select(UserPermission).where(UserPermission.user_id == instructor.id)))
        .scalars()
        .all()
    )
    perm_names = {p.permission for p in perms}
    assert "approve.activities" in perm_names
    assert "plans.generate" in perm_names


@pytest.mark.asyncio
async def test_invite_student(client: AsyncClient, db_session):
    await _register_inst_admin(client)

    resp = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "alice@uni.example.com",
            "display_name": "Alice",
            "institutional_role": "student",
            "learner_name": "Alice",
        },
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["institutional_role"] == "student"
    assert data["linked_child_id"] is not None

    student = (await db_session.execute(select(User).where(User.email == "alice@uni.example.com"))).scalar_one()
    assert student.is_self_learner is True
    assert student.linked_child_id is not None

    child_row = (await db_session.execute(select(Child).where(Child.id == student.linked_child_id))).scalar_one()
    assert child_row.first_name == "Alice"
    assert child_row.household_id == student.household_id


@pytest.mark.asyncio
async def test_non_admin_cannot_invite(client: AsyncClient, db_session):
    """An instructor attempting to invite another user is rejected."""
    from app.core.security import create_access_token

    await _register_inst_admin(client)

    # Admin creates an instructor
    r1 = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "inst@uni.example.com",
            "display_name": "Instructor One",
            "institutional_role": "instructor",
        },
    )
    assert r1.status_code == 201
    instructor = (await db_session.execute(select(User).where(User.email == "inst@uni.example.com"))).scalar_one()

    # Switch to the instructor's token. Delete first so httpx does not
    # keep the admin cookie alongside the new one.
    inst_token = create_access_token(instructor.id, instructor.household_id, "co_parent")
    client.cookies.delete("access_token")
    client.cookies.set("access_token", inst_token)

    r2 = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "ta@uni.example.com",
            "display_name": "TA",
            "institutional_role": "teaching_assistant",
        },
    )
    assert r2.status_code == 403, r2.text


@pytest.mark.asyncio
async def test_student_cannot_access_other_students(client: AsyncClient, db_session):
    """Students get view_progress scoped to their own child only."""
    from app.core.permissions import PERM_VIEW_PROGRESS, check_permission

    await _register_inst_admin(client)

    for email, learner in [("sa@uni.example.com", "StuA"), ("sb@uni.example.com", "StuB")]:
        r = await client.post(
            "/api/v1/auth/invite",
            json={
                "email": email,
                "display_name": learner,
                "institutional_role": "student",
                "learner_name": learner,
            },
        )
        assert r.status_code == 201

    student_a = (await db_session.execute(select(User).where(User.email == "sa@uni.example.com"))).scalar_one()
    student_b = (await db_session.execute(select(User).where(User.email == "sb@uni.example.com"))).scalar_one()
    assert student_a.linked_child_id != student_b.linked_child_id

    # Student A's view_progress is allowed against their own child
    allowed_self = await check_permission(
        db_session, student_a, PERM_VIEW_PROGRESS, scope_type="child", scope_id=student_a.linked_child_id
    )
    assert allowed_self is True

    # Student A's view_progress is denied against student B's child
    allowed_other = await check_permission(
        db_session, student_a, PERM_VIEW_PROGRESS, scope_type="child", scope_id=student_b.linked_child_id
    )
    assert allowed_other is False


# ══════════════════════════════════════════════════
# Email verification tokens (METHEAN-6-03)
# ══════════════════════════════════════════════════


async def _register_and_get_user(client: AsyncClient, db_session, email: str = "verify@test.example.com") -> User:
    """Helper: register a fresh household + return the User row."""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "testpass123",
            "display_name": "Verify Test",
            "household_name": "Verify Family",
        },
    )
    assert resp.status_code == 201, resp.text
    return (await db_session.execute(select(User).where(User.email == email))).scalar_one()


@pytest.mark.asyncio
async def test_register_issues_verification_token_row(client: AsyncClient, db_session):
    """Registration creates exactly one EmailVerificationToken row for the new user."""
    from app.models.identity import EmailVerificationToken

    user = await _register_and_get_user(client, db_session)
    rows = (
        (await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)))
        .scalars()
        .all()
    )
    assert len(rows) == 1
    assert rows[0].used_at is None
    assert rows[0].expires_at is not None


@pytest.mark.asyncio
async def test_verify_email_happy_path(client: AsyncClient, db_session, monkeypatch):
    """A freshly-issued token verifies the user and is single-use."""
    captured: dict = {}

    async def fake_send_email(to, subject, html, text=None):
        captured["html"] = html
        return True

    monkeypatch.setattr("app.services.email.send_email", fake_send_email)
    user = await _register_and_get_user(client, db_session)

    # Pull the plaintext token out of the captured email HTML.
    import re

    match = re.search(r"token=([A-Za-z0-9_\-]+)", captured.get("html", ""))
    assert match, captured.get("html")
    plaintext = match.group(1)

    resp = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert resp.status_code == 200, resp.text

    await db_session.refresh(user)
    assert user.email_verified is True


@pytest.mark.asyncio
async def test_verify_email_rejects_unknown_token(client: AsyncClient):
    resp = await client.post("/api/v1/auth/verify-email", json={"token": "completely-bogus-token-value"})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_verify_email_rejects_expired_token(client: AsyncClient, db_session, monkeypatch):
    """Backdate expires_at — the verify endpoint should now refuse the token."""
    import re
    from datetime import UTC, datetime, timedelta

    from app.models.identity import EmailVerificationToken

    captured: dict = {}

    async def fake_send_email(to, subject, html, text=None):
        captured["html"] = html
        return True

    monkeypatch.setattr("app.services.email.send_email", fake_send_email)
    user = await _register_and_get_user(client, db_session, "expired@test.example.com")

    plaintext = re.search(r"token=([A-Za-z0-9_\-]+)", captured["html"]).group(1)
    row = (
        await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id))
    ).scalar_one()
    row.expires_at = datetime.now(UTC) - timedelta(minutes=1)
    await db_session.commit()

    resp = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_verify_email_rejects_reused_token(client: AsyncClient, db_session, monkeypatch):
    """A token that has been used once cannot be used again."""
    import re

    captured: dict = {}

    async def fake_send_email(to, subject, html, text=None):
        captured["html"] = html
        return True

    monkeypatch.setattr("app.services.email.send_email", fake_send_email)
    await _register_and_get_user(client, db_session, "reuse@test.example.com")
    plaintext = re.search(r"token=([A-Za-z0-9_\-]+)", captured["html"]).group(1)

    first = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert first.status_code == 200, first.text

    second = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert second.status_code == 400


@pytest.mark.asyncio
async def test_verify_email_does_not_accept_user_id_as_token(client: AsyncClient, db_session):
    """Sending the user's UUID as a token must fail — closes the original attack vector."""
    user = await _register_and_get_user(client, db_session, "uuidattack@test.example.com")
    resp = await client.post("/api/v1/auth/verify-email", json={"token": str(user.id)})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_resend_verification_does_not_leak_user_id_in_url(client: AsyncClient, db_session, monkeypatch):
    """The resend email must NOT contain the user's UUID anywhere in the body."""
    captured: dict = {"history": []}

    async def fake_send_email(to, subject, html, text=None):
        captured["history"].append(html)
        return True

    monkeypatch.setattr("app.services.email.send_email", fake_send_email)
    user = await _register_and_get_user(client, db_session, "resend@test.example.com")

    resp = await client.post("/api/v1/auth/resend-verification")
    assert resp.status_code == 200, resp.text

    resend_html = captured["history"][-1]
    assert str(user.id) not in resend_html


@pytest.mark.asyncio
async def test_email_verification_token_is_hashed_at_rest(client: AsyncClient, db_session, monkeypatch):
    """The DB row stores a SHA-256 hash, not the plaintext token sent to the user."""
    import hashlib
    import re

    from app.models.identity import EmailVerificationToken

    captured: dict = {}

    async def fake_send_email(to, subject, html, text=None):
        captured["html"] = html
        return True

    monkeypatch.setattr("app.services.email.send_email", fake_send_email)
    user = await _register_and_get_user(client, db_session, "hashed@test.example.com")

    plaintext = re.search(r"token=([A-Za-z0-9_\-]+)", captured["html"]).group(1)
    row = (
        await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id))
    ).scalar_one()
    assert row.token_hash != plaintext
    assert row.token_hash == hashlib.sha256(plaintext.encode()).hexdigest()
    assert len(row.token_hash) == 64
