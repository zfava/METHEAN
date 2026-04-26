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
