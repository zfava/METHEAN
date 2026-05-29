import * as Tone from "tone";

import {
  buildActivityStartCue,
  buildCorrectCue,
  buildHintRevealedCue,
  buildActivityCompleteCue,
  buildMasteryUpCue,
  buildDayCompleteCue,
  type CueContext,
} from "@/lib/audio/cues";
import { buildAmbientBed, type AmbientBed } from "@/lib/audio/ambient";

export type CueEvent =
  | "activity_start"
  | "correct"
  | "hint_revealed"
  | "activity_complete"
  | "mastery_up"
  | "day_complete";

export type VibeAmbientId = "calm" | "field" | "orbit" | "workshop" | "studio" | "bold";

export type PackTier = "off" | "soft" | "full";

/** Routine cues drop out under reduced-motion; only these survive. */
const REDUCED_MOTION_EVENTS: ReadonlySet<CueEvent> = new Set(["mastery_up", "day_complete"]);

/** Minimum gap between any two cues (ms). */
const MIN_GAP_MS = 200;

/** Volume tier -> master linear gain. off=0, soft=0.5, full=1.0. */
const TIER_GAIN: Record<PackTier, number> = { off: 0, soft: 0.5, full: 1.0 };

const CUE_FACTORIES: Record<CueEvent, (ctx: CueContext) => () => void> = {
  activity_start: buildActivityStartCue,
  correct: buildCorrectCue,
  hint_revealed: buildHintRevealedCue,
  activity_complete: buildActivityCompleteCue,
  mastery_up: buildMasteryUpCue,
  day_complete: buildDayCompleteCue,
};

/**
 * Single owner of the Tone.js audio context for the kid surface.
 *
 * Lifecycle:
 *  - `init()` must be invoked from a user-gesture call stack (it calls
 *    Tone.start() synchronously before its first await), and is
 *    idempotent.
 *  - Cues route through a master gain that carries the pack tier.
 *  - The active ambient bed routes through an ambient gain (used for
 *    voice ducking) into the same master.
 *  - Vibe changes crossfade beds: the old bed fades out over 400ms
 *    while the new bed fades in over 600ms, with no silence between.
 */
class AudioConductor {
  private started = false;
  private initPromise: Promise<void> | null = null;

  private masterGain: Tone.Gain | null = null;
  private ambientGain: Tone.Gain | null = null;

  private currentBed: AmbientBed | null = null;
  private currentVibe: VibeAmbientId | null = null;
  private pendingVibe: VibeAmbientId | null = null;

  private packVolume: PackTier = "soft";
  private reducedMotion = false;
  private duckCount = 0;
  private lastCueAt = 0;

  /** Idempotent. Call from inside a user-gesture handler. */
  async init(): Promise<void> {
    if (this.started) return;
    if (this.initPromise) return this.initPromise;
    this.initPromise = (async () => {
      // Tone.start() runs here, synchronously before any await above
      // resolves, so it sits inside the gesture stack that called init.
      await Tone.start();
      this.masterGain = new Tone.Gain(TIER_GAIN[this.packVolume]).toDestination();
      this.ambientGain = new Tone.Gain(1).connect(this.masterGain);
      this.started = true;
      if (this.pendingVibe) {
        const v = this.pendingVibe;
        this.pendingVibe = null;
        void this.setVibe(v);
      }
    })();
    return this.initPromise;
  }

  setPackVolume(pack: PackTier): void {
    this.packVolume = pack;
    if (this.masterGain) {
      this.masterGain.gain.rampTo(TIER_GAIN[pack], 0.1);
    }
  }

  setReducedMotion(reduced: boolean): void {
    this.reducedMotion = reduced;
  }

  async setVibe(vibe: VibeAmbientId): Promise<void> {
    if (!this.started || !this.ambientGain) {
      this.pendingVibe = vibe;
      return;
    }
    if (this.currentVibe === vibe) return;
    this.currentVibe = vibe;

    const old = this.currentBed;
    if (old) {
      void old.stop(400).then(() => old.dispose());
    }
    const bed = buildAmbientBed(vibe, this.ambientGain);
    this.currentBed = bed;
    await bed.start();
  }

  async playCue(event: CueEvent, opts?: { volume?: number }): Promise<void> {
    if (!this.started || !this.masterGain) return;
    if (TIER_GAIN[this.packVolume] === 0) return;
    if (this.reducedMotion && !REDUCED_MOTION_EVENTS.has(event)) return;

    const now = Date.now();
    if (now - this.lastCueAt < MIN_GAP_MS) return;
    this.lastCueAt = now;

    const volume = Math.max(0, Math.min(1, opts?.volume ?? 1));
    const play = CUE_FACTORIES[event]({ master: this.masterGain, volume });
    play();
  }

  /**
   * Audition a cue at a specific pack tier, independent of the saved
   * profile pack and the reduced-motion gate. Used by the sound-pack
   * pickers' "Hear sample" buttons. The triggering tap is the gesture
   * that unlocks audio, so init() is awaited here. Routes straight to
   * the destination so the current pack's master gain (which may be 0
   * when the saved pack is "off") does not silence the preview.
   */
  async previewCue(event: CueEvent, tier: PackTier): Promise<void> {
    if (tier === "off") return;
    await this.init();
    const ctx: CueContext = {
      master: Tone.getDestination(),
      volume: TIER_GAIN[tier],
    };
    CUE_FACTORIES[event](ctx)();
  }

  /** Ramp ambient down under tutor voice. Refcounted across callers. */
  duckAmbient(): void {
    this.duckCount += 1;
    if (this.duckCount === 1 && this.ambientGain) {
      this.ambientGain.gain.rampTo(0.25, 0.3);
    }
  }

  /** Release one duck. Restores when the last speaker stops. */
  restoreAmbient(): void {
    this.duckCount = Math.max(0, this.duckCount - 1);
    if (this.duckCount === 0 && this.ambientGain) {
      this.ambientGain.gain.rampTo(1, 0.5);
    }
  }

  /** Dispose everything. Used on dev hot-reload. */
  destroy(): void {
    if (this.currentBed) {
      this.currentBed.dispose();
      this.currentBed = null;
    }
    try {
      this.ambientGain?.dispose();
      this.masterGain?.dispose();
    } catch {
      // already disposed
    }
    this.ambientGain = null;
    this.masterGain = null;
    this.started = false;
    this.initPromise = null;
    this.currentVibe = null;
    this.duckCount = 0;
  }
}

export const audioConductor = new AudioConductor();
