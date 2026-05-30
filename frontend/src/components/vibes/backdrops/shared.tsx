"use client";

import type { CSSProperties, ReactNode } from "react";

// Full-viewport backdrop root: fixed, behind all content (z-index:-1),
// non-interactive. Sits between the body background and z-index:auto
// content, so it never occludes cards or text.
export function BackdropRoot({ children }: { children: ReactNode }) {
  return (
    <div
      aria-hidden="true"
      style={{
        position: "fixed",
        inset: 0,
        zIndex: -1,
        pointerEvents: "none",
        overflow: "hidden",
      }}
    >
      {children}
    </div>
  );
}

/**
 * A stretchy SVG layer (preserveAspectRatio="none", viewBox 0 0 100 100)
 * so coordinates read as viewport percentages (y=70 -> 70% height). Used
 * for organic shapes (gradients, waves, hills) where aspect distortion is
 * invisible. Round elements are rendered as positioned divs instead.
 */
export function StretchLayer({
  children,
  style,
}: {
  children: ReactNode;
  style?: CSSProperties;
}) {
  return (
    <svg
      width="100%"
      height="100%"
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      style={{ position: "absolute", inset: 0, display: "block", ...style }}
    >
      {children}
    </svg>
  );
}

/** Alternating sine-hill wave path filled down to the bottom edge. */
export function wavePath(y: number, amp: number, hills: number): string {
  const seg = 100 / hills;
  let d = `M0,${y}`;
  for (let i = 0; i < hills; i++) {
    const x0 = i * seg;
    const cx = x0 + seg / 2;
    const x1 = x0 + seg;
    const dir = i % 2 === 0 ? -1 : 1;
    d += ` Q${cx.toFixed(2)},${(y + dir * amp).toFixed(2)} ${x1.toFixed(2)},${y}`;
  }
  d += " L100,100 L0,100 Z";
  return d;
}
