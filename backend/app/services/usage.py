"""AI usage tracking and budget enforcement.

Every AI call is metered. Families get 2M tokens/month (~$6 in Claude Sonnet).
"""

import uuid
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operational import UsageEvent, UsageLedger

# Cost per million tokens by model family
COST_TABLE = {
    "claude": {"input": 3.0, "output": 15.0},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "mock": {"input": 0.0, "output": 0.0},
}


def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost in USD for a given model and token count."""
    model_lower = (model or "mock").lower()
    for prefix, rates in COST_TABLE.items():
        if prefix in model_lower:
            return (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000
    return 0.0


def _current_period() -> tuple[date, date]:
    """Get current billing period (1st to last day of month)."""
    today = date.today()
    start = today.replace(day=1)
    if today.month == 12:
        end = date(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(today.year, today.month + 1, 1) - timedelta(days=1)
    return start, end


async def get_or_create_current_period(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> UsageLedger:
    """Get current billing period ledger. Create if doesn't exist."""
    start, end = _current_period()

    result = await db.execute(
        select(UsageLedger).where(
            UsageLedger.household_id == household_id,
            UsageLedger.period_start == start,
        )
    )
    ledger = result.scalar_one_or_none()
    if ledger:
        return ledger

    ledger = UsageLedger(
        household_id=household_id,
        period_start=start,
        period_end=end,
        token_budget=2_000_000,
    )
    db.add(ledger)
    await db.flush()
    return ledger


async def record_usage(
    db: AsyncSession,
    household_id: uuid.UUID,
    ai_run_id: uuid.UUID,
    input_tokens: int,
    output_tokens: int,
    model: str,
    role: str,
) -> None:
    """Record token consumption after every AI call."""
    ledger = await get_or_create_current_period(db, household_id)
    total = input_tokens + output_tokens

    ledger.tokens_consumed = (ledger.tokens_consumed or 0) + total
    ledger.ai_calls_count = (ledger.ai_calls_count or 0) + 1
    ledger.last_call_at = datetime.now(UTC)

    cost = _estimate_cost(model, input_tokens, output_tokens)

    event = UsageEvent(
        household_id=household_id,
        ai_run_id=ai_run_id,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total,
        model=model or "unknown",
        role=role or "unknown",
        cost_estimate_usd=cost,
    )
    db.add(event)
    await db.flush()


async def check_budget(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> dict:
    """Check remaining budget. Returns status dict."""
    ledger = await get_or_create_current_period(db, household_id)
    consumed = ledger.tokens_consumed or 0
    budget = ledger.token_budget or 2_000_000
    pct = consumed / max(budget, 1)

    return {
        "allowed": pct < 1.0,
        "remaining_tokens": max(0, budget - consumed),
        "pct_used": round(min(pct, 1.0), 3),
        "tokens_consumed": consumed,
        "token_budget": budget,
        "ai_calls": ledger.ai_calls_count or 0,
        "period_start": ledger.period_start.isoformat(),
        "period_end": ledger.period_end.isoformat(),
        "warning": "approaching_limit" if pct > 0.8 else None,
    }


async def get_usage_breakdown(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> dict:
    """Detailed usage breakdown by role and by day for current period."""
    start, end = _current_period()

    result = await db.execute(
        select(UsageEvent)
        .where(
            UsageEvent.household_id == household_id,
            UsageEvent.created_at >= datetime.combine(start, datetime.min.time()).replace(tzinfo=UTC),
        )
        .order_by(UsageEvent.created_at)
    )
    events = list(result.scalars().all())

    by_role: dict[str, dict] = defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0})
    by_day: dict[str, dict] = defaultdict(lambda: {"tokens": 0, "calls": 0})

    for evt in events:
        by_role[evt.role]["calls"] += 1
        by_role[evt.role]["tokens"] += evt.total_tokens
        by_role[evt.role]["cost"] += evt.cost_estimate_usd

        day_key = evt.created_at.strftime("%Y-%m-%d") if evt.created_at else "unknown"
        by_day[day_key]["tokens"] += evt.total_tokens
        by_day[day_key]["calls"] += 1

    total_cost = sum(r["cost"] for r in by_role.values())

    # Sort by_day
    sorted_days = sorted(by_day.items())[-14:]  # Last 14 days

    return {
        "by_role": {
            k: {"calls": v["calls"], "tokens": v["tokens"], "cost": round(v["cost"], 4)} for k, v in by_role.items()
        },
        "by_day": [{"date": d, "tokens": v["tokens"], "calls": v["calls"]} for d, v in sorted_days],
        "total_cost": round(total_cost, 4),
        "total_events": len(events),
    }


class UsageLimitExceeded(Exception):
    """Raised when monthly AI token budget is exhausted."""

    pass
