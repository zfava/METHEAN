"use client";

import { useReducedMotion } from "framer-motion";

import { personaFromId } from "@/components/companion/personas";

/**
 * Static, stateless rendering of a companion persona by id.
 *
 * This is the thin wrapper form: it renders the procedural persona SVG
 * (the same components CompanionStage uses) in a resting "idle" state
 * with no gaze tracking and no state machine. It is used by surfaces
 * that show a persona by explicit id and may live outside the /child
 * provider tree (onboarding, parent governance, pickers, tutor chat).
 *
 * For the live, stateful companion (gaze, celebrate, sleep, etc.) use
 * CompanionStage instead.
 */

const PERSONA_LABEL: Record<string, string> = {
  default_warm: "Warm companion",
  default_bright: "Bright companion",
  default_steady: "Steady companion",
  default_playful: "Playful companion",
  default_gentle: "Gentle companion",
};

export function CompanionAvatar({
  personaId,
  size = 28,
  className,
  alt,
}: {
  personaId: string;
  size?: number;
  className?: string;
  /** Override the auto-derived persona label. */
  alt?: string;
}) {
  const reduceMotion = useReducedMotion() ?? false;
  const Persona = personaFromId(personaId);
  const label = alt ?? PERSONA_LABEL[personaId] ?? "Companion";

  return (
    <span
      role="img"
      aria-label={label}
      className={className}
      style={{ display: "inline-block", lineHeight: 0, width: size, height: size }}
    >
      <Persona state="idle" size={size} reduceMotion={reduceMotion} />
    </span>
  );
}

export default CompanionAvatar;
