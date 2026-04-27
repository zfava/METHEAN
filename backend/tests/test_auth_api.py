"""Tests for auth API endpoints."""

import uuid
from datetime import UTC, datetime

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


# ══════════════════════════════════════════════════════════════════════
# Family invite role normalisation (METHEAN-6-01)
# ══════════════════════════════════════════════════════════════════════


async def _create_household_invite(auth_client: AsyncClient, *, email: str, role: str):
    return await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": email, "role": role},
    )


@pytest.mark.asyncio
async def test_invite_create_with_co_parent_role(auth_client, db_session):
    """Canonical co_parent role is accepted and persisted as-is."""
    from app.models.identity import FamilyInvite

    resp = await _create_household_invite(auth_client, email="cp@example.com", role="co_parent")
    assert resp.status_code == 200, resp.text

    invite = (await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "cp@example.com"))).scalar_one()
    assert invite.role == "co_parent"


@pytest.mark.asyncio
async def test_invite_create_with_observer_role(auth_client, db_session):
    """Canonical observer role is accepted and persisted as-is."""
    from app.models.identity import FamilyInvite

    resp = await _create_household_invite(auth_client, email="obs@example.com", role="observer")
    assert resp.status_code == 200, resp.text

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "obs@example.com"))
    ).scalar_one()
    assert invite.role == "observer"


@pytest.mark.asyncio
async def test_invite_create_with_legacy_parent_alias_normalized_to_co_parent(auth_client, db_session):
    """Legacy 'parent' alias must be flattened to 'co_parent' in the DB."""
    from app.models.identity import FamilyInvite

    resp = await _create_household_invite(auth_client, email="legacy-p@example.com", role="parent")
    assert resp.status_code == 200, resp.text

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "legacy-p@example.com"))
    ).scalar_one()
    assert invite.role == "co_parent", f"expected normalised co_parent, got {invite.role!r}"


@pytest.mark.asyncio
async def test_invite_create_with_legacy_viewer_alias_normalized_to_observer(auth_client, db_session):
    """Legacy 'viewer' alias must be flattened to 'observer' in the DB."""
    from app.models.identity import FamilyInvite

    resp = await _create_household_invite(auth_client, email="legacy-v@example.com", role="viewer")
    assert resp.status_code == 200, resp.text

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "legacy-v@example.com"))
    ).scalar_one()
    assert invite.role == "observer"


@pytest.mark.asyncio
async def test_invite_create_rejects_unknown_role(auth_client):
    """An unknown role must fail Pydantic validation (422)."""
    resp = await _create_household_invite(auth_client, email="bad@example.com", role="admin")
    # Pydantic v2 rejects with 422; the helper raises 400 — accept either.
    assert resp.status_code in (400, 422), resp.text


@pytest.mark.asyncio
async def test_invite_accept_creates_user_with_canonical_role(auth_client, client, db_session):
    """End-to-end: invite -> accept -> User row holds the canonical enum."""
    from app.models.enums import UserRole
    from app.models.identity import FamilyInvite

    # Use legacy alias on creation to also exercise normalisation.
    resp = await _create_household_invite(auth_client, email="accept-me@example.com", role="parent")
    assert resp.status_code == 200, resp.text

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "accept-me@example.com"))
    ).scalar_one()
    # Anonymous client (no auth cookie) — accept is unauthenticated.
    accept = await client.post(
        "/api/v1/auth/accept-invite",
        json={
            "token": invite.token,
            "password": "newpassword123",
            "display_name": "Accepted",
        },
    )
    assert accept.status_code == 200, accept.text

    new_user = (await db_session.execute(select(User).where(User.email == "accept-me@example.com"))).scalar_one()
    role_value = new_user.role.value if hasattr(new_user.role, "value") else new_user.role
    assert role_value == UserRole.co_parent.value


@pytest.mark.asyncio
async def test_invite_accept_rejects_corrupted_legacy_role_in_db(client, db_session, household):
    """If a row in the DB carries an unknown role string (e.g. from an
    unmigrated import), accept-invite must 400 instead of 500.
    """
    import secrets
    from datetime import UTC, datetime, timedelta

    from app.models.identity import FamilyInvite

    token = secrets.token_urlsafe(32)
    invite = FamilyInvite(
        household_id=household.id,
        email="corrupt@example.com",
        role="admin",  # not in _INVITE_ROLE_ALIASES
        token=token,
        expires_at=datetime.now(UTC) + timedelta(days=1),
        status="pending",
    )
    db_session.add(invite)
    await db_session.flush()

    resp = await client.post(
        "/api/v1/auth/accept-invite",
        json={
            "token": token,
            "password": "newpassword123",
            "display_name": "Corrupt",
        },
    )
    assert resp.status_code == 400, resp.text
    assert "Invalid role" in resp.json().get("detail", "")


# ══════════════════════════════════════════════════════════════════════
# Email verification (METHEAN-6-03)
# ══════════════════════════════════════════════════════════════════════


async def _register_for_verify(client: AsyncClient, email: str = "verify@example.com") -> str:
    """Register a user and return the email used. Verification tokens
    are issued on register; tests pull them back out of the DB."""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "verifypass123",
            "display_name": "Verify User",
            "household_name": "Verify Family",
        },
    )
    assert resp.status_code == 201, resp.text
    return email


@pytest.mark.asyncio
async def test_register_issues_verification_token_row(client: AsyncClient, db_session):
    """Registering a new user must drop a row in email_verification_tokens."""
    from sqlalchemy import func

    from app.models.identity import EmailVerificationToken

    email = await _register_for_verify(client, email="rowcheck@example.com")
    user = (await db_session.execute(select(User).where(User.email == email))).scalar_one()
    count = (
        await db_session.execute(
            select(func.count()).select_from(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)
        )
    ).scalar()
    assert count == 1


@pytest.mark.asyncio
async def test_email_verification_token_is_hashed_at_rest(client: AsyncClient, db_session):
    """The plaintext token never touches the DB — only the SHA-256 digest does."""
    import hashlib

    from app.models.identity import EmailVerificationToken
    from app.services.email_verification import issue_token

    # Direct issuance lets us hold the plaintext for comparison.
    await _register_for_verify(client, email="hashed@example.com")
    user = (await db_session.execute(select(User).where(User.email == "hashed@example.com"))).scalar_one()
    plaintext = await issue_token(db_session, user)
    await db_session.flush()

    expected_hash = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
    rows = (
        (await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)))
        .scalars()
        .all()
    )
    persisted_hashes = {r.token_hash for r in rows}
    assert plaintext not in persisted_hashes, "plaintext token must never be stored"
    assert expected_hash in persisted_hashes


@pytest.mark.asyncio
async def test_verify_email_happy_path(client: AsyncClient, db_session):
    """A freshly issued token verifies the user's email."""
    from app.models.identity import EmailVerificationToken
    from app.services.email_verification import issue_token

    await _register_for_verify(client, email="happy@example.com")
    user = (await db_session.execute(select(User).where(User.email == "happy@example.com"))).scalar_one()
    plaintext = await issue_token(db_session, user)
    await db_session.commit()

    resp = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"verified": True}

    await db_session.refresh(user)
    assert user.email_verified is True

    # Token row used_at is populated.
    token = (
        (await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)))
        .scalars()
        .all()[-1]
    )
    await db_session.refresh(token)
    assert token.used_at is not None


