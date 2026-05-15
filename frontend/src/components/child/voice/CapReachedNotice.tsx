"use client";

export function CapReachedNotice() {
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] rounded-full bg-(--color-warning-light) text-(--color-warning)"
      role="status"
    >
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
      Voice time is up for today. You can still type.
    </span>
  );
}

export default CapReachedNotice;
