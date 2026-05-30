"use client";

import { CompanionBase, type BaseConfig } from "./CompanionBase";
import type { PersonaProps } from "./types";

// Nova (default_playful): playful, exuberant, loves attention. Medium
// breathing, expressive tilted eyes, a default that already leans into a
// smile. No idle accent; tap confetti is fired by CompanionStage through
// the celebration engine (buildTapBurst), not owned here.

const BREATH_SEC = 3;

const MOUTH = {
  neutral: "M-4,3.6 Q0,6.4 4,3.6",
  smile: "M-4.5,3.2 Q0,8 4.5,3.2",
  cheer: "M-5.5,3 Q0,9.5 5.5,3",
  frown: "M-3.5,5 Q0,3 3.5,5",
  sleep: "M-2,4 L2,4",
};

export function Nova(props: PersonaProps) {
  const config: BaseConfig = {
    glow: "rgba(255,122,69,0.22)",
    inner: "rgba(255,122,69,0.9)",
    core: "#FF7A45",
    eyeRx: 2.3,
    eyeRy: 2.8,
    eyeFill: "#FFFFFF",
    eyeTilt: 5,
    mouth: MOUTH,
    mouthStroke: "#FFFFFF",
    breathScale: 1.05,
    breathDurationSec: BREATH_SEC,
  };

  return <CompanionBase config={config} {...props} />;
}
