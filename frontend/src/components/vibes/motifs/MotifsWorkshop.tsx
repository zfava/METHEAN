"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { MotifItem, MotifRoot, withDensity, type MotifLayerProps, type MotifSpec } from "./shared";

// Workshop: four small tool icons (wrench, gear, ruler, hammer).
const SPECS: MotifSpec[] = (() => {
  const rng = mulberry32(0x3007);
  return Array.from({ length: 4 }, () => ({
    left: range(rng, 8, 86),
    top: range(rng, 10, 72),
    size: range(rng, 30, 46),
    amplitude: range(rng, 4, 9),
    duration: range(rng, 8, 14),
    opacity: range(rng, 0.18, 0.25),
    rotate: range(rng, -20, 20),
  }));
})();

const TOOL = "#C8B8A0";

function Tool({ index }: { index: number }) {
  switch (index % 4) {
    case 0: // wrench
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40" fill={TOOL}>
          <path d="M27 6 a8 8 0 1 0 7 13 l-12 12 -5 -5 12 -12 a8 8 0 0 0 -2 -8 Z" />
        </svg>
      );
    case 1: // gear
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40" fill={TOOL}>
          {Array.from({ length: 8 }).map((_, i) => (
            <rect key={i} x="18" y="2" width="4" height="8" transform={`rotate(${i * 45} 20 20)`} />
          ))}
          <circle cx="20" cy="20" r="10" />
          <circle cx="20" cy="20" r="4" fill="#3A2718" />
        </svg>
      );
    case 2: // ruler
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40" fill={TOOL}>
          <rect x="6" y="14" width="28" height="12" rx="1" transform="rotate(20 20 20)" />
        </svg>
      );
    default: // hammer
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40" fill={TOOL}>
          <rect x="18" y="10" width="5" height="26" rx="2" transform="rotate(-15 20 20)" />
          <rect x="10" y="6" width="22" height="9" rx="2" transform="rotate(-15 20 20)" />
        </svg>
      );
  }
}

export function MotifsWorkshop({ density = 1 }: MotifLayerProps) {
  return (
    <MotifRoot>
      {withDensity(SPECS, density).map((spec, i) => (
        <MotifItem key={i} spec={spec}>
          <Tool index={i} />
        </MotifItem>
      ))}
    </MotifRoot>
  );
}

export default MotifsWorkshop;
