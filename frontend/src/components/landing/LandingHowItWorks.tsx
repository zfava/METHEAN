import { RevealSection } from "./RevealSection";

const STEPS = [
  {
    num: "01",
    title: "Set your rules.",
    body: "Choose your educational philosophy. Define the boundaries the AI cannot cross. Set how much authority you delegate. METHEAN encodes your decisions as constitutional rules the system honors on every call.",
  },
  {
    num: "02",
    title: "AI proposes, you approve.",
    body: "METHEAN drafts curriculum, weekly plans, and teaching prompts tailored to your family. Every recommendation routes through your governance rules before reaching your child. Nothing happens without your authorization.",
  },
  {
    num: "03",
    title: "Watch mastery grow.",
    body: "The system tracks what each child has actually learned and remembers what they're forgetting. A family at month three gets a noticeably different experience than day one. METHEAN learns alongside you.",
  },
];

export function LandingHowItWorks() {
  return (
    <RevealSection
      id="how"
      ariaLabelledBy="how-headline"
      className="parchment-noise bg-[var(--parchment)] py-[120px] sm:py-[160px] px-6 scroll-mt-24"
    >
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center mb-20 max-w-[800px] mx-auto">
          <span
            aria-hidden="true"
            className="mx-auto block h-[2px] w-8 bg-[var(--gold-deep)] mb-6"
          />
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-text)] mb-6">
            The Path
          </p>
          <h2
            id="how-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.6vw,72px)]"
          >
            From a blank page to a year, <span className="gold-em">in three deliberate steps.</span>
          </h2>
        </div>

        <ol className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {STEPS.map((step) => (
            <li key={step.num} className="text-center lg:text-left">
              <div
                aria-hidden="true"
                className="font-[family-name:var(--font-cormorant)] italic text-[clamp(56px,6vw,72px)] text-[var(--gold-deep)] leading-none mb-6"
              >
                {step.num}.
              </div>
              <h3 className="font-[family-name:var(--font-cormorant)] text-[28px] text-[var(--navy)] font-medium mb-4 leading-[1.15]">
                {step.title}
              </h3>
              <p className="text-[16px] leading-[1.75] text-[var(--ink-soft)]">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </RevealSection>
  );
}
