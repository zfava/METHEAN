"use client";

import { useState } from "react";
import { cn } from "@/lib/cn";

/**
 * Copyable monospace hash line. Shows a shortened prefix by default;
 * clicking copies the full value and confirms. This is the only place
 * raw hashes surface in the Record UI.
 */
export default function HashLine({
  value,
  chars = 12,
  label,
  className,
}: {
  value: string;
  chars?: number;
  label?: string;
  className?: string;
}) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      // Clipboard unavailable (permissions, http): show the value so
      // the parent can still select it by hand.
      setCopied(false);
    }
  }

  return (
    <button
      onClick={copy}
      title="Click to copy the full hash"
      data-testid="hash-line"
      data-full-hash={value}
      className={cn(
        "inline-flex items-center gap-1.5 font-mono text-[11px] px-2 py-1 rounded-[8px]",
        "bg-(--color-page) border border-(--color-border) text-(--color-text-secondary)",
        "hover:border-(--color-border-strong) hover:text-(--color-text) transition-colors",
        className,
      )}
    >
      {label && <span className="font-sans text-[10px] text-(--color-text-tertiary)">{label}</span>}
      <span>{value.slice(0, chars)}&hellip;</span>
      <span className={cn("font-sans text-[10px]", copied ? "text-(--color-success)" : "text-(--color-text-tertiary)")}>
        {copied ? "Copied" : "Copy"}
      </span>
    </button>
  );
}
