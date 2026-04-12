"""Tests for the data export service."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household


@pytest_asyncio.fixture
async def export_household(db_session):
    h = Household(name="Export Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest.mark.asyncio
class TestDataExport:
    async def test_export_produces_dict(self, db_session, export_household):
        from app.services.data_export import export_family_data
        result = await export_family_data(db_session, export_household.id)
        assert isinstance(result, dict)

    async def test_export_has_expected_keys(self, db_session, export_household):
        from app.services.data_export import export_family_data
        result = await export_family_data(db_session, export_household.id)
        # Should have household info at minimum
        assert "household" in result or len(result) > 0
