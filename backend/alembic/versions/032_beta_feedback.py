"""Beta user feedback table.

Lets beta users submit feedback from the parent dashboard and track
status of their submissions.

Revision ID: 032
Revises: 031
Create Date: 2026-04-17
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "032"
down_revision: Union[str, None] = "031"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SAFE_USING = "USING (household_id = current_setting('app.current_household_id', true)::uuid)"


def upgrade() -> None:
    op.create_table(
        "beta_feedback",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id",
            UUID(as_uuid=True),
            sa.ForeignKey("households.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("feedback_type", sa.String(30), nullable=False, server_default="general"),
        sa.Column("page_context", sa.String(255)),
        sa.Column("rating", sa.Integer),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("screenshot_url", sa.Text),
        sa.Column("status", sa.String(30), nullable=False, server_default="new"),
        sa.Column("admin_notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_beta_feedback_household_created ON beta_feedback (household_id, created_at DESC)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_beta_feedback_user_created ON beta_feedback (user_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_beta_feedback_status ON beta_feedback (status)")

    # RLS — matches migration 027 pattern
    op.execute("ALTER TABLE beta_feedback ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE beta_feedback FORCE ROW LEVEL SECURITY")
    op.execute(f"CREATE POLICY beta_feedback_household_isolation ON beta_feedback {SAFE_USING}")


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS beta_feedback_household_isolation ON beta_feedback")
    op.execute("DROP INDEX IF EXISTS ix_beta_feedback_status")
    op.execute("DROP INDEX IF EXISTS ix_beta_feedback_user_created")
    op.execute("DROP INDEX IF EXISTS ix_beta_feedback_household_created")
    op.drop_table("beta_feedback")
