"""Context Assembly Service — centralized context selection, scoring, and budget management.

Each AI role has a defined context profile specifying which data sources
to fetch, their token budgets, relevance weights, and recency half-lives.
The assembly engine scores and selects the most relevant context within
a strict token budget.
"""

import logging
import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


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


# ══════════════════════════════════════════════════
# Data Fetchers
# ══════════════════════════════════════════════════
# Each returns {"text": str, "metadata": {"timestamp": datetime|None, ...}}
# All are fault-tolerant: return empty text on failure.


def _empty(ts: datetime | None = None) -> dict:
    return {"text": "", "metadata": {"timestamp": ts}}


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def fetch_current_activity(db, child_id, household_id, **kw) -> dict:
    """Current activity details for Tutor."""
    from sqlalchemy import select
    from app.models.governance import Activity
    from app.models.curriculum import LearningNode

    activity_id = kw.get("activity_id")
    if not activity_id:
        return _empty()
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    act = result.scalar_one_or_none()
    if not act:
        return _empty()

    node_title = ""
    if act.node_id:
        nr = await db.execute(select(LearningNode.title).where(LearningNode.id == act.node_id))
        row = nr.one_or_none()
        node_title = row[0] if row else ""

    atype = act.activity_type.value if hasattr(act.activity_type, "value") else str(act.activity_type)
    text = f"Activity: {act.title} | Node: {node_title} | Type: {atype} | Est: {act.estimated_minutes or '?'} min"
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_style_context(db, child_id, household_id, **kw) -> dict:
    """Style vector as formatted text."""
    from app.services.style_engine import build_style_context
    text = await build_style_context(db, child_id, household_id)
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_recent_attempts_node(db, child_id, household_id, **kw) -> dict:
    """Last 3 attempts on the current node."""
    from sqlalchemy import select
    from app.models.governance import Activity, Attempt
    from app.models.state import ChildNodeState

    node_id = kw.get("node_id")
    if not node_id:
        return _empty()

    result = await db.execute(
        select(Attempt).join(Activity, Attempt.activity_id == Activity.id).where(
            Attempt.child_id == child_id,
            Activity.node_id == node_id,
        ).order_by(Attempt.created_at.desc()).limit(3)
    )
    attempts = result.scalars().all()
    if not attempts:
        return _empty()

    # Get mastery
    sr = await db.execute(
        select(ChildNodeState).where(ChildNodeState.child_id == child_id, ChildNodeState.node_id == node_id)
    )
    state = sr.scalar_one_or_none()
    mastery = state.mastery_level.value if state and hasattr(state.mastery_level, "value") else "unknown"

    lines = [f"Recent attempts on this node (mastery: {mastery}):"]
    for a in attempts:
        dt = a.completed_at or a.created_at
        date_str = dt.strftime("%b %d") if dt else "?"
        score = f"score {a.score:.0%}" if a.score is not None else ""
        dur = f"{a.duration_minutes}m" if a.duration_minutes else ""
        lines.append(f"  {date_str}: {score} {dur}".strip())

    ts = attempts[0].created_at if attempts else None
    return {"text": "\n".join(lines), "metadata": {"timestamp": ts}}


async def fetch_recent_attempts_related(db, child_id, household_id, **kw) -> dict:
    """Recent attempts on related nodes (within DAG distance 2)."""
    from sqlalchemy import select
    from app.models.curriculum import LearningMapClosure, LearningNode
    from app.models.governance import Activity, Attempt

    node_id = kw.get("node_id")
    if not node_id:
        return _empty()

    cr = await db.execute(
        select(LearningMapClosure.ancestor_id).where(
            LearningMapClosure.descendant_id == node_id, LearningMapClosure.depth <= 2, LearningMapClosure.depth >= 1,
        )
    )
    related_ids = [r[0] for r in cr.all()]
    if not related_ids:
        return _empty()

    result = await db.execute(
        select(Attempt, Activity.title).join(Activity, Attempt.activity_id == Activity.id).where(
            Attempt.child_id == child_id, Activity.node_id.in_(related_ids),
        ).order_by(Attempt.created_at.desc()).limit(5)
    )
    rows = result.all()
    if not rows:
        return _empty()

    lines = ["Related node attempts:"]
    for att, title in rows:
        dt = (att.completed_at or att.created_at)
        date_str = dt.strftime("%b %d") if dt else "?"
        lines.append(f"  {title}: {date_str}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": rows[0][0].created_at if rows else None}}


