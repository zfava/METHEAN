"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { MotifItem, MotifRoot, withDensity, type MotifLayerProps, type MotifSpec } from "./shared";

// Calm: three soft clouds drifting slowly.
const SPECS: MotifSpec[] = (() => {
  const rng = mulberry32(0xca10);
  return Array.from({ length: 3 }, () => ({
    left: range(rng, 8, 80),
    top: range(rng, 8, 55),
    size: range(rng, 90, 150),
    amplitude: range(rng, 5, 10),
    duration: range(rng, 10, 16),
    opacity: range(rng, 0.15, 0.22),
  }));
})();

function Cloud() {
  return (
    <svg width="100%" height="100%" viewBox="0 0 100 60" fill="#FFFFFF">
      <ellipse cx="32" cy="38" rx="26" ry="16" />
      <ellipse cx="56" cy="32" rx="22" ry="18" />
      <ellipse cx="74" cy="40" rx="18" ry="13" />
      <rect x="14" y="38" width="66" height="16" rx="8" />
    </svg>
  );
}

export function MotifsCalm({ density = 1 }: MotifLayerProps) {
  return (
    <MotifRoot>
      {withDensity(SPECS, density).map((spec, i) => (
        <MotifItem key={i} spec={spec}>
          <Cloud />
        </MotifItem>
      ))}
    </MotifRoot>
  );
}

export default MotifsCalm;
