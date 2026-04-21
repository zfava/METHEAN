"""Achievement and streak tables.

Revision ID: 019
Revises: 018
Create Date: 2026-04-09
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "019"
down_revision: Union[str, None] = "018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "achievements",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("achievement_type", sa.String(100), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("icon", sa.String(10), server_default="⭐"),
        sa.Column("earned_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("metadata", JSONB, server_default="{}"),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_achievements_child_id ON achievements (child_id)")

    op.create_table(
        "streaks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "child_id",
            UUID(as_uuid=True),
            sa.ForeignKey("children.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("current_streak", sa.Integer, server_default="0"),
        sa.Column("longest_streak", sa.Integer, server_default="0"),
        sa.Column("last_activity_date", sa.Date, nullable=True),
        sa.Column("streak_type", sa.String(50), server_default="daily"),
    )
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_streaks_child_id ON streaks (child_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_streaks_child_id")
    op.drop_table("streaks")
    op.execute("DROP INDEX IF EXISTS ix_achievements_child_id")
    op.drop_table("achievements")