async def fetch_frustration_signals(db, child_id, household_id, **kw) -> dict:
    """Active frustration signals from recent evaluations."""
    from sqlalchemy import select
    from app.models.intelligence import LearnerIntelligence
    from app.models.state import StateEvent

    cutoff = _now() - timedelta(days=7)

    # Check regressions
    sr = await db.execute(
        select(StateEvent).where(
            StateEvent.child_id == child_id, StateEvent.event_type == "mastery_change",
            StateEvent.created_at >= cutoff,
        ).order_by(StateEvent.created_at.desc()).limit(5)
    )
    regressions = [e for e in sr.scalars().all()
                   if e.from_state and e.to_state and e.from_state > e.to_state]

    # Check struggles from intelligence
    ir = await db.execute(
        select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id)
    )
    intel = ir.scalar_one_or_none()

    lines = []
    if regressions:
        lines.append(f"Recent regressions ({len(regressions)} in 7 days):")
        for r in regressions[:3]:
            lines.append(f"  {r.from_state} -> {r.to_state}")

    if intel and intel.subject_patterns:
        for subj, data in intel.subject_patterns.items():
            struggles = [s for s in data.get("struggles", []) if s.get("confidence", 0) >= 0.7]
            for s in struggles[:2]:
                lines.append(f"Active frustration: {subj} - {s.get('text', '?')} (confidence {s.get('confidence', 0):.1f})")

    ts = regressions[0].created_at if regressions else None
    return {"text": "\n".join(lines), "metadata": {"timestamp": ts}}


async def fetch_governance_constraints(db, child_id, household_id, **kw) -> dict:
    """Active governance rules affecting this child."""
    from sqlalchemy import select
    from app.models.governance import GovernanceRule

    result = await db.execute(
        select(GovernanceRule).where(GovernanceRule.household_id == household_id, GovernanceRule.is_active == True)
    )
    rules = result.scalars().all()
    if not rules:
        return _empty()

    lines = ["Governance rules:"]
    for r in rules[:8]:
        lines.append(f"  {r.name}: {r.description or r.rule_type.value}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_parent_observations(db, child_id, household_id, **kw) -> dict:
    """Parent observations from intelligence profile."""
    from sqlalchemy import select
    from app.models.intelligence import LearnerIntelligence

    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
    intel = result.scalar_one_or_none()
    if not intel or not intel.parent_observations:
        return _empty()

    obs = intel.parent_observations[-5:]
    lines = ["Parent observations:"]
    for o in obs:
        lines.append(f"  - {o.get('observation', '?')}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": intel.last_updated_at}}


async def fetch_attempt_transcript(db, child_id, household_id, **kw) -> dict:
    """Full attempt data for Evaluator (not compressed)."""
    from sqlalchemy import select
    from app.models.governance import Attempt
    import json

    attempt_id = kw.get("attempt_id")
    if not attempt_id:
        return _empty()
    result = await db.execute(select(Attempt).where(Attempt.id == attempt_id))
    att = result.scalar_one_or_none()
    if not att:
        return _empty()

    text = json.dumps(att.feedback or {}, indent=1, default=str)
    return {"text": text, "metadata": {"timestamp": att.completed_at or att.created_at}}


