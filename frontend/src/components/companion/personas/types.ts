import type { CompanionState } from "../state";

export interface Gaze {
  /** Normalized -1..1 horizontal gaze offset. */
  x: number;
  /** Normalized -1..1 vertical gaze offset. */
  y: number;
}

/**
 * Every persona is a self-contained procedural SVG that takes these
 * props. It deliberately does NOT read MotionContext so it renders
 * correctly inside CompanionStage (stateful), inside the CompanionAvatar
 * static wrapper, and outside the /child provider tree (onboarding,
 * parent governance previews).
 */
export interface PersonaProps {
  state: CompanionState;
  size?: number;
  gaze?: Gaze;
  /** Motion speed multiplier (1 = nominal). Higher = faster breath. */
  speed?: number;
  reduceMotion?: boolean;
  /** ~30s idle: eyes go half-closed. */
  drowsy?: boolean;
}

export interface MouthSet {
  neutral: string;
  smile: string;
  cheer: string;
  frown: string;
  sleep: string;
}
