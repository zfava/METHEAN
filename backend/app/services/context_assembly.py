"""Context Assembly Service — centralized context selection, scoring, and budget management.

Each AI role has a defined context profile specifying which data sources
to fetch, their token budgets, relevance weights, and recency half-lives.
The assembly engine scores and selects the most relevant context within
a strict token budget.

This module defines the profiles and scoring utilities. The data fetchers
and assembly engine are in context_fetchers.py (16B).
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone


# ── Data Structures ──


@dataclass
class ContextSource:
    """Defines a single data source for an AI role's context."""
    name: str                    # e.g. "recent_attempts", "style_vector"
    query_fn: str                # Name of the async function to call
    max_tokens: int              # Token budget for this source's output
    relevance_weight: float      # How important this source is for this role (0.0-1.0)
    recency_half_life_days: int  # Exponential decay half-life for recency scoring
    required: bool = False       # If True, always include even if low relevance score


@dataclass
class RoleContextProfile:
    """Defines the full context needs for an AI role."""
    role: str
    total_token_budget: int
    sources: list[ContextSource] = field(default_factory=list)


@dataclass
class ScoredContext:
    """A context block with its computed relevance score."""
    source_name: str
    text: str
    token_estimate: int
    relevance_score: float       # Combined score: weight * recency * signal
    required: bool


# ── Role Context Profiles ──


TUTOR_PROFILE = RoleContextProfile(
    role="tutor",
    total_token_budget=2000,
    sources=[
        ContextSource("current_activity", "fetch_current_activity", 400, 1.0, 1, required=True),
        ContextSource("style_vector", "fetch_style_context", 300, 0.9, 90, required=True),
        ContextSource("recent_attempts_same_node", "fetch_recent_attempts_node", 400, 0.95, 14),
        ContextSource("recent_attempts_related", "fetch_recent_attempts_related", 300, 0.7, 14),
        ContextSource("active_frustration_signals", "fetch_frustration_signals", 200, 0.85, 7),
        ContextSource("governance_constraints", "fetch_governance_constraints", 200, 0.8, 90, required=True),
        ContextSource("parent_observations", "fetch_parent_observations", 200, 0.6, 90),
    ],
)

EVALUATOR_PROFILE = RoleContextProfile(
    role="evaluator",
    total_token_budget=3000,
    sources=[
        ContextSource("full_attempt_transcript", "fetch_attempt_transcript", 1200, 1.0, 1, required=True),
        ContextSource("calibration_profile", "fetch_calibration_context", 300, 0.9, 90, required=True),
        ContextSource("historical_performance_node", "fetch_node_history", 400, 0.85, 30),
        ContextSource("style_vector_relevant", "fetch_style_evaluator", 200, 0.7, 90),
        ContextSource("node_rubric", "fetch_node_rubric", 300, 0.95, 365, required=True),
        ContextSource("governance_constraints", "fetch_governance_constraints", 200, 0.6, 90),
    ],
)

PLANNER_PROFILE = RoleContextProfile(
    role="planner",
    total_token_budget=4000,
    sources=[
        ContextSource("fsrs_state_snapshot", "fetch_fsrs_snapshot", 600, 1.0, 1, required=True),
        ContextSource("retention_schedule", "fetch_retention_schedule", 400, 0.95, 7, required=True),
        ContextSource("style_vector", "fetch_style_context", 300, 0.9, 90, required=True),
        ContextSource("pace_metrics", "fetch_pace_metrics", 300, 0.85, 30),
        ContextSource("governance_rules", "fetch_governance_rules", 400, 0.9, 90, required=True),
        ContextSource("family_insights", "fetch_family_planner_context", 300, 0.7, 30),
        ContextSource("previous_week_signals", "fetch_previous_week_signals", 400, 0.8, 14),
        ContextSource("intelligence_summary", "fetch_intelligence_summary", 300, 0.6, 30),
    ],
)

