"use client";

import { useCallback, useEffect, useRef } from "react";

import { haptic } from "@/lib/haptics";
import type { VoiceConversationStatus } from "@/lib/useVoiceConversation";

export type InteractionStyle = "press_hold" | "tap_toggle";

interface TalkButtonProps {
  status: VoiceConversationStatus;
  interactionStyle: InteractionStyle;
  onStart: () => void | Promise<void>;
  onStop: () => void | Promise<void>;
  onCancel: () => void;
  /** Hide the button when the kid has no remaining voice time. */
  disabled?: boolean;
}

const DEBOUNCE_MS = 300;
const MAX_HOLD_MS = 10_000;

/**
 * Circular tap-or-hold button that drives the voice-mode state
 * machine. 96px on mobile, 80px on desktop. ARIA pressed reflects
 * the recording state. The 300ms debounce prevents accidental
 * double-taps from kicking the recorder twice; the 10s auto-release
 * stops the recorder when a kid leans on the button.
 */
export function TalkButton({
  status,
  interactionStyle,
  onStart,
  onStop,
  onCancel,
  disabled,
}: TalkButtonProps) {
  const lastFireRef = useRef<number>(0);
  const holdTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isHoldingRef = useRef<boolean>(false);

  const debounced = useCallback((cb: () => void | Promise<void>) => {
    const now = Date.now();
    if (now - lastFireRef.current < DEBOUNCE_MS) return;
    lastFireRef.current = now;
    void cb();
  }, []);

  const triggerStart = useCallback(() => {
    haptic("light");
    debounced(onStart);
  }, [debounced, onStart]);

  const triggerStop = useCallback(() => {
    haptic("medium");
    debounced(onStop);
  }, [debounced, onStop]);

  // Press-and-hold handlers.
  const onPress = useCallback(() => {
    if (disabled || interactionStyle !== "press_hold") return;
    if (status !== "idle") return;
    isHoldingRef.current = true;
    triggerStart();
    holdTimerRef.current = setTimeout(() => {
      if (isHoldingRef.current) {
        isHoldingRef.current = false;
        triggerStop();
      }
    }, MAX_HOLD_MS);
  }, [disabled, interactionStyle, status, triggerStart, triggerStop]);

  const onRelease = useCallback(() => {
    if (interactionStyle !== "press_hold") return;
    if (!isHoldingRef.current) return;
    isHoldingRef.current = false;
    if (holdTimerRef.current) clearTimeout(holdTimerRef.current);
    triggerStop();
  }, [interactionStyle, triggerStop]);

  // Tap-to-toggle handler.
  const onTap = useCallback(() => {
    if (disabled) return;
    if (interactionStyle !== "tap_toggle") return;
    if (status === "idle") triggerStart();
    else if (status === "listening") triggerStop();
    // Other statuses (transcribing/thinking/speaking) ignore taps so
    // the kid doesn't restart mid-flight by accident.
  }, [disabled, interactionStyle, status, triggerStart, triggerStop]);

  // Keyboard: Space + Enter trigger the same as the active style;
  // Escape always cancels.
  const onKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLButtonElement>) => {
      if (e.key === "Escape") {
        e.preventDefault();
        onCancel();
        return;
      }
      if (e.key !== " " && e.key !== "Enter") return;
      e.preventDefault();
      if (interactionStyle === "tap_toggle") {
        onTap();
        return;
      }
      // press_hold: Space-down starts, Space-up stops. We rely on
      // the browser firing keyup separately; for keyboards that
      // repeat keydown, debounce protects us.
      if (status === "idle") triggerStart();
      else if (status === "listening") triggerStop();
    },
    [interactionStyle, status, onTap, triggerStart, triggerStop, onCancel],
  );

  // Cleanup timers on unmount.
  useEffect(() => {
    return () => {
      if (holdTimerRef.current) clearTimeout(holdTimerRef.current);
    };
  }, []);

  const isRecording = status === "listening";
  const isWorking = status === "transcribing" || status === "thinking";
  const isSpeaking = status === "speaking";
  const isCap = status === "cap_input_reached" || status === "cap_output_reached";

  const label = isRecording
    ? "Stop talking"
    : isWorking
      ? "Let me think"
      : isSpeaking
        ? "Speaking"
        : isCap
          ? "Voice time is up"
          : interactionStyle === "press_hold"
            ? "Press and hold to talk"
            : "Tap to talk";

  return (
    <button
      type="button"
      onMouseDown={interactionStyle === "press_hold" ? onPress : undefined}
      onMouseUp={interactionStyle === "press_hold" ? onRelease : undefined}
      onMouseLeave={interactionStyle === "press_hold" ? onRelease : undefined}
      onTouchStart={interactionStyle === "press_hold" ? onPress : undefined}
      onTouchEnd={interactionStyle === "press_hold" ? onRelease : undefined}
      onTouchCancel={interactionStyle === "press_hold" ? onRelease : undefined}
      onClick={interactionStyle === "tap_toggle" ? onTap : undefined}
      onKeyDown={onKeyDown}
      aria-pressed={isRecording}
      aria-label={label}
      disabled={disabled || isCap}
      className={[
        "rounded-full flex items-center justify-center select-none",
        "w-24 h-24 sm:w-20 sm:h-20",
        "min-h-[44px] min-w-[44px]",
        "transition-shadow duration-150 outline-none focus-visible:ring-4 focus-visible:ring-(--color-accent)/30",
        isRecording
          ? "bg-(--color-danger) text-white shadow-[0_0_0_8px_var(--color-danger-light)] motion-safe:animate-pulse"
          : isWorking
            ? "bg-(--color-accent-light) text-(--color-accent)"
            : isSpeaking
              ? "bg-(--color-accent) text-white"
              : isCap
                ? "bg-(--color-page) text-(--color-text-tertiary) opacity-60 cursor-not-allowed"
                : "bg-(--color-accent) text-white",
      ].join(" ")}
    >
      {isWorking ? (
        <span
          className="block w-7 h-7 rounded-full border-[3px] border-current/30 border-t-current animate-spin"
          aria-hidden="true"
        />
      ) : (
        <svg
          width="36"
          height="36"
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
  );
}

export default TalkButton;
