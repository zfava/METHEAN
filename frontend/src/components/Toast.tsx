"use client";

import { createContext, useCallback, useContext, useState } from "react";

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

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

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

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed bottom-6 right-6 sm:bottom-4 sm:right-4 z-50 flex flex-col gap-2 max-w-sm">
        {toasts.map((t) => (
          <div
            key={t.id}
            role="alert"
            aria-live="polite"
            className={`px-4 py-3 rounded-[10px] border text-sm shadow-sm ${t.dismissing ? "animate-fade-out" : "animate-slide-right"} ${typeStyles[t.type]}`}
          >
            <div className="flex items-center gap-2.5">
              {TOAST_ICONS[t.type]}
              <span className="flex-1">{t.message}</span>
              <button
                onClick={() => dismiss(t.id)}
                className="shrink-0 opacity-40 hover:opacity-80 transition-opacity"
                aria-label="Dismiss"
              >
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
