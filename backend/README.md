# METHEAN backend

Learning governance operating system for homeschool families. Governance-first, AI-augmented platform where parents govern and AI serves. Single pricing tier: $99/month. Built by METHEAN, Inc..

## Tech stack

- Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic
- PostgreSQL 16 with Row-Level Security (49 household-scoped tables with RLS policies)
- Redis 7: session cache, rate limiting, state caching (30s TTL)
- Celery with Redis broker for background work
- MinIO / S3-compatible object storage (artifact uploads, 50 MB max)
- Anthropic Claude + OpenAI (8 agent roles), FSRS v6 spaced repetition with per-child weight optimization
- Stripe for checkout, portal, and 5 webhook event types
- Observability: Sentry, Prometheus (5 custom metrics), structlog
- Auth: JWT dual-key rotation, CSRF double-submit, bcrypt, OIDC-ready
- ReportLab for PDF generation (IHIP, transcripts, quarterly reports, attendance records)
- Tests: pytest (730+ unit tests), 7 Playwright E2E specs, locust load tests

## Architecture (five systems)

1. **Curriculum engine**: DAG-based learning maps, nodes, edges, closure table, batch operations, content enrichment, template library, map-existing-curriculum import.
2. **Learner state engine**: FSRS v6 spaced repetition, mastery levels (not_started, emerging, developing, proficient, mastered), attempt workflow, retrievability tracking, per-child FSRS weight optimization (weekly Celery task).
3. **Governance system**: constitutional vs policy rule tiers, 5 rule types (pace_limit, content_filter, schedule_constraint, ai_boundary, approval_required), temporal triggers (age, mastery, date), governance queue, decision traces, parent attestation, philosophical profiles.
4. **Alert & evidence system**: stall detection, regression detection, pattern-failure detection, weekly snapshots, advisor reports, compliance reporting (51 state profiles).
5. **Operations layer**: notifications (in-app + daily email summaries), device registration, artifact storage, data export (ZIP), activity locking, sync protocol, Prometheus metrics.

## Key subsystems

