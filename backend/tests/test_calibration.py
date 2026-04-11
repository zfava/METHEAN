"""Tests for the Evaluator Calibration Service."""

import uuid
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration import CalibrationProfile, EvaluatorPrediction
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.evidence import Alert
from app.models.governance import Activity, Attempt
from app.models.identity import Child, Household
from app.services.calibration import (
    MIN_PREDICTIONS_FOR_CALIBRATION,
    apply_calibration_offset,
    record_prediction,
    reconcile_outcome,
    recompute_profile,
)


# ── Fixtures ──


@pytest_asyncio.fixture
async def cal_household(db_session: AsyncSession) -> Household:
    h = Household(name="Calibration Test Family")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def cal_child(db_session: AsyncSession, cal_household: Household) -> Child:
    c = Child(household_id=cal_household.id, first_name="Cal", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def cal_subject(db_session: AsyncSession, cal_household: Household) -> Subject:
    s = Subject(household_id=cal_household.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def cal_map(db_session: AsyncSession, cal_household: Household, cal_subject: Subject) -> LearningMap:
    m = LearningMap(household_id=cal_household.id, subject_id=cal_subject.id, name="Test Map")
    db_session.add(m)
    await db_session.flush()
    return m


@pytest_asyncio.fixture
async def cal_node(db_session: AsyncSession, cal_household: Household, cal_map: LearningMap) -> LearningNode:
    n = LearningNode(
        learning_map_id=cal_map.id,
        household_id=cal_household.id,
        node_type=NodeType.concept,
        title="Addition Facts",
    )
    db_session.add(n)
    await db_session.flush()
    return n


@pytest_asyncio.fixture
async def cal_attempt(
    db_session: AsyncSession, cal_household: Household, cal_child: Child, cal_node: LearningNode,
) -> Attempt:
    act = Activity(
        household_id=cal_household.id,
        title="Practice Addition",
        activity_type="practice",
        node_id=cal_node.id,
    )
    db_session.add(act)
    await db_session.flush()

    att = Attempt(
        activity_id=act.id,
        household_id=cal_household.id,
        child_id=cal_child.id,
    )
    db_session.add(att)
    await db_session.flush()
    return att


# ── record_prediction ──


@pytest.mark.asyncio
class TestRecordPrediction:
    async def test_creates_prediction(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        pred = await record_prediction(
            db_session,
            child_id=cal_child.id,
            household_id=cal_household.id,
            node_id=cal_node.id,
            attempt_id=cal_attempt.id,
            evaluator_confidence=0.75,
            fsrs_rating=3,
        )
        assert pred.id is not None
        assert pred.predicted_confidence == 0.75
        assert pred.predicted_fsrs_rating == 3
        assert pred.actual_outcome is None
        assert pred.calibration_offset_applied == 0.0

    async def test_records_offset_applied(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        pred = await record_prediction(
            db_session,
            child_id=cal_child.id,
            household_id=cal_household.id,
            node_id=cal_node.id,
            attempt_id=cal_attempt.id,
            evaluator_confidence=0.75,
            fsrs_rating=3,
            calibration_offset_applied=0.05,
        )
        assert pred.calibration_offset_applied == 0.05


# ── reconcile_outcome ──


@pytest.mark.asyncio
class TestReconcileOutcome:
    async def test_reconciles_matching_prediction(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        # Create a prediction
        await record_prediction(
            db_session, cal_child.id, cal_household.id,
            cal_node.id, cal_attempt.id, 0.75, 3,
        )

        # Reconcile with actual outcome
        result = await reconcile_outcome(
            db_session, cal_child.id, cal_household.id, cal_node.id, 3,
        )
        assert result is not None
        assert result.actual_outcome == 3
        assert result.drift_score == 0.0  # predicted 3, actual 3
        assert result.outcome_recorded_at is not None

    async def test_no_match_returns_none(self, db_session, cal_child, cal_household, cal_node):
        # No prediction exists — should return None gracefully
        result = await reconcile_outcome(
            db_session, cal_child.id, cal_household.id, cal_node.id, 3,
        )
        assert result is None

    async def test_drift_calculation(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await record_prediction(
            db_session, cal_child.id, cal_household.id,
            cal_node.id, cal_attempt.id, 0.85, 4,
        )
        result = await reconcile_outcome(
            db_session, cal_child.id, cal_household.id, cal_node.id, 2,
        )
        assert result is not None
        assert result.drift_score == 2.0  # abs(4 - 2)

    async def test_high_drift_creates_warning_alert(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await record_prediction(
            db_session, cal_child.id, cal_household.id,
            cal_node.id, cal_attempt.id, 0.85, 4,
        )
        await reconcile_outcome(
            db_session, cal_child.id, cal_household.id, cal_node.id, 2,
        )

        alerts = (await db_session.execute(
            select(Alert).where(Alert.source == "calibration_drift")
        )).scalars().all()
        assert len(alerts) == 1
        assert alerts[0].severity.value == "warning"

    async def test_extreme_drift_creates_critical_alert(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await record_prediction(
            db_session, cal_child.id, cal_household.id,
            cal_node.id, cal_attempt.id, 0.85, 4,
        )
        await reconcile_outcome(
            db_session, cal_child.id, cal_household.id, cal_node.id, 1,
        )

        alerts = (await db_session.execute(
            select(Alert).where(Alert.source == "calibration_drift")
        )).scalars().all()
        assert len(alerts) == 1
        assert alerts[0].severity.value == "action_required"


# ── apply_calibration_offset ──


@pytest.mark.asyncio
class TestApplyCalibrationOffset:
    async def test_no_profile_returns_raw(self, db_session, cal_child):
        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert result == 0.65

    async def test_active_offset(self, db_session, cal_child, cal_household):
        profile = CalibrationProfile(
            child_id=cal_child.id,
            household_id=cal_household.id,
            recalibration_offset=-0.10,
            offset_active=True,
        )
        db_session.add(profile)
        await db_session.flush()

        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert abs(result - 0.55) < 0.001

    async def test_inactive_offset_returns_raw(self, db_session, cal_child, cal_household):
        profile = CalibrationProfile(
            child_id=cal_child.id,
            household_id=cal_household.id,
            recalibration_offset=-0.10,
            offset_active=False,
        )
        db_session.add(profile)
        await db_session.flush()

        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert result == 0.65

    async def test_parent_override_takes_precedence(self, db_session, cal_child, cal_household):
        profile = CalibrationProfile(
            child_id=cal_child.id,
            household_id=cal_household.id,
            recalibration_offset=-0.10,
            parent_override_offset=0.05,
            offset_active=True,
        )
        db_session.add(profile)
        await db_session.flush()

        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert abs(result - 0.70) < 0.001

    async def test_clamping_to_bounds(self, db_session, cal_child, cal_household):
        # Test upper bound
        profile = CalibrationProfile(
            child_id=cal_child.id,
            household_id=cal_household.id,
            recalibration_offset=0.15,
            offset_active=True,
        )
        db_session.add(profile)
        await db_session.flush()

        result = await apply_calibration_offset(db_session, 0.95, cal_child.id)
        assert result == 1.0  # 0.95 + 0.15 = 1.10, clamped to 1.0

    async def test_clamping_lower_bound(self, db_session, cal_child, cal_household):
        profile = CalibrationProfile(
            child_id=cal_child.id,
            household_id=cal_household.id,
            recalibration_offset=-0.15,
            offset_active=True,
        )
        db_session.add(profile)
        await db_session.flush()

        result = await apply_calibration_offset(db_session, 0.05, cal_child.id)
        assert result == 0.0  # 0.05 - 0.15 = -0.10, clamped to 0.0


# ── recompute_profile ──


@pytest.mark.asyncio
class TestRecomputeProfile:
    async def test_below_threshold_all_zeros(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        # Create < 50 reconciled predictions
        for i in range(10):
            att = Attempt(
                activity_id=cal_attempt.activity_id,
                household_id=cal_household.id,
                child_id=cal_child.id,
            )
            db_session.add(att)
            await db_session.flush()

            pred = EvaluatorPrediction(
                household_id=cal_household.id, child_id=cal_child.id,
                node_id=cal_node.id, attempt_id=att.id,
                predicted_confidence=0.7, predicted_fsrs_rating=3,
                actual_outcome=3, drift_score=0.0,
                outcome_recorded_at=datetime.now(UTC),
            )
            db_session.add(pred)
        await db_session.flush()

        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert profile.mean_drift == 0.0
        assert profile.directional_bias == 0.0
        assert profile.recalibration_offset == 0.0
        assert profile.reconciled_predictions == 10

    async def _create_predictions(self, db_session, cal_household, cal_child, cal_node, cal_attempt,
                                   count, predicted_rating, actual_rating):
        """Helper: create N reconciled predictions."""
        for i in range(count):
            att = Attempt(
                activity_id=cal_attempt.activity_id,
                household_id=cal_household.id,
                child_id=cal_child.id,
            )
            db_session.add(att)
            await db_session.flush()

            conf = 0.85 if predicted_rating == 4 else 0.65 if predicted_rating == 3 else 0.4
            pred = EvaluatorPrediction(
                household_id=cal_household.id, child_id=cal_child.id,
                node_id=cal_node.id, attempt_id=att.id,
                predicted_confidence=conf, predicted_fsrs_rating=predicted_rating,
                actual_outcome=actual_rating,
                drift_score=abs(predicted_rating - actual_rating),
                outcome_recorded_at=datetime.now(UTC),
            )
            db_session.add(pred)
        await db_session.flush()

    async def test_positive_bias_negative_offset(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Evaluator too generous (predicts higher than actual) → negative offset."""
        await self._create_predictions(
            db_session, cal_household, cal_child, cal_node, cal_attempt,
            count=55, predicted_rating=4, actual_rating=2,
        )

        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert profile.directional_bias > 0  # positive = too generous
        assert profile.recalibration_offset < 0  # negative to correct
        assert profile.recalibration_offset >= -0.15

    async def test_negative_bias_positive_offset(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Evaluator too harsh (predicts lower than actual) → positive offset."""
        await self._create_predictions(
            db_session, cal_household, cal_child, cal_node, cal_attempt,
            count=55, predicted_rating=1, actual_rating=3,
        )

        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert profile.directional_bias < 0  # negative = too harsh
        assert profile.recalibration_offset > 0  # positive to correct
        assert profile.recalibration_offset <= 0.15

    async def test_offset_clamping(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Extreme bias still clamped to [-0.15, 0.15]."""
        await self._create_predictions(
            db_session, cal_household, cal_child, cal_node, cal_attempt,
            count=55, predicted_rating=4, actual_rating=1,
        )

        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert -0.15 <= profile.recalibration_offset <= 0.15
