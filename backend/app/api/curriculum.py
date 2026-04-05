"""Curriculum Architecture API (System 1).

Learning Map CRUD, DAG edge management with cycle detection,
child map state, enrollment, parent overrides, and template copying.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import PaginationParams, get_current_user, get_db, require_permission, require_role
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningMapClosure,
    LearningNode,
    Subject,
)
from app.models.enums import GovernanceAction, MasteryLevel, StateEventType
from app.models.governance import GovernanceEvent
from app.models.identity import Child, User
from app.models.state import ChildNodeState, StateEvent
from app.schemas.curriculum import (
    ChildMapStateResponse,
    EdgeCreate,
    EdgeResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    LearningMapCreate,
    LearningMapDetailResponse,
    LearningMapResponse,
    LearningMapUpdate,
    NodeCreate,
    NodeResponse,
    NodeStateStatus,
    NodeUpdate,
    OverrideRequest,
    OverrideResponse,
    SubjectCreate,
    SubjectResponse,
    TemplateCopyResponse,
    TemplateInfo,
)
from app.services.dag_engine import (
    add_closure_entries,
    check_prerequisites_met,
    compute_map_state,
    increment_map_version,
    rebuild_closure_for_map,
    would_create_cycle,
)
from app.services.templates import TEMPLATES

router = APIRouter(tags=["curriculum"])


# ── Helpers ──

async def _get_map_or_404(
    db: AsyncSession, map_id: uuid.UUID, household_id: uuid.UUID,
) -> LearningMap:
    result = await db.execute(
        select(LearningMap).where(
            LearningMap.id == map_id,
            LearningMap.household_id == household_id,
        )
    )
    lmap = result.scalar_one_or_none()
    if not lmap:
        raise HTTPException(status_code=404, detail="Learning map not found")
    return lmap


async def _get_node_or_404(
    db: AsyncSession, map_id: uuid.UUID, node_id: uuid.UUID, household_id: uuid.UUID,
) -> LearningNode:
    result = await db.execute(
        select(LearningNode).where(
            LearningNode.id == node_id,
            LearningNode.learning_map_id == map_id,
            LearningNode.household_id == household_id,
        )
    )
    node = result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


async def _get_child_or_404(
    db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID,
) -> Child:
    result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.household_id == household_id,
        )
    )
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


# ── Subject endpoints ──

@router.post("/subjects", response_model=SubjectResponse, status_code=201)
async def create_subject(
    body: SubjectCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> SubjectResponse:
    subject = Subject(
        household_id=user.household_id,
        name=body.name,
        description=body.description,
        color=body.color,
        icon=body.icon,
        sort_order=body.sort_order,
    )
    db.add(subject)
    await db.flush()
    return SubjectResponse.model_validate(subject)


@router.get("/subjects")
async def list_subjects(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    base = select(Subject).where(
        Subject.household_id == user.household_id, Subject.is_active == True  # noqa: E712
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(Subject.sort_order).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [SubjectResponse.model_validate(s) for s in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


# ── Templates (must be before {map_id} routes to avoid path conflicts) ──

@router.get("/learning-maps/templates", response_model=list[TemplateInfo])
async def list_templates(
    user: User = Depends(get_current_user),
) -> list[TemplateInfo]:
    return [
        TemplateInfo(
            template_id=t.template_id,
            name=t.name,
            description=t.description,
            subject_count=1,
            node_count=len(t.nodes),
        )
        for t in TEMPLATES.values()
    ]


@router.post(
    "/learning-maps/from-template/{template_id}",
    response_model=TemplateCopyResponse,
    status_code=201,
)
async def copy_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("manage.children")),
) -> TemplateCopyResponse:
    template = TEMPLATES.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Create subject
    subject = Subject(
        household_id=user.household_id,
        name=template.subject_name,
        color=template.subject_color,
        description=template.description,
    )
    db.add(subject)
    await db.flush()

    # Create learning map
    lmap = LearningMap(
        household_id=user.household_id,
        subject_id=subject.id,
        name=template.name,
        description=template.description,
    )
    db.add(lmap)
    await db.flush()

    # Create nodes with new UUIDs, maintain ref -> uuid mapping
    ref_to_uuid: dict[str, uuid.UUID] = {}
    for tnode in template.nodes:
        node = LearningNode(
            learning_map_id=lmap.id,
            household_id=user.household_id,
            node_type=tnode.node_type,
            title=tnode.title,
            description=tnode.description,
            estimated_minutes=tnode.estimated_minutes,
            sort_order=tnode.sort_order,
        )
        db.add(node)
        await db.flush()
        ref_to_uuid[tnode.ref] = node.id

    # Create edges
    edge_count = 0
    for tedge in template.edges:
        from_id = ref_to_uuid[tedge.from_ref]
        to_id = ref_to_uuid[tedge.to_ref]
        edge = LearningEdge(
            learning_map_id=lmap.id,
            household_id=user.household_id,
            from_node_id=from_id,
            to_node_id=to_id,
            relation=tedge.relation,
        )
        db.add(edge)
        edge_count += 1

    await db.flush()

    # Build transitive closure for the new map
    await rebuild_closure_for_map(db, lmap.id)

    return TemplateCopyResponse(
        learning_map_id=lmap.id,
        subject_id=subject.id,
        name=template.name,
        node_count=len(template.nodes),
        edge_count=edge_count,
    )


# ── Learning Map CRUD ──

@router.post("/learning-maps", response_model=LearningMapResponse, status_code=201)
async def create_learning_map(
    body: LearningMapCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LearningMapResponse:
    # Verify subject belongs to household
    result = await db.execute(
        select(Subject).where(
            Subject.id == body.subject_id,
            Subject.household_id == user.household_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Subject not found")

    lmap = LearningMap(
        household_id=user.household_id,
        subject_id=body.subject_id,
        name=body.name,
        description=body.description,
    )
    db.add(lmap)
    await db.flush()
    return LearningMapResponse.model_validate(lmap)


@router.get("/learning-maps")
async def list_learning_maps(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> dict:
    base = select(LearningMap).where(LearningMap.household_id == user.household_id)
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(LearningMap.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [LearningMapResponse.model_validate(m) for m in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.get("/learning-maps/{map_id}", response_model=LearningMapDetailResponse)
async def get_learning_map(
    map_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LearningMapDetailResponse:
    result = await db.execute(
        select(LearningMap)
        .where(
            LearningMap.id == map_id,
            LearningMap.household_id == user.household_id,
        )
        .options(
            selectinload(LearningMap.nodes),
            selectinload(LearningMap.edges),
        )
    )
    lmap = result.scalar_one_or_none()
    if not lmap:
        raise HTTPException(status_code=404, detail="Learning map not found")

    # Filter to active nodes only
    active_nodes = [n for n in lmap.nodes if n.is_active]

    return LearningMapDetailResponse(
        id=lmap.id,
        household_id=lmap.household_id,
        subject_id=lmap.subject_id,
        name=lmap.name,
        description=lmap.description,
        version=lmap.version,
        is_published=lmap.is_published,
        created_at=lmap.created_at,
        updated_at=lmap.updated_at,
        nodes=[NodeResponse.model_validate(n) for n in sorted(active_nodes, key=lambda x: x.sort_order)],
        edges=[EdgeResponse.model_validate(e) for e in lmap.edges],
    )


@router.put("/learning-maps/{map_id}", response_model=LearningMapResponse)
async def update_learning_map(
    map_id: uuid.UUID,
    body: LearningMapUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LearningMapResponse:
    lmap = await _get_map_or_404(db, map_id, user.household_id)

    if body.name is not None:
        lmap.name = body.name
    if body.description is not None:
        lmap.description = body.description
    if body.is_published is not None:
        lmap.is_published = body.is_published

    await db.flush()
    await db.refresh(lmap)
    return LearningMapResponse.model_validate(lmap)


# ── Node endpoints ──

@router.post(
    "/learning-maps/{map_id}/nodes",
    response_model=NodeResponse,
    status_code=201,
)
async def create_node(
    map_id: uuid.UUID,
    body: NodeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> NodeResponse:
    lmap = await _get_map_or_404(db, map_id, user.household_id)

    node = LearningNode(
        learning_map_id=lmap.id,
        household_id=user.household_id,
        node_type=body.node_type,
        title=body.title,
        description=body.description,
        content=body.content or {},
        estimated_minutes=body.estimated_minutes,
        sort_order=body.sort_order,
    )
    db.add(node)
    await db.flush()

    # Structural change: increment version
    await increment_map_version(db, lmap.id)

    return NodeResponse.model_validate(node)


@router.put(
    "/learning-maps/{map_id}/nodes/{node_id}",
    response_model=NodeResponse,
)
async def update_node(
    map_id: uuid.UUID,
    node_id: uuid.UUID,
    body: NodeUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> NodeResponse:
    node = await _get_node_or_404(db, map_id, node_id, user.household_id)

    if body.title is not None:
        node.title = body.title
    if body.description is not None:
        node.description = body.description
    if body.content is not None:
        node.content = body.content
    if body.estimated_minutes is not None:
        node.estimated_minutes = body.estimated_minutes
    if body.sort_order is not None:
        node.sort_order = body.sort_order
    if body.node_type is not None:
        node.node_type = body.node_type

    await db.flush()
    return NodeResponse.model_validate(node)


@router.delete(
    "/learning-maps/{map_id}/nodes/{node_id}",
    status_code=204,
)
async def delete_node(
    map_id: uuid.UUID,
    node_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    node = await _get_node_or_404(db, map_id, node_id, user.household_id)

    # Soft delete
    node.is_active = False
    await db.flush()

    # Remove edges involving this node and rebuild closure
    from sqlalchemy import or_, delete as sa_delete

    await db.execute(
        sa_delete(LearningEdge).where(
            LearningEdge.learning_map_id == map_id,
            or_(
                LearningEdge.from_node_id == node_id,
                LearningEdge.to_node_id == node_id,
            ),
        )
    )
    await db.flush()

    # Rebuild closure after edge removal
    await rebuild_closure_for_map(db, map_id)

    # Structural change: increment version
    await increment_map_version(db, map_id)


# ── Edge endpoints ──

@router.post(
    "/learning-maps/{map_id}/edges",
    response_model=EdgeResponse,
    status_code=201,
)
async def create_edge(
    map_id: uuid.UUID,
    body: EdgeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> EdgeResponse:
    lmap = await _get_map_or_404(db, map_id, user.household_id)

    # Verify both nodes exist and belong to this map
    from_node = await _get_node_or_404(db, map_id, body.from_node_id, user.household_id)
    to_node = await _get_node_or_404(db, map_id, body.to_node_id, user.household_id)

    # Check for duplicate edge
    existing = await db.execute(
        select(LearningEdge).where(
            LearningEdge.learning_map_id == map_id,
            LearningEdge.from_node_id == body.from_node_id,
            LearningEdge.to_node_id == body.to_node_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409, detail="Edge already exists between these nodes"
        )

    # CRITICAL: cycle detection
    if await would_create_cycle(db, map_id, body.from_node_id, body.to_node_id):
        raise HTTPException(
            status_code=409,
            detail="Adding this edge would create a cycle in the DAG",
        )

    # Create edge
    edge = LearningEdge(
        learning_map_id=map_id,
        household_id=user.household_id,
        from_node_id=body.from_node_id,
        to_node_id=body.to_node_id,
        relation=body.relation,
        weight=body.weight,
    )
    db.add(edge)
    await db.flush()

    # Update transitive closure
    await add_closure_entries(db, map_id, body.from_node_id, body.to_node_id)

    # Structural change: increment version
    await increment_map_version(db, map_id)

    return EdgeResponse.model_validate(edge)


@router.delete(
    "/learning-maps/{map_id}/edges/{edge_id}",
    status_code=204,
)
async def delete_edge(
    map_id: uuid.UUID,
    edge_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    result = await db.execute(
        select(LearningEdge).where(
            LearningEdge.id == edge_id,
            LearningEdge.learning_map_id == map_id,
            LearningEdge.household_id == user.household_id,
        )
    )
    edge = result.scalar_one_or_none()
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")

    await db.delete(edge)
    await db.flush()

    # Recompute closure after edge removal
    await rebuild_closure_for_map(db, map_id)

    # Structural change: increment version
    await increment_map_version(db, map_id)


# ── Child Map State ──

@router.get(
    "/children/{child_id}/map-state",
    response_model=list[ChildMapStateResponse],
)
async def get_child_map_state(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ChildMapStateResponse]:
    child = await _get_child_or_404(db, child_id, user.household_id)

    # Get all active enrollments for this child
    enrollments_result = await db.execute(
        select(ChildMapEnrollment).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.household_id == user.household_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    enrollments = enrollments_result.scalars().all()

    responses = []
    for enrollment in enrollments:
        # Get the map
        map_result = await db.execute(
            select(LearningMap).where(LearningMap.id == enrollment.learning_map_id)
        )
        lmap = map_result.scalar_one_or_none()
        if not lmap:
            continue

        node_states = await compute_map_state(
            db, child_id, user.household_id, enrollment.learning_map_id
        )

        responses.append(ChildMapStateResponse(
            child_id=child_id,
            learning_map_id=enrollment.learning_map_id,
            map_name=lmap.name,
            enrolled=True,
            progress_pct=enrollment.progress_pct,
            nodes=[NodeStateStatus(**ns) for ns in node_states],
        ))

    return responses


@router.get(
    "/children/{child_id}/map-state/{map_id}",
    response_model=ChildMapStateResponse,
)
async def get_child_single_map_state(
    child_id: uuid.UUID,
    map_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ChildMapStateResponse:
    child = await _get_child_or_404(db, child_id, user.household_id)
    lmap = await _get_map_or_404(db, map_id, user.household_id)

    # Check enrollment
    enroll_result = await db.execute(
        select(ChildMapEnrollment).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.learning_map_id == map_id,
        )
    )
    enrollment = enroll_result.scalar_one_or_none()

    node_states = await compute_map_state(
        db, child_id, user.household_id, map_id
    )

    return ChildMapStateResponse(
        child_id=child_id,
        learning_map_id=map_id,
        map_name=lmap.name,
        enrolled=enrollment is not None,
        progress_pct=enrollment.progress_pct if enrollment else 0.0,
        nodes=[NodeStateStatus(**ns) for ns in node_states],
    )


# ── Enrollment ──

@router.post(
    "/children/{child_id}/enrollments",
    response_model=EnrollmentResponse,
    status_code=201,
)
async def enroll_child(
    child_id: uuid.UUID,
    body: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("manage.children")),
) -> EnrollmentResponse:
    child = await _get_child_or_404(db, child_id, user.household_id)
    lmap = await _get_map_or_404(db, body.learning_map_id, user.household_id)

    # Check for existing enrollment
    existing = await db.execute(
        select(ChildMapEnrollment).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.learning_map_id == body.learning_map_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409, detail="Child is already enrolled in this map"
        )

    enrollment = ChildMapEnrollment(
        child_id=child_id,
        household_id=user.household_id,
        learning_map_id=body.learning_map_id,
        enrolled_at_version=lmap.version,
    )
    db.add(enrollment)
    await db.flush()

    return EnrollmentResponse.model_validate(enrollment)


# ── Parent Override ──

@router.post(
    "/children/{child_id}/nodes/{node_id}/override",
    response_model=OverrideResponse,
)
async def override_blocked_node(
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    body: OverrideRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("override.prerequisites")),
) -> OverrideResponse:
    child = await _get_child_or_404(db, child_id, user.household_id)

    # Find the node
    node_result = await db.execute(
        select(LearningNode).where(
            LearningNode.id == node_id,
            LearningNode.household_id == user.household_id,
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    node = node_result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    # Get or create ChildNodeState
    state_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.node_id == node_id,
            ChildNodeState.household_id == user.household_id,
        )
    )
    state = state_result.scalar_one_or_none()

    if state:
        state.is_unlocked = True
    else:
        state = ChildNodeState(
            child_id=child_id,
            household_id=user.household_id,
            node_id=node_id,
            mastery_level=MasteryLevel.not_started,
            is_unlocked=True,
        )
        db.add(state)

    # Log as GovernanceEvent (immutable audit)
    gov_event = GovernanceEvent(
        household_id=user.household_id,
        user_id=user.id,
        action=GovernanceAction.approve,
        target_type="child_node_state",
        target_id=node_id,
        reason=body.reason,
        metadata_={"child_id": str(child_id), "override_type": "unlock_blocked_node"},
    )
    db.add(gov_event)

    # Also log as StateEvent (append-only state history)
    state_event = StateEvent(
        child_id=child_id,
        household_id=user.household_id,
        node_id=node_id,
        event_type=StateEventType.override,
        from_state="blocked",
        to_state="unlocked",
        trigger="parent_override",
        metadata_={"reason": body.reason, "overridden_by": str(user.id)},
        created_by=user.id,
    )
    db.add(state_event)

    await db.flush()

    return OverrideResponse(
        governance_event_id=gov_event.id,
        node_id=node_id,
        child_id=child_id,
        message=f"Node '{node.title}' unlocked for child via parent override",
    )
