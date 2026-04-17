# METHEAN

![CI](https://github.com/zfava/METHEAN/actions/workflows/ci.yml/badge.svg)

**Learning governance operating system for homeschool families.**

METHEAN gives parents sovereign control over their children's education through AI-augmented curriculum planning, mastery tracking, and compliance management. Every AI recommendation flows through parent-defined governance rules before reaching the child.

## Vital Statistics

| Metric | Count |
|---|---|
| API endpoints | 216 (101 GET, 67 POST, 28 PUT, 8 PATCH, 12 DELETE) |
| Database tables | 51 (all RLS-scoped by household) |
| Alembic migrations | 30 |
| Test cases | 936 parametrized (141 test functions across 62 files) |
| Backend Python LOC | 59,200 |
| Frontend TypeScript LOC | 20,144 |
| Test LOC | 19,992 |
| Service modules | 39 |
| Background tasks | 14 |
| Pre-enriched content nodes | 115 (across 5 subjects) |
| Scope sequence subjects | 6 (mathematics, reading, literature, history, writing, science) |
| State compliance rules | 51 (all 50 states + DC) |
| AI agent roles | 8 |
| Frontend pages | 38 |

## What's in Scope

**Governance Gateway.** 8 AI roles (planner, tutor, evaluator, advisor, cartographer, education architect, content architect, curriculum mapper) with a centralized gateway. Circuit breaker pattern for provider reliability. SSE streaming for the tutor. Every AI output is a recommendation; parents approve or reject.

**DAG Curriculum Engine.** Adjacency list + transitive closure table in PostgreSQL. O(1) ancestor lookups for prerequisite enforcement. Cycle detection on write. Template system with pre-enriched content for 5 foundational subjects (115 nodes with teaching guidance, practice items, and assessment criteria).

**FSRS v6 Spaced Repetition.** Per-child card state with stability, difficulty, and retrievability tracking. Nightly decay batch job transitions mastered nodes back to proficient when retrievability drops below threshold. Idempotent (safe to run twice).

**51-State Compliance Engine.** Homeschool requirements for all 50 US states + DC: notification rules, required subjects, instruction hours, assessment options, record retention. Compliance check API compares household data against state requirements. Document generation: IHIP, quarterly reports, attendance records, transcripts (PDF output).

**5 Intelligence Engines.**
- Learner Intelligence: engagement patterns, pace trends, parent observations
- Calibration Engine: evaluator drift detection, directional bias correction, per-child recalibration
- Wellbeing Detection: 4 algorithms (broad disengagement, frustration spike, performance cliff, session avoidance) with parent-only visibility, self-calibrating thresholds, and empathetic messaging
- Family Intelligence: cross-child pattern detection (shared struggles, curriculum gaps, pacing divergence, environmental correlation, material effectiveness) with predictive scaffolding for younger siblings
- Style Vector Engine: learner style profiling with parent-overridable bounds

**Philosophical Profiles.** Classical, Charlotte Mason, Montessori, and traditional approaches. Philosophy-specific content in every pre-enriched node: different scaffolding, different resources, different assessment methods per approach.

**Parent Controls.** Governance rules (pace limits, content filters, schedule constraints, approval workflows). Manual activity creation. Reading logs. Nature journals. Notification preferences with quiet hours.

**Mobile PWA.** Service worker with stale-while-revalidate caching. Capacitor native shell for iOS/Android. Bottom tab bar, bottom sheets, swipe actions, pull-to-refresh, haptic feedback, offline banner.

## What's Not in Scope Yet

- **Billing dunning and failed payment recovery.** Stripe integration handles checkout, portal, and webhooks, but dunning sequences are not built.
- **Multi-language support.** All content and UI are English-only.
- **Native app store distribution.** The Capacitor shell builds but is not published to App Store or Google Play.
- **Real-time collaboration.** No simultaneous editing by multiple parents.
- **Student-to-student interaction.** METHEAN is a family tool, not a classroom or social platform.
- **Third-party curriculum import.** No SCORM, xAPI, or LTI integration.

## Tech Stack

### Backend

| Package | Version |
|---|---|
| Python | 3.12 |
| FastAPI | 0.115.6 |
| SQLAlchemy (async) | 2.0.36 |
| PostgreSQL | 16 |
| Redis | 7 (hiredis) |
| Celery | 5.4.0 |
| Alembic | 1.14.1 |
| Pydantic | 2.10.4 |
| FSRS | 6.3.1 |
| Sentry SDK | 2.0.0 |
| Prometheus | 0.21.1 |
| structlog | 24.4.0 |

### Frontend

| Package | Version |
|---|---|
| Next.js | 15.x |
| React | 19.x |
| TypeScript | 5.7.x |
| Tailwind CSS | 4.x |
| Capacitor | 6.x |

### Infrastructure

- Docker Compose (dev, staging, prod configurations)
- Nginx reverse proxy with TLS, rate limiting, SSE passthrough
- GitHub Actions CI: 5 jobs (backend tests, backend lint with pip-audit, frontend checks, migration verification, E2E with Playwright)

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/zfava/METHEAN.git
cd METHEAN
cp .env.example .env
# Edit .env: set JWT_SECRET (e.g., openssl rand -hex 32)
# AI_API_KEY is optional; the platform works without it via mock fallback

# 2. Start services
docker compose up -d
# Wait for postgres health check (~10 seconds)

# 3. Run migrations
docker compose exec backend alembic upgrade head

# 4. Verify
curl http://localhost:8000/health
# Expected: {"status": "ok"}

# 5. Seed demo data (optional)
docker compose exec backend python scripts/seed_demo.py

# 6. Open
# Backend API docs: http://localhost:8000/docs
# Frontend: http://localhost:3000
```

### Without Docker

```bash
# Requires: Python 3.12+, Node 20+, PostgreSQL 16, Redis 7
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

cd frontend
npm install
npm run dev
```

## Project Structure

```
METHEAN/
├── backend/
│   ├── app/
│   │   ├── ai/          # Gateway, prompts, provider chain, circuit breaker
│   │   ├── api/         # 216 FastAPI endpoints across 22 route modules
│   │   ├── content/     # Pre-enriched curriculum content (115 nodes, 5 subjects)
│   │   ├── core/        # Config, database, security, middleware, metrics
│   │   ├── models/      # 51 SQLAlchemy models (all RLS-scoped)
│   │   ├── schemas/     # Pydantic v2 request/response schemas
│   │   ├── services/    # 39 service modules (DAG engine, state engine, governance, compliance, intelligence)
│   │   └── tasks/       # 14 Celery tasks (decay, snapshots, enrichment, calibration, wellbeing, digests)
│   ├── alembic/         # 30 database migrations
│   ├── scripts/         # seed_demo.py, export_openapi.py
│   └── tests/           # 62 test files, 936 parametrized test cases
├── frontend/
│   └── src/
│       ├── app/         # 38 Next.js App Router pages (parent dashboard, child experience, onboarding)
│       ├── components/  # Shared UI (bottom sheet, swipe actions, pull-to-refresh, toast, offline banner)
│       └── lib/         # API client with retry, CSRF, SSE streaming, Capacitor bridge
├── docs/                # Architecture decisions, deployment checklist, runbook, SBOM, load test results
├── .github/workflows/   # CI (5 jobs), native builds, staging deploy
├── nginx/               # Reverse proxy config with TLS and rate limiting
├── docker-compose.yml
├── docker-compose.prod.yml
└── docker-compose.staging.yml
```

## Key Design Decisions

**AI never writes to state directly.** Every AI output is a recommendation routed through governance rules. Parents approve, reject, or modify before anything reaches the child. The GovernanceEvent table logs every decision.

**Append-only state history.** Every mastery change is an immutable StateEvent with trigger, from_state, to_state, and metadata. Current state (ChildNodeState) is the materialized view; the event stream is the source of truth.

**DAG-native curriculum.** LearningEdge adjacency list + LearningMapClosure transitive closure table. Closure is maintained on edge write. Prerequisite enforcement is a single query against the closure table.

**Row-Level Security.** PostgreSQL RLS policies on all 51 household-scoped tables. `SET LOCAL app.current_household_id` on every authenticated request via the `set_tenant()` function. RLS enforced at the database level, not the application level.

**Offline-first AI.** Deterministic mock AI fallback produces valid responses for all 8 roles when providers are unavailable. The platform never breaks due to AI downtime.

**Parent-only wellbeing data.** Wellbeing anomalies are never returned by child-facing endpoints. Detection algorithms use empathetic, non-blaming language. Thresholds self-calibrate based on parent dismissals (capped at +1.0 SD to prevent disabling detection).

## Testing

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app --cov-report=term-missing tests/

# Run a specific test file
pytest tests/test_compliance_engine.py -v

# 936 parametrized test cases covering:
# - Auth: token rotation, CSRF double-submit, RLS household isolation
# - Curriculum: DAG cycle detection, transitive closure, prerequisite enforcement
# - State engine: FSRS integration, cascade unblock, nightly decay, idempotency
# - Governance: rule evaluation, plan lifecycle, AI output inspection
# - Compliance: 51-state data integrity, check logic, document generation (PDF)
# - Intelligence: context assembly (70 tests), calibration, style vectors
# - Wellbeing: 4 detection algorithms, sensitivity config, dismissal thresholds
# - Family intelligence: 5 pattern types, cross-child detection, predictive scaffolding
# - Security: 61 protected routes verified, 3 public routes verified, CSRF enforcement
# - Background tasks: decay, snapshots, enrichment, batch operations
```

## CI Pipeline

5 parallel jobs on every push and PR:

1. **backend-tests**: pytest with PostgreSQL 16 service, coverage floor at 35%
2. **backend-lint**: ruff check + ruff format check + pip-audit
3. **frontend-checks**: TypeScript compilation + ESLint + Next.js build
4. **migration-check**: alembic upgrade head + downgrade to verify reversibility
5. **e2e-tests**: Playwright against the full stack

## Deployment

See [docs/deployment-checklist.md](docs/deployment-checklist.md) for the full production checklist.

```bash
# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Staging (offset ports, AI mock enabled)
docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

## License

Proprietary. All rights reserved. Copyright 2026 Spartan Solutions.

---

<details>
<summary>How to verify these numbers</summary>

```bash
# Endpoint count
grep -rE "^@router\.(get|post|put|patch|delete)" backend/app/api/ | wc -l

# Model/table count
grep -rn "__tablename__" backend/app/models/*.py | wc -l

# Test files and functions
find backend/tests -name "test_*.py" | wc -l
grep -rE "^(async )?def test_" backend/tests/ | wc -l

# Parametrized test cases (requires postgres for collection)
cd backend && python -m pytest tests/ --collect-only -q 2>&1 | tail -3

# Migration count
ls backend/alembic/versions/*.py | wc -l

# Frontend pages
find frontend/src/app -name "page.tsx" | wc -l

# Pre-enriched content nodes
grep -rE "^    \"[a-z]+-[0-9]+\":" backend/app/content/*_content.py | wc -l

# State compliance entries
grep -c "^    \"[A-Z][A-Z]\":" backend/app/services/compliance_engine.py

# LOC
find backend/app -name "*.py" | xargs wc -l | tail -1
find backend/tests -name "*.py" | xargs wc -l | tail -1
find frontend/src -name "*.ts" -o -name "*.tsx" | xargs wc -l | tail -1

# Service and task modules
ls backend/app/services/*.py | grep -v __init__ | wc -l
ls backend/app/tasks/*.py | grep -v __init__ | wc -l

# Banned-word and em-dash checks: run the verification
# commands from the Constraints section of the README
# generation prompt (not stored here to avoid false positives)
```

</details>
