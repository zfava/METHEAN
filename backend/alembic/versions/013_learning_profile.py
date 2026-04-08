"""Add learning profile fields to child_preferences.

Revision ID: 013
Revises: 012
Create Date: 2026-04-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "013"
down_revision: Union[str, None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("child_preferences", sa.Column("subject_levels", JSONB, server_default="{}"))
    op.add_column("child_preferences", sa.Column("strengths", JSONB, server_default="[]"))
    op.add_column("child_preferences", sa.Column("areas_for_growth", JSONB, server_default="[]"))
    op.add_column("child_preferences", sa.Column("custom_subjects", JSONB, server_default="[]"))
    op.add_column("child_preferences", sa.Column("parent_notes", sa.Text, nullable=True))


def downgrade() -> None:
    for col in ["parent_notes", "custom_subjects", "areas_for_growth", "strengths", "subject_levels"]:
        op.drop_column("child_preferences", col)
