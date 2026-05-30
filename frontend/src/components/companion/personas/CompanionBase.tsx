"use client";

import { motion } from "framer-motion";
import { useEffect, useState, type ReactNode } from "react";

import type { CompanionState } from "../state";
import type { MouthSet, PersonaProps } from "./types";

// Shared rendering for all five personas: a breathing head, gaze-tracking
// blinking eyes that respond to state, a morphing mouth, an optional Zzz on
// sleep, and slots for persona-specific accents. Everything is driven by
// plain framer-motion (no MotionContext) so personas render anywhere.

export interface BaseConfig {
  /** Outer glow circle fill (rgba), r=22. */
  glow: string;
  /** Inner circle fill (rgba), r=14. */
  inner: string;
  /** Core circle fill (hex), r=8. */
  core: string;
  eyeRx: number;
  eyeRy: number;
  eyeFill: string;
  /** Per-eye inward tilt in degrees (Nova). */
  eyeTilt?: number;
  /** Echo closes its eyes fully (ry -> 0) rather than to a slit. */
  closeFully?: boolean;
  mouth: MouthSet;
  mouthStroke: string;
  mouthStrokeWidth?: number;
  breathScale: number;
  breathDurationSec: number;
  accentBehind?: ReactNode;
  accentFront?: ReactNode;
}

const EYE_GAP = 5;
const EYE_CY = -2;
const MAX_GAZE_PX = 2;

function clamp(v: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, v));
}

function mouthPath(state: CompanionState, m: MouthSet): string {
  switch (state) {
    case "celebrate":
      return m.cheer;
    case "commiserate":
      return m.frown;
    case "sleep":
      return m.sleep;
    case "focus":
      return m.smile;
    case "thinking":
    case "idle":
    default:
      return m.neutral;
  }
}

/** Eye geometry (vertical radius + center-y) for a state. */
function eyeShape(
  state: CompanionState,
  drowsy: boolean,
  blinking: boolean,
  baseRy: number,
  closeFully: boolean,
): { ry: number; cy: number } {
  switch (state) {
    case "sleep":
      return { ry: closeFully ? 0.01 : baseRy * 0.06, cy: EYE_CY + 1 };
    case "celebrate":
      return { ry: baseRy * 0.18, cy: EYE_CY }; // squeezed happy
    case "surprised":
      return { ry: baseRy * 1.3, cy: EYE_CY }; // widened, no blink
    case "commiserate":
      return { ry: baseRy * 0.7, cy: EYE_CY + 2 }; // drooped
    default: {
      const open = blinking ? 0.06 : drowsy ? 0.45 : 1;
      return { ry: baseRy * open, cy: EYE_CY };
    }
  }
}

