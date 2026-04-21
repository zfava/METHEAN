"""Tests for AI cost controls: per-household budgeting and loop-depth guards."""

from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.cost_controls import (
    TutorSessionCounter,
    TutorSessionLimitError,
    check_budget,
    estimate_cost_cents,
    get_daily_usage,
)
from app.core.database import set_tenant
from app.models.identity import Household

# ---------------------------------------------------------------------------
# Cost estimation tests (pure functions, no DB)
# ---------------------------------------------------------------------------


class TestEstimateCostCents:
    def test_sonnet_cost(self):
        """Sonnet: 1M input tokens = $3.00, 1M output = $15.00."""
        cost = estimate_cost_cents("claude-sonnet-4-20250514", 1_000_000, 1_000_000)
        assert cost == 1800  # $3 + $15 = $18.00 = 1800 cents

    def test_opus_cost(self):
        """Opus: 1M input = $15, 1M output = $75."""
        cost = estimate_cost_cents("claude-opus-4-7", 1_000_000, 1_000_000)
        assert cost == 9000  # $15 + $75 = $90 = 9000 cents

    def test_mock_cost_is_zero(self):
        """Mock provider costs nothing."""
        cost = estimate_cost_cents("mock", 100_000, 100_000)
        assert cost == 0

    def test_small_call_cost(self):
        """Typical tutor call: ~500 input, ~1000 output on sonnet."""
        cost = estimate_cost_cents("claude-sonnet-4-20250514", 500, 1000)
        # $0.0015 + $0.015 = $0.0165 = ~2 cents
        assert cost <= 2  # rounding

    def test_unknown_model_defaults_to_zero(self):
        """Unknown model names default to mock (zero cost)."""
        cost = estimate_cost_cents("unknown-model-xyz", 100_000, 100_000)
        assert cost == 0

    def test_integer_output(self):
        """Cost is always an integer (cents, not float)."""
        cost = estimate_cost_cents("claude-sonnet-4-20250514", 12345, 67890)
        assert isinstance(cost, int)


# ---------------------------------------------------------------------------
# Tutor session loop guard tests
# ---------------------------------------------------------------------------


class TestTutorSessionCounter:
    def test_increment_within_limit(self):
        """Calls within the limit succeed."""
        counter = TutorSessionCounter(max_calls=50)
        for i in range(50):
            count = counter.increment()
        assert count == 50

    def test_increment_exceeds_limit_raises(self):
        """Call 51 raises TutorSessionLimitError."""
        counter = TutorSessionCounter(max_calls=50)
        for i in range(50):
            counter.increment()
        with pytest.raises(TutorSessionLimitError):
            counter.increment()

    def test_reset_clears_count(self):
        """Reset allows a new session to start from 0."""
        counter = TutorSessionCounter(max_calls=5)
        for i in range(5):
            counter.increment()
        counter.reset()
        # Should not raise now
        count = counter.increment()
        assert count == 1

    def test_small_limit(self):
        """Custom limit is respected."""
        counter = TutorSessionCounter(max_calls=3)
        counter.increment()
        counter.increment()
        counter.increment()
        with pytest.raises(TutorSessionLimitError):
            counter.increment()

    def test_exception_message_includes_limit(self):
        """Exception message tells the user what happened."""
        counter = TutorSessionCounter(max_calls=2)
        counter.increment()
        counter.increment()
        with pytest.raises(TutorSessionLimitError, match="exceeded 2 AI calls"):
            counter.increment()

    def test_previous_session_does_not_affect_new(self):
        """Resetting between sessions isolates limits."""
        counter = TutorSessionCounter(max_calls=5)
        for i in range(5):
            counter.increment()
        counter.reset()
        # Full new session should work
        for i in range(5):
            counter.increment()
        with pytest.raises(TutorSessionLimitError):
            counter.increment()


# ---------------------------------------------------------------------------
# Budget check tests (need DB)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def budget_hh(db_session: AsyncSession) -> Household:
    h = Household(name="Budget Test Family", timezone="America/New_York")
    db_session.add(h)
    await db_session.flush()
    await set_tenant(db_session, h.id)
    return h


