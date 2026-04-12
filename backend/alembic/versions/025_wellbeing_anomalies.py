"""Wellbeing anomaly detection tables.

Revision ID: 025
Revises: 024
Create Date: 2026-04-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "025"
down_revision: Union[str, None] = "024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # WellbeingAnomaly table
    op.create_table(
        "wellbeing_anomalies",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("anomaly_type", sa.String(30), nullable=False),
        sa.Column("severity", sa.Float, nullable=False),
        sa.Column("affected_subjects", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("evidence_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("parent_message", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="detected"),
        sa.Column("sensitivity_level", sa.String(20), nullable=False),
        sa.Column("false_positive", sa.Boolean, nullable=True),
        sa.Column("parent_response", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index("ix_wellbeing_child_status_created", "wellbeing_anomalies",
                     ["child_id", "status", sa.text("created_at DESC")])
    op.create_index("ix_wellbeing_household_status", "wellbeing_anomalies",
                     ["household_id", "status"])
    op.create_index("ix_wellbeing_child_type_created", "wellbeing_anomalies",
                     ["child_id", "anomaly_type", sa.text("created_at DESC")])

    # WellbeingConfig table
    op.create_table(
        "wellbeing_configs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("sensitivity_level", sa.String(20), nullable=False, server_default="balanced"),
        sa.Column("custom_thresholds", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("threshold_adjustments", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("total_false_positives", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("child_id", name="uq_wellbeing_config_child"),
    )

    # RLS
    for table in ("wellbeing_anomalies", "wellbeing_configs"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"""
            CREATE POLICY {table}_tenant ON {table}
            USING (household_id::text = current_setting('app.current_household_id', true))
        """)


def downgrade() -> None:
    for table in ("wellbeing_configs", "wellbeing_anomalies"):
        op.execute(f"DROP POLICY IF EXISTS {table}_tenant ON {table}")
        op.drop_table(table)
