"""Tests for the Evaluator Calibration Service (Session 10 + Session 11)."""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration import CalibrationProfile, CalibrationSnapshot, EvaluatorPrediction
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import NodeType
from app.models.evidence import Alert
from app.models.governance import Activity, Attempt, GovernanceEvent, Plan, PlanWeek
from app.models.identity import Child, Household
from app.services.calibration import (
    MAX_OFFSET_STEP,
    MIN_PREDICTIONS_FOR_CALIBRATION,
    apply_calibration_offset,
    clamp_offset_change,
    compute_confidence_distribution,
    compute_subject_calibration_detail,
    compute_temporal_drift,
    record_prediction,
    reconcile_outcome,
    recompute_profile,
    run_calibration_health_check,
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
    db_session: AsyncSession,
    cal_household: Household,
    cal_child: Child,
    cal_node: LearningNode,
) -> Attempt:
    plan = Plan(household_id=cal_household.id, child_id=cal_child.id, name="Cal Plan")
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=cal_household.id,
        week_number=1,
        start_date=date(2026, 1, 5),
        end_date=date(2026, 1, 11),
    )
    db_session.add(week)
    await db_session.flush()

    act = Activity(
        plan_week_id=week.id,
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


async def _create_predictions(
    db_session, cal_household, cal_child, cal_node, cal_attempt, count, predicted_rating, actual_rating, conf=None
):
    """Helper: create N reconciled predictions."""
    for i in range(count):
        att = Attempt(
            activity_id=cal_attempt.activity_id,
            household_id=cal_household.id,
            child_id=cal_child.id,
        )
        db_session.add(att)
        await db_session.flush()

        if conf is None:
            c = (
                0.85
                if predicted_rating == 4
                else 0.65
                if predicted_rating == 3
                else 0.4
                if predicted_rating == 2
                else 0.15
            )
        else:
            c = conf
        pred = EvaluatorPrediction(
            household_id=cal_household.id,
            child_id=cal_child.id,
            node_id=cal_node.id,
            attempt_id=att.id,
            predicted_confidence=c,
            predicted_fsrs_rating=predicted_rating,
            actual_outcome=actual_rating,
            drift_score=abs(predicted_rating - actual_rating),
            outcome_recorded_at=datetime.now(UTC),
        )
        db_session.add(pred)
    await db_session.flush()


# ═══════════════════════════════════════════
# SESSION 10 TESTS (original)
# ═══════════════════════════════════════════


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


@pytest.mark.asyncio
class TestReconcileOutcome:
    async def test_reconciles_matching_prediction(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await record_prediction(db_session, cal_child.id, cal_household.id, cal_node.id, cal_attempt.id, 0.75, 3)
        result = await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 3)
        assert result is not None
        assert result.actual_outcome == 3
        assert result.drift_score == 0.0
        assert result.outcome_recorded_at is not None

    async def test_no_match_returns_none(self, db_session, cal_child, cal_household, cal_node):
        result = await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 3)
        assert result is None

    async def test_drift_calculation(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await record_prediction(db_session, cal_child.id, cal_household.id, cal_node.id, cal_attempt.id, 0.85, 4)
        result = await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 2)
        assert result is not None
        assert result.drift_score == 2.0

    async def test_high_drift_creates_warning_alert(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await record_prediction(db_session, cal_child.id, cal_household.id, cal_node.id, cal_attempt.id, 0.85, 4)
        await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 2)
        alerts = (await db_session.execute(select(Alert).where(Alert.source == "calibration_drift"))).scalars().all()
        assert len(alerts) == 1
        assert alerts[0].severity.value == "warning"

    async def test_extreme_drift_creates_critical_alert(
        self, db_session, cal_child, cal_household, cal_node, cal_attempt
    ):
        await record_prediction(db_session, cal_child.id, cal_household.id, cal_node.id, cal_attempt.id, 0.85, 4)
        await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 1)
        alerts = (await db_session.execute(select(Alert).where(Alert.source == "calibration_drift"))).scalars().all()
        assert len(alerts) == 1
        assert alerts[0].severity.value == "action_required"

    async def test_concurrent_reconciliation_only_first_succeeds(
        self, db_session, cal_child, cal_household, cal_node, cal_attempt
    ):
        """Two reconcile calls for same prediction: only the first should match."""
        await record_prediction(db_session, cal_child.id, cal_household.id, cal_node.id, cal_attempt.id, 0.7, 3)
        r1 = await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 3)
        r2 = await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 2)
        assert r1 is not None
        assert r2 is None  # Already reconciled


