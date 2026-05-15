"use client";

import { IconographyPicker } from "@/components/child/pickers/IconographyPicker";
import type { IconographyPack } from "@/lib/personalization-types";

interface StepIconographyProps {
  packs: IconographyPack[];
  selectedId: string;
  onSelect: (id: string) => void;
  onContinue: () => void;
}

export function StepIconography({ packs, selectedId, onSelect, onContinue }: StepIconographyProps) {
  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">Pick your icon style.</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          The little symbols on each activity.
        </p>
      </header>

      <IconographyPicker packs={packs} selectedId={selectedId} onSelect={onSelect} />

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
