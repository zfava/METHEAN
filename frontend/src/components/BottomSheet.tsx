"use client";

import { useEffect, useRef, useCallback } from "react";

interface BottomSheetProps {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  snapPoints?: number[];
  label?: string;
}

export default function BottomSheet({ open, onClose, children, snapPoints, label = "Dialog" }: BottomSheetProps) {
  const sheetRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLElement | null>(null);
  const dragStart = useRef<{ y: number; time: number } | null>(null);
  const dragOffset = useRef(0);
  const animFrame = useRef(0);
  const prevBodyOverflow = useRef("");

  // Lock body scroll + save trigger for focus restore
  useEffect(() => {
    if (open) {
      triggerRef.current = document.activeElement as HTMLElement;
      prevBodyOverflow.current = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      // Focus first focusable element in sheet
      requestAnimationFrame(() => {
        const focusable = sheetRef.current?.querySelector<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        focusable?.focus();
      });
    } else {
      document.body.style.overflow = prevBodyOverflow.current;
      triggerRef.current?.focus();
    }
    return () => {
      document.body.style.overflow = prevBodyOverflow.current;
    };
  }, [open]);

  // Escape to close
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  const setTransform = useCallback((y: number, animate: boolean) => {
    const sheet = sheetRef.current;
    if (!sheet) return;
    sheet.style.transition = animate
      ? "transform 0.3s cubic-bezier(0.32, 0.72, 0, 1)"
      : "none";
    sheet.style.transform = `translateY(${Math.max(0, y)}px)`;
  }, []);

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    const touch = e.touches[0];
    dragStart.current = { y: touch.clientY, time: Date.now() };
    dragOffset.current = 0;
    const sheet = sheetRef.current;
    if (sheet) sheet.style.transition = "none";
  }, []);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (!dragStart.current) return;
    const touch = e.touches[0];
    const dy = touch.clientY - dragStart.current.y;
    dragOffset.current = dy;
    cancelAnimationFrame(animFrame.current);
    animFrame.current = requestAnimationFrame(() => setTransform(dy, false));
  }, [setTransform]);

  const handleTouchEnd = useCallback(() => {
    if (!dragStart.current) return;
    const dy = dragOffset.current;
    const dt = Date.now() - dragStart.current.time;
    const velocity = dy / Math.max(dt, 1) * 1000;
    const sheetH = sheetRef.current?.offsetHeight || 400;
    dragStart.current = null;

    if (dy > sheetH * 0.4 || velocity > 500) {
      setTransform(sheetH, true);
      setTimeout(onClose, 250);
    } else {
      setTransform(0, true);
    }
  }, [onClose, setTransform]);

  useEffect(() => {
    if (open) requestAnimationFrame(() => setTransform(0, true));
  }, [open, setTransform]);

  if (!open) return null;

  const maxH = snapPoints?.[0] ? `${snapPoints[0] * 100}vh` : "85vh";

  return (
    <div className="fixed inset-0 z-50" role="presentation">
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/40 animate-fade-in"
        onClick={onClose}
        aria-hidden="true"
      />
      {/* Sheet */}
      <div
        ref={sheetRef}
        role="dialog"
        aria-modal="true"
        aria-label={label}
        className="absolute bottom-0 left-0 right-0 bg-(--color-surface) rounded-t-[16px] shadow-lg"
        style={{
          maxHeight: maxH,
          paddingBottom: "var(--safe-bottom)",
          animation: "slide-up 0.3s cubic-bezier(0.32, 0.72, 0, 1) both",
          willChange: "transform",
        }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Drag handle */}
        <div className="flex justify-center pt-2.5 pb-1">
          <div className="w-9 h-1 rounded-full bg-(--color-border-strong)" />
        </div>
        {/* Content */}
        <div className="overflow-y-auto" style={{ maxHeight: `calc(${maxH} - 28px)` }}>
          {children}
        </div>
      </div>
    </div>
  );
}
