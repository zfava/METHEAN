const PRINCIPLES = [
  "Parents govern. AI serves.",
  "Every decision is auditable.",
  "Your data stays in your household.",
];

export function LandingPrinciples() {
  return (
    <section className="fade-up py-24 px-6 bg-(--color-page)">
      <div className="max-w-[720px] mx-auto text-center">
        <div
          className="mx-auto h-[2px] w-6 mb-6"
          style={{ background: "var(--gold)" }}
          aria-hidden="true"
        />
        <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) mb-4">
          Built by a Homeschool Family
        </p>
        <h2 className="text-[28px] sm:text-[32px] font-semibold tracking-tight text-(--color-text) mb-10">
          Three principles, written before a single line of code.
        </h2>
        <ul className="space-y-4 max-w-[480px] mx-auto text-left">
          {PRINCIPLES.map((line) => (
            <li
              key={line}
              className="flex items-start gap-3 text-[17px] font-medium text-(--color-text) leading-relaxed"
            >
              <span
                className="mt-2.5 h-1.5 w-1.5 rounded-full shrink-0"
                style={{ background: "var(--gold)" }}
                aria-hidden="true"
              />
              {line}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