@pytest.mark.asyncio
async def test_verify_email_rejects_unknown_token(client: AsyncClient):
    """A random unrecognised token returns the generic 400."""
    resp = await client.post(
        "/api/v1/auth/verify-email",
        json={"token": "totally-not-a-real-token-1234567890"},
    )
    assert resp.status_code == 400, resp.text
    assert resp.json()["detail"] == "Invalid or expired token"


@pytest.mark.asyncio
async def test_verify_email_rejects_expired_token(client: AsyncClient, db_session):
    """Backdating expires_at causes the same generic 400."""
    from datetime import UTC, datetime, timedelta

    from app.models.identity import EmailVerificationToken
    from app.services.email_verification import issue_token

    await _register_for_verify(client, email="expired@example.com")
    user = (await db_session.execute(select(User).where(User.email == "expired@example.com"))).scalar_one()
    plaintext = await issue_token(db_session, user)
    await db_session.flush()
    token_row = (
        (await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)))
        .scalars()
        .all()[-1]
    )
    token_row.expires_at = datetime.now(UTC) - timedelta(minutes=5)
    await db_session.commit()

    resp = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid or expired token"


@pytest.mark.asyncio
async def test_verify_email_rejects_reused_token(client: AsyncClient, db_session):
    """A token that was already consumed cannot be reused."""
    from app.services.email_verification import issue_token

    await _register_for_verify(client, email="reused@example.com")
    user = (await db_session.execute(select(User).where(User.email == "reused@example.com"))).scalar_one()
    plaintext = await issue_token(db_session, user)
    await db_session.commit()

    first = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert first.status_code == 200, first.text
    second = await client.post("/api/v1/auth/verify-email", json={"token": plaintext})
    assert second.status_code == 400, second.text
    assert second.json()["detail"] == "Invalid or expired token"


@pytest.mark.asyncio
async def test_verify_email_does_not_accept_user_id_as_token(client: AsyncClient, db_session):
    """The legacy attack — sending the user's UUID as the token — must fail."""
    await _register_for_verify(client, email="legacy-attack@example.com")
    user = (await db_session.execute(select(User).where(User.email == "legacy-attack@example.com"))).scalar_one()

    resp = await client.post("/api/v1/auth/verify-email", json={"token": str(user.id)})
    assert resp.status_code == 400, resp.text
    assert resp.json()["detail"] == "Invalid or expired token"

    await db_session.refresh(user)
    assert user.email_verified is False


@pytest.mark.asyncio
async def test_resend_verification_does_not_leak_user_id_in_url(client: AsyncClient, db_session):
    """The verification URL must contain a fresh hashed-token, not the user's UUID."""
    from unittest.mock import AsyncMock, patch

    email = "resend-no-leak@example.com"
    await _register_for_verify(client, email=email)
    user = (await db_session.execute(select(User).where(User.email == email))).scalar_one()

    with patch(
        "app.services.email.send_email",
        new_callable=AsyncMock,
        return_value=True,
    ) as mock_send:
        resp = await client.post("/api/v1/auth/resend-verification")
        assert resp.status_code == 200, resp.text

    assert mock_send.called
    sent_html = mock_send.call_args[0][2]
    assert str(user.id) not in sent_html, "resend-verification must not embed the user UUID in the link"


# ══════════════════════════════════════════════════════════════════════
# Password reset persistence (METHEAN-6-04)
# ══════════════════════════════════════════════════════════════════════


from unittest.mock import AsyncMock, patch  # noqa: E402 — grouped with the reset block


