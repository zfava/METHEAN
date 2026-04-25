"""Fitness API: activity logs, benchmarks, and analytics."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_active_subscription, require_child_access
from app.models.fitness import FitnessBenchmark, FitnessLog
from app.models.identity import Child, User
from app.services.fitness_service import (
    get_detailed_stats,
    get_progress_summary,
    log_fitness_activity,
    record_benchmark,
)

router = APIRouter(prefix="/fitness", tags=["fitness"], dependencies=[Depends(require_active_subscription)])


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


# ── Request schemas ──


class FitnessLogCreate(BaseModel):
    child_id: uuid.UUID
    node_id: uuid.UUID
    duration_minutes: int = Field(ge=0)
    measurement_type: str = Field(min_length=1, max_length=50)
    measurement_value: float | None = None
    measurement_unit: str | None = Field(default=None, max_length=20)
    sets: int | None = Field(default=None, ge=0)
    reps: int | None = Field(default=None, ge=0)
    weight_lbs: float | None = Field(default=None, ge=0)
    distance_value: float | None = Field(default=None, ge=0)
    heart_rate_avg: int | None = Field(default=None, ge=0)
    notes: str | None = None
    logged_at: datetime | None = None


class BenchmarkCreate(BaseModel):
    child_id: uuid.UUID
    benchmark_name: str = Field(min_length=1, max_length=255)
    value: float
    unit: str = Field(min_length=1, max_length=20)
    tier: str | None = Field(default=None, max_length=50)
    notes: str | None = None
    measured_at: datetime | None = None


# ── Fitness log endpoints ──


@router.post("/log", status_code=201)
async def create_fitness_log(
    body: FitnessLogCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, body.child_id, user.household_id)
    result = await log_fitness_activity(
        db,
        household_id=user.household_id,
        child_id=body.child_id,
        node_id=body.node_id,
        logged_at=body.logged_at or datetime.now(UTC),
        duration_minutes=body.duration_minutes,
        measurement_type=body.measurement_type,
        measurement_value=body.measurement_value,
        measurement_unit=body.measurement_unit,
        sets=body.sets,
        reps=body.reps,
        weight_lbs=body.weight_lbs,
        distance_value=body.distance_value,
        heart_rate_avg=body.heart_rate_avg,
        notes=body.notes,
        logged_by=user.id,
    )
    return {
        **result,
        "id": str(result["id"]),
        "household_id": str(result["household_id"]),
        "child_id": str(result["child_id"]),
        "node_id": str(result["node_id"]),
        "logged_by": str(result["logged_by"]) if result["logged_by"] else None,
        "logged_at": result["logged_at"].isoformat() if result["logged_at"] else None,
        "state_event_id": str(result["state_event_id"]) if result["state_event_id"] else None,
    }


@router.get("/log/{child_id}")
async def list_fitness_logs(
    child_id: uuid.UUID,
    node_id: uuid.UUID | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    stmt = select(FitnessLog).where(
        FitnessLog.child_id == child_id,
        FitnessLog.household_id == user.household_id,
    )
    if node_id is not None:
        stmt = stmt.where(FitnessLog.node_id == node_id)
    if start_date is not None:
        stmt = stmt.where(FitnessLog.logged_at >= start_date)
    if end_date is not None:
        stmt = stmt.where(FitnessLog.logged_at <= end_date)

    result = await db.execute(stmt.order_by(FitnessLog.logged_at.desc()).limit(limit))
    logs = result.scalars().all()
    return {
        "items": [
            {
                "id": str(log.id),
                "child_id": str(log.child_id),
                "node_id": str(log.node_id),
                "logged_at": log.logged_at.isoformat() if log.logged_at else None,
                "duration_minutes": log.duration_minutes,
                "measurement_type": log.measurement_type,
                "measurement_value": log.measurement_value,
                "measurement_unit": log.measurement_unit,
                "sets": log.sets,
                "reps": log.reps,
                "weight_lbs": log.weight_lbs,
                "distance_value": log.distance_value,
                "heart_rate_avg": log.heart_rate_avg,
                "notes": log.notes,
                "logged_by": str(log.logged_by) if log.logged_by else None,
            }
            for log in logs
        ],
        "count": len(logs),
    }


# ── Benchmark endpoints ──


@router.post("/benchmark", status_code=201)
async def create_benchmark(
    body: BenchmarkCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    await _get_child_or_404(db, body.child_id, user.household_id)
    result = await record_benchmark(
        db,
        household_id=user.household_id,
        child_id=body.child_id,
        benchmark_name=body.benchmark_name,
        value=body.value,
        unit=body.unit,
        tier=body.tier,
        measured_at=body.measured_at,
        notes=body.notes,
    )
    return {
        **result,
        "id": str(result["id"]),
        "household_id": str(result["household_id"]),
        "child_id": str(result["child_id"]),
        "measured_at": result["measured_at"].isoformat() if result["measured_at"] else None,
    }


@router.get("/benchmarks/{child_id}")
async def list_benchmarks(
    child_id: uuid.UUID,
    benchmark_name: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    stmt = select(FitnessBenchmark).where(
        FitnessBenchmark.child_id == child_id,
        FitnessBenchmark.household_id == user.household_id,
    )
    if benchmark_name is not None:
        stmt = stmt.where(FitnessBenchmark.benchmark_name == benchmark_name)

    result = await db.execute(stmt.order_by(FitnessBenchmark.measured_at.desc()))
    benchmarks = result.scalars().all()
    return {
        "items": [
            {
                "id": str(b.id),
                "child_id": str(b.child_id),
                "benchmark_name": b.benchmark_name,
                "measured_at": b.measured_at.isoformat() if b.measured_at else None,
                "value": b.value,
                "unit": b.unit,
                "tier": b.tier,
                "percentile": b.percentile,
                "notes": b.notes,
            }
            for b in benchmarks
        ],
        "count": len(benchmarks),
    }


# ── Analytics ──


@router.get("/progress/{child_id}")
async def get_progress(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    return await get_progress_summary(db, user.household_id, child_id)


@router.get("/stats/{child_id}")
async def get_stats(
    child_id: uuid.UUID,
    period_start: datetime | None = Query(default=None),
    period_end: datetime | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    now = datetime.now(UTC)
    start = period_start or now.replace(hour=0, minute=0, second=0, microsecond=0).replace(day=1)
    end = period_end or now
    stats = await get_detailed_stats(db, user.household_id, child_id, start, end)
    return {
        **stats,
        "period_start": stats["period_start"].isoformat(),
        "period_end": stats["period_end"].isoformat(),
        "strength": [{**s, "date": s["date"].isoformat(), "node_id": str(s["node_id"])} for s in stats["strength"]],
        "endurance": [{**e, "date": e["date"].isoformat(), "node_id": str(e["node_id"])} for e in stats["endurance"]],
        "flexibility": [
            {**f, "date": f["date"].isoformat(), "node_id": str(f["node_id"])} for f in stats["flexibility"]
        ],
    }
