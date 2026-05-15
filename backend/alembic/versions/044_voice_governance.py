"""voice_governance

Adds voice-input governance columns to personalization_policy
(toggle, daily-minutes cap, whisper provider) and creates the
voice_usage_daily counter table that the transcribe endpoint debits
atomically via INSERT ... ON CONFLICT DO UPDATE.

The cap covers voice INPUT (STT) only in this migration. Voice
OUTPUT (TTS) lives in migration 045 alongside the tts_cache table;
keeping them separate makes either feature reversible in isolation.

Revision ID: 044
Revises: 043
Create Date: 2026-05-14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "044"
down_revision: str | None = "043"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # personalization_policy: voice-input governance columns.
    op.add_column(
        "personalization_policy",
        sa.Column("voice_input_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column(
        "personalization_policy",
        sa.Column(
            "voice_minutes_daily_cap",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("60"),
        ),
    )
    op.add_column(
        "personalization_policy",
        sa.Column(
            "whisper_provider",
            sa.Text(),
            nullable=False,
            server_default=sa.text("'openai'"),
        ),
    )
    op.create_check_constraint(
        "ck_personalization_policy_voice_cap_range",
        "personalization_policy",
        "voice_minutes_daily_cap >= 0 AND voice_minutes_daily_cap <= 480",
    )
    op.create_check_constraint(
        "ck_personalization_policy_whisper_provider",
        "personalization_policy",
        "whisper_provider IN ('openai', 'local')",
    )

    # voice_usage_daily: one row per (child, usage_date).
    op.create_table(
        "voice_usage_daily",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("child_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("usage_date", sa.Date(), nullable=False),
        sa.Column(
            "stt_seconds_used",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("child_id", "usage_date", name="uq_voice_usage_daily_child_date"),
        sa.CheckConstraint("stt_seconds_used >= 0", name="ck_voice_usage_daily_seconds_nonneg"),
    )
    op.create_index(
        "idx_voice_usage_daily_household_date",
        "voice_usage_daily",
        ["household_id", "usage_date"],
    )

    # RLS, mirroring migration 042.
    op.execute("ALTER TABLE voice_usage_daily ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE voice_usage_daily FORCE ROW LEVEL SECURITY")
    op.execute("DROP POLICY IF EXISTS household_isolation_voice_usage_daily ON voice_usage_daily")
    op.execute(
        """
        CREATE POLICY household_isolation_voice_usage_daily ON voice_usage_daily
        USING (household_id = current_setting('app.current_household_id', true)::uuid)
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS household_isolation_voice_usage_daily ON voice_usage_daily")
    op.execute("ALTER TABLE voice_usage_daily DISABLE ROW LEVEL SECURITY")
    op.drop_index("idx_voice_usage_daily_household_date", table_name="voice_usage_daily")
    op.drop_table("voice_usage_daily")
    op.drop_constraint("ck_personalization_policy_whisper_provider", "personalization_policy", type_="check")
    op.drop_constraint("ck_personalization_policy_voice_cap_range", "personalization_policy", type_="check")
    op.drop_column("personalization_policy", "whisper_provider")
    op.drop_column("personalization_policy", "voice_minutes_daily_cap")
    op.drop_column("personalization_policy", "voice_input_enabled")
