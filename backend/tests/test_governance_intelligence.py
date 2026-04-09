"""Tests for governance intelligence analysis."""

import uuid
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household, User
from app.models.governance import GovernanceEvent
from app.models.enums import GovernanceAction
from app.core.security import create_access_token, hash_password
from app.services.governance_intelligence import (
    analyze_governance_patterns,
    get_planning_adjustments,
)


@pytest_asyncio.fixture
async def gov_household(db_session: AsyncSession) -> Household:
    h = Household(name="Gov Intel Test Family")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def gov_user(db_session: AsyncSession, gov_household: Household) -> User:
    u = User(
        household_id=gov_household.id,
        email="govintel@test.com",
        password_hash=hash_password("testpass"),
        display_name="Gov User",
        role="owner",
    )
    db_session.add(u)
    await db_session.flush()
    return u


async def _create_events(db, household_id, user_id, action, count, difficulty=None, activity_type=None):
    for _ in range(count):
        evt = GovernanceEvent(
            household_id=household_id,
            user_id=user_id,
            action=action,
            target_type="activity",
            target_id=uuid.uuid4(),
            metadata_={"difficulty": difficulty, "activity_type": activity_type} if difficulty or activity_type else {},
        )
        db.add(evt)
    await db.flush()


@pytest.mark.asyncio
async def test_analyze_empty_history(db_session, gov_household):
    """Empty history returns insufficient data."""
    result = await analyze_governance_patterns(db_session, gov_household.id)
    assert result["sufficient_data"] is False
    assert result["event_count"] == 0


@pytest.mark.asyncio
async def test_analyze_approval_rates_by_difficulty(db_session, gov_household, gov_user):
    """Approval rates computed correctly per difficulty."""
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 10, difficulty=1)
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.reject, 5, difficulty=4)
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 3, difficulty=4)

    result = await analyze_governance_patterns(db_session, gov_household.id)
    assert result["sufficient_data"] is True
    assert result["approval_rate_by_difficulty"][1] == 1.0
    assert result["approval_rate_by_difficulty"][4] < 0.5


@pytest.mark.asyncio
async def test_auto_approve_ceiling_computation(db_session, gov_household, gov_user):
    """Auto-approve ceiling is highest difficulty with 90%+ approval."""
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 10, difficulty=1)
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 10, difficulty=2)
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 10, difficulty=3)
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.reject, 8, difficulty=4)
    await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 2, difficulty=4)

    result = await analyze_governance_patterns(db_session, gov_household.id)
    assert result["auto_approve_ceiling"] == 3


@pytest.mark.asyncio
async def test_get_planning_adjustments_structure(db_session, gov_household, gov_user):
    """Planning adjustments have expected keys when sufficient data exists."""
    for d in range(1, 4):
        await _create_events(db_session, gov_household.id, gov_user.id, GovernanceAction.approve, 5, difficulty=d)

    adjustments = await get_planning_adjustments(db_session, gov_household.id)
    assert "max_difficulty" in adjustments
    assert "preferred_activity_types" in adjustments
    assert "avoided_activity_types" in adjustments


@pytest.mark.asyncio
async def test_get_planning_adjustments_empty(db_session, gov_household):
    """No data returns empty adjustments."""
    adjustments = await get_planning_adjustments(db_session, gov_household.id)
    assert adjustments == {}


@pytest.mark.asyncio
async def test_governance_intelligence_api_requires_auth(client):
    """GET /household/governance-intelligence requires auth."""
    resp = await client.get("/api/v1/household/governance-intelligence")
    assert resp.status_code == 401
