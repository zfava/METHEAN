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
      <div className="type-eyebrow-md text-(--color-text-tertiary) mb-2">{label}</div>
      <div className={cn("type-heading-lg", color || "text-(--color-text)")}>{value}</div>
      {subtitle && <div className="type-body-sm text-(--color-text-secondary) mt-1">{subtitle}</div>}
    </div>
  );
}
