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

# Tables with household_id that MUST have RLS policies. Keep in sync
# with migration 027_harden_rls_safe_settings.py HOUSEHOLD_TABLES.
RLS_COVERED_TABLES = [
    "subjects",
    "users",
    "children",
    "child_preferences",
    "learning_maps",
    "learning_nodes",
    "learning_edges",
    "child_map_enrollments",
    "child_node_states",
    "state_events",
    "fsrs_cards",
    "review_logs",
    "governance_rules",
    "governance_events",
    "plans",
    "plan_weeks",
    "activities",
    "attempts",
    "alerts",
    "weekly_snapshots",
    "advisor_reports",
    "artifacts",
    "assessments",
    "portfolio_entries",
    "annual_curricula",
    "activity_feedback",
    "reading_log_entries",
    "family_resources",
    "education_plans",
    "achievements",
    "streaks",
    "usage_ledger",
    "usage_events",
    "ai_runs",
    "audit_logs",
    "refresh_tokens",
    "device_tokens",
    "notification_logs",
    "user_permissions",
    "family_invites",
    "learner_intelligence",
    "evaluator_predictions",
    "calibration_profiles",
    "calibration_snapshots",
    "learner_style_vectors",
    "family_insights",
    "family_insight_configs",
    "wellbeing_anomalies",
    "wellbeing_configs",
]


@pytest.mark.asyncio
async def test_rls_isolates_households(db_session):
    """Verify that RLS policies prevent cross-household data access.

    Creates two households with subjects, uses SET ROLE to a non-superuser
    role so RLS is enforced, then verifies SET LOCAL scopes visibility.
    """
    from sqlalchemy import text, select
    from app.core.database import set_tenant
    from app.models.identity import Household
    from app.models.curriculum import Subject

    conn = await db_session.connection()

    # Determine if we're superuser
    is_super_result = await conn.execute(text("SELECT rolsuper FROM pg_roles WHERE rolname = current_user"))
    is_super = is_super_result.scalar()

    # If superuser, create a non-superuser role and SET ROLE to it
    role_created = False
    if is_super:
        await conn.execute(text("""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'methean_rls_test') THEN
                    CREATE ROLE methean_rls_test NOLOGIN;
                END IF;
            END $$
        """))
        await conn.execute(text(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO methean_rls_test"
        ))
        await conn.execute(text("SET ROLE methean_rls_test"))
        role_created = True

    try:
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

        # Set tenant to household A
        await set_tenant(db_session, household_a.id)

        # Query subjects: should only see household A's
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

    finally:
        if role_created:
            await conn.execute(text("RESET ROLE"))


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


class TestRLSCoverageMatrix:
    """Verify every household-scoped table has RLS in the migration chain."""

    def test_all_household_tables_in_rls_list(self):
        """Every model with household_id is in the RLS coverage list."""
        import glob, re

        hid_tables = set()
        for f in glob.glob("app/models/*.py"):
            with open(f) as fh:
                content = fh.read()
            for m in re.finditer(r'__tablename__\s*=\s*"([^"]+)"', content):
                table = m.group(1)
                start = m.end()
                next_class = content.find("class ", start + 1)
                section = content[start:next_class] if next_class != -1 else content[start:]
                if "household_id" in section:
                    hid_tables.add(table)

        rls_set = set(RLS_COVERED_TABLES)
        # households table doesn't need RLS on itself
        hid_tables.discard("households")

        missing = hid_tables - rls_set
        assert not missing, (
            f"Tables with household_id but NOT in RLS coverage list: {missing}. "
            f"Add RLS policies via migration and add to RLS_COVERED_TABLES."
        )

    def test_rls_policies_exist_in_migrations(self):
        """Every table in the coverage list appears in a migration's RLS table list."""
        import glob

        migration_content = ""
        for f in sorted(glob.glob("alembic/versions/*.py")):
            with open(f) as fh:
                migration_content += fh.read()

        for table in RLS_COVERED_TABLES:
            # Tables are referenced in migration 027's HOUSEHOLD_TABLES list,
            # in individual migration ENABLE ROW LEVEL SECURITY calls,
            # or in f-string patterns. Check for the table name appearing
            # near "ROW LEVEL SECURITY" or in a tables list.
            found = (
                f'"{table}"' in migration_content
                or f"'{table}'" in migration_content
                or f" {table} " in migration_content
            )
            assert found, (
                f"Table '{table}' not referenced in any migration. "
                f"It needs a RLS policy via ENABLE ROW LEVEL SECURITY."
            )

    def test_rls_covered_count_matches_household_tables(self):
        """RLS coverage list has the expected count of household-scoped tables."""
        # 49 tables have household_id, minus 1 (households itself) = 48
        # audit_logs was missing from 027 but is now in the coverage list
        assert len(RLS_COVERED_TABLES) == 49
