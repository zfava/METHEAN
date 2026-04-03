# METHEAN

**Learning governance operating system for homeschool families.**

METHEAN is an AI-augmented platform that gives parents sovereign control over their children's education. It combines DAG-based curriculum maps, FSRS v6 spaced repetition, and an AI governance gateway where every AI recommendation flows through parent-defined rules before reaching the child.

## Architecture

- **System 1: Curriculum Architecture** — DAG-based learning maps with prerequisite enforcement and transitive closure
- **System 2: Learner State Engine** — FSRS v6 spaced repetition with per-child weight optimization
- **System 3: Parent Governance** — Rule-based AI oversight (pace limits, content filters, schedule constraints, approval workflows)
- **System 4: Evidence & Feedback** — Alerts, weekly snapshots, AI advisor reports, artifact storage
- **System 5: Operations** — Audit logs, notifications, compliance reporting

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL 16, Redis 7, Celery 5
- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS 4
- **AI:** Claude (primary), OpenAI (fallback), deterministic mock (offline)
- **Infrastructure:** Docker Compose, Alembic migrations, RLS multi-tenancy

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env: set JWT_SECRET to a random string (e.g., openssl rand -hex 32)
# Optionally add AI_API_KEY for live AI features (works without it via mock)

# 2. Start all services
docker compose up -d

# 3. Run database migrations
docker compose exec backend alembic upgrade head

# 4. Seed demo data (optional)
docker compose exec backend python scripts/seed_demo.py

# 5. Open the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# Demo login: zack@methean.app / demo123
```

## API Documentation

- **Interactive docs:** http://localhost:8000/docs (Swagger UI)
- **Pinned OpenAPI spec:** [`docs/openapi.json`](docs/openapi.json)
- **76 endpoints** across auth, curriculum, state, governance, AI, and operations

## Project Structure

```
methean/
├── backend/
│   ├── app/
│   │   ├── ai/          # AI gateway, prompts, provider chain
│   │   ├── api/         # FastAPI route handlers
│   │   ├── core/        # Config, database, security, middleware
│   │   ├── models/      # SQLAlchemy models (29 tables)
│   │   ├── schemas/     # Pydantic v2 request/response schemas
│   │   ├── services/    # Business logic (DAG engine, state engine, governance, planner)
│   │   └── tasks/       # Celery tasks (decay, snapshots, FSRS optimizer)
│   ├── alembic/         # Database migrations
│   ├── scripts/         # seed_demo.py, export_openapi.py
│   └── tests/           # 177 tests across 9 test files
├── frontend/
│   └── src/
│       ├── app/         # Next.js App Router pages
│       ├── components/  # Shared UI components
│       └── lib/         # API client with retry + CSRF
├── docs/                # Pinned OpenAPI spec (JSON + YAML)
├── docker-compose.yml
└── docker-compose.prod.yml
```

## Key Design Decisions

- **AI never writes to state directly.** Every AI output is a recommendation routed through governance rules.
- **Append-only state history.** Every mastery change is an immutable StateEvent. Current state is the materialized view; the event stream is the source of truth.
- **DAG-native curriculum.** Adjacency list + transitive closure table in PostgreSQL. O(1) ancestor lookups for prerequisite enforcement.
- **Zero-trust tenant isolation.** PostgreSQL RLS on every household-scoped table, activated via SET LOCAL on every authenticated request.
- **System works offline.** Deterministic mock AI fallback means the platform never breaks when providers are unavailable.

## Testing

```bash
cd backend

# Run all tests
DATABASE_URL=postgresql+asyncpg://methean:methean_dev@localhost:5432/methean \
REDIS_URL=redis://localhost:6379/0 \
pytest tests/ -v

# 177 tests covering:
# - Auth (token rotation, CSRF, RLS isolation)
# - Curriculum (cycle detection, transitive closure, prerequisite enforcement)
# - State engine (FSRS integration, cascade unblock, decay)
# - Governance (rule evaluation, plan lifecycle, AI inspection)
# - Operations (alerts, notifications, snapshots, compliance)
# - OpenAPI spec contract test
```

## License

Proprietary. All rights reserved.
