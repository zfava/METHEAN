#!/usr/bin/env python3
"""Fail CI if coverage on high-trust modules drops below 85 percent.

The global coverage floor (currently 50%) is a project-wide signal,
but the modules that gate authentication, payments, and authorization
need a much tighter bar. This script reads ``coverage.json`` (which
``pytest --cov-report=json`` produces) and exits non-zero when any
high-trust file is below the floor.

Modules that are listed but absent from the report (because the
branch hasn't shipped them yet, or they were removed) emit a warning
rather than failing — the call site is the place to track the gap.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HIGH_TRUST: list[str] = [
    "app/api/auth.py",
    "app/api/deps.py",
    "app/api/billing.py",
    "app/services/email_verification.py",
    "app/services/password_reset.py",
]
FLOOR = 85.0


def main() -> int:
    # CI runs `pytest --cov-report=json` which writes coverage.json
    # directly; only regenerate if it's missing. We pass --fail-under=0
    # to the regen path so the global threshold doesn't make this
    # helper fail before it has a chance to print its own report.
    report = Path("coverage.json")
    if not report.exists():
        subprocess.run(
            ["coverage", "json", "-o", "coverage.json", "--fail-under=0"],
            check=True,
        )
    data = json.loads(report.read_text())
    files = data["files"]

    failures: list[str] = []
    missing: list[str] = []
    for path in HIGH_TRUST:
        if path not in files:
            missing.append(path)
            continue
        pct = files[path]["summary"]["percent_covered"]
        if pct < FLOOR:
            failures.append(f"{path}: {pct:.1f} percent (floor {FLOOR})")

    if missing:
        print("WARN high-trust modules absent from coverage report:")
        for m in missing:
            print(f"  - {m}")

    if failures:
        print("High-trust coverage below floor:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("High-trust coverage OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
