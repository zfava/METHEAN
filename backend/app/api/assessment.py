"""Assessment & Portfolio API."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import PaginationParams, get_current_user, get_db
from app.models.assessment import Assessment, PortfolioEntry
from app.models.enums import AssessmentType
from app.models.identity import Child, User
from app.services.assessment_engine import (
    generate_portfolio_export,
    generate_transcript,
    record_assessment,
)

router = APIRouter(tags=["assessment"])


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


class AssessmentCreate(BaseModel):
    node_id: uuid.UUID | None = None
    # Pydantic rejects values outside the enum with 422 automatically.
    assessment_type: AssessmentType
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    qualitative_notes: str | None = None
    rubric_scores: dict | None = None
    mastery_judgment: str | None = None
    confidence_override: float | None = Field(default=None, ge=0.0, le=1.0)
    artifact_ids: list[str] | None = None
    subject: str | None = None


class PortfolioCreate(BaseModel):
    node_id: uuid.UUID | None = None
    assessment_id: uuid.UUID | None = None
    entry_type: str = Field(min_length=1, max_length=50)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    content: dict | None = None
    subject: str | None = None
    date_completed: date | None = None
    parent_notes: str | None = None
    tags: list[str] | None = None


# ── Assessments ──


@router.post("/children/{child_id}/assessments", status_code=201)
async def create_assessment(
    child_id: uuid.UUID,
    body: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    assessment = await record_assessment(
        db,
        user.household_id,
        child_id,
        body.node_id,
        body.model_dump(),
        user.id,
    )
    return {
        "id": str(assessment.id),
        "assessment_type": assessment.assessment_type,
        "title": assessment.title,
        "mastery_judgment": assessment.mastery_judgment,
        "created_at": assessment.created_at.isoformat() if assessment.created_at else None,
    }


@router.get("/children/{child_id}/assessments")
async def list_assessments(
    child_id: uuid.UUID,
    assessment_type: str | None = Query(default=None),
    subject: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    base = select(Assessment).where(
        Assessment.child_id == child_id,
        Assessment.household_id == user.household_id,
    )
    if assessment_type:
        base = base.where(Assessment.assessment_type == assessment_type)
    if subject:
        base = base.where(Assessment.subject == subject)

    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(Assessment.assessed_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [
            {
                "id": str(a.id),
                "assessment_type": a.assessment_type,
                "title": a.title,
                "qualitative_notes": a.qualitative_notes,
                "mastery_judgment": a.mastery_judgment,
                "subject": a.subject,
                "assessed_at": a.assessed_at.isoformat() if a.assessed_at else None,
            }
            for a in result.scalars().all()
        ],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


# ── Portfolio ──


@router.post("/children/{child_id}/portfolio", status_code=201)
async def create_portfolio_entry(
    child_id: uuid.UUID,
    body: PortfolioCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    entry = PortfolioEntry(
        household_id=user.household_id,
        child_id=child_id,
        assessment_id=body.assessment_id,
        node_id=body.node_id,
        entry_type=body.entry_type,
        title=body.title,
        description=body.description,
        content=body.content or {},
        subject=body.subject,
        date_completed=body.date_completed,
        parent_notes=body.parent_notes,
        tags=body.tags or [],
    )
    db.add(entry)
    await db.flush()
    return {
        "id": str(entry.id),
        "entry_type": entry.entry_type,
        "title": entry.title,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
    }


@router.get("/children/{child_id}/portfolio")
async def list_portfolio(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    base = select(PortfolioEntry).where(
        PortfolioEntry.child_id == child_id,
        PortfolioEntry.household_id == user.household_id,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(PortfolioEntry.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [
            {
                "id": str(e.id),
                "entry_type": e.entry_type,
                "title": e.title,
                "subject": e.subject,
                "date_completed": e.date_completed.isoformat() if e.date_completed else None,
                "tags": e.tags,
            }
            for e in result.scalars().all()
        ],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


# ── Transcript & Export ──


@router.get("/children/{child_id}/transcript")
async def get_transcript(
    child_id: uuid.UUID,
    year: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await generate_transcript(db, user.household_id, child_id, year)


@router.get("/children/{child_id}/portfolio/export")
async def portfolio_export(
    child_id: uuid.UUID,
    period_start: date = Query(alias="from"),
    period_end: date = Query(alias="to"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await generate_portfolio_export(db, user.household_id, child_id, period_start, period_end)
