"use client";

import { useCallback } from "react";

import { CapReachedNotice } from "@/components/child/voice/CapReachedNotice";
import { PermissionDeniedNotice } from "@/components/child/voice/PermissionDeniedNotice";
import { MicButton } from "@/components/child/MicButton";
import { usePersonalization } from "@/lib/PersonalizationProvider";
import { useVoiceInput } from "@/lib/useVoiceInput";

interface VoiceTextareaProps
  extends Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange"> {
  value: string;
  onChange: (next: string) => void;
  /** Defaults to the active child id from useSelectedChild context;
   *  callers can override (e.g., parent admin tools). */
  childId?: string;
  /** Append (default) preserves typed text; replace clears it. */
  appendMode?: "append" | "replace";
  voiceEnabled?: boolean;
  onSafetyIntervention?: (kind: string, suggestedResponse: string | null) => void;
}

/**
 * Drop-in replacement for ``<textarea>`` that adds a microphone
 * affordance. The textarea remains keyboardable; voice input is
 * always additive, never the only path.
 */
export function VoiceTextarea({
  value,
  onChange,
  childId,
  appendMode = "append",
  voiceEnabled,
  onSafetyIntervention,
  className,
  style,
  ...rest
}: VoiceTextareaProps) {
  const { profile } = usePersonalization();
  const policyEnabled = voiceEnabled ?? true;
  const effectiveChildId = childId ?? profile.child_id;
  // The provider's profile already carries the policy snapshot via
  // out_of_policy; the legacy flag is exposed on the library/policy
  // endpoints. For this hook we trust the caller's voiceEnabled
  // prop (default true), and the backend returns 403 if the policy
  // disallows voice. The 403 path renders an inline notice below.

  const handleTranscript = useCallback(
    (text: string) => {
      if (!text) return;
      if (appendMode === "replace") {
        onChange(text);
        return;
      }
      onChange(value.length === 0 ? text : `${value.trim()} ${text.trim()}`.trim());
    },
    [appendMode, onChange, value],
  );

  const [state, controls] = useVoiceInput({
    childId: effectiveChildId,
    onTranscript: handleTranscript,
    onSafetyIntervention,
  });

  const showCapNotice = state.status === "cap_reached";
  const showPermNotice = state.status === "permission_denied";
  const showMic = policyEnabled && !showCapNotice && !showPermNotice;

  return (
    <div
      className={["relative w-full", className ?? ""].join(" ").trim()}
      style={style}
    >
      <textarea
        {...rest}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={[
          "block w-full px-4 py-3 pr-14 text-base leading-relaxed",
          "border border-(--color-border) rounded-2xl bg-(--color-surface) text-(--color-text)",
          "focus:outline-none focus:ring-2 focus:ring-(--color-accent)/30",
          "min-h-[80px]",
          "text-[16px]",  // iOS zoom-on-focus guard
        ].join(" ")}
      />
      <div className="absolute right-2 bottom-2 flex items-center gap-2">
        {showCapNotice && <CapReachedNotice />}
        {showPermNotice && <PermissionDeniedNotice />}
        {showMic && (
          <MicButton
            status={state.status}
            recordingDurationMs={state.recordingDurationMs}
            onStart={controls.start}
            onStop={controls.stop}
            onCancel={controls.cancel}
          />
        )}
      </div>
    </div>
  );
}

export default VoiceTextarea;
