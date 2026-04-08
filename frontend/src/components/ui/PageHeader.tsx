"use client";

import { cn } from "@/lib/cn";

export default function PageHeader({
  title,
  subtitle,
  actions,
  backHref,
  className,
}: {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  backHref?: string;
  className?: string;
}) {
  return (
    <div className={cn("flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between mb-6", className)}>
      <div className="flex items-center gap-3">
        {backHref && (
          <a href={backHref} className="text-(--color-text-tertiary) hover:text-(--color-text-secondary) transition-colors duration-150">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M10 13l-5-5 5-5" stroke="currentColor" strokeWidth="1.5" fill="none"/></svg>
          </a>
        )}
        <div>
          <h1 className="text-[28px] font-semibold tracking-[-0.025em] text-(--color-text)">{title}</h1>
          {subtitle && <p className="text-[15px] text-(--color-text-secondary) mt-1">{subtitle}</p>}
        </div>
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}
