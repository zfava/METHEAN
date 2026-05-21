"use client";

/**
 * NumberLine widget: number sense, addition, and subtraction.
 *
 * Renders a horizontal number line with labeled ticks. The child
 * moves a marker by tapping the line or pressing the arrow keys. In
 * "jump" mode each move draws a visible hop arc so the child sees the
 * jump. When the marker value reaches the target, onComplete fires
 * once.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { MiniWidgetProps } from "./types";

function toNum(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim() !== "") {
    const n = Number(value);
    if (Number.isFinite(n)) return n;
  }
  return null;
}

const W = 360;
const H = 124;
const PAD_X = 26;
const LINE_Y = 84;
const INNER_W = W - PAD_X * 2;

export function NumberLine({
  params,
  target,
  onValueChange,
  onComplete,
  reducedMotion,
}: MiniWidgetProps) {
  const min = toNum(params.min) ?? 0;
  const maxRaw = toNum(params.max) ?? 10;
  const max = maxRaw > min ? maxRaw : min + 10;
  const step = useMemo(() => {
    const s = toNum(params.step);
    return s !== null && s > 0 ? s : 1;
  }, [params.step]);
  const mode = params.mode === "jump" ? "jump" : "locate";
  const label = typeof params.label === "string" ? params.label : undefined;
  const goal = toNum(target);

  const clampToStep = useCallback(
    (v: number) => {
      const steps = Math.round((v - min) / step);
      const snapped = min + steps * step;
      return Math.max(min, Math.min(max, Number(snapped.toFixed(6))));
    },
    [min, max, step],
  );

  const start = useMemo(() => {
    const s = toNum(params.start);
    return clampToStep(s ?? min);
  }, [params.start, min, clampToStep]);

  const completedRef = useRef(false);
  const wrapRef = useRef<HTMLDivElement>(null);
  const [value, setValue] = useState(start);
  const [hop, setHop] = useState<{ from: number; to: number } | null>(null);

  // Reset when the line definition changes.
  useEffect(() => {
    setValue(start);
    setHop(null);
    completedRef.current = false;
  }, [start, min, max, step]);

  useEffect(() => {
    onValueChange?.(value);
  }, [value, onValueChange]);

  useEffect(() => {
    if (goal !== null && Math.abs(value - goal) < 1e-9 && !completedRef.current) {
      completedRef.current = true;
      onComplete?.();
    }
  }, [value, goal, onComplete]);

  const moveTo = useCallback(
    (next: number) => {
      const snapped = clampToStep(next);
      setValue((prev) => {
        if (snapped !== prev && mode === "jump") setHop({ from: prev, to: snapped });
        return snapped;
      });
    },
    [clampToStep, mode],
  );

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === "ArrowLeft" || e.key === "ArrowDown") {
      e.preventDefault();
      moveTo(value - step);
    } else if (e.key === "ArrowRight" || e.key === "ArrowUp") {
      e.preventDefault();
      moveTo(value + step);
    } else if (e.key === "Home") {
      e.preventDefault();
      moveTo(min);
    } else if (e.key === "End") {
      e.preventDefault();
      moveTo(max);
    }
  }

  function onTapLine(e: React.MouseEvent) {
    const wrap = wrapRef.current;
    if (!wrap) return;
    const rect = wrap.getBoundingClientRect();
    if (rect.width === 0) return;
    const vbX = ((e.clientX - rect.left) / rect.width) * W;
    moveTo(min + ((vbX - PAD_X) / INNER_W) * (max - min));
  }

  const xOf = (v: number) => PAD_X + ((v - min) / (max - min)) * INNER_W;

  // Labeled ticks. Capped so a very wide line stays legible.
  const ticks: number[] = [];
  const rawCount = Math.round((max - min) / step) + 1;
  const stride = rawCount > 21 ? Math.ceil(rawCount / 21) : 1;
  for (let i = 0; i < rawCount; i += stride) {
    ticks.push(Number((min + i * step).toFixed(6)));
  }

  const markerX = xOf(value);

  return (
    <div>
      {label && (
        <p className="mb-3 text-sm font-medium text-(--color-text-secondary)">{label}</p>
      )}
      <div
        ref={wrapRef}
        role="slider"
        tabIndex={0}
        aria-label={label ? `${label} number line` : "Number line"}
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
        aria-valuetext={String(value)}
        onKeyDown={onKeyDown}
        onClick={onTapLine}
        className="cursor-pointer rounded-2xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--color-accent)"
      >
        <svg viewBox={`0 0 ${W} ${H}`} className="block w-full" aria-hidden="true">
          {/* Base line */}
          <line
            x1={PAD_X}
            y1={LINE_Y}
            x2={W - PAD_X}
            y2={LINE_Y}
            stroke="var(--color-text-secondary)"
            strokeWidth="2"
            strokeLinecap="round"
          />
          {/* Ticks and labels */}
          {ticks.map((v) => {
            const x = xOf(v);
            return (
              <g key={v}>
                <line
                  x1={x}
                  y1={LINE_Y - 6}
                  x2={x}
                  y2={LINE_Y + 6}
                  stroke="var(--color-text-secondary)"
                  strokeWidth="2"
                />
                <text
                  x={x}
                  y={LINE_Y + 24}
                  textAnchor="middle"
                  fontSize="12"
                  fill="var(--color-text-secondary)"
                >
                  {v}
                </text>
              </g>
            );
          })}
          {/* Hop arc (jump mode) */}
          {mode === "jump" && hop && hop.from !== hop.to && (
            <path
              className={reducedMotion ? undefined : "animate-fade-in"}
              d={`M ${xOf(hop.from)} ${LINE_Y} Q ${(xOf(hop.from) + xOf(hop.to)) / 2} ${
                LINE_Y - 34
              } ${xOf(hop.to)} ${LINE_Y}`}
              fill="none"
              stroke="var(--color-accent)"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          )}
          {/* Marker and current value */}
          <g transform={`translate(${markerX} 0)`}>
            <text
              x="0"
              y="28"
              textAnchor="middle"
              fontSize="22"
              fontWeight="700"
              fill="var(--color-accent)"
            >
              {value}
            </text>
            <path
              d={`M 0 ${LINE_Y - 14} l 7 -11 l -14 0 Z`}
              fill="var(--color-accent)"
            />
            <circle cx="0" cy={LINE_Y} r="7" fill="var(--color-accent)" />
          </g>
        </svg>
      </div>
      <p className="mt-1 text-center text-sm text-(--color-text-secondary)">
        Tap the line or use the arrow keys to move.
      </p>
    </div>
  );
}

export default NumberLine;
