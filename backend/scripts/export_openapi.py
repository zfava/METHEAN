"""Export the FastAPI OpenAPI spec to docs/openapi.json and docs/openapi.yaml.

Run: python -m scripts.export_openapi
"""

import json
from pathlib import Path

import yaml

from app.main import app

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs"


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    spec = app.openapi()

    json_path = DOCS_DIR / "openapi.json"
    json_path.write_text(json.dumps(spec, indent=2, default=str) + "\n")
    print(f"Wrote {json_path}")

    yaml_path = DOCS_DIR / "openapi.yaml"
    yaml_path.write_text(yaml.dump(spec, default_flow_style=False, sort_keys=False, allow_unicode=True))
    print(f"Wrote {yaml_path}")


if __name__ == "__main__":
    main()
