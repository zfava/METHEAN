"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { createBargeInDetector } from "@/lib/audio/barge_in";
import { useVoiceInput, type VoiceInputStatus } from "@/lib/useVoiceInput";
import { useTutorVoice } from "@/lib/useTutorVoice";

/**
 * Voice-mode conversation orchestrator.
 *
 * Combines the input hook (transcribe via Whisper) and the output
 * hook (TTS playback) into one state machine the UI can render
 * declaratively. The state names match the spec's V2-03 diagram
 * (idle → listening → sending → transcribing → thinking →
 * speaking → idle, plus terminal error states).
 *
 * Barge-in: when status is "speaking", we mount a barge-in detector
 * on a fresh mic stream. When it fires, we stop TTS and transition
 * to listening. The detector takes < 200ms with typical browser
 * AudioContext latency.
 *
 * The hook owns the state; the UI is purely reactive. Tap-debouncing
 * lives in TalkButton so this layer doesn't need to know about
 * interaction style.
 */

export type VoiceConversationStatus =
  | "idle"
  | "listening"
  | "sending"
  | "transcribing"
  | "thinking"
  | "speaking"
  | "cap_input_reached"
  | "cap_output_reached"
  | "permission_lost"
  | "network_lost"
  | "error";

export interface VoiceConversationState {
  status: VoiceConversationStatus;
  currentTurnIndex: number;
  remainingInputMinutes: number | null;
  remainingOutputMinutes: number | null;
  error: Error | null;
  /** Last tutor text (for the captions area). */
  lastResponseText: string;
}

export interface VoiceConversationControls {
  startListening: () => Promise<void>;
  stopListening: () => Promise<void>;
  cancel: () => void;
  exit: () => void;
  retry: () => Promise<void>;
}

export interface UseVoiceConversationOptions {
  childId: string;
  /** Caller-supplied async function that sends the transcript to the
   *  tutor backend and yields the tutor's text response. Voice mode
   *  expects ≤2 sentences (server enforces). */
  sendToTutor: (transcript: string) => Promise<string>;
  onTranscriptReceived?: (text: string) => void;
  onResponseReceived?: (text: string) => void;
  onSafetyIntervention?: (kind: string) => void;
  onExit?: () => void;
}

