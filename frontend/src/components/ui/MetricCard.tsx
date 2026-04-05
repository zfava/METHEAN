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
  color?: string; // text color class
  className?: string;
}) {
  return (
    <div className={cn("bg-(--color-surface) rounded-[10px] border border-(--color-border) p-4", className)}>
      <div className={cn("text-2xl font-medium tracking-tight", color || "text-(--color-text)")}>{value}</div>
      <div className="text-xs text-(--color-text-secondary) mt-1">{label}</div>
      {subtitle && <div className="text-[11px] text-(--color-text-tertiary) mt-0.5">{subtitle}</div>}
    </div>
  );
}
