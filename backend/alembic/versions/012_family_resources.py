"""Add family_resources table.

Revision ID: 012
Revises: 011
Create Date: 2026-04-07
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "012"
down_revision: Union[str, None] = "011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "family_resources",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("resource_type", sa.String(100), server_default="textbook"),
        sa.Column("subject_area", sa.String(100)),
        sa.Column("publisher", sa.String(500)),
        sa.Column("grade_range", sa.String(50)),
        sa.Column("notes", sa.Text),
        sa.Column("status", sa.String(50), server_default="owned"),
        sa.Column("linked_node_ids", JSONB, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_family_resources_household ON family_resources (household_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_family_resources_household")
    op.drop_table("family_resources")
