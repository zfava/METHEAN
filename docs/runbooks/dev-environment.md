# Developer environment

Setup notes for working on this repository locally. CI mirrors these
checks, so the goal is to catch failures on your machine before they
land on the build server.

## Linting and pre-commit

The backend uses ruff for linting and formatting. CI fails on any ruff
violation (`ruff check app/` and `ruff format --check app/`), so the
pre-commit hooks are the first line of defense.

### One-time setup

Install pre-commit and wire the hooks into your local git repository:

```bash
pip install pre-commit
pre-commit install
```

`pre-commit install` writes a hook into `.git/hooks/pre-commit`. After
that, ruff runs automatically on every commit, rewrites any
auto-fixable issues in place, and the commit fails if there are
unfixable violations. Resolve them and commit again.

### Manual runs

To run the ruff checks on the backend by hand:

```bash
cd backend
ruff check app/ --fix
ruff format app/
```

To run the full pre-commit suite (ruff plus trailing whitespace,
end-of-file-fixer, merge-conflict markers, YAML syntax, large file
guard) against every tracked file:

```bash
pre-commit run --all-files
```

### What the hooks do

The pinned hooks (see `.pre-commit-config.yaml`):

- `ruff` with `--fix`: import sorting, common style fixes, lints.
- `ruff-format`: opinionated formatting, equivalent to black.
- `trailing-whitespace`, `end-of-file-fixer`: portable whitespace
  normalization. Test fixtures under `backend/tests/fixtures/` are
  excluded because they may contain binary or whitespace-sensitive
  content.
- `check-merge-conflict`: blocks commits that still contain
  `<<<<<<<` markers.
- `check-yaml`: parses every YAML file.
- `check-added-large-files`: refuses commits adding files larger than
  10 MB. Audio test fixtures can approach this; raise the limit if a
  legitimately large fixture is needed.

### Updating hook versions

```bash
pre-commit autoupdate
```

Commit the resulting `.pre-commit-config.yaml` change. Re-run
`pre-commit run --all-files` to confirm no new violations surfaced
under the newer hook versions.

## Backend Python environment

Install backend dependencies into a virtual environment:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install ruff bandit pre-commit
```

The CI workflow installs the same `requirements.txt` plus
`pytest-cov`, `ruff`, and `bandit`, then runs `ruff check app/
--output-format=github` and `ruff format --check app/`. Reproduce the
exact CI lint step locally with:

```bash
cd backend
ruff check app/ --output-format=github
ruff format --check app/
```

Both commands should exit 0.
