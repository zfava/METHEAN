"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useMemo, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

/**
 * View-to-view transition wrapper for the child surface.
 *
 *   fade  :: opacity only (the safe default).
 *   slide :: opacity + translateX 24px.
 *   page  :: signature paper-turn feel. The outgoing view fades and
 *            translates left while subtly tilting; the incoming view
 *            arrives with a small skew and settles. Used between the
 *            map -> activity transitions.
 *
 * A change in `viewKey` triggers the exit-then-enter. Pass a stable
 * key (e.g. the activity id or a phase name) and place the wrapper
 * inside the layout shell, not around the entire app.
 */
interface PageTransitionProps {
  viewKey: string;
  mode?: "fade" | "slide" | "page";
  children: ReactNode;
}

export function PageTransition({ viewKey, mode = "fade", children }: PageTransitionProps) {
  const { reduceMotion, speed } = useMotion();

  const variants = useMemo(() => {
    if (mode === "slide") {
      return {
        initial: { opacity: 0, x: 24 },
        animate: { opacity: 1, x: 0 },
        exit: { opacity: 0, x: -24 },
      };
    }
    if (mode === "page") {
      return {
        initial: { opacity: 0, x: 28, rotateY: 4, transformPerspective: 1200 },
        animate: { opacity: 1, x: 0, rotateY: 0 },
        exit: { opacity: 0, x: -28, rotateY: -2 },
      };
    }
    return {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
      exit: { opacity: 0 },
    };
  }, [mode]);

  if (reduceMotion) {
    return <>{children}</>;
  }

  const dur = MOTION_DURATIONS_SEC.base / speed;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={viewKey}
        initial={variants.initial}
        animate={variants.animate}
        exit={variants.exit}
        transition={{ duration: dur, ease: MOTION_EASINGS.confident }}
        style={{ minHeight: "inherit" }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

export default PageTransition;
