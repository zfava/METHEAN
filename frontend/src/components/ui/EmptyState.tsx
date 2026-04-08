"use client";

import { cn } from "@/lib/cn";

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
  action?: string;
  onAction?: () => void;
  icon?: "check" | "empty" | "search";
  className?: string;
}) {
  const icons = {
    check: <div className="w-12 h-12 rounded-full bg-(--color-success-light) flex items-center justify-center mx-auto mb-3"><span className="text-(--color-success) text-lg">&#10003;</span></div>,
    empty: <div className="w-12 h-12 rounded-full bg-(--color-page) flex items-center justify-center mx-auto mb-3 border border-(--color-border)"><span className="text-(--color-text-tertiary) text-lg">&mdash;</span></div>,
    search: <div className="w-12 h-12 rounded-full bg-(--color-accent-light) flex items-center justify-center mx-auto mb-3"><span className="text-(--color-accent) text-lg">?</span></div>,
  };

  return (
    <div className={cn("bg-(--color-surface) rounded-[14px] border border-(--color-border) py-12 px-6 text-center", className)}>
      {icon && icons[icon]}
      <h3 className="text-sm font-medium text-(--color-text)">{title}</h3>
      {description && <p className="text-xs text-(--color-text-secondary) mt-1 max-w-sm mx-auto">{description}</p>}
      {action && onAction && (
        <button onClick={onAction} className="mt-4 px-4 py-1.5 text-xs font-medium text-(--color-accent) border border-(--color-accent)/30 rounded-[10px] hover:bg-(--color-accent-light) transition-colors duration-150">
          {action}
        </button>
      )}
    </div>
  );
}