- **Governance kernel**: constitutional rules cannot be modified without explicit confirmation; policy rules are parent-adjustable.
- **AI agent roles**: planner, evaluator, cartographer, tutor, advisor, enricher, compliance checker, wellbeing monitor.
- **Calibration**: evaluator prediction tracking, drift analysis, confidence distribution, per-subject calibration, parent override offsets.
- **Learner intelligence**: parent observations (parent's word is law), AI-accumulated profiles, parent override capability.
- **Family insights**: cross-child pattern detection with configurable sensitivity and actionable recommendations.
- **Wellbeing monitoring**: anomaly detection, parent-only visibility, configurable thresholds.
- **Education plans**: multi-year planning, per-year curriculum generation, annual curriculum with week-by-week scope/sequence.
- **Document generation**: IHIP (NY-style), quarterly reports, attendance records, transcripts (all PDF via ReportLab).
- **Academic calendar**: configurable schedule type, instruction days, breaks, daily target minutes.
- **Reading log**: book tracking, narration, parent notes, child ratings, reading statistics.

## API surface

Roughly 215 endpoints across the following route modules under `app/api/`:

auth, curriculum, state, governance, operations, spec_coverage, education_plan, assessment, compliance, annual_curriculum, feedback (activity feedback + reading log), resources, intelligence, calibration, style_vector, family_intelligence, wellbeing, billing, usage, notifications, documents, child_dashboard.

- Cookie-based auth: `access_token`, `refresh_token`, `csrf_token`.
- Pagination via `skip` / `limit` on all list endpoints (max 200).
- OWASP security headers applied by middleware.

## Project structure

```
backend/
  app/
    ai/        # gateway, prompts, cost controls (agent roles live here)
    api/       # FastAPI route handlers, one module per domain
    core/      # config, security, database, cache, middleware, metrics,
               # permissions, learning_levels, logging
    models/    # SQLAlchemy 2.0 models (identity, curriculum, state,
               # governance, evidence, operational, intelligence,
               # calibration, style_vector, family_insight, wellbeing,
               # achievements, education_plan, annual_curriculum, enums)
    schemas/   # Pydantic v2 request / response schemas
    services/  # business logic (dag_engine, state_engine, governance,
               # compliance_engine, planner, evaluator, alert_engine,
               # wellbeing_detection, family_intelligence, calibration,
               # content_engine, document_generator, data_export, ...)
    tasks/     # Celery: worker (entry point + beat schedule),
               # optimizer, temporal_rules, snapshots, decay, enrichment,
               # daily_summary, weekly_digest, check_alerts,
               # wellbeing_batch, family_intelligence_batch,
               # style_vector_batch, calibration_batch, curriculum_eval
  alembic/
    versions/  # migration chain
  scripts/     # seed_demo.py, export_openapi.py, load_test.py
  tests/
```

## Running locally

Service definitions live in the repository root `docker-compose.yml`.

```bash
# from repo root
cp .env.example .env

# start postgres, redis, minio
docker compose up -d

# backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# in a separate terminal, celery worker
celery -A app.tasks.worker worker -l info
```

Health check: `curl http://localhost:8000/health`. OpenAPI docs: `/docs`.

## Testing

Do not run the full suite casually; it takes 10+ minutes.

```bash
# full suite (~730 tests)
pytest

# RLS / household-isolation checks
pytest tests/test_security.py -xvs

# quick smoke
pytest -x --timeout=60

# specific file
pytest tests/test_governance.py -xvs

# Playwright E2E (from frontend/)
npx playwright test
```

Ruff is configured via `pyproject.toml`:

```bash
ruff check app/
ruff format --check app/
```

## Environment variables

See the repo-root `.env.example` for the full list. Required in any real environment:

- `DATABASE_URL` (async), `DATABASE_URL_SYNC` (for Alembic)
- `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY` (dual-key rotation)
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- `ANTHROPIC_API_KEY` (OpenAI key is optional; mock fallback if both are absent)
- `S3_ENDPOINT_URL`, plus S3 access keys and bucket
- `SENTRY_DSN` (optional; disabled if empty)

## Content-Security-Policy rollout

The production CSP issued by `SecurityHeadersMiddleware` drops
`'unsafe-eval'` and replaces `'unsafe-inline'` on `script-src` with
a per-request nonce (`X-CSP-Nonce` response header). The Next.js
layout should read that header and stamp the value onto its inline
scripts.

Rollout sequence:

1. Deploy with `CSP_ENFORCE=False` (default). The strict policy
   ships as `Content-Security-Policy-Report-Only` and violations are
   POSTed to `/api/v1/csp-report`, where the backend logs them via
   structlog under the `csp_violation` event.
2. Tail the report stream for at least one week. Investigate every
   `csp_violation` log line — if a legitimate vendor needs an
   allowlist entry, add it to the production CSP block in
   `app/core/middleware.py:SecurityHeadersMiddleware`.
3. Once the report stream is clean, flip `CSP_ENFORCE=True`. The
   browser starts rejecting violations instead of just reporting
   them.

Development mode keeps `'unsafe-eval' 'unsafe-inline'` and adds
`ws: wss:` to `connect-src` so Next.js HMR and React DevTools work.

## Migrations

Alembic lives at `backend/alembic/`. Migration files are numeric-prefixed and apply in order.

```bash
alembic upgrade head
alembic downgrade -1
alembic revision -m "add foo"
```

RLS policies are created in-migration (see `027_harden_rls_safe_settings.py` for the canonical policy template). Any new household-scoped table must `ENABLE / FORCE ROW LEVEL SECURITY` and add a matching `household_isolation` policy.

## License

Proprietary. Copyright 2026 METHEAN, Inc..