export function CompanionBase({
  config,
  state,
  size = 56,
  gaze = { x: 0, y: 0 },
  speed = 1,
  reduceMotion = false,
  drowsy = false,
}: { config: BaseConfig } & PersonaProps) {
  const [blinking, setBlinking] = useState(false);

  // Randomized blink, only in open resting states and not while drowsy.
  useEffect(() => {
    if (reduceMotion) {
      setBlinking(false);
      return;
    }
    const blinkable = state === "idle" || state === "focus" || state === "thinking";
    if (!blinkable || drowsy) {
      setBlinking(false);
      return;
    }
    let openTimer: ReturnType<typeof setTimeout>;
    let closeTimer: ReturnType<typeof setTimeout>;
    const schedule = () => {
      openTimer = setTimeout(
        () => {
          setBlinking(true);
          closeTimer = setTimeout(() => {
            setBlinking(false);
            schedule();
          }, 180);
        },
        4000 + Math.random() * 4000,
      );
    };
    schedule();
    return () => {
      clearTimeout(openTimer);
      clearTimeout(closeTimer);
    };
  }, [reduceMotion, state, drowsy]);

  const { ry, cy } = eyeShape(state, drowsy, blinking, config.eyeRy, !!config.closeFully);

  // Gaze: tracked except when reduced-motion or in expressive/asleep states.
  const gazeActive =
    !reduceMotion && state !== "sleep" && state !== "celebrate" && state !== "surprised";
  const gx = gazeActive ? clamp(gaze.x, -1, 1) * MAX_GAZE_PX : 0;
  const gy = gazeActive ? clamp(gaze.y, -1, 1) * MAX_GAZE_PX : 0;

  const breathDur = config.breathDurationSec / Math.max(0.25, speed);
  const breathAnim = reduceMotion
    ? { scale: 1 }
    : { scale: [1, config.breathScale, 1] };
  const breathTransition = reduceMotion
    ? { duration: 0 }
    : { duration: breathDur, repeat: Infinity, ease: "easeInOut" as const };

  const eyeTransition = { duration: reduceMotion ? 0 : 0.12, ease: "easeOut" as const };
  const tiltL = config.eyeTilt ? `rotate(${-config.eyeTilt} ${-EYE_GAP} ${cy})` : undefined;
  const tiltR = config.eyeTilt ? `rotate(${config.eyeTilt} ${EYE_GAP} ${cy})` : undefined;

  return (
    <svg
      viewBox="0 0 64 64"
      width={size}
      height={size}
      role="img"
      aria-hidden="true"
      style={{ display: "block", overflow: "visible" }}
    >
      <g transform="translate(32,32)">
        {config.accentBehind}

        <motion.g animate={breathAnim} transition={breathTransition} style={{ transformOrigin: "0px 0px" }}>
          <circle cx={0} cy={0} r={22} fill={config.glow} />
          <circle cx={0} cy={0} r={14} fill={config.inner} />
          <circle cx={0} cy={0} r={8} fill={config.core} />

          {/* Eyes */}
          <motion.g animate={{ x: gx, y: gy }} transition={{ duration: reduceMotion ? 0 : 0.25, ease: "easeOut" }}>
            <motion.ellipse
              cx={-EYE_GAP}
              rx={config.eyeRx}
              fill={config.eyeFill}
              transform={tiltL}
              animate={{ ry, cy }}
              transition={eyeTransition}
            />
            <motion.ellipse
              cx={EYE_GAP}
              rx={config.eyeRx}
              fill={config.eyeFill}
              transform={tiltR}
              animate={{ ry, cy }}
              transition={eyeTransition}
            />
          </motion.g>

          {/* Mouth */}
          {state === "surprised" ? (
            <circle cx={0} cy={5} r={1.6} fill={config.eyeFill} />
          ) : (
            <motion.path
              animate={{ d: mouthPath(state, config.mouth) }}
              transition={{ duration: reduceMotion ? 0 : 0.2, ease: "easeOut" }}
              fill="none"
              stroke={config.mouthStroke}
              strokeWidth={config.mouthStrokeWidth ?? 1.2}
              strokeLinecap="round"
            />
          )}
        </motion.g>

        {config.accentFront}

        {/* Zzz on sleep */}
        {state === "sleep" && !reduceMotion && <Zzz />}
        {state === "sleep" && reduceMotion && (
          <text x={11} y={-12} fontSize={7} fill={config.core} opacity={0.7}>
            z
          </text>
        )}
      </g>
    </svg>
  );
}

function Zzz() {
  return (
    <g>
      {[0, 1, 2].map((i) => (
        <motion.text
          key={i}
          x={10 + i * 3}
          y={-12 - i * 4}
          fontSize={6 + i}
          fill="currentColor"
          initial={{ opacity: 0, y: -8 - i * 4 }}
          animate={{ opacity: [0, 0.8, 0], y: [-8 - i * 4, -16 - i * 4] }}
          transition={{ duration: 2.4, repeat: Infinity, delay: i * 0.5, ease: "easeOut" }}
          style={{ color: "var(--color-accent)" }}
        >
          z
        </motion.text>
      ))}
    </g>
  );
}
