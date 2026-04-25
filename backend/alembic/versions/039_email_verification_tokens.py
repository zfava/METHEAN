"""email_verification_tokens

Replace the broken "token == user_id" email verification with a proper
single-use, expiring, hashed token persisted in its own table.

Two changes happen here:

1. Two new values are added to the `auditaction` PostgreSQL enum:
   `email_verification_issued` and `email_verification_succeeded`.
   PostgreSQL enum value additions are NOT reversible at the DB level
   without dropping and recreating the type. The downgrade() leaves the
   enum values in place and only drops the new table; this is safe
   because the old code never referenced these enum values.

2. New table `email_verification_tokens` (id, user_id, token_hash,
   expires_at, used_at, ip_address, user_agent, created_at) plus indexes
   on user_id and token_hash, RLS enabled and forced. Because the table
   has no household_id column, the policy joins through users — the
   pattern documented in METHEAN-6-03.

Revision ID: 039
Revises: 038
Create Date: 2026-04-23
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "039"
down_revision: Union[str, None] = "038"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Extend the auditaction enum. ADD VALUE IF NOT EXISTS keeps this
    # idempotent against partial re-runs.
    op.execute("ALTER TYPE auditaction ADD VALUE IF NOT EXISTS 'email_verification_issued'")
    op.execute("ALTER TYPE auditaction ADD VALUE IF NOT EXISTS 'email_verification_succeeded'")

    # 2. Token table.
    op.create_table(
        "email_verification_tokens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True)),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_email_verification_tokens_token_hash "
        "ON email_verification_tokens (token_hash)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_email_verification_tokens_user_id ON email_verification_tokens (user_id)")

    op.execute("ALTER TABLE email_verification_tokens ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE email_verification_tokens FORCE ROW LEVEL SECURITY")
    # No household_id column — isolate via the users join.
    op.execute(
        """
        CREATE POLICY email_verification_tokens_household_isolation
        ON email_verification_tokens
        USING (
            user_id IN (
                SELECT id FROM users
                WHERE household_id = current_setting('app.current_household_id', true)::uuid
            )
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS email_verification_tokens_household_isolation ON email_verification_tokens")
    op.execute("DROP INDEX IF EXISTS ix_email_verification_tokens_user_id")
    op.execute("DROP INDEX IF EXISTS ix_email_verification_tokens_token_hash")
    op.drop_table("email_verification_tokens")
    # NOTE: the new auditaction enum values added by upgrade() are NOT
    # removed here. PostgreSQL has no DROP VALUE for enums; reversing
    # the addition would require dropping every column that uses the
    # auditaction type, recreating the type, and rebuilding the columns.
    # Leaving the values in place is safe — the old code paths simply
    # never write them.
