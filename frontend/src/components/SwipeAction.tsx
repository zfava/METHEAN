"use client";

import { useCallback, useRef, useEffect } from "react";
import { haptic } from "@/lib/haptics";
import { useMobile } from "@/lib/useMobile";

// Global reset: only one SwipeAction open at a time
let activeReset: (() => void) | null = null;

interface SwipeActionProps {
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  leftLabel?: string;
  rightLabel?: string;
  leftColor?: string;
  rightColor?: string;
  children: React.ReactNode;
}

export default function SwipeAction({
  onSwipeLeft,
  onSwipeRight,
  // Defaults reflect the most common task-row use case (mark a
  // child's activity Complete vs Reschedule). Callers that need
  // approve/reject etc. continue to override.
  leftLabel = "Complete",
  rightLabel = "Reschedule",
  leftColor = "var(--color-success)",
  rightColor = "var(--color-blocked)",
  children,
}: SwipeActionProps) {
  // Only enable swipe on touch / small viewports. On desktop we
  // pass children straight through so mouse interactions on the
  // underlying card aren't intercepted by the swipe handlers.
  const isMobile = useMobile();
  const contentRef = useRef<HTMLDivElement>(null);
  const dragStart = useRef<{ x: number; y: number; time: number } | null>(null);
  const dragX = useRef(0);
  const triggered = useRef(false);
  const locked = useRef<"h" | "v" | null>(null);
  const leftRef = useRef<HTMLDivElement>(null);
  const rightRef = useRef<HTMLDivElement>(null);

  const THRESHOLD = 80;

  const resetPosition = useCallback(() => {
    const el = contentRef.current;
    if (!el) return;
    el.style.transition = "transform 0.25s cubic-bezier(0.32, 0.72, 0, 1)";
    el.style.transform = "translateX(0)";
    dragX.current = 0;
    triggered.current = false;
  }, []);

  // Register as active, reset previous
  const claimActive = useCallback(() => {
    if (activeReset && activeReset !== resetPosition) {
      activeReset();
    }
    activeReset = resetPosition;
  }, [resetPosition]);

  // Rubber-band: logarithmic resistance past threshold
  function rubberBand(x: number, limit: number): number {
    if (Math.abs(x) <= limit) return x;
    const sign = x > 0 ? 1 : -1;
    const over = Math.abs(x) - limit;
    return sign * (limit + Math.log(1 + over / limit) * limit * 0.4);
  }

  const onTouchStart = useCallback((e: React.TouchEvent) => {
    const t = e.touches[0];
    dragStart.current = { x: t.clientX, y: t.clientY, time: Date.now() };
    locked.current = null;
    triggered.current = false;
    claimActive();
    const el = contentRef.current;
    if (el) el.style.transition = "none";
  }, [claimActive]);

  const onTouchMove = useCallback((e: React.TouchEvent) => {
    if (!dragStart.current) return;
    const t = e.touches[0];
    const dx = t.clientX - dragStart.current.x;
    const dy = t.clientY - dragStart.current.y;

    // Lock direction after 10px of movement
    if (!locked.current) {
      if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
        locked.current = Math.abs(dx) > Math.abs(dy) ? "h" : "v";
      }
      return;
    }

    if (locked.current === "v") return;

    // Only allow swipe in directions that have handlers
    if (dx > 0 && !onSwipeRight) return;
    if (dx < 0 && !onSwipeLeft) return;

    const clamped = rubberBand(dx, THRESHOLD + 40);
    dragX.current = dx;

    const el = contentRef.current;
    if (el) el.style.transform = `translateX(${clamped}px)`;

    // Haptic at threshold crossing
    if (Math.abs(dx) >= THRESHOLD && !triggered.current) {
      haptic("medium");
      triggered.current = true;
    } else if (Math.abs(dx) < THRESHOLD) {
      triggered.current = false;
    }
  }, [onSwipeLeft, onSwipeRight]);

  const onTouchEnd = useCallback(() => {
    if (!dragStart.current) return;
    const dx = dragX.current;
    const dt = Date.now() - dragStart.current.time;
    const velocity = Math.abs(dx) / Math.max(dt, 1) * 1000;
    dragStart.current = null;

    const shouldTrigger = Math.abs(dx) >= THRESHOLD || velocity > 600;

    if (shouldTrigger && dx < 0 && onSwipeLeft) {
      onSwipeLeft();
      resetPosition();
    } else if (shouldTrigger && dx > 0 && onSwipeRight) {
      onSwipeRight();
      resetPosition();
    } else {
      resetPosition();
    }
  }, [onSwipeLeft, onSwipeRight, resetPosition]);

  // Clean up active ref on unmount
  useEffect(() => {
    return () => {
      if (activeReset === resetPosition) activeReset = null;
    };
  }, [resetPosition]);

  // Desktop: render children straight through with no overflow
  // wrapper. The keystroke / click path on the underlying card
  // handlers continues to work uninterrupted.
  if (!isMobile) {
    return <>{children}</>;
  }

  return (
    <div className="relative overflow-hidden">
      {/* Left action (revealed by swiping right) */}
      {onSwipeRight && (
        <div
          ref={leftRef}
          className="absolute inset-y-0 left-0 flex items-center px-5 text-sm font-medium text-white"
          style={{ background: leftColor, width: THRESHOLD + 40 }}
        >
          {leftLabel}
        </div>
      )}
      {/* Right action (revealed by swiping left) */}
      {onSwipeLeft && (
        <div
          ref={rightRef}
          className="absolute inset-y-0 right-0 flex items-center justify-end px-5 text-sm font-medium text-white"
          style={{ background: rightColor, width: THRESHOLD + 40 }}
        >
          {rightLabel}
        </div>
      )}
      {/* Content */}
      <div
        ref={contentRef}
        className="relative bg-(--color-surface)"
        style={{ willChange: "transform" }}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        {children}
      </div>
    </div>
  );
}
