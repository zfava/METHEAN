"""Password reset tokens.

Replaces the legacy in-memory dict in
``app.services.password_reset`` with a durable, hashed, single-use
PostgreSQL table. Adds two ``AuditAction`` values so issuance and
successful reset are traceable.

A partial unique index on ``(user_id) WHERE used_at IS NULL`` enforces
the single-active-token rule at the database level — issuing a fresh
token requires the service to first mark the prior active row used.

PostgreSQL has no ``ALTER TYPE ... DROP VALUE``, so the downgrade
path only reverses the table create; the two new enum values stay on
the type. Documented inline so a future migration author isn't
surprised.

Revision ID: 040
Revises: 039
Create Date: 2026-04-25
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "040"
down_revision: Union[str, None] = "039"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Same join-through-users pattern used by 039_email_verification_tokens
# because this table has no household_id column either.
RLS_USING = (
    "USING (user_id IN ("
    "SELECT id FROM users WHERE household_id = "
    "current_setting('app.current_household_id', true)::uuid"
    "))"
)


def upgrade() -> None:
    op.execute(
        "ALTER TYPE auditaction ADD VALUE IF NOT EXISTS 'password_reset_requested'"
    )
    op.execute(
        "ALTER TYPE auditaction ADD VALUE IF NOT EXISTS 'password_reset_completed'"
    )

    op.create_table(
        "password_reset_tokens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(64), unique=True, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.String(500)),
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_password_reset_tokens_user_id "
        "ON password_reset_tokens (user_id)"
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_password_reset_tokens_token_hash "
        "ON password_reset_tokens (token_hash)"
    )
    # Single-active-token rule: at most one unused token per user.
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_pwreset_user_active "
        "ON password_reset_tokens (user_id) WHERE used_at IS NULL"
    )

    op.execute("ALTER TABLE password_reset_tokens ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE password_reset_tokens FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY password_reset_tokens_household_isolation "
        f"ON password_reset_tokens {RLS_USING}"
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS password_reset_tokens_household_isolation "
        "ON password_reset_tokens"
    )
    op.execute("DROP INDEX IF EXISTS uq_pwreset_user_active")
    op.execute("DROP INDEX IF EXISTS ix_password_reset_tokens_token_hash")
    op.execute("DROP INDEX IF EXISTS ix_password_reset_tokens_user_id")
    op.drop_table("password_reset_tokens")
    # PostgreSQL has no ALTER TYPE DROP VALUE; the two AuditAction
    # values added by upgrade() remain on the type. Re-running
    # upgrade() is safe because of the IF NOT EXISTS guards.
