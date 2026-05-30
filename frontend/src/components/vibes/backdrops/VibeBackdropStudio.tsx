"use client";

import { mulberry32, range } from "@/lib/vibe/rng";
import { BackdropRoot, StretchLayer } from "./shared";

// Studio: paper-cream ground with scattered muted brush strokes and two
// soft paint-splatter clusters. Static and gentle. Harmonizes with the
// studio token page (#FFF8E7).

const STROKE_COLORS = ["#E89B5C", "#6FA8A0", "#B47C9C"];

const STROKES = (() => {
  const rng = mulberry32(0x57d0);
  return Array.from({ length: 7 }, (_, i) => {
    const x = range(rng, 8, 88);
    const y = range(rng, 12, 86);
    const len = range(rng, 14, 30);
    const curve = range(rng, -8, 8);
    return {
      d: `M${x.toFixed(1)},${y.toFixed(1)} q${(len / 2).toFixed(1)},${curve.toFixed(1)} ${len.toFixed(1)},0`,
      color: STROKE_COLORS[i % STROKE_COLORS.length],
      width: range(rng, 1.2, 3),
      dash: `${range(rng, 2, 5).toFixed(1)} ${range(rng, 1, 3).toFixed(1)}`,
      opacity: range(rng, 0.15, 0.22),
    };
  });
})();

function Splatter({ cx, cy, seed }: { cx: number; cy: number; seed: number }) {
  const rng = mulberry32(seed);
  return (
    <g opacity={0.15}>
      {Array.from({ length: 7 }).map((_, i) => (
        <circle
          key={i}
          cx={cx + range(rng, -6, 6)}
          cy={cy + range(rng, -6, 6)}
          r={range(rng, 0.5, 2.2)}
          fill={STROKE_COLORS[i % STROKE_COLORS.length]}
        />
      ))}
    </g>
  );
}

export function VibeBackdropStudio() {
  return (
    <BackdropRoot>
      <div style={{ position: "absolute", inset: 0, background: "#FAF4E8" }} />
      <StretchLayer>
        {STROKES.map((s, i) => (
          <path
            key={i}
            d={s.d}
            fill="none"
            stroke={s.color}
            strokeWidth={s.width}
            strokeDasharray={s.dash}
            strokeLinecap="round"
            opacity={s.opacity}
          />
        ))}
        <Splatter cx={10} cy={12} seed={0x11} />
        <Splatter cx={90} cy={88} seed={0x22} />
      </StretchLayer>
    </BackdropRoot>
  );
}

export default VibeBackdropStudio;
