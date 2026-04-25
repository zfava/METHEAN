"""Operations API: Alerts, Notifications, Artifacts, Snapshots, Compliance, Health."""

import uuid
from datetime import UTC, date, datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import PaginationParams, get_current_user, get_db, require_child_access
from app.models.curriculum import LearningNode
from app.models.enums import AlertStatus, ArtifactType, MasteryLevel
from app.models.evidence import Alert, Artifact, WeeklySnapshot
from app.models.identity import Child, Household, User
from app.models.operational import NotificationLog
from app.models.state import ChildNodeState
from app.services.data_export import export_family_data
from app.services.notifications import send_notification
from app.services.storage import get_presigned_url, upload_artifact

MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB

# Map MIME prefixes/extensions to ArtifactType
_MIME_TYPE_MAP: dict[str, ArtifactType] = {
    "image/": ArtifactType.photo,
    "video/": ArtifactType.video,
    "audio/": ArtifactType.audio,
    "application/pdf": ArtifactType.document,
    "application/msword": ArtifactType.document,
    "application/vnd.": ArtifactType.document,
    "text/": ArtifactType.document,
}


def _detect_artifact_type(content_type: str | None, filename: str | None) -> ArtifactType:
    """Infer ArtifactType from MIME type or filename extension."""
    ct = (content_type or "").lower()
    for prefix, atype in _MIME_TYPE_MAP.items():
        if ct.startswith(prefix):
            return atype

    if filename:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        ext_map = {
            "jpg": ArtifactType.photo,
            "jpeg": ArtifactType.photo,
            "png": ArtifactType.photo,
            "gif": ArtifactType.photo,
            "webp": ArtifactType.photo,
            "svg": ArtifactType.photo,
            "mp4": ArtifactType.video,
            "mov": ArtifactType.video,
            "webm": ArtifactType.video,
            "avi": ArtifactType.video,
            "mp3": ArtifactType.audio,
            "wav": ArtifactType.audio,
            "ogg": ArtifactType.audio,
            "m4a": ArtifactType.audio,
            "pdf": ArtifactType.document,
            "doc": ArtifactType.document,
            "docx": ArtifactType.document,
            "txt": ArtifactType.document,
            "md": ArtifactType.document,
            "csv": ArtifactType.document,
        }
        if ext in ext_map:
            return ext_map[ext]

    return ArtifactType.document  # safe default


router = APIRouter(tags=["operations"])


# ── Helpers ──


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


# ══════════════════════════════════════════════════
# Alerts
# ══════════════════════════════════════════════════


