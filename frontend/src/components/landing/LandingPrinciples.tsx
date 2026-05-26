import { RevealSection } from "./RevealSection";

const PRINCIPLES = [
  {
    numeral: "I.",
    title: "Parents govern. AI serves.",
    body: "The hierarchy is not negotiable. Every recommendation, every lesson, every proposal routes through your authority first. The AI is a draftsman. You are the editor in chief.",
  },
  {
    numeral: "II.",
    title: "Every decision is auditable.",
    body: "Nothing happens in a black box. Each governance rule, each AI proposal, and each parent override is logged with timestamps and reasoning. Open the trail anytime.",
  },
  {
    numeral: "III.",
    title: "Your data stays in your household.",
    body: "We never sell your data. We never train models on your child's work. Full export and deletion are one click. Sovereignty is structural, not promotional.",
  },
];

export function LandingPrinciples() {
  return (
    <RevealSection
      id="manifesto"
      ariaLabelledBy="manifesto-headline"
      className="parchment-noise bg-[var(--parchment)] py-[120px] sm:py-[160px] px-6 scroll-mt-24"
    >
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center max-w-[820px] mx-auto mb-20">
          <span
            aria-hidden="true"
            className="mx-auto block h-[2px] w-8 bg-[var(--gold-deep)] mb-6"
          />
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-text)] mb-6">
            The Charter
          </p>
          <h2
            id="manifesto-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.6vw,72px)]"
          >
            Three principles, <span className="gold-em">written before</span> a single line of code.
          </h2>
        </div>

        <ol className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-10 max-w-[1100px] mx-auto">
          {PRINCIPLES.map((p) => (
            <li key={p.numeral} className="text-center md:text-left">
              <div
                aria-hidden="true"
                className="font-[family-name:var(--font-cormorant)] italic text-[var(--gold-deep)] text-[clamp(56px,5.5vw,72px)] leading-none mb-4"
              >
                {p.numeral}
              </div>
              <span
                aria-hidden="true"
                className="block h-[1px] w-12 bg-[var(--gold-deep)] opacity-50 mx-auto md:mx-0 mb-6"
              />
              <h3 className="font-[family-name:var(--font-cormorant)] text-[28px] text-[var(--navy)] font-medium mb-4 leading-[1.2]">
                {p.title}
              </h3>
              <p className="text-[16px] leading-[1.75] text-[var(--ink-soft)]">{p.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </RevealSection>
  );
}
