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
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import Base
from app.core.security import create_access_token, hash_password
from app.api.deps import get_db
from app.main import app
from app.models.curriculum import LearningMap, Subject
from app.models.identity import Child, Household, User

# Use a test database URL - replace only the database name at the end
TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"

# NullPool is required for async test isolation with asyncpg
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
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
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
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


@pytest_asyncio.fixture
async def auth_client(
    client: AsyncClient, user: User, household: Household,
) -> AsyncClient:
    """Client with access_token cookie set."""
    token = create_access_token(user.id, household.id, "owner")
    client.cookies.set("access_token", token)
    return client


@pytest_asyncio.fixture
async def child(db_session: AsyncSession, household: Household) -> Child:
    c = Child(
        household_id=household.id,
        first_name="Test",
        last_name="Child",
    )
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def subject(db_session: AsyncSession, household: Household) -> Subject:
    s = Subject(household_id=household.id, name="Mathematics")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def learning_map(
    db_session: AsyncSession, household: Household, subject: Subject,
) -> LearningMap:
    lm = LearningMap(
        household_id=household.id,
        subject_id=subject.id,
        name="Elementary Math",
    )
    db_session.add(lm)
    await db_session.flush()
    return lm
