"use client";

import { useEffect, useState, type ReactNode } from "react";

import { usePersonalization } from "@/lib/PersonalizationProvider";
import { CALM_VIBE_FALLBACK, type Vibe } from "@/lib/personalization-types";

/**
 * Wraps children in a div that applies the active vibe's CSS-variable
 * tokens via inline style. React treats `--foo` keys as native CSS
 * custom properties, no escape hatch needed. Switching vibes via
 * `updateProfile({ vibe })` causes this wrapper to re-render with the
 * new token bag; the transition declaration on bg/color smooths the
 * swap unless the user prefers reduced motion.
 */
export function VibeProvider({ children }: { children: ReactNode }) {
  const { profile, library } = usePersonalization();

  // Resolve the active vibe entry, falling back to the calm token set
  // when the library is still loading or the selected vibe ID no
  // longer exists (e.g., parent policy retired it).
  const resolved: Vibe =
    library?.vibes.find((v) => v.id === profile.vibe) ?? CALM_VIBE_FALLBACK;

  const prefersReducedMotion = usePrefersReducedMotion();

  const style: React.CSSProperties = {
    ...(resolved.tokens as React.CSSProperties),
    minHeight: "100dvh",
  };
  if (!prefersReducedMotion) {
    style.transition = "background-color 240ms ease, color 240ms ease";
  }

  return (
    <div data-vibe={profile.vibe} style={style}>
      {children}
    </div>
  );
}

/**
 * Tracks the `prefers-reduced-motion: reduce` media query. Returns
 * false during SSR (no `window`) so the transition isn't omitted on
 * first paint when the client would actually allow it; the effect
 * corrects the value on hydration.
 */
function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState<boolean>(false);
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return;
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mql.matches);
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, []);
  return reduced;
}