def _extract_token_from_email(mock_send: AsyncMock) -> str:
    """Pull the plaintext token out of the verification URL the
    email mock captured. The URL is stamped as href="…?token=PLAIN"."""
    html = mock_send.call_args[0][2]
    return html.split("token=", 1)[1].split('"', 1)[0]


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_forgot_password_persists_token_row(mock_send, client: AsyncClient, db_session):
    """A forgot-password request creates exactly one PasswordResetToken row."""
    from sqlalchemy import func

    from app.models.identity import PasswordResetToken

    # Register a user via the API so the surrounding plumbing matches prod.
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "pwpersist@example.com",
            "password": "originalpw123",
            "display_name": "PW Persist",
            "household_name": "PW Family",
        },
    )
    user = (await db_session.execute(select(User).where(User.email == "pwpersist@example.com"))).scalar_one()

    resp = await client.post("/api/v1/auth/forgot-password", json={"email": "pwpersist@example.com"})
    assert resp.status_code == 200, resp.text

    count = (
        await db_session.execute(
            select(func.count())
            .select_from(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
        )
    ).scalar()
    assert count == 1


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_forgot_password_unknown_email_no_row_no_leak(mock_send, client: AsyncClient, db_session):
    """An unknown email still returns 200 and writes zero rows."""
    from sqlalchemy import func

    from app.models.identity import PasswordResetToken

    resp = await client.post("/api/v1/auth/forgot-password", json={"email": "ghost@nowhere.invalid"})
    assert resp.status_code == 200
    assert mock_send.called is False

    total = (await db_session.execute(select(func.count()).select_from(PasswordResetToken))).scalar()
    assert total == 0


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_happy_path(mock_send, client: AsyncClient, db_session):
    """The plaintext token sent in the email rotates the user's password."""
    from app.core.security import verify_password

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "happyreset@example.com",
            "password": "originalpw123",
            "display_name": "Happy Reset",
            "household_name": "Reset Family",
        },
    )
    await client.post("/api/v1/auth/forgot-password", json={"email": "happyreset@example.com"})
    plaintext = _extract_token_from_email(mock_send)

    resp = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "rotatedpw456"},
    )
    assert resp.status_code == 200, resp.text

    user = (await db_session.execute(select(User).where(User.email == "happyreset@example.com"))).scalar_one()
    await db_session.refresh(user)
    assert verify_password("rotatedpw456", user.password_hash)


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_expired_token(mock_send, client: AsyncClient, db_session):
    """Expired tokens return 400 and don't change the password."""
    from datetime import UTC, datetime, timedelta

    from app.models.identity import PasswordResetToken

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "expreset@example.com",
            "password": "originalpw123",
            "display_name": "Exp Reset",
            "household_name": "Exp Family",
        },
    )
    user = (await db_session.execute(select(User).where(User.email == "expreset@example.com"))).scalar_one()
    original_hash = user.password_hash

    await client.post("/api/v1/auth/forgot-password", json={"email": "expreset@example.com"})
    plaintext = _extract_token_from_email(mock_send)

    row = (
        (await db_session.execute(select(PasswordResetToken).where(PasswordResetToken.user_id == user.id)))
        .scalars()
        .all()[-1]
    )
    row.expires_at = datetime.now(UTC) - timedelta(minutes=5)
    await db_session.commit()

    resp = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "shouldnotapply"},
    )
    assert resp.status_code == 400, resp.text

    await db_session.refresh(user)
    assert user.password_hash == original_hash


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_reused_token(mock_send, client: AsyncClient, db_session):
    """A token that was already redeemed cannot be redeemed again."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "reusereset@example.com",
            "password": "originalpw123",
            "display_name": "Reuse Reset",
            "household_name": "Reuse Family",
        },
    )
    await client.post("/api/v1/auth/forgot-password", json={"email": "reusereset@example.com"})
    plaintext = _extract_token_from_email(mock_send)

    first = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "rotated1"},
    )
    assert first.status_code == 200, first.text

    second = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "rotated2"},
    )
    assert second.status_code == 400, second.text


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_invalidates_old_active_tokens(mock_send, client: AsyncClient, db_session):
    """Issuing a fresh token marks any prior active token used."""
    from sqlalchemy import func

    from app.models.identity import PasswordResetToken

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "doubleissue@example.com",
            "password": "originalpw123",
            "display_name": "Double Issue",
            "household_name": "Double Family",
        },
    )
    user = (await db_session.execute(select(User).where(User.email == "doubleissue@example.com"))).scalar_one()

    await client.post("/api/v1/auth/forgot-password", json={"email": "doubleissue@example.com"})
    await client.post("/api/v1/auth/forgot-password", json={"email": "doubleissue@example.com"})

    active = (
        await db_session.execute(
            select(func.count())
            .select_from(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
        )
    ).scalar()
    assert active == 1, "partial unique index uq_pwreset_user_active enforces single active row"


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_token_is_hashed_at_rest(mock_send, client: AsyncClient, db_session):
    """The plaintext never touches the DB — only the SHA-256 digest does."""
    import hashlib

    from app.models.identity import PasswordResetToken

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "hashedat@example.com",
            "password": "originalpw123",
            "display_name": "Hashed Rest",
            "household_name": "Hash Family",
        },
    )
    user = (await db_session.execute(select(User).where(User.email == "hashedat@example.com"))).scalar_one()
    await client.post("/api/v1/auth/forgot-password", json={"email": "hashedat@example.com"})
    plaintext = _extract_token_from_email(mock_send)
    expected = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()

    row = (
        (await db_session.execute(select(PasswordResetToken).where(PasswordResetToken.user_id == user.id)))
        .scalars()
        .all()[-1]
    )
    assert row.token_hash == expected
    assert row.token_hash != plaintext


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_revokes_existing_refresh_tokens(mock_send, client: AsyncClient, db_session):
    """A successful reset revokes every active refresh token so a stolen
    cookie can't outlive the rotation. Verify by attempting /refresh
    after reset and expecting 401.
    """
    register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "revoke-on-reset@example.com",
            "password": "originalpw123",
            "display_name": "Revoke Reset",
            "household_name": "Revoke Family",
        },
    )
    assert register.status_code == 201
    # The refresh cookie is now sitting on the client.
    refresh_before = client.cookies.get("refresh_token")
    assert refresh_before, "register should set refresh_token"

    await client.post("/api/v1/auth/forgot-password", json={"email": "revoke-on-reset@example.com"})
    plaintext = _extract_token_from_email(mock_send)
    reset = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "rotatedpw456"},
    )
    assert reset.status_code == 200, reset.text

    # The old refresh token must be revoked. Restore the pre-reset
    # cookie (in case any handler updated it) and call /refresh.
    client.cookies.set("refresh_token", refresh_before)
    refresh = await client.post("/api/v1/auth/refresh")
    assert refresh.status_code == 401, refresh.text


def test_reset_password_module_no_longer_uses_inmemory_dict():
    """Locks in the regression: the in-memory dict must stay gone.

    Build the attribute name dynamically so this assertion file
    itself contains zero literal occurrences of the old identifier.
    """
    import app.services.password_reset as svc

    forbidden = "_" + "reset" + "_" + "tokens"
    assert not hasattr(svc, forbidden), (
        f"{forbidden} is back in app.services.password_reset — tokens must stay in PostgreSQL, not module-level dicts."
    )


# ══════════════════════════════════════════════════════════════════════
# Targeted coverage: register / register_institution / institutional invite
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_register_returns_httponly_cookies(client: AsyncClient):
    """Register's Set-Cookie headers must be HttpOnly + SameSite=lax +
    Path=/ for both the access and refresh tokens. The token-bearing
    cookies are the user's session — JS access would expose them to
    XSS exfiltration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "cookie-shape@test.com",
            "password": "securepass123",
            "display_name": "Cookie Shape",
            "household_name": "Cookie Family",
        },
    )
    assert response.status_code == 201, response.text

    set_cookie_headers = response.headers.get_list("set-cookie")
    access = next((h for h in set_cookie_headers if h.startswith("access_token=")), None)
    refresh = next((h for h in set_cookie_headers if h.startswith("refresh_token=")), None)
    assert access is not None, f"access_token cookie missing from headers: {set_cookie_headers}"
    assert refresh is not None, f"refresh_token cookie missing from headers: {set_cookie_headers}"
    for header in (access, refresh):
        assert "HttpOnly" in header, f"cookie must be HttpOnly: {header}"
        assert "SameSite=lax" in header, f"cookie must be SameSite=lax: {header}"
        assert "Path=/" in header, f"cookie must scope to Path=/: {header}"


