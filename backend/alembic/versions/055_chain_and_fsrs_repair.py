"""repair fsrsrating enum labels and governance chain coverage

Two latent defects surfaced by the Family Record integrity badge:

1. fsrsrating labels: migration 001 created the enum with the integer
   VALUES ('1'..'4') as labels, while the ORM writes member NAMES
   ('again', 'hard', 'good', 'easy'). Every FSRS review insert on a
   migration-built database crashed. The labels are renamed in place
   (rows are preserved; rename is metadata-only). Databases created via
   create_all already carry the names and are skipped.

2. Chain repair: before this revision, twenty code paths constructed
   GovernanceEvent rows directly, bypassing the migration 052 hash
   chain (null event_hash), which makes verification fail for any
   household that used assessments, curriculum tools, overrides, or
   wellbeing features. All call sites now route through
   log_governance_event; this migration repairs existing chains by
   recomputing hashes from the first inconsistent row onward, per
   household, inside a sanctioned trigger-disable window (same
   rationale as the purge task: the triggers exist to prevent silent
   revision, and a migration in version control that repairs a
   provably broken chain is neither silent nor revisionist). Hashes of
   already-consistent prefixes are untouched. No sealed Family Record
   bundles existed before this revision, so no exported head hash is
   invalidated.

Revision ID: 055
Revises: 054
Create Date: 2026-06-10
"""

from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

from app.services.governance import build_governance_hash_payload, compute_event_hash

revision: str = "055"
down_revision: str | None = "054"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_FSRS_RENAMES = (("1", "again"), ("2", "hard"), ("3", "good"), ("4", "easy"))


def _rename_fsrs_labels(forward: bool) -> None:
    pairs = _FSRS_RENAMES if forward else tuple((new, old) for old, new in _FSRS_RENAMES)
    for old, new in pairs:
        op.execute(
            f"""
DO $$ BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_enum e JOIN pg_type t ON t.oid = e.enumtypid
        WHERE t.typname = 'fsrsrating' AND e.enumlabel = '{old}'
    ) THEN
        ALTER TYPE fsrsrating RENAME VALUE '{old}' TO '{new}';
    END IF;
END $$;
"""
        )


def _repair_chains(bind) -> None:
    household_ids = bind.execute(text("SELECT id::text FROM households ORDER BY id")).scalars().all()
    for household_id in household_ids:
        bind.execute(
            text("SELECT set_config('app.current_household_id', :hid, true)"),
            {"hid": household_id},
        )
        rows = bind.execute(
            text(
                "SELECT id, household_id::text AS household_id, user_id::text AS user_id, "
                "action, target_type, target_id::text AS target_id, reason, metadata, "
                "created_at, event_hash, prev_event_hash "
                "FROM governance_events WHERE household_id = :hid "
                "ORDER BY created_at, id"
            ),
            {"hid": household_id},
        ).mappings().all()

        prev_hash: str | None = None
        repairing = False
        for row in rows:
            metadata = row["metadata"]
            if isinstance(metadata, str):
                import json

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
            expected = compute_event_hash(payload, prev_hash)
            if not repairing and row["event_hash"] == expected and row["prev_event_hash"] == prev_hash:
                prev_hash = expected
                continue
            # First inconsistency found: every event from here forward
            # is re-chained onto the last consistent hash.
            repairing = True
            bind.execute(
                text(
                    "UPDATE governance_events SET event_hash = :eh, prev_event_hash = :ph WHERE id = :id"
                ),
                {"eh": expected, "ph": prev_hash, "id": row["id"]},
            )
            prev_hash = expected


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    _rename_fsrs_labels(forward=True)

    op.execute("ALTER TABLE governance_events DISABLE TRIGGER governance_events_forbid_mutation")
    _repair_chains(bind)
    op.execute("ALTER TABLE governance_events ENABLE TRIGGER governance_events_forbid_mutation")


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    # Chain repair is not reversed: the repaired hashes are simply the
    # correct ones. Only the enum labels revert for symmetry.
    _rename_fsrs_labels(forward=False)
