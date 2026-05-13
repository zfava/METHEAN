"use client";

import { useCallback, useEffect, useRef } from "react";

import { usePersonalization } from "@/lib/PersonalizationProvider";

export type CueEvent =
  | "activity_start"
  | "correct"
  | "hint_revealed"
  | "activity_complete"
  | "mastery_up"
  | "day_complete";

const CUE_EVENTS: readonly CueEvent[] = [
  "activity_start",
  "correct",
  "hint_revealed",
  "activity_complete",
  "mastery_up",
  "day_complete",
];

// When the user prefers reduced motion the routine cues drop out;
// only the two meaningful event cues still fire (mastery_up,
// day_complete). This keeps "I'm sensitive to repetitive cues"
// users from being pelted while still surfacing the rare ones that
// mark real progress.
const REDUCED_MOTION_EVENTS: Set<CueEvent> = new Set(["mastery_up", "day_complete"]);

// Minimum gap between any two cues. Prevents stack-ups when several
// state transitions land within the same frame (e.g., a correct
// answer that also completes the activity).
const MIN_GAP_MS = 200;

/**
 * Hook: returns a `play(event, opts?)` callback that fires the
 * matching audio cue for the active sound pack.
 *
 * Contract:
 * - Pack "off" or unset profile: no-op.
 * - Before the first user gesture: no-op. (Browsers reject
 *   programmatic playback until the user has tapped or pressed.)
 * - When prefers-reduced-motion is set: only mastery_up and
 *   day_complete play; everything else is suppressed.
 * - Two calls within MIN_GAP_MS: the later one is dropped.
 * - Missing audio file or play() rejection: silently no-op.
 *
 * Audio elements are preloaded on pack change so cue triggers
 * don't pay a network round trip.
 */
export function useSoundCue(): (event: CueEvent, opts?: { volume?: number }) => void {
  const { profile } = usePersonalization();
  const audioRefs = useRef<Map<CueEvent, HTMLAudioElement>>(new Map());
  const lastPlayedAtRef = useRef<number>(0);
  const gestureUnlockedRef = useRef<boolean>(false);
  const reducedMotionRef = useRef<boolean>(false);

  // Latch the first pointer or keyboard gesture so subsequent
  // .play() calls satisfy the browser autoplay policy.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const onGesture = () => {
      gestureUnlockedRef.current = true;
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

  // Track the reduced-motion preference. We read it inside the
  // play callback (not as a closed-over value at definition time)
  // so a mid-session change is honored.
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    reducedMotionRef.current = mq.matches;
    const handler = (e: MediaQueryListEvent) => {
      reducedMotionRef.current = e.matches;
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  // Preload all six cues whenever the pack changes. The "off"
  // pack ships nothing; the hook short-circuits before this map is
  // consulted.
  useEffect(() => {
    audioRefs.current.clear();
    const pack = profile.sound_pack;
    if (!pack || pack === "off") return;
    if (typeof Audio === "undefined") return;
    for (const event of CUE_EVENTS) {
      const audio = new Audio(`/sounds/${pack}/${event}.mp3`);
      audio.preload = "auto";
      audio.volume = 0.5;
      audioRefs.current.set(event, audio);
    }
  }, [profile.sound_pack]);

  return useCallback(
    (event: CueEvent, opts?: { volume?: number }) => {
      const pack = profile.sound_pack;
      if (!pack || pack === "off") return;
      if (!gestureUnlockedRef.current) return;
      if (reducedMotionRef.current && !REDUCED_MOTION_EVENTS.has(event)) return;
      const now = Date.now();
      if (now - lastPlayedAtRef.current < MIN_GAP_MS) return;
      const audio = audioRefs.current.get(event);
      if (!audio) return;
      try {
        audio.currentTime = 0;
        if (opts?.volume !== undefined) {
          audio.volume = Math.max(0, Math.min(1, opts.volume));
        }
        const result = audio.play();
        if (result && typeof result.then === "function") {
          result.catch(() => {
            // Autoplay rejection or device error. Silent no-op
            // is the right answer; cues are advisory.
          });
        }
        lastPlayedAtRef.current = now;
      } catch {
        // Same as above: never throw from a cue path.
      }
    },
    [profile.sound_pack],
  );
}
