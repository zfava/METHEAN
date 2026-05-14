"use client";

import { TonePicker } from "@/components/child/pickers/TonePicker";
import type { AffirmationTone } from "@/lib/personalization-types";

interface StepToneProps {
  tones: AffirmationTone[];
  selectedId: string;
  onSelect: (id: string) => void;
  onContinue: () => void;
}

export function StepTone({ tones, selectedId, onSelect, onContinue }: StepToneProps) {
  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">
          How should your buddy talk to you?
        </h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          You can change this anytime.
        </p>
      </header>

      <TonePicker tones={tones} selectedId={selectedId} onSelect={onSelect} />

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
