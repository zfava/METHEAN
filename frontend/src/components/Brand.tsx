"use client";

const MARK_PATH = "M 50 2 C 58 2, 80 11, 93 17 C 94 17.5, 94 18.5, 94 20 L 94 56 C 94 72, 88 86, 76 96 C 68 103, 58 109, 50 113 C 42 109, 32 103, 24 96 C 12 86, 6 72, 6 56 L 6 20 C 6 18.5, 6 17.5, 7 17 C 20 11, 42 2, 50 2 Z M 21.5 84.5 L 21 28 L 50 51 L 79 28 L 78.5 84.5 L 65.5 84.5 L 65 46 L 50 58.5 L 35 46 L 34.5 84.5 Z";

const WORDMARK_PATH = "M 0 2 L 1.8 2 L 1.8 22 L 0 22 Z M 22.2 2 L 24 2 L 24 22 L 22.2 22 Z M 0 2 L 2.3 2 L 12.9 14 L 11.1 14 Z M 24 2 L 21.7 2 L 11.1 14 L 12.9 14 Z  M 34 2 L 35.8 2 L 35.8 22 L 34 22 Z M 34 2 L 50 2 L 50 3.8 L 34 3.8 Z M 34 11.1 L 48 11.1 L 48 12.9 L 34 12.9 Z M 34 20.2 L 50 20.2 L 50 22 L 34 22 Z  M 58 2 L 78 2 L 78 3.8 L 58 3.8 Z M 67.1 3.8 L 68.9 3.8 L 68.9 22 L 67.1 22 Z  M 88 2 L 89.8 2 L 89.8 22 L 88 22 Z M 108.2 2 L 110 2 L 110 22 L 108.2 22 Z M 89.8 11.1 L 108.2 11.1 L 108.2 12.9 L 89.8 12.9 Z  M 120 2 L 121.8 2 L 121.8 22 L 120 22 Z M 120 2 L 136 2 L 136 3.8 L 120 3.8 Z M 120 11.1 L 134 11.1 L 134 12.9 L 120 12.9 Z M 120 20.2 L 136 20.2 L 136 22 L 120 22 Z  M 155.92 2 L 158.08 2 L 169.08 22 L 165.12 22 Z M 155.92 2 L 158.08 2 L 148.88 22 L 144.92 22 Z M 153.6 13.1 L 160.4 13.1 L 160.4 14.9 L 153.6 14.9 Z  M 178 2 L 179.8 2 L 179.8 22 L 178 22 Z M 198.2 2 L 200 2 L 200 22 L 198.2 22 Z M 178 2 L 180.88 2 L 200 22 L 197.12 22 Z";

/** Gold shield mark */
export function MetheanMark({ size = 28, color = "#C6A24E" }: { size?: number; color?: string }) {
  const h = size;
  const w = Math.round(size * (100 / 115));
  return (
    <svg viewBox="0 0 100 115" width={w} height={h} aria-hidden="true">
      <path fillRule="evenodd" clipRule="evenodd" d={MARK_PATH} fill={color} />
    </svg>
  );
}

/** Geometric wordmark */
export function MetheanWordmark({ height = 16, color = "#C6A24E" }: { height?: number; color?: string }) {
  const w = Math.round(height * (202 / 24));
  return (
    <svg viewBox="0 0 202 24" width={w} height={height} aria-label="METHEAN">
      <path fillRule="evenodd" clipRule="evenodd" d={WORDMARK_PATH} fill={color} />
    </svg>
  );
}

/** Mark + wordmark side by side */
export function MetheanLogo({ markSize = 28, wordmarkHeight = 16, color = "#C6A24E", gap = 12 }: {
  markSize?: number; wordmarkHeight?: number; color?: string; gap?: number;
}) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap }}>
      <MetheanMark size={markSize} color={color} />
      <MetheanWordmark height={wordmarkHeight} color={color} />
    </div>
  );
}

/** Vertical lockup: mark above wordmark */
export function MetheanLogoVertical({ markSize = 48, wordmarkHeight = 20, color = "#C6A24E", gap = 12 }: {
  markSize?: number; wordmarkHeight?: number; color?: string; gap?: number;
}) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap }}>
      <MetheanMark size={markSize} color={color} />
      <MetheanWordmark height={wordmarkHeight} color={color} />
    </div>
  );
}
