"""Tests for calendar-aware materialization and live calendar re-flow.

Covers:
- Break-skip: activities never land on break dates; instructional week count
  is preserved (a break shifts dates / extends the end, it does not delete
  curriculum weeks).
- Cadence: a 4-day (Mon-Thu) and a Tue-Sat calendar place activities only on
  the configured instruction days.
- Immutability (the critical one): a calendar edit re-flows ONLY future,
  uncompleted, untouched weeks; completed / in-progress / past / same-day
  activities are preserved byte-for-byte, and governance_approved is NOT a
  lock signal.
- Live re-flow via PUT /household/academic-calendar emits the governance
  event with correct counts and shifts the future portion.
- Default/traditional calendar reproduces the pre-change ordinal placement
  for an all-future plan (no regression).
"""

from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.models.annual_curriculum import AnnualCurriculum
from app.models.enums import ActivityStatus, GovernanceAction
from app.models.governance import Activity, GovernanceEvent, Plan, PlanWeek
from app.services.annual_curriculum import (
    approve_annual_curriculum,
    reflow_curriculum_plan,
)


def _monday(d: date) -> date:
    """The Monday on or after d."""
    return d + timedelta(days=(7 - d.weekday()) % 7)


def _make_scope(num_weeks: int) -> dict:
    """Scope sequence with 5 Mon-Fri activities per week (authored cadence)."""
    weeks = []
    for w in range(1, num_weeks + 1):
        weeks.append(
            {
                "week_number": w,
                "title": f"Week {w}",
                "focus_nodes": [],
                "objectives": [f"Obj {w}"],
                "suggested_activities": [
                    {"title": f"Lesson {w}", "type": "lesson", "minutes": 25, "day": "Monday"},
                    {"title": f"Practice {w}", "type": "practice", "minutes": 20, "day": "Tuesday"},
                    {"title": f"Review {w}", "type": "review", "minutes": 15, "day": "Wednesday"},
                    {"title": f"Project {w}", "type": "project", "minutes": 30, "day": "Thursday"},
                    {"title": f"Assessment {w}", "type": "assessment", "minutes": 15, "day": "Friday"},
                ],
                "assessment_focus": f"Focus {w}",
            }
        )
    return {"overview": "ov", "weeks": weeks}


async def _set_calendar(db, household, **overrides) -> None:
    settings = dict(household.settings or {})
    settings["academic_calendar"] = {**settings.get("academic_calendar", {}), **overrides}
    household.settings = settings
    await db.flush()


async def _materialize(db, household, user, child, *, start_date, total_weeks) -> AnnualCurriculum:
    c = AnnualCurriculum(
        household_id=household.id,
        child_id=child.id,
        created_by=user.id,
        subject_name="Math",
        academic_year="2026-2027",
        total_weeks=total_weeks,
        hours_per_week=4.0,
        start_date=start_date,
        end_date=start_date + timedelta(weeks=total_weeks),
        scope_sequence=_make_scope(total_weeks),
        status="draft",
        actual_record={"weeks": {}},
    )
    db.add(c)
    await db.flush()
    await approve_annual_curriculum(db, c.id, user.id, household.id)
    return c


async def _plan_weeks(db, curriculum) -> list[PlanWeek]:
    plan = (await db.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum.id))).scalar_one()
    weeks = (
        (await db.execute(select(PlanWeek).where(PlanWeek.plan_id == plan.id).order_by(PlanWeek.week_number)))
        .scalars()
        .all()
    )
    return list(weeks)


async def _activities(db, week) -> list[Activity]:
    return list(
        (await db.execute(select(Activity).where(Activity.plan_week_id == week.id).order_by(Activity.sort_order)))
        .scalars()
        .all()
    )


