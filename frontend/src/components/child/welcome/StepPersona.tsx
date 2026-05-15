"use client";

import { PersonaPicker } from "@/components/child/pickers/PersonaPicker";
import type { VoicePersona } from "@/lib/personalization-types";

interface StepPersonaProps {
  personas: VoicePersona[];
  selectedId: string;
  onSelect: (id: string) => void;
  onContinue: () => void;
}

export function StepPersona({ personas, selectedId, onSelect, onContinue }: StepPersonaProps) {
  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">Pick your study buddy.</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          They&apos;ll help you when you get stuck.
        </p>
      </header>

      <PersonaPicker personas={personas} selectedId={selectedId} onSelect={onSelect} />

      {selectedId && (
        <button
          type="button"
          onClick={onContinue}
          className="w-full py-3.5 rounded-2xl bg-(--color-text) text-white font-semibold min-h-[44px]"
        >
          Continue
        </button>
      )}
    </div>
  );
}
