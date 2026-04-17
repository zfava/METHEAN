"""Add reading_log_entries table.

Revision ID: 011
Revises: 010
Create Date: 2026-04-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reading_log_entries",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("book_title", sa.String(500), nullable=False),
        sa.Column("book_author", sa.String(500)),
        sa.Column("genre", sa.String(100)),
        sa.Column("subject_area", sa.String(100)),
        sa.Column("status", sa.String(50), server_default="reading"),
        sa.Column("pages_total", sa.Integer),
        sa.Column("pages_read", sa.Integer),
        sa.Column("started_date", sa.Date),
        sa.Column("completed_date", sa.Date),
        sa.Column("minutes_spent", sa.Integer),
        sa.Column("narration", sa.Text),
        sa.Column("parent_notes", sa.Text),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="SET NULL")),
        sa.Column("activity_id", UUID(as_uuid=True), sa.ForeignKey("activities.id", ondelete="SET NULL")),
        sa.Column("child_rating", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_reading_log_child ON reading_log_entries (child_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_reading_log_status ON reading_log_entries (child_id, status)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_reading_log_status")
    op.execute("DROP INDEX IF EXISTS ix_reading_log_child")
    op.drop_table("reading_log_entries")
