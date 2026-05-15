"""TTS cache model.

Global cache of generic phrase audio bytes. NOT household-scoped
and NOT RLS-protected; the phrase allowlist
(``app.services.tts.phrase_allowlist``) is the gate that ensures
only non-PII phrases reach the cache.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class TTSCache(Base):
    __tablename__ = "tts_cache"
    __table_args__ = (UniqueConstraint("text_hash", "voice_id", "provider", name="uq_tts_cache_key"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4
    )
    text_hash: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str] = mapped_column(Text, nullable=False)
    audio_bytes: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    audio_duration_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    byte_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    access_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"), default=0)
