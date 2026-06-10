"use client";

import { cn } from "@/lib/cn";
import HashLine from "@/components/record/HashLine";

function ShieldIcon({ ok }: { ok: boolean }) {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z" />
      {ok ? <polyline points="9 12 11 14 15 10" /> : <><line x1="12" y1="8" x2="12" y2="13" /><line x1="12" y1="16" x2="12.01" y2="16" /></>}
    </svg>
  );
}

/**
 * Sealed-record integrity badge. Verified renders calm and
 * affirmative; a failed verification renders loud and unmissable.
 * That state should never occur, which is exactly why it must be
 * visible if it does.
 */
export default function IntegrityBadge({
  verified,
  headHash,
  eventCount,
}: {
  verified: boolean;
  headHash: string | null;
  eventCount: number;
}) {
  if (!verified) {
    return (
      <div
        data-testid="integrity-badge"
        data-verified="false"
        role="alert"
        className="flex items-center gap-3 px-4 py-3 rounded-[14px] bg-(--color-danger) text-white shadow-lg"
      >
        <ShieldIcon ok={false} />
        <div>
          <div className="text-sm font-semibold">Record integrity check failed</div>
          <div className="text-xs text-white/90">
            This record could not be verified against its sealed history. Contact METHEAN support before relying on it.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      data-testid="integrity-badge"
      data-verified="true"
      className={cn(
        "flex items-center gap-2.5 px-3 py-2 rounded-[14px]",
        "bg-(--color-success-light) border border-(--color-success)/25 text-(--color-mastered)",
      )}
    >
      <ShieldIcon ok />
      <div className="flex flex-col">
        <span className="text-xs font-semibold leading-tight">Sealed and verified</span>
        <span className="text-[10px] text-(--color-text-secondary) leading-tight">
          {eventCount} recorded {eventCount === 1 ? "decision" : "decisions"}
        </span>
      </div>
      {headHash && <HashLine value={headHash} label="seal" />}
    </div>
  );
}
