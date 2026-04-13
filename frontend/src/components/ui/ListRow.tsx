"use client";

import { cn } from "@/lib/cn";

export default function ListRow({
  children,
  actions,
  className,
  borderBottom = true,
}: {
  children: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
  borderBottom?: boolean;
}) {
  return (
    <div className={cn(
      "flex items-center justify-between py-3 px-5 press-scale",
      borderBottom && "border-b border-(--color-border)/50 last:border-0",
      className,
    )}>
      <div className="flex-1 min-w-0">{children}</div>
      {actions && <div className="shrink-0 ml-3">{actions}</div>}
    </div>
  );
}
