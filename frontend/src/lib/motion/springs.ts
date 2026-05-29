import type { Transition } from "framer-motion";

/**
 * Per-vibe motion personality. Each entry is a framer-motion spring
 * Transition that frames every primitive's default motion.
 *
 * Stiffness governs how fast it reaches target. Damping governs how
 * much it overshoots. Mass governs the "weight" feel.
 *
 *   calm     :: slow, soft, deliberate, almost drifts into place.
 *   field    :: medium, springy, warm.
 *   orbit    :: medium-fast, glassy, precise.
 *   workshop :: medium, weighty, planted.
 *   studio   :: fast, bouncy, expressive.
 *   bold     :: very fast, very snappy, almost overshoots.
 *
 * The IDs intentionally mirror the canonical vibe IDs seeded in
 * backend/app/content/personalization_library.py so the active vibe
 * maps straight onto a motion personality.
 */

export type VibeMotionId = "calm" | "field" | "orbit" | "workshop" | "studio" | "bold";

export const SPRING_BY_VIBE: Record<VibeMotionId, Transition> = {
  calm: { type: "spring", stiffness: 90, damping: 22, mass: 1.1 },
  field: { type: "spring", stiffness: 220, damping: 24, mass: 0.9 },
  orbit: { type: "spring", stiffness: 280, damping: 28, mass: 0.85 },
  workshop: { type: "spring", stiffness: 200, damping: 26, mass: 1.0 },
  studio: { type: "spring", stiffness: 320, damping: 18, mass: 0.75 },
  bold: { type: "spring", stiffness: 420, damping: 16, mass: 0.7 },
};

/**
 * Functional-class presets, vibe-agnostic. Use these when a motion is
 * conceptually fixed (e.g., a press feedback should always feel crisp
 * regardless of vibe).
 */
export const SPRING_PRESS: Transition = { type: "spring", stiffness: 600, damping: 30 };
export const SPRING_GENTLE: Transition = { type: "spring", stiffness: 160, damping: 24 };
export const SPRING_SETTLE: Transition = { type: "spring", stiffness: 220, damping: 30 };
export const SPRING_BOUNCY: Transition = { type: "spring", stiffness: 360, damping: 14 };

/**
 * Reduced-motion fallback. Non-overridable from component props: every
 * primitive collapses to this when prefers-reduced-motion is set, so
 * state changes resolve in roughly a single frame.
 */
export const INSTANT_TRANSITION: Transition = { duration: 0 };

const VIBE_MOTION_IDS: ReadonlySet<string> = new Set<VibeMotionId>([
  "calm",
  "field",
  "orbit",
  "workshop",
  "studio",
  "bold",
]);

/**
 * Resolve an arbitrary vibe ID string to a known motion personality.
 * Unknown or still-loading vibes fall back to calm, matching the
 * CALM_VIBE_FALLBACK used elsewhere in the personalization layer.
 */
export function vibeMotionIdFromVibe(vibe: string | null | undefined): VibeMotionId {
  if (vibe && VIBE_MOTION_IDS.has(vibe)) {
    return vibe as VibeMotionId;
  }
  return "calm";
}
