"use client";

import { useCallback } from "react";

import { useToast } from "@/components/Toast";
import type { SoundPack } from "@/lib/personalization-types";

interface SoundPickerProps {
  packs: SoundPack[];
  selectedId: string;
  onSelect: (id: string) => void;
}

/**
 * Three cards (Off, Soft, Full). Non-off cards expose a "Hear
 * sample" button that plays the `correct` cue from that pack. The
 * sample uses a fresh Audio instance per tap so it sidesteps the
 * useSoundCue gating; the tap itself counts as the user gesture
 * the browser requires for autoplay.
 */
export function SoundPicker({ packs, selectedId, onSelect }: SoundPickerProps) {
  const { toast } = useToast();

  const playSample = useCallback((packId: string) => {
    if (packId === "off") return;
    try {
      const audio = new Audio(`/sounds/${packId}/correct.mp3`);
      audio.volume = 0.6;
      void audio.play().catch(() => {
        // Browser rejected the play (autoplay or device error).
        // The kid hasn't lost anything; just surface a hint.
        toast("Tap again to hear it", "info");
      });
    } catch {
      // Unsupported environment. No-op.
    }
  }, [toast]);

  return (
    <div className="space-y-2" role="radiogroup" aria-label="Choose sound level">
      {packs.map((pack) => {
        const isSelected = selectedId === pack.id;
        const isLocked = !pack.available;
        const isOff = pack.id === "off";
        return (
          <div
            key={pack.id}
            className={[
              "rounded-2xl border bg-(--color-surface) p-4",
              "transition-shadow duration-150",
              isSelected
                ? "ring-2 ring-(--color-brand-gold) border-(--color-brand-gold)"
                : "border-(--color-border)",
              isLocked ? "opacity-50" : "",
            ].join(" ")}
          >
            <button
              type="button"
              role="radio"
              aria-checked={isSelected}
              disabled={isLocked}
              onClick={() => {
                if (isLocked) {
                  toast("Ask your parent to enable this", "info");
                  return;
                }
                onSelect(pack.id);
              }}
              className="w-full text-left flex items-center gap-3 min-h-[44px] cursor-pointer disabled:cursor-not-allowed"
            >
              <div className="flex-1 min-w-0">
                <div className="text-sm font-semibold text-(--color-text)">{pack.label}</div>
                <div className="text-[11px] text-(--color-text-tertiary) line-clamp-1">
                  {pack.description}
                </div>
              </div>
              {isSelected && (
                <span className="text-xs font-medium text-(--color-brand-gold-text)" aria-hidden="true">
                  Picked
                </span>
              )}
            </button>
            {!isOff && (
              <div className="mt-3 flex items-center justify-end">
                <button
                  type="button"
                  onClick={() => playSample(pack.id)}
                  disabled={isLocked}
                  className="text-xs font-medium text-(--color-accent) hover:underline min-h-[36px] px-2"
                >
                  Hear sample
                </button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
