"use client";

import { cn } from "@/lib/cn";

export type BadgeVariant =
  | "mastered"
  | "progressing"
  | "blocked"
  | "danger"
  | "constitutional"
  | "info";

const VARIANT_STYLES: Record<
  BadgeVariant,
  { text: string; bg: string; dot: string }
> = {
  mastered: {
    text: "text-(--color-mastered)",
    bg: "bg-(--color-success-light)",
    dot: "bg-(--color-mastered)",
  },
  progressing: {
    text: "text-(--color-brand-gold-text)",
    bg: "bg-(--color-warning-light)",
    dot: "bg-(--color-progress)",
  },
  blocked: {
    text: "text-(--color-text-secondary)",
    bg: "bg-[rgba(0,0,0,0.04)]",
    dot: "bg-(--color-blocked)",
  },
  danger: {
    text: "text-(--color-danger)",
    bg: "bg-(--color-danger-light)",
    dot: "bg-(--color-danger)",
  },
  constitutional: {
    text: "text-(--color-constitutional)",
    bg: "bg-(--color-constitutional-light)",
    dot: "bg-(--color-constitutional)",
  },
  info: {
    text: "text-(--color-info)",
    bg: "bg-(--color-accent-light)",
    dot: "bg-(--color-accent)",
  },
};

export default function Badge({
  variant = "info",
  children,
  className,
  withDot = true,
}: {
  variant?: BadgeVariant;
  children: React.ReactNode;
  className?: string;
  withDot?: boolean;
}) {
  const styles = VARIANT_STYLES[variant];
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-[6px] px-2 py-0.5",
        "text-[12px] font-medium leading-none",
        styles.text,
        styles.bg,
        className,
      )}
    >
      {withDot && (
        <span
          aria-hidden="true"
          className={cn("h-1.5 w-1.5 rounded-full shrink-0", styles.dot)}
        />
      )}
      {children}
    </span>
  );
}
