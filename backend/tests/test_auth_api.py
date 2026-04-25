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
# Family invite role normalization (METHEAN-6-01)
# ══════════════════════════════════════════════════


async def _register_household_owner(client: AsyncClient) -> None:
    """Helper: register a parent_governed household and stash the access token."""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "owner@invite-test.example.com",
            "password": "testpass123",
            "display_name": "Owner",
            "household_name": "Invite Test Family",
        },
    )
    assert resp.status_code == 201, resp.text
    token = resp.cookies.get("access_token") or resp.json().get("access_token")
    if token:
        client.cookies.set("access_token", token)


@pytest.mark.asyncio
async def test_invite_create_with_co_parent_role(client: AsyncClient, db_session):
    """Canonical co_parent role round-trips and stores cleanly."""
    await _register_household_owner(client)
    resp = await client.post(
        "/api/v1/auth/household/invite",
        json={"email": "second@invite-test.example.com", "role": "co_parent"},
    )
    assert resp.status_code == 200, resp.text

    from app.models.identity import FamilyInvite

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "second@invite-test.example.com"))
    ).scalar_one()
    assert invite.role == "co_parent"


@pytest.mark.asyncio
async def test_invite_create_with_observer_role(client: AsyncClient, db_session):
    """Canonical observer role round-trips."""
    await _register_household_owner(client)
    resp = await client.post(
        "/api/v1/auth/household/invite",
        json={"email": "watch@invite-test.example.com", "role": "observer"},
    )
    assert resp.status_code == 200, resp.text

    from app.models.identity import FamilyInvite

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "watch@invite-test.example.com"))
    ).scalar_one()
    assert invite.role == "observer"


@pytest.mark.asyncio
async def test_invite_create_with_legacy_parent_alias_normalized_to_co_parent(client: AsyncClient, db_session):
    """Legacy `parent` alias is flattened to canonical `co_parent` at the persistence boundary."""
    await _register_household_owner(client)
    resp = await client.post(
        "/api/v1/auth/household/invite",
        json={"email": "legacy-parent@invite-test.example.com", "role": "parent"},
    )
    assert resp.status_code == 200, resp.text

    from app.models.identity import FamilyInvite

    invite = (
        await db_session.execute(
            select(FamilyInvite).where(FamilyInvite.email == "legacy-parent@invite-test.example.com")
        )
    ).scalar_one()
    assert invite.role == "co_parent"


@pytest.mark.asyncio
async def test_invite_create_with_legacy_viewer_alias_normalized_to_observer(client: AsyncClient, db_session):
    """Legacy `viewer` alias is flattened to canonical `observer`."""
    await _register_household_owner(client)
    resp = await client.post(
        "/api/v1/auth/household/invite",
        json={"email": "legacy-viewer@invite-test.example.com", "role": "viewer"},
    )
    assert resp.status_code == 200, resp.text

    from app.models.identity import FamilyInvite

    invite = (
        await db_session.execute(
            select(FamilyInvite).where(FamilyInvite.email == "legacy-viewer@invite-test.example.com")
        )
    ).scalar_one()
    assert invite.role == "observer"


@pytest.mark.asyncio
async def test_invite_create_rejects_unknown_role(client: AsyncClient):
    """Unknown role string is rejected by the Pydantic validator (422) or by the normalizer (400)."""
    await _register_household_owner(client)
    resp = await client.post(
        "/api/v1/auth/household/invite",
        json={"email": "noaccess@invite-test.example.com", "role": "admin"},
    )
    assert resp.status_code in (400, 422), resp.text


@pytest.mark.asyncio
async def test_invite_accept_creates_user_with_canonical_role(client: AsyncClient, db_session):
    """Accepting a co_parent invite creates a User with UserRole.co_parent."""
    from app.models.enums import UserRole
    from app.models.identity import FamilyInvite

    await _register_household_owner(client)
    invite_resp = await client.post(
        "/api/v1/auth/household/invite",
        json={"email": "accept@invite-test.example.com", "role": "co_parent"},
    )
    assert invite_resp.status_code == 200, invite_resp.text

    invite = (
        await db_session.execute(select(FamilyInvite).where(FamilyInvite.email == "accept@invite-test.example.com"))
    ).scalar_one()

    # Detach owner cookie so the accept handler treats the request as the invitee.
    client.cookies.clear()
    accept_resp = await client.post(
        "/api/v1/auth/accept-invite",
        json={
            "token": invite.token,
            "password": "newuserpass123",
            "display_name": "Co Parent",
        },
    )
    assert accept_resp.status_code == 200, accept_resp.text

    new_user = (
        await db_session.execute(select(User).where(User.email == "accept@invite-test.example.com"))
    ).scalar_one()
    assert new_user.role == UserRole.co_parent


@pytest.mark.asyncio
async def test_invite_accept_rejects_corrupted_legacy_role_in_db(client: AsyncClient, db_session):
    """An invite row with a bogus `role` value is rejected at accept time with a 400."""
    import secrets
    from datetime import UTC, datetime, timedelta

    from app.models.identity import FamilyInvite

    await _register_household_owner(client)
    owner = (await db_session.execute(select(User).where(User.email == "owner@invite-test.example.com"))).scalar_one()

    bad_token = secrets.token_urlsafe(32)
    db_session.add(
        FamilyInvite(
            household_id=owner.household_id,
            email="corrupted@invite-test.example.com",
            role="admin",  # not in _INVITE_ROLE_ALIASES
            invited_by=owner.id,
            token=bad_token,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )
    )
    await db_session.commit()

    client.cookies.clear()
    accept_resp = await client.post(
        "/api/v1/auth/accept-invite",
        json={
            "token": bad_token,
            "password": "newuserpass123",
            "display_name": "Should Fail",
        },
    )
    assert accept_resp.status_code == 400, accept_resp.text
