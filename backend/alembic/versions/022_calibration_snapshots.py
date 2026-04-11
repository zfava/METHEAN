"""Calibration snapshots for historical tracking.

Revision ID: 022
Revises: 021
Create Date: 2026-04-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "022"
down_revision: Union[str, None] = "021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "calibration_snapshots",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", sa.dialects.postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mean_drift", sa.Float, nullable=False),
        sa.Column("directional_bias", sa.Float, nullable=False),
        sa.Column("recalibration_offset", sa.Float, nullable=False),
        sa.Column("reconciled_count", sa.Integer, nullable=False),
        sa.Column("confidence_band_accuracy", postgresql.JSONB, nullable=False,
                   server_default="{}"),
        sa.Column("subject_drift_map", postgresql.JSONB, nullable=False,
                   server_default="{}"),
        sa.Column("computed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index(
        "ix_calsnap_child_computed",
        "calibration_snapshots",
        ["child_id", sa.text("computed_at DESC")],
    )

    op.execute("ALTER TABLE calibration_snapshots ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY calibration_snapshots_tenant ON calibration_snapshots
        USING (household_id::text = current_setting('app.current_household_id', true))
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS calibration_snapshots_tenant ON calibration_snapshots")
    op.drop_table("calibration_snapshots")
