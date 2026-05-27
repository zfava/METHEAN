"use client";

import { cn } from "@/lib/cn";
import { ChevronLeft } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

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
          <a href={backHref} className="text-(--color-text-tertiary) hover:text-(--color-text-secondary) transition-colors duration-150" aria-label="Back">
            <Icon icon={ChevronLeft} size={16} />
          </a>
        )}
        <div>
          <h1 className="type-heading-lg text-(--color-text)">{title}</h1>
          {subtitle && <p className="type-body-md text-(--color-text-secondary) mt-1">{subtitle}</p>}
        </div>
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}
