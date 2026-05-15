"use client";

import { useMemo, useState } from "react";

import { useToast } from "@/components/Toast";
import type { InterestTag } from "@/lib/personalization-types";

interface InterestChipsProps {
  tags: InterestTag[];
  selectedIds: string[];
  maxCount: number;
  onChange: (next: string[]) => void;
}

const CATEGORY_LABELS: Record<string, string> = {
  nature_animals: "Nature and animals",
  space_science: "Space and science",
  vehicles: "Vehicles",
  sports_movement: "Sports and movement",
  arts_music: "Arts and music",
  fantasy_history: "Fantasy and history",
  building_making: "Building and making",
  food_cooking: "Food and cooking",
  everyday_world: "Everyday world",
};

/**
 * Chip grid grouped by category. Live counter on top, max-count
 * enforced with a brief shake on overflow taps. Unavailable tags
 * are dimmed and non-tappable.
 *
 * Icons are deferred to a future iteration; for now each chip
 * shows a leading capital letter from the icon_keyword so the
 * visual rhythm is preserved without shipping 49 SVGs in this
 * prompt.
 */
export function InterestChips({ tags, selectedIds, maxCount, onChange }: InterestChipsProps) {
  const { toast } = useToast();
  const [shakeId, setShakeId] = useState<string | null>(null);
  const grouped = useMemo(() => {
    const byCat = new Map<string, InterestTag[]>();
    for (const t of tags) {
      const list = byCat.get(t.category) ?? [];
      list.push(t);
      byCat.set(t.category, list);
    }
    return Array.from(byCat.entries());
  }, [tags]);

  const selected = new Set(selectedIds);

  function toggle(tag: InterestTag) {
    if (!tag.available) {
      toast("Ask your parent to enable this", "info");
      return;
    }
    if (selected.has(tag.id)) {
      onChange(selectedIds.filter((id) => id !== tag.id));
      return;
    }
    if (selected.size >= maxCount) {
      setShakeId(tag.id);
      window.setTimeout(() => setShakeId((s) => (s === tag.id ? null : s)), 350);
      toast(`You can pick up to ${maxCount}`, "info");
      return;
    }
    onChange([...selectedIds, tag.id]);
  }

  return (
    <div className="space-y-5">
      <div className="flex items-baseline justify-between">
        <p className="text-xs uppercase tracking-[0.06em] text-(--color-text-tertiary)">Your picks</p>
        <p className="text-sm font-medium tabular-nums text-(--color-text)">
          {selected.size} / {maxCount}
        </p>
      </div>

      {grouped.map(([cat, items]) => (
        <div key={cat}>
          <h4 className="text-[11px] font-semibold uppercase tracking-[0.08em] text-(--color-text-secondary) mb-2">
            {CATEGORY_LABELS[cat] ?? cat.replace(/_/g, " ")}
          </h4>
          <div className="flex flex-wrap gap-2">
            {items.map((tag) => {
              const isSel = selected.has(tag.id);
              const isLocked = !tag.available;
              const initial = tag.icon_keyword.charAt(0).toUpperCase();
              return (
                <button
                  key={tag.id}
                  type="button"
                  aria-pressed={isSel}
                  disabled={isLocked}
                  onClick={() => toggle(tag)}
                  className={[
                    "inline-flex items-center gap-2 px-3 py-2 rounded-full border min-h-[44px] sm:min-h-0 sm:py-1.5",
                    "text-sm transition-colors",
                    isSel
                      ? "bg-(--color-accent) text-white border-(--color-accent)"
                      : "bg-(--color-surface) text-(--color-text) border-(--color-border) hover:border-(--color-border-strong)",
                    isLocked ? "opacity-40 cursor-not-allowed" : "",
                    shakeId === tag.id ? "animate-shake" : "",
                  ].join(" ")}
                >
                  <span
                    aria-hidden="true"
                    className={[
                      "inline-flex items-center justify-center w-5 h-5 rounded-full text-[10px] font-bold",
                      isSel ? "bg-white/20 text-white" : "bg-(--color-page) text-(--color-text-secondary)",
                    ].join(" ")}
                  >
                    {initial}
                  </span>
                  {tag.label}
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
