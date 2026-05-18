import { RevealSection } from "./RevealSection";
import { FourPointStar } from "./icons";

const ROWS: Array<{ q: string; them: string; us: string }> = [
  {
    q: "Who decides what your child learns",
    them: "An algorithm, a vendor, a state board",
    us: "You do. Your philosophy is the input. Your approval is the gate.",
  },
  {
    q: "Who builds the year of curriculum",
    them: "You, alone, every Sunday night",
    us: "METHEAN drafts thirty-six weeks per subject. You refine. You approve.",
  },
  {
    q: "What is being tracked",
    them: "Hours logged and lessons completed",
    us: "Mastery, decay, philosophy fit, and compliance, per child.",
  },
  {
    q: "Whose values shape content",
    them: "A nameless committee, somewhere",
    us: "Yours. Classical, Charlotte Mason, Montessori, Traditional, Trade.",
  },
  {
    q: "Who handles state compliance",
    them: "A spreadsheet, hand-maintained",
    us: "All 50 states and DC, document generation included.",
  },
  {
    q: "Where does your data live",
    them: "Sold, brokered, modeled on",
    us: "In your household. We never sell. We never train on child work.",
  },
  {
    q: "Can you see why a decision was made",
    them: "Rarely. The black box stays closed.",
    us: "Always. Every AI proposal logged with its reasoning.",
  },
];

export function LandingComparison() {
  return (
    <RevealSection
      ariaLabelledBy="comparison-headline"
      className="dark-noise relative py-[120px] sm:py-[160px] px-6"
    >
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-0"
        style={{ background: "var(--navy)" }}
      />
      <div className="relative max-w-[1200px] mx-auto">
        <div className="text-center max-w-[860px] mx-auto mb-16">
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold)] mb-6">
            The Difference
          </p>
          <h2
            id="comparison-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-white tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.6vw,68px)]"
          >
            What changes when the family <span className="gold-em">is in charge.</span>
          </h2>
        </div>

        {/* Header row */}
        <div className="hidden md:grid grid-cols-[1.2fr_1fr_1.4fr] gap-x-8 border-b border-white/[0.08] pb-5 mb-2">
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-white/45">
            The Question
          </p>
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-white/45">
            Everyone Else
          </p>
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-[var(--gold-soft)]">
            METHEAN
          </p>
        </div>

        <ul>
          {ROWS.map((row, i) => (
            <li
              key={row.q}
              className={`grid grid-cols-1 md:grid-cols-[1.2fr_1fr_1.4fr] gap-y-3 gap-x-8 py-6 ${
                i < ROWS.length - 1 ? "border-b border-white/[0.06]" : ""
              }`}
            >
              <p className="font-[family-name:var(--font-cormorant)] italic text-[20px] sm:text-[22px] text-white leading-snug">
                {row.q}
              </p>
              <p className="text-[15px] leading-[1.6] text-white/55">
                <span className="text-[var(--ink-faint)] mr-2" aria-hidden="true">
                  ,
                </span>
                {row.them}
              </p>
              <p className="text-[15px] leading-[1.6] text-white">
                <span className="text-[var(--gold)] mr-2 inline-flex align-middle" aria-hidden="true">
                  <FourPointStar size={12} />
                </span>
                {row.us}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </RevealSection>
  );
}
