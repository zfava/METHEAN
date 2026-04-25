"""Activity Feedback and Reading Log API."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_child_access
from app.models.evidence import ActivityFeedback, ReadingLogEntry
from app.models.identity import Child, User

router = APIRouter(tags=["feedback-reading"])


# ── Helpers ───────────────────────────────────────


async def _get_child(db: AsyncSession, child_id: uuid.UUID, hid: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == hid))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(404, "Child not found")
    return child


# ══════════════════════════════════════════════════
# Activity Feedback
# ══════════════════════════════════════════════════


class FeedbackCreate(BaseModel):
    message: str
    feedback_type: str = "comment"
    child_id: uuid.UUID


@router.post("/activities/{activity_id}/feedback", status_code=201)
async def create_feedback(
    activity_id: uuid.UUID,
    body: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Leave a note for a child on a specific activity."""
    fb = ActivityFeedback(
        household_id=user.household_id,
        activity_id=activity_id,
        child_id=body.child_id,
        author_id=user.id,
        message=body.message,
        feedback_type=body.feedback_type,
    )
    db.add(fb)
    await db.commit()
    return {"id": str(fb.id), "message": fb.message, "feedback_type": fb.feedback_type}


@router.get("/activities/{activity_id}/feedback")
async def list_feedback(
    activity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List feedback on an activity."""
    result = await db.execute(
        select(ActivityFeedback)
        .where(ActivityFeedback.activity_id == activity_id, ActivityFeedback.household_id == user.household_id)
        .order_by(ActivityFeedback.created_at)
    )
    return [
        {
            "id": str(f.id),
            "message": f.message,
            "feedback_type": f.feedback_type,
            "author_id": str(f.author_id) if f.author_id else None,
            "created_at": str(f.created_at),
        }
        for f in result.scalars().all()
    ]


@router.get("/children/{child_id}/feedback/recent")
async def recent_feedback(
    child_id: uuid.UUID,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """Recent feedback across all activities for a child."""
    await _get_child(db, child_id, user.household_id)
    result = await db.execute(
        select(ActivityFeedback)
        .where(ActivityFeedback.child_id == child_id, ActivityFeedback.household_id == user.household_id)
        .order_by(ActivityFeedback.created_at.desc())
        .limit(limit)
    )
    return [
        {
            "id": str(f.id),
            "activity_id": str(f.activity_id),
            "message": f.message,
            "feedback_type": f.feedback_type,
            "created_at": str(f.created_at),
        }
        for f in result.scalars().all()
    ]


# ══════════════════════════════════════════════════
# Reading Log
# ══════════════════════════════════════════════════


class ReadingLogCreate(BaseModel):
    book_title: str
    book_author: str | None = None
    genre: str | None = None
    subject_area: str | None = None
    status: str = "reading"
    pages_total: int | None = None
    pages_read: int | None = None
    started_date: date | None = None
    narration: str | None = None
    parent_notes: str | None = None
    child_rating: int | None = Field(None, ge=1, le=5)
    minutes_spent: int | None = None


class ReadingLogUpdate(BaseModel):
    book_title: str | None = None
    book_author: str | None = None
    status: str | None = None
    pages_read: int | None = None
    pages_total: int | None = None
    narration: str | None = None
    parent_notes: str | None = None
    child_rating: int | None = Field(None, ge=1, le=5)
    minutes_spent: int | None = None
    completed_date: date | None = None


@router.post("/children/{child_id}/reading-log", status_code=201)
async def create_reading_entry(
    child_id: uuid.UUID,
    body: ReadingLogCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
):
    """Add a book to the reading log."""
    await _get_child(db, child_id, user.household_id)
    entry = ReadingLogEntry(
        household_id=user.household_id,
        child_id=child_id,
        created_by=user.id,
        book_title=body.book_title,
        book_author=body.book_author,
        genre=body.genre,
        subject_area=body.subject_area,
        status=body.status,
        pages_total=body.pages_total,
        pages_read=body.pages_read,
        started_date=body.started_date or (date.today() if body.status == "reading" else None),
        narration=body.narration,
        parent_notes=body.parent_notes,
        child_rating=body.child_rating,
        minutes_spent=body.minutes_spent,
    )
    db.add(entry)
    await db.commit()
    return _entry_dict(entry)


@router.get("/children/{child_id}/reading-log")
async def list_reading_log(
    child_id: uuid.UUID,
    status: str | None = None,
    subject_area: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """List reading log entries, filterable by status and subject."""
    await _get_child(db, child_id, user.household_id)
    query = select(ReadingLogEntry).where(
        ReadingLogEntry.child_id == child_id,
        ReadingLogEntry.household_id == user.household_id,
    )
    if status:
        query = query.where(ReadingLogEntry.status == status)
    if subject_area:
        query = query.where(ReadingLogEntry.subject_area == subject_area)
    query = query.order_by(ReadingLogEntry.updated_at.desc()).limit(limit)
    result = await db.execute(query)
    return [_entry_dict(e) for e in result.scalars().all()]


@router.put("/reading-log/{entry_id}")
async def update_reading_entry(
    entry_id: uuid.UUID,
    body: ReadingLogUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update a reading log entry."""
    result = await db.execute(
        select(ReadingLogEntry).where(
            ReadingLogEntry.id == entry_id,
            ReadingLogEntry.household_id == user.household_id,
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(404, "Entry not found")

    for field in [
        "book_title",
        "book_author",
        "status",
        "pages_read",
        "pages_total",
        "narration",
        "parent_notes",
        "child_rating",
        "minutes_spent",
        "completed_date",
    ]:
        val = getattr(body, field, None)
        if val is not None:
            setattr(entry, field, val)

    # Auto-set completed_date
    if body.status == "completed" and not entry.completed_date:
        entry.completed_date = date.today()

    await db.commit()
    return _entry_dict(entry)


@router.get("/children/{child_id}/reading-log/stats")
async def reading_stats(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """Reading statistics for a child."""
    await _get_child(db, child_id, user.household_id)
    result = await db.execute(
        select(ReadingLogEntry).where(
            ReadingLogEntry.child_id == child_id,
            ReadingLogEntry.household_id == user.household_id,
        )
    )
    entries = result.scalars().all()

    total = len(entries)
    completed = sum(1 for e in entries if e.status == "completed")
    pages = sum(e.pages_read or 0 for e in entries)
    minutes = sum(e.minutes_spent or 0 for e in entries)

    by_genre: dict[str, int] = {}
    by_subject: dict[str, int] = {}
    for e in entries:
        if e.genre:
            by_genre[e.genre] = by_genre.get(e.genre, 0) + 1
        if e.subject_area:
            by_subject[e.subject_area] = by_subject.get(e.subject_area, 0) + 1

    return {
        "total_books": total,
        "books_completed": completed,
        "pages_read_total": pages,
        "minutes_total": minutes,
        "by_genre": by_genre,
        "by_subject": by_subject,
    }


@router.get("/children/{child_id}/reading-log/current")
async def current_reading(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """Books currently being read."""
    await _get_child(db, child_id, user.household_id)
    result = await db.execute(
        select(ReadingLogEntry)
        .where(
            ReadingLogEntry.child_id == child_id,
            ReadingLogEntry.household_id == user.household_id,
            ReadingLogEntry.status == "reading",
        )
        .order_by(ReadingLogEntry.updated_at.desc())
    )
    return [_entry_dict(e) for e in result.scalars().all()]


def _entry_dict(e: ReadingLogEntry) -> dict:
    return {
        "id": str(e.id),
        "book_title": e.book_title,
        "book_author": e.book_author,
        "genre": e.genre,
        "subject_area": e.subject_area,
        "status": e.status,
        "pages_total": e.pages_total,
        "pages_read": e.pages_read,
        "started_date": str(e.started_date) if e.started_date else None,
        "completed_date": str(e.completed_date) if e.completed_date else None,
        "minutes_spent": e.minutes_spent,
        "narration": e.narration,
        "parent_notes": e.parent_notes,
        "child_rating": e.child_rating,
        "created_at": str(e.created_at) if e.created_at else None,
    }
