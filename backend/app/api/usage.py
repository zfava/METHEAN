"""Usage tracking API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import User
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
