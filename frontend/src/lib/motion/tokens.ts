/**
 * METHEAN motion vocabulary.
 *
 * Reference for every primitive and screen-level animation. Use these
 * named values; do not introduce ad-hoc durations or easings in the
 * child surface. The CSS twin lives in globals.css under the
 * `Motion vocabulary` block so we can also express the same curves
 * inside CSS keyframes when we need to.
 *
 * Curve intent:
 *   confident :: primary decelerate. Entrances. The default.
 *   composed  :: symmetric ease-in-out. Transitions between states.
 *   micro     :: standard material. Taps, focus, small affordances.
 *   cinematic :: dramatic decelerate. Milestones, hero moments.
 */

export type MotionEasing = readonly [number, number, number, number];

export const MOTION_EASINGS = {
  confident: [0.32, 0.72, 0, 1] as MotionEasing,
  composed: [0.65, 0, 0.35, 1] as MotionEasing,
  micro: [0.4, 0, 0.2, 1] as MotionEasing,
  cinematic: [0.16, 1, 0.3, 1] as MotionEasing,
} as const;

export const MOTION_DURATIONS_MS = {
  micro: 120,
  fast: 200,
  base: 320,
  slow: 520,
  cinematic: 900,
  epic: 1400,
} as const;

/** Stagger gaps in ms. Mirrors the gap prop on <Stagger>. */
export const MOTION_STAGGER_MS = {
  tight: 40,
  base: 80,
  generous: 140,
} as const;

export type StaggerGap = keyof typeof MOTION_STAGGER_MS;

/**
 * Framer-motion consumes seconds, not milliseconds. Convert at the
 * primitive boundary; everywhere else in the codebase prefers
 * milliseconds to match the existing design-system convention.
 */
export const MOTION_DURATIONS_SEC = {
  micro: MOTION_DURATIONS_MS.micro / 1000,
  fast: MOTION_DURATIONS_MS.fast / 1000,
  base: MOTION_DURATIONS_MS.base / 1000,
  slow: MOTION_DURATIONS_MS.slow / 1000,
  cinematic: MOTION_DURATIONS_MS.cinematic / 1000,
  epic: MOTION_DURATIONS_MS.epic / 1000,
} as const;

export const MOTION_STAGGER_SEC = {
  tight: MOTION_STAGGER_MS.tight / 1000,
  base: MOTION_STAGGER_MS.base / 1000,
  generous: MOTION_STAGGER_MS.generous / 1000,
} as const;

export const MOTION_TOKENS = {
  easings: MOTION_EASINGS,
  durations: MOTION_DURATIONS_SEC,
  durationsMs: MOTION_DURATIONS_MS,
  stagger: MOTION_STAGGER_SEC,
  staggerMs: MOTION_STAGGER_MS,
} as const;