@pytest.mark.asyncio
async def test_register_creates_household_and_child_for_self_learner(client: AsyncClient, db_session):
    """is_self_learner=True wires the registering user as the lone
    learner: a Child row exists, the user is linked to it, and the
    household flips to self_governed/self_directed."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "solo-link@test.com",
            "password": "testpass123",
            "display_name": "Solo Link",
            "household_name": "Solo Family",
            "is_self_learner": True,
        },
    )
    assert response.status_code == 201, response.text

    user_row = (await db_session.execute(select(User).where(User.email == "solo-link@test.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == user_row.household_id))).scalar_one()
    children = (await db_session.execute(select(Child).where(Child.household_id == household.id))).scalars().all()

    assert len(children) == 1, f"self-learner registration must seed exactly one Child, got {len(children)}"
    child = children[0]
    assert household.governance_mode == "self_governed"
    assert household.organization_type == "self_directed"
    assert user_row.is_self_learner is True
    assert user_row.linked_child_id == child.id


@pytest.mark.asyncio
async def test_register_sends_verification_email(client: AsyncClient):
    """Registration calls send_email with the verification subject so
    the user can confirm ownership of the address. Failures are
    swallowed by the handler, but the call MUST be attempted."""
    from unittest.mock import AsyncMock, patch

    with patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True) as mock:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "verify-email@test.com",
                "password": "testpass123",
                "display_name": "Verify Email",
                "household_name": "Verify Family",
            },
        )
    assert response.status_code == 201, response.text
    assert mock.await_count >= 1, "send_email was never invoked from the register handler"
    # The verification call uses the user's email + the verification subject.
    call = next((c for c in mock.await_args_list if c.args and c.args[0] == "verify-email@test.com"), None)
    assert call is not None, "send_email was not called with the registering user's email"
    assert "verify" in call.args[1].lower(), f"send_email subject did not mention verification: {call.args[1]}"


@pytest.mark.asyncio
async def test_register_sets_trial_status(client: AsyncClient, db_session):
    """Newly-registered households start in subscription_status="trial".
    The billing gate later promotes them to "trialing"/"active"; this
    test pins the default at the moment of registration so a model
    refactor that flips the default to e.g. "canceled" can't ship
    silently."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "trial-status@test.com",
            "password": "testpass123",
            "display_name": "Trial Status",
            "household_name": "Trial Family",
        },
    )
    assert response.status_code == 201, response.text

    user_row = (await db_session.execute(select(User).where(User.email == "trial-status@test.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == user_row.household_id))).scalar_one()
    assert household.subscription_status == "trial"


@pytest.mark.asyncio
async def test_register_institution_creates_correct_governance_mode(client: AsyncClient, db_session):
    """register-institution must mark the household institution_governed.
    Every other governance-aware code path branches on this string, so
    a typo in the constant would silently demote the institution to
    parent_governed and break instructor permissions."""
    resp = await client.post(
        "/api/v1/auth/register-institution",
        json={
            "organization_name": "Governance U",
            "organization_type": "university",
            "admin_email": "gov-admin@u.example.com",
            "admin_password": "testpass123",
            "admin_display_name": "Gov Admin",
        },
    )
    assert resp.status_code == 201, resp.text

    admin = (await db_session.execute(select(User).where(User.email == "gov-admin@u.example.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == admin.household_id))).scalar_one()
    assert household.governance_mode == "institution_governed"


@pytest.mark.asyncio
async def test_register_institution_sets_organization_metadata(client: AsyncClient, db_session):
    """The organization_name and organization_type from the request
    body must round-trip into the household record so admin tooling
    can render the institution's identity."""
    resp = await client.post(
        "/api/v1/auth/register-institution",
        json={
            "organization_name": "Acme Bootcamp",
            "organization_type": "bootcamp",
            "admin_email": "meta-admin@acme.example.com",
            "admin_password": "testpass123",
            "admin_display_name": "Meta Admin",
        },
    )
    assert resp.status_code == 201, resp.text

    admin = (await db_session.execute(select(User).where(User.email == "meta-admin@acme.example.com"))).scalar_one()
    household = (await db_session.execute(select(Household).where(Household.id == admin.household_id))).scalar_one()
    assert household.name == "Acme Bootcamp"
    assert household.organization_type == "bootcamp"


@pytest.mark.asyncio
async def test_register_institution_owner_gets_admin_role(client: AsyncClient, db_session):
    """The bootstrapping admin must be persisted as the household
    owner AND as institutional_role=department_admin. The institutional
    invite endpoint guards on that exact pair, so any drift here breaks
    the entire institutional onboarding flow."""
    resp = await client.post(
        "/api/v1/auth/register-institution",
        json={
            "organization_name": "Owner Role College",
            "organization_type": "university",
            "admin_email": "owner-admin@orc.example.com",
            "admin_password": "testpass123",
            "admin_display_name": "Owner Admin",
        },
    )
    assert resp.status_code == 201, resp.text

    admin = (await db_session.execute(select(User).where(User.email == "owner-admin@orc.example.com"))).scalar_one()
    assert admin.role.value == "owner"
    assert admin.institutional_role == "department_admin"


@pytest.mark.asyncio
async def test_register_institution_missing_org_name_rejected(client: AsyncClient):
    """organization_name is required (min_length=1). Pydantic rejects
    an empty / missing field at the schema layer with 422 — the
    handler never runs."""
    resp = await client.post(
        "/api/v1/auth/register-institution",
        json={
            "organization_type": "university",
            "admin_email": "noname@u.example.com",
            "admin_password": "testpass123",
            "admin_display_name": "No Name",
        },
    )
    assert resp.status_code in (400, 422), resp.text


@pytest.mark.asyncio
async def test_institutional_invite_maps_instructor_role(client: AsyncClient, db_session):
    """instructor → household role co_parent. Locks down the
    _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE mapping at the API layer."""
    await _register_inst_admin(client)

    resp = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "instructor-map@u.example.com",
            "display_name": "Instructor Map",
            "institutional_role": "instructor",
        },
    )
    assert resp.status_code == 201, resp.text

    instructor = (
        await db_session.execute(select(User).where(User.email == "instructor-map@u.example.com"))
    ).scalar_one()
    assert instructor.role.value == "co_parent"
    assert instructor.institutional_role == "instructor"


@pytest.mark.asyncio
async def test_institutional_invite_maps_student_role(client: AsyncClient, db_session):
    """student → household role observer, plus a self-linked Child
    row for permission scoping."""
    await _register_inst_admin(client)

    resp = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "student-map@u.example.com",
            "display_name": "Student Map",
            "institutional_role": "student",
            "learner_name": "Student Map",
        },
    )
    assert resp.status_code == 201, resp.text

    student = (await db_session.execute(select(User).where(User.email == "student-map@u.example.com"))).scalar_one()
    assert student.role.value == "observer"
    assert student.institutional_role == "student"
    assert student.linked_child_id is not None


@pytest.mark.asyncio
async def test_institutional_invite_rejects_unknown_institutional_role(client: AsyncClient):
    """An institutional_role not in the role-mapping must 422.
    department_admin is intentionally NOT in the mapping (admins
    are bootstrapped via /register-institution, never invited)."""
    await _register_inst_admin(client)

    resp = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "unknown-role@u.example.com",
            "display_name": "Unknown Role",
            "institutional_role": "principal",  # not in the role map
        },
    )
    assert resp.status_code == 422, resp.text


@pytest.mark.asyncio
async def test_institutional_invite_requires_admin(client: AsyncClient, db_session):
    """Only department admins can invite — any other institutional
    role attempting to invite must 403."""
    from app.core.security import create_access_token

    await _register_inst_admin(client)

    # Bootstrap an instructor via the admin's session.
    r1 = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "requires-admin-instr@u.example.com",
            "display_name": "Instr",
            "institutional_role": "instructor",
        },
    )
    assert r1.status_code == 201, r1.text
    instructor = (
        await db_session.execute(select(User).where(User.email == "requires-admin-instr@u.example.com"))
    ).scalar_one()

    # Switch to the instructor's token, then try to invite.
    token = create_access_token(instructor.id, instructor.household_id, "co_parent")
    client.cookies.delete("access_token")
    client.cookies.set("access_token", token)

    r2 = await client.post(
        "/api/v1/auth/invite",
        json={
            "email": "requires-admin-target@u.example.com",
            "display_name": "Target",
            "institutional_role": "teaching_assistant",
        },
    )
    assert r2.status_code == 403, r2.text


# ══════════════════════════════════════════════════════════════════════
# Targeted coverage: login / refresh / logout / get_me /
# notification_preferences / forgot_password / reset_password
# ══════════════════════════════════════════════════════════════════════


