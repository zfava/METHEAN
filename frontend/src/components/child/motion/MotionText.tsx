"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

/**
 * Headline entrance with optional weight settle.
 *
 *   weight=true   :: font-weight transitions 400 -> 600 over 520ms.
 *                    Use on the screen's hero headline only.
 *   entrance=true :: opacity 0 -> 1 + translateY 8 -> 0 over 520ms.
 *                    Use on subsequent headings.
 *
 * Inherits its rendered tag from the `as` prop so we never break
 * heading hierarchy.
 */
type ElementTag = "h1" | "h2" | "h3" | "p" | "span" | "div";

interface MotionTextProps {
  as?: ElementTag;
  weight?: boolean;
  entrance?: boolean;
  delay?: number;
  className?: string;
  style?: React.CSSProperties;
  children: ReactNode;
}

export function MotionText({
  as = "h2",
  weight = false,
  entrance = true,
  delay = 0,
  className,
  style,
  children,
}: MotionTextProps) {
  const { reduceMotion, speed } = useMotion();
  const Tag = as;

  if (reduceMotion || !entrance) {
    return (
      <Tag className={className} style={style}>
        {children}
      </Tag>
    );
  }

  const duration = MOTION_DURATIONS_SEC.slow / speed;
  const initial = weight
    ? { opacity: 0, y: 8, fontWeight: 400 }
    : { opacity: 0, y: 8 };
  const animate = weight ? { opacity: 1, y: 0, fontWeight: 600 } : { opacity: 1, y: 0 };

  const MotionTag = motion[Tag];

  return (
    <MotionTag
      className={className}
      style={style}
      initial={initial}
      animate={animate}
      transition={{
        duration,
        ease: MOTION_EASINGS.confident,
        delay,
      }}
    >
      {children}
    </MotionTag>
  );
}

export default MotionText;
