"""Add activity_feedback table.

Revision ID: 010
Revises: 009
Create Date: 2026-04-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "activity_feedback",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("activity_id", UUID(as_uuid=True), sa.ForeignKey("activities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("feedback_type", sa.String(50), server_default="comment"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_activity_feedback_activity ON activity_feedback (activity_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_activity_feedback_child ON activity_feedback (child_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_activity_feedback_child")
    op.execute("DROP INDEX IF EXISTS ix_activity_feedback_activity")
    op.drop_table("activity_feedback")
