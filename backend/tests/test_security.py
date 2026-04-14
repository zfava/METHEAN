"""Tests for security utilities."""

import uuid

import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "secure_password_123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_access_token_roundtrip():
    user_id = uuid.uuid4()
    household_id = uuid.uuid4()
    role = "owner"

    token = create_access_token(user_id, household_id, role)
    payload = decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["hid"] == str(household_id)
    assert payload["role"] == role
    assert payload["type"] == "access"


def test_refresh_token_roundtrip():
    user_id = uuid.uuid4()
    household_id = uuid.uuid4()

    token, token_id = create_refresh_token(user_id, household_id)
    payload = decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["hid"] == str(household_id)
    assert payload["tid"] == str(token_id)
    assert payload["type"] == "refresh"


def test_access_token_contains_expiry():
    token = create_access_token(uuid.uuid4(), uuid.uuid4(), "owner")
    payload = decode_token(token)
    assert "exp" in payload
    assert "iat" in payload


# ══════════════════════════════════════════════════
# CSRF Protection Tests
# ══════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_csrf_rejects_without_header(db_session):
    """POST to a protected endpoint without X-CSRF-Token should return 403."""
    from httpx import ASGITransport, AsyncClient
    from app.api.deps import get_db
    from app.main import app

    async def override():
        yield db_session

    app.dependency_overrides[get_db] = override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Set a csrf cookie but do NOT send the X-CSRF-Token header
        ac.cookies.set("csrf_token", "some-token")
        resp = await ac.post("/api/v1/auth/logout")
        assert resp.status_code == 403
        assert resp.json()["code"] == "csrf_failed"
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_csrf_allows_with_valid_header(db_session):
    """POST with matching csrf cookie and header should succeed (not 403)."""
    from httpx import ASGITransport, AsyncClient
    from app.api.deps import get_db
    from app.main import app

    async def override():
        yield db_session

    app.dependency_overrides[get_db] = override
    transport = ASGITransport(app=app)
    token = "valid-csrf-token"
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"X-CSRF-Token": token},
    ) as ac:
        ac.cookies.set("csrf_token", token)
        # logout returns 200 even without auth (best-effort revocation)
        resp = await ac.post("/api/v1/auth/logout")
        assert resp.status_code != 403
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_csrf_skips_get_requests(db_session):
    """GET requests should not require CSRF."""
    from httpx import ASGITransport, AsyncClient
    from app.api.deps import get_db
    from app.main import app

    async def override():
        yield db_session

    app.dependency_overrides[get_db] = override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # No csrf cookie or header at all
        resp = await ac.get("/health")
        assert resp.status_code == 200
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_csrf_skips_auth_endpoints(db_session):
    """POST to /auth/login should not require CSRF."""
    from httpx import ASGITransport, AsyncClient
    from app.api.deps import get_db
    from app.main import app

    async def override():
        yield db_session

    app.dependency_overrides[get_db] = override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # No CSRF cookie or header — login should not be blocked
        resp = await ac.post(
            "/api/v1/auth/login",
            json={"email": "nobody@test.com", "password": "doesntmatter"},
        )
        # 401 (bad credentials), not 403 (CSRF)
        assert resp.status_code == 401
    app.dependency_overrides.clear()


# ══════════════════════════════════════════════════
# RLS Tenant Isolation Tests
# ══════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_rls_isolates_households(db_session):
    """Verify that RLS policies prevent cross-household data access.

    Creates two households with subjects, enables RLS + FORCE,
    then verifies that SET LOCAL scopes visibility per-household.

    RLS only applies to non-superuser roles. In CI the user is already
    non-superuser so policies are enforced automatically. Locally the dev
    user may be superuser — in that case we skip, since stripping superuser
    via ALTER ROLE requires the very privilege we're trying to remove.
    """
    from sqlalchemy import text, select
    from app.core.database import set_tenant
    from app.models.identity import Household
    from app.models.curriculum import Subject

    conn = await db_session.connection()

    # RLS bypass: superusers bypass all RLS. This test needs a non-superuser
    # role to verify policies. In CI we're already non-super. Locally the dev
    # user is typically superuser and ALTER ROLE can't be safely run here.
    is_super_result = await conn.execute(text("SELECT rolsuper FROM pg_roles WHERE rolname = current_user"))
    if is_super_result.scalar():
        pytest.skip("RLS test requires non-superuser role; run in CI or as non-super user")

    # Create two households
    household_a = Household(name="Family A")
    household_b = Household(name="Family B")
    db_session.add_all([household_a, household_b])
    await db_session.flush()

    # Create subjects in each household
    subj_a = Subject(household_id=household_a.id, name="Math A")
    subj_b = Subject(household_id=household_b.id, name="Math B")
    db_session.add_all([subj_a, subj_b])
    await db_session.flush()

    # Enable RLS on subjects table for this test session
    await conn.execute(text("ALTER TABLE subjects ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE subjects FORCE ROW LEVEL SECURITY"))

    # Create policy with safe missing_ok=true parameter
    await conn.execute(text("DROP POLICY IF EXISTS subjects_household_isolation ON subjects"))
    await conn.execute(
        text(
            "CREATE POLICY subjects_household_isolation ON subjects "
            "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
        )
    )

    # Set tenant to household A
    await set_tenant(db_session, household_a.id)

    # Query subjects — should only see household A's
    result = await db_session.execute(select(Subject))
    visible = result.scalars().all()

    visible_names = {s.name for s in visible}
    assert "Math A" in visible_names, "Household A's subject should be visible"
    assert "Math B" not in visible_names, "Household B's subject should be hidden by RLS"

    # Switch tenant to household B
    await set_tenant(db_session, household_b.id)

    result2 = await db_session.execute(select(Subject))
    visible2 = result2.scalars().all()

    visible_names2 = {s.name for s in visible2}
    assert "Math B" in visible_names2, "Household B's subject should be visible"
    assert "Math A" not in visible_names2, "Household A's subject should be hidden by RLS"

    # Cleanup: disable RLS so it doesn't affect other tests
    await conn.execute(text("ALTER TABLE subjects DISABLE ROW LEVEL SECURITY"))


@pytest.mark.asyncio
async def test_set_tenant_scopes_user_lookup(db_session):
    """Verify set_tenant works and the session variable is readable."""
    from sqlalchemy import text
    from app.core.database import set_tenant

    hid = uuid.uuid4()
    await db_session.connection()
    await set_tenant(db_session, hid)

    result = await db_session.execute(text("SELECT current_setting('app.current_household_id')"))
    value = result.scalar()
    assert value == str(hid)
