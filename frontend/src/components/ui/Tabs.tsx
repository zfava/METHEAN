"use client";

import { cn } from "@/lib/cn";

export default function Tabs<T extends string>({
  tabs,
  active,
  onChange,
  className,
}: {
  tabs: { key: T; label: string }[];
  active: T;
  onChange: (key: T) => void;
  className?: string;
}) {
  return (
    <div className={cn("flex gap-1 p-1 bg-(--color-page) rounded-lg border border-(--color-border)", className)}>
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={cn(
            "px-4 py-1.5 text-sm rounded-md transition-colors duration-150",
            active === tab.key
              ? "bg-(--color-surface) text-(--color-text) font-medium shadow-sm"
              : "text-(--color-text-secondary) hover:text-(--color-text)",
          )}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
