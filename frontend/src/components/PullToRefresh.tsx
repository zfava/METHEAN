"use client";

import { useCallback, useRef, useState } from "react";
import { haptic } from "@/lib/haptics";

const THRESHOLD = 64;

export default function PullToRefresh({
  onRefresh,
  children,
}: {
  onRefresh: () => Promise<void>;
  children: React.ReactNode;
}) {
  const [pulling, setPulling] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const pullY = useRef(0);
  const startY = useRef(0);
  const triggered = useRef(false);
  const indicatorRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const updateIndicator = useCallback((y: number) => {
    const el = indicatorRef.current;
    if (!el) return;
    const progress = Math.min(y / THRESHOLD, 1);
    el.style.transform = `translateY(${Math.min(y, THRESHOLD + 20)}px) scale(${progress})`;
    el.style.opacity = String(progress);
  }, []);

  const onTouchStart = useCallback((e: React.TouchEvent) => {
    const container = containerRef.current;
    if (!container || container.scrollTop > 0) return;
    startY.current = e.touches[0].clientY;
    pullY.current = 0;
    triggered.current = false;
  }, []);

  const onTouchMove = useCallback((e: React.TouchEvent) => {
    if (refreshing) return;
    const container = containerRef.current;
    if (!container || container.scrollTop > 0) {
      startY.current = 0;
      return;
    }
    if (!startY.current) return;

    const dy = e.touches[0].clientY - startY.current;
    if (dy <= 0) {
      pullY.current = 0;
      updateIndicator(0);
      return;
    }

    // Logarithmic resistance
    const dampened = dy * 0.5;
    pullY.current = dampened;
    setPulling(true);
    updateIndicator(dampened);

    if (dampened >= THRESHOLD && !triggered.current) {
      haptic("medium");
      triggered.current = true;
    }
  }, [refreshing, updateIndicator]);

  const onTouchEnd = useCallback(async () => {
    if (!triggered.current || refreshing) {
      setPulling(false);
      updateIndicator(0);
      startY.current = 0;
      return;
    }

    setRefreshing(true);
    try {
      await onRefresh();
    } finally {
      setRefreshing(false);
      setPulling(false);
      updateIndicator(0);
      startY.current = 0;
    }
  }, [onRefresh, refreshing, updateIndicator]);

  return (
    <div
      ref={containerRef}
      className="relative"
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
    >
      {/* Refresh indicator */}
      <div
        ref={indicatorRef}
        className="absolute left-1/2 -ml-4 top-0 z-10 pointer-events-none"
        style={{ opacity: 0, transform: "translateY(0) scale(0)", transition: pulling ? "none" : "all 0.25s var(--ease)" }}
      >
        <div
          className="w-8 h-8 rounded-full border-2 border-(--color-accent) border-t-transparent"
          style={{ animation: refreshing ? "spin 0.6s linear infinite" : "none" }}
        />
      </div>
      {children}
    </div>
  );
}
