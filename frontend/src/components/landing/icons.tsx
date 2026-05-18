const BASE = {
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.5,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

export function ShieldCheck({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <path d="M12 2L4 6v6c0 5 3.5 9.5 8 11 4.5-1.5 8-6 8-11V6z" />
      <path d="M9 12l2 2 4-4" />
    </svg>
  );
}

export function PhilosophyBook({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <path d="M4 4h7a3 3 0 0 1 3 3v13H7a3 3 0 0 1-3-3z" />
      <path d="M20 4h-7a3 3 0 0 0-3 3v13h7a3 3 0 0 0 3-3z" />
    </svg>
  );
}

export function CalendarGrid({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <rect x="3" y="5" width="18" height="16" rx="2" />
      <path d="M3 10h18M9 5V3M15 5V3M9 14h.01M13 14h.01M9 18h.01M13 18h.01" />
    </svg>
  );
}

export function FlagDoc({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <path d="M4 21V4h11l1 2h4v10h-6l-1-2H4" />
      <path d="M4 21V13" />
    </svg>
  );
}

export function FamilyFour({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <circle cx="8" cy="8" r="2.5" />
      <circle cx="16" cy="8" r="2.5" />
      <path d="M3 20c0-3 2-5 5-5" />
      <path d="M21 20c0-3-2-5-5-5" />
      <circle cx="12" cy="14" r="1.5" />
      <path d="M9 20c0-1.5 1.3-2.5 3-2.5s3 1 3 2.5" />
    </svg>
  );
}

export function MasteryChart({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <polyline points="3 17 9 11 13 15 21 7" />
      <polyline points="14 7 21 7 21 14" />
    </svg>
  );
}

export function TradeWrench({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.7 2.7-2.6-.4-.4-2.6z" />
    </svg>
  );
}

export function TutorChat({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" {...BASE}>
      <path d="M4 5h16v11H8l-4 4z" />
      <path d="M9 10h6M9 13h4" />
    </svg>
  );
}

export function HeroOrnament({ size = 56 }: { size?: number }) {
  // Concentric rings used as the rotating hero ornament.
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 56 56"
      fill="none"
      stroke="currentColor"
      aria-hidden="true"
    >
      <circle cx="28" cy="28" r="26" strokeWidth="1" opacity="0.5" />
      <circle cx="28" cy="28" r="18" strokeWidth="1" opacity="0.7" />
      <circle cx="28" cy="28" r="10" strokeWidth="1" />
      <circle cx="28" cy="28" r="1.5" fill="currentColor" stroke="none" />
      <line x1="28" y1="0" x2="28" y2="6" strokeWidth="1" />
      <line x1="28" y1="50" x2="28" y2="56" strokeWidth="1" />
      <line x1="0" y1="28" x2="6" y2="28" strokeWidth="1" />
      <line x1="50" y1="28" x2="56" y2="28" strokeWidth="1" />
    </svg>
  );
}

export function FourPointStar({ size = 12, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="currentColor"
      aria-hidden="true"
      className={className}
    >
      <path d="M8 0 L9 7 L16 8 L9 9 L8 16 L7 9 L0 8 L7 7 Z" />
    </svg>
  );
}
