"use client";

import { motion, type Variants } from "framer-motion";
import { Children, isValidElement, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS, MOTION_STAGGER_SEC } from "@/lib/motion/tokens";
import type { StaggerGap } from "@/lib/motion/tokens";

/**
 * Wrap a list and entrance the children sequentially.
 *
 * Each direct child receives opacity 0->1 + translateY 12->0 with the
 * confident curve. Gap is selected by the `gap` prop and maps to the
 * MOTION_STAGGER_SEC constants. Under reduceMotion the children
 * render statically.
 */
interface StaggerProps {
  gap?: StaggerGap;
  children: ReactNode;
  className?: string;
  style?: React.CSSProperties;
  as?: "div" | "ul" | "ol" | "section" | "nav" | "footer" | "header";
}

const childVariants: Variants = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0 },
};

export function Stagger({
  gap = "base",
  children,
  className,
  style,
  as = "div",
}: StaggerProps) {
  const { reduceMotion, speed } = useMotion();
  const Tag = as;

  if (reduceMotion) {
    return (
      <Tag className={className} style={style}>
        {children}
      </Tag>
    );
  }

  const childDuration = MOTION_DURATIONS_SEC.base / speed;
  const staggerDelay = MOTION_STAGGER_SEC[gap] / speed;

  const containerVariants: Variants = {
    hidden: {},
    show: {
      transition: {
        staggerChildren: staggerDelay,
        delayChildren: 0.05,
      },
    },
  };

  const MotionTag = motion[as];

  // Wrap each direct child in a motion.div so consumers don't have to
  // know about variants. Keeps the public API trivial.
  const wrapped = Children.map(children, (child, i) => {
    if (!isValidElement(child)) return child;
    return (
      <motion.div
        key={i}
        variants={childVariants}
        transition={{ duration: childDuration, ease: MOTION_EASINGS.confident }}
      >
        {child}
      </motion.div>
    );
  });

  return (
    <MotionTag
      className={className}
      style={style}
      initial="hidden"
      animate="show"
      variants={containerVariants}
    >
      {wrapped}
    </MotionTag>
  );
}

export default Stagger;
