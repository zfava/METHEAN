"""tutor efficacy: evidence-bearing tutor memory

Closes the loop on the tutor profile. Each active entry is measured
against the child's real attempt outcomes (migration 057 created the
entries; migration 056 created the per-role autonomy policy that
governs how they are written and retired).

Two changes:

1. tutor_profile_entries gains efficacy signals: a conservative label
   (working_well, no_clear_effect, may_have_outgrown, insufficient_data),
   a running observations count, and the last evaluation timestamp. The
   'retired' status value (an entry the child has outgrown, retired
   through the same autonomy policy as everything else) needs no schema
   change because status is a free String column.

2. tutor_entry_observations records one row per evaluation run: the
   active-window success rate, the baseline-window success rate, the
   delta, and the sample sizes behind each. A delta is meaningless
   without its N, so the N travels with it.

RLS mirrors migration 027's policy pattern exactly. Writes to both the
new columns and the new table happen only through
services/tutor_efficacy.py, the single writer (guard-tested).

Revision ID: 061
Revises: 060
Create Date: 2026-06-12
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "061"
down_revision: str | None = "060"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ENTRIES = "tutor_profile_entries"
OBS = "tutor_entry_observations"


def upgrade() -> None:
    op.add_column(ENTRIES, sa.Column("efficacy_label", sa.String(30), nullable=True))
    op.add_column(
        ENTRIES,
        sa.Column("observations_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(ENTRIES, sa.Column("last_evaluated_at", sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        OBS,
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
        sa.Column(
            "entry_id",
            UUID(as_uuid=True),
            sa.ForeignKey("tutor_profile_entries.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("active_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active_success_rate", sa.Float(), nullable=True),
        sa.Column("baseline_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("baseline_success_rate", sa.Float(), nullable=True),
        sa.Column("delta", sa.Float(), nullable=True),
        sa.Column("subject_scope", sa.String(30), nullable=False, server_default="all"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index(f"ix_{OBS}_household_id", OBS, ["household_id"])
    op.create_index(f"ix_{OBS}_child_id", OBS, ["child_id"])
    op.create_index(f"ix_{OBS}_entry_id", OBS, ["entry_id"])

    if op.get_bind().dialect.name == "postgresql":
        policy = f"{OBS}_household_isolation"
        op.execute(f"ALTER TABLE {OBS} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {OBS} FORCE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY {policy} ON {OBS} "
            "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.execute(f"DROP POLICY IF EXISTS {OBS}_household_isolation ON {OBS}")
    op.drop_index(f"ix_{OBS}_entry_id", table_name=OBS)
    op.drop_index(f"ix_{OBS}_child_id", table_name=OBS)
    op.drop_index(f"ix_{OBS}_household_id", table_name=OBS)
    op.drop_table(OBS)

    op.drop_column(ENTRIES, "last_evaluated_at")
    op.drop_column(ENTRIES, "observations_count")
    op.drop_column(ENTRIES, "efficacy_label")
