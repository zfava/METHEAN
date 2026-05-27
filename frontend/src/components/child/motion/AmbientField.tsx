"use client";

import { motion } from "framer-motion";
import { useMemo } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_EASINGS } from "@/lib/motion/tokens";

/**
 * Ambient drift behind child content.
 *
 * Two visual modes:
 *   stellar :: slow drifting gold points over a navy gradient. Used
 *              for milestone moments and for the dark welcome shell.
 *   warm    :: slow cream-to-parchment gradient sweep. The everyday
 *              default for the parchment-colored child surface.
 *
 * Mode is chosen by an optional `mode` prop, otherwise read from
 * Vibe.tokens["ambient_mode"] if present, otherwise "warm". Never
 * renders an animation when useMotion().ambient is false; falls back
 * to a static gradient so the visual identity is consistent.
 *
 * Pure visual: pointer-events disabled, aria-hidden true.
 */
interface AmbientFieldProps {
  mode?: "stellar" | "warm";
  /** Optional opacity ceiling for the layer; primitives can damp it
   *  inside heavy-content screens. Defaults to 1. */
  intensity?: number;
}

export function AmbientField({ mode = "warm", intensity = 1 }: AmbientFieldProps) {
  const { ambient, reduceMotion } = useMotion();

  const baseStyle = useMemo<React.CSSProperties>(
    () => ({
      position: "absolute",
      inset: 0,
      pointerEvents: "none",
      opacity: Math.max(0, Math.min(1, intensity)),
      zIndex: 0,
    }),
    [intensity],
  );

  // Static fallback: render the gradient without any motion.
  if (!ambient || reduceMotion) {
    return (
      <div
        aria-hidden="true"
        style={{
          ...baseStyle,
          background:
            mode === "stellar"
              ? "radial-gradient(ellipse at 20% 25%, rgba(198,162,78,0.10) 0%, transparent 55%), radial-gradient(ellipse at 80% 70%, rgba(74,111,165,0.08) 0%, transparent 55%), linear-gradient(180deg, #0F1B2D 0%, #1A2740 100%)"
              : "radial-gradient(ellipse at 50% 0%, rgba(198,162,78,0.10) 0%, transparent 70%), linear-gradient(180deg, var(--color-page) 0%, var(--color-surface) 100%)",
        }}
      />
    );
  }

  return (
    <div aria-hidden="true" style={baseStyle}>
      {mode === "stellar" ? (
        <motion.div
          style={{
            position: "absolute",
            inset: "-10%",
            background:
              "radial-gradient(ellipse at 20% 25%, rgba(198,162,78,0.18) 0%, transparent 55%), radial-gradient(ellipse at 80% 70%, rgba(74,111,165,0.12) 0%, transparent 55%), linear-gradient(180deg, #0F1B2D 0%, #1A2740 100%)",
            filter: "blur(40px)",
          }}
          animate={{
            x: ["0%", "-3%", "0%"],
            y: ["0%", "-2%", "0%"],
            scale: [1, 1.04, 1],
          }}
          transition={{
            duration: 28,
            ease: MOTION_EASINGS.composed,
            repeat: Infinity,
            repeatType: "mirror",
          }}
        />
      ) : (
        <motion.div
          style={{
            position: "absolute",
            inset: "-6%",
            background:
              "radial-gradient(ellipse at 50% 0%, rgba(198,162,78,0.12) 0%, transparent 70%), linear-gradient(180deg, var(--color-page) 0%, var(--color-surface) 100%)",
            filter: "blur(60px)",
          }}
          animate={{
            x: ["0%", "1.5%", "-1%", "0%"],
            y: ["0%", "-1%", "1%", "0%"],
          }}
          transition={{
            duration: 36,
            ease: MOTION_EASINGS.composed,
            repeat: Infinity,
            repeatType: "loop",
          }}
        />
      )}
    </div>
  );
}

export default AmbientField;
