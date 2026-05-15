"use client";

/**
 * Renders the kid's chosen companion persona as a small avatar.
 *
 * The SVGs live under /public/companions/<persona_id>.svg and use
 * currentColor + the brand-gold variable so they inherit the
 * surrounding text color. Unknown persona IDs fall back to
 * default_warm so the tutor chat never paints an empty slot.
 */

const KNOWN_PERSONAS = new Set<string>([
  "default_warm",
  "default_bright",
  "default_steady",
  "default_playful",
  "default_gentle",
]);

const FALLBACK_PERSONA = "default_warm";

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
  const safeId = KNOWN_PERSONAS.has(personaId) ? personaId : FALLBACK_PERSONA;
  const label = alt ?? PERSONA_LABEL[safeId] ?? "Companion";
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={`/companions/${safeId}.svg`}
      alt={label}
      role="img"
      width={size}
      height={size}
      className={className}
      style={{ width: size, height: size, display: "block" }}
    />
  );
}

export default CompanionAvatar;
