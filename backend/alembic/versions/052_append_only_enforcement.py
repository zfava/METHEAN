"""Append-only enforcement and hash chain for audit events.

Converts the append-only guarantee on governance_events and state_events
from an application convention into a database-enforced property:

1. BEFORE UPDATE OR DELETE triggers on both tables raise, so no role
   that goes through the normal grant path can mutate audit history.
2. governance_events gains event_hash and prev_event_hash columns and
   every existing row is backfilled into a per-household SHA-256 chain
   (ordered by created_at then id, first row chained to the GENESIS
   sentinel). The canonical algorithm lives in
   app.services.governance.compute_event_hash and is imported here so
   backfilled hashes are byte-identical to ones the service writes.

The backfill runs before the triggers are created (the triggers would
reject the backfill UPDATEs) and is idempotent: rows that already carry
an event_hash are kept as-is and only feed their hash to the next link.
Because both tables FORCE ROW LEVEL SECURITY (migrations 027/042), the
backfill scopes itself per household via set_config of
app.current_household_id (transaction-local, expires with the migration
transaction) instead of assuming a BYPASSRLS role.

Postgres-specific DDL and the backfill are guarded by a dialect check so
non-Postgres environments only get the two nullable columns.

Revision ID: 052
Revises: 051
Create Date: 2026-06-09
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

from app.services.governance import build_governance_hash_payload, compute_event_hash

revision: str = "052"
down_revision: str | None = "051"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

APPEND_ONLY_TABLES = ("governance_events", "state_events")

FORBID_MUTATION_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION methean_forbid_mutation() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'governance and state events are append-only';
END;
$$ LANGUAGE plpgsql
"""


def forbid_mutation_trigger_sql(table: str) -> str:
    return (
        f"CREATE TRIGGER {table}_forbid_mutation "
        f"BEFORE UPDATE OR DELETE ON {table} "
        "FOR EACH ROW EXECUTE FUNCTION methean_forbid_mutation()"
    )


def _backfill_hash_chain(bind: sa.engine.Connection) -> None:
    household_ids = bind.execute(text("SELECT id::text FROM households ORDER BY id")).scalars().all()
    for household_id in household_ids:
        # Scope RLS to this household for the SELECT and UPDATEs below.
        # set_config with is_local=true expires with the migration
        # transaction, so nothing leaks past the upgrade.
        bind.execute(
            text("SELECT set_config('app.current_household_id', :hid, true)"),
            {"hid": household_id},
        )
        rows = bind.execute(
            text(
                "SELECT id, household_id::text AS household_id, user_id::text AS user_id, "
                "action, target_type, target_id::text AS target_id, reason, metadata, "
                "created_at, event_hash "
                "FROM governance_events WHERE household_id = :hid "
                "ORDER BY created_at, id"
            ),
            {"hid": household_id},
        ).mappings()

        prev_hash: str | None = None
        for row in rows:
            if row["event_hash"] is not None:
                prev_hash = row["event_hash"]
                continue
            # Some drivers hand JSONB back as a string in raw SQL rows;
            # the canonical payload hashes the dict form.
            metadata = row["metadata"]
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            payload = build_governance_hash_payload(
                household_id=row["household_id"],
                user_id=row["user_id"],
                action=row["action"],
                target_type=row["target_type"],
                target_id=row["target_id"],
                reason=row["reason"],
                metadata=metadata,
                created_at=row["created_at"],
            )
            event_hash = compute_event_hash(payload, prev_hash)
            bind.execute(
                text(
                    "UPDATE governance_events SET event_hash = :event_hash, prev_event_hash = :prev_hash WHERE id = :id"
                ),
                {"event_hash": event_hash, "prev_hash": prev_hash, "id": row["id"]},
            )
            prev_hash = event_hash


def upgrade() -> None:
    op.add_column("governance_events", sa.Column("event_hash", sa.String(64), nullable=True))
    op.add_column("governance_events", sa.Column("prev_event_hash", sa.String(64), nullable=True))

    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    # Backfill must run before the triggers exist: the triggers reject
    # the very UPDATEs the backfill needs.
    _backfill_hash_chain(bind)

    op.execute(FORBID_MUTATION_FUNCTION_SQL)
    for table in APPEND_ONLY_TABLES:
        op.execute(f"DROP TRIGGER IF EXISTS {table}_forbid_mutation ON {table}")
        op.execute(forbid_mutation_trigger_sql(table))


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in APPEND_ONLY_TABLES:
            op.execute(f"DROP TRIGGER IF EXISTS {table}_forbid_mutation ON {table}")
        op.execute("DROP FUNCTION IF EXISTS methean_forbid_mutation()")

    op.drop_column("governance_events", "prev_event_hash")
    op.drop_column("governance_events", "event_hash")
