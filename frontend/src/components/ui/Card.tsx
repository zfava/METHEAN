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
}: {
  children: React.ReactNode;
  className?: string;
  padding?: string;
  onClick?: () => void;
  href?: string;
  selected?: boolean;
  borderLeft?: string;
}) {
  const base = cn(
    "bg-(--color-surface) rounded-[14px] border border-(--color-border)",
    "shadow-[var(--shadow-card)]",
    "transition-all duration-200",
    padding,
    borderLeft && `border-l-[3px] ${borderLeft}`,
    selected && "border-(--color-accent) ring-2 ring-(--color-accent)/15",
    (onClick || href) && "cursor-pointer hover:shadow-[var(--shadow-card-hover)] hover:-translate-y-[1px]",
    className,
  );

  if (href) return <a href={href} className={base}>{children}</a>;
  if (onClick) return <button onClick={onClick} className={cn(base, "text-left w-full")}>{children}</button>;
  return <div className={base}>{children}</div>;
}
