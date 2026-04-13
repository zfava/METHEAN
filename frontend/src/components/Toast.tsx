"use client";

import { createContext, useCallback, useContext, useRef, useState } from "react";
import { useMobile } from "@/lib/useMobile";

interface ToastItem {
  id: number;
  message: string;
  type: "error" | "success" | "info";
  dismissing?: boolean;
}

interface ToastContextValue {
  toast: (message: string, type?: "error" | "success" | "info") => void;
}

const ToastContext = createContext<ToastContextValue>({
  toast: () => {},
});

export function useToast() {
  return useContext(ToastContext);
}

let nextId = 0;

const TOAST_ICONS = {
  error: (
    <svg className="w-4 h-4 shrink-0" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" fill="var(--color-danger)" opacity="0.15" />
      <circle cx="8" cy="8" r="7" stroke="var(--color-danger)" strokeWidth="1" fill="none" />
      <path d="M5.5 5.5l5 5M10.5 5.5l-5 5" stroke="var(--color-danger)" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  ),
  success: (
    <svg className="w-4 h-4 shrink-0" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" fill="var(--color-success)" opacity="0.15" />
      <circle cx="8" cy="8" r="7" stroke="var(--color-success)" strokeWidth="1" fill="none" />
      <path d="M5 8l2 2 4-4" stroke="var(--color-success)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  ),
  info: (
    <svg className="w-4 h-4 shrink-0" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="7" fill="var(--color-accent)" opacity="0.15" />
      <circle cx="8" cy="8" r="7" stroke="var(--color-accent)" strokeWidth="1" fill="none" />
      <path d="M8 7v4M8 5.5v.01" stroke="var(--color-accent)" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  ),
};

const typeStyles = {
  error: "bg-(--color-danger-light) border-(--color-danger)/20 text-(--color-danger)",
  success: "bg-(--color-success-light) border-(--color-success)/20 text-(--color-success)",
  info: "bg-(--color-accent-light) border-(--color-accent)/20 text-(--color-accent)",
};

function SwipeableToast({
  item,
  onDismiss,
}: {
  item: ToastItem;
  onDismiss: () => void;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const startX = useRef(0);
  const currentX = useRef(0);

  const onTouchStart = useCallback((e: React.TouchEvent) => {
    startX.current = e.touches[0].clientX;
    const el = ref.current;
    if (el) el.style.transition = "none";
  }, []);

  const onTouchMove = useCallback((e: React.TouchEvent) => {
    const dx = e.touches[0].clientX - startX.current;
    currentX.current = dx;
    const el = ref.current;
    if (el) {
      el.style.transform = `translateX(${dx}px)`;
      el.style.opacity = String(Math.max(0, 1 - Math.abs(dx) / 200));
    }
  }, []);

  const onTouchEnd = useCallback(() => {
    if (Math.abs(currentX.current) > 80) {
      onDismiss();
    } else {
      const el = ref.current;
      if (el) {
        el.style.transition = "transform 0.2s var(--ease), opacity 0.2s var(--ease)";
        el.style.transform = "translateX(0)";
        el.style.opacity = "1";
      }
    }
    currentX.current = 0;
  }, [onDismiss]);

  return (
    <div
      ref={ref}
      role="alert"
      aria-live="polite"
      className={`px-4 py-3 rounded-[10px] border text-sm shadow-sm ${item.dismissing ? "animate-fade-out" : "animate-slide-right"} ${typeStyles[item.type]}`}
      style={{ willChange: "transform" }}
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
    >
      <div className="flex items-center gap-2.5">
        {TOAST_ICONS[item.type]}
        <span className="flex-1">{item.message}</span>
        <button
          onClick={onDismiss}
          className="shrink-0 opacity-40 hover:opacity-80 transition-opacity"
          aria-label="Dismiss"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const isMobile = useMobile();

  const dismiss = useCallback((id: number) => {
    setToasts((prev) => prev.map((t) => t.id === id ? { ...t, dismissing: true } : t));
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 200);
  }, []);

  const toast = useCallback((message: string, type: "error" | "success" | "info" = "error") => {
    const id = nextId++;
    setToasts((prev) => [...prev, { id, message, type }]);
    const duration = type === "error" ? 5000 : 3000;
    setTimeout(() => dismiss(id), duration);
  }, [dismiss]);

  // Mobile: bottom (above tab bar). Desktop: bottom-right.
  const positionClass = isMobile
    ? "fixed left-4 right-4 z-50 flex flex-col gap-2"
    : "fixed bottom-6 right-6 sm:bottom-4 sm:right-4 z-50 flex flex-col gap-2 max-w-sm";
  const positionStyle: React.CSSProperties = isMobile
    ? { bottom: "calc(56px + var(--safe-bottom) + 12px)" }
    : {};

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className={positionClass} style={positionStyle}>
        {toasts.map((t) => (
          <SwipeableToast key={t.id} item={t} onDismiss={() => dismiss(t.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}
