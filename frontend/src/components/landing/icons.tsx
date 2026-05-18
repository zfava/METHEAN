const SVG_PROPS = {
  width: 24,
  height: 24,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.5,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

export function FeatureShield() {
  return (
    <svg {...SVG_PROPS}>
      <path d="M12 2L4 6v6c0 5 3.5 9.5 8 11 4.5-1.5 8-6 8-11V6z" />
    </svg>
  );
}

export function FeatureDoc() {
  return (
    <svg {...SVG_PROPS}>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <path d="M14 2v6h6" />
      <path d="M9 14l2 2 4-4" />
    </svg>
  );
}

export function FeatureFamily() {
  return (
    <svg {...SVG_PROPS}>
      <circle cx="9" cy="9" r="3" />
      <circle cx="16" cy="9" r="3" />
      <path d="M4 20c0-3 2-5 5-5" />
      <path d="M20 20c0-3-2-5-5-5" />
    </svg>
  );
}

export function FeatureChart() {
  return (
    <svg {...SVG_PROPS}>
      <polyline points="3 17 9 11 13 15 21 7" />
      <polyline points="14 7 21 7 21 14" />
    </svg>
  );
}

export function FeatureWrench() {
  return (
    <svg {...SVG_PROPS}>
      <path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.7 2.7-2.6-.4-.4-2.6z" />
    </svg>
  );
}

export function FeatureLightbulb() {
  return (
    <svg {...SVG_PROPS}>
      <path d="M12 2a7 7 0 0 1 4 12.7c-.7.5-1 1.3-1 2.1V18H9v-1.2c0-.8-.3-1.6-1-2.1A7 7 0 0 1 12 2z" />
      <path d="M9 18h6" />
      <path d="M10 22h4" />
    </svg>
  );
}

// Small inline icons used for non-feature surfaces.

export function CheckIcon({ size = 16, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className={className}
    >
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

export function CrossIcon({ size = 16, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className={className}
    >
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

export function ChevronIcon({ size = 16, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className={className}
    >
      <polyline points="9 6 15 12 9 18" />
    </svg>
  );
}
