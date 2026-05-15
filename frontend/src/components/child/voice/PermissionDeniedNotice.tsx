"use client";

export function PermissionDeniedNotice() {
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[11px] rounded-full bg-(--color-danger-light) text-(--color-danger)"
      role="status"
    >
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <rect x="5" y="11" width="14" height="9" rx="2" />
        <path d="M8 11V8a4 4 0 0 1 8 0v3" />
      </svg>
      We need mic permission. Open your browser settings to allow it.
    </span>
  );
}

export default PermissionDeniedNotice;
