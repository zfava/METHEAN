# subscription_exempt: learner state read surface; account/recovery visibility
# See fix/methean6-08-subscription-gating for classification rationale.
"""Learner State Engine API (System 2).

State queries, retention summaries, attempt workflow, and state history.
"""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    PaginationParams,
    get_current_user,
    get_db,
    require_child_access,
    require_role,
)
from app.core.cache import cache_get, cache_set
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningNode,
)
from app.models.enums import (
    EdgeRelation,
    GovernanceAction,
    MasteryLevel,
)
from app.models.governance import Attempt, SupervisionAttestation
from app.models.identity import Child, Household, User
from app.models.state import ChildNodeState, FSRSCard, StateEvent
from app.schemas.state import (
    AttemptProgressRequest,
    AttemptResponse,
    AttemptStartRequest,
    AttemptSubmitRequest,
    AttemptSubmitResponse,
    ChildStateResponse,
    DemotionFeedItem,
    MasteryOverrideRequest,
    MasteryOverrideResponse,
    NodeStateResponse,
    RetentionSummaryResponse,
    StateEventResponse,
    SupervisionAttestationRequest,
    SupervisionAttestationResponse,
)
from app.services.attempt_workflow import save_attempt_progress, start_attempt, submit_attempt
from app.services.learning_context import get_activity_learning_context
from app.services.node_content import requires_qualified_human_present_at_runtime
from app.services.state_engine import apply_mastery_override, compute_retrievability
from app.services.supervision import local_end_of_day

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


