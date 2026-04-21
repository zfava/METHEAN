"""Document generation API endpoints."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import Child, User
from app.services.document_generator import (
    generate_attendance_record,
    generate_ihip,
    generate_quarterly_report,
    generate_transcript,
)

router = APIRouter(tags=["documents"])


async def _child_or_404(db, child_id, household_id):
    r = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    c = r.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Child not found")
    return c


def _pdf_response(data: bytes, filename: str) -> Response:
    content_type = "application/pdf" if data[:4] == b"%PDF" else "text/plain"
    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/children/{child_id}/documents/ihip")
async def get_ihip(
    child_id: uuid.UUID,
    academic_year: str = Query(description="e.g. 2026-2027"),
    state: str = Query("NY"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await _child_or_404(db, child_id, user.household_id)
    pdf = await generate_ihip(db, user.household_id, child_id, state, academic_year)
    return _pdf_response(pdf, f"IHIP_{academic_year}_{state}.pdf")


@router.get("/children/{child_id}/documents/quarterly-report")
async def get_quarterly_report(
    child_id: uuid.UUID,
    quarter: int = Query(ge=1, le=4),
    academic_year: str = Query(description="e.g. 2026-2027"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await _child_or_404(db, child_id, user.household_id)
    pdf = await generate_quarterly_report(db, user.household_id, child_id, quarter, academic_year)
    return _pdf_response(pdf, f"Q{quarter}_Report_{academic_year}.pdf")


@router.get("/children/{child_id}/documents/attendance")
async def get_attendance(
    child_id: uuid.UUID,
    start: date = Query(description="Start date"),
    end: date = Query(description="End date"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await _child_or_404(db, child_id, user.household_id)
    pdf = await generate_attendance_record(db, user.household_id, child_id, start, end)
    return _pdf_response(pdf, f"Attendance_{start}_{end}.pdf")


@router.get("/children/{child_id}/documents/transcript")
async def get_transcript(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await _child_or_404(db, child_id, user.household_id)
    pdf = await generate_transcript(db, user.household_id, child_id)
    return _pdf_response(pdf, "Transcript.pdf")
