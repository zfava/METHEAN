// Sections render in their final position by default. A subtle CSS-only
// opacity fade-in is applied via the `.section-reveal` class, which uses
// `animation-timeline: view()` where supported and falls back to a no-op
// when not. No JS observer, no translate-y, no zero-height reservation:
// content never disappears and the page never visibly jumps on scroll.
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
  return (
    <section
      id={id}
      aria-labelledby={ariaLabelledBy}
      className={`section-reveal ${className}`}
    >
      {children}
    </section>
  );
}