ADVISOR_PROFILE = RoleContextProfile(
    role="advisor",
    total_token_budget=6000,
    sources=[
        ContextSource("weekly_state_events", "fetch_weekly_events", 1000, 1.0, 7, required=True),
        ContextSource("evaluator_signals_week", "fetch_weekly_signals", 800, 0.95, 7, required=True),
        ContextSource("style_vector_with_trends", "fetch_style_trends", 400, 0.85, 90),
        ContextSource("family_patterns", "fetch_family_context", 400, 0.8, 30),
        ContextSource("calibration_profile", "fetch_calibration_context", 300, 0.7, 90),
        ContextSource("governance_events_week", "fetch_governance_week", 400, 0.75, 7),
        ContextSource("fsrs_retention_summary", "fetch_retention_summary", 300, 0.7, 30),
        ContextSource("intelligence_full", "fetch_intelligence_full", 400, 0.6, 30),
        ContextSource("parent_observations", "fetch_parent_observations", 300, 0.65, 90),
    ],
)

CARTOGRAPHER_PROFILE = RoleContextProfile(
    role="cartographer",
    total_token_budget=3000,
    sources=[
        ContextSource("parent_goals", "fetch_parent_goals", 500, 1.0, 365, required=True),
        ContextSource("child_age_level", "fetch_child_profile", 200, 0.95, 365, required=True),
        ContextSource("existing_map_structure", "fetch_map_structure", 600, 0.9, 90),
        ContextSource("style_vector_strategic", "fetch_style_strategic", 300, 0.7, 90),
        ContextSource("family_material_effectiveness", "fetch_material_effectiveness", 300, 0.6, 90),
        ContextSource("subject_affinity", "fetch_subject_affinity", 200, 0.65, 30),
    ],
)

ROLE_PROFILES: dict[str, RoleContextProfile] = {
    "tutor": TUTOR_PROFILE,
    "evaluator": EVALUATOR_PROFILE,
    "planner": PLANNER_PROFILE,
    "advisor": ADVISOR_PROFILE,
    "cartographer": CARTOGRAPHER_PROFILE,
}


# ── Token Estimation ──


def estimate_tokens(text: str) -> int:
    """Rough token estimate. 1 token ~ 4 characters for English text."""
    return max(1, len(text) // 4)


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to approximately fit within a token budget."""
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    # Truncate at last newline before budget to avoid mid-line cuts
    truncated = text[:max_chars]
    last_nl = truncated.rfind("\n")
    if last_nl > max_chars * 0.5:
        truncated = truncated[:last_nl]
    return truncated + "\n[...truncated]"


# ── Relevance Scoring ──


def recency_score(timestamp: datetime | None, half_life_days: int) -> float:
    """Exponential decay score based on age of data point.

    Returns 1.0 for just-now, 0.5 at half_life_days, approaches 0.0
    as age increases.
    """
    if timestamp is None:
        return 0.5  # Neutral if no timestamp
    now = datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    age_days = (now - timestamp).total_seconds() / 86400
    if age_days <= 0:
        return 1.0
    return math.exp(-0.693 * age_days / max(half_life_days, 1))


def topical_proximity_score(
    source_node_id: str | None,
    target_node_id: str | None,
    closure_distances: dict[str, int],
) -> float:
    """Score based on graph distance in curriculum DAG.

    closure_distances: precomputed dict of {node_id_str: distance_from_target}.
    """
    if source_node_id is None or target_node_id is None:
        return 0.3  # Unknown topology
    if source_node_id == target_node_id:
        return 1.0
    distance = closure_distances.get(source_node_id)
    if distance is None:
        return 0.1  # Unrelated node
    return max(0.1, 1.0 / (1 + distance))


def signal_strength_score(data_point: dict) -> float:
    """Higher score for high-impact data: drift, frustration, mastery
    transitions, governance overrides."""
    score = 0.5  # Baseline
    if data_point.get("drift_score") and data_point["drift_score"] >= 1.5:
        score += 0.3
    if data_point.get("signal_type") in ("frustration", "regression"):
        score += 0.2
    if data_point.get("is_mastery_transition"):
        score += 0.15
    if data_point.get("is_governance_override"):
        score += 0.2
    return min(1.0, score)


def composite_relevance(
    weight: float,
    recency: float,
    signal: float = 0.5,
    topology: float = 0.5,
) -> float:
    """Combine multiple relevance factors into a single score.

    Weight is the role-defined importance. Other factors modulate it.
    """
    return weight * (0.4 * recency + 0.3 * signal + 0.3 * topology)
