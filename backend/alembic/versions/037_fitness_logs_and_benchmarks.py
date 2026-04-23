"""Fitness logs and benchmarks tables.

Tracks per-practice fitness log entries (fitness_logs) and standardised
benchmark scores (fitness_benchmarks), both scoped by household for RLS.

Revision ID: 037
Revises: 036
Create Date: 2026-04-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "037"
down_revision: Union[str, None] = "036"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SAFE_USING = (
    "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
)


def upgrade() -> None:
    # ── fitness_logs ──
    op.create_table(
        "fitness_logs",
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
        ),
        sa.Column(
            "node_id",
            UUID(as_uuid=True),
            sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False),
        sa.Column("measurement_type", sa.String(50), nullable=False),
        sa.Column("measurement_value", sa.Float),
        sa.Column("measurement_unit", sa.String(20)),
        sa.Column("sets", sa.Integer),
        sa.Column("reps", sa.Integer),
        sa.Column("weight_lbs", sa.Float),
        sa.Column("distance_value", sa.Float),
        sa.Column("heart_rate_avg", sa.Integer),
        sa.Column("notes", sa.Text),
        sa.Column(
            "logged_by",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fitness_logs_child_node_logged "
        "ON fitness_logs (child_id, node_id, logged_at)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fitness_logs_household_logged "
        "ON fitness_logs (household_id, logged_at)"
    )

    op.execute("ALTER TABLE fitness_logs ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE fitness_logs FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY fitness_logs_household_isolation ON fitness_logs {SAFE_USING}"
    )

    # ── fitness_benchmarks ──
    op.create_table(
        "fitness_benchmarks",
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
        ),
        sa.Column("benchmark_name", sa.String(255), nullable=False),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("value", sa.Float, nullable=False),
        sa.Column("unit", sa.String(20), nullable=False),
        sa.Column("tier", sa.String(50)),
        sa.Column("percentile", sa.Float),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fitness_benchmarks_child_name_measured "
        "ON fitness_benchmarks (child_id, benchmark_name, measured_at)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fitness_benchmarks_household "
        "ON fitness_benchmarks (household_id)"
    )

    op.execute("ALTER TABLE fitness_benchmarks ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE fitness_benchmarks FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY fitness_benchmarks_household_isolation ON fitness_benchmarks {SAFE_USING}"
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS fitness_benchmarks_household_isolation ON fitness_benchmarks"
    )
    op.execute("DROP INDEX IF EXISTS ix_fitness_benchmarks_household")
    op.execute("DROP INDEX IF EXISTS ix_fitness_benchmarks_child_name_measured")
    op.drop_table("fitness_benchmarks")

    op.execute("DROP POLICY IF EXISTS fitness_logs_household_isolation ON fitness_logs")
    op.execute("DROP INDEX IF EXISTS ix_fitness_logs_household_logged")
    op.execute("DROP INDEX IF EXISTS ix_fitness_logs_child_node_logged")
    op.drop_table("fitness_logs")
