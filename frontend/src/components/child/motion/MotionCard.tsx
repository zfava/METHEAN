"use client";

import { motion } from "framer-motion";
import { forwardRef, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

/**
 * Card primitive for the child surface.
 *
 * Defaults render a plain rounded-card div with the existing
 * --shadow-card token. Optional behaviors:
 *   - breathing :: 4-second 1.0 -> 1.005 -> 1.0 scale, gated on
 *                  useMotion().ambient. Offsets via the `phase` prop
 *                  so a row of cards doesn't beat in unison.
 *   - hoverLift :: hover translateY(-2px) + deeper shadow, confident.
 *   - onPress   :: tactile 0.985 scale on pointerdown.
 *
 * `depth` is a 0..1 modulation that multiplies the shadow weight
 * (default = useMotion().depth). Set to 0 to disable shadow.
 */
interface MotionCardProps {
  children: ReactNode;
  breathing?: boolean;
  hoverLift?: boolean;
  onPress?: () => void;
  /** Per-card phase offset (seconds) so a row of cards breathes out
   *  of phase. Pass the array index as `phase={index * 0.4}`. */
  phase?: number;
  /** 0..1. Overrides the global useMotion().depth value for this
   *  card. Use sparingly for hero cells. */
  depth?: number;
  className?: string;
  style?: React.CSSProperties;
  role?: string;
  tabIndex?: number;
  "aria-label"?: string;
  "aria-selected"?: boolean;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
  onFocus?: () => void;
  onBlur?: () => void;
  onClick?: () => void;
}

export const MotionCard = forwardRef<HTMLDivElement, MotionCardProps>(function MotionCard(
  {
    children,
    breathing = false,
    hoverLift = true,
    onPress,
    phase = 0,
    depth,
    className,
    style,
    onClick,
    ...rest
  },
  ref,
) {
  const motionState = useMotion();
  const effectiveDepth = depth ?? motionState.depth;

  const baseShadow =
    effectiveDepth > 0
      ? `0 ${1 * effectiveDepth}px ${3 * effectiveDepth}px rgba(0,0,0,${0.02 * effectiveDepth}), 0 ${4 * effectiveDepth}px ${12 * effectiveDepth}px rgba(0,0,0,${0.04 * effectiveDepth})`
      : "none";
  const liftedShadow =
    effectiveDepth > 0
      ? `0 ${4 * effectiveDepth}px ${16 * effectiveDepth}px rgba(0,0,0,${0.06 * effectiveDepth}), 0 ${12 * effectiveDepth}px ${40 * effectiveDepth}px rgba(0,0,0,${0.08 * effectiveDepth})`
      : "none";

  const mergedStyle: React.CSSProperties = {
    ...(style ?? {}),
    boxShadow: baseShadow,
  };

  if (motionState.reduceMotion) {
    return (
      <div
        ref={ref}
        className={className}
        style={mergedStyle}
        onClick={onPress ?? onClick}
        {...rest}
      >
        {children}
      </div>
    );
  }

  const breathingActive = breathing && motionState.ambient;
  const baseDuration = MOTION_DURATIONS_SEC.base / motionState.speed;

  return (
    <motion.div
      ref={ref}
      className={className}
      style={mergedStyle}
      initial={false}
      animate={breathingActive ? { scale: [1, 1.005, 1] } : undefined}
      transition={
        breathingActive
          ? {
              duration: 4,
              ease: MOTION_EASINGS.composed,
              repeat: Infinity,
              repeatType: "mirror",
              delay: phase,
            }
          : undefined
      }
      whileHover={
        hoverLift
          ? {
              y: -2,
              boxShadow: liftedShadow,
              transition: { duration: baseDuration, ease: MOTION_EASINGS.confident },
            }
          : undefined
      }
      whileTap={onPress ? { scale: 0.985 } : undefined}
      onTapStart={onPress ? () => onPress() : undefined}
      onClick={onClick}
      {...rest}
    >
      {children}
    </motion.div>
  );
});

export default MotionCard;
