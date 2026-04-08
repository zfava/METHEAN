"""Add certification_progress to child_preferences.

Revision ID: 014
Revises: 013
Create Date: 2026-04-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "014"
down_revision: Union[str, None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("child_preferences", sa.Column("certification_progress", JSONB, server_default="[]"))


def downgrade() -> None:
    op.drop_column("child_preferences", "certification_progress")
