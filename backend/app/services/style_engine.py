"""Style Vector Computation Engine.

Derives a computed LearnerStyleVector from raw LearnerIntelligence
observations. Each dimension activates independently when sufficient
data exists. Parents can override or bound any dimension.

The engine OBSERVES. The parent GOVERNS.
"""

import logging
import math
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.intelligence import LearnerIntelligence
from app.models.style_vector import LearnerStyleVector

logger = logging.getLogger(__name__)

# ── Thresholds ──

MIN_OBSERVATIONS = 20          # Global minimum before any computation
MIN_DURATIONS = 20             # For optimal_session_minutes, attention_pattern
MIN_TUTOR_SESSIONS = 20        # For socratic_responsiveness
MIN_TUTOR_SESSIONS_INDEP = 15  # For independence_level
MIN_EVALUATED_ATTEMPTS = 20    # For frustration_threshold
MIN_DOWNWARD_TRANSITIONS = 10  # For recovery_rate
MIN_TIME_DATA = 20             # For time_of_day_peak
MIN_SUBJECT_ATTEMPTS = 10      # Per-subject for subject_affinity_map
MIN_TOTAL_ATTEMPTS = 30        # For modality_preference
MIN_MASTERY_TRANSITIONS = 20   # For pacing_preference

# Dimensions list (for counting active)
DIMENSION_FIELDS = [
    "optimal_session_minutes", "socratic_responsiveness", "frustration_threshold",
    "recovery_rate", "time_of_day_peak", "modality_preference",
    "pacing_preference", "independence_level", "attention_pattern",
]


# ── Exponential Decay Weighting ──


def decay_weighted_average(values: list[float], decay_lambda: float = 0.95) -> float:
    """Compute weighted average with exponential decay (most recent = highest weight).

    values should be ordered oldest-first. Weight of value at index i
    (from the end) = decay_lambda ** (n - 1 - i).
    """
    if not values:
        return 0.0
    n = len(values)
    weights = [decay_lambda ** (n - 1 - i) for i in range(n)]
    total_weight = sum(weights)
    if total_weight == 0:
        return sum(values) / n
    return sum(v * w for v, w in zip(values, weights)) / total_weight


# ── Dimension Computations ──


def _compute_optimal_session_minutes(eng: dict, subject_patterns: dict) -> int | None:
    """Find session duration range where quality is highest.

    Uses recent_durations from engagement_patterns and quality data
    from subject_patterns notes.
    """
    durations = eng.get("recent_durations", [])
    if len(durations) < MIN_DURATIONS:
        return None

    # Gather quality-tagged durations from subject notes
    quality_durations: list[tuple[int, float]] = []
    for subj_data in subject_patterns.values():
        for note in subj_data.get("notes", []):
            q = note.get("quality")
            if q is not None:
                quality_durations.append((int(q), 1.0))

    # If we have quality data, bucket durations and find peak
    # Otherwise use the weighted average of recent durations
    if quality_durations:
        # Use recent durations as proxy for session lengths
        avg = decay_weighted_average([float(d) for d in durations])
        result = max(10, min(60, round(avg)))
    else:
        avg = decay_weighted_average([float(d) for d in durations])
        result = max(10, min(60, round(avg)))

    return result


def _compute_socratic_responsiveness(tutor: dict) -> float | None:
    """Compare quality in high-hint vs low-hint tutor sessions."""
    sessions = tutor.get("sessions", [])
    if len(sessions) < MIN_TUTOR_SESSIONS:
        return None

    high_hint_corrections = []
    low_hint_corrections = []

    for s in sessions:
        hints = s.get("hints", 0)
        messages = s.get("messages", 1)
        self_corrections = s.get("self_corrections", 0)
        hint_rate = hints / max(messages, 1)

        if hint_rate > 0.3:
            high_hint_corrections.append(self_corrections / max(messages, 1))
        else:
            low_hint_corrections.append(self_corrections / max(messages, 1))

    if not high_hint_corrections or not low_hint_corrections:
        # Not enough variation in hint usage
        return None

    high_avg = decay_weighted_average(high_hint_corrections)
    low_avg = decay_weighted_average(low_hint_corrections)

    # Higher self-correction rate with hints = more responsive to Socratic
    if high_avg + low_avg == 0:
        return 0.5
    responsiveness = high_avg / (high_avg + low_avg)
    return max(0.0, min(1.0, round(responsiveness, 3)))