export function useVoiceConversation(
  opts: UseVoiceConversationOptions,
): [VoiceConversationState, VoiceConversationControls] {
  const [status, setStatus] = useState<VoiceConversationStatus>("idle");
  const [turn, setTurn] = useState(0);
  const [error, setError] = useState<Error | null>(null);
  const [lastResponseText, setLastResponseText] = useState<string>("");
  const [remainingInputMinutes, setRemainingInputMinutes] = useState<number | null>(null);

  const turnRef = useRef(0);

  const [inputState, inputControls] = useVoiceInput({
    childId: opts.childId,
    onTranscript: (text) => {
      // Don't act on empty transcripts; the input hook already
      // surfaces "didn't hear that" inline.
      if (!text) return;
      opts.onTranscriptReceived?.(text);
      void runTutorTurn(text);
    },
    onSafetyIntervention: (kind) => {
      setStatus("idle");
      opts.onSafetyIntervention?.(kind);
    },
  });

  const [tutorVoiceState, tutorVoiceControls] = useTutorVoice();

  // Mirror cap signals from the underlying hooks.
  useEffect(() => {
    if (inputState.remainingMinutes !== null) {
      setRemainingInputMinutes(inputState.remainingMinutes);
    }
  }, [inputState.remainingMinutes]);

  // Translate input-hook status into conversation status. We only
  // mirror the input states that have a 1:1 conversation analog;
  // the tutor-turn states (thinking, speaking) are driven below.
  useEffect(() => {
    setStatus((cur) => mapInputToConversation(inputState.status, cur));
    if (inputState.error) setError(new Error(inputState.error.message));
  }, [inputState.status, inputState.error]);

  // Drive a tutor turn end-to-end: send transcript, await response,
  // play TTS. State transitions reflect each leg.
  const runTutorTurn = useCallback(
    async (transcript: string) => {
      setStatus("thinking");
      try {
        const responseText = await opts.sendToTutor(transcript);
        opts.onResponseReceived?.(responseText);
        setLastResponseText(responseText);
        if (!responseText) {
          setStatus("idle");
          return;
        }
        const messageId = `voice-${Date.now()}`;
        setStatus("speaking");
        await tutorVoiceControls.speak(messageId, responseText, { voiceMode: true });
        // The speak() call resolves immediately after Audio.play();
        // we transition back to idle when playback ends via the
        // separate effect below.
      } catch (e) {
        setStatus("error");
        setError(e as Error);
      }
    },
    [opts, tutorVoiceControls],
  );

  // Listen for tutor-voice "isPlaying" flipping false to advance
  // from speaking → idle. Also catches barge-in stops.
  useEffect(() => {
    if (status === "speaking" && !tutorVoiceState.isPlaying) {
      setStatus("idle");
      turnRef.current += 1;
      setTurn(turnRef.current);
    }
  }, [status, tutorVoiceState.isPlaying]);

  // Barge-in: while speaking, watch for ambient speech.
  useEffect(() => {
    if (status !== "speaking") return;
    if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) return;
    let detector: { stop: () => void } | null = null;
    let stream: MediaStream | null = null;
    let cancelled = false;
    void (async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (cancelled) {
          for (const t of stream.getTracks()) t.stop();
          return;
        }
        detector = createBargeInDetector(stream, {
          onSpeechDetected: () => {
            tutorVoiceControls.stop();
            // Auto-start listening on the kid's behalf; the kid is
            // already talking, so dropping straight into capture is
            // what they expect.
            void inputControls.start();
          },
        });
      } catch {
        // Permission lost or device missing; tutor will simply
        // finish speaking without a barge-in option.
      }
    })();
    return () => {
      cancelled = true;
      detector?.stop();
      if (stream) for (const t of stream.getTracks()) t.stop();
    };
  }, [status, tutorVoiceControls, inputControls]);

  const startListening = useCallback(async () => {
    setError(null);
    await inputControls.start();
  }, [inputControls]);

  const stopListening = useCallback(async () => {
    await inputControls.stop();
  }, [inputControls]);

  const cancel = useCallback(() => {
    inputControls.cancel();
    tutorVoiceControls.stop();
    setStatus("idle");
  }, [inputControls, tutorVoiceControls]);

  const exit = useCallback(() => {
    cancel();
    opts.onExit?.();
  }, [cancel, opts]);

  const retry = useCallback(async () => {
    setError(null);
    setStatus("idle");
  }, []);

  return [
    {
      status,
      currentTurnIndex: turn,
      remainingInputMinutes,
      remainingOutputMinutes: tutorVoiceState.error ? null : null,
      error,
      lastResponseText,
    },
    { startListening, stopListening, cancel, exit, retry },
  ];
}

function mapInputToConversation(
  inputStatus: VoiceInputStatus,
  current: VoiceConversationStatus,
): VoiceConversationStatus {
  switch (inputStatus) {
    case "idle":
      // Don't clobber thinking/speaking; those are driven by the
      // tutor turn, not the input hook.
      if (current === "thinking" || current === "speaking") return current;
      return "idle";
    case "requesting_permission":
      return "listening";
    case "recording":
      return "listening";
    case "transcribing":
      return "transcribing";
    case "transcribed":
      // Bridge state; the actual transition to "thinking" happens
      // inside runTutorTurn. Keep showing transcribing until then.
      return current === "transcribing" ? "transcribing" : current;
    case "cap_reached":
      return "cap_input_reached";
    case "permission_denied":
      return "permission_lost";
    case "error":
      return "error";
    default:
      return current;
  }
}
