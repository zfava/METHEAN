"use client";

import { motion } from "framer-motion";

import { CompanionBase, type BaseConfig } from "./CompanionBase";
import type { PersonaProps } from "./types";

// Sage (default_warm): warm guide, deliberate, kind. Slow breathing,
// gentle blink, golden spokes that pulse with the breath.

const BREATH_SEC = 4;
const SPOKE_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];

const MOUTH = {
  neutral: "M-3,4 Q0,5 3,4",
  smile: "M-4,3 Q0,7 4,3",
  cheer: "M-5,3 Q0,8 5,3",
  frown: "M-3,5 Q0,3 3,5",
  sleep: "M-2,4 L2,4",
};

export function Sage(props: PersonaProps) {
  const reduce = props.reduceMotion ?? false;
  const speed = props.speed ?? 1;

  const spokes = (
    <motion.g
      stroke="#C6A24E"
      strokeWidth={2}
      strokeLinecap="round"
      animate={reduce ? { opacity: 0.6 } : { opacity: [0.4, 0.7, 0.4] }}
      transition={reduce ? { duration: 0 } : { duration: BREATH_SEC / Math.max(0.25, speed), repeat: Infinity, ease: "easeInOut" }}
    >
      {SPOKE_ANGLES.map((deg) => {
        const r = (deg * Math.PI) / 180;
        return (
          <line
            key={deg}
            x1={Math.cos(r) * 23}
            y1={Math.sin(r) * 23}
            x2={Math.cos(r) * 29}
            y2={Math.sin(r) * 29}
          />
        );
      })}
    </motion.g>
  );

  const config: BaseConfig = {
    glow: "rgba(198,162,78,0.18)",
    inner: "rgba(198,162,78,0.85)",
    core: "#C6A24E",
    eyeRx: 2,
    eyeRy: 2.5,
    eyeFill: "#FAFAF8",
    mouth: MOUTH,
    mouthStroke: "#FAFAF8",
    breathScale: 1.04,
    breathDurationSec: BREATH_SEC,
    accentBehind: spokes,
  };

  return <CompanionBase config={config} {...props} />;
}
