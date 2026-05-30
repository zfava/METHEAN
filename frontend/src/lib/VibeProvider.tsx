"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState, type ReactNode } from "react";

import { usePersonalization } from "@/lib/PersonalizationProvider";
import { CALM_VIBE_FALLBACK, type Vibe } from "@/lib/personalization-types";
import { worldFromVibe } from "@/lib/vibe/worlds";

/**
 * Wraps children in a div that applies the active vibe's CSS-variable
 * tokens and mounts the vibe's environmental world (procedural backdrop
 * + motif layer) behind the content. Switching vibes crossfades the
 * world over 300ms.
 *
 * `--font-weight-heading` is intentionally dropped from the inline token
 * bag so the per-vibe typography modifiers in globals.css ([data-vibe])
 * are authoritative (inline styles would otherwise shadow the CSS).
 *
 * Note on provider order: this provider must sit *inside* MotionProvider
 * so the backdrop/motif AmbientFloat + ParallaxOnScroll primitives read
 * the real reduced-motion / speed state rather than the default.
 */
export function VibeProvider({ children }: { children: ReactNode }) {
  const { profile, library } = usePersonalization();

  const resolved: Vibe =
    library?.vibes.find((v) => v.id === profile.vibe) ?? CALM_VIBE_FALLBACK;

  const prefersReducedMotion = usePrefersReducedMotion();
  const motifDensity = useMotifDensity(!prefersReducedMotion);

  // Apply the token bag minus --font-weight-heading (see note above).
  const tokenStyle: Record<string, string> = {};
  for (const [k, v] of Object.entries(resolved.tokens)) {
    if (k === "--font-weight-heading") continue;
    tokenStyle[k] = v;
  }
  const style: React.CSSProperties = {
    ...(tokenStyle as React.CSSProperties),
    minHeight: "100dvh",
  };
  if (!prefersReducedMotion) {
    style.transition = "background-color 240ms ease, color 240ms ease";
  }

  const { Backdrop, Motifs } = worldFromVibe(profile.vibe);

  return (
    <div data-vibe={profile.vibe} style={style}>
      <AnimatePresence mode="wait">
        <motion.div
          key={profile.vibe}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
        >
          <Backdrop />
          <Motifs density={motifDensity} />
        </motion.div>
      </AnimatePresence>
      {children}
    </div>
  );
}

/**
 * Rolling-window FPS guard. If the average frame rate drops below 50fps
 * for 3 consecutive 30-frame samples, halve the motif count once. Skipped
 * entirely when animations are off (reduced-motion), since there is then
 * nothing to drop frames.
 */
function useMotifDensity(enabled: boolean): number {
  const [density, setDensity] = useState(1);
  useEffect(() => {
    if (!enabled || typeof window === "undefined") {
      setDensity(1);
      return;
    }
    let raf = 0;
    let last = 0;
    let frames = 0;
    let lowStreak = 0;
    let stopped = false;
    const buf: number[] = [];
    const loop = (t: number) => {
      if (stopped) return;
      if (last) {
        const dt = t - last;
        if (dt > 0) {
          buf.push(1000 / dt);
          if (buf.length > 30) buf.shift();
          frames++;
          if (frames % 30 === 0 && buf.length >= 30) {
            const avg = buf.reduce((a, b) => a + b, 0) / buf.length;
            if (avg < 50) {
              lowStreak++;
              if (lowStreak >= 3) {
                setDensity(0.5);
                stopped = true;
                return;
              }
            } else {
              lowStreak = 0;
            }
          }
        }
      }
      last = t;
      raf = window.requestAnimationFrame(loop);
    };
    raf = window.requestAnimationFrame(loop);
    return () => {
      stopped = true;
      window.cancelAnimationFrame(raf);
    };
  }, [enabled]);
  return density;
}

/**
 * Tracks the `prefers-reduced-motion: reduce` media query. Returns
 * false during SSR (no `window`) so the transition isn't omitted on
 * first paint when the client would actually allow it; the effect
 * corrects the value on hydration.
 */
function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState<boolean>(false);
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mql.matches);
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, []);
  return reduced;
}
