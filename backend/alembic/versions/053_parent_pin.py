"""add parent_pin_hash to users for kid-mode exit

Kid mode (child-scoped sessions) is exited with a short parent PIN
instead of the full password. The PIN is hashed with the exact same
bcrypt utility as passwords and stored per parent user. Nullable:
households that never set a PIN exit kid mode with the password.

No RLS change needed: the users table is already covered by the
household isolation policy (see docs/rls-coverage.md).

Revision ID: 053
Revises: 052
Create Date: 2026-06-09
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "053"
down_revision: str | None = "052"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("parent_pin_hash", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "parent_pin_hash")
