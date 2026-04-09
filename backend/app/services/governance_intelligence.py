"""Governance Intelligence — learn from parent review patterns.

Analyzes governance events to compute behavioral patterns that inform
the planner. The parent's review history becomes planning intelligence.
"""

import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.governance import GovernanceEvent
from app.models.enums import GovernanceAction


async def analyze_governance_patterns(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> dict:
    """Analyze all governance events and compute behavioral patterns."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)

    result = await db.execute(
        select(GovernanceEvent)
        .where(
            GovernanceEvent.household_id == household_id,
            GovernanceEvent.created_at >= cutoff,
        )
        .order_by(desc(GovernanceEvent.created_at))
        .limit(200)
    )
    events = list(result.scalars().all())

    if len(events) < 3:
        return {"event_count": len(events), "sufficient_data": False}

    # ── Approval rate by difficulty ──
    difficulty_counts: dict[int, dict[str, int]] = defaultdict(lambda: {"approved": 0, "total": 0})
    type_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"approved": 0, "total": 0})
    modification_patterns: list[str] = []
    rejection_reasons: list[str] = []
    review_times: list[float] = []
    hour_counts: dict[int, int] = defaultdict(int)

    for evt in events:
        meta = evt.metadata_ or {}
        action_str = evt.action.value if hasattr(evt.action, "value") else str(evt.action)

        # Track difficulty
        difficulty = meta.get("difficulty")
        if difficulty is not None:
            try:
                d = int(difficulty)
                difficulty_counts[d]["total"] += 1
                if action_str in ("approve", "auto_approve"):
                    difficulty_counts[d]["approved"] += 1
            except (ValueError, TypeError):
                pass

        # Track activity type
        activity_type = meta.get("activity_type")
        if activity_type:
            type_counts[activity_type]["total"] += 1
            if action_str in ("approve", "auto_approve"):
                type_counts[activity_type]["approved"] += 1

        # Track modifications
        if action_str == "modify":
            reason = evt.reason or ""
            if reason:
                modification_patterns.append(reason)

        # Track rejections
        if action_str == "reject" and evt.reason:
            rejection_reasons.append(evt.reason)

        # Track time-of-day
        if evt.created_at:
            hour_counts[evt.created_at.hour] += 1

        # Track review time (from metadata if available)
        queued_at = meta.get("queued_at")
        if queued_at and evt.created_at:
            try:
                q = datetime.fromisoformat(queued_at.replace("Z", "+00:00"))
                diff_hours = (evt.created_at.replace(tzinfo=timezone.utc) - q).total_seconds() / 3600
                if 0 < diff_hours < 168:  # Ignore outliers > 1 week
                    review_times.append(diff_hours)
            except (ValueError, TypeError):
                pass

    # ── Compute rates ──
    approval_rate_by_difficulty = {}
    for d in sorted(difficulty_counts.keys()):
        c = difficulty_counts[d]
        approval_rate_by_difficulty[d] = round(c["approved"] / max(c["total"], 1), 2)

    approval_rate_by_type = {}
    for t, c in type_counts.items():
        approval_rate_by_type[t] = round(c["approved"] / max(c["total"], 1), 2)

    # Auto-approve ceiling: highest difficulty with 90%+ approval and 3+ samples
    auto_approve_ceiling = 0
    for d in sorted(difficulty_counts.keys()):
        c = difficulty_counts[d]
        if c["total"] >= 3 and (c["approved"] / c["total"]) >= 0.9:
            auto_approve_ceiling = d

    # Average review time
    avg_review_hours = round(sum(review_times) / len(review_times), 1) if review_times else None

    # Peak review hour
    peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else None
    peak_label = None
    if peak_hour is not None:
        if peak_hour < 12:
            peak_label = "morning"
        elif peak_hour < 17:
            peak_label = "afternoon"
        else:
            peak_label = "evening"

    # Deduplicate and count rejection reasons
    reason_freq: dict[str, int] = defaultdict(int)
    for r in rejection_reasons:
        # Normalize: lowercase, strip, first 80 chars
        key = r.strip().lower()[:80]
        if key:
            reason_freq[key] += 1
    top_rejections = sorted(reason_freq.items(), key=lambda x: -x[1])[:5]

    return {
        "event_count": len(events),
        "sufficient_data": len(events) >= 10,
        "approval_rate_by_difficulty": approval_rate_by_difficulty,
        "approval_rate_by_type": approval_rate_by_type,
        "auto_approve_ceiling": auto_approve_ceiling,
        "modification_count": len(modification_patterns),
        "rejection_count": len(rejection_reasons),
        "top_rejection_reasons": [{"reason": r, "count": c} for r, c in top_rejections],
        "avg_review_hours": avg_review_hours,
        "peak_review_time": peak_label,
        "peak_review_hour": peak_hour,
    }


async def get_planning_adjustments(
    db: AsyncSession,
    household_id: uuid.UUID,
) -> dict:
    """Returns adjustments the planner should apply based on governance patterns."""
    patterns = await analyze_governance_patterns(db, household_id)

    if not patterns.get("sufficient_data"):
        return {}

    ceiling = patterns.get("auto_approve_ceiling", 3)
    type_rates = patterns.get("approval_rate_by_type", {})
    rejections = patterns.get("top_rejection_reasons", [])

    # Favor activity types with high approval rates
    preferred_types = [t for t, rate in type_rates.items() if rate >= 0.8]
    avoided_types = [t for t, rate in type_rates.items() if rate < 0.5]

    return {
        "max_difficulty": min(ceiling + 1, 5),
        "preferred_activity_types": preferred_types,
        "avoided_activity_types": avoided_types,
        "avoid_patterns": [r["reason"] for r in rejections[:3]],
        "auto_approve_ceiling": ceiling,
    }
