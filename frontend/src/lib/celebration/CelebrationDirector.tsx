"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";

import { audioConductor, type CueEvent } from "@/lib/audio/AudioConductor";
import { Scale, useMotion } from "@/lib/motion";
import { usePersonalization } from "@/lib/PersonalizationProvider";

import { ParticleEngine } from "./ParticleEngine";
import {
  buildParticles,
  buildStreak100Explosion,
  buildStreak100Fireflies,
  buildStreak100Rocket,
  buildTapBurst,
  type CelebrationTier,
  type ProfileContext,
  type VibeId,
} from "./profiles";

export interface CelebrationRequest {
  tier: CelebrationTier;
  /** Centered display text, e.g. "Mastered!" or the kid's name. */
  microcopy?: string;
  /** Override the default microcopy dwell (ms). */
  durationMs?: number;
}

interface CelebrationContextValue {
  trigger: (req: CelebrationRequest) => void;
  /** Small confetti burst at a screen point (no sound). Used by Nova's
   *  tap handler; routes through the same single canvas. */
  tapBurst: (x: number, y: number) => void;
}

const CelebrationContext = createContext<CelebrationContextValue>({
  trigger: () => {},
  tapBurst: () => {},
});

const VIBE_IDS: ReadonlySet<string> = new Set<VibeId>([
  "calm",
  "field",
  "orbit",
  "workshop",
  "studio",
  "bold",
]);

function toVibeId(vibe: string | null | undefined): VibeId {
  return vibe && VIBE_IDS.has(vibe) ? (vibe as VibeId) : "calm";
}

function cueForTier(tier: CelebrationTier): CueEvent {
  switch (tier) {
    case "activity_complete":
      return "activity_complete";
    case "mastery_up":
      return "mastery_up";
    case "day_complete":
      return "day_complete";
    // No dedicated streak cue yet; reuse the celebratory mastery cue.
    case "streak_7":
    case "streak_30":
    case "streak_100":
      return "mastery_up";
  }
}

// Cue loudness per tier, matching the prior direct-call volumes.
function volumeForTier(tier: CelebrationTier): number | undefined {
  switch (tier) {
    case "activity_complete":
      return undefined; // default inherent loudness
    default:
      return 0.6;
  }
}

const DEFAULT_MICROCOPY_MS = 1400;

// Small seeded PRNG (mulberry32) so a celebration's randomness is
// deterministic per trigger and testable.
function mulberry32(seed: number): () => number {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function CelebrationProvider({ children }: { children: ReactNode }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const engineRef = useRef<ParticleEngine | null>(null);
  const timersRef = useRef<Set<ReturnType<typeof setTimeout>>>(new Set());
  const seedRef = useRef(0);

  const { profile } = usePersonalization();
  const { reduceMotion } = useMotion();

  // Read live vibe / reduced-motion through refs so trigger() stays a
  // stable callback (it is used in effect dependency arrays).
  const vibeRef = useRef<VibeId>(toVibeId(profile.vibe));
  const reducedRef = useRef<boolean>(reduceMotion);
  useEffect(() => {
    vibeRef.current = toVibeId(profile.vibe);
  }, [profile.vibe]);
  useEffect(() => {
    reducedRef.current = reduceMotion;
  }, [reduceMotion]);

  const [microcopy, setMicrocopy] = useState<{ text: string; key: number } | null>(null);
  const microcopyTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const engine = new ParticleEngine(canvasRef.current);
    engineRef.current = engine;
    const timers = timersRef.current;
    return () => {
      engine.destroy();
      engineRef.current = null;
      for (const id of timers) clearTimeout(id);
      timers.clear();
      if (microcopyTimerRef.current) clearTimeout(microcopyTimerRef.current);
    };
  }, []);

  const profileCtx = useCallback(
    (engine: ParticleEngine, tier: CelebrationTier, rng: () => number): ProfileContext => ({
      tier,
      vibe: vibeRef.current,
      reducedMotion: reducedRef.current,
      centerX: engine.width / 2,
      centerY: engine.height / 2,
      canvasWidth: engine.width,
      canvasHeight: engine.height,
      rng,
    }),
    [],
  );

  const schedule = useCallback((fn: () => void, ms: number) => {
    const id = setTimeout(() => {
      timersRef.current.delete(id);
      fn();
    }, ms);
    timersRef.current.add(id);
  }, []);

  const trigger = useCallback(
    (req: CelebrationRequest) => {
      const { tier } = req;

      // 1. Sound cue (director is the single owner of celebration sound).
      void audioConductor.playCue(cueForTier(tier), { volume: volumeForTier(tier) });

      // 2. Companion-state signal for Prompt 4 (no consumer yet).
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("metheanCelebration", { detail: { tier } }));
      }

      // 3. Particles.
      const engine = engineRef.current;
      if (engine) {
        const seed = (Date.now() ^ (seedRef.current++ << 16)) >>> 0;
        const rng = mulberry32(seed);
        const ctx = profileCtx(engine, tier, rng);
        engine.emit(buildParticles(ctx));

        if (tier === "streak_100") {
          // Wave 2: a rocket that climbs and bursts at its apex.
          schedule(() => {
            const e = engineRef.current;
            if (e) e.emit(buildStreak100Rocket(profileCtx(e, tier, rng)));
          }, 400);
          schedule(() => {
            const e = engineRef.current;
            if (e) {
              const apexX = e.width / 2;
              const apexY = e.height * 0.3;
              e.emit(buildStreak100Explosion(profileCtx(e, tier, rng), apexX, apexY));
            }
          }, 1100);
          // Wave 3: ambient fireflies.
          schedule(() => {
            const e = engineRef.current;
            if (e) e.emit(buildStreak100Fireflies(profileCtx(e, tier, rng)));
          }, 900);
        }
      }

      // 4. Microcopy overlay (auto-dismisses).
      if (req.microcopy) {
        setMicrocopy({ text: req.microcopy, key: seedRef.current });
        if (microcopyTimerRef.current) clearTimeout(microcopyTimerRef.current);
        microcopyTimerRef.current = setTimeout(
          () => setMicrocopy(null),
          req.durationMs ?? DEFAULT_MICROCOPY_MS,
        );
      }
    },
    [profileCtx, schedule],
  );

  const tapBurst = useCallback((x: number, y: number) => {
    const engine = engineRef.current;
    if (!engine) return;
    const seed = (Date.now() ^ (seedRef.current++ << 16)) >>> 0;
    engine.emit(buildTapBurst(x, y, mulberry32(seed), reducedRef.current));
  }, []);

  return (
    <CelebrationContext.Provider value={{ trigger, tapBurst }}>
      {children}
      <canvas
        ref={canvasRef}
        aria-hidden="true"
        className="fixed inset-0 z-[55] h-full w-full"
        style={{ pointerEvents: "none" }}
      />
      <AnimatePresence>
        {microcopy && (
          <motion.div
            key={microcopy.key}
            aria-hidden="true"
            className="fixed inset-0 z-[56] flex items-center justify-center"
            style={{ pointerEvents: "none" }}
            initial={reduceMotion ? false : { opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, transition: { duration: 0.3 } }}
          >
            <Scale from={0.85}>
              <p className="type-display-md text-(--color-text) text-center px-6 drop-shadow-sm">
                {microcopy.text}
              </p>
            </Scale>
          </motion.div>
        )}
      </AnimatePresence>
    </CelebrationContext.Provider>
  );
}

export function useCelebration(): CelebrationContextValue {
  return useContext(CelebrationContext);
}
