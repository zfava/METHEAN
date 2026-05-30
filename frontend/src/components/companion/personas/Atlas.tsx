"use client";

import { useId } from "react";

import { CompanionBase, type BaseConfig } from "./CompanionBase";
import type { PersonaProps } from "./types";

// Atlas (default_steady): grounded, reliable, calm strength. Very slow
// steady breath, infrequent deliberate blinks, a stable ground-line
// beneath the body for a sense of weight. Reserved, low-amplitude mouth.

const BREATH_SEC = 5;

const MOUTH = {
  neutral: "M-3,4 Q0,4.6 3,4",
  smile: "M-3.5,3.6 Q0,5.4 3.5,3.6",
  cheer: "M-4,3.5 Q0,6 4,3.5",
  frown: "M-3,4.6 Q0,3.8 3,4.6",
  sleep: "M-2,4 L2,4",
};

export function Atlas(props: PersonaProps) {
  const gid = useId().replace(/:/g, "");

  const ground = (
    <g>
      <defs>
        <linearGradient id={`atlas-ground-${gid}`} x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#C6A24E" stopOpacity="0" />
          <stop offset="50%" stopColor="#C6A24E" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#C6A24E" stopOpacity="0" />
        </linearGradient>
      </defs>
      <line x1={-15} y1={24} x2={15} y2={24} stroke={`url(#atlas-ground-${gid})`} strokeWidth={2} strokeLinecap="round" />
    </g>
  );

  const config: BaseConfig = {
    glow: "rgba(74,90,120,0.18)",
    inner: "#1A2740",
    core: "#4A5A78",
    eyeRx: 1.8,
    eyeRy: 2,
    eyeFill: "#FAFAF8",
    mouth: MOUTH,
    mouthStroke: "#FAFAF8",
    breathScale: 1.02,
    breathDurationSec: BREATH_SEC,
    accentFront: ground,
  };

  return <CompanionBase config={config} {...props} />;
}
