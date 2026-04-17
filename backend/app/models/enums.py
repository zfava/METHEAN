"""PostgreSQL-backed enums for METHEAN."""

import enum


class UserRole(str, enum.Enum):
    owner = "owner"
    co_parent = "co_parent"
    observer = "observer"


class NodeType(str, enum.Enum):
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


class EdgeRelation(str, enum.Enum):
    prerequisite = "prerequisite"
    corequisite = "corequisite"
    recommended = "recommended"


class MasteryLevel(str, enum.Enum):
    not_started = "not_started"
    emerging = "emerging"
    developing = "developing"
    proficient = "proficient"
    mastered = "mastered"


class StateEventType(str, enum.Enum):
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


class RuleType(str, enum.Enum):
    pace_limit = "pace_limit"
    content_filter = "content_filter"
    schedule_constraint = "schedule_constraint"
    ai_boundary = "ai_boundary"
    approval_required = "approval_required"


class RuleTier(str, enum.Enum):
    constitutional = "constitutional"  # Requires ceremony to change
    policy = "policy"  # Normal CRUD


class RuleScope(str, enum.Enum):
    household = "household"
    child = "child"
    subject = "subject"
    map = "map"


class GovernanceAction(str, enum.Enum):
    approve = "approve"
    reject = "reject"
    modify = "modify"
    defer = "defer"


class PlanStatus(str, enum.Enum):
    draft = "draft"
    proposed = "proposed"
    approved = "approved"
    active = "active"
    completed = "completed"
    archived = "archived"


class ActivityType(str, enum.Enum):
    lesson = "lesson"
    practice = "practice"
    assessment = "assessment"
    review = "review"
    project = "project"
    field_trip = "field_trip"


class ActivityStatus(str, enum.Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"
    cancelled = "cancelled"


class AttemptStatus(str, enum.Enum):
    started = "started"
    completed = "completed"
    abandoned = "abandoned"


class ArtifactType(str, enum.Enum):
    photo = "photo"
    video = "video"
    document = "document"
    audio = "audio"
    link = "link"


class AlertSeverity(str, enum.Enum):
    info = "info"
    warning = "warning"
    action_required = "action_required"


class AlertStatus(str, enum.Enum):
    unread = "unread"
    read = "read"
    dismissed = "dismissed"
    acted_on = "acted_on"


class AIRunStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class AuditAction(str, enum.Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    login = "login"
    logout = "logout"
    export = "export"


class FamilyPatternType(str, enum.Enum):
    shared_struggle = "shared_struggle"
    curriculum_gap = "curriculum_gap"
    pacing_divergence = "pacing_divergence"
    environmental_correlation = "environmental_correlation"
    material_effectiveness = "material_effectiveness"


class InsightStatus(str, enum.Enum):
    detected = "detected"
    notified = "notified"
    acknowledged = "acknowledged"
    acted_on = "acted_on"
    dismissed = "dismissed"


class AnomalyType(str, enum.Enum):
    broad_disengagement = "broad_disengagement"
    frustration_spike = "frustration_spike"
    performance_cliff = "performance_cliff"
    session_avoidance = "session_avoidance"


class AnomalyStatus(str, enum.Enum):
    detected = "detected"
    notified = "notified"
    acknowledged = "acknowledged"
    dismissed = "dismissed"
    resolved = "resolved"


class SensitivityLevel(str, enum.Enum):
    conservative = "conservative"
    balanced = "balanced"
    sensitive = "sensitive"


class BetaFeedbackType(str, enum.Enum):
    bug = "bug"
    feature_request = "feature_request"
    usability = "usability"
    content = "content"
    general = "general"


class BetaFeedbackStatus(str, enum.Enum):
    new = "new"
    reviewed = "reviewed"
    in_progress = "in_progress"
    resolved = "resolved"
    wont_fix = "wont_fix"
