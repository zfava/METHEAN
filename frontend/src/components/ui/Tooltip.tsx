"use client";

import { useEffect, useRef, useState } from "react";

import { cn } from "@/lib/cn";

const LONG_PRESS_MS = 500;
const HIDE_AFTER_MS = 2400;

export type TooltipPlacement = "top" | "bottom";

export default function Tooltip({
  content,
  children,
  placement = "top",
  className,
}: {
  content: React.ReactNode;
  children: React.ReactNode;
  placement?: TooltipPlacement;
  className?: string;
}) {
  const [open, setOpen] = useState(false);
  const longPressTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearTimers = () => {
    if (longPressTimer.current) {
      clearTimeout(longPressTimer.current);
      longPressTimer.current = null;
    }
    if (hideTimer.current) {
      clearTimeout(hideTimer.current);
      hideTimer.current = null;
    }
  };

  useEffect(() => () => clearTimers(), []);

  const handleTouchStart = () => {
    clearTimers();
    longPressTimer.current = setTimeout(() => {
      setOpen(true);
      hideTimer.current = setTimeout(() => setOpen(false), HIDE_AFTER_MS);
    }, LONG_PRESS_MS);
  };

  const handleTouchEnd = () => {
    if (longPressTimer.current) {
      clearTimeout(longPressTimer.current);
      longPressTimer.current = null;
    }
  };

  const positionClass =
    placement === "top"
      ? "bottom-full left-1/2 -translate-x-1/2 mb-2"
      : "top-full left-1/2 -translate-x-1/2 mt-2";

  const arrowClass =
    placement === "top"
      ? "top-full left-1/2 -translate-x-1/2 border-t-white/72 border-x-transparent border-b-transparent"
      : "bottom-full left-1/2 -translate-x-1/2 border-b-white/72 border-x-transparent border-t-transparent";

  return (
    <span
      className={cn("relative inline-flex", className)}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onFocus={() => setOpen(true)}
      onBlur={() => setOpen(false)}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onTouchCancel={handleTouchEnd}
    >
      {children}
      {open && (
        <span
          role="tooltip"
          className={cn(
            "absolute z-50 pointer-events-none whitespace-nowrap",
            "glass border border-(--color-border) shadow-[var(--shadow-card)]",
            "rounded-[8px] px-2.5 py-1.5",
            "text-[12px] font-medium text-(--color-text)",
            "animate-scale-in",
            positionClass,
          )}
        >
          {content}
          <span
            aria-hidden="true"
            className={cn(
              "absolute h-0 w-0 border-solid border-[5px]",
              arrowClass,
            )}
          />
        </span>
      )}
    </span>
  );
}
