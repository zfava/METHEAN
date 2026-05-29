import * as Tone from "tone";

import type { VibeAmbientId } from "@/lib/audio/AudioConductor";

/**
 * Per-vibe ambient beds, composed in Tone.js. Each bed is a
 * continuously evolving texture: drones run as uninterrupted
 * oscillators (no loop boundary, so no audible repeat click) and
 * sparse events are fired by a self-rescheduling randomized timer.
 *
 * A bed exposes start/stop/dispose. `start` fades the bed in over
 * 600ms; `stop(ms)` fades it out over `ms` for crossfades. The shared
 * ambient gain node (owned by the conductor, used for voice ducking)
 * sits downstream of every bed's own output gain.
 */

export interface AmbientBed {
  start(): Promise<void>;
  stop(rampMs: number): Promise<void>;
  dispose(): void;
}

const FADE_IN_S = 0.6;

/** Self-rescheduling randomized-interval event scheduler. */
function makeScheduler() {
  let timer: ReturnType<typeof setTimeout> | null = null;
  let stopped = false;
  function schedule(minS: number, maxS: number, fn: () => void) {
    const delay = (minS + Math.random() * (maxS - minS)) * 1000;
    timer = setTimeout(() => {
      if (stopped) return;
      try {
        fn();
      } catch {
        // advisory; never throw from the ambient path.
      }
      schedule(minS, maxS, fn);
    }, delay);
  }
  return {
    start(minS: number, maxS: number, fn: () => void) {
      schedule(minS, maxS, fn);
    },
    stop() {
      stopped = true;
      if (timer) clearTimeout(timer);
    },
  };
}

/** Common bed scaffold: an output gain plus standard lifecycle. */
function makeBed(
  ambientNode: Tone.Gain,
  build: (out: Tone.Gain) => { nodes: Array<{ dispose: () => void }>; schedulers: ReturnType<typeof makeScheduler>[] },
): AmbientBed {
  const out = new Tone.Gain(0).connect(ambientNode);
  const { nodes, schedulers } = build(out);
  return {
    async start() {
      out.gain.cancelScheduledValues(Tone.now());
      out.gain.rampTo(1, FADE_IN_S);
    },
    async stop(rampMs: number) {
      for (const s of schedulers) s.stop();
      out.gain.rampTo(0, rampMs / 1000);
      await new Promise((r) => setTimeout(r, rampMs + 50));
    },
    dispose() {
      for (const s of schedulers) s.stop();
      for (const n of nodes) {
        try {
          n.dispose();
        } catch {
          // already disposed
        }
      }
      try {
        out.dispose();
      } catch {
        // already disposed
      }
    },
  };
}

const PENTATONIC_C = ["C5", "D5", "E5", "G5", "A5", "C6", "D6", "E6", "G6", "A6", "C7", "D7", "E7", "G7", "A7"];
const E_MINOR_PENT = ["E5", "G5", "A5", "B5", "D6"];
const C_MAJOR_4_5 = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5"];

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

/**
 * calm: a C3 + G3 perfect-fifth sine drone under slow-LFO lowpass,
 * with distant pentatonic wind-chimes every 12-30s.
 */
export function buildCalmAmbient(ambientNode: Tone.Gain): AmbientBed {
  return makeBed(ambientNode, (out) => {
    const filter = new Tone.Filter(1500, "lowpass").connect(out);
    const lfo = new Tone.LFO({ frequency: 0.05, min: 1000, max: 2000 }).start();
    lfo.connect(filter.frequency);
    const droneA = new Tone.Oscillator({ frequency: "C3", type: "sine", volume: -28 }).connect(filter).start();
    const droneB = new Tone.Oscillator({ frequency: "G3", type: "sine", volume: -28 }).connect(filter).start();

    const chimeGain = new Tone.Gain(Tone.dbToGain(-20)).connect(out);
    const reverb = new Tone.Reverb({ decay: 3, wet: 0.5 }).connect(chimeGain);
    const delay = new Tone.FeedbackDelay({ delayTime: 0.28, feedback: 0.3, wet: 0.4 }).connect(reverb);
    const chime = new Tone.FMSynth({
      harmonicity: 3.01,
      modulationIndex: 6,
      oscillator: { type: "sine" },
      envelope: { attack: 0.002, decay: 0.4, sustain: 0.0, release: 0.4 },
      modulation: { type: "sine" },
      modulationEnvelope: { attack: 0.002, decay: 0.3, sustain: 0.0, release: 0.2 },
    }).connect(delay);

    const sched = makeScheduler();
    sched.start(12, 30, () => chime.triggerAttackRelease(pick(PENTATONIC_C), 0.3, Tone.now()));

    return { nodes: [filter, lfo, droneA, droneB, chime, delay, reverb, chimeGain], schedulers: [sched] };
  });
}

