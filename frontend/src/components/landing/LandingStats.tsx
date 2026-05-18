import { RevealSection } from "./RevealSection";

const STATS = [
  { value: "51 / 51", label: "Jurisdictions, including DC" },
  { value: "220+", label: "API endpoints, parent-governed" },
  { value: "49 / 51", label: "Isolated tables, full RLS" },
  { value: "8", label: "AI roles, every one constrained" },
];

export function LandingStats() {
  return (
    <RevealSection
      ariaLabelledBy="stats-headline"
      className="dark-noise relative border-t border-b border-[rgba(198,162,78,0.15)] py-[120px] sm:py-[160px] px-6"
      // bg via inline style to ensure tokens resolve
    >
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-0"
        style={{ background: "var(--navy)" }}
      />
      <div className="relative max-w-[1200px] mx-auto">
        <div className="text-center max-w-[820px] mx-auto mb-20">
          <span
            aria-hidden="true"
            className="mx-auto block h-[2px] w-8 bg-[var(--gold)] mb-6"
          />
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold)] mb-6">
            The Build
          </p>
          <h2
            id="stats-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-white tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.6vw,72px)]"
          >
            Built like infrastructure. <span className="gold-em">Because it is.</span>
          </h2>
        </div>

        <dl className="grid grid-cols-2 md:grid-cols-4 gap-y-12">
          {STATS.map((s, i) => (
            <div
              key={s.label}
              className={`text-center px-4 ${
                i < STATS.length - 1 ? "md:border-r md:border-[rgba(198,162,78,0.18)]" : ""
              }`}
            >
              <dt className="sr-only">{s.label}</dt>
              <dd className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--gold-soft)] text-[clamp(44px,5vw,64px)] leading-none mb-4">
                {s.value}
              </dd>
              <dd className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.18em] text-white/60 leading-snug max-w-[200px] mx-auto">
                {s.label}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </RevealSection>
  );
}