@router.get("/children/{child_id}/alerts")
async def list_alerts(
    child_id: uuid.UUID,
    status: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    base = select(Alert).where(
        Alert.child_id == child_id,
        Alert.household_id == user.household_id,
    )
    if status:
        base = base.where(Alert.status == status)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0

    result = await db.execute(base.order_by(Alert.created_at.desc()).offset(pagination.skip).limit(pagination.limit))
    alerts = result.scalars().all()
    items = [
        {
            "id": str(a.id),
            "severity": a.severity.value if hasattr(a.severity, "value") else str(a.severity),
            "status": a.status.value if hasattr(a.status, "value") else str(a.status),
            "title": a.title,
            "message": a.message,
            "source": a.source,
            "metadata": a.metadata_,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]
    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.put("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.household_id == user.household_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = AlertStatus.read
    alert.read_at = datetime.now(UTC)
    await db.flush()
    return {"id": str(alert_id), "status": "read"}


@router.put("/alerts/{alert_id}/dismiss")
async def dismiss_alert(
    alert_id: uuid.UUID,
    reason: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.household_id == user.household_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = AlertStatus.dismissed
    alert.read_at = datetime.now(UTC)
    await db.flush()
    return {"id": str(alert_id), "status": "dismissed"}


# ══════════════════════════════════════════════════
# Notifications
# ══════════════════════════════════════════════════


@router.get("/notifications")
async def list_notifications(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    base = select(NotificationLog).where(
        NotificationLog.household_id == user.household_id,
        NotificationLog.user_id == user.id,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(NotificationLog.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [
            {
                "id": str(n.id),
                "channel": n.channel,
                "title": n.title,
                "body": n.body,
                "sent_at": n.sent_at.isoformat() if n.sent_at else None,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in result.scalars().all()
        ],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.post("/notifications/test")
async def send_test_notification(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Send a test notification to verify the system."""
    # Look up household timezone for quiet hours check
    h_result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = h_result.scalar_one()
    notif = await send_notification(
        db,
        user.household_id,
        user.id,
        "test",
        "Test Notification",
        "This is a test notification from METHEAN.",
        timezone=household.timezone or "UTC",
    )
    return {"sent": notif is not None}


# ══════════════════════════════════════════════════
# Weekly Snapshots
# ══════════════════════════════════════════════════


@router.get("/children/{child_id}/snapshots")
async def list_snapshots(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)
    base = select(WeeklySnapshot).where(
        WeeklySnapshot.child_id == child_id,
        WeeklySnapshot.household_id == user.household_id,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(WeeklySnapshot.week_start.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [
            {
                "id": str(s.id),
                "week_start": s.week_start.isoformat(),
                "week_end": s.week_end.isoformat(),
                "total_minutes": s.total_minutes,
                "activities_completed": s.activities_completed,
                "nodes_mastered": s.nodes_mastered,
                "nodes_progressed": s.nodes_progressed,
                "reviews_completed": s.reviews_completed,
                "summary": s.summary,
            }
            for s in result.scalars().all()
        ],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.get("/children/{child_id}/snapshots/compare")
async def compare_snapshots(
    child_id: uuid.UUID,
    from_date: date = Query(alias="from"),
    to_date: date = Query(alias="to"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    await _get_child_or_404(db, child_id, user.household_id)

    from_result = await db.execute(
        select(WeeklySnapshot).where(
            WeeklySnapshot.child_id == child_id,
            WeeklySnapshot.week_start == from_date,
        )
    )
    to_result = await db.execute(
        select(WeeklySnapshot).where(
            WeeklySnapshot.child_id == child_id,
            WeeklySnapshot.week_start == to_date,
        )
    )
    from_snap = from_result.scalar_one_or_none()
    to_snap = to_result.scalar_one_or_none()

    if not from_snap or not to_snap:
        raise HTTPException(status_code=404, detail="Snapshot not found for specified dates")

    return {
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "nodes_mastered_delta": (to_snap.nodes_mastered or 0) - (from_snap.nodes_mastered or 0),
        "nodes_progressed_delta": (to_snap.nodes_progressed or 0) - (from_snap.nodes_progressed or 0),
        "total_minutes_delta": (to_snap.total_minutes or 0) - (from_snap.total_minutes or 0),
        "activities_completed_delta": (to_snap.activities_completed or 0) - (from_snap.activities_completed or 0),
    }


# ══════════════════════════════════════════════════
# Compliance Report
# ══════════════════════════════════════════════════


@router.get("/children/{child_id}/compliance-report")
async def compliance_report(
    child_id: uuid.UUID,
    from_date: date = Query(alias="from"),
    to_date: date = Query(alias="to"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Generate structured compliance report for homeschool state reporting."""
    child = await _get_child_or_404(db, child_id, user.household_id)

    # Get all node states
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == user.household_id,
        )
    )
    states = states_result.scalars().all()

    # Get node titles
    node_ids = [s.node_id for s in states]
    nodes_result = await db.execute(select(LearningNode).where(LearningNode.id.in_(node_ids))) if node_ids else None
    node_map = {n.id: n for n in (nodes_result.scalars().all() if nodes_result else [])}

    total_minutes = sum(s.time_spent_minutes or 0 for s in states)
    total_attempts = sum(s.attempts_count or 0 for s in states)
    mastered = [s for s in states if s.mastery_level == MasteryLevel.mastered]

    return {
        "child_name": f"{child.first_name} {child.last_name or ''}".strip(),
        "date_range": {"from": from_date.isoformat(), "to": to_date.isoformat()},
        "grade_level": child.grade_level,
        "total_hours_logged": round(total_minutes / 60, 1),
        "total_activities_attempted": total_attempts,
        "nodes_mastered": len(mastered),
        "nodes_in_progress": len(
            [s for s in states if s.mastery_level not in (MasteryLevel.mastered, MasteryLevel.not_started)]
        ),
        "mastered_skills": [
            {
                "title": node_map[s.node_id].title if s.node_id in node_map else "Unknown",
                "attempts": s.attempts_count,
                "time_minutes": s.time_spent_minutes,
            }
            for s in mastered
        ],
        "generated_at": datetime.now(UTC).isoformat(),
    }


# ══════════════════════════════════════════════════
# Artifacts
# ══════════════════════════════════════════════════


@router.post("/children/{child_id}/artifacts", status_code=201)
async def upload_artifact_endpoint(
    child_id: uuid.UUID,
    file: UploadFile = File(...),
    attempt_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
) -> dict:
    """Upload an artifact file for a child. Max 50 MB."""
    await _get_child_or_404(db, child_id, user.household_id)

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        )

    content_type = file.content_type or "application/octet-stream"
    filename = file.filename or "upload"
    artifact_type = _detect_artifact_type(content_type, filename)

    # Upload to S3
    s3_key = upload_artifact(
        file_bytes=contents,
        filename=filename,
        content_type=content_type,
        household_id=user.household_id,
        child_id=child_id,
    )

    # Create DB record
    artifact = Artifact(
        household_id=user.household_id,
        child_id=child_id,
        attempt_id=attempt_id,
        artifact_type=artifact_type,
        title=filename,
        s3_key=s3_key,
        mime_type=content_type,
        file_size_bytes=len(contents),
    )
    db.add(artifact)
    await db.flush()

    download_url = get_presigned_url(s3_key)

    return {
        "id": str(artifact.id),
        "child_id": str(child_id),
        "artifact_type": artifact_type.value,
        "title": filename,
        "mime_type": content_type,
        "file_size_bytes": len(contents),
        "s3_key": s3_key,
        "download_url": download_url,
        "created_at": artifact.created_at.isoformat() if artifact.created_at else None,
    }


@router.get("/children/{child_id}/artifacts")
async def list_artifacts(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """List artifacts for a child with pagination."""
    await _get_child_or_404(db, child_id, user.household_id)

    base = select(Artifact).where(
        Artifact.child_id == child_id,
        Artifact.household_id == user.household_id,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0

    result = await db.execute(base.order_by(Artifact.created_at.desc()).offset(pagination.skip).limit(pagination.limit))
    items = []
    for a in result.scalars().all():
        item = {
            "id": str(a.id),
            "artifact_type": a.artifact_type.value if hasattr(a.artifact_type, "value") else str(a.artifact_type),
            "title": a.title,
            "mime_type": a.mime_type,
            "file_size_bytes": a.file_size_bytes,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        if a.s3_key:
            item["download_url"] = get_presigned_url(a.s3_key)
        items.append(item)

    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.get("/artifacts/{artifact_id}/download")
async def download_artifact(
    artifact_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> RedirectResponse:
    """Redirect to a presigned S3 download URL (15-min expiry)."""
    result = await db.execute(
        select(Artifact).where(
            Artifact.id == artifact_id,
            Artifact.household_id == user.household_id,
        )
    )
    artifact = result.scalar_one_or_none()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    if not artifact.s3_key:
        raise HTTPException(status_code=404, detail="Artifact has no file stored")

    url = get_presigned_url(artifact.s3_key, expires_in=900)
    return RedirectResponse(url=url, status_code=302)


@router.post("/household/export")
async def export_household_data(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Export complete family educational record as ZIP."""
    from fastapi.responses import Response

    data = await export_family_data(db, user.household_id)
    return Response(
        content=data,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="methean_export.zip"'},
    )
