"""Guard: model/migration schema parity for every enum-mapped column.

The drift class this makes extinct: a model maps a native Python enum
(SQLAlchemy binds parameters as ::typename) while the Alembic
migration created a plain String column. The Postgres enum type then
exists only on databases born from Base.metadata.create_all (the test
harness), and every query touching the column explodes on a
migration-born (production-shaped) database. It shipped twice:
fsrsrating (repaired in migration 055) and the family_insights and
wellbeing columns (repaired in migration 060, after the verification
harness caught plans/generate 500ing in PR 58).

Mechanism: unlike the rest of the suite, which builds its schema via
create_all (see conftest.py), this module builds a scratch database
from THE MIGRATIONS, introspects it, and asserts that every
enum-mapped model column has the matching Postgres enum type with
exactly the model's member set. A future model enum without a
matching migration, or a migration whose member list goes stale,
fails here before it can reach a production database.

Pattern note for future schema tests: the scratch database is created,
migrated via `alembic upgrade head` in a subprocess (the same
invocation CI and deploys use), introspected once per session, and
dropped at teardown. Reuse `migrated_schema` if another test needs a
migration-born schema.
"""

import asyncio
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.core.database import Base

BACKEND_DIR = Path(__file__).resolve().parents[1]


def _enum_columns() -> list[tuple[str, str, str, frozenset[str]]]:
    """Every enum-mapped column in the model metadata:
    (table, column, pg type name, member names)."""
    import app.models  # noqa: F401  (register all models on Base)

    found = []
    for table in Base.metadata.sorted_tables:
        for col in table.columns:
            if isinstance(col.type, sa.Enum):
                found.append((table.name, col.name, col.type.name, frozenset(col.type.enums)))
    return found


async def _introspect(url: str) -> dict[tuple[str, str], tuple[str, str, frozenset[str] | None]]:
    """Map (table, column) -> (data_type, udt_name, enum labels or None)."""
    engine = create_async_engine(url)
    out: dict[tuple[str, str], tuple[str, str, frozenset[str] | None]] = {}
    try:
        async with engine.connect() as conn:
            cols = (
                await conn.execute(
                    sa.text(
                        "SELECT table_name, column_name, data_type, udt_name "
                        "FROM information_schema.columns WHERE table_schema = 'public'"
                    )
                )
            ).all()
            labels = (
                await conn.execute(
                    sa.text("SELECT t.typname, e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid = e.enumtypid")
                )
            ).all()
        by_type: dict[str, set[str]] = {}
        for typname, label in labels:
            by_type.setdefault(typname, set()).add(label)
        for table, column, data_type, udt in cols:
            members = frozenset(by_type[udt]) if udt in by_type else None
            out[(table, column)] = (data_type, udt, members)
    finally:
        await engine.dispose()
    return out