async def fetch_calibration_context(db, child_id, household_id, **kw) -> dict:
    """Calibration profile summary."""
    from sqlalchemy import select
    from app.models.calibration import CalibrationProfile

    result = await db.execute(select(CalibrationProfile).where(CalibrationProfile.child_id == child_id))
    p = result.scalar_one_or_none()
    if not p:
        return _empty()

    direction = "generous" if p.directional_bias > 0.1 else "harsh" if p.directional_bias < -0.1 else "balanced"
    text = f"Calibration: drift {p.mean_drift:.2f}, bias {direction} ({p.directional_bias:+.2f}), offset {p.recalibration_offset:+.3f}, {p.reconciled_predictions} reconciled"
    return {"text": text, "metadata": {"timestamp": p.last_computed_at}}


async def fetch_node_history(db, child_id, household_id, **kw) -> dict:
    """Historical performance on current node."""
    from sqlalchemy import select
    from app.models.state import ChildNodeState, StateEvent

    node_id = kw.get("node_id")
    if not node_id:
        return _empty()

    sr = await db.execute(
        select(ChildNodeState).where(ChildNodeState.child_id == child_id, ChildNodeState.node_id == node_id)
    )
    state = sr.scalar_one_or_none()
    if not state:
        return _empty()

    mastery = state.mastery_level.value if hasattr(state.mastery_level, "value") else str(state.mastery_level)
    lines = [f"Node history: {mastery}, {state.attempts_count} attempts, {state.time_spent_minutes}m total"]

    er = await db.execute(
        select(StateEvent).where(
            StateEvent.child_id == child_id, StateEvent.node_id == node_id,
        ).order_by(StateEvent.created_at.desc()).limit(5)
    )
    for e in er.scalars().all():
        lines.append(f"  {e.event_type.value}: {e.from_state} -> {e.to_state}")

    return {"text": "\n".join(lines), "metadata": {"timestamp": state.last_activity_at}}


async def fetch_style_evaluator(db, child_id, household_id, **kw) -> dict:
    """Style dimensions relevant to evaluation."""
    from sqlalchemy import select
    from app.models.style_vector import LearnerStyleVector

    result = await db.execute(select(LearnerStyleVector).where(LearnerStyleVector.child_id == child_id))
    v = result.scalar_one_or_none()
    if not v or v.dimensions_active == 0:
        return _empty()

    parts = []
    if v.frustration_threshold is not None:
        parts.append(f"frustration_threshold={v.frustration_threshold:.2f}")
    if v.recovery_rate is not None:
        parts.append(f"recovery_rate={v.recovery_rate:.2f}")
    if v.socratic_responsiveness is not None:
        parts.append(f"socratic={v.socratic_responsiveness:.2f}")
    return {"text": f"Style (eval): {', '.join(parts)}" if parts else "", "metadata": {"timestamp": v.last_computed_at}}


async def fetch_node_rubric(db, child_id, household_id, **kw) -> dict:
    """Rubric/mastery criteria from node content."""
    from sqlalchemy import select
    from app.models.curriculum import LearningNode

    node_id = kw.get("node_id")
    if not node_id:
        return _empty()
    result = await db.execute(select(LearningNode).where(LearningNode.id == node_id))
    node = result.scalar_one_or_none()
    if not node or not node.content:
        return _empty()

    content = node.content
    lines = []
    ac = content.get("assessment_criteria", {})
    if ac:
        for key in ("mastery_indicators", "proficiency_indicators", "developing_indicators"):
            indicators = ac.get(key, [])
            if indicators:
                lines.append(f"{key}: {', '.join(indicators[:3])}")
    if content.get("learning_objectives"):
        lines.append(f"Objectives: {', '.join(content['learning_objectives'][:3])}")

    return {"text": "\n".join(lines) if lines else "", "metadata": {"timestamp": _now()}}


