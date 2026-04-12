"""Learner style vectors — computed learning profile per child.

Revision ID: 023
Revises: 022
Create Date: 2026-04-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "023"
down_revision: Union[str, None] = "022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "learner_style_vectors",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        # Computed dimensions
        sa.Column("optimal_session_minutes", sa.Integer, nullable=True),
        sa.Column("socratic_responsiveness", sa.Float, nullable=True),
        sa.Column("frustration_threshold", sa.Float, nullable=True),
        sa.Column("recovery_rate", sa.Float, nullable=True),
        sa.Column("time_of_day_peak", sa.Integer, nullable=True),
        sa.Column("subject_affinity_map", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("modality_preference", sa.String(20), nullable=True),
        sa.Column("pacing_preference", sa.Float, nullable=True),
        sa.Column("independence_level", sa.Float, nullable=True),
        sa.Column("attention_pattern", sa.String(20), nullable=True),
        # Metadata
        sa.Column("data_points_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("dimensions_active", sa.Integer, nullable=False, server_default="0"),
        # Parent governance
        sa.Column("parent_overrides", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("parent_bounds", postgresql.JSONB, nullable=False, server_default="{}"),
        # Timestamps
        sa.Column("last_computed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("child_id", name="uq_style_vector_child"),
    )

    # RLS
    op.execute("ALTER TABLE learner_style_vectors ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY learner_style_vectors_tenant ON learner_style_vectors
        USING (household_id::text = current_setting('app.current_household_id', true))
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS learner_style_vectors_tenant ON learner_style_vectors")
    op.drop_table("learner_style_vectors")
