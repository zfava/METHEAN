"use client";

import { cn } from "@/lib/cn";

const variants = {
  primary: "bg-(--color-accent) text-white hover:bg-(--color-accent-hover) shadow-sm",
  secondary: "bg-(--color-surface) text-(--color-text) border border-(--color-border) hover:bg-(--color-page) hover:border-(--color-border-strong)",
  ghost: "text-(--color-text-secondary) hover:text-(--color-text) hover:bg-(--color-accent-light)",
  danger: "bg-(--color-surface) text-(--color-danger) border border-(--color-danger)/20 hover:bg-(--color-danger-light)",
  success: "bg-(--color-success) text-white hover:opacity-90 shadow-sm",
  gold: "bg-(--gold) text-white hover:opacity-90 shadow-sm",
};

const sizes = {
  sm: "px-3 py-1.5 text-[13px]",
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
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-[10px] font-medium",
        "transition-all duration-200 active:scale-[0.97]",
        "disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none",
        variants[variant],
        sizes[size],
        className,
      )}
    >
      {children}
    </button>
  );
}
