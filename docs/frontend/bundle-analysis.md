# Frontend Bundle Analysis

Measured from `npm run build` output. Next.js 15.5.15, React 19, Tailwind CSS 4.

Last measured: 2026-04-17

## Shared JavaScript (loaded on every route)

| Chunk | Size | Contents |
|---|---|---|
| framework-*.js | 186 kB (raw) | React 19 + React DOM |
| 4bd1b696-*.js | 169 kB (raw) | Next.js runtime |
| 1255-*.js | 169 kB (raw) | App Router shared code |
| main-*.js | 125 kB (raw) | Next.js client entry |
| polyfills-*.js | 110 kB (raw) | Browser polyfills |
| **Total shared (gzipped)** | **~102 kB** | Reported by Next.js build |

## Top 10 Heaviest Routes (by First Load JS)

| Route | Page Size | First Load JS | Primary Content |
|---|---|---|---|
| /child | 19.9 kB | 127 kB | Child learning experience (progress ring, activity timer, celebrations) |
| /dashboard | 8.05 kB | 125 kB | Parent dashboard (metrics grid, governance queue preview, child carousel) |
| /governance/rules | 8.88 kB | 119 kB | Governance rule editor (complex form) |
| /onboarding | 8.77 kB | 119 kB | Multi-step onboarding flow |
| /governance | 7.06 kB | 117 kB | Governance overview page |
| /governance/queue | 6.11 kB | 116 kB | Approval queue with swipe actions |
| /curriculum/mapper | 5.56 kB | 116 kB | DAG visualization |
| /calibration | 9.39 kB | 116 kB | Calibration dashboard (charts, drift history) |
| /settings | 6.35 kB | 116 kB | Settings with state dropdown, export |
| /curriculum | 8.50 kB | 115 kB | Curriculum overview |

## Dependency Size Analysis

| Package | Installed Size | In Bundle | Notes |
|---|---|---|---|
| next | 155 MB | ~102 kB shared | Framework (required) |
| @next/* | 137 MB | included above | SWC compiler, platform binaries |
| typescript | 23 MB | 0 (dev only) | Not in production bundle |
| @img/sharp-* | 17 MB | 0 (server only) | Image optimization, server-side only |
| playwright-core | 12 MB | 0 (dev only) | E2E testing |
| react-dom | 7.2 MB | ~45 kB gzipped | Required |
| tailwindcss | 3.3 MB | 0 (build only) | CSS compiled at build time |
| @capacitor/* | ~5 MB | tree-shaken | Only native bridge code in bundle |

## Observations

1. **No bloated dependencies**: No single dependency contributes more than framework-standard JS to the client bundle.
2. **All routes static**: Every route is statically pre-rendered (SSG). No SSR or ISR.
3. **Shared chunk dominates**: The 102 kB shared chunk is 80-95% of every route's First Load JS. Per-route code is small (1-20 kB).
4. **Capacitor tree-shaking works**: The Capacitor runtime packages are present in node_modules but tree-shaken to only the used APIs.
5. **No code splitting issues**: No duplicated dependencies across route chunks (Next.js handles this automatically).

## Recommendations

1. **No immediate action needed on bundle size.** All routes are under 130 kB First Load, which is fast on mobile networks.
2. **Monitor /child page**: At 19.9 kB page code, it is 2.5x the average. If it grows further, consider splitting the celebration animation into a lazy-loaded component.
3. **Consider prefetching Tier 1 routes**: Dashboard -> child, dashboard -> plans, dashboard -> governance/queue are the most common navigation paths.
