"use client";

import { cn } from "@/lib/cn";

const variants = {
  primary: "bg-(--color-accent) text-white hover:bg-(--color-accent-hover)",
  secondary: "bg-(--color-surface) text-(--color-text) border border-(--color-border) hover:bg-(--color-page)",
  ghost: "text-(--color-text-secondary) hover:text-(--color-text) hover:bg-(--color-page)",
  danger: "bg-(--color-danger) text-white hover:opacity-90",
  success: "bg-(--color-success) text-white hover:opacity-90",
};

const sizes = {
  sm: "px-3 py-1 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "px-6 py-2.5 text-sm font-medium",
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
        "rounded-[6px] font-medium transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none",
        variants[variant],
        sizes[size],
        className,
      )}
    >
      {children}
    </button>
  );
}
