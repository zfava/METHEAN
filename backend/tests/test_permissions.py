"""Tests for granular user permissions.

Covers:
- Owner has all permissions (bypass)
- Observer cannot approve activities
- Co-parent cannot modify constitutional rules
- Scoped permissions: tutor.interact for child A denied for child B
- Permission grant and revoke via API
"""

import pytest

from app.core.permissions import (
    ALL_PERMISSIONS,
    PERM_APPROVE_ACTIVITIES,
    PERM_RULES_CONSTITUTIONAL,
    PERM_TUTOR_INTERACT,
    PERM_VIEW_PROGRESS,
    check_permission,
    grant_role_permissions,
)
from app.core.security import hash_password
from app.models.identity import User, UserPermission


@pytest.mark.asyncio
async def test_owner_has_all_permissions(db_session, household, user):
    """Owners bypass the permission check entirely."""
    for perm in ALL_PERMISSIONS:
        assert await check_permission(db_session, user, perm) is True


@pytest.mark.asyncio
async def test_observer_cannot_approve_activities(db_session, household, user):
    """An observer role with only view.progress should be denied approve.activities."""
    observer = User(
        household_id=household.id,
        email="observer@test.com",
        password_hash=hash_password("observerpass"),
        display_name="Observer",
        role="observer",
    )
    db_session.add(observer)
    await db_session.flush()

    # Grant observer permissions
    await grant_role_permissions(db_session, observer.id, household.id, "observer", user.id)

    assert await check_permission(db_session, observer, PERM_VIEW_PROGRESS) is True
    assert await check_permission(db_session, observer, PERM_APPROVE_ACTIVITIES) is False


@pytest.mark.asyncio
async def test_co_parent_cannot_change_constitutional_rules(db_session, household, user):
    """Co-parents get most permissions but NOT rules.constitutional."""
    co_parent = User(
        household_id=household.id,
        email="coparent@test.com",
        password_hash=hash_password("coparentpass"),
        display_name="Co-Parent",
        role="co_parent",
    )
    db_session.add(co_parent)
    await db_session.flush()

    await grant_role_permissions(db_session, co_parent.id, household.id, "co_parent", user.id)

    assert await check_permission(db_session, co_parent, PERM_APPROVE_ACTIVITIES) is True
    assert await check_permission(db_session, co_parent, PERM_RULES_CONSTITUTIONAL) is False


@pytest.mark.asyncio
async def test_scoped_permission_child_specific(db_session, household, user):
    """Grant tutor.interact for child A only. Should be denied for child B."""
    from app.models.identity import Child

    child_a = Child(household_id=household.id, first_name="Child A")
    child_b = Child(household_id=household.id, first_name="Child B")
    db_session.add_all([child_a, child_b])
    await db_session.flush()

    tutor_user = User(
        household_id=household.id,
        email="tutor@test.com",
        password_hash=hash_password("tutorpass"),
        display_name="Tutor",
        role="observer",
    )
    db_session.add(tutor_user)
    await db_session.flush()

    # Grant tutor.interact scoped only to child A
    db_session.add(
        UserPermission(
            user_id=tutor_user.id,
            household_id=household.id,
            permission=PERM_TUTOR_INTERACT,
            scope_type="child",
            scope_id=child_a.id,
            granted_by=user.id,
        )
    )
    await db_session.flush()

    # Check scoped: allowed for child A
    assert (
        await check_permission(
            db_session,
            tutor_user,
            PERM_TUTOR_INTERACT,
            scope_type="child",
            scope_id=child_a.id,
        )
        is True
    )

    # Check scoped: denied for child B
    assert (
        await check_permission(
            db_session,
            tutor_user,
            PERM_TUTOR_INTERACT,
            scope_type="child",
            scope_id=child_b.id,
        )
        is False
    )


@pytest.mark.asyncio
async def test_permission_grant_and_revoke_api(auth_client, db_session, household, user):
    """Grant and revoke permissions via the API."""
    # Create a target user
    target = User(
        household_id=household.id,
        email="target@test.com",
        password_hash=hash_password("targetpass"),
        display_name="Target",
        role="observer",
    )
    db_session.add(target)
    await db_session.flush()

    # Grant
    resp = await auth_client.post(
        f"/api/v1/users/{target.id}/permissions",
        json={
            "permission": "view.progress",
        },
    )
    assert resp.status_code == 201
    perm_id = resp.json()["id"]

    # List
    list_resp = await auth_client.get(f"/api/v1/users/{target.id}/permissions")
    assert list_resp.status_code == 200
    perms = list_resp.json()
    assert any(p["permission"] == "view.progress" for p in perms)

    # Revoke
    del_resp = await auth_client.delete(f"/api/v1/users/{target.id}/permissions/{perm_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["revoked"] is True

    # Verify gone
    list_resp2 = await auth_client.get(f"/api/v1/users/{target.id}/permissions")
    assert not any(p["id"] == perm_id for p in list_resp2.json())


@pytest.mark.asyncio
async def test_auto_grant_on_register(client):
    """Registration auto-grants owner permissions."""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "permtest@test.com",
            "password": "securepass123",
            "display_name": "Perm Tester",
            "household_name": "Perm Family",
        },
    )
    assert resp.status_code == 201
    # The user should now have permissions (verified via API)
    token = resp.json()["access_token"]
    client.cookies.set("access_token", token)

    # Get user ID from /me
    me = await client.get("/api/v1/auth/me")
    user_id = me.json()["id"]

    # List permissions
    perms_resp = await client.get(f"/api/v1/users/{user_id}/permissions")
    assert perms_resp.status_code == 200
    perms = perms_resp.json()
    assert len(perms) == len(ALL_PERMISSIONS)