class TestBreakSkip:
    @pytest.mark.asyncio
    async def test_break_week_is_skipped_and_count_preserved(self, db_session, household, child, user):
        start = _monday(date.today() + timedelta(days=60))
        # Break covers the whole calendar week that week 3 would occupy.
        brk_start = start + timedelta(days=14)
        brk_end = start + timedelta(days=18)
        await _set_calendar(
            db_session,
            household,
            breaks=[{"start": brk_start.isoformat(), "end": brk_end.isoformat()}],
        )

        c = await _materialize(db_session, household, user, child, start_date=start, total_weeks=5)
        weeks = await _plan_weeks(db_session, c)

        # Count preserved: a break does not delete curriculum weeks.
        assert len(weeks) == 5

        # Week 3 shifted past the break week (start+14 -> start+21).
        by_num = {w.week_number: w for w in weeks}
        assert by_num[3].start_date == start + timedelta(days=21)
        # Later weeks shifted by the same one week.
        assert by_num[4].start_date == start + timedelta(days=28)
        assert by_num[5].start_date == start + timedelta(days=35)

        # No activity anywhere lands inside the break.
        for w in weeks:
            for a in await _activities(db_session, w):
                assert not (brk_start <= a.scheduled_date <= brk_end)


class TestCadence:
    @pytest.mark.asyncio
    async def test_four_day_week_never_friday(self, db_session, household, child, user):
        start = _monday(date.today() + timedelta(days=60))
        await _set_calendar(
            db_session,
            household,
            instruction_days=["monday", "tuesday", "wednesday", "thursday"],
            instruction_days_per_week=4,
        )

        c = await _materialize(db_session, household, user, child, start_date=start, total_weeks=2)
        weeks = await _plan_weeks(db_session, c)

        for w in weeks:
            assert w.end_date.weekday() == 3  # Thursday
            for a in await _activities(db_session, w):
                assert a.scheduled_date.weekday() in {0, 1, 2, 3}
                assert a.scheduled_date.weekday() != 4  # never Friday

    @pytest.mark.asyncio
    async def test_tue_sat_cadence(self, db_session, household, child, user):
        start = _monday(date.today() + timedelta(days=60))
        await _set_calendar(
            db_session,
            household,
            instruction_days=["tuesday", "wednesday", "thursday", "friday", "saturday"],
            instruction_days_per_week=5,
        )

        c = await _materialize(db_session, household, user, child, start_date=start, total_weeks=2)
        weeks = await _plan_weeks(db_session, c)

        for w in weeks:
            for a in await _activities(db_session, w):
                # Tue(1)..Sat(5) only; never Monday(0) or Sunday(6).
                assert a.scheduled_date.weekday() in {1, 2, 3, 4, 5}


class TestImmutability:
    @pytest.mark.asyncio
    async def test_reflow_preserves_locked_activities_byte_for_byte(self, db_session, household, child, user):
        # Fixed Monday anchor + a fixed "today" inside week 3, so the
        # locked/future split is deterministic regardless of the run date.
        start = _monday(date(2026, 1, 5))
        today_ref = start + timedelta(days=16)  # Wednesday of week 3

        c = await _materialize(db_session, household, user, child, start_date=start, total_weeks=6)
        weeks = await _plan_weeks(db_session, c)
        by_num = {w.week_number: w for w in weeks}

        # Simulate real engagement on week 1 (locked by status as well as date).
        wk1_acts = await _activities(db_session, by_num[1])
        wk1_acts[0].status = ActivityStatus.completed
        wk1_acts[1].status = ActivityStatus.in_progress
        await db_session.flush()

        # Snapshot every activity in the preserved frontier (weeks 1-3), incl.
        # week 3's strictly-future Thu/Fri activities (preserved because their
        # week contains same-day/past locked siblings -> week granularity).
        def _snap(acts):
            return {a.id: (a.scheduled_date, a.status, a.governance_approved) for a in acts}

        locked_before = {}
        for wn in (1, 2, 3):
            locked_before[wn] = _snap(await _activities(db_session, by_num[wn]))

        # Materialization auto-approved every week (start is far in the past
        # relative to the real clock), so future weeks 4-6 carry
        # governance_approved=True. They must STILL re-flow: governance is not
        # a lock signal.
        wk4_before = await _activities(db_session, by_num[4])
        assert all(a.governance_approved for a in wk4_before)
        wk4_dates_before = {a.id: a.scheduled_date for a in wk4_before}

        # Edit the calendar: a break over week 4's original calendar window.
        new_cal = {
            "instruction_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "breaks": [
                {
                    "start": (start + timedelta(days=21)).isoformat(),
                    "end": (start + timedelta(days=25)).isoformat(),
                }
            ],
        }
        summary = await reflow_curriculum_plan(db_session, c, new_cal, user.id, today=today_ref)

        assert summary is not None
        assert summary["weeks_reflowed"] == 3  # weeks 4, 5, 6
        assert summary["weeks_preserved_locked"] == 3  # weeks 1, 2, 3

        # Locked frontier preserved byte-for-byte.
        weeks_after = await _plan_weeks(db_session, c)
        by_num_after = {w.week_number: w for w in weeks_after}
        for wn in (1, 2, 3):
            after = _snap(await _activities(db_session, by_num_after[wn]))
            assert after == locked_before[wn], f"week {wn} locked rows were mutated"
        # Week 3's stored dates unchanged too (whole-week preservation).
        assert by_num_after[3].start_date == by_num[3].start_date
        assert by_num_after[3].end_date == by_num[3].end_date

        # Future weeks re-flowed: week 4 moved past the break, never on it.
        assert by_num_after[4].start_date == start + timedelta(days=28)
        wk4_after = await _activities(db_session, by_num_after[4])
        for a in wk4_after:
            assert a.scheduled_date != wk4_dates_before[a.id]  # actually moved
            assert not (start + timedelta(days=21) <= a.scheduled_date <= start + timedelta(days=25))


