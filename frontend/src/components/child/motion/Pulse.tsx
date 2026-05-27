"use client";

import { motion } from "framer-motion";
import { useEffect, useRef, useState, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_EASINGS } from "@/lib/motion/tokens";

/**
 * Audio-reactive halo around the wrapped node.
 *
 * `intensity` is a 0..1 number. When the caller can't provide a
 * real amplitude reading, leave it undefined; the primitive falls
 * back to a slow 1.2Hz sine so the affordance still reads as alive.
 *
 * The halo is a layered radial glow plus a subtle outward ring that
 * scales 1.0 -> 1.10 with the amplitude. Under reduceMotion the
 * halo renders statically at base size.
 */
interface PulseProps {
  intensity?: number;
  color?: string;
  children: ReactNode;
  className?: string;
}

export function Pulse({
  intensity,
  color = "var(--color-danger)",
  children,
  className,
}: PulseProps) {
  const { reduceMotion } = useMotion();
  const [sinePhase, setSinePhase] = useState(0);
  const frameRef = useRef<number | null>(null);

  // If no real amplitude is provided, drive a slow sine. We do this
  // in useEffect with rAF so the animation can be killed on unmount.
  useEffect(() => {
    if (intensity !== undefined) return;
    if (reduceMotion) return;
    let mounted = true;
    const start = performance.now();
    const tick = (now: number) => {
      if (!mounted) return;
      const seconds = (now - start) / 1000;
      // 1.2Hz sine, mapped to 0.3..0.7 so the halo never collapses.
      setSinePhase(0.3 + 0.4 * (0.5 + 0.5 * Math.sin(2 * Math.PI * 1.2 * seconds)));
      frameRef.current = requestAnimationFrame(tick);
    };
    frameRef.current = requestAnimationFrame(tick);
    return () => {
      mounted = false;
      if (frameRef.current !== null) cancelAnimationFrame(frameRef.current);
    };
  }, [intensity, reduceMotion]);

  const effectiveIntensity =
    intensity !== undefined ? Math.max(0, Math.min(1, intensity)) : sinePhase;

  if (reduceMotion) {
    return (
      <div className={className} style={{ position: "relative", display: "inline-flex" }}>
        {children}
      </div>
    );
  }

  // Map intensity to a halo expansion and an opacity.
  const haloScale = 1 + effectiveIntensity * 0.55;
  const haloOpacity = 0.25 + effectiveIntensity * 0.5;

  return (
    <div className={className} style={{ position: "relative", display: "inline-flex" }}>
      <motion.span
        aria-hidden="true"
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: "9999px",
          background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
          pointerEvents: "none",
          filter: "blur(10px)",
        }}
        animate={{ scale: haloScale, opacity: haloOpacity }}
        transition={{ duration: 0.16, ease: MOTION_EASINGS.composed }}
      />
      <motion.span
        aria-hidden="true"
        style={{
          position: "absolute",
          inset: -4,
          borderRadius: "9999px",
          border: `2px solid ${color}`,
          pointerEvents: "none",
          opacity: 0.4,
        }}
        animate={{ scale: haloScale, opacity: haloOpacity * 0.6 }}
        transition={{ duration: 0.16, ease: MOTION_EASINGS.composed }}
      />
      <div style={{ position: "relative", zIndex: 1 }}>{children}</div>
    </div>
  );
}

export default Pulse;
