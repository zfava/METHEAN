"use client";

import { motion } from "framer-motion";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

const MARK_PATH =
  "M 50 2 C 58 2, 80 11, 93 17 C 94 17.5, 94 18.5, 94 20 L 94 56 C 94 72, 88 86, 76 96 C 68 103, 58 109, 50 113 C 42 109, 32 103, 24 96 C 12 86, 6 72, 6 56 L 6 20 C 6 18.5, 6 17.5, 7 17 C 20 11, 42 2, 50 2 Z M 21.5 84.5 L 21 28 L 50 51 L 79 28 L 78.5 84.5 L 65.5 84.5 L 65 46 L 50 58.5 L 35 46 L 34.5 84.5 Z";

/**
 * METHEAN shield drawn in with pathLength 0 -> 1.
 *
 * Used inside MilestoneMoment and any hero composition that wants
 * the brand mark to *arrive* rather than appear. Renders the same
 * SVG path that components/Brand.tsx draws statically, so the visual
 * identity is identical when fully drawn.
 *
 * Under reduceMotion, renders the path filled instantly. Stroke
 * variant is also available for a more "etched" feel — pass
 * `variant="stroke"`.
 */
interface ShieldDrawProps {
  size?: number;
  color?: string;
  delay?: number;
  /** "fill" draws the outline then fills; "stroke" leaves it as a
   *  hairline outline. Default "fill". */
  variant?: "fill" | "stroke";
}

export function ShieldDraw({
  size = 56,
  color = "var(--color-brand-gold)",
  delay = 0,
  variant = "fill",
}: ShieldDrawProps) {
  const { reduceMotion, speed } = useMotion();
  const h = size;
  const w = Math.round(size * (100 / 115));

  if (reduceMotion) {
    return (
      <svg viewBox="0 0 100 115" width={w} height={h} aria-hidden="true">
        <path fillRule="evenodd" clipRule="evenodd" d={MARK_PATH} fill={color} />
      </svg>
    );
  }

  const drawDuration = MOTION_DURATIONS_SEC.cinematic / speed;
  const fillDelay = drawDuration * 0.75 + delay;

  return (
    <svg viewBox="0 0 100 115" width={w} height={h} aria-hidden="true">
      <motion.path
        d={MARK_PATH}
        fill={variant === "fill" ? color : "transparent"}
        stroke={color}
        strokeWidth={1.2}
        fillRule="evenodd"
        clipRule="evenodd"
        initial={{ pathLength: 0, fillOpacity: variant === "fill" ? 0 : 1 }}
        animate={{
          pathLength: 1,
          fillOpacity: variant === "fill" ? 1 : 0,
        }}
        transition={{
          pathLength: {
            duration: drawDuration,
            ease: MOTION_EASINGS.cinematic,
            delay,
          },
          fillOpacity:
            variant === "fill"
              ? {
                  duration: drawDuration * 0.4,
                  ease: MOTION_EASINGS.confident,
                  delay: fillDelay,
                }
              : undefined,
        }}
      />
    </svg>
  );
}

export default ShieldDraw;
