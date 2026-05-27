/**
 * Display-name mapping for the two mastery taxonomies.
 *
 * METHEAN has two distinct axes that the API both wires as bare
 * strings, and which we used to render with the raw wire format. The
 * wire format stays unchanged (the backend's MasteryLevel enum and
 * LEARNING_LEVELS keys are unaffected); we layer human display names
 * on top here so the product reads cleanly and consistently.
 *
 *  1. Per-node MASTERY STATE (FSRS, on every ChildNodeState row):
 *       not_started -> "Just started"
 *       emerging    -> "Learning"
 *       developing  -> "Practiced"
 *       proficient  -> "Confident"
 *       mastered    -> "Mastered"
 *
 *  2. Curriculum CONTENT TIER (on every annual curriculum / subject):
 *       foundational -> "Foundations"
 *       developing   -> "Building"
 *       intermediate -> "Expanding"
 *       advanced     -> "Mastering"
 *       mastery      -> "Mastered"
 *
 * The two taxonomies share zero words except the shared endpoint
 * "Mastered". That collision is intentional: once a child has truly
 * mastered the highest content tier of a subject, both axes converge.
 *
 * The functions accept an arbitrary string (the wire format), tolerate
 * unknown values by falling back to a humanized form (so a forward-
 * compatible backend value doesn't blank out the UI), and never throw.
 */

export type MasteryState =
  | "not_started"
  | "emerging"
  | "developing"
  | "proficient"
  | "mastered";

export type ContentTier =
  | "foundational"
  | "developing"
  | "intermediate"
  | "advanced"
  | "mastery";

const MASTERY_STATE_LABELS: Record<MasteryState, string> = {
  not_started: "Just started",
  emerging: "Learning",
  developing: "Practiced",
  proficient: "Confident",
  mastered: "Mastered",
};

const CONTENT_TIER_LABELS: Record<ContentTier, string> = {
  foundational: "Foundations",
  developing: "Building",
  intermediate: "Expanding",
  advanced: "Mastering",
  mastery: "Mastered",
};

/** Pedagogical ordering, lowest to highest, for both axes. */
export const MASTERY_STATE_ORDER: readonly MasteryState[] = [
  "not_started",
  "emerging",
  "developing",
  "proficient",
  "mastered",
] as const;

export const CONTENT_TIER_ORDER: readonly ContentTier[] = [
  "foundational",
  "developing",
  "intermediate",
  "advanced",
  "mastery",
] as const;

/** A one-line explanation per content tier, shown in the picker
 *  explainer card. Plain, parent-facing language. */
export const CONTENT_TIER_DESCRIPTIONS: Record<ContentTier, string> = {
  foundational: "Building core concepts from scratch.",
  developing: "Working through fundamentals with growing independence.",
  intermediate: "Solid foundation, ready for deeper exploration.",
  advanced: "Strong mastery, ready for complex and original work.",
  mastery: "Deep expertise, self-directed, teaching and creating.",
};

function humanizeUnknown(raw: string): string {
  if (!raw) return "";
  return raw
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Display name for a per-node FSRS mastery state. Unknown values are
 *  humanized rather than thrown so a new backend value still renders. */
export function formatMasteryState(level: string | null | undefined): string {
  if (!level) return "";
  if (level in MASTERY_STATE_LABELS) {
    return MASTERY_STATE_LABELS[level as MasteryState];
  }
  return humanizeUnknown(level);
}

/** Display name for a curriculum content tier. Same fallback rule. */
export function formatContentTier(tier: string | null | undefined): string {
  if (!tier) return "";
  if (tier in CONTENT_TIER_LABELS) {
    return CONTENT_TIER_LABELS[tier as ContentTier];
  }
  return humanizeUnknown(tier);
}

export function isContentTier(value: unknown): value is ContentTier {
  return typeof value === "string" && value in CONTENT_TIER_LABELS;
}

export function isMasteryState(value: unknown): value is MasteryState {
  return typeof value === "string" && value in MASTERY_STATE_LABELS;
}
