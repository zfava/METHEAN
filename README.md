# METHEAN

![CI](https://github.com/zfava/METHEAN/actions/workflows/ci.yml/badge.svg)

**Universal learning governance operating system.**

METHEAN runs the same learning-state engine under four different governance models: parent-governed (homeschool families), self-directed (college and adult learners), institution-governed (universities, bootcamps, corporate training), and mentor-governed (trade apprenticeships). Every AI recommendation flows through whichever governance authority owns the learner's household before it reaches the learner.

**Foundational principle.** Age never restricts access to content. Mastery of prerequisites is the sole gate. A 10-year-old who demonstrates PhD-level prerequisite mastery receives PhD-level content.

## Governance Modes

- **parent-governed.** Default for homeschool families. Parents own the governance queue; every AI plan, every content item, every rule change routes through parent approval (configurable by autonomy level).
- **self-directed.** A single user is both governor and learner (college students, adult learners, credential seekers). A linked Child record is auto-created at registration; the user approves their own plans or opts into full autonomy.
- **institution-governed.** A department admin bootstraps an organization, invites instructors, TAs, and students. Instructors operate at co-parent level on the curriculum; students see only their own progress (permission-scoped per learner).
- **mentor-governed.** Trade apprenticeship flow: a mentor governs OJT hours, competency sign-offs, and related instruction for their apprentice. Compliance maps to DOL apprenticeship formats.

## Vital Statistics

| Metric | Count |
|---|---|
| API endpoints | 220+ |
| Database tables | 51 (all RLS-scoped by household) |
| Alembic migrations | 35+ |
| Test cases | 950+ |
| Backend Python LOC | ~84,000 |
| Frontend TypeScript LOC | 20,144 |
| Service modules | 40+ |
| Background tasks | 14 |
| Pre-enriched content nodes | 115 (across 5 subjects) |
| State compliance rules | 51 (all 50 states + DC) |
| AI agent roles | 8 |
| Frontend pages | 38 |

## Universal Platform Features

- **Credit hour tracking.** Nodes carry `credit.hours`, `credit.type`, and `credit.contact_per_week` in their content JSONB. Per-map credit summaries roll up total, earned, remaining, and a by-type breakdown.
- **Grading scale abstraction.** Five built-in scales (letter, four-point, percentage, pass/fail, competency) plus caller-supplied custom scales. `get_grade(level, scale)` for translation; `compute_gpa(levels, hours)` for credit-weighted averages.
- **Multi-domain compliance.** Six compliance domains: `k12_homeschool` (delegates to the 51-state engine), `undergraduate` (credit hours + GPA minima), `graduate` (thesis + comprehensive exam), `professional_cert` (CEU tracking, renewal windows), `trade_apprentice` (OJT hours + competency signoffs, DOL format), `corporate` (mandatory completion, deadline enforcement).
- **Self-directed registration.** `POST /auth/register` with `is_self_learner=true` flips the household to `self_governed`, creates a linked Child, and wires the user as both governor and learner in one request.
- **Institutional multi-role.** `POST /auth/register-institution` creates an institution-governed household. `POST /auth/invite` supports `department_admin`, `instructor`, `teaching_assistant`, and `student` with the appropriate household-role mapping. Student permissions are scoped to the student's own learner record.
- **Cohort analytics.** `GET /learning-maps/{map_id}/cohort` produces class-wide mastery distribution, completion rate, and at-risk learner list for instructors and admins.
- **Higher-education node types.** Eight new `NodeType` values for higher-ed content: `lecture`, `reading`, `research`, `lab`, `thesis_component`, `exam_prep`, `peer_review`, `practicum`.
- **Expanded assessment types.** Seven new `AssessmentType` values for higher-ed: `timed_exam`, `research_paper`, `lab_report`, `oral_defense`, `peer_assessment`, `portfolio_review`, `clinical_evaluation`. Pydantic-validated at the API boundary.

## What's in Scope

**Governance Gateway.** 8 AI roles (planner, tutor, evaluator, advisor, cartographer, education architect, content architect, curriculum mapper) with a centralized gateway. Circuit breaker pattern for provider reliability. SSE streaming for the tutor. Every AI output is a recommendation; the governing authority (parent, self, instructor, mentor) approves or rejects.

**DAG Curriculum Engine.** Adjacency list plus transitive closure table in PostgreSQL. O(1) ancestor lookups for prerequisite enforcement. Cycle detection on write. Template system with pre-enriched content for 5 foundational subjects (115 nodes with teaching guidance, practice items, and assessment criteria).

**FSRS v6 Spaced Repetition.** Per-child card state with stability, difficulty, and retrievability tracking. Nightly decay batch job transitions mastered nodes back to proficient when retrievability drops below threshold. Idempotent (safe to run twice).

**51-State Compliance Engine.** Homeschool requirements for all 50 US states plus DC: notification rules, required subjects, instruction hours, assessment options, record retention. Compliance check API compares household data against state requirements. Document generation: IHIP, quarterly reports, attendance records, transcripts (PDF output).

**5 Intelligence Engines.**
- Learner Intelligence: engagement patterns, pace trends, governor observations.
- Calibration Engine: evaluator drift detection, directional bias correction, per-child recalibration.
- Wellbeing Detection: 4 algorithms (broad disengagement, frustration spike, performance cliff, session avoidance) with governor-only visibility, self-calibrating thresholds, and empathetic messaging.
- Family Intelligence: cross-child pattern detection (shared struggles, curriculum gaps, pacing divergence, environmental correlation, material effectiveness) with predictive scaffolding for younger siblings.
- Style Vector Engine: learner style profiling with governor-overridable bounds.

**Philosophical Profiles.** Classical, Charlotte Mason, Montessori, and traditional approaches. Philosophy-specific content in every pre-enriched node: different scaffolding, different resources, different assessment methods per approach. Prompt language adapts automatically to governance mode.

**Governance Controls.** Governance rules (pace limits, content filters, schedule constraints, approval workflows). Manual activity creation. Reading logs. Nature journals. Notification preferences with quiet hours.

**Mobile PWA.** Service worker with stale-while-revalidate caching. Capacitor native shell for iOS and Android. Bottom tab bar, bottom sheets, swipe actions, pull-to-refresh, haptic feedback, offline banner.

## What's Not in Scope Yet

- **Billing dunning and failed payment recovery.** Stripe integration handles checkout, portal, and webhooks, but dunning sequences are not built.
- **Multi-language support.** All content and UI are English-only.
- **Native app store distribution.** The Capacitor shell builds but is not published to App Store or Google Play.
- **Real-time collaboration.** No simultaneous editing by multiple governors.
- **Learner-to-learner interaction.** METHEAN is a governance tool, not a classroom or social platform.
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
│   │   ├── api/         # 220+ FastAPI endpoints across 22 route modules
│   │   ├── content/     # Pre-enriched curriculum content (115 nodes, 5 subjects)
│   │   ├── core/        # Config, database, security, middleware, metrics
│   │   ├── models/      # 51 SQLAlchemy models (all RLS-scoped)
│   │   ├── schemas/     # Pydantic v2 request/response schemas
│   │   ├── services/    # 40+ service modules (DAG, state, governance, compliance, grading, cohort)
│   │   └── tasks/       # 14 Celery tasks (decay, snapshots, enrichment, calibration, wellbeing, digests)
│   ├── alembic/         # 35+ database migrations
│   ├── scripts/         # seed_demo.py, export_openapi.py
│   └── tests/           # 950+ parametrized test cases
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

**AI never writes to state directly.** Every AI output is a recommendation routed through governance rules. The governing authority (parent, self, instructor, mentor) approves, rejects, or modifies before anything reaches the learner. The GovernanceEvent table logs every decision.

**Append-only state history.** Every mastery change is an immutable StateEvent with trigger, from_state, to_state, and metadata. Current state (ChildNodeState) is the materialized view; the event stream is the source of truth.

**DAG-native curriculum.** LearningEdge adjacency list plus LearningMapClosure transitive closure table. Closure is maintained on edge write. Prerequisite enforcement is a single query against the closure table.

**Row-Level Security.** PostgreSQL RLS policies on every household-scoped table. `SET LOCAL app.current_household_id` on every authenticated request via the `set_tenant()` function. RLS enforced at the database level, not the application level.

**Offline-first AI.** Deterministic mock AI fallback produces valid responses for all 8 roles when providers are unavailable. The platform never breaks due to AI downtime.

**Governor-only wellbeing data.** Wellbeing anomalies are never returned by learner-facing endpoints. Detection algorithms use empathetic, non-blaming language. Thresholds self-calibrate based on governor dismissals (capped at +1.0 SD to prevent disabling detection).

**Prompt language tracks governance mode.** The philosophical-constraints block that is injected into every AI system prompt swaps authority terms (parent, you, the institution, your mentor) and labels (`PARENT-LED TOPIC` vs `GOVERNOR-LED TOPIC`) based on `household.governance_mode`. Default is `parent_governed` to preserve existing output.

## Testing

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app --cov-report=term-missing tests/

# Run a specific test file
pytest tests/test_compliance_engine.py -v
```

Test areas:
- Auth: token rotation, CSRF double-submit, RLS household isolation, self-directed and institutional registration flows.
- Curriculum: DAG cycle detection, transitive closure, prerequisite enforcement, credit-hour tracking, cohort analytics.
- State engine: FSRS integration, cascade unblock, nightly decay, idempotency.
- Governance: rule evaluation, plan lifecycle, AI output inspection, self-governed auto-approve.
- Compliance: 51-state data integrity, check logic, document generation (PDF), multi-domain framework.
- Grading: scale translation, GPA computation.
- Intelligence: context assembly, calibration, style vectors.
- Wellbeing: 4 detection algorithms, sensitivity config, dismissal thresholds.
- Family intelligence: 5 pattern types, cross-child detection, predictive scaffolding.
- Security: protected routes verified, public routes verified, CSRF enforcement.
- Background tasks: decay, snapshots, enrichment, batch operations.

## CI Pipeline

5 parallel jobs on every push and PR:

1. **backend-tests**: pytest with PostgreSQL 16 service, coverage floor at 25%.
2. **backend-lint**: ruff check plus ruff format check plus pip-audit.
3. **frontend-checks**: TypeScript compilation plus ESLint plus Next.js build.
4. **migration-check**: alembic upgrade head plus downgrade to verify reversibility.
5. **e2e-tests**: Playwright against the full stack.

Triggered on pushes to `main` and any `claude/**` feature branch, and on pull requests to `main`.

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
```

</details>
