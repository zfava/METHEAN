"""Shared test fixtures."""

import asyncio
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

from app.api.deps import get_db
from app.core.config import settings
from app.core.database import Base, set_tenant
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.curriculum import LearningMap, Subject
from app.models.identity import Child, Household, User

# Tests rely on the deterministic mock provider as a stand-in for real
# AI calls. Production now defaults AI_MOCK_ENABLED to False, so flip
# it on for the test session to keep existing gateway-driven tests
# working. Tests that need the prod default (e.g. the new
# AIProviderUnavailableError path) override via monkeypatch.
settings.AI_MOCK_ENABLED = True

# Use a test database URL - replace only the database name at the end
TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"

# NullPool is required for async test isolation with asyncpg
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
test_session_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# Fixed CSRF token for all test clients
TEST_CSRF_TOKEN = "test-csrf-token-for-tests"


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
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"X-CSRF-Token": TEST_CSRF_TOKEN},
    ) as ac:
        ac.cookies.set("csrf_token", TEST_CSRF_TOKEN)
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def household(db_session: AsyncSession) -> Household:
    from datetime import UTC, datetime, timedelta

    # Default test household is in an active trial so the
    # require_active_subscription gate doesn't block tests that aren't
    # specifically exercising billing state. Tests that need a
    # canceled/past_due/etc. household construct their own Household.
    h = Household(
        name="Test Family",
        timezone="America/New_York",
        subscription_status="trialing",
        trial_ends_at=datetime.now(UTC) + timedelta(days=14),
    )
    db_session.add(h)
    await db_session.flush()
    # Set RLS tenant context so all subsequent queries are scoped
    await set_tenant(db_session, h.id)
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
    client: AsyncClient,
    user: User,
    household: Household,
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
    db_session: AsyncSession,
    household: Household,
    subject: Subject,
) -> LearningMap:
    lm = LearningMap(
        household_id=household.id,
        subject_id=subject.id,
        name="Elementary Math",
    )
    db_session.add(lm)
    await db_session.flush()
    return lm


# ══════════════════════════════════════════════════════════════════════
# Per-child access fixtures (METHEAN-6-05)
# ══════════════════════════════════════════════════════════════════════


@pytest_asyncio.fixture
async def co_parent_user(db_session: AsyncSession, household: Household) -> User:
    from app.models.enums import UserRole

    u = User(
        household_id=household.id,
        email="coparent@test.local",
        password_hash=hash_password("xxxxxxxx"),
        display_name="Co Parent",
        role=UserRole.co_parent,
    )
    db_session.add(u)
    await db_session.flush()
    return u


@pytest_asyncio.fixture
async def observer_user(db_session: AsyncSession, household: Household) -> User:
    from app.models.enums import UserRole

    u = User(
        household_id=household.id,
        email="observer@test.local",
        password_hash=hash_password("xxxxxxxx"),
        display_name="Observer",
        role=UserRole.observer,
    )
    db_session.add(u)
    await db_session.flush()
    return u


@pytest_asyncio.fixture
async def second_child(db_session: AsyncSession, household: Household) -> Child:
    from datetime import date

    c = Child(
        household_id=household.id,
        first_name="Second",
        last_name="Child",
        date_of_birth=date(2015, 1, 1),
    )
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def self_learner_user(db_session: AsyncSession, household: Household, child: Child) -> User:
    from app.models.enums import UserRole

    u = User(
        household_id=household.id,
        email="learner@test.local",
        password_hash=hash_password("xxxxxxxx"),
        display_name="Self Learner",
        role=UserRole.co_parent,
        is_self_learner=True,
        linked_child_id=child.id,
    )
    db_session.add(u)
    await db_session.flush()
    return u


def _client_with_token(client: AsyncClient, user: User, household: Household, role: str) -> AsyncClient:
    token = create_access_token(user.id, household.id, role)
    client.cookies.set("access_token", token)
    return client


@pytest_asyncio.fixture
async def co_parent_client(
    client: AsyncClient,
    co_parent_user: User,
    household: Household,
) -> AsyncClient:
    return _client_with_token(client, co_parent_user, household, "co_parent")


@pytest_asyncio.fixture
async def observer_client(
    client: AsyncClient,
    observer_user: User,
    household: Household,
) -> AsyncClient:
    return _client_with_token(client, observer_user, household, "observer")


@pytest_asyncio.fixture
async def self_learner_client(
    client: AsyncClient,
    self_learner_user: User,
    household: Household,
) -> AsyncClient:
    return _client_with_token(client, self_learner_user, household, "co_parent")
