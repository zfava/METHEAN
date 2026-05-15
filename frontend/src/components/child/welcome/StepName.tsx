"use client";

import { useEffect, useRef, useState } from "react";

import { CompanionAvatar } from "@/components/CompanionAvatar";
import type { VoicePersona } from "@/lib/personalization-types";

interface StepNameProps {
  persona: VoicePersona | null;
  initialName: string;
  requiresReview: boolean;
  onContinue: (name: string) => void;
}

/**
 * Pre-fills the input with the persona's default companion name so
 * a kid who just wants the suggestion can hit Continue immediately.
 * Trims, enforces 1-30 chars, surfaces the parent-review note when
 * the household policy requires it.
 */
export function StepName({ persona, initialName, requiresReview, onContinue }: StepNameProps) {
  const fallbackDefault = persona?.default_companion_name ?? "";
  const [value, setValue] = useState<string>(initialName || fallbackDefault);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const trimmed = value.trim();
  const ok = trimmed.length >= 1 && trimmed.length <= 30;

  return (
    <div className="space-y-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold text-(--color-text) tracking-tight">What should we call them?</h1>
        <p className="text-sm text-(--color-text-secondary) mt-2">You can change this anytime.</p>
      </header>

      {persona && (
        <div className="flex justify-center text-(--color-accent)">
          <CompanionAvatar personaId={persona.id} size={72} />
        </div>
      )}

      <input
        ref={inputRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        maxLength={30}
        placeholder={fallbackDefault || "Name"}
        className="w-full px-4 py-3 text-lg border border-(--color-border) rounded-2xl bg-(--color-surface) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/30 min-h-[44px]"
        aria-label="Companion name"
      />
      <p className="text-[11px] text-(--color-text-tertiary) text-right -mt-4">{trimmed.length}/30</p>

      {requiresReview && (
        <div className="text-xs text-(--color-warning) bg-(--color-warning-light) px-3 py-2 rounded-xl">
          Your parent will check the name before it&apos;s used.
        </div>
      )}

      <button
        type="button"
        disabled={!ok}
        onClick={() => ok && onContinue(trimmed)}
        className="w-full py-3.5 rounded-2xl bg-(--color-text) text-white font-semibold disabled:opacity-40 min-h-[44px]"
      >
        Continue
      </button>
    </div>
  );
}
