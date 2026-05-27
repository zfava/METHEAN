"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { useChild } from "@/lib/ChildContext";
import { usePersonalization } from "@/lib/PersonalizationProvider";

/**
 * The motion contract for the child surface.
 *
 * Precedence (each step's match wins over earlier ones):
 *   1. OS prefers-reduced-motion -> reserved + ambient/milestones off.
 *   2. Child age band (derived from grade_level) -> default intensity.
 *   3. Vibe.tokens motion_intensity / motion_speed -> if present.
 *   4. Parent governance motion_preference (calm/standard/lively).
 *
 * Consumers call useMotion() inside every primitive. Primitives must
 * also branch on reduceMotion to render the final state instantly.
 */

export type MotionIntensity = "ambient" | "standard" | "reserved";

export type AgeBand = "early" | "middle" | "older" | "adolescent";

export type MotionPreference = "calm" | "standard" | "lively";

export interface MotionState {
  intensity: MotionIntensity;
  /** Multiplier on base durations (0.7..1.3). */
  speed: number;
  /** Drives shadow/parallax weight. 0..1. */
  depth: number;
  /** Background drift and breathing on/off. */
  ambient: boolean;
  /** Big cinematic moments allowed. */
  milestones: boolean;
  /** Hard switch: when true every primitive degrades to instant. */
  reduceMotion: boolean;
  /** The age band actually applied, for debug and screen-level hints. */
  ageBand: AgeBand;
}

const DEFAULT_STATE: MotionState = {
  intensity: "standard",
  speed: 1.0,
  depth: 0.7,
  ambient: true,
  milestones: true,
  reduceMotion: false,
  ageBand: "middle",
};

const MotionStateContext = createContext<MotionState>(DEFAULT_STATE);

/**
 * Map K/1/2/3/4/.../12 grade strings to one of our four age bands.
 * The grade_level field is free-form on the API (the seed produces
 * strings like "3", "5", "PreK"), so be tolerant of variants.
 */
export function ageBandFromGrade(grade: string | null | undefined): AgeBand {
  if (!grade) return "middle";
  const trimmed = grade.trim().toLowerCase();
  if (trimmed === "k" || trimmed === "pk" || trimmed === "prek" || trimmed === "kindergarten") {
    return "early";
  }
  const match = trimmed.match(/^(\d{1,2})/);
  if (!match) return "middle";
  const n = parseInt(match[1], 10);
  if (Number.isNaN(n)) return "middle";
  if (n <= 3) return "early";
  if (n <= 6) return "middle";
  if (n <= 9) return "older";
  return "adolescent";
}

function ageBandDefaults(band: AgeBand): MotionState {
  switch (band) {
    case "early":
      return {
        intensity: "ambient",
        speed: 0.9,
        depth: 0.9,
        ambient: true,
        milestones: true,
        reduceMotion: false,
        ageBand: band,
      };
    case "middle":
      return {
        intensity: "standard",
        speed: 1.0,
        depth: 0.7,
        ambient: true,
        milestones: true,
        reduceMotion: false,
        ageBand: band,
      };
    case "older":
      return {
        intensity: "reserved",
        speed: 1.1,
        depth: 0.5,
        ambient: false,
        milestones: true,
        reduceMotion: false,
        ageBand: band,
      };
    case "adolescent":
      return {
        intensity: "reserved",
        speed: 1.15,
        depth: 0.4,
        ambient: false,
        milestones: true,
        reduceMotion: false,
        ageBand: band,
      };
  }
}

function applyVibeTokens(
  state: MotionState,
  tokens: Record<string, string> | undefined,
): MotionState {
  if (!tokens) return state;
  const next = { ...state };
  const tokenIntensity = tokens["motion_intensity"];
  if (
    tokenIntensity === "ambient" ||
    tokenIntensity === "standard" ||
    tokenIntensity === "reserved"
  ) {
    next.intensity = tokenIntensity;
    if (tokenIntensity === "ambient") next.ambient = true;
    if (tokenIntensity === "reserved") next.ambient = false;
  }
  const tokenSpeed = tokens["motion_speed"];
  if (tokenSpeed) {
    const parsed = parseFloat(tokenSpeed);
    if (!Number.isNaN(parsed) && parsed > 0.4 && parsed < 2.0) {
      next.speed = parsed;
    }
  }
  return next;
}

function applyMotionPreference(
  state: MotionState,
  preference: MotionPreference | undefined,
): MotionState {
  if (!preference) return state;
  if (preference === "calm") {
    // calm: tighter, lower-amplitude, ambient off, milestones still
    // allowed but the primitives will read intensity=reserved to keep
    // them shorter.
    return { ...state, intensity: "reserved", ambient: false };
  }
  if (preference === "lively") {
    return { ...state, intensity: "ambient", ambient: true };
  }
  return state; // "standard" -> pass through age-band defaults
}

function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);
  return reduced;
}

interface MotionPreferenceShape {
  motion_preference?: MotionPreference;
}

export function MotionProvider({ children }: { children: ReactNode }) {
  const reduceMotion = usePrefersReducedMotion();
  const { selectedChild } = useChild();
  const { profile, library } = usePersonalization();

  const state = useMemo<MotionState>(() => {
    if (reduceMotion) {
      return {
        intensity: "reserved",
        speed: 1.0,
        depth: 0,
        ambient: false,
        milestones: false,
        reduceMotion: true,
        ageBand: ageBandFromGrade(selectedChild?.grade_level),
      };
    }
    const band = ageBandFromGrade(selectedChild?.grade_level);
    let next = ageBandDefaults(band);

    // Vibe.tokens may carry optional motion hints. Applied after
    // age-band so a vibe explicitly designed for a calm intensity can
    // dial things down even for younger kids.
    const vibeTokens = library?.vibes.find((v) => v.id === profile.vibe)?.tokens;
    next = applyVibeTokens(next, vibeTokens);

    // Parent governance is the highest-precedence non-OS signal.
    // motion_preference now lives on ChildPersonalization directly.
    next = applyMotionPreference(next, profile.motion_preference);

    return next;
  }, [reduceMotion, selectedChild?.grade_level, profile, library]);

  return <MotionStateContext.Provider value={state}>{children}</MotionStateContext.Provider>;
}

export function useMotion(): MotionState {
  return useContext(MotionStateContext);
}