class TestLiveReflowEndpoint:
    @pytest.mark.asyncio
    async def test_put_calendar_reflows_future_and_logs_event(self, auth_client, db_session, household, child, user):
        # All-future plan so the entire plan is re-flowable on a calendar edit.
        start = _monday(date.today() + timedelta(days=45))
        c = await _materialize(db_session, household, user, child, start_date=start, total_weeks=4)

        weeks_before = await _plan_weeks(db_session, c)
        assert all(w.end_date.weekday() == 4 for w in weeks_before)  # Friday ends

        resp = await auth_client.put(
            "/api/v1/household/academic-calendar",
            json={"instruction_days": ["monday", "tuesday", "wednesday", "thursday"]},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["reflow"], "expected re-flow summaries in the response"
        summary = next(s for s in body["reflow"] if s["curriculum_id"] == str(c.id))
        assert summary["weeks_reflowed"] == 4
        assert summary["weeks_preserved_locked"] == 0

        # Future weeks now end on Thursday (no Friday on a Mon-Thu cadence).
        weeks_after = await _plan_weeks(db_session, c)
        for w in weeks_after:
            assert w.end_date.weekday() == 3
            for a in await _activities(db_session, w):
                assert a.scheduled_date.weekday() != 4

        # Governance event emitted with correct counts.
        events = (
            (
                await db_session.execute(
                    select(GovernanceEvent).where(
                        GovernanceEvent.target_id == c.id,
                        GovernanceEvent.action == GovernanceAction.modify,
                    )
                )
            )
            .scalars()
            .all()
        )
        reflow_events = [e for e in events if (e.metadata_ or {}).get("event_type") == "calendar_reflow"]
        assert len(reflow_events) == 1
        assert reflow_events[0].metadata_["weeks_reflowed"] == 4
        assert reflow_events[0].metadata_["weeks_preserved_locked"] == 0
        assert reflow_events[0].metadata_["calendar_version"]

        # Snapshot refreshed on the curriculum.
        await db_session.refresh(c)
        assert c.calendar_version == reflow_events[0].metadata_["calendar_version"]


class TestDefaultCalendarRegression:
    @pytest.mark.asyncio
    async def test_default_calendar_matches_prior_ordinal_layout(self, db_session, household, child, user):
        start = date.today() + timedelta(days=45)  # all future, default calendar
        c = await _materialize(db_session, household, user, child, start_date=start, total_weeks=4)
        weeks = await _plan_weeks(db_session, c)

        day_offsets = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
        for w in weeks:
            expected_start = start + timedelta(weeks=w.week_number - 1)
            assert w.start_date == expected_start
            assert w.end_date == expected_start + timedelta(days=4)
            for a in await _activities(db_session, w):
                # sort_order indexes the authored Mon-Fri activities in order.
                day_name = list(day_offsets)[a.sort_order]
                assert a.scheduled_date == expected_start + timedelta(days=day_offsets[day_name])
