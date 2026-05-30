"use client";

import { BackdropRoot } from "./shared";

// Workshop: warm wood-grain at a slight angle, a faint grain (turbulence)
// overlay, a pegboard with tool silhouettes on the right, and a floor
// band. Harmonized darker than dawn vibes to match the workshop token
// page (#3A2718) and keep its light text readable.

const PEG_ROWS = 9;
const PEG_COLS = 3;

export function VibeBackdropWorkshop() {
  return (
    <BackdropRoot>
      {/* Wood-grain striped gradient, rotated 2deg, oversized to avoid
          gaps at the corners. */}
      <div
        style={{
          position: "absolute",
          inset: "-10%",
          transform: "rotate(2deg)",
          backgroundColor: "#4A3525",
          backgroundImage:
            "repeating-linear-gradient(90deg, #6B4F35 0px, #4A3525 36px, #5C4632 72px, #6B4F35 110px)",
        }}
      />

      {/* Faint grain */}
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, opacity: 0.05 }}>
        <filter id="ws-grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} stitchTiles="stitch" />
        </filter>
        <rect width="100%" height="100%" filter="url(#ws-grain)" />
      </svg>

      {/* Floor band */}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: "12%", background: "rgba(0,0,0,0.22)" }} />

      {/* Pegboard + tool silhouettes on the right edge */}
      <svg
        width="160"
        height="100%"
        viewBox="0 0 160 600"
        preserveAspectRatio="xMaxYMid slice"
        style={{ position: "absolute", right: 0, top: 0, opacity: 0.5 }}
      >
        {Array.from({ length: PEG_ROWS }).map((_, r) =>
          Array.from({ length: PEG_COLS }).map((__, c) => (
            <circle key={`${r}-${c}`} cx={40 + c * 40} cy={50 + r * 60} r={3} fill="#2A1C12" />
          )),
        )}
        {/* Hammer */}
        <g opacity={0.6} transform="translate(28,120)">
          <rect x="14" y="0" width="6" height="70" rx="2" fill="#2A1C12" />
          <rect x="0" y="-6" width="34" height="16" rx="3" fill="#2A1C12" />
        </g>
        {/* Ruler */}
        <g opacity={0.6} transform="translate(70,300)">
          <rect x="0" y="0" width="12" height="120" rx="2" fill="#2A1C12" />
          {Array.from({ length: 6 }).map((_, i) => (
            <rect key={i} x="0" y={12 + i * 18} width="6" height="2" fill="#6B4F35" />
          ))}
        </g>
      </svg>
    </BackdropRoot>
  );
}

export default VibeBackdropWorkshop;
