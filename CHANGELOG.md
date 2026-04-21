# Changelog

All notable changes to METHEAN are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.3.0] - 2026-04-15

### Added
- Playwright E2E testing: 7 specs across auth, dashboard, governance
- Complete Stripe billing: checkout, portal, 5 webhook event types, cancellation
- Sentry error tracking with traces and profiles sampling
- Prometheus /metrics endpoint with 5 custom business metrics
- Redis caching layer for hot API paths (child state, governance queue)
- JWT dual-key rotation (PREVIOUS_JWT_SECRET)
- Security response headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
- Dependabot for pip, npm, and GitHub Actions dependencies
- pip-audit in CI pipeline
- Locust load testing framework with performance targets
- AI prompt snapshot regression tests
- Staging environment (docker-compose.staging.yml) with isolated ports
- Staging deploy GitHub Actions workflow
- Operational runbook and deployment checklist
- Mobile: dashboard carousel, swipe governance queue, plans accordion
- Mobile: child celebration animation, activity timer, theme persistence
- Push notification delivery via FCM HTTP v1 API
- Native bridge: haptics, biometric auth, share, badge
- Capacitor native shell for iOS and Android

### Changed
- CI coverage floor raised from 25% to 30%
- Migration 028: stripe_subscription_id field on households
- Ruff config expanded with N, SIM, TCH, RUF rules

## [0.2.0] - 2026-04-13

### Added
- Evaluator Calibration Engine: prediction ledger, reconciliation, adaptive offset
- Learner Style Engine: 10-dimension computed vector with parent overrides
- Family Intelligence: 5 cross-child pattern detectors, predictive scaffolding
- Wellbeing Anomaly Detection: 4 anomaly types, sensitivity controls
- Context Assembly Service: role-specific profiles for 5 AI roles
- RLS hardening: migrations 026-027, safe current_setting
- GitHub Actions CI: backend tests, linting, frontend build, migration safety
- Mobile PWA: manifest, service worker, bottom tab bar, bottom sheet navigation
- Child dashboard API with personalized greetings

## [0.1.0] - 2026-04-07

### Added
- 50-state + DC compliance engine with document generation
- Assessment engine and portfolio entries
- Annual curriculum with year plans and scope sequences
- Education Plan service with AI Education Architect role
- Billing and usage metering models
- Achievement and streak tracking
- Governance Intelligence (learns from parent review patterns)
- Reading log, family resources, email system, notifications
- Family invites with permission-based access
- Data export for household sovereignty

## [0.0.1] - 2026-04-03

### Added
- DAG-based curriculum engine with transitive closure
- FSRS v6 spaced repetition with per-child weight optimization
- Parent governance rule engine (5 rule types, 2 tiers)
- AI governance gateway (8 roles, 3-tier fallback, recommendation-only)
- Philosophical profile with constraint injection
- Constitutional ceremony for foundational rules
- Attempt workflow pipeline
- Frontend: 20 parent pages, auth, onboarding, child view
- Docker Compose with PostgreSQL 16, Redis 7, MinIO
