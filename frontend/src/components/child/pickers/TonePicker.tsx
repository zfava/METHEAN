"use client";

import { useToast } from "@/components/Toast";
import type { AffirmationTone } from "@/lib/personalization-types";

interface TonePickerProps {
  tones: AffirmationTone[];
  selectedId: string;
  onSelect: (id: string) => void;
}

// Hardcoded for Part 1; replaced by a live AI sample in a future
// iteration. Indexed by the tone library id.
const SAMPLE_LINES: Record<string, string> = {
  warm: "Solid work. I can tell you're getting this.",
  direct: "Correct. Next one.",
  playful: "Nailed it. Onward, captain.",
};

export function TonePicker({ tones, selectedId, onSelect }: TonePickerProps) {
  const { toast } = useToast();
  return (
    <div className="space-y-2" role="radiogroup" aria-label="Choose a tone">
      {tones.map((tone) => {
        const isSelected = selectedId === tone.id;
        const isLocked = !tone.available;
        const sample = SAMPLE_LINES[tone.id] ?? tone.tone_summary;
        return (
          <button
            key={tone.id}
            type="button"
            role="radio"
            aria-checked={isSelected}
            disabled={isLocked}
            onClick={() => {
              if (isLocked) {
                toast("Ask your parent to enable this", "info");
                return;
              }
              onSelect(tone.id);
            }}
            className={[
              "w-full text-left rounded-2xl border bg-(--color-surface) p-4 min-h-[44px]",
              "transition-shadow duration-150",
              isSelected
                ? "ring-2 ring-(--color-brand-gold) border-(--color-brand-gold)"
                : "border-(--color-border) hover:border-(--color-border-strong)",
              isLocked ? "opacity-50 cursor-not-allowed" : "",
            ].join(" ")}
          >
            <div className="flex items-baseline justify-between gap-2">
              <div className="text-sm font-semibold text-(--color-text)">{tone.label}</div>
              {isSelected && (
                <span className="text-xs font-medium text-(--color-brand-gold-text)" aria-hidden="true">
                  Picked
                </span>
              )}
            </div>
            <p className="mt-2 text-sm text-(--color-text) italic leading-relaxed">
              &ldquo;{sample}&rdquo;
            </p>
            <p className="text-[11px] text-(--color-text-tertiary) mt-1.5 line-clamp-2">{tone.tone_summary}</p>
          </button>
        );
      })}
    </div>
  );
}