/**
 * field: a warm detuned F2 triangle drone with a low pink-noise
 * grass-rustle bed, and FM birdsong chirps every 15-45s.
 */
export function buildFieldAmbient(ambientNode: Tone.Gain): AmbientBed {
  return makeBed(ambientNode, (out) => {
    const droneA = new Tone.Oscillator({ frequency: "F2", type: "triangle", volume: -30, detune: -5 }).connect(out).start();
    const droneB = new Tone.Oscillator({ frequency: "F2", type: "triangle", volume: -30, detune: 5 }).connect(out).start();

    const rustleFilter = new Tone.Filter(900, "lowpass").connect(out);
    const rustle = new Tone.Noise({ type: "pink", volume: -36 }).connect(rustleFilter).start();

    const birdFilter = new Tone.Filter(5000, "lowpass").connect(new Tone.Gain(Tone.dbToGain(-22)).connect(out));
    const bird = new Tone.FMSynth({
      harmonicity: 2,
      modulationIndex: 3,
      oscillator: { type: "sine" },
      envelope: { attack: 0.005, decay: 0.05, sustain: 0.0, release: 0.03 },
      modulation: { type: "sine" },
      modulationEnvelope: { attack: 0.005, decay: 0.04, sustain: 0.0, release: 0.02 },
    }).connect(birdFilter);

    const sched = makeScheduler();
    sched.start(15, 45, () => {
      const chirps = 2 + Math.floor(Math.random() * 3); // 2-4
      let t = Tone.now();
      for (let i = 0; i < chirps; i++) {
        bird.triggerAttack(2000, t);
        bird.frequency.exponentialRampToValueAtTime(4000, t + 0.06);
        bird.frequency.exponentialRampToValueAtTime(3500, t + 0.08);
        bird.triggerRelease(t + 0.08);
        t += 0.06 + Math.random() * 0.09; // 60-150ms apart
      }
    });

    return { nodes: [droneA, droneB, rustle, rustleFilter, bird, birdFilter], schedulers: [sched] };
  });
}

/**
 * orbit: a sweeping filtered-saw E2 + B2 pad with a bitcrushed digital
 * blip in E-minor pentatonic every 8-20s.
 */
export function buildOrbitAmbient(ambientNode: Tone.Gain): AmbientBed {
  return makeBed(ambientNode, (out) => {
    const filter = new Tone.Filter(1400, "lowpass").connect(out);
    const lfo = new Tone.LFO({ frequency: 0.03, min: 400, max: 2400 }).start();
    lfo.connect(filter.frequency);
    const padA = new Tone.Oscillator({ frequency: "E2", type: "sawtooth", volume: -28 }).connect(filter).start();
    const padB = new Tone.Oscillator({ frequency: "B2", type: "sawtooth", volume: -28 }).connect(filter).start();

    const crush = new Tone.BitCrusher(8).connect(new Tone.Gain(Tone.dbToGain(-24)).connect(out));
    const blip = new Tone.Synth({
      oscillator: { type: "sine" },
      envelope: { attack: 0.002, decay: 0.04, sustain: 0.0, release: 0.02 },
    }).connect(crush);

    const sched = makeScheduler();
    sched.start(8, 20, () => blip.triggerAttackRelease(pick(E_MINOR_PENT), 0.04, Tone.now()));

    return { nodes: [filter, lfo, padA, padB, blip, crush], schedulers: [sched] };
  });
}

/**
 * workshop: a bandpassed brown-noise room bed with a low C2 hum and
 * soft wood-knocks every 20-50s.
 */
