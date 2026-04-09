"use client";

import { cn } from "@/lib/cn";

export default function Card({
  children,
  className,
  padding = "p-4 sm:p-5",
  onClick,
  href,
  selected,
  borderLeft,
  animate,
}: {
  children: React.ReactNode;
  className?: string;
  padding?: string;
  onClick?: () => void;
  href?: string;
  selected?: boolean;
  borderLeft?: string;
  animate?: boolean;
}) {
  const base = cn(
    "bg-(--color-surface) rounded-[14px] border border-(--color-border)",
    "shadow-[var(--shadow-card)]",
    "transition-all duration-200 ease-[cubic-bezier(0.25,0.1,0.25,1)]",
    padding,
    borderLeft && `border-l-[3px] ${borderLeft}`,
    selected && "border-(--color-accent) ring-2 ring-(--color-accent)/15",
    (onClick || href) && "cursor-pointer hover:shadow-[var(--shadow-card-hover)] hover:-translate-y-[1px]",
    animate && "animate-fade-up",
    className,
  );

  if (href) return <a href={href} className={base}>{children}</a>;
  if (onClick) {
    return (
      <button
        onClick={onClick}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onClick(); } }}
        className={cn(base, "text-left w-full")}
      >
        {children}
      </button>
    );
  }
  return <div className={base}>{children}</div>;
}
