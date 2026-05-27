"use client";

import { useEffect, useRef } from "react";

import { haptic } from "@/lib/haptics";
import type { VoiceInputStatus } from "@/lib/useVoiceInput";
import { Pulse } from "@/components/child/motion";
import { Mic } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

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

  // While recording, wrap the button in <Pulse> so the listening
  // affordance reads as alive. Pulse honors reduceMotion internally
  // and falls back to the static border + danger background. The
  // wrapper does not affect the button's hit target.
  const buttonNode = (
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
            ? "bg-(--color-danger) text-white"
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
          <Icon icon={Mic} size={18} strokeWidth={2} />
        )}
      </button>
  );

  return (
    <>
      <span ref={liveRef} aria-live="polite" className="sr-only" />
      {isRecording ? <Pulse color="var(--color-danger)">{buttonNode}</Pulse> : buttonNode}
    </>
  );
}

export default MicButton;
