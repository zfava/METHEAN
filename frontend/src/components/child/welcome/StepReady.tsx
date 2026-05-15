"use client";

import { CompanionAvatar } from "@/components/CompanionAvatar";

interface StepReadyProps {
  companionName: string;
  companionVoice: string;
  onLaunch: () => void;
}

export function StepReady({ companionName, companionVoice, onLaunch }: StepReadyProps) {
  const name = companionName || "Your companion";
  return (
    <div className="space-y-6 text-center py-6">
      <div className="flex justify-center text-(--color-accent)">
        <CompanionAvatar personaId={companionVoice || "default_warm"} size={96} />
      </div>

      <header>
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">{name} is ready.</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          Let&apos;s go do today&apos;s learning.
        </p>
      </header>

      <button
        type="button"
        onClick={onLaunch}
        className="w-full py-4 rounded-2xl bg-(--color-accent) text-white text-lg font-semibold min-h-[44px]"
      >
        Let&apos;s go
      </button>
    </div>
  );
}
