"""Add governance tracking fields to activities table.

Revision ID: 002
Revises: 001
Create Date: 2026-04-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("activities", sa.Column(
        "governance_approved", sa.Boolean, server_default="false", nullable=False,
    ))
    op.add_column("activities", sa.Column(
        "governance_reviewed_by", UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
    ))
    op.add_column("activities", sa.Column(
        "governance_reviewed_at", sa.DateTime(timezone=True), nullable=True,
    ))


def downgrade() -> None:
    op.drop_column("activities", "governance_reviewed_at")
    op.drop_column("activities", "governance_reviewed_by")
    op.drop_column("activities", "governance_approved")
