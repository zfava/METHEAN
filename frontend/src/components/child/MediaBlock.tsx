"use client";

/**
 * Renders a single content media block: an image, figure, diagram, or
 * a lightweight inline number line. Forward-compatible: an unknown
 * kind renders nothing rather than throwing.
 *
 * Images always carry their authored alt text. The number line is a
 * dependency-free SVG built from kind-specific params and is safe
 * under prefers-reduced-motion (it has no animation).
 */

import type { MediaBlockData } from "@/lib/api";

const IMG_KINDS = new Set(["image", "figure", "diagram"]);

function toNum(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim() !== "") {
    const n = Number(value);
    if (Number.isFinite(n)) return n;
  }
  return null;
}

function formatTick(value: number): string {
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}

function tickCountFor(requested: number | null, span: number): number {
  const base = requested !== null ? Math.floor(requested) : Math.round(span) + 1;
  return Math.max(2, Math.min(21, base));
}

function NumberLine({ params, alt }: { params: Record<string, unknown> | undefined; alt: string }) {
  const min = toNum(params?.min);
  const max = toNum(params?.max);
  if (min === null || max === null || max <= min) return null;

  const span = max - min;
  const count = tickCountFor(toNum(params?.ticks), span);
  const highlight = toNum(params?.highlight);

  const W = 320;
  const H = 92;
  const padX = 26;
  const lineY = 48;
  const innerW = W - padX * 2;
  const posOf = (v: number) => padX + ((v - min) / span) * innerW;
  const ticks = Array.from({ length: count }, (_, i) => min + (span * i) / (count - 1));

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      role="img"
      aria-label={alt}
      className="w-full max-w-md mx-auto block"
    >
      <line
        x1={padX}
        y1={lineY}
        x2={W - padX}
        y2={lineY}
        stroke="var(--color-text-secondary)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      {ticks.map((v, i) => {
        const x = posOf(v);
        return (
          <g key={i}>
            <line
              x1={x}
              y1={lineY - 6}
              x2={x}
              y2={lineY + 6}
              stroke="var(--color-text-secondary)"
              strokeWidth="2"
            />
            <text
              x={x}
              y={lineY + 22}
              textAnchor="middle"
              fontSize="11"
              fill="var(--color-text-secondary)"
            >
              {formatTick(v)}
            </text>
          </g>
        );
      })}
      {highlight !== null && highlight >= min && highlight <= max && (
        <g>
          <circle cx={posOf(highlight)} cy={lineY} r="7" fill="var(--color-accent)" />
          <text
            x={posOf(highlight)}
            y={lineY - 14}
            textAnchor="middle"
            fontSize="12"
            fontWeight="600"
            fill="var(--color-accent)"
          >
            {formatTick(highlight)}
          </text>
        </g>
      )}
    </svg>
  );
}

export function MediaBlock({ block }: { block: MediaBlockData }) {
  if (block.kind === "number_line") {
    return (
      <figure className="my-4 rounded-2xl border border-(--color-border) bg-(--color-surface) p-5 shadow-[var(--shadow-card)]">
        <NumberLine params={block.params} alt={block.alt} />
        {block.caption && (
          <figcaption className="mt-3 text-center text-sm text-(--color-text-secondary)">
            {block.caption}
          </figcaption>
        )}
      </figure>
    );
  }

  if (IMG_KINDS.has(block.kind)) {
    // An image kind with no source cannot render anything useful.
    if (!block.src) return null;
    return (
      <figure className="my-4 text-center">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={block.src}
          alt={block.alt}
          loading="lazy"
          className="mx-auto max-w-full max-h-[420px] rounded-2xl border border-(--color-border)"
        />
        {block.caption && (
          <figcaption className="mt-2 text-sm text-(--color-text-secondary)">
            {block.caption}
          </figcaption>
        )}
      </figure>
    );
  }

  // Unknown kind: render nothing so new kinds are forward-compatible.
  return null;
}

export default MediaBlock;
