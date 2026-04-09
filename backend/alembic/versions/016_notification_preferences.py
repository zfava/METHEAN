"""Add notification_preferences JSONB column to users.

Revision ID: 016
Revises: 015
Create Date: 2026-04-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "016"
down_revision: Union[str, None] = "015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_PREFS = '{"email_daily_summary": true, "email_milestones": true, "email_governance_alerts": true, "email_weekly_digest": true, "email_compliance_warnings": true}'


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("notification_preferences", JSONB, server_default=DEFAULT_PREFS),
    )


def downgrade() -> None:
    op.drop_column("users", "notification_preferences")
