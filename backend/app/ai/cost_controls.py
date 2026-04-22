"""Per-household AI cost controls and loop-depth guards.

Enforces daily token and cost budgets per household to keep unit
economics defensible at $99/month. Degrades to mock provider when
budget is exceeded rather than blocking (configurable).
"""

import logging
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operational import AIRun

logger = logging.getLogger(__name__)

# Per-model cost in USD per million tokens (input, output).
# Source: provider pricing pages as of 2026-04-17.
MODEL_COST_PER_MTOK: dict[str, dict[str, float]] = {
    # Historical sonnet model kept so old AIRun rows still cost-estimate cleanly
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-opus-4-6": {"input": 15.00, "output": 75.00},
    "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "mock": {"input": 0.00, "output": 0.00},
}

# Default daily limits (generous for 4 children, 2 parents, full use)
DEFAULT_DAILY_TOKEN_LIMIT = 200_000
DEFAULT_DAILY_COST_LIMIT_CENTS = 300  # $3.00/day = $90/month ceiling
DEFAULT_ALERT_THRESHOLD_PCT = 80
DEFAULT_HARD_LIMIT_BEHAVIOR = "degrade"  # "degrade" or "block"

# Tutor session loop guard
MAX_TUTOR_SESSION_CALLS = 50
TUTOR_WARN_THRESHOLDS = [20, 30, 40]


def estimate_cost_cents(model: str, input_tok: int, output_tok: int) -> int:
    """Estimate cost in integer cents for a single AI call."""
    rates = MODEL_COST_PER_MTOK.get(model, MODEL_COST_PER_MTOK.get("mock", {"input": 0, "output": 0}))
    cost_usd = (input_tok * rates["input"] / 1_000_000) + (output_tok * rates["output"] / 1_000_000)
    return round(cost_usd * 100)


async def get_daily_usage(
    db: AsyncSession,
    household_id,
    *,
    reference_time: datetime | None = None,
) -> dict:
    """Get today's cumulative AI usage for a household.

    Returns: {total_tokens: int, total_cost_cents: int, call_count: int}
    """
    now = reference_time or datetime.now(UTC)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    result = await db.execute(
        select(
            func.coalesce(func.sum(AIRun.input_tokens + AIRun.output_tokens), 0).label("tokens"),
            func.coalesce(func.sum(AIRun.input_tokens), 0).label("input_tokens"),
            func.coalesce(func.sum(AIRun.output_tokens), 0).label("output_tokens"),
            func.count().label("calls"),
        ).where(
            AIRun.household_id == household_id,
            AIRun.started_at >= today_start,
        )
    )
    row = result.one()

    # Compute cost from recorded tokens since cost_usd may be NULL on old records
    total_input = row.input_tokens or 0
    total_output = row.output_tokens or 0
    # Use sonnet pricing as default for aggregation (most calls use sonnet)
    est_cost = estimate_cost_cents("claude-sonnet-4-20250514", total_input, total_output)

    return {
        "total_tokens": row.tokens or 0,
        "total_cost_cents": est_cost,
        "call_count": row.calls or 0,
        "input_tokens": total_input,
        "output_tokens": total_output,
    }


async def check_budget(
    db: AsyncSession,
    household_id,
    *,
    daily_token_limit: int = DEFAULT_DAILY_TOKEN_LIMIT,
    daily_cost_limit_cents: int = DEFAULT_DAILY_COST_LIMIT_CENTS,
    alert_threshold_pct: int = DEFAULT_ALERT_THRESHOLD_PCT,
    hard_limit_behavior: str = DEFAULT_HARD_LIMIT_BEHAVIOR,
) -> dict:
    """Check if a household is within its daily AI budget.

    Returns:
        {
            "allowed": bool,
            "should_degrade": bool,  # True = use mock instead of real AI
            "should_alert": bool,
            "usage": {...},
            "budget": {...},
            "pct_tokens": int,
            "pct_cost": int,
        }
    """
    usage = await get_daily_usage(db, household_id)

    pct_tokens = int(usage["total_tokens"] / max(daily_token_limit, 1) * 100)
    pct_cost = int(usage["total_cost_cents"] / max(daily_cost_limit_cents, 1) * 100)
    pct_max = max(pct_tokens, pct_cost)

    should_alert = pct_max >= alert_threshold_pct
    over_limit = pct_tokens >= 100 or pct_cost >= 100

    if over_limit:
        if hard_limit_behavior == "block":
            return {
                "allowed": False,
                "should_degrade": False,
                "should_alert": True,
                "usage": usage,
                "budget": {
                    "daily_token_limit": daily_token_limit,
                    "daily_cost_limit_cents": daily_cost_limit_cents,
                },
                "pct_tokens": pct_tokens,
                "pct_cost": pct_cost,
            }
        else:
            # Degrade: allow the call but force mock provider
            return {
                "allowed": True,
                "should_degrade": True,
                "should_alert": True,
                "usage": usage,
                "budget": {
                    "daily_token_limit": daily_token_limit,
                    "daily_cost_limit_cents": daily_cost_limit_cents,
                },
                "pct_tokens": pct_tokens,
                "pct_cost": pct_cost,
            }

    return {
        "allowed": True,
        "should_degrade": False,
        "should_alert": should_alert,
        "usage": usage,
        "budget": {
            "daily_token_limit": daily_token_limit,
            "daily_cost_limit_cents": daily_cost_limit_cents,
        },
        "pct_tokens": pct_tokens,
        "pct_cost": pct_cost,
    }


class TutorSessionLimitError(Exception):
    """Raised when a tutor session exceeds the loop-depth guard."""

    pass


class DailyBudgetExceededError(Exception):
    """Raised when a household exceeds its daily AI budget in block mode."""

    pass


class TutorSessionCounter:
    """Per-session loop-depth counter for tutor conversations.

    Prevents runaway agent loops from consuming unlimited tokens.
    Warns at 20, 30, 40 calls; hard-stops at 50.
    """

    def __init__(self, max_calls: int = MAX_TUTOR_SESSION_CALLS):
        self.max_calls = max_calls
        self.call_count = 0

    def increment(self) -> int:
        """Increment and return the new count. Raises at max."""
        self.call_count += 1

        if self.call_count > self.max_calls:
            logger.warning(
                "tutor_session_limit_exceeded: call_count=%d max_calls=%d",
                self.call_count,
                self.max_calls,
            )
            raise TutorSessionLimitError(
                f"Tutor session exceeded {self.max_calls} AI calls. "
                f"This session has been paused to protect your account. "
                f"Start a new session to continue."
            )

        if self.call_count in TUTOR_WARN_THRESHOLDS:
            logger.info(
                "tutor_session_approaching_limit: call_count=%d max_calls=%d",
                self.call_count,
                self.max_calls,
            )

        return self.call_count

    def reset(self) -> None:
        """Reset for a new session."""
        self.call_count = 0
