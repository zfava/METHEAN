"use client";

/**
 * CountingObjects widget: cardinality and one-to-one counting.
 *
 * Renders `count` tappable objects. Tapping toggles an object
 * "counted" and updates a live running tally. When the counted total
 * reaches the target (or the full count when no target is given) the
 * widget fires onComplete once and settles into a calm success state.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import type { MiniWidgetProps } from "./types";

type Shape = "circle" | "star" | "square";

function toInt(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return Math.floor(value);
  if (typeof value === "string" && value.trim() !== "") {
    const n = Number(value);
    if (Number.isFinite(n)) return Math.floor(n);
  }
  return null;
}

const STAR_PATH =
  "M12 2.5 L14.23 8.93 L21.03 9.06 L15.61 13.17 L17.58 19.69 L12 15.8 " +
  "L6.42 19.69 L8.39 13.17 L2.97 9.06 L9.77 8.93 Z";

function ObjectShape({ shape, counted }: { shape: Shape; counted: boolean }) {
  const fill = counted ? "var(--color-accent)" : "none";
  const stroke = counted ? "var(--color-accent)" : "var(--color-text-secondary)";
  return (
    <svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true">
      {shape === "circle" && (
        <circle cx="12" cy="12" r="9" fill={fill} stroke={stroke} strokeWidth="2" />
      )}
      {shape === "square" && (
        <rect x="3.5" y="3.5" width="17" height="17" rx="3" fill={fill} stroke={stroke} strokeWidth="2" />
      )}
      {shape === "star" && (
        <path d={STAR_PATH} fill={fill} stroke={stroke} strokeWidth="2" strokeLinejoin="round" />
      )}
      {counted && (
        <path
          d="M7 12.4l3.2 3.2L17 9"
          fill="none"
          stroke="var(--color-surface)"
          strokeWidth="2.6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      )}
    </svg>
  );
}

export function CountingObjects({
  params,
  target,
  onValueChange,
  onComplete,
  reducedMotion,
}: MiniWidgetProps) {
  const count = useMemo(() => {
    const c = toInt(params.count) ?? 0;
    return Math.max(0, Math.min(50, c));
  }, [params.count]);

  const label = typeof params.label === "string" ? params.label : undefined;
  const shape: Shape =
    params.shape === "star" || params.shape === "square" ? params.shape : "circle";

  const goal = useMemo(() => {
    const g = toInt(target) ?? toInt(params.target) ?? count;
    return Math.max(0, Math.min(count, g));
  }, [target, params.target, count]);

  const completedRef = useRef(false);
  const [counted, setCounted] = useState<boolean[]>(() => Array(count).fill(false));

  // Reset when the object count changes (a fresh widget instance).
  useEffect(() => {
    setCounted(Array(count).fill(false));
    completedRef.current = false;
  }, [count]);

  const tally = counted.reduce((n, c) => (c ? n + 1 : n), 0);
  const done = goal > 0 && tally >= goal;

  useEffect(() => {
    onValueChange?.(tally);
  }, [tally, onValueChange]);

  useEffect(() => {
    if (done && !completedRef.current) {
      completedRef.current = true;
      onComplete?.();
    }
  }, [done, onComplete]);

  function toggle(i: number) {
    setCounted((prev) => {
      const next = [...prev];
      next[i] = !next[i];
      return next;
    });
  }

  return (
    <div>
      {label && (
        <p className="mb-3 text-sm font-medium text-(--color-text-secondary)">{label}</p>
      )}

      <div className="flex flex-wrap justify-center gap-2.5">
        {counted.map((isCounted, i) => (
          <button
            key={i}
            type="button"
            onClick={() => toggle(i)}
            aria-label={`Object ${i + 1}, ${isCounted ? "counted" : "not counted"}`}
            aria-pressed={isCounted}
            className={`flex h-14 w-14 min-h-[44px] min-w-[44px] items-center justify-center rounded-2xl border bg-(--color-page) focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--color-accent) ${
              isCounted ? "border-(--color-accent)" : "border-(--color-border)"
            } ${reducedMotion ? "" : "transition-colors"}`}
          >
            <ObjectShape shape={shape} counted={isCounted} />
          </button>
        ))}
      </div>

      <div className="mt-4 text-center">
        <p aria-live="polite" className="text-3xl font-bold text-(--color-text)">
          {tally}
        </p>
        <p className="text-sm text-(--color-text-secondary)">
          {done
            ? "You counted them all. Great counting!"
            : `Tap to count${goal > 0 ? ` to ${goal}` : ""}`}
        </p>
      </div>
    </div>
  );
}

export default CountingObjects;
