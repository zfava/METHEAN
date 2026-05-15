"use client";

import { useState } from "react";

import { InterestChips } from "@/components/child/pickers/InterestChips";
import type { InterestTag } from "@/lib/personalization-types";

interface StepInterestsProps {
  tags: InterestTag[];
  maxCount: number;
  initialSelected: string[];
  onContinue: (selected: string[]) => void;
}

export function StepInterests({ tags, maxCount, initialSelected, onContinue }: StepInterestsProps) {
  const [selected, setSelected] = useState<string[]>(initialSelected);

  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">What are you into?</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">
          Pick up to {maxCount}. We&apos;ll use these to make learning more your style.
        </p>
      </header>

      <InterestChips
        tags={tags}
        selectedIds={selected}
        maxCount={maxCount}
        onChange={setSelected}
      />

      <button
        type="button"
        onClick={() => onContinue(selected)}
        className="w-full py-3.5 rounded-2xl bg-(--color-text) text-white font-semibold min-h-[44px]"
      >
        Continue
      </button>
    </div>
  );
}
