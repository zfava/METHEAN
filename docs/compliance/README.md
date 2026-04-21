# METHEAN Compliance Documentation

This directory contains compliance posture documents for METHEAN. These are working drafts for legal review, not final legal documents. Every claim is backed by code; verification commands are included.

## Documents

| Document | Purpose |
|---|---|
| [data-inventory.md](data-inventory.md) | Complete inventory of personal data collected, stored, and processed |
| [coppa.md](coppa.md) | Children's Online Privacy Protection Act posture statement |
| [ferpa.md](ferpa.md) | Family Educational Rights and Privacy Act posture statement |
| [processors.md](processors.md) | Third-party data processors and DPA status |
| [state-privacy.md](state-privacy.md) | State-level privacy law posture (CPRA, CPA, etc.) |

## Related

| Document | Location |
|---|---|
| Privacy Policy (user-facing) | [frontend/src/app/privacy/page.tsx](../../frontend/src/app/privacy/page.tsx) |
| Terms of Service (user-facing) | [frontend/src/app/terms/page.tsx](../../frontend/src/app/terms/page.tsx) |
| RLS Coverage Matrix | [docs/rls-coverage.md](../rls-coverage.md) |
| Architecture Decisions | [docs/architecture-decisions.md](../architecture-decisions.md) |

## Key Technical Controls

1. **Row-Level Security**: 49 household-scoped tables with PostgreSQL RLS policies. See [rls-coverage.md](../rls-coverage.md).
2. **Data Export**: `POST /api/v1/household/export` produces a ZIP containing all family data. See `app/services/data_export.py`.
3. **Data Deletion**: Household deletion cascades via ON DELETE CASCADE on all child tables. All 49 household-scoped tables have foreign keys to households with CASCADE.
4. **AI Data Handling**: AI calls send child-generated content to providers (Anthropic, OpenAI). No persistent storage at the provider. Mock fallback available for offline operation.
5. **No Behavioral Advertising**: No ad SDK, no tracking pixels, no third-party analytics beyond Sentry error reporting.
6. **No Social Features**: No child-to-child communication, no public profiles, no user-generated content visible outside the household.

## How to verify

```bash
# PII fields inventory
grep -rnE "(first_name|last_name|email|date_of_birth|display_name|password)" backend/app/models/ | grep -v __pycache__

# Cascade deletion chain
grep -rn "ondelete.*CASCADE" backend/app/models/ | grep -v __pycache__ | wc -l

# Data export completeness
cd backend && python -m pytest tests/test_data_export.py -v

# RLS coverage
cd backend && python -m pytest tests/test_security.py -k "TestRLSCoverageMatrix" -v
```
