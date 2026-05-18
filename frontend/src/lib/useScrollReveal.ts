"use client";

import { useEffect, useRef, useState } from "react";

export function useScrollReveal<T extends HTMLElement = HTMLDivElement>(
  threshold = 0.05,
  rootMargin = "0px 0px -60px 0px",
) {
  const ref = useRef<T>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (typeof window === "undefined" || !("IntersectionObserver" in window)) {
      setVisible(true);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setVisible(true);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold, rootMargin },
    );
    io.observe(el);
    const fallback = window.setTimeout(() => setVisible(true), 1800);
    return () => {
      io.disconnect();
      window.clearTimeout(fallback);
    };
  }, [threshold, rootMargin]);

  return { ref, visible };
}
