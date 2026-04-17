# Deploy and Rollback

Last verified: 2026-04-17 (CI pipeline verified; production deploy not yet exercised)

## Deploy Architecture

- **Hosting**: Railway (or Docker Compose for self-hosted)
- **Backend**: Python/FastAPI running via gunicorn + uvicorn workers
- **Frontend**: Next.js static export served by Nginx or Vercel
- **Database**: PostgreSQL 16 (managed)
- **Cache/Queue**: Redis 7 (managed)
- **Worker**: Celery worker process (same codebase as backend)

## Deploy Flow

1. Push to `main` branch
2. CI runs (5 jobs: backend tests, lint, frontend build, migration check, E2E)
3. On CI green, Railway auto-deploys backend + worker
4. Migrations run automatically on startup (via Procfile or entrypoint)
5. Frontend deploys independently (Next.js build + static export)

## Smoke Tests Post-Deploy

Run immediately after every deploy:

```bash
# Health check
curl -f https://api.methean.app/health || echo "FAIL: health"

# Auth flow
curl -X POST https://api.methean.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"smoke@test.com","password":"smoketest"}' || echo "FAIL: auth"

# Compliance states (public, no auth needed)
curl -f https://api.methean.app/api/v1/compliance/states | head -c 200 || echo "FAIL: compliance"

# AI gateway (requires auth)
# Check circuit breaker state
curl -H "Authorization: Bearer $TOK" https://api.methean.app/api/v1/ai/health || echo "FAIL: ai"
```

## Rollback a Deploy

### Railway

```bash
# List recent deployments
railway deployment list

# Rollback to the previous deployment
railway deployment rollback

# Or rollback to a specific deployment ID
railway deployment rollback --deployment-id <id>
```

### Docker Compose

```bash
# Rollback to the previous image
docker compose pull  # gets the latest tagged image
# Or pin to a specific version:
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-build

# If using git-based deploys:
git log --oneline -5  # find the last good commit
git checkout <good_commit>
docker compose up -d --build
```

### Git Revert

If the bad deploy was a specific commit:

```bash
git revert HEAD
git push origin main
# CI will rebuild and redeploy the reverted state
```

## Diagnosing Deploy Failures

1. **Check Railway logs**: `railway logs --service backend`
2. **Check Sentry**: new errors in the last 15 minutes
3. **Check migrations**: `alembic current` vs expected head
4. **Check environment variables**: `railway variables list` (missing var = startup crash)
5. **Check container health**: is the process running? Is it OOM-killed?

Common failure modes:
- Missing environment variable (new one added, not set in Railway)
- Migration failure (schema drift, see migration-rollback.md)
- Dependency conflict (new package version incompatible)
- Frontend build failure (TypeScript error, Tailwind config change)
