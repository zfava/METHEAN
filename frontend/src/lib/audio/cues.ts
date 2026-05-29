import * as Tone from "tone";

/**
 * Procedural event cues for the kid surface, composed entirely in
 * Tone.js. No sample files.
 *
 * Each factory returns a `play()` that builds a small ephemeral graph
 * (oscillators -> envelope -> effects -> master), schedules it, and
 * disposes its nodes after the envelope plus a short tail. Building
 * fresh per play keeps repeated triggers from reusing disposed nodes.
 *
 * Loudness discipline: every cue carries an inherent dBFS peak (the
 * "full" level). `ctx.volume` (0..1, from the caller's opts.volume,
 * default 1) scales it down. The master node then applies the pack
 * tier. Nothing in the system peaks above -6dBFS.
 */

export interface CueContext {
  master: Tone.ToneAudioNode;
  /** 0..1, multiplied by the cue's inherent loudness. */
  volume: number;
}

// Note frequencies (Hz) used across the cues.
const C5 = 523.25;
const E5 = 659.25;
const G5 = 783.99;
const A5 = 880.0;
const F5 = 698.46;
const C6 = 1046.5;

/** Dispose a set of nodes after `seconds`, swallowing any errors. */
function disposeAfter(nodes: Array<{ dispose: () => void }>, seconds: number): void {
  setTimeout(() => {
    for (const n of nodes) {
      try {
        n.dispose();
      } catch {
        // node may already be disposed; cues are advisory.
      }
    }
  }, seconds * 1000);
}

/** Linear gain for an inherent dBFS peak scaled by the caller volume. */
function cueGain(peakDb: number, volume: number): Tone.Gain {
  return new Tone.Gain(Tone.dbToGain(peakDb) * volume);
}

/**
 * activity_start: a single soft sine rising a perfect fifth C5 -> G5.
 * Gentle reverb tail. Inherent -16dBFS, ~700ms.
 */
export function buildActivityStartCue(ctx: CueContext): () => void {
  return () => {
    void (async () => {
      const out = cueGain(-16, ctx.volume).connect(ctx.master);
      const reverb = new Tone.Reverb({ decay: 1.2, wet: 0.15 }).connect(out);
      const synth = new Tone.Synth({
        oscillator: { type: "sine" },
        envelope: { attack: 0.18, decay: 0.28, sustain: 0.5, release: 0.32 },
      }).connect(reverb);
      await reverb.ready;
      const now = Tone.now();
      synth.triggerAttack(C5, now);
      synth.frequency.exponentialRampToValueAtTime(G5, now + 0.18);
      synth.triggerRelease(now + 0.48);
      disposeAfter([synth, reverb, out], 1.5);
    })();
  };
}

/**
 * correct: a consonant major third C5 + E5 on triangle oscillators,
 * panned slightly apart, bell-like decay, subtle chorus. The third is
 * always a major third (never dissonant). Inherent -14dBFS, ~600ms.
 */
export function buildCorrectCue(ctx: CueContext): () => void {
  return () => {
    const out = cueGain(-14, ctx.volume).connect(ctx.master);
    const chorus = new Tone.Chorus({ frequency: 0.5, delayTime: 2.5, depth: 0.1, wet: 0.5 })
      .connect(out)
      .start();
    const envelope = { attack: 0.08, decay: 0.4, sustain: 0.0, release: 0.1 } as const;
    const lowVoice = new Tone.Synth({ oscillator: { type: "triangle" }, envelope }).connect(
      new Tone.Panner(-0.1).connect(chorus),
    );
    const highVoice = new Tone.Synth({ oscillator: { type: "triangle" }, envelope }).connect(
      new Tone.Panner(0.1).connect(chorus),
    );
    const now = Tone.now();
    lowVoice.triggerAttackRelease(C5, 0.4, now);
    highVoice.triggerAttackRelease(E5, 0.4, now);
    disposeAfter([lowVoice, highVoice, chorus, out], 1.5);
  };
}

/**
 * hint_revealed: a falling perfect fourth A5 -> E5 on a soft FM patch,
 * with a pitch glide. Quieter than `correct` (it is a "consider this",
 * not a reward). Inherent -18dBFS, ~500ms, no extra effects.
 */
export function buildHintRevealedCue(ctx: CueContext): () => void {
  return () => {
    const out = cueGain(-18, ctx.volume).connect(ctx.master);
    const fm = new Tone.FMSynth({
      harmonicity: 2,
      modulationIndex: 1.5,
      oscillator: { type: "sine" },
      envelope: { attack: 0.06, decay: 0.1, sustain: 0.6, release: 0.35 },
      modulation: { type: "sine" },
      modulationEnvelope: { attack: 0.05, decay: 0.1, sustain: 0.4, release: 0.2 },
    }).connect(out);
    const now = Tone.now();
    fm.triggerAttack(A5, now);
    fm.frequency.exponentialRampToValueAtTime(E5, now + 0.35);
    fm.triggerRelease(now + 0.41);
    disposeAfter([fm, out], 1.5);
  };
}

/**
 * activity_complete: a four-note resolved phrase C5 -> G5 -> A5 -> F5
 * (I-V-vi-IV in C major, in inversion), each note 200ms with 50ms
 * overlap, warm pad (sine melody plus a quiet detuned-saw undertone),
 * subtle reverb. Final note has an extended release. Inherent -10dBFS,
 * ~900ms.
 */