@pytest.mark.asyncio
class TestApplyCalibrationOffset:
    async def test_no_profile_returns_raw(self, db_session, cal_child):
        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert result == 0.65

    async def test_active_offset(self, db_session, cal_child, cal_household):
        db_session.add(
            CalibrationProfile(
                child_id=cal_child.id, household_id=cal_household.id, recalibration_offset=-0.10, offset_active=True
            )
        )
        await db_session.flush()
        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert abs(result - 0.55) < 0.001

    async def test_inactive_offset_returns_raw(self, db_session, cal_child, cal_household):
        db_session.add(
            CalibrationProfile(
                child_id=cal_child.id, household_id=cal_household.id, recalibration_offset=-0.10, offset_active=False
            )
        )
        await db_session.flush()
        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert result == 0.65

    async def test_parent_override_takes_precedence(self, db_session, cal_child, cal_household):
        db_session.add(
            CalibrationProfile(
                child_id=cal_child.id,
                household_id=cal_household.id,
                recalibration_offset=-0.10,
                parent_override_offset=0.05,
                offset_active=True,
            )
        )
        await db_session.flush()
        result = await apply_calibration_offset(db_session, 0.65, cal_child.id)
        assert abs(result - 0.70) < 0.001

    async def test_clamping_to_upper_bound(self, db_session, cal_child, cal_household):
        db_session.add(
            CalibrationProfile(
                child_id=cal_child.id, household_id=cal_household.id, recalibration_offset=0.15, offset_active=True
            )
        )
        await db_session.flush()
        result = await apply_calibration_offset(db_session, 0.95, cal_child.id)
        assert result == 1.0

    async def test_clamping_to_lower_bound(self, db_session, cal_child, cal_household):
        db_session.add(
            CalibrationProfile(
                child_id=cal_child.id, household_id=cal_household.id, recalibration_offset=-0.15, offset_active=True
            )
        )
        await db_session.flush()
        result = await apply_calibration_offset(db_session, 0.05, cal_child.id)
        assert result == 0.0


@pytest.mark.asyncio
class TestRecomputeProfile:
    async def test_below_threshold_all_zeros(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 10, 3, 3)
        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert profile.mean_drift == 0.0
        assert profile.directional_bias == 0.0
        assert profile.recalibration_offset == 0.0
        assert profile.reconciled_predictions == 10

    async def test_positive_bias_negative_offset(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 4, 2)
        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert profile.directional_bias > 0
        assert profile.recalibration_offset < 0
        assert profile.recalibration_offset >= -0.15

    async def test_negative_bias_positive_offset(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 1, 3)
        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert profile.directional_bias < 0
        assert profile.recalibration_offset > 0
        assert profile.recalibration_offset <= 0.15

    async def test_offset_clamping(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 4, 1)
        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        assert -0.15 <= profile.recalibration_offset <= 0.15


# ═══════════════════════════════════════════
# SESSION 11A TESTS: Regression Safeguards
# ═══════════════════════════════════════════


class TestClampOffsetChange:
    """Unit tests for the rate limiter function."""

    def test_small_change_passes_through(self):
        assert clamp_offset_change(0.0, 0.03) == 0.03

    def test_large_positive_jump_clamped(self):
        assert abs(clamp_offset_change(0.0, 0.15) - 0.05) < 0.001

    def test_large_negative_jump_clamped(self):
        assert abs(clamp_offset_change(0.0, -0.15) - (-0.05)) < 0.001

    def test_preserves_positive_direction(self):
        result = clamp_offset_change(0.02, 0.12)
        assert result > 0.02

    def test_preserves_negative_direction(self):
        result = clamp_offset_change(-0.02, -0.12)
        assert result < -0.02

    def test_three_step_convergence(self):
        """0.0 → 0.15 converges in 3 nightly runs."""
        current = 0.0
        current = clamp_offset_change(current, 0.15)
        assert abs(current - 0.05) < 0.001
        current = clamp_offset_change(current, 0.15)
        assert abs(current - 0.10) < 0.001
        current = clamp_offset_change(current, 0.15)
        assert abs(current - 0.15) < 0.001

    def test_exact_step_passes_through(self):
        assert clamp_offset_change(0.0, 0.05) == 0.05


