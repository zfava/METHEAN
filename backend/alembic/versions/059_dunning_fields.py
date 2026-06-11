"""add dunning fields to households for failed-payment recovery

Stripe stays authoritative for payment facts; these columns hold
METHEAN's derived dunning policy state. dunning_state walks
none -> grace -> restricted -> canceled under the daily task in
app/tasks/dunning.py, and any successful payment resets it to none
regardless of where it was. last_dunning_email_at enforces the
24-hour email throttle; dunning_emails_sent makes per-state email
sends idempotent across task reruns.

Revision ID: 059
Revises: 058
Create Date: 2026-06-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "059"
down_revision: str | None = "058"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "households",
        sa.Column("dunning_state", sa.String(20), nullable=False, server_default="none"),
    )
    op.add_column(
        "households",
        sa.Column("dunning_started_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "households",
        sa.Column("last_dunning_email_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "households",
        sa.Column("dunning_emails_sent", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("households", "dunning_emails_sent")
    op.drop_column("households", "last_dunning_email_at")
    op.drop_column("households", "dunning_started_at")
    op.drop_column("households", "dunning_state")
