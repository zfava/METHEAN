"use client";

import type { VoiceConversationStatus } from "@/lib/useVoiceConversation";

interface Props {
  status: VoiceConversationStatus;
  interactionStyle: "press_hold" | "tap_toggle";
}

const STATUS_COPY: Record<
  VoiceConversationStatus,
  (style: "press_hold" | "tap_toggle") => string
> = {
  idle: (style) => (style === "press_hold" ? "Press and hold to talk." : "Tap to talk."),
  listening: () => "I'm listening.",
  sending: () => "Sending what you said...",
  transcribing: () => "Catching up...",
  thinking: () => "Let me think.",
  speaking: () => "Speaking.",
  cap_input_reached: () => "Voice time is up for today.",
  cap_output_reached: () => "I can't speak right now, but I'm here.",
  permission_lost: () => "We lost mic access. Open browser settings to give it back.",
  network_lost: () => "Lost the connection. Tap to try again.",
  error: () => "Something went wrong. Tap to try again.",
};

export function VoiceModeStatusLine({ status, interactionStyle }: Props) {
  const copy = STATUS_COPY[status](interactionStyle);
  return (
    <p
      className="text-sm text-(--color-text-secondary) text-center"
      role="status"
      aria-live="polite"
    >
      {copy}
    </p>
  );
}

export default VoiceModeStatusLine;
