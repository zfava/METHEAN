"""add tutor_profile_entries for parent-governed tutor memory

Per-child abstracted teaching strategies the tutor learns over time.
The parent's per-role autonomy policy (migration 056) decides how
entries are written: off forms no memory, standard routes every
proposal through parent approval, autonomous applies immediately under
the standing grant with the grant's event hash recorded on the row.

Privacy is structural: content is a 300-character abstracted strategy,
validated against verbatim speech and clinical language on every write
path in services/tutor_profile.py.

RLS mirrors migration 027's policy pattern exactly.

Revision ID: 057
Revises: 056
Create Date: 2026-06-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "057"
down_revision: str | None = "056"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "tutor_profile_entries"


def upgrade() -> None:
    op.create_table(
        TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id",
            UUID(as_uuid=True),
            sa.ForeignKey("households.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "child_id",
            UUID(as_uuid=True),
            sa.ForeignKey("children.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("content", sa.String(300), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="proposed"),
        sa.Column("grant_event_hash", sa.String(64), nullable=True),
        sa.Column("proposed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("decided_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
    )
    op.create_index(f"ix_{TABLE}_household_id", TABLE, ["household_id"])
    op.create_index(f"ix_{TABLE}_child_id", TABLE, ["child_id"])
    op.create_index("ix_tutor_profile_child_status", TABLE, ["child_id", "status"])

    if op.get_bind().dialect.name == "postgresql":
        policy = f"{TABLE}_household_isolation"
        op.execute(f"ALTER TABLE {TABLE} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {TABLE} FORCE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY {policy} ON {TABLE} "
            "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.execute(f"DROP POLICY IF EXISTS {TABLE}_household_isolation ON {TABLE}")
    op.drop_index("ix_tutor_profile_child_status", table_name=TABLE)
    op.drop_index(f"ix_{TABLE}_child_id", table_name=TABLE)
    op.drop_index(f"ix_{TABLE}_household_id", table_name=TABLE)
    op.drop_table(TABLE)
