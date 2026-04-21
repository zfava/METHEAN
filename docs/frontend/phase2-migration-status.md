# Phase 2 UX Migration Status

Page-by-page inventory of design system adoption. Status based on automated scan of design token usage, raw hex color count, and mobile responsiveness markers.

Last measured: 2026-04-17 (automated scan of page.tsx files)

## Status Key

- **DONE**: Uses design system tokens throughout, minimal raw hex, mobile-responsive
- **PARTIAL**: Some design tokens adopted, may have raw hex colors or missing mobile patterns
- **NOT STARTED**: Primarily raw hex colors, no design system tokens

## Tier 1: Investor Demo Path (migrate first)

| Route | Bundle Size | First Load | Design Tokens | Raw Hex | Mobile | Status |
|---|---|---|---|---|---|---|
| /dashboard | 8.05 kB | 125 kB | 57 | 2 | 9 | DONE |
| /child | 19.9 kB | 127 kB | 71 | 8 | 6 | PARTIAL |
| /onboarding | 8.77 kB | 119 kB | 64 | 1 | 3 | DONE |
| /curriculum/year | 5.24 kB | 112 kB | 31 | 0 | 3 | PARTIAL |
| /governance/queue | 6.11 kB | 116 kB | 29 | 0 | 2 | PARTIAL |
| /plans | 6.15 kB | 113 kB | 19 | 0 | 3 | PARTIAL |

Tier 1 status: 2 DONE, 4 PARTIAL. The child view (/child) is the largest bundle at 19.9 kB (127 kB First Load) and still has 8 raw hex colors to convert.

## Tier 2: Parent Power-User Path

| Route | Bundle Size | First Load | Design Tokens | Raw Hex | Mobile | Status |
|---|---|---|---|---|---|---|
| /governance/rules | 8.88 kB | 119 kB | 67 | 0 | 1 | PARTIAL |
| /governance | 7.06 kB | 117 kB | 44 | 0 | 8 | PARTIAL |
| /governance/trace | 4.03 kB | 114 kB | 17 | 0 | 3 | PARTIAL |
| /governance/philosophy | 6.17 kB | 113 kB | 29 | 0 | 1 | PARTIAL |
| /governance/reports | 4.99 kB | 115 kB | 33 | 5 | 2 | PARTIAL |
| /governance/overrides | 3.31 kB | 110 kB | 4 | 0 | 2 | PARTIAL |
| /family | 7.79 kB | 115 kB | 34 | 0 | 4 | PARTIAL |
| /family-insights | 6.38 kB | 113 kB | 33 | 2 | 3 | DONE |
| /intelligence | 7.29 kB | 114 kB | 41 | 0 | 4 | PARTIAL |
| /calibration | 9.39 kB | 116 kB | 86 | 0 | 3 | PARTIAL |
| /calendar | 6.45 kB | 113 kB | 33 | 1 | 5 | DONE |
| /compliance | 4.10 kB | 111 kB | 31 | 0 | 4 | PARTIAL |
| /resources | 5.66 kB | 112 kB | 15 | 0 | 3 | PARTIAL |
| /reading | 6.55 kB | 113 kB | 31 | 0 | 2 | PARTIAL |
| /maps | 3.42 kB | 114 kB | 18 | 0 | 2 | PARTIAL |
| /wellbeing | 6.88 kB | 114 kB | 45 | 1 | 3 | DONE |

Tier 2 status: 3 DONE, 13 PARTIAL.

## Tier 3: Settings and Ancillary

| Route | Bundle Size | First Load | Design Tokens | Raw Hex | Mobile | Status |
|---|---|---|---|---|---|---|
| /settings | 6.35 kB | 116 kB | 38 | 0 | 3 | PARTIAL |
| /billing | 5.36 kB | 112 kB | 17 | 0 | 2 | PARTIAL |
| /assessment | 5.44 kB | 112 kB | 23 | 0 | 2 | PARTIAL |
| /style-profile | 6.74 kB | 113 kB | 29 | 0 | 3 | PARTIAL |
| /plans/vision | 7.35 kB | 114 kB | 64 | 0 | 2 | PARTIAL |
| /inspection | 7.97 kB | 115 kB | 55 | 1 | 4 | DONE |
| /curriculum | 8.50 kB | 115 kB | 45 | 2 | 4 | DONE |
| /curriculum/editor | 3.91 kB | 111 kB | 41 | 0 | 4 | PARTIAL |
| /curriculum/history | 3.97 kB | 111 kB | 10 | 0 | 2 | PARTIAL |
| /curriculum/mapper | 5.56 kB | 116 kB | 39 | 0 | 5 | PARTIAL |
| /curriculum/scope | 3.90 kB | 111 kB | 18 | 0 | 1 | PARTIAL |
| /auth | 2.39 kB | 109 kB | 18 | 1 | 0 | DONE |
| /auth/reset | 2.91 kB | 110 kB | 7 | 1 | 0 | DONE |
| / (landing) | 6.19 kB | 113 kB | 39 | 21 | 11 | PARTIAL |
| /privacy | 1.02 kB | 107 kB | 18 | 2 | 1 | DONE |
| /terms | 1.02 kB | 107 kB | 14 | 2 | 1 | DONE |

## Summary

| Status | Count | Percentage |
|---|---|---|
| DONE | 13 | 34% |
| PARTIAL | 25 | 66% |
| NOT STARTED | 0 | 0% |

All pages have at least some design system adoption. No page is entirely unstyled. The primary remaining work is converting raw hex colors to design tokens and adding mobile-responsive breakpoints to PARTIAL pages.

## Bundle Size Summary

| Metric | Value |
|---|---|
| Shared JS (all routes) | 102 kB |
| Heaviest route (First Load) | /child at 127 kB |
| Lightest routes (First Load) | /privacy, /terms at 107 kB |
| Average First Load | ~114 kB |
| All routes static (SSG) | Yes |

No route exceeds 130 kB First Load. No dependency over 100 kB gzipped in route bundles. The shared chunk (React + framework) is 102 kB, which is standard for Next.js 15 + React 19.

## Migration Effort Estimate

| Tier | Pages | DONE | Remaining | Est. Hours |
|---|---|---|---|---|
| Tier 1 | 6 | 2 | 4 | 8-12 |
| Tier 2 | 16 | 3 | 13 | 20-30 |
| Tier 3 | 16 | 8 | 8 | 12-16 |
| **Total** | **38** | **13** | **25** | **40-58** |
