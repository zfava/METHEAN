"""Pydantic v2 schemas for Curriculum Architecture (System 1)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import EdgeRelation, MasteryLevel, NodeType

# ── Subject schemas ──


class SubjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    color: str | None = Field(default=None, max_length=7, pattern=r"^#[0-9a-fA-F]{6}$")
    icon: str | None = Field(default=None, max_length=50)
    sort_order: int = 0


class SubjectResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    name: str
    description: str | None
    color: str | None
    icon: str | None
    is_active: bool
    sort_order: int
    created_at: datetime


# ── Learning Map schemas ──


class LearningMapCreate(BaseModel):
    subject_id: uuid.UUID
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class LearningMapUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    is_published: bool | None = None


class LearningMapResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    subject_id: uuid.UUID
    name: str
    description: str | None
    version: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class LearningMapDetailResponse(LearningMapResponse):
    nodes: list["NodeResponse"]
    edges: list["EdgeResponse"]


# ── Node schemas ──


class NodeCreate(BaseModel):
    node_type: NodeType
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    content: dict | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    sort_order: int = 0


class NodeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    content: dict | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    sort_order: int | None = None
    node_type: NodeType | None = None


class NodeResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    learning_map_id: uuid.UUID
    household_id: uuid.UUID
    node_type: NodeType
    title: str
    description: str | None
    content: dict | None
    estimated_minutes: int | None
    sort_order: int
    is_active: bool
    created_at: datetime


# ── Edge schemas ──


class EdgeCreate(BaseModel):
    from_node_id: uuid.UUID
    to_node_id: uuid.UUID
    relation: EdgeRelation = EdgeRelation.prerequisite
    weight: float = Field(default=1.0, ge=0.0)


class EdgeResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    learning_map_id: uuid.UUID
    from_node_id: uuid.UUID
    to_node_id: uuid.UUID
    relation: EdgeRelation
    weight: float
    created_at: datetime


# ── Child Map State schemas ──


class NodeStateStatus(BaseModel):
    """Per-node status for a child in a map."""

    node_id: uuid.UUID
    node_type: NodeType
    title: str
    mastery_level: MasteryLevel
    status: str  # "available", "blocked", "mastered", "in_progress"
    is_unlocked: bool
    prerequisites_met: bool
    prerequisite_node_ids: list[uuid.UUID]
    attempts_count: int
    time_spent_minutes: int


class ChildMapStateResponse(BaseModel):
    child_id: uuid.UUID
    learning_map_id: uuid.UUID
    map_name: str
    enrolled: bool
    progress_pct: float
    nodes: list[NodeStateStatus]


# ── Enrollment schemas ──


class EnrollmentCreate(BaseModel):
    learning_map_id: uuid.UUID


class EnrollmentResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    child_id: uuid.UUID
    household_id: uuid.UUID
    learning_map_id: uuid.UUID
    enrolled_at: datetime
    enrolled_at_version: int
    is_active: bool
    progress_pct: float


# ── Override schemas ──


class OverrideRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=1000)


class OverrideResponse(BaseModel):
    governance_event_id: uuid.UUID
    node_id: uuid.UUID
    child_id: uuid.UUID
    message: str


# ── Template schemas ──


class TemplateInfo(BaseModel):
    template_id: str
    name: str
    description: str
    subject_count: int
    node_count: int


class TemplateCopyResponse(BaseModel):
    learning_map_id: uuid.UUID
    subject_id: uuid.UUID
    name: str
    node_count: int
    edge_count: int
