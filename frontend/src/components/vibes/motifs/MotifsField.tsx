"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { MotifItem, MotifRoot, withDensity, type MotifLayerProps, type MotifSpec } from "./shared";

// Field: four small leaf/flower shapes.
const SPECS: MotifSpec[] = (() => {
  const rng = mulberry32(0xf1e1);
  return Array.from({ length: 4 }, () => ({
    left: range(rng, 6, 88),
    top: range(rng, 10, 70),
    size: range(rng, 28, 46),
    amplitude: range(rng, 6, 12),
    duration: range(rng, 7, 13),
    opacity: range(rng, 0.18, 0.25),
    rotate: range(rng, -25, 25),
  }));
})();

function Leaf({ index }: { index: number }) {
  if (index % 2 === 0) {
    // Leaf
    return (
      <svg width="100%" height="100%" viewBox="0 0 40 40">
        <path d="M20 4 C34 10 34 30 20 38 C6 30 6 10 20 4 Z" fill="#5E7C36" />
        <path d="M20 6 L20 36" stroke="#3F5723" strokeWidth="1.5" fill="none" />
      </svg>
    );
  }
  // Flower
  return (
    <svg width="100%" height="100%" viewBox="0 0 40 40">
      {[0, 72, 144, 216, 288].map((a) => (
        <ellipse key={a} cx="20" cy="9" rx="5" ry="9" fill="#C9A24E" transform={`rotate(${a} 20 20)`} />
      ))}
      <circle cx="20" cy="20" r="5" fill="#6B8A3E" />
    </svg>
  );
}

export function MotifsField({ density = 1 }: MotifLayerProps) {
  return (
    <MotifRoot>
      {withDensity(SPECS, density).map((spec, i) => (
        <MotifItem key={i} spec={spec}>
          <Leaf index={i} />
        </MotifItem>
      ))}
    </MotifRoot>
  );
}

export default MotifsField;
