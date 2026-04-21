"""Learner Intelligence service — accumulate observations, synthesize context.

The intelligence layer OBSERVES. The parent GOVERNS. The AI ADAPTS.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.intelligence import LearnerIntelligence

# ── Helpers ──


async def _get_or_create(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> LearnerIntelligence:
    """Get existing intelligence profile or create a new one."""
    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
    profile = result.scalar_one_or_none()
    if profile:
        return profile

    profile = LearnerIntelligence(
        child_id=child_id,
        household_id=household_id,
        learning_style_observations=[],
        subject_patterns={},
        engagement_patterns={},
        tutor_interaction_analysis={},
        pace_trends={},
        parent_observations=[],
        governance_learned_preferences={},
    )
    db.add(profile)
    await db.flush()
    return profile


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


# ── Accumulation Functions ──


async def record_evaluation_insight(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    evaluation_result: dict,
    activity_title: str,
    subject: str,
) -> None:
    """Called after every evaluator run. Extracts strengths/struggles into subject_patterns."""
    profile = await _get_or_create(db, child_id, household_id)

    strengths = evaluation_result.get("strengths", [])
    struggles = evaluation_result.get("areas_for_improvement", evaluation_result.get("struggles", []))
    quality = evaluation_result.get("quality_rating", evaluation_result.get("score"))

    patterns = dict(profile.subject_patterns or {})
    sub = patterns.get(subject, {"strengths": [], "struggles": [], "notes": []})

    # Append new observations, deduplicate by incrementing confidence
    for s in strengths:
        text = s if isinstance(s, str) else str(s)
        existing = next((x for x in sub["strengths"] if x.get("text") == text), None)
        if existing:
            existing["evidence_count"] = existing.get("evidence_count", 1) + 1
            existing["confidence"] = min(1.0, existing.get("confidence", 0.5) + 0.1)
        else:
            sub["strengths"].append({"text": text, "confidence": 0.5, "evidence_count": 1, "observed_at": _now_iso()})

    for s in struggles:
        text = s if isinstance(s, str) else str(s)
        existing = next((x for x in sub["struggles"] if x.get("text") == text), None)
        if existing:
            existing["evidence_count"] = existing.get("evidence_count", 1) + 1
            existing["confidence"] = min(1.0, existing.get("confidence", 0.5) + 0.1)
        else:
            sub["struggles"].append({"text": text, "confidence": 0.5, "evidence_count": 1, "observed_at": _now_iso()})

    if quality is not None:
        sub["notes"].append({"activity": activity_title, "quality": quality, "at": _now_iso()})
        sub["notes"] = sub["notes"][-20:]  # Keep last 20

    # Cap lists to prevent unbounded growth
    sub["strengths"] = sorted(sub["strengths"], key=lambda x: -x.get("confidence", 0))[:15]
    sub["struggles"] = sorted(sub["struggles"], key=lambda x: -x.get("confidence", 0))[:15]

    patterns[subject] = sub
    profile.subject_patterns = patterns
    profile.observation_count = (profile.observation_count or 0) + 1
    profile.last_updated_at = datetime.now(UTC)
    await db.flush()


async def record_attempt_engagement(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    duration_minutes: int,
    activity_type: str,
    time_of_day: str,
    completed: bool,
    estimated_minutes: int | None = None,
) -> None:
    """Called after every attempt submission. Updates engagement_patterns."""
    profile = await _get_or_create(db, child_id, household_id)

    eng = dict(profile.engagement_patterns or {})

    # Rolling average of focus minutes (last 20)
    recent = eng.get("recent_durations", [])
    recent.append(duration_minutes)
    recent = recent[-20:]
    eng["recent_durations"] = recent
    eng["avg_focus_minutes"] = round(sum(recent) / len(recent), 1)

    # Time of day tracking
    tod_counts = eng.get("time_of_day_counts", {})
    tod_counts[time_of_day] = tod_counts.get(time_of_day, 0) + 1
    eng["time_of_day_counts"] = tod_counts
    eng["best_time_of_day"] = max(tod_counts, key=tod_counts.get)

    # Activity type preferences (completion rate)
    type_stats = eng.get("activity_type_stats", {})
    ts = type_stats.get(activity_type, {"completed": 0, "total": 0})
    ts["total"] += 1
    if completed:
        ts["completed"] += 1
    type_stats[activity_type] = ts
    eng["activity_type_stats"] = type_stats
    eng["activity_type_preferences"] = {k: round(v["completed"] / max(v["total"], 1), 2) for k, v in type_stats.items()}

    # Focus flag
    if estimated_minutes and duration_minutes < estimated_minutes * 0.5:
        flags = eng.get("focus_flags", [])
        flags.append(
            {
                "activity_type": activity_type,
                "duration": duration_minutes,
                "expected": estimated_minutes,
                "at": _now_iso(),
            }
        )
        eng["focus_flags"] = flags[-10:]

    profile.engagement_patterns = eng
    profile.observation_count = (profile.observation_count or 0) + 1
    profile.last_updated_at = datetime.now(UTC)
    await db.flush()


async def record_tutor_interaction(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    subject: str,
    messages_count: int,
    hints_used: int,
    self_corrections: int,
) -> None:
    """Called after tutor chat session ends. Updates tutor_interaction_analysis."""
    profile = await _get_or_create(db, child_id, household_id)

    analysis = dict(profile.tutor_interaction_analysis or {})

    # Question frequency by subject
    freq = analysis.get("question_frequency_by_subject", {})
    freq[subject] = freq.get(subject, 0) + messages_count
    analysis["question_frequency_by_subject"] = freq

    # Hint usage rate (rolling)
    sessions = analysis.get("sessions", [])
    sessions.append({"hints": hints_used, "messages": messages_count, "self_corrections": self_corrections})
    sessions = sessions[-30:]
    analysis["sessions"] = sessions

    total_hints = sum(s["hints"] for s in sessions)
    total_messages = sum(s["messages"] for s in sessions)
    total_corrections = sum(s["self_corrections"] for s in sessions)

    analysis["hint_usage_rate"] = round(total_hints / max(total_messages, 1), 3)
    analysis["self_correction_rate"] = round(total_corrections / max(total_messages, 1), 3)

    profile.tutor_interaction_analysis = analysis
    profile.observation_count = (profile.observation_count or 0) + 1
    profile.last_updated_at = datetime.now(UTC)
    await db.flush()


async def record_mastery_transition(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    subject: str,
    from_level: str,
    to_level: str,
    node_title: str,
) -> None:
    """Called after every mastery change. Updates pace_trends."""
    profile = await _get_or_create(db, child_id, household_id)

    levels_order = ["emerging", "developing", "proficient", "mastered"]
    from_idx = levels_order.index(from_level) if from_level in levels_order else -1
    to_idx = levels_order.index(to_level) if to_level in levels_order else -1
    is_upward = to_idx > from_idx

    pace = dict(profile.pace_trends or {})
    transitions = pace.get("transitions", [])
    transitions.append(
        {
            "subject": subject,
            "node": node_title,
            "from": from_level,
            "to": to_level,
            "direction": "up" if is_upward else "down",
            "at": _now_iso(),
        }
    )
    transitions = transitions[-50:]
    pace["transitions"] = transitions

    # Compute per-subject mastery rate
    subject_rates = pace.get("subject_rates", {})
    subject_transitions = [t for t in transitions if t["subject"] == subject]
    ups = sum(1 for t in subject_transitions if t["direction"] == "up")
    downs = sum(1 for t in subject_transitions if t["direction"] == "down")
    total = ups + downs
    subject_rates[subject] = round(ups / max(total, 1), 2) if total > 0 else None
    pace["subject_rates"] = subject_rates

    # Overall mastery rate
    all_ups = sum(1 for t in transitions if t["direction"] == "up")
    pace["overall_mastery_rate"] = round(all_ups / max(len(transitions), 1), 2)

    profile.pace_trends = pace
    profile.observation_count = (profile.observation_count or 0) + 1
    profile.last_updated_at = datetime.now(UTC)
    await db.flush()


async def record_governance_pattern(
    db: AsyncSession,
    household_id: uuid.UUID,
    action: str,
    activity_type: str | None = None,
    difficulty: int | None = None,
) -> None:
    """Called after every governance decision. Updates governance_learned_preferences for all children."""
    # Get all intelligence profiles for this household
    result = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.household_id == household_id))
    profiles = result.scalars().all()
    if not profiles:
        return

    for profile in profiles:
        prefs = dict(profile.governance_learned_preferences or {})

        # Track decisions
        decisions = prefs.get("decisions", [])
        decisions.append(
            {
                "action": action,
                "activity_type": activity_type,
                "difficulty": difficulty,
                "at": _now_iso(),
            }
        )
        decisions = decisions[-100:]
        prefs["decisions"] = decisions

        # After 20+ decisions, compute difficulty ceiling
        if len(decisions) >= 20:
            [d for d in decisions if d["action"] in ("approve", "auto_approve")]
            rejected = [d for d in decisions if d["action"] == "reject"]

            if difficulty is not None:
                # Find highest difficulty with 90%+ approval rate
                for ceiling in range(5, 0, -1):
                    at_level = [d for d in decisions if d.get("difficulty") == ceiling]
                    if len(at_level) >= 3:
                        approve_rate = sum(1 for d in at_level if d["action"] in ("approve", "auto_approve")) / len(
                            at_level
                        )
                        if approve_rate >= 0.9:
                            prefs["auto_approve_difficulty_ceiling"] = ceiling
                            break

            # Track rejected activity types
            rejected_types = {}
            for d in rejected:
                if d.get("activity_type"):
                    rejected_types[d["activity_type"]] = rejected_types.get(d["activity_type"], 0) + 1
            prefs["rejected_activity_types"] = [k for k, v in rejected_types.items() if v >= 2]

        profile.governance_learned_preferences = prefs
        profile.last_updated_at = datetime.now(UTC)

    await db.flush()


# ── Synthesis Function ──


async def get_intelligence_context(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> dict:
    """Returns a structured summary for injection into AI prompts."""
    result = await db.execute(
        select(LearnerIntelligence).where(
            LearnerIntelligence.child_id == child_id,
            LearnerIntelligence.household_id == household_id,
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        return {}

    # Top 5 learning style observations (highest confidence)
    style_obs = sorted(
        profile.learning_style_observations or [],
        key=lambda x: -(x.get("confidence", 0)),
    )[:5]

    # Per-subject strengths and struggles (top 3 each)
    subject_summary = {}
    for subject, data in (profile.subject_patterns or {}).items():
        subject_summary[subject] = {
            "strengths": [
                s["text"] for s in sorted(data.get("strengths", []), key=lambda x: -x.get("confidence", 0))[:3]
            ],
            "struggles": [
                s["text"] for s in sorted(data.get("struggles", []), key=lambda x: -x.get("confidence", 0))[:3]
            ],
        }

    # Engagement summary
    eng = profile.engagement_patterns or {}
    engagement = {
        "avg_focus_minutes": eng.get("avg_focus_minutes"),
        "best_time_of_day": eng.get("best_time_of_day"),
        "preferred_activity_types": eng.get("activity_type_preferences", {}),
    }

    # Pace assessment
    pace = profile.pace_trends or {}
    pace_assessment = {
        "overall_mastery_rate": pace.get("overall_mastery_rate"),
        "subject_rates": pace.get("subject_rates", {}),
    }

    # Parent observations (all, unfiltered — parent's word is law)
    parent_obs = profile.parent_observations or []

    # Governance preferences
    gov_prefs = profile.governance_learned_preferences or {}
    governance = {
        "auto_approve_difficulty_ceiling": gov_prefs.get("auto_approve_difficulty_ceiling"),
        "rejected_activity_types": gov_prefs.get("rejected_activity_types", []),
    }

    return {
        "learning_style_observations": [o.get("observation", "") for o in style_obs],
        "subject_patterns": subject_summary,
        "engagement": engagement,
        "pace": pace_assessment,
        "parent_observations": [o.get("observation", "") for o in parent_obs],
        "governance_preferences": governance,
        "observation_count": profile.observation_count or 0,
        "last_updated": profile.last_updated_at.isoformat() if profile.last_updated_at else None,
    }
