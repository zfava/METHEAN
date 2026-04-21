"""Add assessments and portfolio_entries tables.

Revision ID: 008
Revises: 007
Create Date: 2026-04-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="SET NULL")),
        sa.Column("assessed_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("assessment_type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("qualitative_notes", sa.Text),
        sa.Column("rubric_scores", JSONB, server_default="{}"),
        sa.Column("mastery_judgment", sa.String(50)),
        sa.Column("confidence_override", sa.Float),
        sa.Column("artifact_ids", JSONB, server_default="[]"),
        sa.Column("subject", sa.String(255)),
        sa.Column("assessed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_assessments_child_node ON assessments (child_id, node_id)")

    op.create_table(
        "portfolio_entries",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assessment_id", UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="SET NULL")),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="SET NULL")),
        sa.Column("entry_type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("content", JSONB, server_default="{}"),
        sa.Column("artifact_id", UUID(as_uuid=True), sa.ForeignKey("artifacts.id", ondelete="SET NULL")),
        sa.Column("subject", sa.String(255)),
        sa.Column("date_completed", sa.Date),
        sa.Column("parent_notes", sa.Text),
        sa.Column("tags", JSONB, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # RLS
    conn = op.get_bind()
    for table in ["assessments", "portfolio_entries"]:
        conn.execute(sa.text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
        conn.execute(sa.text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))
        conn.execute(
            sa.text(
                f"CREATE POLICY {table}_household_isolation ON {table} "
                f"USING (household_id = current_setting('app.current_household_id')::uuid)"
            )
        )


def downgrade() -> None:
    op.drop_table("portfolio_entries")
    op.drop_table("assessments")
