"""record which provider answered each AI run

Adds ai_runs.provider: the named provider that produced a run
(anthropic, openai, local, native, mock). Provenance the family can
audit, and proof that a tutor turn ran on local inference rather than
an external vendor. Nullable so historical rows predating the column
stay readable; model_used continues to hold the model identifier.

Revision ID: 063
Revises: 062
Create Date: 2026-06-13
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "063"
down_revision: str | None = "062"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ai_runs",
        sa.Column("provider", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("ai_runs", "provider")