@pytest.mark.asyncio
class TestDailyUsage:
    async def test_empty_usage(self, db_session, budget_hh):
        """No AI calls today: usage is zero."""
        usage = await get_daily_usage(db_session, budget_hh.id)
        assert usage["total_tokens"] == 0
        assert usage["total_cost_cents"] == 0
        assert usage["call_count"] == 0

    async def test_usage_aggregates_calls(self, db_session, budget_hh):
        """Usage sums across multiple AI runs."""
        from app.models.enums import AIRunStatus
        from app.models.operational import AIRun

        for i in range(3):
            run = AIRun(
                household_id=budget_hh.id,
                run_type="tutor",
                status=AIRunStatus.completed,
                input_tokens=100,
                output_tokens=200,
                started_at=datetime.now(UTC),
            )
            db_session.add(run)
        await db_session.flush()

        usage = await get_daily_usage(db_session, budget_hh.id)
        assert usage["total_tokens"] == 900  # 3 * (100 + 200)
        assert usage["call_count"] == 3
        assert usage["input_tokens"] == 300
        assert usage["output_tokens"] == 600


@pytest.mark.asyncio
class TestCheckBudget:
    async def test_under_limit_allowed(self, db_session, budget_hh):
        """Household at 0% usage: call is allowed, no alert, no degrade."""
        result = await check_budget(db_session, budget_hh.id)
        assert result["allowed"] is True
        assert result["should_degrade"] is False
        assert result["should_alert"] is False
        assert result["pct_tokens"] == 0

    async def test_alert_at_threshold(self, db_session, budget_hh):
        """Household at 80%+ of token limit triggers alert."""
        from app.models.enums import AIRunStatus
        from app.models.operational import AIRun

        # Fill to 85% of default 200k token limit = 170k tokens
        run = AIRun(
            household_id=budget_hh.id,
            run_type="tutor",
            status=AIRunStatus.completed,
            input_tokens=85_000,
            output_tokens=85_000,
            started_at=datetime.now(UTC),
        )
        db_session.add(run)
        await db_session.flush()

        result = await check_budget(db_session, budget_hh.id)
        assert result["allowed"] is True
        assert result["should_alert"] is True
        assert result["should_degrade"] is False
        assert result["pct_tokens"] >= 80

    async def test_over_limit_degrades(self, db_session, budget_hh):
        """Default behavior: over limit degrades to mock."""
        from app.models.enums import AIRunStatus
        from app.models.operational import AIRun

        # Exceed 200k token limit
        run = AIRun(
            household_id=budget_hh.id,
            run_type="tutor",
            status=AIRunStatus.completed,
            input_tokens=110_000,
            output_tokens=110_000,
            started_at=datetime.now(UTC),
        )
        db_session.add(run)
        await db_session.flush()

        result = await check_budget(db_session, budget_hh.id)
        assert result["allowed"] is True  # degrade mode allows
        assert result["should_degrade"] is True
        assert result["should_alert"] is True
        assert result["pct_tokens"] >= 100

    async def test_over_limit_blocks_when_configured(self, db_session, budget_hh):
        """Block mode: over limit denies the call."""
        from app.models.enums import AIRunStatus
        from app.models.operational import AIRun

        run = AIRun(
            household_id=budget_hh.id,
            run_type="tutor",
            status=AIRunStatus.completed,
            input_tokens=110_000,
            output_tokens=110_000,
            started_at=datetime.now(UTC),
        )
        db_session.add(run)
        await db_session.flush()

        result = await check_budget(
            db_session,
            budget_hh.id,
            hard_limit_behavior="block",
        )
        assert result["allowed"] is False
        assert result["should_degrade"] is False

    async def test_custom_limits(self, db_session, budget_hh):
        """Custom token limit changes the threshold."""
        from app.models.enums import AIRunStatus
        from app.models.operational import AIRun

        run = AIRun(
            household_id=budget_hh.id,
            run_type="tutor",
            status=AIRunStatus.completed,
            input_tokens=5_000,
            output_tokens=5_000,
            started_at=datetime.now(UTC),
        )
        db_session.add(run)
        await db_session.flush()

        # With a tiny limit (10k tokens), 10k used = 100%
        result = await check_budget(
            db_session,
            budget_hh.id,
            daily_token_limit=10_000,
        )
        assert result["pct_tokens"] >= 100
        assert result["should_degrade"] is True

    async def test_budget_resets_daily(self, db_session, budget_hh):
        """Yesterday's usage does not count against today's budget."""
        from app.models.enums import AIRunStatus
        from app.models.operational import AIRun

        # Add a large run from yesterday
        yesterday = datetime.now(UTC) - timedelta(days=1)
        run = AIRun(
            household_id=budget_hh.id,
            run_type="tutor",
            status=AIRunStatus.completed,
            input_tokens=500_000,
            output_tokens=500_000,
            started_at=yesterday,
        )
        db_session.add(run)
        await db_session.flush()

        # Today's usage should be zero
        usage = await get_daily_usage(db_session, budget_hh.id)
        assert usage["total_tokens"] == 0

        result = await check_budget(db_session, budget_hh.id)
        assert result["allowed"] is True
        assert result["pct_tokens"] == 0
