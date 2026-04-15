"""Tests for the data export service."""

import io
import json
import zipfile

import pytest
import pytest_asyncio

from app.core.security import hash_password
from app.models.identity import Child, Household, User


@pytest_asyncio.fixture
async def export_household(db_session):
    h = Household(name="Export Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def export_user(db_session, export_household):
    u = User(
        household_id=export_household.id,
        email="export@test.com",
        password_hash=hash_password("testpass123"),
        display_name="Export Parent",
        role="owner",
    )
    db_session.add(u)
    await db_session.flush()
    return u


@pytest_asyncio.fixture
async def export_child(db_session, export_household):
    c = Child(household_id=export_household.id, first_name="ExportKid")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest.mark.asyncio
class TestDataExport:
    async def test_export_produces_zip(self, db_session, export_household):
        from app.services.data_export import export_family_data

        result = await export_family_data(db_session, export_household.id)
        assert isinstance(result, bytes)
        assert result[:2] == b"PK"  # ZIP magic bytes

    async def test_export_has_expected_files(self, db_session, export_household):
        from app.services.data_export import export_family_data

        result = await export_family_data(db_session, export_household.id)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            names = zf.namelist()
        assert "family_profile.json" in names
        assert "metadata.json" in names
        assert "governance_rules.json" in names

    async def test_export_includes_household_name(self, db_session, export_household):
        from app.services.data_export import export_family_data

        result = await export_family_data(db_session, export_household.id)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            profile = json.loads(zf.read("family_profile.json"))
        assert profile["name"] == "Export Test"

    async def test_export_includes_children(self, db_session, export_household, export_child):
        from app.services.data_export import export_family_data

        result = await export_family_data(db_session, export_household.id)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            names = zf.namelist()
        # Child data should be in a child-named directory
        assert any("exportkid" in n.lower() for n in names)

    async def test_export_excludes_password_hashes(self, db_session, export_household, export_user):
        from app.services.data_export import export_family_data

        result = await export_family_data(db_session, export_household.id)
        # Scan entire ZIP content for password hash patterns
        content = result.decode("latin-1")  # binary-safe decode
        assert "password_hash" not in content
        assert "$2b$" not in content  # bcrypt prefix

    async def test_export_requires_auth(self, client):
        resp = await client.post("/api/v1/household/export")
        assert resp.status_code == 401

    async def test_export_metadata_has_version(self, db_session, export_household):
        from app.services.data_export import export_family_data

        result = await export_family_data(db_session, export_household.id)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            meta = json.loads(zf.read("metadata.json"))
        assert "methean_version" in meta
        assert meta["methean_version"] == "0.1.0"
