"use client";

import { motion } from "framer-motion";
import { useEffect, useMemo, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { useSoundCue, type CueEvent } from "@/lib/useSoundCue";
import {
  MOTION_DURATIONS_SEC,
  MOTION_EASINGS,
} from "@/lib/motion/tokens";

/**
 * Cinematic rare. Renders a full-bleed scene with:
 *   - Navy radial gradient fade-in over 480ms.
 *   - A bloom of gold particle points rising from center.
 *   - The composed children (typically a ShieldDraw + MotionText
 *     headline + Stagger summary block + MotionButton).
 *
 * Strictly gated on useMotion().milestones; if the gate is off, the
 * children render plain (no scene). Under reduceMotion the scene
 * renders instantly (no particles, no animation, but still composed).
 *
 * Fires a single sound cue on mount via useSoundCue. The cue
 * defaults to "day_complete" but can be overridden.
 */
interface MilestoneMomentProps {
  /** Trigger key. Re-mounting with a new trigger replays the scene. */
  trigger: string;
  /** Cue to fire on mount. Default "day_complete". */
  soundCue?: CueEvent;
  /** Suppress the mount cue when sound is owned elsewhere (e.g. the
   *  CelebrationDirector owns day_complete). Defaults to false. */
  muteCue?: boolean;
  children: ReactNode;
}

const PARTICLE_COUNT = 14;

export function MilestoneMoment({
  trigger,
  soundCue = "day_complete",
  muteCue = false,
  children,
}: MilestoneMomentProps) {
  const { reduceMotion, milestones, speed } = useMotion();
  const playCue = useSoundCue();

  useEffect(() => {
    if (!muteCue) playCue(soundCue, { volume: 0.6 });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [trigger]);

  // Deterministic particle positions seeded by trigger so re-renders
  // don't reshuffle. We do not need cryptographic randomness here.
  const particles = useMemo(() => {
    const seed = (trigger || "").split("").reduce((acc, c) => acc + c.charCodeAt(0), 0);
    const rand = (i: number) => {
      const x = Math.sin(seed + i * 12.9898) * 43758.5453;
      return x - Math.floor(x);
    };
    return Array.from({ length: PARTICLE_COUNT }, (_, i) => ({
      id: i,
      angle: rand(i) * Math.PI * 2,
      distance: 80 + rand(i + 100) * 180,
      delay: rand(i + 200) * 0.6,
      size: 4 + rand(i + 300) * 6,
    }));
  }, [trigger]);

  if (!milestones || reduceMotion) {
    // Static composition: render children with a soft ambient backdrop.
    return (
      <div className="relative isolate">
        <div
          aria-hidden="true"
          className="absolute inset-0 -z-10"
          style={{
            background:
              "radial-gradient(ellipse at 50% 30%, rgba(198,162,78,0.10) 0%, transparent 60%), linear-gradient(180deg, var(--color-page) 0%, var(--color-surface) 100%)",
          }}
        />
        {children}
      </div>
    );
  }

  const dimDuration = 0.48 / speed;
  const epicDuration = MOTION_DURATIONS_SEC.epic / speed;

  return (
    <div className="relative isolate">
      {/* Backdrop dim + ambient navy wash. Sits behind the scene. */}
      <motion.div
        aria-hidden="true"
        className="absolute inset-0 -z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: dimDuration, ease: MOTION_EASINGS.confident }}
        style={{
          background:
            "radial-gradient(ellipse at 50% 30%, rgba(198,162,78,0.18) 0%, transparent 55%), linear-gradient(180deg, rgba(15,27,45,0.06) 0%, rgba(15,27,45,0.10) 100%)",
        }}
      />

      {/* Particle bloom from center. Hidden behind content. */}
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-10 overflow-hidden pointer-events-none"
        style={{ borderRadius: "inherit" }}
      >
        {particles.map((p) => {
          const tx = Math.cos(p.angle) * p.distance;
          const ty = Math.sin(p.angle) * p.distance - 40;
          return (
            <motion.span
              key={p.id}
              style={{
                position: "absolute",
                left: "50%",
                top: "50%",
                width: p.size,
                height: p.size,
                marginLeft: -p.size / 2,
                marginTop: -p.size / 2,
                borderRadius: "9999px",
                background:
                  "radial-gradient(circle, rgba(198,162,78,0.85) 0%, rgba(198,162,78,0) 75%)",
              }}
              initial={{ opacity: 0, x: 0, y: 0, scale: 0.6 }}
              animate={{
                opacity: [0, 0.9, 0],
                x: tx,
                y: ty,
                scale: [0.6, 1, 0.9],
              }}
              transition={{
                duration: epicDuration,
                ease: MOTION_EASINGS.cinematic,
                delay: p.delay,
                times: [0, 0.4, 1],
              }}
            />
          );
        })}
      </div>

      {children}
    </div>
  );
}

export default MilestoneMoment;
