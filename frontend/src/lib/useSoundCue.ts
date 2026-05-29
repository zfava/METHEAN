"use client";

import { useCallback, useEffect } from "react";

import { usePersonalization } from "@/lib/PersonalizationProvider";
import {
  audioConductor,
  type CueEvent,
  type PackTier,
  type VibeAmbientId,
} from "@/lib/audio/AudioConductor";

// Re-exported so existing callers keep importing the cue union from
// this module (e.g. MilestoneMoment imports `type CueEvent` here).
export type { CueEvent };

const VIBE_IDS: ReadonlySet<string> = new Set<VibeAmbientId>([
  "calm",
  "field",
  "orbit",
  "workshop",
  "studio",
  "bold",
]);

function toPackTier(pack: string | null | undefined): PackTier {
  if (pack === "full") return "full";
  if (pack === "soft") return "soft";
  // off, unset, or any unknown pack id -> silent, matching the prior
  // HTMLAudio behavior where a missing pack folder produced no sound.
  return "off";
}

function toVibeAmbientId(vibe: string | null | undefined): VibeAmbientId {
  return vibe && VIBE_IDS.has(vibe) ? (vibe as VibeAmbientId) : "calm";
}

/**
 * Hook: returns a `play(event, opts?)` callback that fires the matching
 * procedural cue through the AudioConductor (Tone.js).
 *
 * Contract (unchanged from the previous HTMLAudio implementation):
 * - Pack "off" or unset: no-op.
 * - Before the first user gesture: no-op (the conductor is not started
 *   until init() runs, which only happens on first gesture).
 * - prefers-reduced-motion: only mastery_up and day_complete play.
 * - Two calls within 200ms: the later one is dropped.
 * - Never throws from the cue path.
 *
 * The throttle and reduced-motion gating now live in the conductor;
 * this hook only wires React state (pack, vibe, reduced-motion, and the
 * first-gesture latch) into it.
 */
export function useSoundCue(): (event: CueEvent, opts?: { volume?: number }) => void {
  const { profile } = usePersonalization();

  // First-gesture latch. Calling init() synchronously inside the
  // gesture handler is required so Tone.start() runs within the
  // gesture call stack and the audio context actually unlocks.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const onGesture = () => {
      void audioConductor.init();
      window.removeEventListener("pointerdown", onGesture);
      window.removeEventListener("keydown", onGesture);
      window.removeEventListener("touchstart", onGesture);
    };
    window.addEventListener("pointerdown", onGesture, { once: true });
    window.addEventListener("keydown", onGesture, { once: true });
    window.addEventListener("touchstart", onGesture, { once: true });
    return () => {
      window.removeEventListener("pointerdown", onGesture);
      window.removeEventListener("keydown", onGesture);
      window.removeEventListener("touchstart", onGesture);
    };
  }, []);

  // Pack tier -> master volume scaling.
  useEffect(() => {
    audioConductor.setPackVolume(toPackTier(profile.sound_pack));
  }, [profile.sound_pack]);

  // Vibe -> ambient bed (crossfades inside the conductor).
  useEffect(() => {
    void audioConductor.setVibe(toVibeAmbientId(profile.vibe));
  }, [profile.vibe]);

  // Live reduced-motion preference.
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    audioConductor.setReducedMotion(mq.matches);
    const handler = (e: MediaQueryListEvent) => audioConductor.setReducedMotion(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  return useCallback((event: CueEvent, opts?: { volume?: number }) => {
    void audioConductor.playCue(event, opts);
  }, []);
}
