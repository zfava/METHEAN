"""Learner intelligence profiles — persistent per-child learning observations.

Revision ID: 015
Revises: 014
Create Date: 2026-04-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "015"
down_revision: Union[str, None] = "014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "learner_intelligence",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("learning_style_observations", JSONB, server_default="[]"),
        sa.Column("subject_patterns", JSONB, server_default="{}"),
        sa.Column("engagement_patterns", JSONB, server_default="{}"),
        sa.Column("tutor_interaction_analysis", JSONB, server_default="{}"),
        sa.Column("pace_trends", JSONB, server_default="{}"),
        sa.Column("parent_observations", JSONB, server_default="[]"),
        sa.Column("governance_learned_preferences", JSONB, server_default="{}"),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("observation_count", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_learner_intelligence_child_id ON learner_intelligence (child_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_learner_intelligence_household_id ON learner_intelligence (household_id)")

    # RLS policy
    op.execute("ALTER TABLE learner_intelligence ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY learner_intelligence_household_isolation ON learner_intelligence
        USING (household_id = current_setting('app.current_household_id')::uuid)
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS learner_intelligence_household_isolation ON learner_intelligence")
    op.execute("DROP INDEX IF EXISTS ix_learner_intelligence_household_id")
    op.execute("DROP INDEX IF EXISTS ix_learner_intelligence_child_id")
    op.drop_table("learner_intelligence")
