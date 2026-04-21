"""Async database engine and session factory using asyncpg."""

import uuid
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def set_tenant(session: AsyncSession, household_id: uuid.UUID) -> None:
    """Set the RLS tenant context for the current transaction.

    Executes SET LOCAL so the setting is scoped to the current transaction
    and automatically reset on commit/rollback.

    Uses string formatting (not bound params) because SET doesn't support
    parameterized queries in PostgreSQL. The household_id is pre-validated
    as a UUID so there's no injection risk.
    """
    hid = str(household_id)
    await session.execute(text(f"SET LOCAL app.current_household_id = '{hid}'"))


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
