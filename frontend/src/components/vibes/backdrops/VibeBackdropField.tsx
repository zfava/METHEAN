"use client";

import { AmbientFloat } from "@/lib/motion";

import { mulberry32, range } from "@/lib/vibe/rng";
import { BackdropRoot, StretchLayer } from "./shared";

// Field: morning sky over three rolling hills with a few trees and a
// drifting dust-mote layer. Harmonizes with the field token page.

const TREES = (() => {
  const rng = mulberry32(0x1e1d);
  // Deterministic placement along the hills.
  return [
    { x: 18, bottom: 18, scale: 1.0, tone: "#6B8A3E" },
    { x: 48, bottom: 22, scale: 1.25, tone: "#8FAB5A" },
    { x: 79, bottom: 16, scale: 0.85, tone: "#6B8A3E" },
  ].map((t) => ({ ...t, x: t.x + range(rng, -3, 3) }));
})();

const MOTES = (() => {
  const rng = mulberry32(0x9a3c);
  return Array.from({ length: 12 }, () => ({
    left: range(rng, 4, 96),
    top: range(rng, 4, 33),
    size: range(rng, 1.5, 3),
    opacity: range(rng, 0.1, 0.25),
    amplitude: range(rng, 4, 10),
    duration: range(rng, 6, 12),
  }));
})();

function Tree({ x, bottom, scale, tone }: { x: number; bottom: number; scale: number; tone: string }) {
  return (
    <svg
      width={44 * scale}
      height={56 * scale}
      viewBox="0 0 44 56"
      style={{ position: "absolute", left: `${x}%`, bottom: `${bottom}%`, transform: "translateX(-50%)" }}
    >
      <rect x="19" y="38" width="6" height="18" rx="2" fill="#5A4A2A" />
      <path
        d="M22 2 C34 4 42 16 38 28 C44 30 40 42 28 40 C24 46 14 44 14 36 C2 36 2 22 12 20 C8 8 16 0 22 2 Z"
        fill={tone}
      />
    </svg>
  );
}

export function VibeBackdropField() {
  return (
    <BackdropRoot>
      <StretchLayer>
        <defs>
          <linearGradient id="field-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#F4E8C0" />
            <stop offset="100%" stopColor="#E8D8A8" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="100" height="100" fill="url(#field-sky)" />
        {/* Rolling hills */}
        <path d="M0,65 Q50,55 100,65 L100,100 L0,100 Z" fill="#B8C97A" />
        <path d="M0,75 Q50,67 100,75 L100,100 L0,100 Z" fill="#8FAB5A" />
        <path d="M0,85 Q50,79 100,85 L100,100 L0,100 Z" fill="#6B8A3E" />
      </StretchLayer>

      {TREES.map((t, i) => (
        <Tree key={i} {...t} />
      ))}

      {MOTES.map((m, i) => (
        <AmbientFloat
          key={i}
          amplitude={m.amplitude}
          duration={m.duration}
          style={{
            position: "absolute",
            left: `${m.left}%`,
            top: `${m.top}%`,
            width: m.size,
            height: m.size,
            borderRadius: "50%",
            background: "#FBF6E4",
            opacity: m.opacity,
          }}
        >
          <span />
        </AmbientFloat>
      ))}
    </BackdropRoot>
  );
}

export default VibeBackdropField;
