import { RevealSection } from "./RevealSection";

const ARCHETYPES = [
  {
    numeral: "I",
    name: "The Classical Family",
    detail:
      "Trivium-shaped year. Latin and logic respected. Memory work weighted, narration honored. Lessons drafted in the vocabulary of the tradition.",
  },
  {
    numeral: "II",
    name: "The Charlotte Mason Home",
    detail:
      "Living books at the center. Short lessons, nature notebooks, narration over worksheets. The builder writes a week that looks like CM, not a workbook.",
  },
  {
    numeral: "III",
    name: "The Montessori Household",
    detail:
      "Three-period lessons. Concrete to abstract. Child-led work blocks. Practical life is curriculum, not a chore list.",
  },
  {
    numeral: "IV",
    name: "The Trade-Bound Apprentice",
    detail:
      "Academics on a vocational spine. Welding, electrical, automotive, culinary, agriculture. Certification milestones tracked alongside English and math.",
  },
];

export function LandingPhilosophies() {
  return (
    <RevealSection
      ariaLabelledBy="philosophies-headline"
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
            The Traditions
          </p>
          <h2
            id="philosophies-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-white tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.4vw,68px)] mb-5"
          >
            Every family teaches differently.{" "}
            <span className="gold-em">METHEAN honors all of them.</span>
          </h2>
          <p className="font-[family-name:var(--font-cormorant)] italic text-[20px] leading-[1.55] text-white/70">
            The curriculum builder writes in your tradition's vocabulary, paces by your tradition's
            rhythm, and proposes the kind of work your tradition values.
          </p>
        </div>

        <ul className="grid grid-cols-1 min-[540px]:grid-cols-2 min-[900px]:grid-cols-4 gap-4">
          {ARCHETYPES.map((a) => (
            <li
              key={a.numeral}
              className="group bg-[var(--navy)] border border-white/[0.06] rounded-[10px] p-7 transition-all duration-300 hover:bg-[var(--navy-soft)] hover:border-[rgba(198,162,78,0.25)]"
            >
              <div
                aria-hidden="true"
                className="font-[family-name:var(--font-cormorant)] italic text-[var(--gold)] text-[40px] leading-none mb-5"
              >
                {a.numeral}
              </div>
              <h3 className="font-[family-name:var(--font-cormorant)] text-white text-[22px] font-medium mb-3 leading-tight">
                {a.name}
              </h3>
              <p className="text-[14px] leading-[1.65] text-white/60">{a.detail}</p>
            </li>
          ))}
        </ul>
      </div>
    </RevealSection>
  );
}
