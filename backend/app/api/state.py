"""Learner State Engine API (System 2).

State queries, retention summaries, attempt workflow, and state history.
"""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import PaginationParams, get_current_user, get_db, require_child_access
from app.core.cache import cache_get, cache_set
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningNode,
)
from app.models.enums import (
    EdgeRelation,
    MasteryLevel,
)
from app.models.governance import Attempt
from app.models.identity import Child, User
from app.models.state import ChildNodeState, FSRSCard, StateEvent
from app.schemas.state import (
    AttemptResponse,
    AttemptStartRequest,
    AttemptSubmitRequest,
    AttemptSubmitResponse,
    ChildStateResponse,
    NodeStateResponse,
    RetentionSummaryResponse,
    StateEventResponse,
)
from app.services.attempt_workflow import start_attempt, submit_attempt
from app.services.learning_context import get_activity_learning_context
from app.services.state_engine import compute_retrievability

router = APIRouter(tags=["state"])


# ── Helpers ──


async def _get_child_or_404(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
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


# ── State Query Endpoints ──


@router.get(
    "/children/{child_id}/state",
    response_model=ChildStateResponse,
)
async def get_child_state(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> ChildStateResponse:
    """Full state across all enrolled maps: every node with mastery, FSRS data."""
    # Check cache first (30s TTL)
    cache_key = f"child_state:{user.household_id}:{child_id}"
    cached = await cache_get(cache_key)
    if cached:
        return ChildStateResponse(**cached)

    await _get_child_or_404(db, child_id, user.household_id)

    # Get all enrolled maps
    enrollments = await db.execute(
        select(ChildMapEnrollment.learning_map_id).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.household_id == user.household_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    map_ids = list(enrollments.scalars().all())

    if not map_ids:
        return ChildStateResponse(
            child_id=child_id,
            nodes=[],
            total_nodes=0,
            mastered_count=0,
            in_progress_count=0,
            not_started_count=0,
        )

    # Get all active nodes in enrolled maps
    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id.in_(map_ids),
            LearningNode.household_id == user.household_id,
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    nodes = nodes_result.scalars().all()
    node_ids = [n.id for n in nodes]

    if not node_ids:
        return ChildStateResponse(
            child_id=child_id,
            nodes=[],
            total_nodes=0,
            mastered_count=0,
            in_progress_count=0,
            not_started_count=0,
        )

    # Batch fetch all states
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.node_id.in_(node_ids),
        )
    )
    states = {s.node_id: s for s in states_result.scalars().all()}

    # Batch fetch all FSRS cards
    cards_result = await db.execute(
        select(FSRSCard).where(
            FSRSCard.child_id == child_id,
            FSRSCard.node_id.in_(node_ids),
        )
    )
    cards = {c.node_id: c for c in cards_result.scalars().all()}

    now = datetime.now(UTC)
    node_responses = []
    mastered = in_progress = not_started = 0

    in_progress_levels = {MasteryLevel.emerging, MasteryLevel.developing, MasteryLevel.proficient}

    for node in nodes:
        state = states.get(node.id)
        card = cards.get(node.id)
        mastery = state.mastery_level if state else MasteryLevel.not_started

        retrievability = compute_retrievability(card, now) if card else None

        node_responses.append(
            NodeStateResponse(
                node_id=node.id,
                node_title=node.title,
                mastery_level=mastery,
                is_unlocked=state.is_unlocked if state else False,
                attempts_count=state.attempts_count if state else 0,
                time_spent_minutes=state.time_spent_minutes if state else 0,
                last_activity_at=state.last_activity_at if state else None,
                fsrs_due=card.due if card else None,
                fsrs_stability=card.stability if card else None,
                fsrs_difficulty=card.difficulty if card else None,
                fsrs_retrievability=round(retrievability, 4) if retrievability is not None else None,
                fsrs_state=card.state if card else None,
            )
        )

        if mastery == MasteryLevel.mastered:
            mastered += 1
        elif mastery in in_progress_levels:
            in_progress += 1
        else:
            not_started += 1

    response = ChildStateResponse(
        child_id=child_id,
        nodes=node_responses,
        total_nodes=len(nodes),
        mastered_count=mastered,
        in_progress_count=in_progress,
        not_started_count=not_started,
    )
    await cache_set(cache_key, response.model_dump(), ttl_seconds=30)
    return response


@router.get(
    "/children/{child_id}/nodes/{node_id}/history",
)
async def get_node_history(
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """StateEvent stream for one node, chronological."""
    await _get_child_or_404(db, child_id, user.household_id)

    base = select(StateEvent).where(
        StateEvent.child_id == child_id,
        StateEvent.node_id == node_id,
        StateEvent.household_id == user.household_id,
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(StateEvent.created_at.asc()).offset(pagination.skip).limit(pagination.limit)
    )
    return {
        "items": [StateEventResponse.model_validate(e) for e in result.scalars().all()],
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.get(
    "/children/{child_id}/retention-summary",
    response_model=RetentionSummaryResponse,
)
async def get_retention_summary(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> RetentionSummaryResponse:
    """Aggregate retention summary: counts and average retrievability."""
    await _get_child_or_404(db, child_id, user.household_id)

    # Get all enrolled map IDs
    enrollments = await db.execute(
        select(ChildMapEnrollment.learning_map_id).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.household_id == user.household_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    map_ids = list(enrollments.scalars().all())

    if not map_ids:
        return RetentionSummaryResponse(
            child_id=child_id,
            total_nodes=0,
            mastered_count=0,
            in_progress_count=0,
            not_started_count=0,
            decaying_count=0,
            blocked_count=0,
            average_retrievability=None,
        )

    # Count nodes
    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id.in_(map_ids),
            LearningNode.household_id == user.household_id,
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    nodes = nodes_result.scalars().all()
    node_ids = [n.id for n in nodes]
    total_nodes = len(nodes)

    if not node_ids:
        return RetentionSummaryResponse(
            child_id=child_id,
            total_nodes=0,
            mastered_count=0,
            in_progress_count=0,
            not_started_count=0,
            decaying_count=0,
            blocked_count=0,
            average_retrievability=None,
        )

    # Get states
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.node_id.in_(node_ids),
        )
    )
    states = {s.node_id: s for s in states_result.scalars().all()}

    # Get FSRS cards for mastered nodes
    cards_result = await db.execute(
        select(FSRSCard).where(
            FSRSCard.child_id == child_id,
            FSRSCard.node_id.in_(node_ids),
        )
    )
    cards = {c.node_id: c for c in cards_result.scalars().all()}

    # Get prerequisite edges for blocked computation
    edges_result = await db.execute(
        select(LearningEdge).where(
            LearningEdge.learning_map_id.in_(map_ids),
            LearningEdge.relation == EdgeRelation.prerequisite,
        )
    )
    edges = edges_result.scalars().all()
    prereqs: dict[uuid.UUID, list[uuid.UUID]] = {n.id: [] for n in nodes}
    for edge in edges:
        if edge.to_node_id in prereqs:
            prereqs[edge.to_node_id].append(edge.from_node_id)

    mastered_set = {nid for nid, s in states.items() if s.mastery_level == MasteryLevel.mastered}

    now = datetime.now(UTC)
    mastered_count = 0
    in_progress_count = 0
    not_started_count = 0
    blocked_count = 0
    decaying_count = 0
    retrievabilities = []

    in_progress_levels = {MasteryLevel.emerging, MasteryLevel.developing, MasteryLevel.proficient}

    for node in nodes:
        state = states.get(node.id)
        mastery = state.mastery_level if state else MasteryLevel.not_started
        card = cards.get(node.id)

        if mastery == MasteryLevel.mastered:
            mastered_count += 1
            if card:
                r = compute_retrievability(card, now)
                if r is not None:
                    retrievabilities.append(r)
                    from app.core.config import settings as cfg

                    if r < cfg.DECAY_RETRIEVABILITY_THRESHOLD:
                        decaying_count += 1
        elif mastery in in_progress_levels:
            in_progress_count += 1
        else:
            # Check if blocked
            node_prereqs = prereqs.get(node.id, [])
            if node_prereqs:
                is_unlocked = state.is_unlocked if state else False
                all_met = all(pid in mastered_set for pid in node_prereqs)
                if not all_met and not is_unlocked:
                    blocked_count += 1
                else:
                    not_started_count += 1
            else:
                not_started_count += 1

    avg_retrievability = round(sum(retrievabilities) / len(retrievabilities), 4) if retrievabilities else None

    return RetentionSummaryResponse(
        child_id=child_id,
        total_nodes=total_nodes,
        mastered_count=mastered_count,
        in_progress_count=in_progress_count,
        not_started_count=not_started_count,
        decaying_count=decaying_count,
        blocked_count=blocked_count,
        average_retrievability=avg_retrievability,
    )


# ── Attempt Endpoints ──


@router.post(
    "/activities/{activity_id}/attempts",
    response_model=AttemptResponse,
    status_code=201,
)
async def create_attempt(
    activity_id: uuid.UUID,
    body: AttemptStartRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AttemptResponse:
    """Start a new attempt for an activity."""
    # Verify child belongs to household
    child = await _get_child_or_404(db, body.child_id, user.household_id)

    try:
        attempt = await start_attempt(db, activity_id, child.id, user.household_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return AttemptResponse.model_validate(attempt)


@router.put(
    "/attempts/{attempt_id}/submit",
    response_model=AttemptSubmitResponse,
)
async def submit_attempt_endpoint(
    attempt_id: uuid.UUID,
    body: AttemptSubmitRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AttemptSubmitResponse:
    """Submit an attempt, triggering the evaluation pipeline."""
    try:
        result = await submit_attempt(
            db,
            attempt_id=attempt_id,
            household_id=user.household_id,
            duration_minutes=body.duration_minutes,
            score=body.score,
            confidence=body.confidence,
            feedback=body.feedback,
            user_id=user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    attempt = result["attempt"]

    return AttemptSubmitResponse(
        attempt=AttemptResponse.model_validate(attempt),
        mastery_level=result["mastery_level"] or MasteryLevel.not_started,
        previous_mastery=result["previous_mastery"] or MasteryLevel.not_started,
        fsrs_due=result["fsrs_due"],
        fsrs_rating=result["fsrs_rating"] or 0,
        state_event_id=result["state_event_id"] or uuid.UUID(int=0),
        nodes_unblocked=result["nodes_unblocked"],
    )


@router.get(
    "/attempts/{attempt_id}",
    response_model=AttemptResponse,
)
async def get_attempt(
    attempt_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AttemptResponse:
    """Get attempt details."""
    result = await db.execute(
        select(Attempt).where(
            Attempt.id == attempt_id,
            Attempt.household_id == user.household_id,
        )
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    return AttemptResponse.model_validate(attempt)


@router.get("/activities/{activity_id}/learn")
async def get_learning_context(
    activity_id: uuid.UUID,
    child_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get the full learning context for a child's activity.

    Returns teaching content, lesson steps, practice prompts,
    assessment criteria, and previous attempt history.
    """
    try:
        return await get_activity_learning_context(db, activity_id, user.household_id, child_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
