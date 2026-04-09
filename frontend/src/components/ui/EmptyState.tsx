"use client";

import { cn } from "@/lib/cn";

function CheckIcon() {
  return (
    <svg className="w-10 h-10" viewBox="0 0 40 40" fill="none">
      {/* Celebration burst lines */}
      <line x1="20" y1="4" x2="20" y2="8" stroke="var(--color-success)" strokeWidth="1.5" strokeLinecap="round" opacity="0.5" />
      <line x1="30" y1="8" x2="28" y2="11" stroke="var(--color-success)" strokeWidth="1.5" strokeLinecap="round" opacity="0.4" />
      <line x1="10" y1="8" x2="12" y2="11" stroke="var(--color-success)" strokeWidth="1.5" strokeLinecap="round" opacity="0.4" />
      {/* Circle */}
      <circle cx="20" cy="22" r="11" stroke="var(--color-success)" strokeWidth="1.5" fill="var(--color-success-light)" />
      {/* Checkmark */}
      <path d="M14 22l4 4 8-8" stroke="var(--color-success)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

function EmptyIcon() {
  return (
    <svg className="w-10 h-10" viewBox="0 0 40 40" fill="none">
      {/* Book spine */}
      <path d="M8 10c0-2 2-4 6-4h12c4 0 6 2 6 4v20c0 2-2 4-6 4H14c-4 0-6-2-6-4V10z"
        stroke="var(--color-text-tertiary)" strokeWidth="1.5" fill="none" />
      {/* Pages */}
      <path d="M14 10v20" stroke="var(--color-border-strong)" strokeWidth="1" />
      {/* Lines on page */}
      <line x1="18" y1="14" x2="28" y2="14" stroke="var(--color-border)" strokeWidth="1" strokeLinecap="round" />
      <line x1="18" y1="18" x2="26" y2="18" stroke="var(--color-border)" strokeWidth="1" strokeLinecap="round" />
      <line x1="18" y1="22" x2="24" y2="22" stroke="var(--color-border)" strokeWidth="1" strokeLinecap="round" />
      {/* Open book spread */}
      <path d="M4 12c2-1 4-1 6 0" stroke="var(--color-text-tertiary)" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />
      <path d="M36 12c-2-1-4-1-6 0" stroke="var(--color-text-tertiary)" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg className="w-10 h-10" viewBox="0 0 40 40" fill="none">
      {/* Magnifying glass circle */}
      <circle cx="18" cy="18" r="10" stroke="var(--color-accent)" strokeWidth="1.5" fill="var(--color-accent-light)" />
      {/* Handle */}
      <line x1="25" y1="25" x2="34" y2="34" stroke="var(--color-accent)" strokeWidth="2" strokeLinecap="round" />
      {/* Question mark inside */}
      <path d="M15 15c0-2.5 2-3.5 3.5-3.5s3 1.5 3 3c0 1.5-1.5 2-2.5 2.5" stroke="var(--color-accent)" strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <circle cx="18.5" cy="21.5" r="0.8" fill="var(--color-accent)" />
    </svg>
  );
}

export default function EmptyState({
  title,
  description,
  action,
  onAction,
  icon,
  className,
}: {
  title: string;
  description?: string;
  action?: string | React.ReactNode;
  onAction?: () => void;
  icon?: "check" | "empty" | "search";
  className?: string;
}) {
  const icons = {
    check: <CheckIcon />,
    empty: <EmptyIcon />,
    search: <SearchIcon />,
  };

  return (
    <div role="status" className={cn("bg-(--color-surface) rounded-[14px] border border-(--color-border) py-12 px-6 text-center", className)}>
      {icon && (
        <div className="flex justify-center mb-4 animate-scale-in">
          <div className="w-14 h-14 rounded-full bg-(--color-page) border border-(--color-border) flex items-center justify-center">
            {icons[icon]}
          </div>
        </div>
      )}
      <div className="animate-fade-up" style={{ animationDelay: "100ms" }}>
        <h3 className="text-sm font-medium text-(--color-text)">{title}</h3>
        {description && <p className="text-xs text-(--color-text-secondary) mt-1 max-w-sm mx-auto">{description}</p>}
      </div>
      {action && typeof action === "string" && onAction && (
        <div className="animate-fade-up" style={{ animationDelay: "200ms" }}>
          <button onClick={onAction} className="mt-4 px-4 py-1.5 text-xs font-medium text-(--color-accent) border border-(--color-accent)/30 rounded-[10px] hover:bg-(--color-accent-light) transition-colors duration-150">
            {action}
          </button>
        </div>
      )}
      {action && typeof action !== "string" && (
        <div className="mt-4 animate-fade-up" style={{ animationDelay: "200ms" }}>
          {action}
        </div>
      )}
    </div>
  );
}
