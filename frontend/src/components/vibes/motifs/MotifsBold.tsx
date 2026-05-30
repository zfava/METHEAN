"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { MotifItem, MotifRoot, withDensity, type MotifLayerProps, type MotifSpec } from "./shared";

// Bold: three large geometric shapes (triangle, square, circle).
const SPECS: MotifSpec[] = (() => {
  const rng = mulberry32(0xb01d);
  return Array.from({ length: 3 }, () => ({
    left: range(rng, 8, 78),
    top: range(rng, 10, 66),
    size: range(rng, 120, 180),
    amplitude: range(rng, 8, 14),
    duration: range(rng, 6, 11),
    opacity: range(rng, 0.15, 0.2),
    rotate: range(rng, 0, 45),
  }));
})();

function Geometric({ index }: { index: number }) {
  const fill = "#FFFFFF";
  switch (index % 3) {
    case 0: // triangle
      return (
        <svg width="100%" height="100%" viewBox="0 0 100 100">
          <path d="M50 8 L92 88 L8 88 Z" fill={fill} />
        </svg>
      );
    case 1: // square
      return (
        <svg width="100%" height="100%" viewBox="0 0 100 100">
          <rect x="14" y="14" width="72" height="72" rx="6" fill={fill} />
        </svg>
      );
    default: // circle
      return (
        <svg width="100%" height="100%" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="42" fill={fill} />
        </svg>
      );
  }
}

export function MotifsBold({ density = 1 }: MotifLayerProps) {
  return (
    <MotifRoot>
      {withDensity(SPECS, density).map((spec, i) => (
        <MotifItem key={i} spec={spec}>
          <Geometric index={i} />
        </MotifItem>
      ))}
    </MotifRoot>
  );
}

export default MotifsBold;
