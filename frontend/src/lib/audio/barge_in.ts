"use client";

/**
 * Ambient voice-activity detector used to pause tutor TTS playback
 * when the kid starts talking ("barge-in"). Listens on a separate
 * MediaStream from the recorder so the kid can interrupt without
 * the recorder having to be active.
 *
 * The detector fires the callback ONCE per engagement; the parent
 * stops the detector, handles the interruption, and creates a new
 * detector when it wants to listen again. This avoids spamming the
 * callback on every frame of speech.
 */

export interface BargeInDetectorOptions {
  energyThreshold?: number;
  minSpeechMs?: number;
  onSpeechDetected: () => void;
}

export interface BargeInDetector {
  stop: () => void;
}

const DEFAULT_ENERGY_THRESHOLD = 0.15;
const DEFAULT_MIN_SPEECH_MS = 200;

export function createBargeInDetector(
  stream: MediaStream,
  opts: BargeInDetectorOptions,
): BargeInDetector {
  const threshold = opts.energyThreshold ?? DEFAULT_ENERGY_THRESHOLD;
  const minSpeechMs = opts.minSpeechMs ?? DEFAULT_MIN_SPEECH_MS;

  let raf = 0;
  let speechStartedAt: number | null = null;
  let stopped = false;
  let audioCtx: AudioContext | null = null;

  const Ctx =
    (window as unknown as { AudioContext?: typeof AudioContext; webkitAudioContext?: typeof AudioContext })
      .AudioContext ??
    (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;

  if (!Ctx) {
    // No Web Audio API: detector is a no-op. Caller still gets a
    // working .stop() so wiring is uniform.
    return { stop: () => {} };
  }

  try {
    audioCtx = new Ctx();
    const src = audioCtx.createMediaStreamSource(stream);
    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = 256;
    src.connect(analyser);
    const buf = new Uint8Array(analyser.frequencyBinCount);

    const tick = () => {
      if (stopped) return;
      analyser.getByteTimeDomainData(buf);
      let peak = 0;
      for (const v of buf) {
        const delta = Math.abs(v - 128);
        if (delta > peak) peak = delta;
      }
      const level = Math.min(1, peak / 128);
      const now = performance.now();
      if (level >= threshold) {
        if (speechStartedAt === null) speechStartedAt = now;
        if (now - speechStartedAt >= minSpeechMs) {
          // Fire once; the caller is responsible for stopping us.
          stopped = true;
          try {
            opts.onSpeechDetected();
          } catch {
            // Callback errors are swallowed; barge-in is advisory.
          }
          return;
        }
      } else {
        speechStartedAt = null;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  } catch {
    // Some browsers reject AudioContext on insecure origins; treat
    // detector as no-op.
  }

  return {
    stop() {
      stopped = true;
      if (raf) cancelAnimationFrame(raf);
      try {
        void audioCtx?.close();
      } catch {
        // ignore
      }
    },
  };
}
