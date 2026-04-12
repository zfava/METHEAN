"""Tests for academic calendar service and API."""

from datetime import date

import pytest
from app.services.academic_calendar import (
    DEFAULT_CALENDAR,
    calculate_end_date,
    get_daily_minutes_for_grade,
    get_instruction_days,
    is_break_date,
)


class TestCalendarService:

    def test_default_is_traditional(self):
        """Default calendar is 36 weeks Mon-Fri."""
        assert DEFAULT_CALENDAR["total_instructional_weeks"] == 36
        assert DEFAULT_CALENDAR["instruction_days_per_week"] == 5
        assert "monday" in DEFAULT_CALENDAR["instruction_days"]
        assert "saturday" not in DEFAULT_CALENDAR["instruction_days"]

    def test_instruction_days(self):
        """Instruction days read from calendar."""
        cal = {**DEFAULT_CALENDAR, "instruction_days": ["monday", "tuesday", "wednesday", "thursday"]}
        assert get_instruction_days(cal) == ["monday", "tuesday", "wednesday", "thursday"]

    def test_daily_minutes_by_grade(self):
        """Grade-based daily minute targets."""
        assert get_daily_minutes_for_grade(DEFAULT_CALENDAR, "K") == 90
        assert get_daily_minutes_for_grade(DEFAULT_CALENDAR, "3rd") == 120
        assert get_daily_minutes_for_grade(DEFAULT_CALENDAR, "7th") == 150
        assert get_daily_minutes_for_grade(DEFAULT_CALENDAR, "10th") == 180

    def test_break_detection(self):
        """Break date detection."""
        cal = {**DEFAULT_CALENDAR, "breaks": [
            {"name": "Christmas", "start": "2026-12-20", "end": "2027-01-03"},
        ]}
        assert is_break_date(cal, date(2026, 12, 25)) is True
        assert is_break_date(cal, date(2026, 12, 15)) is False
        assert is_break_date(cal, date(2027, 1, 3)) is True
        assert is_break_date(cal, date(2027, 1, 4)) is False

    def test_end_date_no_breaks(self):
        """End date calculation without breaks."""
        start = date(2026, 8, 17)  # Monday
        end = calculate_end_date(start, 36, DEFAULT_CALENDAR)
        # 36 weeks of 5-day instruction spans ~245-260 calendar days
        assert (end - start).days >= 240
        assert (end - start).days <= 270

    def test_end_date_with_breaks(self):
        """End date extends when breaks are included."""
        start = date(2026, 8, 17)
        cal_no_breaks = {**DEFAULT_CALENDAR, "breaks": []}
        cal_with_breaks = {**DEFAULT_CALENDAR, "breaks": [
            {"name": "Break", "start": "2026-10-12", "end": "2026-10-18"},  # 1 week break
        ]}
        end_no = calculate_end_date(start, 36, cal_no_breaks)
        end_with = calculate_end_date(start, 36, cal_with_breaks)
        assert end_with > end_no


class TestCalendarAPI:

    @pytest.mark.asyncio
    async def test_get_default_calendar(self, auth_client):
        """GET returns defaults for a new household."""
        resp = await auth_client.get("/api/v1/household/academic-calendar")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_instructional_weeks"] == 36
        assert data["instruction_days_per_week"] == 5

    @pytest.mark.asyncio
    async def test_update_calendar(self, auth_client):
        """PUT saves calendar preferences."""
        resp = await auth_client.put("/api/v1/household/academic-calendar", json={
            "schedule_type": "year_round",
            "total_instructional_weeks": 42,
            "instruction_days_per_week": 4,
            "instruction_days": ["monday", "tuesday", "wednesday", "thursday"],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_instructional_weeks"] == 42
        assert data["instruction_days_per_week"] == 4

    @pytest.mark.asyncio
    async def test_validate_weeks_range(self, auth_client):
        """Reject weeks outside 1-52."""
        resp = await auth_client.put("/api/v1/household/academic-calendar", json={
            "total_instructional_weeks": 0,
        })
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_validate_invalid_day(self, auth_client):
        """Reject invalid day names."""
        resp = await auth_client.put("/api/v1/household/academic-calendar", json={
            "instruction_days": ["moonday"],
        })
        assert resp.status_code == 400
