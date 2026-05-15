"use client";

import { useToast } from "@/components/Toast";
import type { Vibe } from "@/lib/personalization-types";

interface VibePickerProps {
  vibes: Vibe[];
  selectedId: string;
  onSelect: (id: string) => void;
}

/**
 * One small preview tile per vibe. The tile applies the vibe's
 * token bag as CSS variables on the swatch so the kid sees a
 * real flavor of the vibe (page bg + a mock activity card on the
 * surface) without needing to commit. Unavailable vibes dim with
 * a lock badge.
 */
export function VibePicker({ vibes, selectedId, onSelect }: VibePickerProps) {
  const { toast } = useToast();
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3" role="radiogroup" aria-label="Choose a vibe">
      {vibes.map((v) => {
        const isSelected = selectedId === v.id;
        const isLocked = !v.available;
        return (
          <button
            key={v.id}
            type="button"
            role="radio"
            aria-checked={isSelected}
            disabled={isLocked}
            onClick={() => {
              if (isLocked) {
                toast("Ask your parent to enable this", "info");
                return;
              }
              onSelect(v.id);
            }}
            className={[
              "relative rounded-2xl border min-h-[44px] overflow-hidden text-left",
              "transition-shadow duration-150",
              isSelected
                ? "ring-2 ring-(--color-brand-gold) border-(--color-brand-gold)"
                : "border-(--color-border) hover:border-(--color-border-strong)",
              isLocked ? "opacity-50 cursor-not-allowed" : "",
            ].join(" ")}
          >
            <div
              className="relative h-[100px] p-3 flex flex-col gap-2"
              style={{ ...(v.tokens as React.CSSProperties), background: v.tokens["--color-page"] }}
            >
              {/* Stripe of accent color sets the vibe's character. */}
              <div className="h-1.5 w-10 rounded-full" style={{ background: v.tokens["--color-accent"] }} />
              {/* Mocked activity card on the surface. */}
              <div
                className="mt-auto rounded-[10px] px-2.5 py-1.5"
                style={{ background: v.tokens["--color-surface"], borderRadius: v.tokens["--radius-card"] }}
              >
                <div className="h-1.5 w-12 rounded-full" style={{ background: v.tokens["--color-text-secondary"], opacity: 0.55 }} />
                <div className="mt-1 h-1.5 w-8 rounded-full" style={{ background: v.tokens["--color-text-secondary"], opacity: 0.3 }} />
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
            <div className="px-3 py-2 bg-(--color-surface)">
              <div className="text-sm font-semibold text-(--color-text)">{v.label}</div>
              <div className="text-[11px] text-(--color-text-tertiary) line-clamp-1">{v.description}</div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
