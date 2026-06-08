"""add native_curriculum_access entitlement to households

Adds a per-household boolean entitlement gating native-library curriculum
generation and materialization (the "Approve and Create" / generate-year-plan
path that fires the NATIVE provider when API keys are blank).

Default OFF for everyone. The column is NOT NULL with server_default false,
so every existing row is backfilled to false and the feature is dark for all
households until the entitlement is flipped to true for a specific household.
Going live for a family later is a one-boolean data write: no code change,
no deploy.

A first-class column (not a JSONB key) so it is typed and queryable and sits
alongside the other household-scoped access/mode columns (subscription_status,
governance_mode). The server gate reads it in a request dependency; flipping it
to true requires zero code change.

Revision ID: 051
Revises: 050
Create Date: 2026-06-08
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "051"
down_revision: str | None = "050"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "households",
        sa.Column(
            "native_curriculum_access",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    op.drop_column("households", "native_curriculum_access")
