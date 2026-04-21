"""Pydantic v2 schemas for Learner State Engine (System 2)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import MasteryLevel, StateEventType

# ── State query responses ──


class NodeStateResponse(BaseModel):
    """Full state for a single node for a child."""

    node_id: uuid.UUID
    node_title: str
    mastery_level: MasteryLevel
    is_unlocked: bool
    attempts_count: int
    time_spent_minutes: int
    last_activity_at: datetime | None
    # FSRS fields
    fsrs_due: datetime | None = None
    fsrs_stability: float | None = None
    fsrs_difficulty: float | None = None
    fsrs_retrievability: float | None = None
    fsrs_state: int | None = None  # 0=new, 1=learning, 2=review, 3=relearning


class ChildStateResponse(BaseModel):
    """Full state across all enrolled maps."""

    child_id: uuid.UUID
    nodes: list[NodeStateResponse]
    total_nodes: int
    mastered_count: int
    in_progress_count: int
    not_started_count: int


class StateEventResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    child_id: uuid.UUID
    node_id: uuid.UUID
    event_type: StateEventType
    from_state: str | None
    to_state: str | None
    trigger: str | None
    created_at: datetime


class RetentionSummaryResponse(BaseModel):
    child_id: uuid.UUID
    total_nodes: int
    mastered_count: int
    in_progress_count: int
    not_started_count: int
    decaying_count: int  # mastered but retrievability < threshold
    blocked_count: int
    average_retrievability: float | None


# ── Attempt schemas ──


class AttemptStartRequest(BaseModel):
    child_id: uuid.UUID


class AttemptSubmitRequest(BaseModel):
    duration_minutes: int | None = Field(default=None, ge=0)
    score: float | None = Field(default=None, ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0, description="Evaluator confidence 0-1")
    feedback: dict | None = None


class AttemptResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    activity_id: uuid.UUID
    household_id: uuid.UUID
    child_id: uuid.UUID
    status: str
    started_at: datetime
    completed_at: datetime | None
    duration_minutes: int | None
    score: float | None
    feedback: dict | None
    created_at: datetime


class AttemptSubmitResponse(BaseModel):
    attempt: AttemptResponse
    mastery_level: MasteryLevel
    previous_mastery: MasteryLevel
    fsrs_due: datetime | None
    fsrs_rating: int
    state_event_id: uuid.UUID
    nodes_unblocked: list[uuid.UUID]


# ── Decay job result ──


class DecayJobResult(BaseModel):
    cards_checked: int
    cards_decayed: int
    duration_ms: int
