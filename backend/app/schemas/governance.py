"""Pydantic v2 schemas for Parent Governance + AI integration."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.enums import GovernanceAction, PlanStatus, RuleScope, RuleTier, RuleType

# ── Governance Rules ──


class GovernanceRuleCreate(BaseModel):
    rule_type: RuleType
    tier: RuleTier = RuleTier.policy
    scope: RuleScope = RuleScope.household
    scope_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    parameters: dict = Field(default_factory=dict)
    priority: int = 0
    confirm_constitutional: bool = False
    effective_from: date | None = None
    effective_until: date | None = None
    trigger_conditions: dict | None = None


class GovernanceRuleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    parameters: dict | None = None
    priority: int | None = None
    is_active: bool | None = None
    confirm_constitutional: bool = False
    reason: str | None = None


class GovernanceRuleResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    rule_type: RuleType
    tier: RuleTier
    scope: RuleScope
    scope_id: uuid.UUID | None
    name: str
    description: str | None
    parameters: dict
    is_active: bool
    priority: int
    effective_from: date | None
    effective_until: date | None
    trigger_conditions: dict | None
    created_at: datetime


class GovernanceEventResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    user_id: uuid.UUID | None
    action: GovernanceAction
    target_type: str
    target_id: uuid.UUID
    reason: str | None
    metadata_: dict | None = None
    created_at: datetime


# ── Plans ──


class PlanGenerateRequest(BaseModel):
    week_start: date
    daily_minutes: int = Field(default=120, ge=15, le=480)


class PlanResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    child_id: uuid.UUID
    name: str
    description: str | None
    status: PlanStatus
    start_date: date | None
    end_date: date | None
    ai_generated: bool
    ai_run_id: uuid.UUID | None
    created_at: datetime


class ActivityInPlan(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    title: str
    activity_type: str
    description: str | None
    estimated_minutes: int | None
    status: str
    scheduled_date: date | None
    node_id: uuid.UUID | None
    sort_order: int


class PlanDetailResponse(PlanResponse):
    activities: list[ActivityInPlan]


class ActivityApproveReject(BaseModel):
    reason: str | None = None


# ── AI Runs ──


class AIRunResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    run_type: str
    status: str
    model_used: str | None
    input_tokens: int | None
    output_tokens: int | None
    input_data: dict | None
    output_data: dict | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


# ── Tutor ──


class TutorMessageRequest(BaseModel):
    child_id: uuid.UUID | None = None
    message: str = Field(min_length=1, max_length=2000)
    conversation_history: list[dict] | None = None
    # Sprint v2 Prompt 3: when true, ask the model for brevity and
    # enforce a hard 1-2 sentence cap on the response server-side
    # before streaming back to the client.
    voice_mode: bool = False


class TutorMessageResponse(BaseModel):
    message: str
    hints: list[str]
    encouragement: bool
    ai_run_id: uuid.UUID


# ── Evaluator ──


class EvaluatorResult(BaseModel):
    quality_rating: int = Field(ge=1, le=5)
    confidence_score: float = Field(ge=0.0, le=1.0)
    strengths: list[str]
    areas_for_improvement: list[str]
    evidence_summary: str
    ai_run_id: uuid.UUID


# ── Cartographer ──


class CartographerCalibrateRequest(BaseModel):
    learning_map_id: uuid.UUID
    parent_goals: str = ""
    notes: str = ""


class CartographerRecommendation(BaseModel):
    ai_run_id: uuid.UUID
    difficulty_adjustments: list[dict]
    suggested_additions: list[dict]
    suggested_removals: list[dict]
    estimated_weeks: int
    rationale: str


# ── Advisor ──


class AdvisorReportResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    child_id: uuid.UUID
    report_type: str
    period_start: date
    period_end: date
    content: dict
    recommendations: list | None
    parent_reviewed: bool
    created_at: datetime
