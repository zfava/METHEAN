# AI Provider Outage

Last verified: 2026-04-17 (circuit breaker tested; mock fallback tested; full outage scenario not yet exercised)

## Architecture

The AI gateway (`app/ai/gateway.py`) has three providers in a chain:

1. **Claude (Anthropic)**: primary. Circuit breaker with 3-failure threshold, 60s recovery.
2. **OpenAI**: fallback. Separate circuit breaker.
3. **Mock**: always available. Deterministic responses for all 8 AI roles.

The circuit breaker lifecycle: closed (normal) -> open (after 3 failures in 60s window) -> half_open (after 60s recovery timeout, allows one test request) -> closed (on success) or open (on failure).

## Detection

- **Automatic**: circuit breaker opens, ai_calls_total metric shows provider=mock increasing
- **Sentry**: errors classified as "provider_error" or "timeout" in structured logs
- **Manual**: `GET /api/v1/ai/health` returns circuit breaker state per provider

## Automatic Failover

When Claude is down:
1. Circuit breaker opens after 3 consecutive failures
2. Gateway tries OpenAI as fallback
3. If OpenAI is also down, gateway falls through to mock
4. Mock returns valid but deterministic responses for all roles
5. Users see functional but non-personalized AI

No manual intervention is needed for failover. The system degrades gracefully.

## Manual Override to Mock

If you need to force all traffic to mock (e.g., during a billing dispute with a provider):

```bash
# Set environment variable
railway variables set AI_MOCK_ENABLED=true

# Restart the backend service
railway service restart backend
```

To restore:

```bash
railway variables set AI_MOCK_ENABLED=false
railway service restart backend
```

## Monitoring Recovery

After a provider outage ends:
1. Circuit breaker automatically transitions to half_open after 60 seconds
2. One test request is sent to the provider
3. If it succeeds, circuit closes (normal operation)
4. If it fails, circuit reopens for another 60 seconds

No manual intervention is needed for recovery.

## Cost Control Interaction

If the household daily budget is exceeded during an outage recovery (tokens were consumed on retries), the cost control system will degrade to mock independently. This is correct behavior: the budget protects unit economics regardless of outage state.

## Verification Commands

```bash
# Check circuit breaker state
curl -H "Authorization: Bearer $TOK" http://localhost:8000/api/v1/ai/health

# Check recent AI call success rate
psql -c "SELECT model_used, status, COUNT(*) FROM ai_runs WHERE started_at > NOW() - INTERVAL '1 hour' GROUP BY model_used, status;"

# Force a test AI call
curl -X POST -H "Authorization: Bearer $TOK" http://localhost:8000/api/v1/notifications/test-daily-summary
```