@router.get("/children/{child_id}/session-signal")
async def get_session_signal(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Parent live view of the child's ephemeral within-session signal.

    Read only, parent scope, verified email (router level). Returns
    {signal, as_of, expires_at} when a signal is live, or {} otherwise.
    The signal is ephemeral and clears itself when its TTL lapses. The
    child never reaches this view: a classification of a child is never
    shown to that child.
    """
    # Parent surface only. A child-scoped session is denied outright so a
    # child can never see its own classification.
    if getattr(user, "token_scope", "parent") == "child":
        raise HTTPException(status_code=403, detail="parent_scope_required")

    # Policy off for the tutor role disables the whole layer, this view
    # included.
    from app.services.governance import AI_AUTONOMY_OFF, get_ai_role_policy

    if await get_ai_role_policy(db, user.household_id, "tutor") == AI_AUTONOMY_OFF:
        return {}

    from app.services.tutor_session_signals import get_live_signal

    return await get_live_signal(child_id) or {}


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
    "/children/{child_id}/demotions",
)
async def get_demotions(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
    _child: Child = Depends(require_child_access("read")),
) -> dict:
    """Recent automated mastery demotions for a child, newest first.

    A demotion is any StateEvent carrying a ``demotion_explanation`` envelope in
    its metadata (written in Phase 1). That single predicate captures both the
    attempt path and the decay path regardless of event_type. Read-only.
    """
    await _get_child_or_404(db, child_id, user.household_id)

    base = select(StateEvent).where(
        StateEvent.child_id == child_id,
        StateEvent.household_id == user.household_id,
        StateEvent.metadata_.has_key("demotion_explanation"),
    )
    total_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = total_result.scalar() or 0
    result = await db.execute(
        base.order_by(StateEvent.created_at.desc()).offset(pagination.skip).limit(pagination.limit)
    )
    items = [
        DemotionFeedItem(
            id=e.id,
            node_id=e.node_id,
            event_type=e.event_type,
            from_state=e.from_state,
            to_state=e.to_state,
            trigger=e.trigger,
            created_at=e.created_at,
            explanation=(e.metadata_ or {}).get("demotion_explanation") or {},
        )
        for e in result.scalars().all()
    ]
    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@router.post(
    "/children/{child_id}/nodes/{node_id}/mastery-override",
    response_model=MasteryOverrideResponse,
)
async def override_mastery_demotion(
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    body: MasteryOverrideRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("write")),
) -> MasteryOverrideResponse:
    """Parent override of an automated mastery demotion.

    Restores the node to the chosen level with a recorded reason, dual-logged to
    an immutable GovernanceEvent (the audit decision) and a StateEvent (the
    append-only state history), mirroring the blocked-node unlock override. A
    no-op (target equal to the current level) is recorded as a reaffirmation,
    not rejected.
    """
    await _get_child_or_404(db, child_id, user.household_id)

    # Validate the node exists and belongs to the household (mirror the
    # blocked-node override's LearningNode lookup).
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

    # Log the parent decision as an immutable GovernanceEvent (audit),
    # through the hashed chain logger.
    from app.services.governance import log_governance_event

    gov_event = await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        "child_node_state",
        node_id,
        reason=body.reason,
        metadata={
            "child_id": str(child_id),
            "override_type": "mastery_demotion_reversal",
            "target_level": body.target_level.value,
        },
    )

    # Apply the ChildNodeState change + append the override StateEvent.
    override = await apply_mastery_override(
        db,
        child_id,
        user.household_id,
        node_id,
        body.target_level,
        body.reason,
        user.id,
    )

    await db.commit()

    return MasteryOverrideResponse(
        governance_event_id=gov_event.id,
        state_event_id=override["state_event_id"],
        child_id=child_id,
        node_id=node_id,
        new_mastery_level=override["new_level"],
        message=f"Node '{node.title}' mastery set to {override['new_level'].value} via parent override",
    )


@router.post(
    "/children/{child_id}/supervision-attestation",
    response_model=SupervisionAttestationResponse,
    status_code=201,
)
async def attest_supervision(
    child_id: uuid.UUID,
    body: SupervisionAttestationRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("owner", "co_parent")),
    _child: Child = Depends(require_child_access("write")),
) -> SupervisionAttestationResponse:
    """Parent attestation that the qualified human a hazardous node names
    is physically present at the work, today, for this child.

    The runtime presence gate in services/learning_context.py refuses
    to surface a node flagged by
    requires_qualified_human_present_at_runtime until an unexpired
    attestation exists. Attestations are per child, per node, per day:
    expires_at is the household-local end of day, never longer, so
    there are no standing waivers. Only parent-scoped parent roles can
    attest (require_role rejects child-scoped tokens outright), and the
    attestation is hash-chained as a governance event.
    """
    await _get_child_or_404(db, child_id, user.household_id)

    node_result = await db.execute(
        select(LearningNode).where(
            LearningNode.id == body.node_id,
            LearningNode.household_id == user.household_id,
            LearningNode.is_active == True,  # noqa: E712
        )
    )
    node = node_result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    # An attestation only means something on a node that requires the
    # runtime presence check; attesting anything else is a client error.
    if not requires_qualified_human_present_at_runtime(node.content):
        raise HTTPException(
            status_code=400,
            detail="Node does not require a qualified human present at runtime",
        )

    household_result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = household_result.scalar_one()
    now = datetime.now(UTC)
    expires_at = local_end_of_day(household.timezone, now)

    attestation = SupervisionAttestation(
        household_id=user.household_id,
        child_id=child_id,
        node_id=node.id,
        attested_by=user.id,
        role_claimed=body.role_claimed,
        attested_at=now,
        expires_at=expires_at,
        note=body.note,
    )
    db.add(attestation)
    await db.flush()

    from app.services.governance import log_governance_event

    gov_event = await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.approve,
        "supervision_attested",
        node.id,
        reason=body.note or f"Qualified human attested present: {body.role_claimed}",
        metadata={
            "child_id": str(child_id),
            "node_id": str(node.id),
            "attestation_id": str(attestation.id),
            "role_claimed": body.role_claimed,
            "expires_at": expires_at.isoformat(),
        },
    )

    await db.commit()

    return SupervisionAttestationResponse(
        id=attestation.id,
        governance_event_id=gov_event.id,
        child_id=child_id,
        node_id=node.id,
        role_claimed=attestation.role_claimed,
        attested_at=now,
        expires_at=expires_at,
        message=f"Qualified human presence attested for '{node.title}' until end of day",
    )


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


@router.post(
    "/attempts/{attempt_id}/progress",
    response_model=AttemptResponse,
)
async def save_attempt_progress_endpoint(
    attempt_id: uuid.UUID,
    body: AttemptProgressRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AttemptResponse:
    """Save partial work on an attempt without submitting it."""
    try:
        attempt = await save_attempt_progress(
            db,
            attempt_id=attempt_id,
            household_id=user.household_id,
            notes=body.notes,
            user_id=user.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return AttemptResponse.model_validate(attempt)


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
