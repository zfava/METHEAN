"use client";

import { useScrollReveal } from "@/lib/useScrollReveal";

export function RevealSection({
  id,
  ariaLabelledBy,
  className = "",
  children,
}: {
  id?: string;
  ariaLabelledBy?: string;
  className?: string;
  children: React.ReactNode;
}) {
  const { ref, visible } = useScrollReveal<HTMLElement>();
  return (
    <section
      ref={ref}
      id={id}
      aria-labelledby={ariaLabelledBy}
      className={`transition-all duration-700 ease-out ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      } ${className}`}
    >
      {children}
    </section>
  );
}
