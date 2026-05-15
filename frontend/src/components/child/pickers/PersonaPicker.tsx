"use client";

import { useState } from "react";

import { CompanionAvatar } from "@/components/CompanionAvatar";
import { useToast } from "@/components/Toast";
import type { VoicePersona } from "@/lib/personalization-types";

interface PersonaPickerProps {
  personas: VoicePersona[];
  selectedId: string;
  onSelect: (id: string) => void;
}

/**
 * Five voice personas in a 2x3 grid (six slots with one empty on
 * five-persona libraries). Each tile shows the avatar, the label,
 * and the one-line tone summary. Unavailable personas dim with a
 * lock badge and a toast on tap so the kid knows to ask a parent.
 */
export function PersonaPicker({ personas, selectedId, onSelect }: PersonaPickerProps) {
  const { toast } = useToast();
  const [shakeId, setShakeId] = useState<string | null>(null);

  function nudge(id: string) {
    setShakeId(id);
    window.setTimeout(() => setShakeId((s) => (s === id ? null : s)), 350);
  }

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3" role="radiogroup" aria-label="Choose a study buddy">
      {personas.map((p) => {
        const isSelected = selectedId === p.id;
        const isLocked = !p.available;
        return (
          <button
            key={p.id}
            type="button"
            role="radio"
            aria-checked={isSelected}
            disabled={isLocked}
            onClick={() => {
              if (isLocked) {
                toast("Ask your parent to enable this", "info");
                nudge(p.id);
                return;
              }
              onSelect(p.id);
            }}
            className={[
              "relative rounded-2xl border bg-(--color-surface) p-4 text-left min-h-[44px]",
              "transition-shadow duration-150",
              isSelected
                ? "ring-2 ring-(--color-brand-gold) border-(--color-brand-gold)"
                : "border-(--color-border) hover:border-(--color-border-strong)",
              isLocked ? "opacity-50 cursor-not-allowed" : "",
              shakeId === p.id ? "animate-shake" : "",
            ].join(" ")}
          >
            <div className="flex items-center gap-3 text-(--color-accent)">
              <CompanionAvatar personaId={p.id} size={48} />
              <div className="min-w-0 flex-1">
                <div className="text-sm font-semibold text-(--color-text)">{p.label}</div>
                <div className="text-[11px] text-(--color-text-tertiary)">
                  {p.default_companion_name}
                </div>
              </div>
              {isLocked && (
                <span aria-hidden="true" className="absolute top-2 right-2 text-(--color-text-tertiary)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <rect x="5" y="11" width="14" height="9" rx="2" />
                    <path d="M8 11V8a4 4 0 0 1 8 0v3" />
                  </svg>
                </span>
              )}
            </div>
            <p className="text-xs text-(--color-text-secondary) mt-2 line-clamp-2 leading-snug">
              {p.tone_summary}
            </p>
          </button>
        );
      })}
    </div>
  );
}
