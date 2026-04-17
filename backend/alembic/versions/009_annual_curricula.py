"""Add annual_curricula table and link Plans to curricula.

Revision ID: 009
Revises: 008
Create Date: 2026-04-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "annual_curricula",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("learning_map_id", UUID(as_uuid=True), sa.ForeignKey("learning_maps.id", ondelete="SET NULL")),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("subject_name", sa.String(255), nullable=False),
        sa.Column("academic_year", sa.String(20), nullable=False),
        sa.Column("grade_level", sa.String(50)),
        sa.Column("total_weeks", sa.Integer, server_default="36"),
        sa.Column("hours_per_week", sa.Float),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
        sa.Column("scope_sequence", JSONB, nullable=False, server_default="{}"),
        sa.Column("status", sa.String(50), server_default="draft"),
        sa.Column("ai_run_id", UUID(as_uuid=True)),
        sa.Column("approved_at", sa.DateTime(timezone=True)),
        sa.Column("approved_by", UUID(as_uuid=True)),
        sa.Column("actual_record", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_annual_curricula_child ON annual_curricula (child_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_annual_curricula_household ON annual_curricula (household_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_annual_curricula_year ON annual_curricula (child_id, academic_year)")

    # Link Plans to AnnualCurriculum
    op.add_column("plans", sa.Column("annual_curriculum_id", UUID(as_uuid=True), sa.ForeignKey("annual_curricula.id", ondelete="SET NULL")))
    op.add_column("plans", sa.Column("curriculum_week_number", sa.Integer))


def downgrade() -> None:
    op.drop_column("plans", "curriculum_week_number")
    op.drop_column("plans", "annual_curriculum_id")
    op.execute("DROP INDEX IF EXISTS ix_annual_curricula_year")
    op.execute("DROP INDEX IF EXISTS ix_annual_curricula_household")
    op.execute("DROP INDEX IF EXISTS ix_annual_curricula_child")
    op.drop_table("annual_curricula")
