"use client";

/**
 * MediaRecorder wrapper that normalizes codec selection across
 * browsers and exposes a live amplitude callback for the recording
 * indicator's waveform.
 *
 * Preferred codec: webm/opus. iOS Safari falls back to audio/mp4 if
 * webm/opus is unsupported. The recorder enforces a hard duration cap
 * (defaults to 60s) so a stuck button can't OOM the device.
 */

export interface AudioRecording {
  blob: Blob;
  mimeType: string;
  durationSeconds: number;
  bytes: number;
}

export interface AudioRecorder {
  start: () => Promise<void>;
  stop: () => Promise<AudioRecording>;
  cancel: () => void;
  onAmplitude: (cb: (level: number) => void) => void;
}

export interface CreateAudioRecorderOptions {
  maxDurationSeconds?: number;
  bitsPerSecond?: number;
  silenceAutoStopMs?: number | null;
}

const PREFERRED_TYPES = [
  "audio/webm;codecs=opus",
  "audio/webm",
  "audio/mp4",
  "audio/mp4;codecs=mp4a.40.2",
];

function pickMimeType(): string {
  if (typeof MediaRecorder === "undefined") return "audio/webm";
  for (const t of PREFERRED_TYPES) {
    if (MediaRecorder.isTypeSupported(t)) return t;
  }
  return "audio/webm";
}

export async function createAudioRecorder(
  opts: CreateAudioRecorderOptions = {},
): Promise<AudioRecorder> {
  if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) {
    throw new Error("MediaRecorder unsupported in this environment");
  }
  const maxDuration = opts.maxDurationSeconds ?? 60;

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mimeType = pickMimeType();

  const recorderOptions: MediaRecorderOptions = {
    mimeType,
    audioBitsPerSecond: opts.bitsPerSecond ?? 24000,
  };
  const recorder = new MediaRecorder(stream, recorderOptions);
  const chunks: Blob[] = [];
  let startedAt = 0;
  let autoStopTimer: ReturnType<typeof setTimeout> | null = null;
  let amplitudeCb: ((level: number) => void) | null = null;
  let analyser: AnalyserNode | null = null;
  let rafId = 0;
  let audioCtx: AudioContext | null = null;

  recorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) chunks.push(e.data);
  };

  function setupAnalyser() {
    try {
      const Ctx =
        (window as unknown as { AudioContext?: typeof AudioContext; webkitAudioContext?: typeof AudioContext })
          .AudioContext ??
        (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!Ctx) return;
      audioCtx = new Ctx();
      const src = audioCtx.createMediaStreamSource(stream);
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      src.connect(analyser);
      const buf = new Uint8Array(analyser.frequencyBinCount);
      const tick = () => {
        if (!analyser) return;
        analyser.getByteTimeDomainData(buf);
        let peak = 0;
        for (const v of buf) {
          const delta = Math.abs(v - 128);
          if (delta > peak) peak = delta;
        }
        const level = Math.min(1, peak / 128);
        amplitudeCb?.(level);
        rafId = requestAnimationFrame(tick);
      };
      rafId = requestAnimationFrame(tick);
    } catch {
      // Visualization is a UX nicety; failures should not block recording.
    }
  }

  function teardown() {
    if (autoStopTimer) clearTimeout(autoStopTimer);
    autoStopTimer = null;
    if (rafId) cancelAnimationFrame(rafId);
    analyser = null;
    try {
      void audioCtx?.close();
    } catch {
      // ignored
    }
    audioCtx = null;
    for (const track of stream.getTracks()) track.stop();
  }

  return {
    async start() {
      chunks.length = 0;
      startedAt = Date.now();
      recorder.start(250);
      setupAnalyser();
      autoStopTimer = setTimeout(() => {
        if (recorder.state === "recording") recorder.stop();
      }, maxDuration * 1000);
    },

    async stop(): Promise<AudioRecording> {
      const stopped = new Promise<void>((resolve) => {
        recorder.addEventListener("stop", () => resolve(), { once: true });
      });
      if (recorder.state === "recording") recorder.stop();
      await stopped;
      teardown();
      const durationSeconds = Math.max(0, (Date.now() - startedAt) / 1000);
      const blob = new Blob(chunks, { type: mimeType });
      return {
        blob,
        mimeType,
        durationSeconds,
        bytes: blob.size,
      };
    },

    cancel() {
      if (recorder.state === "recording") recorder.stop();
      teardown();
      chunks.length = 0;
    },

    onAmplitude(cb) {
      amplitudeCb = cb;
    },
  };
}
