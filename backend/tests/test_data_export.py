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
        import zipfile
        import io
        from app.services.data_export import export_family_data
        result = await export_family_data(db_session, export_household.id)
        assert isinstance(result, bytes)

    async def test_export_has_expected_keys(self, db_session, export_household):
        import zipfile
        import io
        from app.services.data_export import export_family_data
        result = await export_family_data(db_session, export_household.id)
        # result is a ZIP; verify it contains the expected top-level files
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            names = zf.namelist()
        assert "family_profile.json" in names
        assert len(names) > 0
