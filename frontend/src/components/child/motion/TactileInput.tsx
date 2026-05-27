"use client";

import { motion, useAnimation } from "framer-motion";
import { useEffect, useRef, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

/**
 * Focus-ring physics for form inputs and textareas.
 *
 * Wraps the input/textarea and renders a sibling ring layer that
 * scales 0.92 -> 1.0 with the confident curve on focusin, and fades
 * out on focusout. Gold border tint comes in over 200ms ease.
 *
 * The primitive doesn't capture the input value; it listens for
 * focus events on its container so any nested input/textarea works.
 */
interface TactileInputProps {
  children: ReactNode;
  className?: string;
}

export function TactileInput({ children, className }: TactileInputProps) {
  const { reduceMotion, speed } = useMotion();
  const ref = useRef<HTMLDivElement>(null);
  const ringControls = useAnimation();

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    if (reduceMotion) return;

    const onFocusIn = () => {
      ringControls.start({
        opacity: 1,
        scale: 1,
        transition: {
          duration: MOTION_DURATIONS_SEC.fast / speed,
          ease: MOTION_EASINGS.confident,
        },
      });
    };
    const onFocusOut = () => {
      ringControls.start({
        opacity: 0,
        scale: 0.96,
        transition: {
          duration: MOTION_DURATIONS_SEC.fast / speed,
          ease: MOTION_EASINGS.composed,
        },
      });
    };

    node.addEventListener("focusin", onFocusIn);
    node.addEventListener("focusout", onFocusOut);
    return () => {
      node.removeEventListener("focusin", onFocusIn);
      node.removeEventListener("focusout", onFocusOut);
    };
  }, [reduceMotion, speed, ringControls]);

  return (
    <div
      ref={ref}
      className={["relative", className ?? ""].join(" ").trim()}
    >
      {children}
      {!reduceMotion && (
        <motion.span
          aria-hidden="true"
          initial={{ opacity: 0, scale: 0.92 }}
          animate={ringControls}
          style={{
            position: "absolute",
            inset: -2,
            borderRadius: "inherit",
            border: "2px solid var(--color-brand-gold)",
            opacity: 0,
            pointerEvents: "none",
            zIndex: 1,
          }}
        />
      )}
    </div>
  );
}

export default TactileInput;
