"""Child Personal Dashboard API.

Single endpoint that assembles everything a child needs on load.
No waterfall of API calls — one request, complete dashboard.
Performance-critical: ZERO database queries inside loops.
"""

import uuid
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningMap,
    LearningNode,
    Subject,
)
from app.models.enums import ActivityStatus
from app.models.governance import Activity, Attempt
from app.models.identity import Child, User
from app.models.state import ChildNodeState, StateEvent

router = APIRouter(tags=["child-dashboard"])

DEFAULT_COLORS = {
    "Mathematics": "#3b82f6",
    "Reading": "#10b981",
    "Phonics & Reading": "#10b981",
    "Science": "#8b5cf6",
    "History": "#f59e0b",
    "Writing & Grammar": "#ec4899",
    "Literature": "#06b6d4",
}


async def _get_child_or_404(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


@router.get("/children/{child_id}/dashboard")
async def get_child_dashboard(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Single endpoint: everything the child needs on load."""
    child = await _get_child_or_404(db, child_id, user.household_id)
    household_id = user.household_id
    today = date.today()
    datetime.now(UTC)
    week_start = today - timedelta(days=today.weekday())

    # ── Streak & achievements (2 queries) ──
    try:
        from app.services.achievements import get_achievements, get_streak

        streak_data = await get_streak(db, child_id, household_id)
        achievements = await get_achievements(db, child_id)
    except Exception:
        streak_data = {"current_streak": 0, "longest_streak": 0, "last_activity_date": None}
        achievements = []

    current_streak = streak_data.get("current_streak", 0)
    is_today_complete = streak_data.get("last_activity_date") == today.isoformat()

    # ── Today's activities (1 query) ──
    act_result = await db.execute(
        select(Activity)
        .where(
            Activity.household_id == household_id,
            Activity.scheduled_date == today,
            Activity.status.in_([ActivityStatus.scheduled, ActivityStatus.in_progress, ActivityStatus.completed]),
        )
        .order_by(Activity.sort_order)
    )
    today_activities = act_result.scalars().all()

    # Resolve node+subject info for activities (1 query, batch)
    node_ids = [a.node_id for a in today_activities if a.node_id]
    node_map: dict[uuid.UUID, dict] = {}
    subject_map: dict[uuid.UUID, dict] = {}

    if node_ids:
        node_result = await db.execute(
            select(LearningNode, LearningMap, Subject)
            .join(LearningMap, LearningNode.learning_map_id == LearningMap.id)
            .join(Subject, LearningMap.subject_id == Subject.id)
            .where(LearningNode.id.in_(node_ids))
        )
        for node, _lmap, subj in node_result.all():
            node_map[node.id] = {"title": node.title, "subject_id": subj.id}
            subject_map[subj.id] = {"name": subj.name, "color": subj.color or DEFAULT_COLORS.get(subj.name, "#6b7280")}

    # Mastery states for today's nodes (1 query, batch)
    state_result = (
        await db.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child_id,
                ChildNodeState.node_id.in_(node_ids),
            )
        )
        if node_ids
        else None
    )
    node_states = {s.node_id: s for s in (state_result.scalars().all() if state_result else [])}

    completed_count = sum(
        1 for a in today_activities if (a.status.value if hasattr(a.status, "value") else str(a.status)) == "completed"
    )
    remaining_minutes = sum(
        (a.estimated_minutes or 20)
        for a in today_activities
        if (a.status.value if hasattr(a.status, "value") else str(a.status)) != "completed"
    )

    activity_items = []
    for i, a in enumerate(today_activities):
        node_info = node_map.get(a.node_id, {}) if a.node_id else {}
        subj_info = subject_map.get(node_info.get("subject_id"), {})
        state = node_states.get(a.node_id) if a.node_id else None
        mastery = (
            state.mastery_level.value
            if state and hasattr(state.mastery_level, "value")
            else str(state.mastery_level)
            if state
            else "not_started"
        )
        activity_items.append(
            {
                "id": str(a.id),
                "title": a.title,
                "subject": subj_info.get("name", ""),
                "subject_color": subj_info.get("color", "#6b7280"),
                "type": a.activity_type.value if hasattr(a.activity_type, "value") else str(a.activity_type),
                "estimated_minutes": a.estimated_minutes,
                "status": a.status.value if hasattr(a.status, "value") else str(a.status),
                "is_review": (a.activity_type.value if hasattr(a.activity_type, "value") else str(a.activity_type))
                == "review",
                "node_title": node_info.get("title", ""),
                "node_mastery": mastery,
                "sequence_number": i + 1,
            }
        )

    # ── Progress (pre-fetch all data outside loops) ──

    # All child states (1 query)
    all_states = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
        )
    )
    all_states_list = all_states.scalars().all()
    all_states_by_node = {s.node_id: s for s in all_states_list}

    # Enrolled maps (1 query)
    enrolled_maps = await db.execute(
        select(ChildMapEnrollment.learning_map_id).where(
            ChildMapEnrollment.child_id == child_id,
            ChildMapEnrollment.household_id == household_id,
            ChildMapEnrollment.is_active == True,  # noqa: E712
        )
    )
    map_ids = list(enrolled_maps.scalars().all())

    # PRE-FETCH: All nodes grouped by map (1 query, replaces N per-map queries)
    nodes_by_map: dict[uuid.UUID, list[uuid.UUID]] = defaultdict(list)
    all_map_nodes: dict[uuid.UUID, LearningNode] = {}
    if map_ids:
        all_nodes_result = await db.execute(
            select(LearningNode)
            .where(
                LearningNode.learning_map_id.in_(map_ids),
                LearningNode.is_active == True,  # noqa: E712
            )
            .order_by(LearningNode.sort_order)
        )
        for node in all_nodes_result.scalars().all():
            nodes_by_map[node.learning_map_id].append(node.id)
            all_map_nodes[node.id] = node

    total_nodes = len(all_map_nodes)
    mastered_count = sum(
        1
        for s in all_states_list
        if (s.mastery_level.value if hasattr(s.mastery_level, "value") else str(s.mastery_level)) == "mastered"
    )
    overall_pct = round((mastered_count / max(total_nodes, 1)) * 100)

    # PRE-FETCH: Map-to-subject mapping (1 query, replaces N per-map queries)
    subject_progress = []
    map_subject_info: dict[uuid.UUID, tuple[str, str]] = {}  # map_id -> (name, color)
    if map_ids:
        map_subj_result = await db.execute(
            select(LearningMap.id, Subject.name, Subject.color)
            .join(Subject, LearningMap.subject_id == Subject.id)
            .where(LearningMap.id.in_(map_ids))
        )
        for map_id, subj_name, subj_color in map_subj_result.all():
            color = subj_color or DEFAULT_COLORS.get(subj_name, "#6b7280")
            map_subject_info[map_id] = (subj_name, color)

            # O(1) dict lookups — NO database queries in this loop
            map_node_ids = set(nodes_by_map.get(map_id, []))
            subj_total = len(map_node_ids)
            subj_mastered = sum(
                1
                for nid in map_node_ids
                if nid in all_states_by_node
                and (
                    all_states_by_node[nid].mastery_level.value
                    if hasattr(all_states_by_node[nid].mastery_level, "value")
                    else str(all_states_by_node[nid].mastery_level)
                )
                == "mastered"
            )

            subject_progress.append(
                {
                    "name": subj_name,
                    "color": color,
                    "mastered": subj_mastered,
                    "total": subj_total,
                    "percentage": round((subj_mastered / max(subj_total, 1)) * 100),
                }
            )

    # ── This week stats (2 queries, outside loops) ──
    week_events_r = await db.execute(
        select(StateEvent).where(
            StateEvent.child_id == child_id,
            StateEvent.created_at >= datetime.combine(week_start, datetime.min.time(), tzinfo=UTC),
        )
    )
    week_events = week_events_r.scalars().all()
    ups = sum(1 for e in week_events if e.to_state == "mastered" and e.from_state != "mastered")
    downs = sum(1 for e in week_events if e.from_state == "mastered" and e.to_state != "mastered")

    week_attempts_r = await db.execute(
        select(func.count(), func.coalesce(func.sum(Attempt.duration_minutes), 0)).where(
            Attempt.child_id == child_id,
            Attempt.status == "completed",
            Attempt.created_at >= datetime.combine(week_start, datetime.min.time(), tzinfo=UTC),
        )
    )
    week_row = week_attempts_r.one()
    week_completed = week_row[0] or 0
    week_minutes = week_row[1] or 0

    # ── Journey Maps (0 additional queries — uses pre-fetched data) ──
    journey_maps = []
    if map_ids:
        for map_id in map_ids[:5]:
            subj_info_tuple = map_subject_info.get(map_id)
            if not subj_info_tuple:
                continue
            subj_name, color = subj_info_tuple

            map_mastered = 0
            node_items = []
            found_current = False
            for nid in nodes_by_map.get(map_id, []):
                node = all_map_nodes.get(nid)
                if not node:
                    continue
                state = all_states_by_node.get(nid)
                m = (
                    state.mastery_level.value
                    if state and hasattr(state.mastery_level, "value")
                    else str(state.mastery_level)
                    if state
                    else "not_started"
                )
                is_current = m not in ("mastered", "not_started")
                is_next = is_current and not found_current
                if is_next:
                    found_current = True
                if m == "mastered":
                    map_mastered += 1
                node_items.append(
                    {
                        "id": str(nid),
                        "title": node.title,
                        "mastery": m,
                        "is_current": is_current,
                        "is_next": is_next,
                    }
                )

            journey_maps.append(
                {
                    "map_id": str(map_id),
                    "subject": subj_name,
                    "subject_color": color,
                    "nodes": node_items,
                    "total_nodes": len(node_items),
                    "mastered_nodes": map_mastered,
                }
            )

    # ── Greeting & Encouragement (1 query for node titles, pre-fetched) ──
    first_subject = activity_items[0]["subject"] if activity_items else None
    recent_mastery_node = None
    for e in sorted(week_events, key=lambda x: x.created_at or datetime.min.replace(tzinfo=UTC), reverse=True):
        if e.to_state == "mastered" and e.from_state != "mastered":
            # Use pre-fetched node data (0 additional queries)
            node = all_map_nodes.get(e.node_id)
            if node:
                recent_mastery_node = node.title
            break

    from app.services.child_greeting import generate_encouragement, generate_greeting

    # Best week mastery (1 query for ALL past weeks, not 3 separate queries)
    best_week = ups
    if week_start > date.today() - timedelta(weeks=4):
        past_weeks_start = week_start - timedelta(weeks=3)
        past_events_r = await db.execute(
            select(StateEvent.created_at).where(
                StateEvent.child_id == child_id,
                StateEvent.to_state == "mastered",
                StateEvent.created_at >= datetime.combine(past_weeks_start, datetime.min.time(), tzinfo=UTC),
                StateEvent.created_at < datetime.combine(week_start, datetime.min.time(), tzinfo=UTC),
            )
        )
        past_events = past_events_r.scalars().all()
        # Group by week
        week_counts: dict[int, int] = defaultdict(int)
        for evt_dt in past_events:
            if evt_dt:
                week_num = (evt_dt.date() - past_weeks_start).days // 7
                week_counts[week_num] += 1
        if week_counts:
            best_past = max(week_counts.values())
            if best_past > best_week:
                best_week = best_past

    greeting = generate_greeting(
        first_name=child.first_name,
        current_streak=current_streak,
        today_count=len(today_activities),
        first_subject=first_subject,
        recent_mastery=recent_mastery_node,
    )

    # Avg session minutes from intelligence (1 query)
    avg_session = None
    try:
        from app.models.intelligence import LearnerIntelligence

        intel_r = await db.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == child_id))
        intel = intel_r.scalar_one_or_none()
        if intel and intel.engagement_patterns:
            avg_session = intel.engagement_patterns.get("avg_focus_minutes")
    except Exception:
        pass

    encouragement = generate_encouragement(
        activities_completed_this_week=week_completed,
        time_spent_this_week=week_minutes,
        mastery_ups_this_week=ups,
        reviews_this_week=sum(
            1
            for e in week_events
            if e.event_type
            and (e.event_type.value if hasattr(e.event_type, "value") else str(e.event_type)) == "review_completed"
        ),
        best_week_mastery=best_week,
        avg_session_minutes=avg_session,
    )

    # ── Style hints (1 query) ──
    style_hints = {}
    try:
        from app.models.style_vector import LearnerStyleVector

        sv_r = await db.execute(select(LearnerStyleVector).where(LearnerStyleVector.child_id == child_id))
        sv = sv_r.scalar_one_or_none()
        if sv and sv.dimensions_active > 0:
            style_hints = {
                "optimal_session_minutes": sv.optimal_session_minutes,
                "best_time_of_day": {9: "morning", 14: "afternoon", 19: "evening"}.get(sv.time_of_day_peak)
                if sv.time_of_day_peak
                else None,
                "attention_pattern": sv.attention_pattern,
            }
    except Exception:
        pass

    return {
        "child": {
            "first_name": child.first_name,
            "grade_level": child.grade_level,
            "streak": {
                "current": current_streak,
                "longest": streak_data.get("longest_streak", 0),
                "is_today_complete": is_today_complete,
            },
            "recent_achievements": [
                {"title": a["title"], "icon": a.get("icon", ""), "earned_at": a.get("earned_at")}
                for a in achievements[:3]
            ],
        },
        "greeting": greeting,
        "today": {
            "total_activities": len(today_activities),
            "completed": completed_count,
            "estimated_minutes_remaining": remaining_minutes,
            "activities": activity_items,
        },
        "progress": {
            "overall_mastery_percentage": overall_pct,
            "nodes_mastered": mastered_count,
            "nodes_total": total_nodes,
            "subjects": subject_progress,
            "this_week": {
                "activities_completed": week_completed,
                "time_spent_minutes": week_minutes,
                "mastery_transitions_up": ups,
                "mastery_transitions_down": downs,
            },
        },
        "journey_maps": journey_maps,
        "encouragement": encouragement,
        "style_hints": style_hints,
    }
