"""add ui_preferences JSONB to households

Adds a JSONB column for client-only UI state that should persist across
sessions and devices but does not belong in households.settings (which
carries server-side config like ai_tier).

First use: the curriculum picker rebuild persists which contextual
explainer cards the user has dismissed, so the explainer does not
re-appear on every visit. The shape is intentionally open-ended so
future UI affordances (dismissed tooltips, last-used panels, layout
choices) can be appended without further migrations.

The API layer treats updates as a shallow merge (PATCH semantics):
the client sends only the keys it wants to change, the server merges
them over the existing object. Per-key deletion uses an explicit null.

Backfill: existing rows get the JSONB literal '{}'. The column is
NOT NULL with that server_default attached so freshly inserted rows
also get a non-null default.

Revision ID: 049
Revises: 048
Create Date: 2026-05-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "049"
down_revision: str | None = "048"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "households",
        sa.Column(
            "ui_preferences",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("households", "ui_preferences")
