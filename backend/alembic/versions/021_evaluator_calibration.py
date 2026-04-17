"""Evaluator calibration system.

Revision ID: 021
Revises: 020
Create Date: 2026-04-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "021"
down_revision: Union[str, None] = "020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # EvaluatorPrediction table
    op.create_table(
        "evaluator_predictions",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attempt_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("predicted_confidence", sa.Float, nullable=False),
        sa.Column("predicted_fsrs_rating", sa.Integer, nullable=False),
        sa.Column("predicted_retention_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_outcome", sa.Integer, nullable=True),
        sa.Column("outcome_recorded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("drift_score", sa.Float, nullable=True),
        sa.Column("calibration_offset_applied", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_evalpred_child_node_created ON evaluator_predictions (child_id, node_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_evalpred_child_unreconciled ON evaluator_predictions (child_id)")

    # CalibrationProfile table
    op.create_table(
        "calibration_profiles",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_predictions", sa.Integer, nullable=False, server_default="0"),
        sa.Column("reconciled_predictions", sa.Integer, nullable=False, server_default="0"),
        sa.Column("mean_drift", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("directional_bias", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("confidence_band_accuracy", postgresql.JSONB, nullable=False,
                   server_default="{}"),
        sa.Column("subject_drift_map", postgresql.JSONB, nullable=False,
                   server_default="{}"),
        sa.Column("recalibration_offset", sa.Float, nullable=False, server_default="0.0"),
        sa.Column("offset_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("parent_override_offset", sa.Float, nullable=True),
        sa.Column("last_computed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("child_id", name="uq_calibration_child"),
    )

    # Enable RLS on new tables
    op.execute("ALTER TABLE evaluator_predictions ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY evaluator_predictions_tenant ON evaluator_predictions
        USING (household_id::text = current_setting('app.current_household_id', true))
    """)
    op.execute("ALTER TABLE calibration_profiles ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY calibration_profiles_tenant ON calibration_profiles
        USING (household_id::text = current_setting('app.current_household_id', true))
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS calibration_profiles_tenant ON calibration_profiles")
    op.execute("DROP POLICY IF EXISTS evaluator_predictions_tenant ON evaluator_predictions")
    op.drop_table("calibration_profiles")
    op.drop_table("evaluator_predictions")
