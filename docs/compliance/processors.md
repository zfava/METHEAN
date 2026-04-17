# Third-Party Data Processors

List of all third-party services that process METHEAN user data. Each processor's data handling is documented for COPPA, FERPA, and state privacy law compliance.

Last updated: 2026-04-17

## Processor Inventory

| Processor | Purpose | Data Shared | Contains Child Data | DPA Status |
|---|---|---|---|---|
| Anthropic (Claude) | Primary AI provider: tutoring, planning, evaluation, content generation | Child-generated content (responses, scores), parent context (governance rules, preferences). No names or DOB sent. | Yes (pseudonymized) | Required; not yet signed |
| OpenAI | Fallback AI provider | Same as Anthropic (circuit breaker failover) | Yes (pseudonymized) | Required; not yet signed |
| Stripe | Payment processing | Parent email, payment method, subscription status. No child data. | No | In place (Stripe standard DPA) |
| Resend | Transactional email | Parent email address, notification content (may include child first names in parent-addressed emails) | Minimal (first names in email body) | Required; not yet signed |
| Hosting provider (Railway/Render/AWS) | Infrastructure | All platform data at rest and in transit | Yes | Required; provider-dependent |
| Sentry | Error tracking and monitoring | Stack traces, request metadata. No PII by default; configured to scrub sensitive fields. | Possible (error context) | Required; not yet signed |
| PostgreSQL (managed) | Database | All platform data | Yes | Covered by hosting provider DPA |
| Redis (managed) | Caching, rate limiting, Celery broker | Session tokens, rate limit counters, task queue data. No persistent PII. | No | Covered by hosting provider DPA |

## Data Handling by Processor

### Anthropic (Claude)

- **What is sent**: System prompt (role instructions), user prompt (child's response or learning context, mastery state, governance rules). Prompts include learning level and subject but NOT child name, DOB, or other PII.
- **Retention**: Anthropic retains API inputs for 30 days by default for trust and safety, then deletes. Anthropic does not train on API data.
- **Verification**: `grep -n "user_prompt\|system_prompt" backend/app/ai/gateway.py`

### OpenAI

- **What is sent**: Same content as Anthropic (fallback provider).
- **Retention**: OpenAI does not use API data for training (API data usage policy, effective March 2023).
- **Verification**: `grep -n "openai" backend/app/ai/gateway.py`

### Stripe

- **What is sent**: Parent email, household name (for invoice), payment method token (handled by Stripe.js, never touches METHEAN servers).
- **Child data**: None. Stripe never receives child names, DOB, or educational data.
- **Verification**: `grep -n "stripe" backend/app/services/billing.py`

### Resend

- **What is sent**: Parent email address, email subject, HTML body. Email body may contain child first names in context like "Emma mastered Fractions."
- **Retention**: Resend retains email logs for 30 days.
- **Verification**: `grep -n "send_email" backend/app/services/email.py`

### Sentry

- **What is sent**: Error stack traces, request URLs, user agent. Configured to NOT send request bodies or PII.
- **Child data**: Possible only in error context (e.g., if an error occurs during a tutoring session, the stack trace might include a child_id UUID).
- **Mitigation**: Sentry is configured with `send_default_pii=False`.
- **Verification**: `grep -n "sentry" backend/app/main.py`

## DPA Action Items

| Processor | Action Needed | Priority |
|---|---|---|
| Anthropic | Sign DPA before any school-district deployment | P1 (pre-beta) |
| OpenAI | Sign DPA before any school-district deployment | P1 (pre-beta) |
| Resend | Sign DPA or switch to provider with DPA in place | P2 |
| Sentry | Review data scrubbing config; sign DPA | P2 |
| Hosting | Sign DPA with hosting provider | P1 |
| Stripe | Already in place via standard Stripe DPA | Done |
