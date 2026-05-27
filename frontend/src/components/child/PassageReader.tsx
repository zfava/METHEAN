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
import { Square, Volume2 } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

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
      {/* Optional level eyebrow (e.g., "Decodable · Short A") sets the
          context above the title without competing with it. */}
      {passage.level && (
        <p className="type-eyebrow-sm text-(--color-text-tertiary) mb-2">{passage.level}</p>
      )}
      {passage.title && (
        <h3 className="mb-4 type-heading-lg text-(--color-text)">{passage.title}</h3>
      )}
      {/* Editorial body. Fraunces at opsz=36 + SOFT=75, ~19px, max
          ~640px measure. This is the highest-fidelity text surface
          in the product. */}
      <p
        className="type-editorial-lg text-(--color-text) whitespace-pre-line"
        style={{ maxWidth: "40rem" }}
      >
        {passage.text}
      </p>
      <button
        type="button"
        onClick={handleToggle}
        aria-label={isThisPlaying ? "Stop reading this passage aloud" : "Hear this passage read aloud"}
        className="mt-5 inline-flex items-center gap-2 min-h-[44px] px-5 rounded-2xl bg-(--color-accent) text-white font-medium hover:opacity-90 transition-opacity focus:outline-none focus-visible:ring-2 focus-visible:ring-(--color-accent)/40"
      >
        {isThisPlaying ? (
          <Icon icon={Square} size={18} strokeWidth={2} fill="currentColor" />
        ) : (
          <Icon icon={Volume2} size={18} strokeWidth={2} />
        )}
        {isThisPlaying ? "Stop" : "Hear it"}
      </button>
    </section>
  );
}

export default PassageReader;
