"use client";

import { useState } from "react";

import { Clock } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

interface Props {
  remainingInputMinutes: number | null;
  remainingOutputMinutes: number | null;
}

/**
 * Compact "minutes left today" badge in the top-right of voice mode.
 * Tap to expand into a small popover showing the input and output
 * breakdown. Falls back gracefully when either value is unknown.
 */
export function VoiceModeMinutesIndicator({
  remainingInputMinutes,
  remainingOutputMinutes,
}: Props) {
  const [open, setOpen] = useState(false);
  if (remainingInputMinutes === null && remainingOutputMinutes === null) return null;
  const compact =
    remainingInputMinutes !== null ? `${remainingInputMinutes} min` : "--";
  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] rounded-full bg-(--color-page) border border-(--color-border) text-(--color-text-secondary) min-h-[36px]"
        aria-expanded={open}
        aria-label={`Voice time left: ${compact}`}
      >
        <Icon icon={Clock} size={12} strokeWidth={2} />
        {compact}
      </button>
      {open && (
        <div
          role="dialog"
          aria-label="Voice time breakdown"
          className="absolute right-0 top-full mt-2 z-50 w-48 rounded-2xl border border-(--color-border) bg-(--color-surface) shadow-[var(--shadow-card)] p-3 text-xs"
        >
          <div className="flex items-center justify-between">
            <span className="text-(--color-text-secondary)">Talking</span>
            <span className="font-medium tabular-nums text-(--color-text)">
              {remainingInputMinutes ?? "--"} min
            </span>
          </div>
          <div className="flex items-center justify-between mt-1.5">
            <span className="text-(--color-text-secondary)">Listening</span>
            <span className="font-medium tabular-nums text-(--color-text)">
              {remainingOutputMinutes ?? "--"} min
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

export default VoiceModeMinutesIndicator;
