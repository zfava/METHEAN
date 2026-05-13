"""personalization

Adds a personalization JSONB column to child_preferences and creates
the personalization_policy table. The JSONB column captures the
kid-driven profile (companion, vibe, packs, tone); the policy table
holds household-level allowlists that gate which library entries each
child can pick from. Both are RLS-protected by household_id, matching
the pattern established in migration 042.

The ``'*'`` sentinel inside the policy arrays means "all from the
library" and is expanded at the API layer (see
backend/app/content/personalization_library.py::expand_allowlist) so
new library entries do not require a data migration.

Revision ID: 043
Revises: 042
Create Date: 2026-05-13
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "043"
down_revision: str | None = "042"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Add personalization JSONB column to child_preferences.
    op.add_column(
        "child_preferences",
        sa.Column(
            "personalization",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.execute(
        "COMMENT ON COLUMN child_preferences.personalization IS "
        "'Child-driven personalization profile (companion, vibe, packs, tone).'"
    )

    # 2. Create personalization_policy table. One row per household.
    op.create_table(
        "personalization_policy",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "household_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("households.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "allowed_vibes",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY['*']::text[]"),
        ),
        sa.Column(
            "allowed_interest_tags",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY['*']::text[]"),
        ),
        sa.Column(
            "allowed_voice_personas",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY['*']::text[]"),
        ),
        sa.Column(
            "allowed_iconography_packs",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY['*']::text[]"),
        ),
        sa.Column(
            "allowed_sound_packs",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY['*']::text[]"),
        ),
        sa.Column(
            "allowed_affirmation_tones",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY['*']::text[]"),
        ),
        sa.Column(
            "companion_name_requires_review",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "max_interest_tags_per_child",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("5"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    # 3. Enable RLS + household isolation policy, mirroring migration 042.
    op.execute("ALTER TABLE personalization_policy ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE personalization_policy FORCE ROW LEVEL SECURITY")
    op.execute("DROP POLICY IF EXISTS household_isolation_personalization_policy ON personalization_policy")
    op.execute(
        """
        CREATE POLICY household_isolation_personalization_policy ON personalization_policy
        USING (household_id = current_setting('app.current_household_id', true)::uuid)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS household_isolation_personalization_policy ON personalization_policy")
    op.execute("ALTER TABLE personalization_policy DISABLE ROW LEVEL SECURITY")
    op.drop_table("personalization_policy")
    op.drop_column("child_preferences", "personalization")
