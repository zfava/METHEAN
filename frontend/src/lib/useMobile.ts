"use client";

import { useEffect, useState } from "react";

/** Returns true when viewport width is below the given breakpoint. */
export function useMobile(breakpoint = 768): boolean {
  const [mobile, setMobile] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${breakpoint - 1}px)`);
    setMobile(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMobile(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [breakpoint]);

  return mobile;
}

/** Returns true on devices with touch capability. */
export function useTouchDevice(): boolean {
  const [touch, setTouch] = useState(false);

  useEffect(() => {
    setTouch(
      "ontouchstart" in window || navigator.maxTouchPoints > 0
    );
  }, []);

  return touch;
}
