"""voice_output

Adds voice-output governance columns to personalization_policy
(toggle, daily-minutes cap, tts_provider), extends voice_usage_daily
with the TTS counter, and creates the tts_cache table (global cache
of generic phrase audio bytes; no RLS, gated by the phrase allowlist).

Revision ID: 045
Revises: 044
Create Date: 2026-05-14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "045"
down_revision: str | None = "044"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # PersonalizationPolicy: voice-output governance.
    op.add_column(
        "personalization_policy",
        sa.Column("voice_output_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column(
        "personalization_policy",
        sa.Column(
            "voice_output_minutes_daily_cap",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("120"),
        ),
    )
    op.add_column(
        "personalization_policy",
        sa.Column(
            "tts_provider",
            sa.Text(),
            nullable=False,
            server_default=sa.text("'openai'"),
        ),
    )
    op.create_check_constraint(
        "ck_personalization_policy_voice_output_cap_range",
        "personalization_policy",
        "voice_output_minutes_daily_cap >= 0 AND voice_output_minutes_daily_cap <= 600",
    )
    op.create_check_constraint(
        "ck_personalization_policy_tts_provider",
        "personalization_policy",
        "tts_provider IN ('openai', 'elevenlabs')",
    )

    # voice_usage_daily: TTS counter (input counter lives in
    # migration 044's stt_seconds_used column).
    op.add_column(
        "voice_usage_daily",
        sa.Column(
            "tts_seconds_used",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )
    op.create_check_constraint(
        "ck_voice_usage_daily_tts_seconds_nonneg",
        "voice_usage_daily",
        "tts_seconds_used >= 0",
    )

    # tts_cache: global cache of generic phrase audio. NOT RLS-
    # protected; the phrase allowlist gates what reaches the cache.
    op.create_table(
        "tts_cache",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("text_hash", sa.Text(), nullable=False),
        sa.Column("voice_id", sa.Text(), nullable=False),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("audio_bytes", postgresql.BYTEA(), nullable=False),
        sa.Column("audio_duration_seconds", sa.Float(), nullable=False),
        sa.Column("byte_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("access_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.UniqueConstraint("text_hash", "voice_id", "provider", name="uq_tts_cache_key"),
    )
    op.create_index("idx_tts_cache_last_accessed", "tts_cache", ["last_accessed_at"])


def downgrade() -> None:
    op.drop_index("idx_tts_cache_last_accessed", table_name="tts_cache")
    op.drop_table("tts_cache")
    op.drop_constraint("ck_voice_usage_daily_tts_seconds_nonneg", "voice_usage_daily", type_="check")
    op.drop_column("voice_usage_daily", "tts_seconds_used")
    op.drop_constraint("ck_personalization_policy_tts_provider", "personalization_policy", type_="check")
    op.drop_constraint("ck_personalization_policy_voice_output_cap_range", "personalization_policy", type_="check")
    op.drop_column("personalization_policy", "tts_provider")
    op.drop_column("personalization_policy", "voice_output_minutes_daily_cap")
    op.drop_column("personalization_policy", "voice_output_enabled")