async def _register_and_capture(
    client: AsyncClient,
    email: str,
    *,
    password: str = "securepass123",
    display_name: str = "Session User",
    household_name: str = "Session Family",
) -> dict:
    """Register a fresh user and return the registration response JSON.
    Helper to avoid repeating the same payload in every session test."""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "display_name": display_name,
            "household_name": household_name,
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


# ── login ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_login_sets_httponly_cookies(client: AsyncClient):
    """Login must set both access and refresh cookies with HttpOnly +
    SameSite=lax + Path=/. The cookies are the user's session — JS
    access would expose them to XSS exfiltration."""
    await _register_and_capture(client, "login-cookies@test.com")
    client.cookies.clear()

    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "login-cookies@test.com", "password": "securepass123"},
    )
    assert resp.status_code == 200, resp.text

    headers = resp.headers.get_list("set-cookie")
    access = next((h for h in headers if h.startswith("access_token=")), None)
    refresh = next((h for h in headers if h.startswith("refresh_token=")), None)
    assert access is not None, f"access_token cookie missing: {headers}"
    assert refresh is not None, f"refresh_token cookie missing: {headers}"
    for header in (access, refresh):
        assert "HttpOnly" in header, f"cookie must be HttpOnly: {header}"
        assert "SameSite=lax" in header, f"cookie must be SameSite=lax: {header}"
        assert "Path=/" in header, f"cookie must scope to Path=/: {header}"


@pytest.mark.asyncio
async def test_login_returns_user_data_in_body(client: AsyncClient):
    """Login's TokenResponse body carries the bearer token, type, and
    expiry. NB: it does NOT carry user_id / email / role — those live
    on /auth/me, which the frontend hits right after login. Locking
    down the actual shape so a future ``return user.id`` change can't
    silently leak the household_id pair."""
    await _register_and_capture(client, "login-body@test.com")
    client.cookies.clear()

    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "login-body@test.com", "password": "securepass123"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str) and body["access_token"]
    assert isinstance(body["expires_in"], int) and body["expires_in"] > 0


@pytest.mark.asyncio
async def test_login_nonexistent_email_returns_401(client: AsyncClient):
    """A login attempt for an email that has never registered must
    return 401 with the same generic message used for wrong passwords
    so an attacker can't enumerate existing accounts."""
    client.cookies.clear()
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody-here@test.com", "password": "securepass123"},
    )
    assert resp.status_code == 401, resp.text
    assert "Invalid" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login_creates_refresh_token_in_db(client: AsyncClient, db_session):
    """Successful login must persist a RefreshToken row keyed to the
    user. Without the row, /auth/refresh would have no way to verify
    that the cookie's tid maps to a live, unrevoked session."""
    from app.models.operational import RefreshToken

    await _register_and_capture(client, "login-row@test.com")
    client.cookies.clear()

    user = (await db_session.execute(select(User).where(User.email == "login-row@test.com"))).scalar_one()
    rows_before = (
        (await db_session.execute(select(RefreshToken).where(RefreshToken.user_id == user.id))).scalars().all()
    )
    count_before = len(rows_before)

    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "login-row@test.com", "password": "securepass123"},
    )
    assert resp.status_code == 200, resp.text

    rows_after = (await db_session.execute(select(RefreshToken).where(RefreshToken.user_id == user.id))).scalars().all()
    assert len(rows_after) == count_before + 1, "login must add exactly one RefreshToken row"
    new_row = next(r for r in rows_after if r.id not in {r0.id for r0 in rows_before})
    assert new_row.is_revoked is False
    assert new_row.token_hash, "stored row must carry a hash, never the plaintext"


# ── refresh ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_refresh_rotates_token(client: AsyncClient):
    """Refresh endpoint issues a new refresh token cookie, invalidating
    the old one. The comparison is on the COOKIE values — comparing
    ``json()["access_token"]`` against the registration response's
    access_token is unreliable because the JSON body never echoes the
    refresh token, and access tokens are short-lived enough that
    test-side timing can produce identical iat-second JWTs."""
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh_rotate@test.com",
            "password": "TestPass123!",
            "display_name": "Rotate Test",
            "household_name": "Rotate Family",
        },
    )
    assert reg.status_code == 201
    original_refresh = reg.cookies.get("refresh_token")
    assert original_refresh, "Register must set refresh_token cookie"

    r1 = await client.post(
        "/api/v1/auth/refresh",
        cookies={"refresh_token": original_refresh},
    )
    assert r1.status_code == 200
    new_refresh = r1.cookies.get("refresh_token")
    assert new_refresh, "Refresh must set a new refresh_token cookie"
    assert new_refresh != original_refresh, "Refresh must rotate the token"


@pytest.mark.asyncio
async def test_refresh_no_cookie_returns_403(client: AsyncClient):
    """No refresh_token cookie → 403, never a 500."""
    client.cookies.clear()
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_refresh_expired_token_returns_401(client: AsyncClient, db_session):
    """A refresh token whose JWT is structurally valid but whose
    embedded ``exp`` claim is in the past must be rejected as 401 by
    the decode_token guard — without leaking why."""
    import jwt as _jwt

    from app.core.config import settings as _settings
    from app.models.operational import RefreshToken

    await _register_and_capture(client, "refresh-expired@test.com")
    client.cookies.clear()
    user = (await db_session.execute(select(User).where(User.email == "refresh-expired@test.com"))).scalar_one()

    expired_jwt = _jwt.encode(
        {
            "sub": str(user.id),
            "hid": str(user.household_id),
            "tid": str(uuid.uuid4()),
            "type": "refresh",
            "exp": int(datetime.now(UTC).timestamp()) - 60,
            "iat": int(datetime.now(UTC).timestamp()) - 3600,
        },
        _settings.JWT_SECRET,
        algorithm=_settings.JWT_ALGORITHM,
    )
    client.cookies.set("refresh_token", expired_jwt)
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 401
    # Touch RefreshToken table only to keep the import live for ruff.
    _ = RefreshToken


@pytest.mark.asyncio
async def test_refresh_sets_new_cookies(client: AsyncClient):
    """Refresh response must carry fresh Set-Cookie headers with the
    same security attributes as register/login (HttpOnly etc.)."""
    await _register_and_capture(client, "refresh-cookies@test.com")
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 200

    headers = resp.headers.get_list("set-cookie")
    access = next((h for h in headers if h.startswith("access_token=")), None)
    refresh = next((h for h in headers if h.startswith("refresh_token=")), None)
    assert access is not None and refresh is not None
    for header in (access, refresh):
        assert "HttpOnly" in header
        assert "SameSite=lax" in header
        assert "Path=/" in header


