"use client";

import { useEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";

import { useCelebration } from "@/lib/celebration/CelebrationDirector";
import { useMotion } from "@/lib/motion";
import { usePersonalization } from "@/lib/PersonalizationProvider";

import { personaFromId } from "./personas";
import { useCompanionState } from "./state";

function clamp(v: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, v));
}

const GAZE_RADIUS_PX = 260;

/**
 * Mounts the active companion (resolved from profile.companion_voice) in
 * the live, stateful form: it reads the companion state machine, the
 * motion preferences, and tracks the cursor for eye gaze. Nova taps fire
 * a confetti burst through the shared celebration canvas.
 *
 * `position="centered"` overlays the companion full-screen (used during
 * the day-complete celebration).
 */
export function CompanionStage({
  size = 56,
  position = "inline",
}: {
  size?: number;
  position?: "inline" | "centered";
}) {
  const { profile } = usePersonalization();
  const { state, drowsy } = useCompanionState();
  const { speed, reduceMotion } = useMotion();
  const { tapBurst } = useCelebration();

  const Persona = personaFromId(profile.companion_voice);
  const isNova = profile.companion_voice === "default_playful";

  const wrapRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number | null>(null);
  const [gaze, setGaze] = useState({ x: 0, y: 0 });

  // Cursor gaze tracking, rAF-throttled, disabled under reduced-motion.
  useEffect(() => {
    if (reduceMotion) {
      setGaze({ x: 0, y: 0 });
      return;
    }
    const onMove = (e: MouseEvent) => {
      if (rafRef.current !== null) return;
      rafRef.current = window.requestAnimationFrame(() => {
        rafRef.current = null;
        const el = wrapRef.current;
        if (!el) return;
        const r = el.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        setGaze({
          x: clamp((e.clientX - cx) / GAZE_RADIUS_PX, -1, 1),
          y: clamp((e.clientY - cy) / GAZE_RADIUS_PX, -1, 1),
        });
      });
    };
    window.addEventListener("mousemove", onMove);
    return () => {
      window.removeEventListener("mousemove", onMove);
      if (rafRef.current !== null) window.cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    };
  }, [reduceMotion]);

  const onPointerDown = isNova
    ? (e: ReactPointerEvent<HTMLDivElement>) => tapBurst(e.clientX, e.clientY)
    : undefined;

  const companion = (
    <div
      ref={wrapRef}
      onPointerDown={onPointerDown}
      style={{
        width: size,
        height: size,
        display: "inline-block",
        lineHeight: 0,
        cursor: isNova ? "pointer" : undefined,
        pointerEvents: position === "centered" ? "none" : undefined,
      }}
    >
      <Persona
        state={state}
        size={size}
        gaze={gaze}
        speed={speed}
        reduceMotion={reduceMotion}
        drowsy={drowsy}
      />
    </div>
  );

  if (position === "centered") {
    return (
      <div className="fixed inset-0 z-[57] flex items-center justify-center pointer-events-none">
        {companion}
      </div>
    );
  }
  return companion;
}

export default CompanionStage;
