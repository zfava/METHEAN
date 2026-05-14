"use client";

import { SoundPicker } from "@/components/child/pickers/SoundPicker";
import type { SoundPack } from "@/lib/personalization-types";

interface StepSoundProps {
  packs: SoundPack[];
  selectedId: string;
  onSelect: (id: string) => void;
  onContinue: () => void;
}

export function StepSound({ packs, selectedId, onSelect, onContinue }: StepSoundProps) {
  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">How much sound?</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          Tap a card to pick. Tap &ldquo;Hear sample&rdquo; to listen.
        </p>
      </header>

      <SoundPicker packs={packs} selectedId={selectedId} onSelect={onSelect} />

      <button
        type="button"
        onClick={onContinue}
        className="w-full py-3.5 rounded-2xl bg-(--color-text) text-white font-semibold min-h-[44px]"
      >
        Continue
      </button>
    </div>
  );
}