# ── logout ───────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_logout_clears_cookies(client: AsyncClient):
    """Logout must emit ``Max-Age=0`` (or expire-in-the-past) cookies
    so the browser drops them. We check the raw Set-Cookie headers."""
    await _register_and_capture(client, "logout-clear@test.com")

    resp = await client.post("/api/v1/auth/logout")
    assert resp.status_code == 200

    headers = resp.headers.get_list("set-cookie")
    access = next((h for h in headers if h.startswith("access_token=")), None)
    refresh = next((h for h in headers if h.startswith("refresh_token=")), None)
    assert access is not None and refresh is not None
    # Starlette's delete_cookie sets max-age=0 + an expired Expires.
    for header in (access, refresh):
        assert "Max-Age=0" in header or 'expires="Thu, 01 Jan 1970' in header.lower(), (
            f"logout must mark the cookie for deletion, got: {header}"
        )


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client: AsyncClient, db_session):
    """The refresh-token row must be marked is_revoked=True after a
    logout so the cookie can't be replayed even if it leaked."""
    from app.models.operational import RefreshToken

    await _register_and_capture(client, "logout-revoke@test.com")
    user = (await db_session.execute(select(User).where(User.email == "logout-revoke@test.com"))).scalar_one()

    rows = (await db_session.execute(select(RefreshToken).where(RefreshToken.user_id == user.id))).scalars().all()
    assert rows and not rows[0].is_revoked

    resp = await client.post("/api/v1/auth/logout")
    assert resp.status_code == 200
    await db_session.refresh(rows[0])
    assert rows[0].is_revoked is True


# ── get_me ───────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_me_includes_household_id(client: AsyncClient, db_session):
    """/auth/me must include the user's household_id so the frontend
    can scope subsequent requests without a separate /household call."""
    await _register_and_capture(client, "me-household@test.com")

    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 200
    body = resp.json()
    assert "household_id" in body
    user = (await db_session.execute(select(User).where(User.email == "me-household@test.com"))).scalar_one()
    assert body["household_id"] == str(user.household_id)


@pytest.mark.asyncio
async def test_get_me_includes_role(client: AsyncClient):
    """/auth/me must include the user's role so the frontend can
    branch on owner vs co_parent vs observer when rendering UI."""
    await _register_and_capture(client, "me-role@test.com")

    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 200
    body = resp.json()
    assert body["role"] == "owner"


# ── notification_preferences ────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_notification_preferences_returns_defaults(client: AsyncClient):
    """A freshly-registered user has notification_preferences=NULL,
    so the endpoint falls through to the hardcoded all-True default
    set."""
    await _register_and_capture(client, "notif-defaults@test.com")

    resp = await client.get("/api/v1/auth/me/notification-preferences")
    assert resp.status_code == 200, resp.text
    prefs = resp.json()
    for key in (
        "email_daily_summary",
        "email_milestones",
        "email_governance_alerts",
        "email_weekly_digest",
        "email_compliance_warnings",
    ):
        assert prefs.get(key) is True, f"default for {key} should be True, got {prefs}"


@pytest.mark.asyncio
async def test_update_notification_preferences_persists(client: AsyncClient):
    """A PUT with a subset of allowed flags must persist; a follow-up
    GET must read the same values back. Allowed keys are the
    email_* set; anything else is silently dropped (locked down by
    a separate test elsewhere)."""
    await _register_and_capture(client, "notif-persist@test.com")

    put_resp = await client.put(
        "/api/v1/auth/me/notification-preferences",
        json={
            "email_daily_summary": False,
            "email_weekly_digest": False,
            # Unknown key — silently dropped by the allowlist filter.
            "quiet_hours": "22:00-07:00",
        },
    )
    assert put_resp.status_code == 200, put_resp.text
    assert put_resp.json()["email_daily_summary"] is False
    assert put_resp.json()["email_weekly_digest"] is False
    assert "quiet_hours" not in put_resp.json()

    get_resp = await client.get("/api/v1/auth/me/notification-preferences")
    assert get_resp.status_code == 200
    assert get_resp.json()["email_daily_summary"] is False
    assert get_resp.json()["email_weekly_digest"] is False
    # Untouched keys keep their default of True (or are absent — both
    # behaviors are acceptable since the endpoint merges over the
    # stored dict, not the defaults).
    assert get_resp.json().get("email_milestones", True) is True


@pytest.mark.asyncio
async def test_notification_preferences_requires_auth(client: AsyncClient):
    """Both GET and PUT for notification-preferences must reject
    unauthenticated requests with 401."""
    client.cookies.clear()
    client.headers.pop("Authorization", None)

    get_resp = await client.get("/api/v1/auth/me/notification-preferences")
    assert get_resp.status_code == 401
    put_resp = await client.put(
        "/api/v1/auth/me/notification-preferences",
        json={"email_daily_summary": False},
    )
    assert put_resp.status_code == 401


# ── forgot_password / reset_password ────────────────────────────────


@pytest.mark.asyncio
async def test_forgot_password_creates_token_row(client: AsyncClient, db_session):
    """POST /auth/forgot-password must drop a PasswordResetToken row
    even if the email service is mocked. Without the row, the user
    couldn't redeem the link."""
    from unittest.mock import AsyncMock, patch

    from app.models.identity import PasswordResetToken

    await _register_and_capture(client, "forgot-row@test.com")

    rows_before = (await db_session.execute(select(PasswordResetToken))).scalars().all()
    count_before = len(rows_before)

    with patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True):
        resp = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "forgot-row@test.com"},
        )
    assert resp.status_code == 200

    rows_after = (await db_session.execute(select(PasswordResetToken))).scalars().all()
    assert len(rows_after) == count_before + 1, "forgot-password must add exactly one PasswordResetToken row"


@pytest.mark.asyncio
async def test_forgot_password_sends_email(client: AsyncClient):
    """The endpoint dispatches a reset email (subject containing
    'reset') with the plaintext token in the URL of the body."""
    from unittest.mock import AsyncMock, patch

    await _register_and_capture(client, "forgot-email@test.com")

    with patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True) as mock:
        resp = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "forgot-email@test.com"},
        )
    assert resp.status_code == 200
    assert mock.await_count == 1
    args = mock.await_args.args
    assert args[0] == "forgot-email@test.com"
    assert "reset" in args[1].lower()
    assert "token=" in args[2]


@pytest.mark.asyncio
async def test_reset_password_with_valid_token_changes_hash(client: AsyncClient, db_session):
    """After redeeming a reset token, the user's password_hash must
    differ from the pre-reset hash and verify against the new
    plaintext."""
    from unittest.mock import AsyncMock, patch

    from app.core.security import verify_password

    await _register_and_capture(client, "reset-hash@test.com", password="oldpassword123")
    user_pre = (await db_session.execute(select(User).where(User.email == "reset-hash@test.com"))).scalar_one()
    old_hash = user_pre.password_hash

    with patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True) as mock:
        forgot = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "reset-hash@test.com"},
        )
    assert forgot.status_code == 200
    sent_html = mock.await_args.args[2]
    plaintext = sent_html.split("token=")[1].split('"')[0]

    reset = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "brandnewpass456"},
    )
    assert reset.status_code == 200, reset.text

    await db_session.refresh(user_pre)
    assert user_pre.password_hash != old_hash
    assert verify_password("brandnewpass456", user_pre.password_hash)


