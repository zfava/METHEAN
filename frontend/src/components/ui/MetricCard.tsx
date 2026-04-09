"use client";

import { cn } from "@/lib/cn";

export default function MetricCard({
  label,
  value,
  subtitle,
  color,
  className,
}: {
  label: string;
  value: string | number;
  subtitle?: string;
  color?: string;
  className?: string;
}) {
  return (
    <div className={cn(
      "bg-(--color-surface) rounded-[14px] border border-(--color-border) p-5",
      "shadow-[var(--shadow-card)]",
      className
    )}>
      <div className="text-xs text-(--color-text-tertiary) uppercase tracking-wide mb-2">{label}</div>
      <div className={cn("text-[22px] sm:text-[28px] font-semibold tracking-tight", color || "text-(--color-text)")}>{value}</div>
      {subtitle && <div className="text-[13px] text-(--color-text-secondary) mt-1">{subtitle}</div>}
    </div>
  );
}
