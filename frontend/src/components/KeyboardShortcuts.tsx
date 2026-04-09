"use client";

import { useEffect, useState, useCallback } from "react";

const SHORTCUTS = [
  { keys: "?", label: "Show shortcuts" },
  { keys: "Esc", label: "Close modal / drawer" },
  { keys: "⌘ K", label: "Focus search / input" },
];

export default function KeyboardShortcuts() {
  const [visible, setVisible] = useState(false);

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    // ? — show/toggle shortcut overlay (only when not typing in an input)
    const tag = (e.target as HTMLElement).tagName;
    const isInput = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || (e.target as HTMLElement).isContentEditable;

    if (e.key === "?" && !isInput) {
      e.preventDefault();
      setVisible((v) => !v);
      return;
    }

    // Escape — close overlay (or modals handled elsewhere)
    if (e.key === "Escape" && visible) {
      setVisible(false);
      return;
    }

    // Cmd/Ctrl + K — focus first visible input
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {
      e.preventDefault();
      const input = document.querySelector<HTMLElement>(
        "main input:not([type=hidden]):not([disabled]), main textarea:not([disabled]), main select:not([disabled])"
      );
      if (input) input.focus();
      return;
    }
  }, [visible]);

  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  // Auto-dismiss after 5 seconds
  useEffect(() => {
    if (!visible) return;
    const t = setTimeout(() => setVisible(false), 5000);
    return () => clearTimeout(t);
  }, [visible]);

  if (!visible) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-fade-up">
      <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) shadow-[var(--shadow-lg)] px-4 py-3 min-w-[200px]">
        <div className="text-[10px] font-medium text-(--color-text-tertiary) uppercase tracking-wider mb-2">Keyboard Shortcuts</div>
        <div className="space-y-1.5">
          {SHORTCUTS.map((s) => (
            <div key={s.keys} className="flex items-center justify-between gap-4">
              <span className="text-xs text-(--color-text-secondary)">{s.label}</span>
              <kbd className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-(--color-page) border border-(--color-border) text-(--color-text-tertiary)">
                {s.keys}
              </kbd>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
