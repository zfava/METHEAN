# Accessibility Baseline

Preliminary assessment based on code inspection. Full axe-core automated audit pending (requires running app with authenticated routes).

Last measured: 2026-04-17 (code inspection, not automated scan)

## Methodology

Until a full Playwright + axe-core scan is set up for authenticated routes, this baseline is derived from:
1. Manual code inspection of page.tsx files for ARIA attributes, semantic HTML, and WCAG patterns
2. Build output analysis for missing alt text, form labels, and heading hierarchy
3. Design token analysis for color contrast compliance

## Known Accessibility Patterns (Positive)

| Pattern | Implementation | Status |
|---|---|---|
| Semantic HTML | Most pages use section, header, nav, main, footer | Good |
| Focus management | BottomSheet has focus trap, Escape key closes | Good |
| ARIA labels | Tab bars use role="tablist", tabs use role="tab" | Good |
| Color contrast | Design tokens use --color-text on --color-page (dark on light) | Likely passes AA |
| Keyboard navigation | Interactive elements are buttons, not divs with onClick | Good |
| Screen reader text | Some sr-only labels present on icon-only buttons | Partial |

## Known Accessibility Gaps (To Fix)

| Issue | Affected Routes | Severity | Fix |
|---|---|---|---|
| Missing landmark regions | Landing page (/) | Moderate | Wrap sections in main, add nav landmarks |
| Form labels | /auth, /onboarding | Serious | Associate labels with form inputs via htmlFor |
| Image alt text | /child (progress ring SVG) | Moderate | Add aria-label to decorative SVGs |
| Touch targets | Mobile governance queue | Moderate | Ensure all tap targets are 44x44px minimum |
| Color contrast (brand gold) | Accent text on light backgrounds | Needs measurement | Verify --color-brand-gold (#C6A24E) against --color-page at 4.5:1 |
| Heading hierarchy | Several pages skip h2 or use h4 before h3 | Minor | Fix heading order |
| Focus visible | Custom styled inputs may lose focus ring | Moderate | Ensure :focus-visible outline on all interactive elements |

## Color Contrast Check

Key color pairs to verify at WCAG AA (4.5:1 for normal text, 3:1 for large text):

| Foreground | Background | Ratio (estimated) | Pass AA? |
|---|---|---|---|
| --color-text (#0F1B2D) | --color-page (#FAFAF7) | ~16:1 | Yes |
| --color-text-secondary | --color-surface | ~8:1 | Yes |
| --color-brand-gold (#C6A24E) | --color-page (#FAFAF7) | ~3.5:1 | Fails for small text, passes for large |
| --color-accent (blue) | --color-page | ~5:1 | Yes |

Action: --color-brand-gold may need darkening for small-text usage. Use it only for headings (large text, 3:1 threshold) or decorative elements.

## Automated Testing Plan

Install axe-core for Playwright and run against all routes:

```bash
cd frontend
npm install -D @axe-core/playwright
```

Test file at `frontend/e2e/accessibility.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Public routes (no auth needed)
const publicRoutes = ['/', '/auth', '/privacy', '/terms'];

for (const route of publicRoutes) {
  test(`a11y: ${route}`, async ({ page }) => {
    await page.goto(route);
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  });
}

// Authenticated routes require login first
// Add after auth fixture is available in e2e tests
```

## Target

- All Tier 1 pages: zero critical or serious axe-core violations
- All pages: WCAG AA color contrast (4.5:1 for text, 3:1 for large text and UI components)
- Lighthouse accessibility score: 90+ on all public routes
