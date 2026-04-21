"""Tests for home_state persistence on Household."""

import pytest


@pytest.mark.asyncio
async def test_household_update_saves_home_state(auth_client, db_session, household):
    """PUT /household/settings with home_state='UT' persists."""
    resp = await auth_client.put("/api/v1/household/settings", json={"home_state": "UT"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["home_state"] == "UT"


@pytest.mark.asyncio
async def test_household_update_validates_state_code(auth_client, db_session, household):
    """PUT /household/settings with home_state='XX' returns 422."""
    resp = await auth_client.put("/api/v1/household/settings", json={"home_state": "XX"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_household_get_returns_home_state(auth_client, db_session, household):
    """GET /household/settings includes home_state field."""
    # Set it first
    await auth_client.put("/api/v1/household/settings", json={"home_state": "TX"})
    # Then get
    resp = await auth_client.get("/api/v1/household/settings")
    assert resp.status_code == 200
    assert resp.json()["home_state"] == "TX"


@pytest.mark.asyncio
async def test_home_state_nullable(auth_client, db_session, household):
    """PUT /household/settings with home_state='' clears it."""
    await auth_client.put("/api/v1/household/settings", json={"home_state": "CA"})
    resp = await auth_client.put("/api/v1/household/settings", json={"home_state": ""})
    assert resp.status_code == 200
    assert resp.json()["home_state"] is None