async def fetch_fsrs_snapshot(db, child_id, household_id, **kw) -> dict:
    """FSRS state for all enrolled nodes."""
    from sqlalchemy import select
    from app.models.state import ChildNodeState, FSRSCard
    from app.models.curriculum import LearningNode

    sr = await db.execute(
        select(ChildNodeState).where(ChildNodeState.child_id == child_id, ChildNodeState.household_id == household_id)
    )
    states = sr.scalars().all()
    if not states:
        return _empty()

    node_ids = [s.node_id for s in states]
    nr = await db.execute(select(LearningNode.id, LearningNode.title).where(LearningNode.id.in_(node_ids)))
    titles = {r[0]: r[1] for r in nr.all()}

    cr = await db.execute(select(FSRSCard).where(FSRSCard.child_id == child_id, FSRSCard.node_id.in_(node_ids)))
    cards = {c.node_id: c for c in cr.scalars().all()}

    lines = [f"FSRS snapshot ({len(states)} nodes):"]
    for s in states[:20]:
        mastery = s.mastery_level.value if hasattr(s.mastery_level, "value") else str(s.mastery_level)
        card = cards.get(s.node_id)
        due = card.due.strftime("%b %d") if card and card.due else "n/a"
        title = titles.get(s.node_id, "?")[:30]
        lines.append(f"  {title}: {mastery}, due {due}")

    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_retention_schedule(db, child_id, household_id, **kw) -> dict:
    """Nodes due for review within 7 days."""
    from sqlalchemy import select
    from app.models.state import FSRSCard
    from app.models.curriculum import LearningNode
    from app.services.state_engine import compute_retrievability

    cutoff = _now() + timedelta(days=7)
    cr = await db.execute(
        select(FSRSCard).where(FSRSCard.child_id == child_id, FSRSCard.due <= cutoff).order_by(FSRSCard.due)
    )
    cards = cr.scalars().all()
    if not cards:
        return {"text": "No reviews due in next 7 days.", "metadata": {"timestamp": _now()}}

    node_ids = [c.node_id for c in cards]
    nr = await db.execute(select(LearningNode.id, LearningNode.title).where(LearningNode.id.in_(node_ids)))
    titles = {r[0]: r[1] for r in nr.all()}

    lines = [f"Review due ({len(cards)} nodes):"]
    for c in cards[:15]:
        title = titles.get(c.node_id, "?")[:30]
        ret = compute_retrievability(c)
        ret_str = f"{ret:.0%}" if ret is not None else "?"
        due_str = c.due.strftime("%b %d") if c.due else "?"
        lines.append(f"  {title}: ret {ret_str}, due {due_str}")

    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_pace_metrics(db, child_id, household_id, **kw) -> dict:
    """Pace trends for planner."""
    from sqlalchemy import select
    from app.models.intelligence import LearnerIntelligence

    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
    intel = result.scalar_one_or_none()
    if not intel or not intel.pace_trends:
        return _empty()

    pace = intel.pace_trends
    rate = pace.get("overall_mastery_rate", "?")
    subj = pace.get("subject_rates", {})
    subj_str = ", ".join(f"{s}: {r}" for s, r in subj.items()) if subj else "no data"
    text = f"Pace: {rate} overall mastery rate. By subject: {subj_str}"
    return {"text": text, "metadata": {"timestamp": intel.last_updated_at}}


