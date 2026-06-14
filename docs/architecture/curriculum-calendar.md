# Calendar-aware curriculum materialization

This document describes how an annual curriculum is laid onto real school days,
and how a parent's edit to the household academic calendar re-flows the future,
uncompleted portion of an already-materialized plan.

## The household academic calendar

The per-household calendar lives in `Household.settings["academic_calendar"]`
(JSONB), read and merged with `DEFAULT_CALENDAR` by
`app.services.academic_calendar.get_academic_calendar`. It carries:

- `start_date`, `total_instructional_weeks`
- `instruction_days` (the weekly cadence, e.g. Monday-Friday, Monday-Thursday,
  or Tuesday-Saturday) and `instruction_days_per_week`
- `breaks`: a list of `{start, end}` ranges
- `schedule_type` in `{traditional, year_round, custom}`
- `daily_target_minutes` per grade band

It is edited through `GET/PUT /household/academic-calendar`
(`app.api.academic_calendar`).

## Materialization honors the calendar

`materialize_full_year` (`app.services.annual_curriculum`) loads the calendar at
approval time and lays weeks/days onto real instruction dates via `_lay_weeks`,
mirroring the weekly planner's calendar handling
(`is_break_date` + `instruction_days`):

- Each curriculum week consumes the next calendar week whose instruction days
  are not all inside a break. A fully-break calendar week is skipped and does
  not consume a curriculum week, so a break shifts dates and extends the
  calendar end without ever deleting a curriculum week (the instructional week
  count is preserved).
- An activity's authored day name is mapped onto the configured instruction
  days by `_place_offset`. If the authored day is an instruction day the
  activity lands on it exactly; otherwise it is clamped to the nearest available
  instruction day (a Friday activity on a Monday-Thursday cadence lands on
  Thursday). Activities never land on a non-instruction or break day.
- A default Monday-Friday calendar reproduces the prior ordinal placement
  exactly (`week_start = start_date + 7 * (week_number - 1)`), so the common
  case does not regress.

The resolved calendar is snapshotted onto the curriculum
(`AnnualCurriculum.calendar_snapshot`) with a stable hash
(`calendar_version`, migration 063), so a later edit can detect drift and
re-flow deterministically.

## Live re-flow on a calendar edit

When the calendar is saved (`PUT /household/academic-calendar`),
`reflow_household_active_curricula` applies the edit to every active
curriculum's plan, re-dating only the future, uncompleted portion.

### The immutability predicate

An activity is RE-FLOWABLE (its date may be recomputed) only when all hold:

- `status == scheduled`
- `scheduled_date > today` (an activity scheduled for today is treated as
  locked; same-day work is never re-flowed)

An activity is LOCKED (preserved byte-for-byte: id, scheduled_date, status, and
governance fields untouched) when its status is `in_progress`, `completed`,
`skipped`, or `cancelled`, or its `scheduled_date <= today`.

`governance_approved` is deliberately NOT a lock signal. It is set automatically
by the near-window auto-approval at materialization, so it does not represent a
deliberate parent lock; using it would pin the parent's own calendar edits in
the common editing case.

### Week granularity and ordering

Re-flow operates per week. A `PlanWeek` is re-flowable only when it has
activities and every non-cancelled one is re-flowable; any week containing a
locked activity keeps its stored dates entirely. Only weeks strictly after the
last preserved week are re-dated, walking the calendar forward from the end of
that week, so a locked week never collides with a re-dated one and dates stay
monotonic. Cancelled activities inside a re-flowed week are left untouched.

Each plan that actually moves emits a `modify` governance event carrying the
`calendar_version`, `weeks_reflowed`, and `weeks_preserved_locked`, and its
curriculum snapshot is refreshed to the new calendar.

## Out of scope (follow-up work)

- FSRS / spaced-review break pausing: due dates still run on wall-clock time.
- Frontend de-hardcoding: the calendar and year-plan pages still assume a
  Monday-Friday grid (`app.api.annual_curriculum` also still has a hardcoded
  day table in `add_activity_to_week`).