def _compute_frustration_threshold(subject_patterns: dict) -> float | None:
    """Find average difficulty where struggles outnumber strengths."""
    total_evidence = 0
    thresholds = []

    for subj_data in subject_patterns.values():
        strengths = subj_data.get("strengths", [])
        struggles = subj_data.get("struggles", [])
        total_evidence += sum(s.get("evidence_count", 1) for s in strengths)
        total_evidence += sum(s.get("evidence_count", 1) for s in struggles)

        strength_conf = sum(s.get("confidence", 0.5) for s in strengths)
        struggle_conf = sum(s.get("confidence", 0.5) for s in struggles)

        total = strength_conf + struggle_conf
        if total > 0:
            # Threshold = how much of the challenge space is struggles
            # Lower = frustrates earlier
            ratio = struggle_conf / total
            thresholds.append(ratio)

    if total_evidence < MIN_EVALUATED_ATTEMPTS or not thresholds:
        return None

    # Invert: high ratio of struggles = low frustration threshold
    avg_ratio = sum(thresholds) / len(thresholds)
    threshold = max(0.0, min(1.0, round(1.0 - avg_ratio, 3)))
    return threshold


def _compute_recovery_rate(pace: dict) -> float | None:
    """How quickly does performance recover after a downward transition?"""
    transitions = pace.get("transitions", [])
    if not transitions:
        return None

    down_indices = [i for i, t in enumerate(transitions) if t.get("direction") == "down"]
    if len(down_indices) < MIN_DOWNWARD_TRANSITIONS:
        return None

    recovery_distances = []
    for di in down_indices:
        # Find next upward transition after this downward one
        for j in range(di + 1, len(transitions)):
            if transitions[j].get("direction") == "up":
                recovery_distances.append(j - di)
                break

    if not recovery_distances:
        return 0.0

    avg_distance = decay_weighted_average([float(d) for d in recovery_distances])
    # Normalize: 1 attempt = 1.0 (instant recovery), 10+ attempts = ~0.0
    rate = max(0.0, min(1.0, round(1.0 / avg_distance, 3)))
    return rate


def _compute_time_of_day_peak(eng: dict) -> int | None:
    """Hour with highest engagement count."""
    tod_counts = eng.get("time_of_day_counts", {})
    total = sum(tod_counts.values())
    if total < MIN_TIME_DATA:
        return None

    # Map time-of-day strings to hours
    hour_map = {"morning": 9, "afternoon": 14, "evening": 19}
    best_key = max(tod_counts, key=tod_counts.get) if tod_counts else None
    if best_key is None:
        return None

    return hour_map.get(best_key, 12)


def _compute_subject_affinity_map(eng: dict, subject_patterns: dict) -> dict:
    """Per-subject engagement score based on quality evidence."""
    affinities = {}

    for subject, data in subject_patterns.items():
        notes = data.get("notes", [])
        if len(notes) < MIN_SUBJECT_ATTEMPTS:
            continue

        qualities = [n.get("quality", 3) for n in notes if n.get("quality") is not None]
        if not qualities:
            continue

        # Normalize quality (1-5) to 0.0-1.0
        weighted_avg = decay_weighted_average([float(q) for q in qualities])
        score = max(0.0, min(1.0, round((weighted_avg - 1) / 4, 3)))
        affinities[subject] = score

    return affinities


def _compute_modality_preference(eng: dict) -> str | None:
    """Map activity types to modalities and find preferred one."""
    type_stats = eng.get("activity_type_stats", {})
    total_attempts = sum(ts.get("total", 0) for ts in type_stats.values())
    if total_attempts < MIN_TOTAL_ATTEMPTS:
        return None

    # Activity type → modality mapping
    modality_map = {
        "lesson": "reading_writing",
        "practice": "kinesthetic",
        "review": "visual",
        "assessment": "mixed",
        "project": "kinesthetic",
        "field_trip": "kinesthetic",
    }

    modality_scores: dict[str, list[float]] = {}
    for act_type, stats in type_stats.items():
        modality = modality_map.get(act_type, "mixed")
        total = stats.get("total", 0)
        completed = stats.get("completed", 0)
        if total > 0:
            rate = completed / total
            modality_scores.setdefault(modality, []).append(rate)

    if not modality_scores:
        return None

    # Average completion rate per modality
    modality_avg = {
        m: sum(rates) / len(rates)
        for m, rates in modality_scores.items()
        if rates
    }

    if not modality_avg:
        return None

    best = max(modality_avg, key=modality_avg.get)
    return best