@pytest.mark.asyncio
async def test_reset_password_revokes_refresh_tokens(client: AsyncClient, db_session):
    """Resetting the password must revoke every active refresh token
    so any session that relied on the old credentials is killed.
    Mirrors test_reset_password_revokes_existing_refresh_tokens but
    drives the API end-to-end without monkeypatching the service."""
    from unittest.mock import AsyncMock, patch

    from app.models.operational import RefreshToken

    await _register_and_capture(client, "reset-revoke@test.com", password="oldpassword123")
    user = (await db_session.execute(select(User).where(User.email == "reset-revoke@test.com"))).scalar_one()

    active_before = (
        (
            await db_session.execute(
                select(RefreshToken).where(
                    RefreshToken.user_id == user.id,
                    RefreshToken.is_revoked == False,  # noqa: E712 SQL three-valued
                )
            )
        )
        .scalars()
        .all()
    )
    assert active_before, "registration should have left at least one active refresh token"

    with patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True) as mock:
        await client.post("/api/v1/auth/forgot-password", json={"email": "reset-revoke@test.com"})
    plaintext = mock.await_args.args[2].split("token=")[1].split('"')[0]

    reset = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": plaintext, "new_password": "brandnewpass456"},
    )
    assert reset.status_code == 200

    active_after = (
        (
            await db_session.execute(
                select(RefreshToken).where(
                    RefreshToken.user_id == user.id,
                    RefreshToken.is_revoked == False,  # noqa: E712
                )
            )
        )
        .scalars()
        .all()
    )
    assert active_after == [], "all active refresh tokens must be revoked after a password reset"


# ══════════════════════════════════════════════════════════════════════
# Targeted coverage: resend_verification + family invites + accept_invite
# ══════════════════════════════════════════════════════════════════════


# ── resend_verification ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_resend_verification_creates_new_token(client: AsyncClient, db_session):
    """POST /auth/resend-verification must drop a fresh
    EmailVerificationToken row keyed to the requesting user."""
    from sqlalchemy import func

    from app.models.identity import EmailVerificationToken

    await _register_and_capture(client, "resend-new@test.com")
    user = (await db_session.execute(select(User).where(User.email == "resend-new@test.com"))).scalar_one()

    count_before = (await db_session.execute(select(func.count(EmailVerificationToken.id)))).scalar_one()

    resp = await client.post("/api/v1/auth/resend-verification")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"sent": True}

    rows = (
        (await db_session.execute(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)))
        .scalars()
        .all()
    )
    count_after = (await db_session.execute(select(func.count(EmailVerificationToken.id)))).scalar_one()
    assert count_after >= count_before + 1
    assert rows, "no token row was persisted for the user"
    assert rows[-1].used_at is None


@pytest.mark.skip(
    reason=(
        "issue_token currently allows multiple coexisting valid tokens; "
        "invalidating prior tokens on resend would require a service-layer "
        "change in app/services/email_verification.py and is out of scope "
        "for this commit. Locking in a skip-marker so the gap stays visible."
    )
)
@pytest.mark.asyncio
async def test_resend_verification_invalidates_old_token(client: AsyncClient, db_session):
    """Aspirational: after resend, the previous token should no longer
    verify. Skipped pending the service-layer change described in the
    skip reason."""


@pytest.mark.asyncio
async def test_resend_verification_for_already_verified_user(client: AsyncClient, db_session):
    """A user whose email is already verified must not be able to
    burn a new verification token — return 400."""
    await _register_and_capture(client, "resend-verified@test.com")
    user = (await db_session.execute(select(User).where(User.email == "resend-verified@test.com"))).scalar_one()
    user.email_verified = True
    await db_session.flush()

    resp = await client.post("/api/v1/auth/resend-verification")
    assert resp.status_code == 400, resp.text
    assert "already verified" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_resend_verification_sends_email(client: AsyncClient):
    """The handler must invoke send_email with the verification subject
    and a tokenised URL in the body."""
    from unittest.mock import AsyncMock, patch

    await _register_and_capture(client, "resend-send@test.com")

    with patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True) as mock:
        resp = await client.post("/api/v1/auth/resend-verification")
    assert resp.status_code == 200, resp.text
    assert mock.await_count == 1
    args = mock.await_args.args
    assert args[0] == "resend-send@test.com"
    assert "verify" in args[1].lower()
    assert "token=" in args[2]


@pytest.mark.asyncio
async def test_resend_verification_requires_auth(client: AsyncClient):
    """No access_token cookie → 401, never a 500."""
    client.cookies.clear()
    client.headers.pop("Authorization", None)
    resp = await client.post("/api/v1/auth/resend-verification")
    assert resp.status_code == 401


# ── invite_family_member (POST /household/invite) ───────────────────


@pytest.mark.asyncio
async def test_invite_family_member_creates_invite_row(auth_client, db_session):
    """The POST handler must persist a FamilyInvite row keyed to the
    inviter's household, with the email + canonical role on the row."""
    from app.models.identity import FamilyInvite

    resp = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "fam-row@test.com", "role": "co_parent"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"invited": True, "email": "fam-row@test.com"}

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "fam-row@test.com"))
    ).scalar_one()
    assert invite.role == "co_parent"
    assert invite.status == "pending"
    assert invite.token, "invite must carry a token"


@pytest.mark.asyncio
async def test_invite_family_member_sends_email(auth_client):
    """send_email must be called with the invitee's address and a
    subject mentioning the inviter."""
    from unittest.mock import AsyncMock, patch

    with patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True) as mock:
        resp = await auth_client.post(
            "/api/v1/auth/household/invite",
            json={"email": "fam-email@test.com", "role": "co_parent"},
        )
    assert resp.status_code == 200, resp.text
    assert mock.await_count == 1
    assert mock.await_args.args[0] == "fam-email@test.com"
    assert "invited" in mock.await_args.args[1].lower()


@pytest.mark.asyncio
async def test_invite_family_member_observer_cannot_invite(observer_client):
    """Observers can read but cannot invite new household members."""
    resp = await observer_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "fam-observer@test.com", "role": "co_parent"},
    )
    assert resp.status_code == 403, resp.text
    assert "observer" in resp.json()["detail"].lower() or "cannot" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_invite_family_member_duplicate_email_rejected(auth_client, db_session):
    """A second pending invite for the same email in the same
    household must be rejected with 409 — stops accidental dupes when
    the inviter retries the form."""
    from app.models.identity import FamilyInvite

    r1 = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "fam-dup@test.com", "role": "co_parent"},
    )
    assert r1.status_code == 200, r1.text

    r2 = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "fam-dup@test.com", "role": "observer"},
    )
    assert r2.status_code == 409, r2.text

    rows = (
        (await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "fam-dup@test.com"))).scalars().all()
    )
    assert len(rows) == 1, f"only the first invite must be persisted; found {len(rows)}"


# ── list_invites (GET /household/invites) ───────────────────────────


@pytest.mark.asyncio
async def test_list_invites_returns_pending(auth_client):
    """A pending invite created via POST must appear in the GET
    listing with the same email + role."""
    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "list-pending@test.com", "role": "observer"},
    )
    assert create.status_code == 200, create.text

    listing = await auth_client.get("/api/v1/auth/household/invites")
    assert listing.status_code == 200, listing.text
    items = listing.json()
    match = next((i for i in items if i["email"] == "list-pending@test.com"), None)
    assert match is not None, f"pending invite missing from listing: {items}"
    assert match["role"] == "observer"


