"use client";

import { VibePicker } from "@/components/child/pickers/VibePicker";
import type { Vibe } from "@/lib/personalization-types";

interface StepVibeProps {
  vibes: Vibe[];
  selectedId: string;
  onSelect: (id: string) => void;
  onContinue: () => void;
}

export function StepVibe({ vibes, selectedId, onSelect, onContinue }: StepVibeProps) {
  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">Pick your vibe.</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          This is how the whole app will look and feel.
        </p>
      </header>

      <VibePicker vibes={vibes} selectedId={selectedId} onSelect={onSelect} />

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
