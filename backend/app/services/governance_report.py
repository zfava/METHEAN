"""Governance Report Generator.

Produces the "board meeting minutes" for a homeschool family —
a synthesized document proving the parent was in charge of every
decision during the period.
"""

import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import GovernanceAction, MasteryLevel
from app.models.evidence import WeeklySnapshot
from app.models.governance import GovernanceEvent, GovernanceRule
from app.models.identity import Child, Household
from app.models.operational import AIRun
from app.models.state import ChildNodeState, StateEvent


async def generate_governance_report(
    db: AsyncSession,
    household_id: uuid.UUID,
    period_start: date,
    period_end: date,
    user_id: uuid.UUID,
) -> dict:
    """Generate a comprehensive governance report for the period."""

    # ── Household info ──
    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one()

    # ── Children ──
    children_result = await db.execute(
        select(Child).where(Child.household_id == household_id, Child.is_active == True)  # noqa: E712
    )
    children = children_result.scalars().all()
    child_names = {c.id: f"{c.first_name} {c.last_name or ''}".strip() for c in children}

    # ── Governance events in period ──
    events_result = await db.execute(
        select(GovernanceEvent).where(
            GovernanceEvent.household_id == household_id,
            GovernanceEvent.created_at >= datetime(period_start.year, period_start.month, period_start.day, tzinfo=UTC),
            GovernanceEvent.created_at < datetime(period_end.year, period_end.month, period_end.day, tzinfo=UTC) + timedelta(days=1),
        ).order_by(GovernanceEvent.created_at.asc())
    )
    events = events_result.scalars().all()

    # Categorize events
    approvals = [e for e in events if e.action == GovernanceAction.approve]
    rejections = [e for e in events if e.action == GovernanceAction.reject]
    modifications = [e for e in events if e.action == GovernanceAction.modify]
    deferrals = [e for e in events if e.action == GovernanceAction.defer]
    overrides = [e for e in events if e.target_type == "child_node_state"]
    constitutional_changes = [e for e in events if e.target_type == "constitutional_rule_change"]
    rule_changes = [e for e in events if e.target_type in ("governance_rule", "constitutional_rule_change")]

    # ── AI runs in period ──
    ai_result = await db.execute(
        select(AIRun).where(
            AIRun.household_id == household_id,
            AIRun.created_at >= datetime(period_start.year, period_start.month, period_start.day, tzinfo=UTC),
            AIRun.created_at < datetime(period_end.year, period_end.month, period_end.day, tzinfo=UTC) + timedelta(days=1),
        )
    )
    ai_runs = ai_result.scalars().all()
    ai_by_role = {}
    for run in ai_runs:
        role = run.run_type
        ai_by_role.setdefault(role, []).append(run)

    # ── Per-child mastery state ──
    child_progress = []
    for child in children:
        states_result = await db.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.household_id == household_id,
            )
        )
        states = states_result.scalars().all()
        mastered = sum(1 for s in states if s.mastery_level == MasteryLevel.mastered)
        total = len(states)
        total_minutes = sum(s.time_spent_minutes or 0 for s in states)
        total_attempts = sum(s.attempts_count or 0 for s in states)

        child_progress.append({
            "child_id": str(child.id),
            "child_name": child_names[child.id],
            "grade_level": child.grade_level,
            "nodes_mastered": mastered,
            "nodes_total": total,
            "total_hours": round(total_minutes / 60, 1),
            "total_attempts": total_attempts,
        })

    # ── Snapshots for progress trends ──
    snapshots_result = await db.execute(
        select(WeeklySnapshot).where(
            WeeklySnapshot.household_id == household_id,
            WeeklySnapshot.week_start >= period_start,
            WeeklySnapshot.week_end <= period_end,
        ).order_by(WeeklySnapshot.week_start.asc())
    )
    snapshots = snapshots_result.scalars().all()

    # ── AI acceptance rate ──
    total_ai_decisions = len(approvals) + len(rejections)
    ai_acceptance_rate = round(len(approvals) / total_ai_decisions * 100, 1) if total_ai_decisions > 0 else None

    # ── Build report ──
    return {
        "report_type": "governance_report",
        "generated_at": datetime.now(UTC).isoformat(),
        "generated_by": str(user_id),
        "period": {
            "start": period_start.isoformat(),
            "end": period_end.isoformat(),
            "days": (period_end - period_start).days,
        },
        "household": {
            "name": household.name,
            "timezone": household.timezone,
        },

        "executive_summary": {
            "children_covered": len(children),
            "total_governance_events": len(events),
            "activities_approved": len(approvals),
            "activities_rejected": len(rejections),
            "activities_deferred": len(deferrals),
            "overrides_count": len(overrides),
            "rule_changes_count": len(rule_changes),
            "constitutional_changes_count": len(constitutional_changes),
            "ai_runs_count": len(ai_runs),
            "ai_acceptance_rate_pct": ai_acceptance_rate,
        },

        "governance_decisions": [
            {
                "timestamp": e.created_at.isoformat() if e.created_at else None,
                "action": e.action.value if hasattr(e.action, "value") else str(e.action),
                "target_type": e.target_type,
                "target_id": str(e.target_id),
                "reason": e.reason,
            }
            for e in events
        ],

        "ai_oversight": {
            "total_ai_runs": len(ai_runs),
            "runs_by_role": {role: len(runs) for role, runs in ai_by_role.items()},
            "acceptance_rate_pct": ai_acceptance_rate,
            "rejections": [
                {
                    "timestamp": e.created_at.isoformat() if e.created_at else None,
                    "target_type": e.target_type,
                    "reason": e.reason,
                }
                for e in rejections
            ],
        },

        "rule_changes": [
            {
                "timestamp": e.created_at.isoformat() if e.created_at else None,
                "target_type": e.target_type,
                "reason": e.reason,
                "metadata": e.metadata_,
            }
            for e in rule_changes
        ],

        "constitutional_actions": [
            {
                "timestamp": e.created_at.isoformat() if e.created_at else None,
                "reason": e.reason,
                "metadata": e.metadata_,
            }
            for e in constitutional_changes
        ],

        "overrides": [
            {
                "timestamp": e.created_at.isoformat() if e.created_at else None,
                "target_id": str(e.target_id),
                "reason": e.reason,
            }
            for e in overrides
        ],

        "learning_progress": child_progress,

        "compliance_metrics": {
            "total_hours_logged": round(sum(cp["total_hours"] for cp in child_progress), 1),
            "total_attempts": sum(cp["total_attempts"] for cp in child_progress),
            "children_with_mastery_gains": sum(1 for cp in child_progress if cp["nodes_mastered"] > 0),
        },

        "rule_enforcement": _compute_rule_enforcement(events),

        "parent_attestation": {
            "status": "pending",
            "text": None,
            "attested_at": None,
        },
    }


def _compute_rule_enforcement(events: list) -> dict:
    """Compute per-rule evaluation and trigger counts from event metadata."""
    stats: dict[str, dict] = {}
    for event in events:
        evals = (event.metadata_ or {}).get("evaluations", [])
        for ev in evals:
            name = ev.get("rule", "unknown")
            if name not in stats:
                stats[name] = {
                    "evaluated": 0, "triggered": 0,
                    "type": ev.get("type", ""), "tier": "",
                }
            stats[name]["evaluated"] += 1
            if not ev.get("passed", True):
                stats[name]["triggered"] += 1
    return stats
