# Pre-Deployment Checklist

## Every Deploy
- [ ] All CI checks pass (backend tests, frontend build, migration safety)
- [ ] No high-severity Bandit findings
- [ ] `ruff check app/` passes with zero errors
- [ ] `ruff format --check app/` passes with zero reformats
- [ ] Frontend builds: `npm run build` succeeds
- [ ] Alembic migrations tested (upgrade + downgrade + re-upgrade)
- [ ] No secrets in committed code (check `git diff` for .env, keys, tokens)

## Major Releases
- [ ] CHANGELOG.md updated with user-facing changes
- [ ] Version bumped: `npm run version:bump [patch|minor|major]`
- [ ] Load test run with acceptable results (see docs/load-test-results.md)
- [ ] Manual smoke test on staging environment
- [ ] Sentry release tagged: `sentry-cli releases new methean@X.Y.Z`
- [ ] Database migration tested on staging data (not just empty DB)
- [ ] Mobile testing matrix completed (see frontend/MOBILE_TESTING.md)

## First Production Deploy
- [ ] JWT_SECRET is unique, cryptographically random, >= 64 characters
- [ ] PREVIOUS_JWT_SECRET is empty (no rotation needed on first deploy)
- [ ] STRIPE_SECRET_KEY is live mode (not sk_test_)
- [ ] STRIPE_WEBHOOK_SECRET configured and webhook endpoint registered
- [ ] SENTRY_DSN configured for production project
- [ ] FCM_PROJECT_ID and FCM_SERVICE_ACCOUNT_JSON for push notifications
- [ ] RESEND_API_KEY for transactional emails
- [ ] Database backups configured (daily, 30-day retention)
- [ ] Health check monitoring configured (uptime robot, Datadog, etc.)
- [ ] SSL certificate valid for methean.app domain
- [ ] CORS_ORIGINS set to production domains only
- [ ] AI_MOCK_ENABLED=false (real AI providers active)
- [ ] Rate limiting tested (120 req/min per IP)
- [ ] RLS policies verified on production database
- [ ] COPPA/FERPA legal review complete
- [ ] Privacy policy published at methean.app/privacy
- [ ] Terms of service published at methean.app/terms
- [ ] Apple Developer account configured (for iOS app)
- [ ] Google Play Console account configured (for Android app)

## Post-Deploy Verification
- [ ] `curl https://api.methean.app/health` returns `{"status": "ok"}`
- [ ] `curl https://api.methean.app/health/ready` shows all checks "ok"
- [ ] Login flow works end-to-end
- [ ] Child dashboard loads with greeting
- [ ] Governance queue renders (empty or with items)
- [ ] Sentry receives a test event
- [ ] Prometheus metrics endpoint accessible