@pytest.mark.asyncio
async def test_list_invites_empty_for_new_household(auth_client):
    """A household with no invites returns an empty list (not 404)."""
    resp = await auth_client.get("/api/v1/auth/household/invites")
    assert resp.status_code == 200
    assert resp.json() == []


# ── revoke_invite (DELETE /household/invites/{id}) ──────────────────


@pytest.mark.asyncio
async def test_revoke_invite_marks_inactive(auth_client, db_session):
    """Revoking a pending invite must flip its status to "revoked";
    a follow-up GET listing must no longer include it."""
    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "revoke-marks@test.com", "role": "co_parent"},
    )
    assert create.status_code == 200, create.text
    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "revoke-marks@test.com"))
    ).scalar_one()

    revoke = await auth_client.delete(f"/api/v1/auth/household/invites/{invite.id}")
    assert revoke.status_code == 200, revoke.text
    assert revoke.json() == {"revoked": True}

    await db_session.refresh(invite)
    assert invite.status == "revoked"

    listing = await auth_client.get("/api/v1/auth/household/invites")
    assert listing.status_code == 200
    assert all(i["email"] != "revoke-marks@test.com" for i in listing.json())


@pytest.mark.asyncio
async def test_revoke_invite_not_found_returns_404(auth_client):
    """A made-up invite id → 404. Cross-household ids fall into the
    same branch (the where-clause filters by household_id), so the
    same response code applies."""
    bogus = uuid.uuid4()
    resp = await auth_client.delete(f"/api/v1/auth/household/invites/{bogus}")
    assert resp.status_code == 404, resp.text


@pytest.mark.asyncio
async def test_revoke_invite_observer_cannot_revoke(auth_client, observer_client, db_session):
    """Observers can read but cannot revoke invites."""
    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "rev-obs-target@test.com", "role": "co_parent"},
    )
    assert create.status_code == 200, create.text
    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "rev-obs-target@test.com"))
    ).scalar_one()

    resp = await observer_client.delete(f"/api/v1/auth/household/invites/{invite.id}")
    assert resp.status_code == 403, resp.text


# ── accept_invite (POST /accept-invite) ─────────────────────────────


async def _create_invite(auth_client, *, email: str, role: str) -> str:
    from sqlalchemy import select as _select

    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": email, "role": role},
    )
    assert create.status_code == 200, create.text
    # Pull the token directly from the DB — the API doesn't return it
    # so the "real" flow is email-only delivery; we cheat for tests.
    from tests.conftest import test_session_factory  # local helper module

    async with test_session_factory() as session:
        row = (await session.execute(_select(FamilyInvite).where(FamilyInvite.email == email))).scalar_one()
        return row.token


@pytest.mark.asyncio
async def test_accept_invite_creates_user_in_household(auth_client, client, db_session):
    """The accepting user must land in the inviter's household."""
    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "accept-user@test.com", "role": "co_parent"},
    )
    assert create.status_code == 200, create.text
    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "accept-user@test.com"))
    ).scalar_one()

    client.cookies.clear()
    resp = await client.post(
        "/api/v1/auth/accept-invite",
        json={"token": invite.token, "password": "newuserpass123", "display_name": "New User"},
    )
    assert resp.status_code == 200, resp.text

    new_user = (await db_session.execute(select(User).where(User.email == "accept-user@test.com"))).scalar_one()
    assert new_user.household_id == invite.household_id


@pytest.mark.asyncio
async def test_accept_invite_sets_correct_role(auth_client, client, db_session):
    """The role on the persisted user must match the role on the
    invite (canonicalised through _normalize_invite_role)."""
    from app.models.identity import FamilyInvite

    for email, role, expected in [
        ("accept-cp@test.com", "co_parent", "co_parent"),
        ("accept-obs@test.com", "observer", "observer"),
    ]:
        create = await auth_client.post(
            "/api/v1/auth/household/invite",
            json={"email": email, "role": role},
        )
        assert create.status_code == 200, create.text
        invite = (await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == email))).scalar_one()

        client.cookies.clear()
        resp = await client.post(
            "/api/v1/auth/accept-invite",
            json={"token": invite.token, "password": "abcdef123456", "display_name": "X"},
        )
        assert resp.status_code == 200, resp.text
        new_user = (await db_session.execute(select(User).where(User.email == email))).scalar_one()
        assert new_user.role.value == expected


@pytest.mark.asyncio
async def test_accept_invite_with_expired_invite_returns_error(auth_client, client, db_session):
    """An invite whose expires_at is in the past → 400 'expired'."""
    from datetime import timedelta

    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "accept-exp@test.com", "role": "co_parent"},
    )
    assert create.status_code == 200, create.text
    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "accept-exp@test.com"))
    ).scalar_one()
    invite.expires_at = datetime.now(UTC) - timedelta(days=1)
    await db_session.flush()

    client.cookies.clear()
    resp = await client.post(
        "/api/v1/auth/accept-invite",
        json={"token": invite.token, "password": "abcdef123456", "display_name": "Y"},
    )
    assert resp.status_code == 400, resp.text
    assert "expired" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_accept_invite_already_accepted_returns_error(auth_client, client, db_session):
    """Accepting an already-accepted invite must 400 — the handler
    queries pending-only, so an accepted row is invisible to it."""
    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "accept-twice@test.com", "role": "observer"},
    )
    assert create.status_code == 200, create.text
    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "accept-twice@test.com"))
    ).scalar_one()
    token = invite.token

    client.cookies.clear()
    first = await client.post(
        "/api/v1/auth/accept-invite",
        json={"token": token, "password": "abcdef123456", "display_name": "Twice"},
    )
    assert first.status_code == 200, first.text

    client.cookies.clear()
    second = await client.post(
        "/api/v1/auth/accept-invite",
        json={"token": token, "password": "abcdef123456", "display_name": "Twice"},
    )
    assert second.status_code == 400, second.text


@pytest.mark.asyncio
async def test_accept_invite_sets_cookies(auth_client, client, db_session):
    """A successful accept must set the access_token cookie so the
    user is logged in immediately and doesn't need a follow-up
    /login round trip."""
    from app.models.identity import FamilyInvite

    create = await auth_client.post(
        "/api/v1/auth/household/invite",
        json={"email": "accept-cookie@test.com", "role": "co_parent"},
    )
    assert create.status_code == 200, create.text
    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "accept-cookie@test.com"))
    ).scalar_one()

    client.cookies.clear()
    resp = await client.post(
        "/api/v1/auth/accept-invite",
        json={"token": invite.token, "password": "abcdef123456", "display_name": "Cookie"},
    )
    assert resp.status_code == 200, resp.text

    headers = resp.headers.get_list("set-cookie")
    access = next((h for h in headers if h.startswith("access_token=")), None)
    assert access is not None, f"access_token cookie missing: {headers}"
    assert "HttpOnly" in access
    assert "SameSite=lax" in access
