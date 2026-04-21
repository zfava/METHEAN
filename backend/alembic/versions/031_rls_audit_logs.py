"""Add RLS policy to audit_logs table.

audit_logs has household_id but was omitted from migration 027's
HOUSEHOLD_TABLES list. This adds the missing RLS policy.

Revision ID: 031
Revises: 030
Create Date: 2026-04-17
"""

from typing import Sequence, Union

from alembic import op

revision: str = "031"
down_revision: Union[str, None] = "030"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SAFE_USING = "USING (household_id = current_setting('app.current_household_id', true)::uuid)"


def upgrade() -> None:
    op.execute("DROP POLICY IF EXISTS audit_logs_household_isolation ON audit_logs")
    op.execute("ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE audit_logs FORCE ROW LEVEL SECURITY")
    op.execute(f"CREATE POLICY audit_logs_household_isolation ON audit_logs {SAFE_USING}")


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS audit_logs_household_isolation ON audit_logs")
    op.execute("ALTER TABLE audit_logs NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE audit_logs DISABLE ROW LEVEL SECURITY")
