"use client";

import { useEffect, useRef, useState } from "react";

const DURATION_MS = 400;

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

function defaultFormat(n: number): string {
  if (Number.isInteger(n)) return n.toLocaleString();
  return n.toFixed(1);
}

export default function AnimatedNumber({
  value,
  format = defaultFormat,
  className,
}: {
  value: number;
  format?: (n: number) => string;
  className?: string;
}) {
  const [displayed, setDisplayed] = useState<number>(value);
  const fromRef = useRef<number>(value);
  const startRef = useRef<number | null>(null);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (value === displayed) return;
    fromRef.current = displayed;
    startRef.current = null;

    const tick = (now: number) => {
      if (startRef.current === null) startRef.current = now;
      const elapsed = now - startRef.current;
      const progress = Math.min(1, elapsed / DURATION_MS);
      const eased = easeOutCubic(progress);
      const next = fromRef.current + (value - fromRef.current) * eased;
      setDisplayed(progress >= 1 ? value : next);
      if (progress < 1) rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
    // displayed intentionally omitted: we capture the current displayed
    // value at the moment `value` changes via fromRef and run the
    // tween from there. Including it would restart the tween on every
    // tick and freeze the number.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value]);

  return (
    <span className={className} aria-live="polite">
      {format(displayed)}
    </span>
  );
}