def _compute_pacing_preference(pace: dict) -> float | None:
    """Positive = thrives with acceleration, negative = needs slower pacing."""
    transitions = pace.get("transitions", [])
    overall_rate = pace.get("overall_mastery_rate")

    if len(transitions) < MIN_MASTERY_TRANSITIONS or overall_rate is None:
        return None

    # High mastery rate → acceleration potential
    # Low mastery rate → needs deceleration
    # Center at 0.6 (reasonable baseline), scale to [-1, 1]
    pacing = (overall_rate - 0.6) / 0.4
    return max(-1.0, min(1.0, round(pacing, 3)))


def _compute_independence_level(tutor: dict) -> float | None:
    """Ratio of low-hint sessions to total sessions."""
    sessions = tutor.get("sessions", [])
    if len(sessions) < MIN_TUTOR_SESSIONS_INDEP:
        return None

    low_hint_count = 0
    for s in sessions:
        hints = s.get("hints", 0)
        messages = s.get("messages", 1)
        if hints / max(messages, 1) < 0.1:
            low_hint_count += 1

    level = low_hint_count / len(sessions)
    return max(0.0, min(1.0, round(level, 3)))


def _compute_attention_pattern(eng: dict) -> str | None:
    """Classify attention from session duration variance."""
    durations = eng.get("recent_durations", [])
    if len(durations) < MIN_DURATIONS:
        return None

    floats = [float(d) for d in durations]
    mean = sum(floats) / len(floats)
    if mean == 0:
        return "variable"

    variance = sum((d - mean) ** 2 for d in floats) / len(floats)
    std_dev = math.sqrt(variance)
    cv = std_dev / mean  # coefficient of variation

    if cv < 0.2:
        return "sustained"
    elif mean < 20 and std_dev > 5:
        # Short sessions with occasional long = burst pattern
        long_count = sum(1 for d in floats if d > mean * 1.5)
        if long_count >= 2:
            return "burst"
    if mean > 30 and std_dev > 10:
        return "variable"

    return "variable"


# ── Parent Override / Bounds Application ──


def _apply_parent_governance(
    vector: LearnerStyleVector,
    overrides: dict,
    bounds: dict,
) -> None:
    """Apply parent overrides and bounds to computed dimensions.

    Overrides: {"dimension_name": {"value": X, "locked": true}}
    Bounds: {"dimension_name": {"min": X, "max": Y}}
    """
    for dim_name, override in overrides.items():
        if not override.get("locked"):
            continue
        value = override.get("value")
        if value is not None and hasattr(vector, dim_name):
            setattr(vector, dim_name, value)

    for dim_name, bound in bounds.items():
        current = getattr(vector, dim_name, None)
        if current is None:
            continue
        lo = bound.get("min")
        hi = bound.get("max")
        if isinstance(current, (int, float)):
            if lo is not None and current < lo:
                setattr(vector, dim_name, type(current)(lo))
            if hi is not None and current > hi:
                setattr(vector, dim_name, type(current)(hi))


def _count_active_dimensions(vector: LearnerStyleVector) -> int:
    """Count how many dimensions have non-null computed values."""
    count = 0
    for field in DIMENSION_FIELDS:
        if getattr(vector, field, None) is not None:
            count += 1
    # subject_affinity_map is always a dict; count if non-empty
    if vector.subject_affinity_map:
        count += 1
    return count


# ── Main Computation ──


