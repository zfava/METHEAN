"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { MotifItem, MotifRoot, withDensity, type MotifLayerProps, type MotifSpec } from "./shared";

// Orbit: five small satellite-like geometric shapes.
const SPECS: MotifSpec[] = (() => {
  const rng = mulberry32(0x0721);
  return Array.from({ length: 5 }, () => ({
    left: range(rng, 6, 90),
    top: range(rng, 8, 80),
    size: range(rng, 26, 44),
    amplitude: range(rng, 5, 11),
    duration: range(rng, 9, 15),
    opacity: range(rng, 0.18, 0.25),
    rotate: range(rng, 0, 90),
  }));
})();

function Satellite() {
  return (
    <svg width="100%" height="100%" viewBox="0 0 40 40" fill="none" stroke="#7BD9F0" strokeWidth="2">
      <rect x="16" y="16" width="8" height="8" rx="1.5" fill="#7BD9F0" />
      <rect x="2" y="17" width="10" height="6" rx="1" />
      <rect x="28" y="17" width="10" height="6" rx="1" />
      <line x1="20" y1="16" x2="20" y2="8" />
      <circle cx="20" cy="6" r="2" fill="#7BD9F0" stroke="none" />
    </svg>
  );
}

export function MotifsOrbit({ density = 1 }: MotifLayerProps) {
  return (
    <MotifRoot>
      {withDensity(SPECS, density).map((spec, i) => (
        <MotifItem key={i} spec={spec}>
          <Satellite />
        </MotifItem>
      ))}
    </MotifRoot>
  );
}

export default MotifsOrbit;
