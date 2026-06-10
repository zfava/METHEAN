"""add household_ai_role_settings for per-role AI autonomy policy

Per-household, per-AI-role autonomy policy: off, standard, or
autonomous. Absent rows mean standard (today's behavior: the AI
advises, every persistent change routes through parent approval).
Autonomy is opt-in and never a default: the column's server_default is
standard, and nothing in the system may ever default to autonomous.

RLS mirrors migration 027's policy pattern exactly: household-scoped
isolation with the missing_ok current_setting form.

Revision ID: 056
Revises: 055
Create Date: 2026-06-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "056"
down_revision: str | None = "055"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "household_ai_role_settings"


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
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("autonomy", sa.String(20), nullable=False, server_default="standard"),
        sa.Column("updated_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("household_id", "role", name="uq_household_ai_role"),
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