@pytest.mark.asyncio
class TestCalibrationSnapshot:
    async def test_snapshot_created_on_recompute(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Each recompute_profile call creates exactly one snapshot."""
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 3, 3)
        await recompute_profile(db_session, cal_child.id, cal_household.id)

        snaps = (
            (await db_session.execute(select(CalibrationSnapshot).where(CalibrationSnapshot.child_id == cal_child.id)))
            .scalars()
            .all()
        )
        assert len(snaps) == 1
        assert snaps[0].reconciled_count == 55

    async def test_snapshots_accumulate(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Multiple recompute calls accumulate snapshots."""
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 3, 3)
        await recompute_profile(db_session, cal_child.id, cal_household.id)
        await recompute_profile(db_session, cal_child.id, cal_household.id)
        await recompute_profile(db_session, cal_child.id, cal_household.id)

        snaps = (
            (await db_session.execute(select(CalibrationSnapshot).where(CalibrationSnapshot.child_id == cal_child.id)))
            .scalars()
            .all()
        )
        assert len(snaps) == 3


@pytest.mark.asyncio
class TestRateLimiterInRecompute:
    async def test_rate_limiter_activates_on_large_jump(
        self, db_session, cal_child, cal_household, cal_node, cal_attempt
    ):
        """First recompute from 0.0 should be clamped by rate limiter."""
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 4, 1)
        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        # Max step from 0.0 is 0.05
        assert abs(profile.recalibration_offset) <= MAX_OFFSET_STEP + 0.001


@pytest.mark.asyncio
class TestHealthCheck:
    async def test_no_profiles_no_alerts(self, db_session):
        result = await run_calibration_health_check(db_session)
        assert result["profiles_checked"] == 0
        assert result["alerts_created"] == 0

    async def test_well_calibrated_no_alerts(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 3, 3)
        await recompute_profile(db_session, cal_child.id, cal_household.id)

        result = await run_calibration_health_check(db_session)
        assert result["alerts_created"] == 0

    async def test_critical_drift_child_creates_alert(
        self, db_session, cal_child, cal_household, cal_node, cal_attempt
    ):
        """Child with drift > 2.0 and 100+ predictions triggers critical alert."""
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 110, 4, 1)
        profile = await recompute_profile(db_session, cal_child.id, cal_household.id)
        # Force the mean_drift high (recompute may rate-limit offset but drift is direct)
        assert profile.mean_drift > 2.0

        result = await run_calibration_health_check(db_session)
        assert result["alerts_created"] >= 1

        alerts = (
            (await db_session.execute(select(Alert).where(Alert.source == "calibration_health_check"))).scalars().all()
        )
        assert any(a.title == "Critical Calibration Drift" for a in alerts)


