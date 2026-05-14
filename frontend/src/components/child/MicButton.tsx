"use client";

import { useEffect, useRef } from "react";

import { haptic } from "@/lib/haptics";
import type { VoiceInputStatus } from "@/lib/useVoiceInput";

interface MicButtonProps {
  status: VoiceInputStatus;
  recordingDurationMs: number;
  onStart: () => void | Promise<void>;
  onStop: () => void | Promise<string | void>;
  onCancel: () => void;
  /** Hide the button entirely (e.g., when voice is policy-disabled). */
  hidden?: boolean;
}

/**
 * Accessible mic button. Tap toggles record/stop; Space and Enter do
 * the same; Escape cancels. Minimum 44x44 hit target on mobile.
 *
 * The aria-label updates per state so screen readers announce the
 * transition without the consumer wiring a separate live region.
 */
export function MicButton({
  status,
  recordingDurationMs,
  onStart,
  onStop,
  onCancel,
  hidden,
}: MicButtonProps) {
  const liveRef = useRef<HTMLSpanElement>(null);
  const isRecording = status === "recording";
  const isBusy = status === "requesting_permission" || status === "transcribing";

  useEffect(() => {
    if (!liveRef.current) return;
    if (status === "recording") liveRef.current.textContent = "Recording started";
    else if (status === "transcribing") liveRef.current.textContent = "Transcribing";
    else if (status === "transcribed") liveRef.current.textContent = "Transcribed";
  }, [status]);

  if (hidden) return null;

  const onClick = async () => {
    if (isRecording) {
      haptic("medium");
      await onStop();
      return;
    }
    if (isBusy) return;
    haptic("light");
    await onStart();
  };

  const onKey = async (e: React.KeyboardEvent<HTMLButtonElement>) => {
    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      await onClick();
      return;
    }
    if (e.key === "Escape") {
      e.preventDefault();
      onCancel();
    }
  };

  const seconds = Math.floor(recordingDurationMs / 1000);
  const label = isRecording
    ? "Stop voice input"
    : isBusy
      ? "Transcribing"
      : status === "cap_reached"
        ? "Voice time used up"
        : status === "permission_denied"
          ? "Microphone blocked"
          : "Start voice input";

  return (
    <>
      <span ref={liveRef} aria-live="polite" className="sr-only" />
      <button
        type="button"
        onClick={onClick}
        onKeyDown={onKey}
        aria-pressed={isRecording}
        aria-label={label}
        disabled={isBusy || status === "cap_reached" || status === "permission_denied"}
        className={[
          "inline-flex items-center justify-center rounded-full",
          "min-h-[44px] min-w-[44px] w-11 h-11 sm:w-9 sm:h-9 sm:min-h-0 sm:min-w-0",
          "transition-colors disabled:opacity-50",
          isRecording
            ? "bg-(--color-danger) text-white animate-pulse"
            : "bg-(--color-accent) text-white hover:opacity-90",
        ].join(" ")}
      >
        {isBusy ? (
          <span
            className="block w-4 h-4 rounded-full border-2 border-white/40 border-t-white animate-spin"
            aria-hidden="true"
          />
        ) : isRecording ? (
          <span className="text-xs font-semibold tabular-nums" aria-hidden="true">
            {String(Math.floor(seconds / 60)).padStart(1, "0")}:{String(seconds % 60).padStart(2, "0")}
          </span>
        ) : (
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
            <path d="M19 10a7 7 0 0 1-14 0" />
            <line x1="12" y1="19" x2="12" y2="23" />
            <line x1="8" y1="23" x2="16" y2="23" />
          </svg>
        )}
      </button>
    </>
  );
}

export default MicButton;
