# Motion foundation

Physics-based motion layer for the child surface, built on framer-motion.
Springs (not linear easings) drive every primitive, motion personality is
tuned per vibe, and prefers-reduced-motion is the strictest tested path.

Source: `frontend/src/lib/motion/`.

## Layers

1. `springs.ts` :: the per-vibe spring table plus fixed functional presets.
2. `MotionContext.tsx` :: `MotionProvider` + `useMotion()`. Resolves the
   active vibe to a spring, folds in age-band and parent governance, and
   exposes the hard reduced-motion switch.
3. `primitives.tsx` :: the 11 spring-based primitives.
4. `index.ts` :: the barrel. Import from `@/lib/motion`.

The earlier easing/duration token layer (`tokens.ts`) and the existing
`components/child/motion/*` primitives still ship and still work; this
foundation augments them with springs rather than rewriting them.

## Per-vibe motion personality

`SPRING_BY_VIBE` keys a framer-motion spring `Transition` off the canonical
vibe IDs (`calm`, `field`, `orbit`, `workshop`, `studio`, `bold`, mirrored
from `backend/app/content/personalization_library.py`). Switching vibe
changes the motion feel:

| vibe     | feel                                  |
| -------- | ------------------------------------- |
| calm     | slow, soft, drifts into place         |
| field    | medium, springy, warm                 |
| orbit    | medium-fast, glassy, precise          |
| workshop | medium, weighty, planted              |
| studio   | fast, bouncy, expressive              |
| bold     | very fast, very snappy, near overshoot |

Fixed presets (`SPRING_PRESS`, `SPRING_GENTLE`, `SPRING_SETTLE`,
`SPRING_BOUNCY`) stay vibe-agnostic for motions that should feel constant
(press feedback, celebration pop).

`useMotion()` returns the resolved `spring` plus the existing age-band /
governance fields. Every primitive reads it and applies the vibe spring
automatically unless given a `transition` override prop.

## Reduced motion (non-overridable)

When `prefers-reduced-motion: reduce` is set, `MotionProvider` flips
`reduceMotion` true and `spring` to `INSTANT_TRANSITION` (`{ duration: 0 }`).
Every primitive branches on `reduceMotion` first and collapses to an
instant or static render. A component `transition` prop never overrides
this: reduced motion wins.

## Primitives

| primitive          | role                                                       |
| ------------------ | ---------------------------------------------------------- |
| `Fade`             | fade in, optional directional drift; stagger-aware         |
| `Scale`            | scale-in from 0.92 with the vibe spring                    |
| `Slide`            | directional slide; presence-aware (enter/exit) with `dir`  |
| `Press`            | tap scale to 0.97 with `SPRING_PRESS`                      |
| `Hover`            | hover lift + shadow bump                                   |
| `Stagger`          | orchestrates child entrance timing (`delay`, `step`)       |
| `AmbientFloat`     | looped idle vertical drift (suspended when reduced)        |
| `ParallaxOnScroll` | scroll-linked Y translate (`depth` 0 static .. 1 with content) |
| `SharedLayout`     | `LayoutGroup` wrapper for shared-layout morphs             |
| `SharedItem`       | `layoutId` element that morphs between renders             |
| `RouteTransition`  | page entry/exit fade + translate (custom cubic-bezier)     |

`Fade` inside a `Stagger` becomes a variant child and lets the parent drive
timing; standalone it animates itself.

## Proof-point migrations (child surface)

- Activity card list :: `Stagger` + `Fade`, CTA in `Press`, completed rows
  in `Hover` (`app/child/page.tsx`).
- Celebration overlay :: `Scale` (`SPRING_BOUNCY`) + delayed `Fade`.
- Progress ring :: `motion.circle` animating `strokeDashoffset` on the vibe
  spring.
- Card to activity view :: `SharedLayout` + `SharedItem` morph (no cross-fade).
- Welcome step navigation :: `AnimatePresence` + `Slide` (down on mobile,
  right on desktop; direction inverts on back) in `WelcomeShell`.

## Notes / scope

- The globals.css keyframe utilities (`animate-fade-up`, `animate-scale-in`,
  `stagger-1..8`, etc.) are intentionally retained: 40+ parent/onboarding
  surfaces still depend on them. Only the child-surface usages were migrated.
  Converting the parent surface and deleting the keyframes is follow-up work.
- `MotionProvider` depends on `PersonalizationProvider` + `ChildContext`, so
  it stays scoped to the `/child` subtree. The parent layout has no
  personalization provider, so wiring motion there is deferred.
