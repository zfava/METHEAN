"""Usage balance: ledger and event tables.

Revision ID: 020
Revises: 019
Create Date: 2026-04-10
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "020"
down_revision: Union[str, None] = "019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usage_ledger",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("period_start", sa.Date, nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("token_budget", sa.Integer, server_default="2000000"),
        sa.Column("tokens_consumed", sa.Integer, server_default="0"),
        sa.Column("ai_calls_count", sa.Integer, server_default="0"),
        sa.Column("last_call_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_usage_ledger_household_period ON usage_ledger (household_id, period_start)")

    op.create_table(
        "usage_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ai_run_id", UUID(as_uuid=True), sa.ForeignKey("ai_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("input_tokens", sa.Integer, server_default="0"),
        sa.Column("output_tokens", sa.Integer, server_default="0"),
        sa.Column("total_tokens", sa.Integer, server_default="0"),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("role", sa.String(100), nullable=False),
        sa.Column("cost_estimate_usd", sa.Float, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_usage_events_household_id ON usage_events (household_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_usage_events_household_id")
    op.drop_table("usage_events")
    op.execute("DROP INDEX IF EXISTS ix_usage_ledger_household_period")
    op.drop_table("usage_ledger")
