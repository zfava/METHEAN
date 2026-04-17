"""Add user_permissions table.

Revision ID: 005
Revises: 004
Create Date: 2026-04-05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_permissions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True),
                  sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("permission", sa.String(100), nullable=False),
        sa.Column("scope_type", sa.String(50), nullable=True),
        sa.Column("scope_id", UUID(as_uuid=True), nullable=True),
        sa.Column("granted_by", UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("granted_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now()),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_user_permissions_user_perm ON user_permissions (user_id, permission)")

    # Enable RLS
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE user_permissions ENABLE ROW LEVEL SECURITY"))
    conn.execute(sa.text("ALTER TABLE user_permissions FORCE ROW LEVEL SECURITY"))
    conn.execute(sa.text(
        "CREATE POLICY user_permissions_household_isolation ON user_permissions "
        "USING (household_id = current_setting('app.current_household_id')::uuid)"
    ))


def downgrade() -> None:
    op.drop_table("user_permissions")
