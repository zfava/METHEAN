"use client";

import { useEffect, useId, useState } from "react";

import { cn } from "@/lib/cn";

export type ProgressRingTone = "gold" | "accent" | "success" | "danger";

const TONE_TO_CSS_VAR: Record<ProgressRingTone, string> = {
  gold: "var(--color-brand-gold)",
  accent: "var(--color-accent)",
  success: "var(--color-success)",
  danger: "var(--color-danger)",
};

export default function ProgressRing({
  value,
  size = 96,
  strokeWidth = 8,
  tone = "accent",
  label,
  className,
  showPercent = true,
}: {
  /** 0-100. Values outside the range are clamped. */
  value: number;
  size?: number;
  strokeWidth?: number;
  tone?: ProgressRingTone;
  label?: string;
  className?: string;
  /** When true (default), render the value as a centered percentage. */
  showPercent?: boolean;
}) {
  const gradientId = useId();
  const clamped = Math.max(0, Math.min(100, value));

  // Animate stroke-dashoffset from 0% (full hidden) to the clamped
  // value on mount and whenever `value` changes. Holding the rendered
  // value in state lets the SVG transition handle the easing.
  const [rendered, setRendered] = useState(0);
  useEffect(() => {
    const raf = requestAnimationFrame(() => setRendered(clamped));
    return () => cancelAnimationFrame(raf);
  }, [clamped]);

  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (rendered / 100) * circumference;
  const stroke = TONE_TO_CSS_VAR[tone];

  return (
    <div
      className={cn("relative inline-flex items-center justify-center", className)}
      style={{ width: size, height: size }}
      role="progressbar"
      aria-valuenow={Math.round(clamped)}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={label ?? `${Math.round(clamped)} percent`}
    >
      <svg width={size} height={size} className="-rotate-90" aria-hidden="true">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={stroke} stopOpacity="0.85" />
            <stop offset="100%" stopColor={stroke} stopOpacity="1" />
          </linearGradient>
        </defs>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="var(--color-border)"
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#${gradientId})`}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.6s var(--ease)" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        {label !== undefined ? (
          <span className="text-[13px] font-medium tracking-tight text-(--color-text)">{label}</span>
        ) : showPercent ? (
          <span className="text-[18px] font-semibold tracking-tight text-(--color-text)">
            {Math.round(clamped)}%
          </span>
        ) : null}
      </div>
    </div>
  );
}
