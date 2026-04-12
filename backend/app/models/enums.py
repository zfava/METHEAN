"""PostgreSQL-backed enums for METHEAN."""

import enum


class UserRole(enum.StrEnum):
    owner = "owner"
    co_parent = "co_parent"
    observer = "observer"


class NodeType(enum.StrEnum):
    # Academic
    root = "root"
    milestone = "milestone"
    concept = "concept"
    skill = "skill"
    # Vocational
    safety = "safety"
    knowledge = "knowledge"
    technique = "technique"
    project = "project"
    certification_prep = "certification_prep"


class EdgeRelation(enum.StrEnum):
    prerequisite = "prerequisite"
    corequisite = "corequisite"
    recommended = "recommended"


class MasteryLevel(enum.StrEnum):
    not_started = "not_started"
    emerging = "emerging"
    developing = "developing"
    proficient = "proficient"
    mastered = "mastered"


class StateEventType(enum.StrEnum):
    mastery_change = "mastery_change"
    review_completed = "review_completed"
    node_unlocked = "node_unlocked"
    node_skipped = "node_skipped"
    override = "override"


class FSRSRating(int, enum.Enum):
    again = 1
    hard = 2
    good = 3
    easy = 4


class RuleType(enum.StrEnum):
    pace_limit = "pace_limit"
    content_filter = "content_filter"
    schedule_constraint = "schedule_constraint"
    ai_boundary = "ai_boundary"
    approval_required = "approval_required"


class RuleTier(enum.StrEnum):
    constitutional = "constitutional"  # Requires ceremony to change
    policy = "policy"  # Normal CRUD


class RuleScope(enum.StrEnum):
    household = "household"
    child = "child"
    subject = "subject"
    map = "map"


class GovernanceAction(enum.StrEnum):
    approve = "approve"
    reject = "reject"
    modify = "modify"
    defer = "defer"


class PlanStatus(enum.StrEnum):
    draft = "draft"
    proposed = "proposed"
    approved = "approved"
    active = "active"
    completed = "completed"
    archived = "archived"


class ActivityType(enum.StrEnum):
    lesson = "lesson"
    practice = "practice"
    assessment = "assessment"
    review = "review"
    project = "project"
    field_trip = "field_trip"


class ActivityStatus(enum.StrEnum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"
    cancelled = "cancelled"


class AttemptStatus(enum.StrEnum):
    started = "started"
    completed = "completed"
    abandoned = "abandoned"


class ArtifactType(enum.StrEnum):
    photo = "photo"
    video = "video"
    document = "document"
    audio = "audio"
    link = "link"


class AlertSeverity(enum.StrEnum):
    info = "info"
    warning = "warning"
    action_required = "action_required"


class AlertStatus(enum.StrEnum):
    unread = "unread"
    read = "read"
    dismissed = "dismissed"
    acted_on = "acted_on"


class AIRunStatus(enum.StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class AuditAction(enum.StrEnum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    login = "login"
    logout = "logout"
    export = "export"


class FamilyPatternType(enum.StrEnum):
    shared_struggle = "shared_struggle"
    curriculum_gap = "curriculum_gap"
    pacing_divergence = "pacing_divergence"
    environmental_correlation = "environmental_correlation"
    material_effectiveness = "material_effectiveness"


class InsightStatus(enum.StrEnum):
    detected = "detected"
    notified = "notified"
    acknowledged = "acknowledged"
    acted_on = "acted_on"
    dismissed = "dismissed"


class AnomalyType(enum.StrEnum):
    broad_disengagement = "broad_disengagement"
    frustration_spike = "frustration_spike"
    performance_cliff = "performance_cliff"
    session_avoidance = "session_avoidance"


class AnomalyStatus(enum.StrEnum):
    detected = "detected"
    notified = "notified"
    acknowledged = "acknowledged"
    dismissed = "dismissed"
    resolved = "resolved"


class SensitivityLevel(enum.StrEnum):
    conservative = "conservative"
    balanced = "balanced"
    sensitive = "sensitive"
