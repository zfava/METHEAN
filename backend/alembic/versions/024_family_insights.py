"""Family intelligence — cross-child pattern detection.

Revision ID: 024
Revises: 023
Create Date: 2026-04-12
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "024"
down_revision: Union[str, None] = "023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # FamilyInsight table
    op.create_table(
        "family_insights",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("households.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("pattern_type", sa.String(50), nullable=False),
        sa.Column("affected_children", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("affected_nodes", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("affected_subjects", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("evidence_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("recommendation", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="detected"),
        sa.Column("parent_response", sa.Text, nullable=True),
        sa.Column("false_positive", sa.Boolean, nullable=True),
        sa.Column(
            "predictive_child_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("children.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "predictive_node_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("learning_nodes.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_faminsight_household_status_created ON family_insights (household_id, status, created_at DESC)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_faminsight_household_pattern ON family_insights (household_id, pattern_type)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_faminsight_household_predictive ON family_insights (household_id, predictive_child_id)"
    )

    # FamilyInsightConfig table
    default_settings = (
        '{"shared_struggle": {"enabled": true, "min_children": 2, "drift_threshold": 1.5}, '
        '"curriculum_gap": {"enabled": true, "confidence_threshold": 0.5}, '
        '"pacing_divergence": {"enabled": true, "divergence_factor": 2.0}, '
        '"environmental_correlation": {"enabled": true, "window_days": 7}, '
        '"material_effectiveness": {"enabled": true, "min_attempts": 5}}'
    )

    op.create_table(
        "family_insight_configs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("households.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("pattern_settings", postgresql.JSONB, nullable=False, server_default=default_settings),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("household_id", name="uq_insight_config_household"),
    )

    # RLS
    for table in ("family_insights", "family_insight_configs"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"""
            CREATE POLICY {table}_tenant ON {table}
            USING (household_id::text = current_setting('app.current_household_id', true))
        """)


def downgrade() -> None:
    for table in ("family_insight_configs", "family_insights"):
        op.execute(f"DROP POLICY IF EXISTS {table}_tenant ON {table}")
        op.drop_table(table)
