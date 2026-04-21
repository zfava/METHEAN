# METHEAN Operational Runbook

## Deployment

### Local Development
```bash
cp .env.example .env  # Edit with your values
docker compose up -d
cd backend && alembic upgrade head
cd frontend && npm run dev
```

### Staging
```bash
cp .env.staging.example .env.staging  # Edit with staging values
docker compose -f docker-compose.staging.yml up -d
docker compose -f docker-compose.staging.yml exec backend alembic upgrade head
# Seed demo data:
docker compose -f docker-compose.staging.yml exec backend python scripts/seed_demo.py
```

### Production (Railway)
- Push to `main` branch triggers Railway auto-deploy
- Ensure all env vars are set in Railway dashboard
- Run migrations via Railway CLI: `railway run alembic upgrade head`

## Rollback

### Database
```bash
# Check current version
alembic current
# Rollback one migration
alembic downgrade -1
# Rollback to specific version
alembic downgrade 025
```

### Application
- Revert the git commit and push to trigger redeploy
- Or use Railway's rollback feature to restore previous deployment

## Health Checks

### API Health
```bash
curl http://localhost:8000/health
# Returns: {"status": "ok", "service": "methean"}

curl http://localhost:8000/health/ready
# Returns: {"status": "ok", "checks": {"api": "ok", "database": "ok", "redis": "ok", "celery": "ok"}}
```

### Metrics
```bash
curl http://localhost:8000/metrics
# Returns Prometheus-format metrics including:
#   http_requests_total, http_request_duration_seconds
#   methean_ai_calls_total, methean_attempts_completed_total
```

## Accessing Logs

### Docker
```bash
docker compose logs backend --tail 100 -f
docker compose logs celery-worker --tail 100 -f
docker compose logs celery-beat --tail 50 -f
```

### Structured Log Format
All logs use structlog JSON format. Key fields: `event`, `level`, `timestamp`, `request_id`.

Filter errors:
```bash
docker compose logs backend | jq 'select(.level == "error")'
```

## Database Operations

### Run Migrations
```bash
docker compose exec backend alembic upgrade head
```

### Check Migration Status
```bash
docker compose exec backend alembic current
docker compose exec backend alembic history --verbose
```

### Backup (PostgreSQL)
```bash
docker compose exec postgres pg_dump -U methean methean > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
cat backup_20260414.sql | docker compose exec -T postgres psql -U methean methean
```

## Redis Operations

### Check Cache Keys
```bash
docker compose exec redis redis-cli KEYS "child_state:*"
docker compose exec redis redis-cli KEYS "gov_queue:*"
```

### Flush Cache (safe — advisory cache only)
```bash
docker compose exec redis redis-cli FLUSHDB
```

## Celery Tasks

### Check Worker Status
```bash
docker compose exec celery-worker celery -A app.tasks.worker inspect active
docker compose exec celery-worker celery -A app.tasks.worker inspect scheduled
```

### Manually Trigger a Task
```bash
docker compose exec backend python -c "
from app.tasks.worker import celery_app
celery_app.send_task('app.tasks.worker.nightly_decay_task')
"
```

### Scheduled Tasks
| Task | Schedule | Purpose |
|------|----------|---------|
| nightly_decay_task | Daily 2:00 AM | FSRS mastery decay check |
| nightly_calibration_task | Daily 3:00 AM | Evaluator calibration recompute |
| nightly_style_vector_task | Daily 3:30 AM | Learning style vector recompute |
| nightly_family_intelligence_task | Daily 4:00 AM | Cross-child pattern detection |
| nightly_wellbeing_task | Daily 4:30 AM | Wellbeing anomaly detection |
| daily_summary_task | Daily 7:00 PM | Daily email summary |
| weekly_digest_task | Sunday 10:00 AM | Weekly digest email |
| weekly_snapshot_task | Sunday 2:00 AM | Weekly progress snapshots |

## Incident Response

### High Error Rate
1. Check `/health/ready` — identify which component is failing
2. Check Sentry for error details and stack traces
3. Check `docker compose logs backend --tail 200` for recent errors
4. If database: `docker compose exec postgres psql -U methean -c "SELECT count(*) FROM pg_stat_activity;"`
5. If Redis: `docker compose exec redis redis-cli INFO clients`
6. If Celery: check worker logs, may need restart

### AI Provider Down
- The AI gateway has 3-tier fallback: Claude → OpenAI → Mock
- If both live providers are down, the mock returns deterministic responses
- No child-facing features break — they just get generic content
- Check AI_MOCK_ENABLED env var

### Database Full
```bash
docker compose exec postgres psql -U methean -c "SELECT pg_size_pretty(pg_database_size('methean'));"
docker compose exec postgres psql -U methean -c "
  SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
  FROM pg_catalog.pg_statio_user_tables
  ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;
"
```

### Rate Limiting Issues
```bash
# Check current rate limit state in Redis
docker compose exec redis redis-cli KEYS "ratelimit:*"
# Clear rate limits for a specific IP
docker compose exec redis redis-cli DEL "ratelimit:192.168.1.1:$(date +%s | head -c 10)"
```

### RLS (Row Level Security) Issues
If queries return empty results unexpectedly:
```bash
# Check if RLS is enabled
docker compose exec postgres psql -U methean -c "SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname='public' AND rowsecurity=true;"
# Check current tenant variable
docker compose exec postgres psql -U methean -c "SELECT current_setting('app.current_household_id', true);"
```

## CI Gates and What Each Catches

Five gates run on every push and PR. Each prevents a specific class of regression.

| Gate | CI Step | What It Catches |
|---|---|---|
| **Migration round-trip** | `migration-check` job: upgrade head, downgrade base, re-upgrade | Migrations that work on an existing DB but fail on a fresh DB (duplicate indexes, missing tables, non-reversible DDL) |
| **Route contract** | `Route contract check` in backend-tests: `pytest tests/test_route_contract.py` | Tests that reference routes by string that do not actually exist (wrong path, wrong method, stale route list). Catches 404/405 failures before they become auth-test false negatives. |
| **Route auth contract** | `Route auth contract check` in backend-tests: `pytest tests/test_unauthenticated_paths.py` | Protected endpoints that accidentally lose auth (return 200 instead of 401), public endpoints that accidentally gain auth (return 401 instead of 200), and method mismatches on auth-tested routes. |
| **Coverage floor** | `coverage report --fail-under=35` in backend-tests | Test coverage regressions below 35%. The floor is raised periodically as coverage improves. |
| **E2E smoke** | `e2e-tests` job: Playwright against full stack | Integration failures between frontend and backend (broken API contracts, CORS, auth flow). |

When a gate fails, check these first:
- **Migration round-trip fails**: run `grep -rn "<index_name>" backend/alembic/versions/` to find duplicate definitions
- **Route contract fails**: the error message names the missing route; check `app/api/` for the expected decorator
- **Route auth contract fails**: check the HTTP status code in the error. 404 = route missing (route contract issue). 405 = wrong method. 401 on a public route = auth dependency added accidentally. 200 on a protected route = auth dependency removed accidentally.
