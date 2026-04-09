"""Add billing columns to households and email_verified to users.

Revision ID: 017
Revises: 016
Create Date: 2026-04-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "017"
down_revision: Union[str, None] = "016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Billing columns on households
    op.add_column("households", sa.Column("stripe_customer_id", sa.Text, nullable=True))
    op.add_column("households", sa.Column("subscription_status", sa.Text, server_default="trial"))
    op.add_column("households", sa.Column("trial_ends_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("households", sa.Column("subscription_ends_at", sa.DateTime(timezone=True), nullable=True))

    # Email verification on users
    op.add_column("users", sa.Column("email_verified", sa.Boolean, server_default="false"))


def downgrade() -> None:
    op.drop_column("users", "email_verified")
    op.drop_column("households", "subscription_ends_at")
    op.drop_column("households", "trial_ends_at")
    op.drop_column("households", "subscription_status")
    op.drop_column("households", "stripe_customer_id")
