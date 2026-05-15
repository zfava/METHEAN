# Developer environment

## Linting and pre-commit

The backend uses ruff for linting and formatting. CI fails on any ruff
violation in `backend/app/`.

To install the pre-commit hooks (one-time setup, run from the repo root):

```bash
pip install pre-commit
pre-commit install
```

After installation, ruff runs automatically on every commit and rewrites any
auto-fixable issues. The commit will fail if there are unfixable violations;
resolve them and commit again.

To run the checks manually:

```bash
cd backend
ruff check app/ --fix
ruff format app/
```

To run all pre-commit hooks against the full codebase:

```bash
pre-commit run --all-files
```

## Scope

The ruff hooks are restricted to `backend/app/**/*.py`, matching the CI
command (`ruff check app/ --output-format=github`). Files under
`backend/tests/` are not covered by the hook today; some pre-existing
violations remain and will be addressed in a follow-up.

## Hook reference

The `.pre-commit-config.yaml` at the repo root configures:

- `ruff` and `ruff-format` (astral-sh/ruff-pre-commit)
- `trailing-whitespace`, `end-of-file-fixer`, `check-merge-conflict`,
  `check-yaml`, `check-added-large-files` (pre-commit/pre-commit-hooks)

To upgrade pinned revisions:

```bash
pre-commit autoupdate
```
