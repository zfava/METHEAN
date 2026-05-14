"use client";

import { ActivityIcon, type ActivityType } from "@/components/ActivityIcon";
import { useToast } from "@/components/Toast";
import type { IconographyPack } from "@/lib/personalization-types";

interface IconographyPickerProps {
  packs: IconographyPack[];
  selectedId: string;
  onSelect: (id: string) => void;
}

const PREVIEW_ORDER: ActivityType[] = ["lesson", "practice", "review", "assessment", "project", "field_trip"];

/**
 * Each row shows the pack's six activity icons inline followed by
 * the label. Tapping selects. Locked packs dim and toast.
 */
export function IconographyPicker({ packs, selectedId, onSelect }: IconographyPickerProps) {
  const { toast } = useToast();
  return (
    <div className="space-y-2" role="radiogroup" aria-label="Choose an icon style">
      {packs.map((pack) => {
        const isSelected = selectedId === pack.id;
        const isLocked = !pack.available;
        return (
          <button
            key={pack.id}
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
            className={[
              "w-full flex items-center gap-3 px-4 py-3 rounded-2xl border min-h-[44px] bg-(--color-surface) text-left",
              "transition-shadow duration-150",
              isSelected
                ? "ring-2 ring-(--color-brand-gold) border-(--color-brand-gold)"
                : "border-(--color-border) hover:border-(--color-border-strong)",
              isLocked ? "opacity-50 cursor-not-allowed" : "",
            ].join(" ")}
          >
            <div className="flex items-center gap-2 text-(--color-text-secondary)">
              {PREVIEW_ORDER.map((t) => (
                <ActivityIcon key={t} type={t} packOverride={pack.id} size={20} />
              ))}
            </div>
            <div className="ml-auto text-right">
              <div className="text-sm font-semibold text-(--color-text)">{pack.label}</div>
              <div className="text-[11px] text-(--color-text-tertiary) line-clamp-1">{pack.description}</div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
