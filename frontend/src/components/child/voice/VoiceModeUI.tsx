"use client";

import { useEffect } from "react";

import { CompanionAvatar } from "@/components/CompanionAvatar";
import { TalkButton, type InteractionStyle } from "@/components/child/voice/TalkButton";
import { VoiceModeMinutesIndicator } from "@/components/child/voice/VoiceModeMinutesIndicator";
import { VoiceModeStatusLine } from "@/components/child/voice/VoiceModeStatusLine";
import type {
  VoiceConversationControls,
  VoiceConversationState,
} from "@/lib/useVoiceConversation";

interface Props {
  companionVoice: string;
  companionName: string;
  state: VoiceConversationState;
  controls: VoiceConversationControls;
  interactionStyle: InteractionStyle;
  onExit: () => void;
}

/**
 * Full-bleed voice-mode surface that replaces the text composer
 * inside TutorChat when voice mode is on. The avatar breathes on
 * idle and tracks the conversation status; the caption area shows
 * the tutor's last reply so deaf users (and read-along learners)
 * never lose the content.
 */
export function VoiceModeUI({
  companionVoice,
  companionName,
  state,
  controls,
  interactionStyle,
  onExit,
}: Props) {
  // Announce status transitions via a polite live region. The
  // StatusLine already has aria-live; this is a backup that fires
  // exactly once per status change for screen readers that ignore
  // re-renders inside a polite region.
  useEffect(() => {
    const live = document.getElementById("voice-mode-live");
    if (live) live.textContent = state.status;
  }, [state.status]);

  const avatarBreathing =
    state.status === "idle" || state.status === "speaking";

  return (
    <div className="flex flex-col h-full bg-(--color-surface)">
      <header className="flex items-center justify-between px-4 pt-3">
        <button
          type="button"
          onClick={onExit}
          aria-label="Exit voice mode"
          className="w-10 h-10 rounded-full flex items-center justify-center text-(--color-text-tertiary) hover:bg-(--color-page) min-h-[44px] min-w-[44px]"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
            <line x1="6" y1="6" x2="18" y2="18" />
            <line x1="18" y1="6" x2="6" y2="18" />
          </svg>
        </button>
        <VoiceModeMinutesIndicator
          remainingInputMinutes={state.remainingInputMinutes}
          remainingOutputMinutes={state.remainingOutputMinutes}
        />
      </header>

      <span id="voice-mode-live" aria-live="polite" className="sr-only" />

      <main className="flex-1 flex flex-col items-center justify-center px-6 gap-5">
        <div
          className={[
            "text-(--color-accent) flex items-center justify-center",
            avatarBreathing ? "motion-safe:animate-pulse-soft" : "",
          ].join(" ")}
          style={{ width: 144, height: 144 }}
          aria-hidden="true"
        >
          <CompanionAvatar personaId={companionVoice || "default_warm"} size={144} />
        </div>

        <div className="w-full max-w-sm flex flex-col items-center gap-2">
          <p className="text-sm font-medium text-(--color-text)">{companionName || "Your Companion"}</p>
          <VoiceModeStatusLine status={state.status} interactionStyle={interactionStyle} />
        </div>

        {state.lastResponseText && (
          <div
            role="region"
            aria-label="Tutor caption"
            className="w-full max-w-md rounded-2xl border border-(--color-border) bg-(--color-page) px-4 py-3 text-sm text-(--color-text) leading-relaxed text-center"
          >
            {state.lastResponseText}
          </div>
        )}

        {state.error && (
          <p className="text-xs text-(--color-danger)" role="alert">
            {state.error.message}
          </p>
        )}
      </main>

      <footer className="flex flex-col items-center pb-8 gap-2">
        <TalkButton
          status={state.status}
          interactionStyle={interactionStyle}
          onStart={controls.startListening}
          onStop={controls.stopListening}
          onCancel={controls.cancel}
          disabled={state.status === "cap_input_reached" || state.status === "permission_lost"}
        />
        {(state.status === "cap_input_reached" || state.status === "permission_lost") && (
          <button
            type="button"
            onClick={onExit}
            className="text-xs text-(--color-text-secondary) hover:text-(--color-text) underline underline-offset-2 min-h-[36px] px-2"
          >
            Return to text
          </button>
        )}
      </footer>
    </div>
  );
}

export default VoiceModeUI;
