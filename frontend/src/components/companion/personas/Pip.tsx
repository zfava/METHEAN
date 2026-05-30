"use client";

import { motion } from "framer-motion";

import { CompanionBase, type BaseConfig } from "./CompanionBase";
import type { PersonaProps } from "./types";

// Pip (default_bright): bright, energetic, curious. Faster breathing,
// frequent blinks, a single sparkle that orbits the body and pulses.

const BREATH_SEC = 2.5;
const STAR = "M0,-4 L1,-1 L4,0 L1,1 L0,4 L-1,1 L-4,0 L-1,-1 Z";

const MOUTH = {
  neutral: "M-3,4 Q0,5.5 3,4",
  smile: "M-4,3 Q0,8 4,3",
  cheer: "M-5,3 Q0,9 5,3",
  frown: "M-3,5 Q0,3 3,5",
  sleep: "M-2,4 L2,4",
};

export function Pip(props: PersonaProps) {
  const reduce = props.reduceMotion ?? false;
  const speed = props.speed ?? 1;

  const sparkle = reduce ? (
    <g transform="translate(0,-28)">
      <path d={STAR} fill="#FFE066" />
    </g>
  ) : (
    <motion.g
      animate={{ rotate: 360 }}
      transition={{ duration: 6 / Math.max(0.25, speed), repeat: Infinity, ease: "linear" }}
      style={{ transformOrigin: "0px 0px" }}
    >
      <g transform="translate(28,0)">
        <motion.g
          animate={{ scale: [0.8, 1, 0.8], rotate: 360 }}
          transition={{
            scale: { duration: 1.2, repeat: Infinity, ease: "easeInOut" },
            rotate: { duration: 3, repeat: Infinity, ease: "linear" },
          }}
          style={{ transformOrigin: "0px 0px" }}
        >
          <path d={STAR} fill="#FFE066" />
        </motion.g>
      </g>
    </motion.g>
  );

  const config: BaseConfig = {
    glow: "rgba(255,238,180,0.2)",
    inner: "rgba(255,238,180,0.85)",
    core: "#FFE066",
    eyeRx: 2.5,
    eyeRy: 3,
    eyeFill: "#6B5A1E",
    mouth: MOUTH,
    mouthStroke: "#6B5A1E",
    breathScale: 1.05,
    breathDurationSec: BREATH_SEC,
    accentFront: sparkle,
  };

  return <CompanionBase config={config} {...props} />;
}
