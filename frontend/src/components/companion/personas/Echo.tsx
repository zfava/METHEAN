"use client";

import { motion } from "framer-motion";

import { CompanionBase, type BaseConfig } from "./CompanionBase";
import type { PersonaProps } from "./types";

// Echo (default_gentle): gentle, contemplative, softly present. Very slow
// breath, wide eyes that close fully on blink, soft concentric wave
// ripples that continuously expand and fade.

const BREATH_SEC = 5.5;
const RIPPLE = "#9B8FCB";

const MOUTH = {
  neutral: "M-2.5,4 Q0,5 2.5,4",
  smile: "M-3,3.5 Q0,6 3,3.5",
  cheer: "M-3.5,3.4 Q0,6.5 3.5,3.4",
  frown: "M-2.5,4.6 Q0,3.8 2.5,4.6",
  sleep: "M-2,4 L2,4",
};

export function Echo(props: PersonaProps) {
  const reduce = props.reduceMotion ?? false;

  const ripples = reduce ? (
    <g fill="none" stroke={RIPPLE}>
      <circle cx={0} cy={0} r={26} strokeWidth={1} opacity={0.4} />
      <circle cx={0} cy={0} r={30} strokeWidth={1} opacity={0.2} />
    </g>
  ) : (
    <g fill="none" stroke={RIPPLE} strokeWidth={1}>
      <motion.circle
        cx={0}
        cy={0}
        animate={{ r: [14, 30], opacity: [0.45, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeOut" }}
      />
      <motion.circle
        cx={0}
        cy={0}
        animate={{ r: [14, 30], opacity: [0.45, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeOut", delay: 2 }}
      />
    </g>
  );

  const config: BaseConfig = {
    glow: "rgba(180,170,220,0.22)",
    inner: "rgba(180,170,220,0.85)",
    core: "#9B8FCB",
    eyeRx: 3,
    eyeRy: 2.5,
    eyeFill: "#FFFFFF",
    closeFully: true,
    mouth: MOUTH,
    mouthStroke: "#FFFFFF",
    breathScale: 1.03,
    breathDurationSec: BREATH_SEC,
    accentBehind: ripples,
  };

  return <CompanionBase config={config} {...props} />;
}
