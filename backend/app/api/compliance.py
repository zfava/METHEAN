"""Compliance & Attendance API."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_child_access
from app.models.identity import Child, User
from app.services.attendance import get_attendance_record
from app.services.compliance_engine import (
    COMPLIANCE_DOMAINS,
    STATE_REQUIREMENTS,
    check_compliance,
    check_domain_compliance,
    get_hours_breakdown,
)

router = APIRouter(tags=["compliance"])


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


@router.get("/compliance/states")
async def list_states() -> list[dict]:
    """List all supported states with summary. Public endpoint — no auth required."""
    return [
        {
            "code": s["code"],
            "name": s["name"],
            "strictness": s.get("strictness", "unknown"),
            "notification_required": s.get("notification", {}).get("required", False),
            "annual_assessment_required": s.get("annual_assessment", {}).get("required", False),
        }
        for s in sorted(STATE_REQUIREMENTS.values(), key=lambda x: x["name"])
    ]


@router.get("/compliance/states/{code}")
async def get_state_detail(code: str, user: User = Depends(get_current_user)) -> dict:
    """Detailed requirements for a state."""
    reqs = STATE_REQUIREMENTS.get(code.upper())
    if not reqs:
        raise HTTPException(status_code=404, detail=f"State '{code}' not found")
    return reqs


@router.get("/children/{child_id}/compliance/check")
async def compliance_check(
    child_id: uuid.UUID,
    state: str = Query(description="State code, e.g. NY, TX, CA"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await check_compliance(db, user.household_id, child_id, state)


@router.get("/children/{child_id}/attendance")
async def get_attendance(
    child_id: uuid.UUID,
    start: date = Query(alias="start"),
    end: date = Query(alias="end"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await get_attendance_record(db, user.household_id, child_id, start, end)


@router.get("/children/{child_id}/hours")
async def get_hours(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await get_hours_breakdown(db, user.household_id, child_id)


@router.get("/compliance/domains")
async def list_compliance_domains() -> list[dict]:
    """List every configured compliance domain."""
    return [{"domain": name, **cfg} for name, cfg in COMPLIANCE_DOMAINS.items()]


@router.get("/compliance/domain/{domain}/check/{child_id}")
async def check_domain_compliance_api(
    domain: str,
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await check_domain_compliance(user.household_id, child_id, domain, db)
