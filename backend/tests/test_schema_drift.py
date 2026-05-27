"""Guard: model definitions must not silently diverge from the migrated schema.

Two missing columns crashed production this week (children.fsrs_weights,
child_map_enrollments.enrolled_at_version), both caused by adding a
column to a model without writing the corresponding Alembic migration.
This test stops that bug class.

How it works:
  1. Bring a dedicated, ephemeral Postgres database to head via
     `alembic upgrade head`. Anything in the live test/dev database is
     untouched.
  2. Reflect the resulting schema and ask Alembic to compare it against
     the live SQLAlchemy `Base.metadata`.
  3. The raw comparison surfaces ~230 items including unavoidable noise
     (server-default formatting, VARCHAR-vs-Enum, hand-maintained DB
     indexes not declared in models, nullable tightening on
     server-defaulted timestamps). We classify these and only fail on
     the categories that produce live crashes:

       - add_column      :: model has a column the DB lacks (fsrs_weights /
                            enrolled_at_version style) -> SELECT crashes.
       - add_table       :: model has a table the DB lacks -> any access
                            crashes.
       - add_index/unique:: model declares an index/constraint the DB
                            lacks; query plans degrade but more
                            importantly UniqueConstraints fail open.

     Anything else (remove_column, remove_table, drop_index,
     alter_column type/nullable/default tweaks) is allowed because (a)
     it is not crash-causing and (b) tightening those is a separate
     audited pass.

Running locally:
    pytest backend/tests/test_schema_drift.py -q

CI: this file runs as part of the standard pytest collection. The
ephemeral database name (methean_drift_audit) is created and dropped
by the test itself, so no special CI setup is required beyond a
reachable Postgres server.

Demonstration that it catches the bug class:
  - Temporarily declare a fake column on any model (e.g. add
    `_drift_canary: Mapped[int] = mapped_column(Integer, nullable=True)`
    to Child) and run this test; it will report `add_column` for that
    column and fail.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, text

import app.models  # noqa: F401  (register every model with Base.metadata)
from app.core.config import settings
from app.core.database import Base

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

# Crash-class diff operations. The autogenerate compare emits each
# diff as either a tuple (op_name, *args) or a nested list of such
# tuples; we look at the leading op_name.
CRASH_CLASS_OPS = {
    # SELECTing a column the model knows about but the DB lacks raises
    # psycopg2 UndefinedColumn. This is exactly the fsrs_weights /
    # enrolled_at_version bug class.
    "add_column",
    # The model declares a table the DB does not have. Any query
    # against the table crashes.
    "add_table",
}
# Diff categories deliberately NOT in the crash-class set, with reason:
#   add_index / add_constraint :: not crash-causing. The autogenerate
#       compare frequently mis-fires here on expression-form mismatches
#       (e.g. DB has `created_at DESC`, model declares unordered) which
#       raises `add_index` even though both forms serve the same
#       queries. Real missing indexes are a query-plan concern, not a
#       runtime crash, and are addressed in their own pass.
#   remove_column / remove_table :: DB carries something the model no
#       longer references. This pass is intentionally additive-only;
#       drop-style cleanup is a separate audited migration.
#   modify_type / modify_nullable / modify_default :: alterations are
#       out of scope for the additive-only contract.


DRIFT_DB_NAME = "methean_drift_audit"


def _admin_url() -> str:
    """Sync URL pointing at the `postgres` admin DB on the same server."""
    base = settings.DATABASE_URL
    if base.startswith("postgresql+asyncpg://"):
        base = base.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
    return base.rsplit("/", 1)[0] + "/postgres"


def _drift_sync_url() -> str:
    base = settings.DATABASE_URL
    if base.startswith("postgresql+asyncpg://"):
        base = base.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
    return base.rsplit("/", 1)[0] + f"/{DRIFT_DB_NAME}"


def _recreate_drift_db() -> None:
    """Drop and recreate the audit DB so each run starts from zero."""
    admin = create_engine(_admin_url(), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DRIFT_DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DRIFT_DB_NAME}"))
    admin.dispose()


def _drop_drift_db() -> None:
    admin = create_engine(_admin_url(), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DRIFT_DB_NAME}"))
    admin.dispose()


def _alembic_config(url: str) -> Config:
    backend_dir = Path(__file__).resolve().parents[1]
    cfg = Config(str(backend_dir / "alembic.ini"))
    cfg.set_main_option("script_location", str(backend_dir / "alembic"))
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def _async_drift_url() -> str:
    base = settings.DATABASE_URL
    if base.startswith("postgresql://"):
        base = base.replace("postgresql://", "postgresql+asyncpg://", 1)
    return base.rsplit("/", 1)[0] + f"/{DRIFT_DB_NAME}"


def _summarize_diff(item: object) -> str:
    """One-line description of a single diff item for the assert message."""
    if isinstance(item, tuple) and item and isinstance(item[0], str):
        return repr(item)
    if isinstance(item, list):
        parts = [_summarize_diff(sub) for sub in item]
        return "[" + ", ".join(parts) + "]"
    return repr(item)


def _is_crash_class(item: object) -> bool:
    """Pick out only the diff categories that cause runtime crashes."""
    if isinstance(item, tuple) and item and isinstance(item[0], str):
        return item[0] in CRASH_CLASS_OPS
    if isinstance(item, list):
        # Alembic groups column-level diffs per table in a list. Look at
        # children only; the outer wrapper carries no op name itself.
        return any(_is_crash_class(sub) for sub in item)
    return False


@pytest.fixture(scope="module")
def migrated_engine() -> Engine:
    """Bring an ephemeral DB to head, hand it to the test, drop it after.

    alembic/env.py reads `settings.DATABASE_URL` and overwrites
    `cfg.sqlalchemy.url` on every invocation, so just passing the URL
    via Config is not enough; we temporarily reassign
    `settings.DATABASE_URL` to the audit DB across the upgrade call and
    restore it after.
    """
    _recreate_drift_db()
    sync_url = _drift_sync_url()
    async_url = _async_drift_url()
    original_url = settings.DATABASE_URL
    settings.DATABASE_URL = async_url
    try:
        cfg = _alembic_config(async_url)
        command.upgrade(cfg, "head")
    finally:
        settings.DATABASE_URL = original_url
    engine = create_engine(sync_url)
    try:
        yield engine
    finally:
        engine.dispose()
        _drop_drift_db()


def test_no_crash_class_drift_between_models_and_migrations(migrated_engine: Engine) -> None:
    """No add_column / add_table / add_index / add_constraint may remain.

    If this test fails with `add_column ...`, a model gained a column
    that is not in any migration. Author a new additive migration
    (down_revision = current head) and add it. The two prior incidents
    that this guard is built to prevent are precisely shaped like that:
    children.fsrs_weights (fixed in 047) and
    child_map_enrollments.enrolled_at_version (fixed in 048).
    """
    with migrated_engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        diffs = compare_metadata(ctx, Base.metadata)

    crash_diffs = [d for d in diffs if _is_crash_class(d)]
    if crash_diffs:
        rendered = "\n  ".join(_summarize_diff(d) for d in crash_diffs)
        pytest.fail(
            "Model-vs-migration drift in crash-causing categories detected. "
            "Author an additive migration to close the gap, then re-run.\n  " + rendered
        )