export function buildActivityCompleteCue(ctx: CueContext): () => void {
  return () => {
    void (async () => {
      const out = cueGain(-10, ctx.volume).connect(ctx.master);
      const reverb = new Tone.Reverb({ decay: 1.0, wet: 0.2 }).connect(out);
      const melody = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "sine" },
        envelope: { attack: 0.04, decay: 0.2, sustain: 0.3, release: 0.3 },
      }).connect(reverb);
      // Detuned-saw undertone, filtered and -12dB under the melody.
      const underGain = new Tone.Gain(Tone.dbToGain(-12)).connect(reverb);
      const underFilter = new Tone.Filter(1800, "lowpass").connect(underGain);
      const under = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "sawtooth" },
        detune: 6,
        envelope: { attack: 0.05, decay: 0.2, sustain: 0.3, release: 0.4 },
      }).connect(underFilter);
      await reverb.ready;
      const now = Tone.now();
      const phrase = [C5, G5, A5, F5];
      phrase.forEach((freq, i) => {
        const t = now + i * 0.15; // 200ms note, 50ms overlap => 150ms step
        const dur = i === phrase.length - 1 ? 0.6 : 0.2;
        melody.triggerAttackRelease(freq, dur, t);
        under.triggerAttackRelease(freq, dur, t);
      });
      disposeAfter([melody, under, underFilter, underGain, reverb, out], 2.0);
    })();
  };
}

/**
 * mastery_up: the rare celebration cue. A rising octave arpeggio
 * C5 -> E5 -> G5 -> C6 on a bell-like FM patch, then a sparkle layer
 * of eight short filtered-noise bursts panned randomly across 600ms.
 * The loudest cue in the system at -6dBFS, ~1.4s.
 */
export function buildMasteryUpCue(ctx: CueContext): () => void {
  return () => {
    void (async () => {
      const out = cueGain(-6, ctx.volume).connect(ctx.master);
      const reverb = new Tone.Reverb({ decay: 2.0, wet: 0.3 }).connect(out);
      const bell = new Tone.FMSynth({
        harmonicity: 3.01,
        modulationIndex: 8,
        oscillator: { type: "sine" },
        envelope: { attack: 0.005, decay: 0.25, sustain: 0.0, release: 0.2 },
        modulation: { type: "sine" },
        modulationEnvelope: { attack: 0.005, decay: 0.2, sustain: 0.0, release: 0.2 },
      }).connect(reverb);
      await reverb.ready;
      const now = Tone.now();
      const arp = [C5, E5, G5, C6];
      arp.forEach((freq, i) => {
        bell.triggerAttackRelease(freq, 0.18, now + i * 0.13);
      });
      // Sparkle: 8 bandpass noise bursts scattered after the C6 hits.
      const c6At = now + 3 * 0.13;
      const sparkleNodes: Array<{ dispose: () => void }> = [];
      for (let k = 0; k < 8; k++) {
        const panner = new Tone.Panner(Math.random() * 2 - 1).connect(reverb);
        const bp = new Tone.Filter({
          type: "bandpass",
          frequency: 4000 + Math.random() * 4000,
          Q: 4,
        }).connect(panner);
        const burst = new Tone.NoiseSynth({
          noise: { type: "white" },
          envelope: { attack: 0.005, decay: 0.045, sustain: 0.0, release: 0.02 },
        }).connect(bp);
        burst.triggerAttackRelease(0.05, c6At + Math.random() * 0.6);
        sparkleNodes.push(burst, bp, panner);
      }
      disposeAfter([bell, ...sparkleNodes, reverb, out], 2.5);
    })();
  };
}

/**
 * day_complete: the warmest, longest cue. A vi-IV-I-V progression in
 * C major (Am-F-C-G) with smooth close-voicing voice-leading, warm
 * detuned-saw pad lowpass-filtered with a slow vibrato on the cutoff,
 * deep reverb. Evokes "well done, rest." Inherent -12dBFS, ~2.8s.
 */
export function buildDayCompleteCue(ctx: CueContext): () => void {
  return () => {
    void (async () => {
      const out = cueGain(-12, ctx.volume).connect(ctx.master);
      const reverb = new Tone.Reverb({ decay: 3.5, wet: 0.4 }).connect(out);
      const filter = new Tone.Filter(3000, "lowpass").connect(reverb);
      // Tape-like vibrato: 0.5Hz LFO on cutoff, +/-200Hz around 3kHz.
      const lfo = new Tone.LFO({ frequency: 0.5, min: 2800, max: 3200 }).start();
      lfo.connect(filter.frequency);
      const pad = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "sawtooth" },
        detune: 8,
        envelope: { attack: 0.2, decay: 0.3, sustain: 0.6, release: 0.6 },
      }).connect(filter);
      const sub = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "sine" },
        envelope: { attack: 0.2, decay: 0.3, sustain: 0.6, release: 0.6 },
      }).connect(new Tone.Gain(Tone.dbToGain(-6)).connect(filter));
      await reverb.ready;
      const now = Tone.now();
      // vi-IV-I-V, close voicings descending for smooth voice-leading.
      const chords: string[][] = [
        ["A4", "C5", "E5"], // Am (vi)
        ["F4", "A4", "C5"], // F  (IV)
        ["E4", "G4", "C5"], // C  (I)
        ["D4", "G4", "B4"], // G  (V)
      ];
      const subRoots = ["A2", "F2", "C2", "G2"];
      chords.forEach((chord, i) => {
        const t = now + i * 0.6;
        const dur = i === chords.length - 1 ? 0.9 : 0.6;
        pad.triggerAttackRelease(chord, dur, t);
        sub.triggerAttackRelease(subRoots[i], dur, t);
      });
      disposeAfter([pad, sub, filter, lfo, reverb, out], 4.5);
    })();
  };
}
