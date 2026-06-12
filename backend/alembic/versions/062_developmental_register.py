"""developmental register: tier_band on entries, child_tutor_preferences

Adds the developmental register substrate:
  - tutor_profile_entries.tier_band: the content tier (LEARNING_LEVELS key)
    the child was at, in the relevant subject, when the entry was proposed.
    Lets the efficacy engine notice a strategy tied to an outgrown stage.
  - child_tutor_preferences: one row per child carrying the per-child
    register override (auto when null) and the relationship_memory flag
    (ships off here, consumed by a later prompt). RLS mirrors migration
    027's household_isolation policy exactly.

Revision ID: 062
Revises: 061
Create Date: 2026-06-12
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "062"
down_revision: str | None = "061"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "child_tutor_preferences"


def upgrade() -> None:
    op.add_column(
        "tutor_profile_entries",
        sa.Column("tier_band", sa.String(20), nullable=True),
    )

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
            unique=True,
        ),
        # One of the five LEARNING_LEVELS keys, or null for automatic
        # (derive from the child's content tier).
        sa.Column("register_override", sa.String(20), nullable=True),
        # Ships off; activated by the relationship memory prompt. Values
        # off|on. Built now so a fourth migration need not touch this table.
        sa.Column("relationship_memory", sa.String(8), nullable=False, server_default="off"),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
    )
    op.create_index(f"ix_{TABLE}_household_id", TABLE, ["household_id"])

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
    op.drop_index(f"ix_{TABLE}_household_id", table_name=TABLE)
    op.drop_table(TABLE)
    op.drop_column("tutor_profile_entries", "tier_band")
