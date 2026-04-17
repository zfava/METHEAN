"""Family invite system for co-parent support.

Revision ID: 018
Revises: 017
Create Date: 2026-04-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "018"
down_revision: Union[str, None] = "017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "family_invites",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("role", sa.String(50), server_default="parent"),
        sa.Column("invited_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("token", sa.Text, nullable=False, unique=True),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_family_invites_household_id ON family_invites (household_id)")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_family_invites_token ON family_invites (token)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_family_invites_token")
    op.execute("DROP INDEX IF EXISTS ix_family_invites_household_id")
    op.drop_table("family_invites")