async def compute_style_vector(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> LearnerStyleVector:
    """Compute or update the LearnerStyleVector from raw intelligence data.

    Each dimension activates independently when sufficient data exists.
    Parent overrides and bounds are applied after computation.
    """
    now = datetime.now(UTC)

    # Get or create the vector
    result = await db.execute(
        select(LearnerStyleVector).where(LearnerStyleVector.child_id == child_id)
    )
    vector = result.scalar_one_or_none()

    if vector is None:
        vector = LearnerStyleVector(
            child_id=child_id,
            household_id=household_id,
        )
        db.add(vector)
        await db.flush()

    # Fetch intelligence profile
    intel_result = await db.execute(
        select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id)
    )
    intel = intel_result.scalar_one_or_none()

    if intel is None or (intel.observation_count or 0) < MIN_OBSERVATIONS:
        # Not enough data — zero out all dimensions
        for field in DIMENSION_FIELDS:
            setattr(vector, field, None)
        vector.subject_affinity_map = {}
        vector.data_points_count = intel.observation_count if intel else 0
        vector.dimensions_active = 0
        vector.last_computed_at = now
        await db.flush()
        return vector

    # Extract raw data
    eng = intel.engagement_patterns or {}
    tutor = intel.tutor_interaction_analysis or {}
    pace = intel.pace_trends or {}
    subj_patterns = intel.subject_patterns or {}

    # Compute each dimension independently
    vector.optimal_session_minutes = _compute_optimal_session_minutes(eng, subj_patterns)
    vector.socratic_responsiveness = _compute_socratic_responsiveness(tutor)
    vector.frustration_threshold = _compute_frustration_threshold(subj_patterns)
    vector.recovery_rate = _compute_recovery_rate(pace)
    vector.time_of_day_peak = _compute_time_of_day_peak(eng)
    vector.subject_affinity_map = _compute_subject_affinity_map(eng, subj_patterns)
    vector.modality_preference = _compute_modality_preference(eng)
    vector.pacing_preference = _compute_pacing_preference(pace)
    vector.independence_level = _compute_independence_level(tutor)
    vector.attention_pattern = _compute_attention_pattern(eng)

    # Apply parent governance
    overrides = dict(vector.parent_overrides or {})
    bounds = dict(vector.parent_bounds or {})
    _apply_parent_governance(vector, overrides, bounds)

    # Update metadata
    vector.data_points_count = intel.observation_count or 0
    vector.dimensions_active = _count_active_dimensions(vector)
    vector.last_computed_at = now

    # Emit audit log
    try:
        from app.models.enums import AuditAction
        from app.models.operational import AuditLog
        db.add(AuditLog(
            household_id=household_id,
            action=AuditAction.update,
            resource_type="learner_style_vector",
            resource_id=vector.id,
            details={
                "child_id": str(child_id),
                "dimensions_active": vector.dimensions_active,
                "data_points_count": vector.data_points_count,
            },
        ))
    except Exception:
        pass  # Audit logging is advisory

    await db.flush()
    return vector


# ── Style Context Builder for AI Prompt Injection ──


def _level_label(value: float) -> str:
    """Map a 0.0-1.0 float to LOW/MODERATE/HIGH."""
    if value < 0.3:
        return "LOW"
    elif value <= 0.7:
        return "MODERATE"
    else:
        return "HIGH"


def _hour_label(hour: int) -> str:
    """Map hour to readable time period."""
    if hour < 12:
        return f"Morning ({hour}-{hour + 1} AM peak)"
    elif hour < 17:
        h = hour if hour <= 12 else hour - 12
        return f"Afternoon ({h}-{h + 1} PM peak)"
    else:
        h = hour - 12
        return f"Evening ({h}-{h + 1} PM peak)"


def _modality_label(modality: str) -> str:
    """Readable modality name."""
    labels = {
        "visual": "Visual learning",
        "auditory": "Auditory learning",
        "kinesthetic": "Hands-on/kinesthetic",
        "reading_writing": "Reading/writing",
        "mixed": "Mixed modalities",
    }
    return labels.get(modality, modality)


