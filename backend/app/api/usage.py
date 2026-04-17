"""Usage tracking API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.cost_controls import check_budget as check_ai_budget
from app.ai.cost_controls import get_daily_usage
from app.api.deps import get_current_user, get_db
from app.models.identity import User
from app.models.operational import AIRun
from app.services.usage import check_budget, get_usage_breakdown

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("/current")
async def current_usage(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get current billing period usage status."""
    return await check_budget(db, user.household_id)


@router.get("/breakdown")
async def usage_breakdown(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get detailed usage breakdown by role and day."""
    return await get_usage_breakdown(db, user.household_id)


@router.get("/ai-daily")
async def ai_daily_usage(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get today's AI token and cost usage with budget status."""
    budget = await check_ai_budget(db, user.household_id)

    # Per-role breakdown for today
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    role_result = await db.execute(
        select(
            AIRun.run_type,
            func.sum(AIRun.input_tokens).label("input"),
            func.sum(AIRun.output_tokens).label("output"),
            func.count().label("calls"),
        )
        .where(
            AIRun.household_id == user.household_id,
            AIRun.started_at >= today_start,
        )
        .group_by(AIRun.run_type)
    )
    by_role = {
        row.run_type: {
            "input_tokens": row.input or 0,
            "output_tokens": row.output or 0,
            "calls": row.calls or 0,
        }
        for row in role_result.all()
    }

    return {
        **budget,
        "by_role": by_role,
    }
