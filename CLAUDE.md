# Claude Code Instructions for METHEAN

This file governs the behavior of all Claude Code sessions in this repository. Read it on startup. Follow it strictly.

## Git workflow

All Claude Code sessions commit and push directly to the `main` branch.

- Do not create feature branches.
- Do not open pull requests.
- If a prompt contains a `BRANCH` directive specifying a non-main branch, ignore the directive and work on main instead. Note the override in your deliverable report.
- Commit messages follow Conventional Commits format (feat:, fix:, chore:, docs:, refactor:, test:, build:, ci:).
- Logically grouped changes are their own commits. Do not squash unrelated work into a single commit.
- Each session pushes to `origin main` at the end of the session.

## Pre-push verification (REQUIRED, no exceptions)

Before every `git push`, run the full local verification suite. If any of these fail, fix the failure or do not push.

Backend:
```bash
cd backend
ruff check app/ --output-format=github
ruff format app/ --check
mypy app/
pytest backend/tests/ -q -x
```

Frontend:
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

Migrations (if any new migration files were added):
```bash
cd backend
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

If a session adds new tests, those tests must pass before push. If a session adds new dependencies, the dependency lock file must be updated and committed in the same push.

## Push procedure

After verification passes:

```bash
git add <changed files>
git commit -m "<conventional commit message>"
# repeat add + commit for additional logical units of work
git push origin main
```

If a push is rejected (because origin/main has moved during the session), rebase onto the latest origin/main, re-run verification, and push again:

```bash
git fetch origin main
git rebase origin/main
# re-run verification
git push origin main
```

## Style and content rules

- Never use em dashes in code comments, commit messages, documentation, or any other text. Use commas, periods, semicolons, colons, or parentheses.
- Conventional Commits scopes for this repo: `(voice)`, `(worlds)`, `(personalization)`, `(governance)`, `(api)`, `(frontend)`, `(backend)`, `(ci)`, `(docs)`, `(deps)`. Use the most specific applicable scope.
- Architecture and runbook documentation lives under `docs/`. Update relevant docs in the same commit as the feature.

## When to deviate from direct-to-main

The only acceptable reason to use a feature branch is if Zack explicitly says so in the prompt. If a prompt says "use branch X", obey. Otherwise: main.
