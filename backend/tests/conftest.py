"""Shared test fixtures."""

import asyncio
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.database import Base, get_session
from app.core.security import hash_password
from app.main import app
from app.models.identity import Household, User

# Use a test database URL
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/methean", "/methean_test")

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session_factory = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def household(db_session: AsyncSession) -> Household:
    h = Household(name="Test Family", timezone="America/New_York")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def user(db_session: AsyncSession, household: Household) -> User:
    u = User(
        household_id=household.id,
        email="parent@test.com",
        password_hash=hash_password("testpass123"),
        display_name="Test Parent",
        role="owner",
    )
    db_session.add(u)
    await db_session.flush()
    return u
