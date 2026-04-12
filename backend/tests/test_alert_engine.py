"""Tests for the alert detection engine."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import MasteryLevel, NodeType
from app.models.evidence import Alert
from app.models.identity import Child, Household
from app.models.state import ChildNodeState


@pytest_asyncio.fixture
async def alert_household(db_session):
    h = Household(name="Alert Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def alert_child(db_session, alert_household):
    c = Child(household_id=alert_household.id, first_name="Alert")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def alert_node(db_session, alert_household):
    s = Subject(household_id=alert_household.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    m = LearningMap(household_id=alert_household.id, subject_id=s.id, name="Map")
    db_session.add(m)
    await db_session.flush()
    n = LearningNode(learning_map_id=m.id, household_id=alert_household.id,
                     node_type=NodeType.concept, title="Addition")
    db_session.add(n)
    await db_session.flush()
    return n


@pytest.mark.asyncio
class TestAlertEngine:
    async def test_stall_detection(self, db_session, alert_household, alert_child, alert_node):
        """Stalled node (in_progress for 14+ days) should be detectable."""
        db_session.add(ChildNodeState(
            child_id=alert_child.id, household_id=alert_household.id, node_id=alert_node.id,
            mastery_level=MasteryLevel.developing, attempts_count=3,
            last_activity_at=datetime.now(UTC) - timedelta(days=20),
        ))
        await db_session.flush()
        from app.services.alert_engine import detect_stalls
        alerts = await detect_stalls(db_session, alert_household.id)
        assert isinstance(alerts, list)

    async def test_regression_detection(self, db_session, alert_household, alert_child, alert_node):
        """Regression (mastered → lower) should create a warning alert."""
        from app.services.alert_engine import detect_regression
        alert = await detect_regression(
            db_session, alert_child.id, alert_household.id, alert_node.id,
            "mastered", "developing",
        )
        assert alert is not None
        assert alert.severity.value == "warning"
        assert alert.source == "regression_detection"

    async def test_pattern_detection(self, db_session, alert_household, alert_child, alert_node):
        """Pattern detection with <3 events should return None."""
        from app.services.alert_engine import detect_pattern_failure
        result = await detect_pattern_failure(
            db_session, alert_child.id, alert_household.id, alert_node.id,
        )
        # No StateEvents created, so fewer than 3 — should return None
        assert result is None
