"""Verify the pinned OpenAPI spec matches the current app.

If this test fails, the spec file is out of date. Regenerate it with:

    cd backend && python -m scripts.export_openapi
"""

import json
from pathlib import Path

import pytest

SPEC_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "openapi.json"


@pytest.mark.asyncio
async def test_openapi_spec_is_current():
    from app.main import app

    if not SPEC_PATH.exists():
        pytest.fail(f"Pinned spec not found at {SPEC_PATH}. Run: cd backend && python -m scripts.export_openapi")

    pinned = json.loads(SPEC_PATH.read_text())
    current = app.openapi()

    # Compare just the paths and schemas — the parts that matter for contract testing.
    # Ignore info.version or description tweaks.
    pinned_paths = set(pinned.get("paths", {}).keys())
    current_paths = set(current.get("paths", {}).keys())

    missing = pinned_paths - current_paths
    added = current_paths - pinned_paths

    if missing or added:
        parts = []
        if missing:
            parts.append(f"Removed endpoints: {sorted(missing)}")
        if added:
            parts.append(f"New endpoints: {sorted(added)}")
        pytest.fail(
            "OpenAPI spec is out of date. " + "; ".join(parts) + "\n"
            "Regenerate: cd backend && python -m scripts.export_openapi"
        )

    # Deep-compare the full spec for schema changes
    if pinned != current:
        pytest.fail(
            "OpenAPI spec content has changed (schemas, parameters, or responses). "
            "Regenerate: cd backend && python -m scripts.export_openapi"
        )
