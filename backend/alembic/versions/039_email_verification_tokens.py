"""Email verification tokens.

Replaces the legacy ``token = user_id`` scheme with a hashed,
expiring, single-use token persisted in PostgreSQL. Adds two
``AuditAction`` enum values so issuance and successful verification
are traceable in the audit log.

Adding values to a PostgreSQL enum type is irreversible at the DB
level — `ALTER TYPE ... DROP VALUE` does not exist. The downgrade
path therefore only reverses the table create + RLS policy; the two
new enum values stay on the type. Documented inline so a future
migration author isn't surprised.

Revision ID: 039
Revises: 038
Create Date: 2026-04-25
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "039"
down_revision: Union[str, None] = "038"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# This table has no household_id column, so the RLS policy joins
# through users to scope by household. Owners cannot see other
# households' verification tokens.
RLS_USING = (
    "USING (user_id IN ("
    "SELECT id FROM users WHERE household_id = "
    "current_setting('app.current_household_id', true)::uuid"
    "))"
)


def upgrade() -> None:
    op.execute(
        "ALTER TYPE auditaction ADD VALUE IF NOT EXISTS 'email_verification_issued'"
    )
    op.execute(
        "ALTER TYPE auditaction ADD VALUE IF NOT EXISTS 'email_verification_succeeded'"
    )

    op.create_table(
        "email_verification_tokens",
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
        "CREATE INDEX IF NOT EXISTS ix_email_verification_tokens_user_id "
        "ON email_verification_tokens (user_id)"
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_email_verification_tokens_token_hash "
        "ON email_verification_tokens (token_hash)"
    )

    op.execute("ALTER TABLE email_verification_tokens ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE email_verification_tokens FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY email_verification_tokens_household_isolation "
        f"ON email_verification_tokens {RLS_USING}"
    )


def downgrade() -> None:
    op.execute(
        "DROP POLICY IF EXISTS email_verification_tokens_household_isolation "
        "ON email_verification_tokens"
    )
    op.execute("DROP INDEX IF EXISTS ix_email_verification_tokens_token_hash")
    op.execute("DROP INDEX IF EXISTS ix_email_verification_tokens_user_id")
    op.drop_table("email_verification_tokens")
    # PostgreSQL has no `ALTER TYPE ... DROP VALUE`, so the two
    # AuditAction enum values added by upgrade() remain on the type.
    # Re-running upgrade() is safe because of the IF NOT EXISTS guards.