export function buildWorkshopAmbient(ambientNode: Tone.Gain): AmbientBed {
  return makeBed(ambientNode, (out) => {
    const roomFilter = new Tone.Filter({ type: "bandpass", frequency: 400, Q: 1 }).connect(
      new Tone.Gain(Tone.dbToGain(-28)).connect(out),
    );
    const room = new Tone.Noise({ type: "brown" }).connect(roomFilter).start();
    const hum = new Tone.Oscillator({ frequency: "C2", type: "sine", volume: -34 }).connect(out).start();

    const knockGain = new Tone.Gain(Tone.dbToGain(-22)).connect(out);
    const knock = new Tone.MembraneSynth({
      pitchDecay: 0.02,
      octaves: 2,
      envelope: { attack: 0.001, decay: 0.15, sustain: 0.0, release: 0.1 },
    }).connect(knockGain);
    const click = new Tone.NoiseSynth({
      noise: { type: "white" },
      envelope: { attack: 0.001, decay: 0.03, sustain: 0.0, release: 0.02 },
    }).connect(new Tone.Filter(1200, "bandpass").connect(knockGain));

    const sched = makeScheduler();
    sched.start(20, 50, () => {
      const now = Tone.now();
      knock.triggerAttackRelease("C2", 0.1, now);
      click.triggerAttackRelease(0.03, now);
    });

    return { nodes: [room, roomFilter, hum, knock, click, knockGain], schedulers: [sched] };
  });
}

/**
 * studio: no drone; intimate nylon-string plucks in C major every
 * 10-25s through a short room reverb. Silence between is part of it.
 */
export function buildStudioAmbient(ambientNode: Tone.Gain): AmbientBed {
  return makeBed(ambientNode, (out) => {
    const reverb = new Tone.Reverb({ decay: 0.8, wet: 0.3 }).connect(
      new Tone.Gain(Tone.dbToGain(-22)).connect(out),
    );
    const pluck = new Tone.FMSynth({
      harmonicity: 3,
      modulationIndex: 5,
      oscillator: { type: "sine" },
      envelope: { attack: 0.003, decay: 0.4, sustain: 0.0, release: 0.3 },
      modulation: { type: "triangle" },
      modulationEnvelope: { attack: 0.002, decay: 0.2, sustain: 0.0, release: 0.1 },
    }).connect(reverb);

    const sched = makeScheduler();
    sched.start(10, 25, () => pluck.triggerAttackRelease(pick(C_MAJOR_4_5), 0.5, Tone.now()));

    return { nodes: [pluck, reverb], schedulers: [sched] };
  });
}

/**
 * bold: a muted ~50Hz kick pulse at 80bpm (slightly humanized off the
 * grid) over a C1 sine sub, with a high-shelf cut to stay warm.
 */
export function buildBoldAmbient(ambientNode: Tone.Gain): AmbientBed {
  return makeBed(ambientNode, (out) => {
    const shelf = new Tone.Filter({ type: "highshelf", frequency: 4000, gain: -6 }).connect(out);
    const sub = new Tone.Oscillator({ frequency: "C1", type: "sine", volume: -28 }).connect(shelf).start();

    const kickGain = new Tone.Gain(Tone.dbToGain(-24)).connect(shelf);
    const kick = new Tone.MembraneSynth({
      pitchDecay: 0.03,
      octaves: 4,
      envelope: { attack: 0.001, decay: 0.2, sustain: 0.0, release: 0.1 },
    }).connect(kickGain);

    const sched = makeScheduler();
    const BEAT_S = 60 / 80; // 0.75s
    const beat = () => {
      const humanize = (Math.random() * 0.01 - 0.005); // +/-5ms
      kick.triggerAttackRelease(50, 0.12, Tone.now() + Math.max(0, humanize));
    };
    // Fixed-tempo pulse with small humanize; reschedule at the beat.
    sched.start(BEAT_S, BEAT_S, beat);

    return { nodes: [shelf, sub, kick, kickGain], schedulers: [sched] };
  });
}

const BUILDERS: Record<VibeAmbientId, (node: Tone.Gain) => AmbientBed> = {
  calm: buildCalmAmbient,
  field: buildFieldAmbient,
  orbit: buildOrbitAmbient,
  workshop: buildWorkshopAmbient,
  studio: buildStudioAmbient,
  bold: buildBoldAmbient,
};

export function buildAmbientBed(vibe: VibeAmbientId, ambientNode: Tone.Gain): AmbientBed {
  return BUILDERS[vibe](ambientNode);
}