@pytest.fixture(scope="module")
def migrated_db_url():
    """A scratch database built from the migrations; yields its URL."""
    base_url = settings.DATABASE_URL
    admin_url = base_url.rsplit("/", 1)[0] + "/postgres"
    scratch_name = f"methean_parity_{uuid.uuid4().hex[:8]}"
    scratch_url = base_url.rsplit("/", 1)[0] + f"/{scratch_name}"

    async def _admin(statement: str) -> None:
        engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")
        try:
            async with engine.connect() as conn:
                await conn.execute(sa.text(statement))
        finally:
            await engine.dispose()

    asyncio.run(_admin(f'CREATE DATABASE "{scratch_name}"'))
    try:
        env = {
            **os.environ,
            "DATABASE_URL": scratch_url,
            "PYTHONPATH": str(BACKEND_DIR),
        }
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=BACKEND_DIR,
            env=env,
            capture_output=True,
            text=True,
            timeout=600,
        )
        assert result.returncode == 0, (
            f"alembic upgrade head failed on the scratch database:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        yield scratch_url
    finally:
        asyncio.run(_admin(f'DROP DATABASE IF EXISTS "{scratch_name}" WITH (FORCE)'))


@pytest.fixture(scope="module")
def migrated_schema(migrated_db_url):
    """Introspection of the migration-built scratch database."""
    return asyncio.run(_introspect(migrated_db_url))


def test_every_enum_mapped_column_is_a_matching_db_enum(migrated_schema):
    """For each enum-mapped model column, the migration-built database
    must carry the same Postgres enum type with exactly the model's
    member set. String columns (the drift), missing types, and stale
    member lists all fail."""
    problems = []
    for table, column, type_name, members in _enum_columns():
        actual = migrated_schema.get((table, column))
        if actual is None:
            problems.append(f"{table}.{column}: column missing from migration-built schema")
            continue
        data_type, udt, db_members = actual
        if data_type != "USER-DEFINED" or udt != type_name:
            problems.append(
                f"{table}.{column}: model maps enum '{type_name}' but the "
                f"migration-built column is {data_type}/{udt}. Add a repair "
                "migration (see 055 and 060 for the pattern)."
            )
            continue
        if db_members != members:
            missing = sorted(members - (db_members or frozenset()))
            extra = sorted((db_members or frozenset()) - members)
            problems.append(
                f"{table}.{column}: enum '{type_name}' member drift; missing in db: {missing}, extra in db: {extra}"
            )
    assert problems == [], "Schema parity violations:\n" + "\n".join(problems)


def test_audit_covers_a_sane_number_of_enum_columns():
    """The audit walked 25 enum-mapped columns when this guard landed.
    If this number ever DROPS unexpectedly, model registration broke
    and the parity test above would silently shrink its coverage."""
    assert len(_enum_columns()) >= 25


@pytest.mark.asyncio
async def test_plans_generate_succeeds_on_a_migration_built_database(migrated_db_url):
    """The exact PR 58 repro, inverted into proof of fix.

    On a migration-born database, POST /children/{id}/plans/generate
    used to 500: the planner's context assembly queries family_insights
    with parameters bound as ::insightstatus, the type that only
    create_all databases carried before migration 060, and the aborted
    transaction then poisoned the rest of the request. This runs the
    full endpoint against the migration-built scratch schema, the
    database shape production actually has.
    """
    from datetime import UTC, date, datetime, timedelta

    from httpx import ASGITransport, AsyncClient
    from sqlalchemy.ext.asyncio import async_sessionmaker

    from app.api.deps import get_db
    from app.core.database import set_tenant
    from app.core.security import create_access_token, hash_password
    from app.main import app
    from app.models.identity import Child, Household, User

    engine = create_async_engine(migrated_db_url, poolclass=None)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        household = Household(
            name="Migration Born Family",
            subscription_status="trialing",
            trial_ends_at=datetime.now(UTC) + timedelta(days=14),
        )
        session.add(household)
        await session.flush()
        await set_tenant(session, household.id)
        user = User(
            household_id=household.id,
            email=f"parity-{uuid.uuid4().hex[:8]}@test.methean.app",
            password_hash=hash_password("ParityPass123!"),
            display_name="Parity Parent",
            role="owner",
            email_verified=True,
        )
        child = Child(household_id=household.id, first_name="Genny")
        session.add_all([user, child])
        await session.flush()

        async def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db
        try:
            token = create_access_token(user.id, household.id, "owner")
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                ac.cookies.set("access_token", token)
                csrf = "parity-csrf-token"
                ac.cookies.set("csrf_token", csrf)
                resp = await ac.post(
                    f"/api/v1/children/{child.id}/plans/generate",
                    json={"week_start": str(date.today()), "daily_minutes": 60},
                    headers={"X-CSRF-Token": csrf},
                )
            assert resp.status_code == 201, (
                f"plans/generate failed on a migration-built database ({resp.status_code}): {resp.text}"
            )
        finally:
            app.dependency_overrides.pop(get_db, None)
    await engine.dispose()
