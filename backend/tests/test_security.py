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
# RLS Tenant Isolation Tests
# ══════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_rls_isolates_households(db_session):
    """Verify that RLS policies prevent cross-household data access.

    Creates two households with subjects, enables RLS on the subjects table,
    then verifies that setting the tenant to household A hides household B's data.
    """
    from sqlalchemy import text
    from app.core.database import set_tenant
    from app.models.identity import Household
    from app.models.curriculum import Subject

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
    conn = await db_session.connection()
    await conn.execute(text("ALTER TABLE subjects ENABLE ROW LEVEL SECURITY"))
    await conn.execute(text("ALTER TABLE subjects FORCE ROW LEVEL SECURITY"))

    # Drop policy if exists (idempotent), then create
    await conn.execute(text(
        "DROP POLICY IF EXISTS subjects_household_isolation ON subjects"
    ))
    await conn.execute(text(
        "CREATE POLICY subjects_household_isolation ON subjects "
        "USING (household_id = current_setting('app.current_household_id')::uuid)"
    ))

    # Set tenant to household A
    await set_tenant(db_session, household_a.id)

    # Query subjects — should only see household A's
    from sqlalchemy import select
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

    result = await db_session.execute(
        text("SELECT current_setting('app.current_household_id')")
    )
    value = result.scalar()
    assert value == str(hid)
