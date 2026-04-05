"use client";

import { cn } from "@/lib/cn";

export default function Card({
  children,
  className,
  padding = "p-5",
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
  borderLeft?: string; // e.g. "border-l-(--color-success)" for status accent
}) {
  const base = cn(
    "bg-(--color-surface) rounded-[10px] border border-(--color-border)",
    padding,
    borderLeft && `border-l-[3px] ${borderLeft}`,
    selected && "border-(--color-accent) ring-1 ring-(--color-accent)/20",
    (onClick || href) && "cursor-pointer hover:border-(--color-border-strong) transition-colors duration-150",
    className,
  );

  if (href) return <a href={href} className={base}>{children}</a>;
  if (onClick) return <button onClick={onClick} className={cn(base, "text-left w-full")}>{children}</button>;
  return <div className={base}>{children}</div>;
}