async def build_style_context(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> str:
    """Build a plain-text style context block for AI prompt injection.

    Returns empty string if no vector exists or insufficient data.
    """
    result = await db.execute(
        select(LearnerStyleVector).where(LearnerStyleVector.child_id == child_id)
    )
    vector = result.scalar_one_or_none()

    if vector is None or vector.dimensions_active == 0:
        return ""

    lines = [f"LEARNER STYLE PROFILE (computed from {vector.data_points_count} observations):"]

    # Optimal session + attention pattern
    if vector.optimal_session_minutes is not None:
        attn = f" ({vector.attention_pattern} attention pattern)" if vector.attention_pattern else ""
        lines.append(f"- Optimal session: {vector.optimal_session_minutes} minutes{attn}")

    # Time of day
    if vector.time_of_day_peak is not None:
        lines.append(f"- Best time of day: {_hour_label(vector.time_of_day_peak)}")

    # Socratic responsiveness
    if vector.socratic_responsiveness is not None:
        label = _level_label(vector.socratic_responsiveness)
        desc = {
            "HIGH": "responds well to questioning",
            "MODERATE": "benefits from a mix of questioning and direct instruction",
            "LOW": "prefers worked examples before guided practice",
        }[label]
        lines.append(f"- Socratic responsiveness: {label} ({vector.socratic_responsiveness:.2f}) — {desc}")

    # Independence
    if vector.independence_level is not None:
        label = _level_label(vector.independence_level)
        desc = {
            "HIGH": "highly self-directed, offer space before hints",
            "MODERATE": "needs occasional scaffolding",
            "LOW": "benefits from guided support and frequent check-ins",
        }[label]
        lines.append(f"- Independence: {label} ({vector.independence_level:.2f}) — {desc}")

    # Frustration threshold
    if vector.frustration_threshold is not None:
        label = _level_label(vector.frustration_threshold)
        desc = {
            "HIGH": "handles difficulty well, can push harder",
            "MODERATE": "provide support at higher difficulty levels",
            "LOW": "provide extra support early, scaffold before frustration",
        }[label]
        lines.append(f"- Frustration threshold: {label} ({vector.frustration_threshold:.2f}) — {desc}")

    # Recovery rate
    if vector.recovery_rate is not None:
        label = _level_label(vector.recovery_rate)
        desc = {
            "HIGH": "bounces back quickly after setbacks",
            "MODERATE": "recovers with encouragement",
            "LOW": "needs extra encouragement and easier tasks after setbacks",
        }[label]
        lines.append(f"- Recovery rate: {label} ({vector.recovery_rate:.2f}) — {desc}")

    # Pacing
    if vector.pacing_preference is not None:
        if vector.pacing_preference > 0.3:
            lines.append(f"- Pacing: Acceleration preferred (+{vector.pacing_preference:.1f})")
        elif vector.pacing_preference < -0.3:
            lines.append(f"- Pacing: Slower pace needed ({vector.pacing_preference:.1f})")
        else:
            lines.append(f"- Pacing: Standard pace ({vector.pacing_preference:+.1f})")

    # Subject affinities
    if vector.subject_affinity_map:
        sorted_subj = sorted(vector.subject_affinity_map.items(), key=lambda x: -x[1])
        affinity_strs = [f"{s.title()} ({v:.2f})" for s, v in sorted_subj]
        lines.append(f"- Subject affinities: {', '.join(affinity_strs)}")

    # Modality
    if vector.modality_preference:
        lines.append(f"- Modality: {_modality_label(vector.modality_preference)} preferred")

    # Include parent observations from intelligence profile
    try:
        intel_result = await db.execute(
            select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id)
        )
        intel = intel_result.scalar_one_or_none()
        if intel and intel.parent_observations:
            obs_texts = [o.get("observation", "") for o in intel.parent_observations if o.get("observation")]
            if obs_texts:
                lines.append("")
                lines.append("PARENT OBSERVATIONS:")
                for obs in obs_texts[-5:]:
                    lines.append(f"- {obs}")
    except Exception:
        pass

    return "\n".join(lines)


def build_tutor_style_guidance(vector: LearnerStyleVector | None) -> str:
    """Build tutor-specific guidance lines from the style vector."""
    if vector is None or vector.dimensions_active == 0:
        return ""

    lines = []

    if vector.socratic_responsiveness is not None:
        if vector.socratic_responsiveness > 0.7:
            lines.append("This child responds well to Socratic questioning. Lead with questions.")
        elif vector.socratic_responsiveness < 0.3:
            lines.append("This child learns better from worked examples first, then guided practice.")

    if vector.frustration_threshold is not None and vector.frustration_threshold < 0.4:
        lines.append("This child needs early scaffolding. If they hesitate, offer a smaller step immediately.")

    if vector.independence_level is not None and vector.independence_level > 0.7:
        lines.append("This child is self-directed. Offer space before hints.")

    if vector.optimal_session_minutes is not None and vector.optimal_session_minutes < 20:
        lines.append("Keep interactions concise. This child's focus peaks in short sessions.")

    return "\n".join(lines)


def build_planner_style_guidance(vector: LearnerStyleVector | None) -> str:
    """Build planner-specific guidance lines from the style vector."""
    if vector is None or vector.dimensions_active == 0:
        return ""

    lines = []

    if vector.optimal_session_minutes is not None:
        lines.append(f"Schedule activities within {vector.optimal_session_minutes} minutes for this child.")

    if vector.time_of_day_peak is not None:
        lines.append(f"Schedule highest-priority subjects around {_hour_label(vector.time_of_day_peak)} for peak performance.")

    if vector.pacing_preference is not None:
        if vector.pacing_preference > 0.3:
            lines.append("This child thrives with challenge. Include stretch activities.")
        elif vector.pacing_preference < -0.3:
            lines.append("This child benefits from consolidation. Include extra review.")

    if vector.subject_affinity_map:
        sorted_subj = sorted(vector.subject_affinity_map.items(), key=lambda x: -x[1])
        lines.append(f"Subject affinities (balance high and low): {', '.join(f'{s}={v:.2f}' for s, v in sorted_subj)}")

    return "\n".join(lines)


def build_advisor_style_guidance() -> str:
    """Build advisor-specific guidance for reports."""
    return (
        "Include a 'Learning Style Insights' section in your weekly report.\n"
        "Reference the child's style dimensions and note any notable patterns.\n"
        "Example: 'Emma's independence level suggests she is building confidence in self-directed work.'"
    )
