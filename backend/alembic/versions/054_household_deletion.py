"""add household deletion lifecycle fields

Self-service household deletion (COPPA/GDPR erasure rights) uses a
7-day soft-delete window: deletion_requested_at marks the household
for purge, deletion_requested_by records the requesting parent, and
restore clears both. The daily purge task erases every row, S3 object,
and the Stripe subscription once the window elapses.

Revision ID: 054
Revises: 053
Create Date: 2026-06-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "054"
down_revision: str | None = "053"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("households", sa.Column("deletion_requested_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("households", sa.Column("deletion_requested_by", UUID(as_uuid=True), nullable=True))


def downgrade() -> None:
    op.drop_column("households", "deletion_requested_by")
    op.drop_column("households", "deletion_requested_at")
