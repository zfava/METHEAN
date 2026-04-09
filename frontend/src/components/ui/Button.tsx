"use client";

import { cn } from "@/lib/cn";

const variants = {
  primary: "bg-(--color-accent) text-white hover:bg-(--color-accent-hover) hover:shadow-md shadow-sm",
  secondary: "bg-(--color-surface) text-(--color-text) border border-(--color-border) hover:bg-(--color-page) hover:border-(--color-border-strong)",
  ghost: "text-(--color-text-secondary) hover:text-(--color-text) hover:bg-(--color-accent-light)",
  danger: "bg-(--color-surface) text-(--color-danger) border border-(--color-danger)/20 hover:bg-(--color-danger-light)",
  success: "bg-(--color-success) text-white hover:opacity-90 hover:shadow-md shadow-sm",
  gold: "bg-(--gold) text-white hover:opacity-90 hover:shadow-md shadow-sm",
};

const sizes = {
  sm: "px-3 py-1.5 text-[13px] min-h-[44px] sm:min-h-0",
  md: "px-5 py-2.5 text-[14px]",
  lg: "px-7 py-3 text-[15px]",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  className,
  disabled,
  onClick,
  type = "button",
}: {
  children: React.ReactNode;
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
  className?: string;
  disabled?: boolean;
  onClick?: () => void;
  type?: "button" | "submit";
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled || undefined}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-[10px] font-medium",
        "transition-all duration-150 active:scale-[0.97] active:shadow-none",
        "disabled:opacity-40 disabled:saturate-50 disabled:cursor-not-allowed disabled:pointer-events-none",
        "focus-visible:ring-2 focus-visible:ring-(--color-accent)/30 focus-visible:ring-offset-2",
        variants[variant],
        sizes[size],
        className,
      )}
    >
      {children}
    </button>
  );
}
