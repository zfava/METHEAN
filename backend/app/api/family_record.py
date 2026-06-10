"""Family Record API: cumulative evidence-backed record and sealed exports.

Read-only over learner state. Subscription-gated at the router level,
matching the documents router (transcript and compliance documents are
the same product tier). Email verification is applied at mount time in
main.py like every other child-data router, and the fail-closed
ChildScopeMiddleware denies child-scoped tokens on all of these paths.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_active_subscription, require_child_access
from app.models.evidence import Artifact
from app.models.identity import Child, User
from app.schemas.family_record import ExportListItem, ExportResponse, FamilyRecord
from app.services.family_record import assemble_family_record, export_family_record

router = APIRouter(tags=["family-record"], dependencies=[Depends(require_active_subscription)])


@router.get("/children/{child_id}/family-record", response_model=FamilyRecord)
async def get_family_record(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> FamilyRecord:
    """The cumulative Family Record as JSON: transcript, mastery
    evidence chains, attendance, reading log, and chain integrity."""
    try:
        return await assemble_family_record(db, user.household_id, child_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Child not found")


@router.post("/children/{child_id}/family-record/export", response_model=ExportResponse)
async def export_family_record_endpoint(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> ExportResponse:
    """Build and store a sealed export bundle.

    The export itself is logged to the governance chain, so every
    issued bundle leaves a permanent, tamper-evident receipt.
    """
    try:
        result = await export_family_record(db, user.household_id, child_id, user.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Child not found")
    return ExportResponse(**result)


@router.get("/family-record/exports", response_model=list[ExportListItem])
async def list_family_record_exports(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ExportListItem]:
    """Prior sealed exports for this household, with hashes and dates."""
    result = await db.execute(
        select(Artifact)
        .where(
            Artifact.household_id == user.household_id,
            Artifact.metadata_.contains({"kind": "family_record_bundle"}),
        )
        .order_by(Artifact.created_at.desc())
    )
    items = []
    for artifact in result.scalars().all():
        meta = artifact.metadata_ or {}
        items.append(
            ExportListItem(
                artifact_id=artifact.id,
                child_id=artifact.child_id,
                title=artifact.title,
                bundle_hash=meta.get("bundle_hash"),
                content_hash=meta.get("content_hash"),
                created_at=artifact.created_at,
                file_size_bytes=artifact.file_size_bytes,
            )
        )
    return items
