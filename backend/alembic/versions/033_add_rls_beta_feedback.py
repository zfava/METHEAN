"""add_rls_beta_feedback

Idempotent RLS policy for beta_feedback. The initial table migration
(032_beta_feedback) already enables RLS and creates the policy; this
revision formalizes the coverage gap fix and re-applies the policy
safely in environments where it was missing or drifted.

Revision ID: 033
Revises: 032
Create Date: 2026-04-18
"""

from typing import Sequence, Union

from alembic import op

revision: str = "033"
down_revision: Union[str, None] = "032"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop first to keep the migration idempotent across environments
    # where 032 already created the policy.
    op.execute("DROP POLICY IF EXISTS beta_feedback_household_isolation ON beta_feedback")
    op.execute("ALTER TABLE beta_feedback ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE beta_feedback FORCE ROW LEVEL SECURITY")
    op.execute(
        "CREATE POLICY beta_feedback_household_isolation ON beta_feedback "
        "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS beta_feedback_household_isolation ON beta_feedback")
    op.execute("ALTER TABLE beta_feedback DISABLE ROW LEVEL SECURITY")
