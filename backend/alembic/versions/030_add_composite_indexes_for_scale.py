"""Add composite indexes for scale.

Revision ID: 030
Revises: 029
Create Date: 2026-04-16

Note: ix_child_node_states_child_node already exists from migration 001
(line 514) and is intentionally omitted here to avoid a DuplicateTableError.
"""

from typing import Sequence, Union

from alembic import op

revision: str = "030"
down_revision: Union[str, None] = "029"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_governance_events_household_created ON governance_events (household_id, created_at)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_ai_runs_household_started ON ai_runs (household_id, started_at)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_state_events_child_node ON state_events (child_id, node_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_attempts_activity_child ON attempts (activity_id, child_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_attempts_activity_child")
    op.execute("DROP INDEX IF EXISTS ix_state_events_child_node")
    op.execute("DROP INDEX IF EXISTS ix_ai_runs_household_started")
    op.execute("DROP INDEX IF EXISTS ix_governance_events_household_created")
