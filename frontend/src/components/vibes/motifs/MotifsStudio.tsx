"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { MotifItem, MotifRoot, withDensity, type MotifLayerProps, type MotifSpec } from "./shared";

// Studio: five small art-supply shapes (paintbrush, palette, pencil).
const SPECS: MotifSpec[] = (() => {
  const rng = mulberry32(0x57a1);
  return Array.from({ length: 5 }, () => ({
    left: range(rng, 6, 88),
    top: range(rng, 10, 78),
    size: range(rng, 30, 48),
    amplitude: range(rng, 5, 10),
    duration: range(rng, 8, 14),
    opacity: range(rng, 0.18, 0.25),
    rotate: range(rng, -30, 30),
  }));
})();

function ArtSupply({ index }: { index: number }) {
  switch (index % 3) {
    case 0: // paintbrush
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40">
          <rect x="18" y="4" width="4" height="20" rx="2" fill="#B47C9C" />
          <path d="M16 22 h8 l-2 12 h-4 Z" fill="#E89B5C" />
        </svg>
      );
    case 1: // palette
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40">
          <path d="M20 6 C32 6 36 16 32 24 C29 30 22 28 22 33 C22 37 10 36 7 28 C4 18 8 6 20 6 Z" fill="#FBEFD8" stroke="#B47C9C" strokeWidth="1.5" />
          <circle cx="15" cy="16" r="2.5" fill="#E89B5C" />
          <circle cx="24" cy="14" r="2.5" fill="#6FA8A0" />
          <circle cx="27" cy="22" r="2.5" fill="#B47C9C" />
        </svg>
      );
    default: // pencil
      return (
        <svg width="100%" height="100%" viewBox="0 0 40 40">
          <rect x="17" y="6" width="6" height="24" fill="#6FA8A0" transform="rotate(25 20 20)" />
          <path d="M17 30 l3 6 l3 -6 Z" fill="#3A2A2A" transform="rotate(25 20 20)" />
        </svg>
      );
  }
}

export function MotifsStudio({ density = 1 }: MotifLayerProps) {
  return (
    <MotifRoot>
      {withDensity(SPECS, density).map((spec, i) => (
        <MotifItem key={i} spec={spec}>
          <ArtSupply index={i} />
        </MotifItem>
      ))}
    </MotifRoot>
  );
}

export default MotifsStudio;
