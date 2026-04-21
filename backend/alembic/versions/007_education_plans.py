"""Add education_plans table.

Revision ID: 007
Revises: 006
Create Date: 2026-04-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "education_plans",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "child_id",
            UUID(as_uuid=True),
            sa.ForeignKey("children.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), server_default="draft"),
        sa.Column("year_plans", JSONB, nullable=False, server_default="{}"),
        sa.Column("goals", JSONB, server_default="{}"),
        sa.Column("baseline_assessment", JSONB, server_default="{}"),
        sa.Column("ai_run_id", UUID(as_uuid=True)),
        sa.Column("approved_at", sa.DateTime(timezone=True)),
        sa.Column("approved_by", UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # RLS
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE education_plans ENABLE ROW LEVEL SECURITY"))
    conn.execute(sa.text("ALTER TABLE education_plans FORCE ROW LEVEL SECURITY"))
    conn.execute(
        sa.text(
            "CREATE POLICY education_plans_household_isolation ON education_plans "
            "USING (household_id = current_setting('app.current_household_id')::uuid)"
        )
    )


def downgrade() -> None:
    op.drop_table("education_plans")