# ═══════════════════════════════════════════
# SESSION 11B TESTS: Advanced Analytics
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestTemporalDrift:
    async def test_insufficient_data(self, db_session, cal_child, cal_household):
        result = await compute_temporal_drift(db_session, cal_child.id, cal_household.id)
        assert result["trend"] == "insufficient_data"

    async def test_stable_pattern(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Consistent drift produces stable trend."""
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 3, 3)
        result = await compute_temporal_drift(db_session, cal_child.id, cal_household.id)
        assert result["trend"] in ("stable", "insufficient_data")

    async def test_returns_weekly_buckets(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 3, 2)
        result = await compute_temporal_drift(db_session, cal_child.id, cal_household.id)
        assert len(result["weekly_buckets"]) >= 1
        for bucket in result["weekly_buckets"]:
            assert "week" in bucket
            assert "mean_drift" in bucket
            assert "count" in bucket


@pytest.mark.asyncio
class TestConfidenceDistribution:
    async def test_insufficient_data(self, db_session, cal_child, cal_household):
        result = await compute_confidence_distribution(db_session, cal_child.id, cal_household.id)
        assert result["histogram"] == []
        assert result["compression_warning"] is False

    async def test_normal_distribution(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Varied confidence scores produce a distribution."""
        # Create predictions with varied confidence
        for i, conf in enumerate([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]):
            att = Attempt(activity_id=cal_attempt.activity_id, household_id=cal_household.id, child_id=cal_child.id)
            db_session.add(att)
            await db_session.flush()
            db_session.add(
                EvaluatorPrediction(
                    household_id=cal_household.id,
                    child_id=cal_child.id,
                    node_id=cal_node.id,
                    attempt_id=att.id,
                    predicted_confidence=conf,
                    predicted_fsrs_rating=3,
                )
            )
        await db_session.flush()

        result = await compute_confidence_distribution(db_session, cal_child.id, cal_household.id)
        assert len(result["histogram"]) == 10
        assert result["total"] == 10
        assert result["std_dev"] > 0.1
        assert result["compression_warning"] is False

    async def test_compression_warning(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        """Narrow confidence range triggers compression warning."""
        for i in range(20):
            att = Attempt(activity_id=cal_attempt.activity_id, household_id=cal_household.id, child_id=cal_child.id)
            db_session.add(att)
            await db_session.flush()
            db_session.add(
                EvaluatorPrediction(
                    household_id=cal_household.id,
                    child_id=cal_child.id,
                    node_id=cal_node.id,
                    attempt_id=att.id,
                    predicted_confidence=0.70 + (i * 0.002),  # Very narrow range
                    predicted_fsrs_rating=3,
                )
            )
        await db_session.flush()

        result = await compute_confidence_distribution(db_session, cal_child.id, cal_household.id)
        assert result["compression_warning"] is True
        assert result["std_dev"] < 0.1


@pytest.mark.asyncio
class TestSubjectCalibrationDetail:
    async def test_empty_returns_empty(self, db_session, cal_child, cal_household):
        result = await compute_subject_calibration_detail(db_session, cal_child.id, cal_household.id)
        assert result == []

    async def test_well_calibrated_subject(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 15, 3, 3)
        result = await compute_subject_calibration_detail(db_session, cal_child.id, cal_household.id)
        assert len(result) >= 1
        assert result[0]["action"] == "well_calibrated"

    async def test_review_recommended(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 15, 4, 1)
        result = await compute_subject_calibration_detail(db_session, cal_child.id, cal_household.id)
        assert len(result) >= 1
        found = [s for s in result if s["action"] == "review_recommended"]
        assert len(found) >= 1

    async def test_insufficient_data_subject(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 5, 3, 3)
        result = await compute_subject_calibration_detail(db_session, cal_child.id, cal_household.id)
        assert len(result) >= 1
        assert result[0]["action"] == "insufficient_data"


# ═══════════════════════════════════════════
# SESSION 11D TESTS: Governance & Integration
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestGovernanceEvents:
    async def test_recompute_emits_governance_event(self, db_session, cal_child, cal_household, cal_node, cal_attempt):
        await _create_predictions(db_session, cal_household, cal_child, cal_node, cal_attempt, 55, 3, 3)
        await recompute_profile(db_session, cal_child.id, cal_household.id)

        events = (
            (
                await db_session.execute(
                    select(GovernanceEvent).where(GovernanceEvent.target_type == "calibration_profile")
                )
            )
            .scalars()
            .all()
        )
        assert len(events) >= 1
        assert "recomputed" in events[0].reason.lower()


@pytest.mark.asyncio
class TestDegradation:
    async def test_evaluator_works_without_profile(self, db_session, cal_child):
        """apply_calibration_offset works even when no profile exists."""
        result = await apply_calibration_offset(db_session, 0.72, cal_child.id)
        assert result == 0.72

    async def test_reconcile_works_without_predictions(self, db_session, cal_child, cal_household, cal_node):
        """reconcile_outcome gracefully handles no predictions."""
        result = await reconcile_outcome(db_session, cal_child.id, cal_household.id, cal_node.id, 3)
        assert result is None
