"use client";

import { Lock } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

export function PermissionDeniedNotice() {
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] rounded-full bg-(--color-danger-light) text-(--color-danger)"
      role="status"
    >
      <Icon icon={Lock} size={12} strokeWidth={2} />
      We need mic permission. Open your browser settings to allow it.
    </span>
  );
}

export default PermissionDeniedNotice;
