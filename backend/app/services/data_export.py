"""Full family data export service.

Exports the complete educational record as a ZIP file containing
JSON files organized by child.
"""

import io
import json
import uuid
import zipfile
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.annual_curriculum import AnnualCurriculum
from app.models.evidence import ReadingLogEntry, WeeklySnapshot
from app.models.governance import GovernanceEvent, GovernanceRule
from app.models.identity import Child, Household
from app.models.state import ChildNodeState
from app.services.compliance_engine import get_hours_breakdown


def _json_serial(obj):
    """JSON serializer for objects not serializable by default."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if hasattr(obj, "value"):
        return obj.value
    return str(obj)


async def export_family_data(db: AsyncSession, household_id: uuid.UUID) -> bytes:
    """Export complete family educational record as ZIP."""

    buf = io.BytesIO()
    zf = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)

    # Household profile
    hh_r = await db.execute(select(Household).where(Household.id == household_id))
    hh = hh_r.scalar_one()
    zf.writestr(
        "family_profile.json",
        json.dumps(
            {
                "name": hh.name,
                "philosophical_profile": hh.philosophical_profile,
                "settings": hh.settings if hasattr(hh, "settings") else {},
            },
            default=_json_serial,
            indent=2,
        ),
    )

    # Governance rules
    rules_r = await db.execute(select(GovernanceRule).where(GovernanceRule.household_id == household_id))
    rules = [
        {
            "name": r.name,
            "type": r.rule_type.value,
            "tier": r.tier.value,
            "scope": r.scope.value,
            "parameters": r.parameters,
            "is_active": r.is_active,
        }
        for r in rules_r.scalars().all()
    ]
    zf.writestr("governance_rules.json", json.dumps(rules, default=_json_serial, indent=2))

    # Governance events
    events_r = await db.execute(
        select(GovernanceEvent).where(GovernanceEvent.household_id == household_id).order_by(GovernanceEvent.created_at)
    )
    events = [
        {
            "action": e.action.value,
            "target_type": e.target_type,
            "target_id": str(e.target_id),
            "reason": e.reason,
            "created_at": str(e.created_at),
        }
        for e in events_r.scalars().all()
    ]
    zf.writestr("governance_events.json", json.dumps(events, default=_json_serial, indent=2))

    # Children
    children_r = await db.execute(select(Child).where(Child.household_id == household_id))
    children = children_r.scalars().all()

    total_records = len(rules) + len(events)

    for child in children:
        name = child.first_name.lower().replace(" ", "_")
        prefix = f"{name}/"

        # Curricula
        curr_r = await db.execute(
            select(AnnualCurriculum)
            .where(
                AnnualCurriculum.child_id == child.id,
                AnnualCurriculum.household_id == household_id,
            )
            .order_by(AnnualCurriculum.academic_year)
        )
        curricula = [
            {
                "subject": c.subject_name,
                "year": c.academic_year,
                "grade": c.grade_level,
                "status": c.status,
                "scope_sequence": c.scope_sequence,
                "actual_record": c.actual_record,
            }
            for c in curr_r.scalars().all()
        ]
        zf.writestr(f"{prefix}curricula.json", json.dumps(curricula, default=_json_serial, indent=2))
        total_records += len(curricula)

        # Reading log
        read_r = await db.execute(select(ReadingLogEntry).where(ReadingLogEntry.child_id == child.id))
        reading = [
            {
                "title": r.book_title,
                "author": r.book_author,
                "genre": r.genre,
                "status": r.status,
                "pages_read": r.pages_read,
                "pages_total": r.pages_total,
                "narration": r.narration,
                "rating": r.child_rating,
            }
            for r in read_r.scalars().all()
        ]
        zf.writestr(f"{prefix}reading_log.json", json.dumps(reading, default=_json_serial, indent=2))
        total_records += len(reading)

        # Mastery states
        states_r = await db.execute(select(ChildNodeState).where(ChildNodeState.child_id == child.id))
        states = [
            {
                "node_id": str(s.node_id),
                "mastery_level": s.mastery_level.value if hasattr(s.mastery_level, "value") else str(s.mastery_level),
                "time_spent_minutes": s.time_spent_minutes,
                "attempts_count": s.attempts_count,
            }
            for s in states_r.scalars().all()
        ]
        zf.writestr(f"{prefix}mastery_states.json", json.dumps(states, default=_json_serial, indent=2))
        total_records += len(states)

        # Weekly snapshots
        snaps_r = await db.execute(
            select(WeeklySnapshot).where(WeeklySnapshot.child_id == child.id).order_by(WeeklySnapshot.week_start)
        )
        snapshots = [
            {
                "week_start": str(s.week_start),
                "week_end": str(s.week_end),
                "total_minutes": s.total_minutes,
                "activities_completed": s.activities_completed,
                "nodes_mastered": s.nodes_mastered,
            }
            for s in snaps_r.scalars().all()
        ]
        zf.writestr(f"{prefix}weekly_snapshots.json", json.dumps(snapshots, default=_json_serial, indent=2))
        total_records += len(snapshots)

        # Hours
        hours = await get_hours_breakdown(db, household_id, child.id)
        zf.writestr(f"{prefix}compliance_hours.json", json.dumps(hours, default=_json_serial, indent=2))

    # Metadata
    zf.writestr(
        "metadata.json",
        json.dumps(
            {
                "export_date": date.today().isoformat(),
                "methean_version": "0.1.0",
                "total_children": len(children),
                "total_records": total_records,
            },
            indent=2,
        ),
    )

    zf.close()
    return buf.getvalue()
