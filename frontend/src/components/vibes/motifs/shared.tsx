"use client";

import type { ReactNode } from "react";

import { AmbientFloat } from "@/lib/motion";

// Motif layer scaffolding. Motifs sit over the backdrop but behind
// content (same z-index:-1; DOM order places them above the backdrop).
// Each element drifts via AmbientFloat (auto-static under reduced-motion)
// and is capped at low opacity so it never competes with content.

export function MotifRoot({ children }: { children: ReactNode }) {
  return (
    <div
      aria-hidden="true"
      style={{ position: "fixed", inset: 0, zIndex: -1, pointerEvents: "none", overflow: "hidden" }}
    >
      {children}
    </div>
  );
}

export interface MotifSpec {
  left: number; // %
  top: number; // %
  size: number; // px
  amplitude: number; // px drift
  duration: number; // s
  opacity: number; // 0.15..0.25
  rotate?: number; // deg
}

export function MotifItem({ spec, children }: { spec: MotifSpec; children: ReactNode }) {
  // Rotation lives on an inner wrapper: AmbientFloat animates `transform`
  // (translateY), so a transform set on its own style would be clobbered.
  return (
    <AmbientFloat
      amplitude={spec.amplitude}
      duration={spec.duration}
      style={{
        position: "absolute",
        left: `${spec.left}%`,
        top: `${spec.top}%`,
        width: spec.size,
        height: spec.size,
        opacity: spec.opacity,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: spec.rotate ? `rotate(${spec.rotate}deg)` : undefined,
        }}
      >
        {children}
      </div>
    </AmbientFloat>
  );
}

export interface MotifLayerProps {
  /** FPS auto-scale: 1 = full, 0.5 = halved count. */
  density?: number;
}

/** Trim a motif list by the FPS-driven density factor. */
export function withDensity<T>(items: T[], density: number): T[] {
  return items.slice(0, Math.max(1, Math.ceil(items.length * density)));
}
