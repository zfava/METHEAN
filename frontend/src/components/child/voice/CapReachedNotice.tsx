"use client";

import { Clock } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

export function CapReachedNotice() {
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] rounded-full bg-(--color-warning-light) text-(--color-warning)"
      role="status"
    >
      <Icon icon={Clock} size={12} strokeWidth={2} />
      Voice time is up for today. You can still type.
    </span>
  );
}

export default CapReachedNotice;
