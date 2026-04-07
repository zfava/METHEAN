"""Family Resource Library API."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.evidence import FamilyResource
from app.models.identity import User

router = APIRouter(tags=["resources"])


class CreateResourceRequest(BaseModel):
    name: str
    resource_type: str = "textbook"
    subject_area: str | None = None
    publisher: str | None = None
    grade_range: str | None = None
    notes: str | None = None
    status: str = "owned"


class UpdateResourceRequest(BaseModel):
    name: str | None = None
    resource_type: str | None = None
    subject_area: str | None = None
    publisher: str | None = None
    grade_range: str | None = None
    notes: str | None = None
    status: str | None = None


def _serialize(r: FamilyResource) -> dict:
    return {
        "id": str(r.id), "name": r.name, "resource_type": r.resource_type,
        "subject_area": r.subject_area, "publisher": r.publisher,
        "grade_range": r.grade_range, "notes": r.notes, "status": r.status,
        "linked_node_ids": r.linked_node_ids or [],
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


@router.post("/resources", status_code=201)
async def create_resource(
    body: CreateResourceRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Add a resource to the family library."""
    resource = FamilyResource(
        household_id=user.household_id,
        created_by=user.id,
        name=body.name,
        resource_type=body.resource_type,
        subject_area=body.subject_area,
        publisher=body.publisher,
        grade_range=body.grade_range,
        notes=body.notes,
        status=body.status,
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return _serialize(resource)


@router.get("/resources")
async def list_resources(
    resource_type: str | None = None,
    subject_area: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List family resources with optional filters."""
    query = select(FamilyResource).where(FamilyResource.household_id == user.household_id)
    if resource_type:
        query = query.where(FamilyResource.resource_type == resource_type)
    if subject_area:
        query = query.where(FamilyResource.subject_area == subject_area)
    if status:
        query = query.where(FamilyResource.status == status)
    query = query.order_by(FamilyResource.name)
    result = await db.execute(query)
    return [_serialize(r) for r in result.scalars().all()]


@router.put("/resources/{resource_id}")
async def update_resource(
    resource_id: uuid.UUID,
    body: UpdateResourceRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update a resource."""
    result = await db.execute(
        select(FamilyResource).where(
            FamilyResource.id == resource_id,
            FamilyResource.household_id == user.household_id,
        )
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    await db.commit()
    await db.refresh(resource)
    return _serialize(resource)


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Delete a resource."""
    result = await db.execute(
        select(FamilyResource).where(
            FamilyResource.id == resource_id,
            FamilyResource.household_id == user.household_id,
        )
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    await db.delete(resource)
    await db.commit()
    return {"deleted": True}


@router.post("/resources/{resource_id}/link/{node_id}")
async def link_to_node(
    resource_id: uuid.UUID,
    node_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Link a resource to a learning node."""
    result = await db.execute(
        select(FamilyResource).where(
            FamilyResource.id == resource_id,
            FamilyResource.household_id == user.household_id,
        )
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    node_str = str(node_id)
    if node_str not in (resource.linked_node_ids or []):
        resource.linked_node_ids = (resource.linked_node_ids or []) + [node_str]
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(resource, "linked_node_ids")
    await db.commit()
    return _serialize(resource)


@router.delete("/resources/{resource_id}/link/{node_id}")
async def unlink_from_node(
    resource_id: uuid.UUID,
    node_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Unlink a resource from a learning node."""
    result = await db.execute(
        select(FamilyResource).where(
            FamilyResource.id == resource_id,
            FamilyResource.household_id == user.household_id,
        )
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource.linked_node_ids = [nid for nid in (resource.linked_node_ids or []) if nid != str(node_id)]
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(resource, "linked_node_ids")
    await db.commit()
    return _serialize(resource)
