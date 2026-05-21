"use client";

/**
 * Presents a decodable reading passage in a comfortable reading
 * measure with a single tap-to-hear button.
 *
 * Playback reuses the tutor TTS path through useTutorVoice, so it
 * inherits the household voice-output policy gate, the chosen persona
 * voice, and the session-mute toggle. No separate audio stack.
 */

import type { PassageData } from "@/lib/api";
import { useTutorVoice } from "@/lib/useTutorVoice";

function SpeakerIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
      <path d="M15.5 8.5a5 5 0 0 1 0 7" />
      <path d="M18.5 5.5a9 9 0 0 1 0 13" />
    </svg>
  );
}

function StopIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <rect x="6" y="6" width="12" height="12" rx="2" />
    </svg>
  );
}

export function PassageReader({ passage }: { passage: PassageData }) {
  const [voiceState, voiceControls] = useTutorVoice();
  const isThisPlaying = voiceState.isPlaying && voiceState.currentMessageId === passage.id;

  function handleToggle() {
    if (isThisPlaying) {
      voiceControls.stop();
    } else {
      void voiceControls.speak(passage.id, passage.text);
    }
  }

  return (
    <section className="my-4 rounded-2xl border border-(--color-border) bg-(--color-surface) p-6 shadow-[var(--shadow-card)]">
      {passage.title && (
        <h3 className="mb-3 text-lg font-semibold text-(--color-text)">{passage.title}</h3>
      )}
      <p
        className="text-(--color-text) whitespace-pre-line"
        style={{ fontSize: "19px", lineHeight: 1.8, maxWidth: "34rem" }}
      >
        {passage.text}
      </p>
      <button
        type="button"
        onClick={handleToggle}
        aria-label={isThisPlaying ? "Stop reading this passage aloud" : "Hear this passage read aloud"}
        className="mt-5 inline-flex items-center gap-2 min-h-[44px] px-5 rounded-2xl bg-(--color-accent) text-white font-medium hover:opacity-90 transition-opacity focus:outline-none focus-visible:ring-2 focus-visible:ring-(--color-accent)/40"
      >
        {isThisPlaying ? <StopIcon /> : <SpeakerIcon />}
        {isThisPlaying ? "Stop" : "Hear it"}
      </button>
    </section>
  );
}

export default PassageReader;