async def fetch_governance_rules(db, child_id, household_id, **kw) -> dict:
    """Full governance rule set for planner."""
    from sqlalchemy import select
    from app.models.governance import GovernanceRule
    import json

    result = await db.execute(
        select(GovernanceRule).where(GovernanceRule.household_id == household_id, GovernanceRule.is_active == True)
    )
    rules = result.scalars().all()
    if not rules:
        return _empty()

    lines = ["Active governance rules:"]
    for r in rules[:10]:
        rtype = r.rule_type.value if hasattr(r.rule_type, "value") else str(r.rule_type)
        params = json.dumps(r.parameters, default=str) if r.parameters else "{}"
        lines.append(f"  [{rtype}] {r.name}: {params[:80]}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_family_planner_context(db, child_id, household_id, **kw) -> dict:
    """Planner-specific family intelligence."""
    from app.services.family_intelligence import build_planner_scaffolding_context
    text = await build_planner_scaffolding_context(db, child_id, household_id)
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_previous_week_signals(db, child_id, household_id, **kw) -> dict:
    """Summary of last week's evaluator signals."""
    from sqlalchemy import select, func
    from app.models.calibration import EvaluatorPrediction

    cutoff = _now() - timedelta(days=7)
    result = await db.execute(
        select(EvaluatorPrediction).where(
            EvaluatorPrediction.child_id == child_id, EvaluatorPrediction.created_at >= cutoff,
        )
    )
    preds = result.scalars().all()
    if not preds:
        return {"text": "No evaluator signals last week.", "metadata": {"timestamp": _now()}}

    confs = [p.predicted_confidence for p in preds]
    reconciled = [p for p in preds if p.actual_outcome is not None]
    drifts = [p.drift_score for p in reconciled if p.drift_score is not None]
    avg_conf = sum(confs) / len(confs) if confs else 0
    avg_drift = sum(drifts) / len(drifts) if drifts else 0

    text = f"Last week: {len(preds)} predictions, avg confidence {avg_conf:.2f}, {len(reconciled)} reconciled, avg drift {avg_drift:.2f}"
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_intelligence_summary(db, child_id, household_id, **kw) -> dict:
    """Intelligence context summary."""
    from app.services.intelligence import get_intelligence_context
    ctx = await get_intelligence_context(db, child_id, household_id)
    if not ctx:
        return _empty()

    lines = []
    if ctx.get("engagement"):
        eng = ctx["engagement"]
        lines.append(f"Focus: {eng.get('avg_focus_minutes', '?')}m avg, best time: {eng.get('best_time_of_day', '?')}")
    if ctx.get("pace"):
        lines.append(f"Pace: mastery rate {ctx['pace'].get('overall_mastery_rate', '?')}")
    if ctx.get("observation_count"):
        lines.append(f"Observations: {ctx['observation_count']}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_weekly_events(db, child_id, household_id, **kw) -> dict:
    """All state events from past week for Advisor."""
    from sqlalchemy import select
    from app.models.state import StateEvent

    cutoff = _now() - timedelta(days=7)
    result = await db.execute(
        select(StateEvent).where(
            StateEvent.child_id == child_id, StateEvent.created_at >= cutoff,
        ).order_by(StateEvent.created_at.desc()).limit(30)
    )
    events = result.scalars().all()
    if not events:
        return {"text": "No state events this week.", "metadata": {"timestamp": _now()}}

    lines = [f"State events this week ({len(events)}):"]
    for e in events[:15]:
        etype = e.event_type.value if hasattr(e.event_type, "value") else str(e.event_type)
        lines.append(f"  {etype}: {e.from_state} -> {e.to_state}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": events[0].created_at if events else None}}


async def fetch_weekly_signals(db, child_id, household_id, **kw) -> dict:
    """Evaluator signals from past week for Advisor."""
    return await fetch_previous_week_signals(db, child_id, household_id, **kw)


async def fetch_style_trends(db, child_id, household_id, **kw) -> dict:
    """Style vector with trend context for Advisor."""
    return await fetch_style_context(db, child_id, household_id, **kw)


async def fetch_family_context(db, child_id, household_id, **kw) -> dict:
    """Family intelligence for Advisor."""
    from app.services.family_intelligence import build_family_context
    text = await build_family_context(db, household_id)
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_governance_week(db, child_id, household_id, **kw) -> dict:
    """Governance events from past week for Advisor."""
    from sqlalchemy import select
    from app.models.governance import GovernanceEvent

    cutoff = _now() - timedelta(days=7)
    result = await db.execute(
        select(GovernanceEvent).where(
            GovernanceEvent.household_id == household_id, GovernanceEvent.created_at >= cutoff,
        ).order_by(GovernanceEvent.created_at.desc()).limit(10)
    )
    events = result.scalars().all()
    if not events:
        return {"text": "No governance events this week.", "metadata": {"timestamp": _now()}}

    lines = [f"Governance events ({len(events)}):"]
    for e in events[:8]:
        action = e.action.value if hasattr(e.action, "value") else str(e.action)
        lines.append(f"  {action} {e.target_type}: {e.reason or ''}"[:80])
    return {"text": "\n".join(lines), "metadata": {"timestamp": events[0].created_at if events else None}}


async def fetch_retention_summary(db, child_id, household_id, **kw) -> dict:
    """Aggregate retention stats for Advisor."""
    from sqlalchemy import select, func
    from app.models.state import FSRSCard

    result = await db.execute(
        select(func.count(), func.avg(FSRSCard.stability)).where(FSRSCard.child_id == child_id)
    )
    row = result.one_or_none()
    if not row or row[0] == 0:
        return _empty()
    text = f"Retention: {row[0]} cards, avg stability {row[1]:.1f} days" if row[1] else f"Retention: {row[0]} cards"
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_intelligence_full(db, child_id, household_id, **kw) -> dict:
    """Full intelligence context for Advisor."""
    from app.services.intelligence import get_intelligence_context
    import json
    ctx = await get_intelligence_context(db, child_id, household_id)
    if not ctx:
        return _empty()
    text = json.dumps(ctx, indent=1, default=str)
    return {"text": text, "metadata": {"timestamp": _now()}}


async def fetch_parent_goals(db, child_id, household_id, **kw) -> dict:
    """Education plan goals for Cartographer."""
    from sqlalchemy import select
    from app.models.identity import Household

    result = await db.execute(select(Household).where(Household.id == household_id))
    h = result.scalar_one_or_none()
    if not h or not h.philosophical_profile:
        return _empty()

    phil = h.philosophical_profile
    lines = ["Parent educational goals:"]
    if phil.get("primary_philosophy"):
        lines.append(f"  Philosophy: {phil['primary_philosophy']}")
    for g in phil.get("custom_constraints", [])[:5]:
        if g:
            lines.append(f"  Goal: {g}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_child_profile(db, child_id, household_id, **kw) -> dict:
    """Child age, grade, preferences for Cartographer."""
    from sqlalchemy import select
    from app.models.identity import Child, ChildPreferences

    result = await db.execute(select(Child).where(Child.id == child_id))
    child = result.scalar_one_or_none()
    if not child:
        return _empty()

    age = ""
    if child.date_of_birth:
        from datetime import date
        age_days = (date.today() - child.date_of_birth).days
        age = f"{age_days / 365.25:.1f} years"

    pr = await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child_id))
    prefs = pr.scalar_one_or_none()

    lines = [f"Child: {child.first_name}, age {age or '?'}, grade {child.grade_level or '?'}"]
    if prefs and prefs.learning_style:
        lines.append(f"  Style: {prefs.learning_style}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_map_structure(db, child_id, household_id, **kw) -> dict:
    """Existing learning map DAG structure for Cartographer."""
    from sqlalchemy import select
    from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode

    er = await db.execute(
        select(ChildMapEnrollment.learning_map_id).where(
            ChildMapEnrollment.child_id == child_id, ChildMapEnrollment.is_active == True,
        )
    )
    map_ids = [r[0] for r in er.all()]
    if not map_ids:
        return _empty()

    lines = ["Enrolled maps:"]
    for mid in map_ids[:5]:
        mr = await db.execute(select(LearningMap).where(LearningMap.id == mid))
        m = mr.scalar_one_or_none()
        if not m:
            continue
        nr = await db.execute(
            select(LearningNode).where(LearningNode.learning_map_id == mid, LearningNode.is_active == True)
        )
        nodes = nr.scalars().all()
        lines.append(f"  {m.name}: {len(nodes)} nodes")
    return {"text": "\n".join(lines), "metadata": {"timestamp": _now()}}


async def fetch_style_strategic(db, child_id, household_id, **kw) -> dict:
    """Pacing and subject affinity for Cartographer."""
    from sqlalchemy import select
    from app.models.style_vector import LearnerStyleVector

    result = await db.execute(select(LearnerStyleVector).where(LearnerStyleVector.child_id == child_id))
    v = result.scalar_one_or_none()
    if not v or v.dimensions_active == 0:
        return _empty()

    parts = []
    if v.pacing_preference is not None:
        parts.append(f"pacing={v.pacing_preference:+.1f}")
    if v.subject_affinity_map:
        aff = ", ".join(f"{s}={sc:.2f}" for s, sc in sorted(v.subject_affinity_map.items(), key=lambda x: -x[1])[:5])
        parts.append(f"affinities: {aff}")
    return {"text": f"Strategy: {'; '.join(parts)}" if parts else "", "metadata": {"timestamp": v.last_computed_at}}


async def fetch_material_effectiveness(db, child_id, household_id, **kw) -> dict:
    """Family-level material effectiveness for Cartographer."""
    from sqlalchemy import select
    from app.models.family_insight import FamilyInsight
    from app.models.enums import FamilyPatternType

    result = await db.execute(
        select(FamilyInsight).where(
            FamilyInsight.household_id == household_id,
            FamilyInsight.pattern_type == FamilyPatternType.material_effectiveness,
        ).order_by(FamilyInsight.confidence.desc()).limit(3)
    )
    insights = result.scalars().all()
    if not insights:
        return _empty()

    lines = ["Material effectiveness insights:"]
    for i in insights:
        lines.append(f"  {i.recommendation[:80]}")
    return {"text": "\n".join(lines), "metadata": {"timestamp": insights[0].created_at if insights else None}}


async def fetch_subject_affinity(db, child_id, household_id, **kw) -> dict:
    """Subject affinity map from style vector."""
    from sqlalchemy import select
    from app.models.style_vector import LearnerStyleVector

    result = await db.execute(select(LearnerStyleVector).where(LearnerStyleVector.child_id == child_id))
    v = result.scalar_one_or_none()
    if not v or not v.subject_affinity_map:
        return _empty()

    aff = ", ".join(f"{s}: {sc:.2f}" for s, sc in sorted(v.subject_affinity_map.items(), key=lambda x: -x[1]))
    return {"text": f"Subject affinities: {aff}", "metadata": {"timestamp": v.last_computed_at}}


# ══════════════════════════════════════════════════
# Fetcher Registry
# ══════════════════════════════════════════════════

FETCHER_MAP: dict[str, callable] = {
    "fetch_current_activity": fetch_current_activity,
    "fetch_style_context": fetch_style_context,
    "fetch_recent_attempts_node": fetch_recent_attempts_node,
    "fetch_recent_attempts_related": fetch_recent_attempts_related,
    "fetch_frustration_signals": fetch_frustration_signals,
    "fetch_governance_constraints": fetch_governance_constraints,
    "fetch_parent_observations": fetch_parent_observations,
    "fetch_attempt_transcript": fetch_attempt_transcript,
    "fetch_calibration_context": fetch_calibration_context,
    "fetch_node_history": fetch_node_history,
    "fetch_style_evaluator": fetch_style_evaluator,
    "fetch_node_rubric": fetch_node_rubric,
    "fetch_fsrs_snapshot": fetch_fsrs_snapshot,
    "fetch_retention_schedule": fetch_retention_schedule,
    "fetch_pace_metrics": fetch_pace_metrics,
    "fetch_governance_rules": fetch_governance_rules,
    "fetch_family_planner_context": fetch_family_planner_context,
    "fetch_previous_week_signals": fetch_previous_week_signals,
    "fetch_intelligence_summary": fetch_intelligence_summary,
    "fetch_weekly_events": fetch_weekly_events,
    "fetch_weekly_signals": fetch_weekly_signals,
    "fetch_style_trends": fetch_style_trends,
    "fetch_family_context": fetch_family_context,
    "fetch_governance_week": fetch_governance_week,
    "fetch_retention_summary": fetch_retention_summary,
    "fetch_intelligence_full": fetch_intelligence_full,
    "fetch_parent_goals": fetch_parent_goals,
    "fetch_child_profile": fetch_child_profile,
    "fetch_map_structure": fetch_map_structure,
    "fetch_style_strategic": fetch_style_strategic,
    "fetch_material_effectiveness": fetch_material_effectiveness,
    "fetch_subject_affinity": fetch_subject_affinity,
}


# ══════════════════════════════════════════════════
# Assembly Engine
# ══════════════════════════════════════════════════


async def assemble_context(
    db,
    role: str,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    **kwargs,
) -> dict:
    """Assemble the complete context for an AI role within token budget.

    Returns:
        {"context_text": str, "sources_used": list, "tokens_used": int,
         "tokens_budget": int, "sources_truncated": list, "sources_failed": list}
    """
    profile = ROLE_PROFILES.get(role)
    if not profile:
        return {
            "context_text": "", "sources_used": [], "tokens_used": 0,
            "tokens_budget": 0, "sources_truncated": [], "sources_failed": [],
        }

    # 1. Fetch all sources
    fetched: list[ScoredContext] = []
    failed: list[str] = []

    for source in profile.sources:
        fetcher = FETCHER_MAP.get(source.query_fn)
        if not fetcher:
            logger.warning("No fetcher for %s", source.query_fn)
            failed.append(source.name)
            continue

        try:
            result = await fetcher(db, child_id, household_id, **kwargs)
            text = result.get("text", "")
            if not text:
                continue

            metadata = result.get("metadata", {})
            ts = metadata.get("timestamp")

            # 2. Score relevance
            rec = recency_score(ts, source.recency_half_life_days)
            sig = signal_strength_score(metadata) if metadata else 0.5
            rel = composite_relevance(source.relevance_weight, rec, sig)

            # Truncate to source budget
            token_est = estimate_tokens(text)
            if token_est > source.max_tokens:
                text = truncate_to_tokens(text, source.max_tokens)
                token_est = estimate_tokens(text)

            fetched.append(ScoredContext(
                source_name=source.name,
                text=text,
                token_estimate=token_est,
                relevance_score=rel,
                required=source.required,
            ))
        except Exception:
            logger.warning("Fetcher %s failed for child %s", source.query_fn, child_id, exc_info=True)
            failed.append(source.name)

    # 3. Sort: required first, then by relevance
    required = [s for s in fetched if s.required]
    optional = sorted([s for s in fetched if not s.required], key=lambda s: -s.relevance_score)

    # 4. Build context within budget
    budget = profile.total_token_budget
    used = 0
    parts: list[str] = []
    sources_used: list[str] = []
    sources_truncated: list[str] = []

    for ctx in required + optional:
        if used >= budget:
            break

        remaining = budget - used
        if ctx.token_estimate <= remaining:
            parts.append(ctx.text)
            used += ctx.token_estimate
            sources_used.append(ctx.source_name)
        elif remaining >= 50:
            # Truncate to fit
            truncated = truncate_to_tokens(ctx.text, remaining)
            parts.append(truncated)
            used += estimate_tokens(truncated)
            sources_used.append(ctx.source_name)
            sources_truncated.append(ctx.source_name)
        # else: skip — not enough room

    context_text = "\n\n".join(p for p in parts if p)

    return {
        "context_text": context_text,
        "sources_used": sources_used,
        "tokens_used": used,
        "tokens_budget": budget,
        "sources_truncated": sources_truncated,
        "sources_failed": failed,
    }
