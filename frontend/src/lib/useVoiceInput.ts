"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { transcribe as transcribeApi } from "@/lib/api";
import { type AudioRecorder, createAudioRecorder } from "@/lib/audio/encoder";
import { requestMicPermission } from "@/lib/audio/permissions";

export type VoiceInputStatus =
  | "idle"
  | "requesting_permission"
  | "permission_denied"
  | "recording"
  | "transcribing"
  | "transcribed"
  | "cap_reached"
  | "error";

export interface VoiceInputError {
  kind: string;
  message: string;
}

export interface VoiceInputState {
  status: VoiceInputStatus;
  recordingDurationMs: number;
  amplitude: number;
  remainingMinutes: number | null;
  error: VoiceInputError | null;
  lastTranscript: string | null;
}

export interface VoiceInputControls {
  start: () => Promise<void>;
  stop: () => Promise<string>;
  cancel: () => void;
  retry: () => Promise<void>;
}

export interface UseVoiceInputOptions {
  childId: string;
  maxDurationSeconds?: number;
  silenceAutoStopMs?: number | null;
  onTranscript?: (text: string) => void;
  onSafetyIntervention?: (kind: string, suggestedResponse: string | null) => void;
}

/**
 * State machine: idle -> requesting_permission -> recording ->
 * transcribing -> transcribed -> idle (auto). Errors are terminal
 * until retry()/cancel().
 *
 * The hook never throws to its caller; failures land in
 * ``state.error`` and the consuming component renders the matching
 * notice (PermissionDeniedNotice, CapReachedNotice, etc.).
 */
export function useVoiceInput(opts: UseVoiceInputOptions): [VoiceInputState, VoiceInputControls] {
  const { childId, onTranscript, onSafetyIntervention } = opts;
  const [status, setStatus] = useState<VoiceInputStatus>("idle");
  const [recordingDurationMs, setRecordingDurationMs] = useState(0);
  const [amplitude, setAmplitude] = useState(0);
  const [remainingMinutes, setRemainingMinutes] = useState<number | null>(null);
  const [error, setError] = useState<VoiceInputError | null>(null);
  const [lastTranscript, setLastTranscript] = useState<string | null>(null);

  const recorderRef = useRef<AudioRecorder | null>(null);
  const startedAtRef = useRef<number>(0);
  const tickerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Clean up on unmount: drop the active recorder if any, so the
  // microphone LED goes dark even when the component unmounts mid-
  // recording.
  useEffect(() => {
    return () => {
      recorderRef.current?.cancel();
      if (tickerRef.current) clearInterval(tickerRef.current);
    };
  }, []);

  const start = useCallback(async () => {
    setError(null);
    setStatus("requesting_permission");
    const perm = await requestMicPermission();
    if (perm !== "granted") {
      setStatus("permission_denied");
      setError({ kind: perm, message: "Microphone access is required." });
      return;
    }
    try {
      const recorder = await createAudioRecorder({
        maxDurationSeconds: opts.maxDurationSeconds ?? 55,
        silenceAutoStopMs: opts.silenceAutoStopMs ?? null,
      });
      recorder.onAmplitude((lvl) => setAmplitude(lvl));
      await recorder.start();
      recorderRef.current = recorder;
      startedAtRef.current = Date.now();
      setRecordingDurationMs(0);
      tickerRef.current = setInterval(() => {
        setRecordingDurationMs(Date.now() - startedAtRef.current);
      }, 100);
      setStatus("recording");
    } catch (err) {
      const message = (err as { message?: string } | null)?.message ?? "Couldn't start recording.";
      setStatus("error");
      setError({ kind: "recorder_failed", message });
    }
  }, [opts.maxDurationSeconds, opts.silenceAutoStopMs]);

  const stop = useCallback(async (): Promise<string> => {
    if (!recorderRef.current) return "";
    if (tickerRef.current) clearInterval(tickerRef.current);
    tickerRef.current = null;
    setStatus("transcribing");
    setAmplitude(0);
    let recording: { blob: Blob; durationSeconds: number };
    try {
      recording = await recorderRef.current.stop();
    } catch (err) {
      const message = (err as { message?: string } | null)?.message ?? "Couldn't finish recording.";
      setStatus("error");
      setError({ kind: "recorder_stop_failed", message });
      return "";
    } finally {
      recorderRef.current = null;
    }

    try {
      const resp = await transcribeApi.submit(childId, recording.blob);
      setRemainingMinutes(resp.remaining_minutes);
      if (resp.safety_intervention) {
        onSafetyIntervention?.(resp.intervention_kind ?? "unknown", resp.suggested_response);
        setStatus("idle");
        setLastTranscript("");
        return "";
      }
      setLastTranscript(resp.text);
      setStatus("transcribed");
      onTranscript?.(resp.text);
      // Auto-rest after a brief transcribed flash so consecutive
      // recordings don't need an extra tap.
      window.setTimeout(() => setStatus("idle"), 400);
      return resp.text;
    } catch (err) {
      const e = err as { status?: number; message?: string } | null;
      let detail: { error?: string } = {};
      try {
        detail = JSON.parse(e?.message ?? "{}") as { error?: string };
      } catch {
        // detail stays empty; the kind below covers it.
      }
      if (e?.status === 429) {
        setStatus("cap_reached");
        setError({ kind: detail.error ?? "voice_cap_reached", message: "Voice time is up for today." });
        return "";
      }
      if (e?.status === 403) {
        setStatus("error");
        setError({ kind: detail.error ?? "voice_input_disabled", message: "Voice is off right now." });
        return "";
      }
      setStatus("error");
      setError({
        kind: detail.error ?? "transcribe_failed",
        message: e?.message ?? "Couldn't transcribe that.",
      });
      return "";
    }
  }, [childId, onTranscript, onSafetyIntervention]);

  const cancel = useCallback(() => {
    recorderRef.current?.cancel();
    recorderRef.current = null;
    if (tickerRef.current) clearInterval(tickerRef.current);
    tickerRef.current = null;
    setAmplitude(0);
    setRecordingDurationMs(0);
    setStatus("idle");
    setError(null);
  }, []);

  const retry = useCallback(async () => {
    setError(null);
    setStatus("idle");
    await start();
  }, [start]);

  return [
    {
      status,
      recordingDurationMs,
      amplitude,
      remainingMinutes,
      error,
      lastTranscript,
    },
    { start, stop, cancel, retry },
  ];
}
