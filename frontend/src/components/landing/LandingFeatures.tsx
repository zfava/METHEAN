import { RevealSection } from "./RevealSection";
import {
  CalendarGrid,
  FamilyFour,
  FlagDoc,
  MasteryChart,
  PhilosophyBook,
  ShieldCheck,
  TradeWrench,
  TutorChat,
} from "./icons";

const SMALL_CARDS = [
  {
    numeral: "II.",
    icon: <PhilosophyBook size={26} />,
    title: "Your Philosophy",
    body: "Classical, Charlotte Mason, Montessori, Traditional, Trade. The builder writes in your tradition's vocabulary and pace.",
  },
  {
    numeral: "III.",
    icon: <CalendarGrid size={26} />,
    title: "The Curriculum Builder",
    body: "Thirty-six weeks per subject, Monday through Friday with built-in review weeks. Drafted in minutes, refined over years, every block parent-approved before it reaches your child.",
  },
  {
    numeral: "IV.",
    icon: <FlagDoc size={26} />,
    title: "All 51 Jurisdictions",
    body: "All 50 states and Washington DC. Hour tracking, mastery records, and required documents generated on schedule.",
  },
  {
    numeral: "V.",
    icon: <FamilyFour size={26} />,
    title: "Multi-Child Families",
    body: "Unlimited children, one subscription. Each child tracked separately. All of them visible on one screen.",
  },
  {
    numeral: "VI.",
    icon: <MasteryChart size={26} />,
    title: "Mastery Over Memorization",
    body: "The system remembers what your child has learned and surfaces what they are forgetting. No grade levels. No busywork.",
  },
  {
    numeral: "VII.",
    icon: <TradeWrench size={26} />,
    title: "Trades and Apprenticeships",
    body: "Welding, electrical, automotive, culinary, agriculture. Certification milestones tracked alongside academics.",
  },
  {
    numeral: "VIII.",
    icon: <TutorChat size={26} />,
    title: "Optional Child Tutor",
    body: "An AI tutor your child can talk to, only if you turn it on. Themed for their age. Always inside your rules.",
  },
];

export function LandingFeatures() {
  return (
    <RevealSection
      id="features"
      ariaLabelledBy="features-headline"
      className="parchment-noise bg-[var(--parchment)] py-[120px] sm:py-[160px] px-6 scroll-mt-24"
    >
      <div className="max-w-[1200px] mx-auto">
        <div className="text-center max-w-[820px] mx-auto mb-16">
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-text)] mb-6">
            The Capabilities
          </p>
          <h2
            id="features-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.4vw,68px)]"
          >
            Eight working parts. <span className="gold-em">One operating system.</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 min-[540px]:grid-cols-2 min-[900px]:grid-cols-3 gap-4">
          {/* Large Parent Sovereignty card */}
          <article className="dark-noise relative min-[900px]:row-span-2 rounded-[14px] overflow-hidden p-8 sm:p-10 bg-[var(--navy)] border border-white/[0.06]">
            <div className="relative z-10 flex flex-col h-full">
              <div className="text-[var(--gold)] mb-6">
                <ShieldCheck size={36} />
              </div>
              <p
                aria-hidden="true"
                className="font-[family-name:var(--font-cormorant)] italic text-[var(--gold-soft)] text-[40px] leading-none mb-4"
              >
                I.
              </p>
              <h3 className="font-[family-name:var(--font-cormorant)] text-white text-[30px] font-medium leading-tight mb-5">
                Parent Sovereignty
              </h3>
              <p className="text-[16px] leading-[1.7] text-white/[0.78]">
                Constitutional rules the AI cannot override. Every recommendation routes through
                your governance first. Every decision logged. Every override recorded. Full
                transparency by structural choice, not by promise.
              </p>
            </div>
          </article>

          {SMALL_CARDS.map((c) => (
            <article
              key={c.title}
              className="group rounded-[14px] p-7 bg-[var(--cream-warm)] border border-[rgba(166,132,58,0.18)] transition-all duration-300 hover:bg-white hover:border-[var(--gold)] hover:-translate-y-[3px] hover:shadow-[0_14px_36px_rgba(15,27,45,0.10)]"
            >
              <div className="text-[var(--gold-deep)] mb-5">{c.icon}</div>
              <p
                aria-hidden="true"
                className="font-[family-name:var(--font-cormorant)] italic text-[var(--gold-deep)] text-[28px] leading-none mb-3"
              >
                {c.numeral}
              </p>
              <h3 className="font-[family-name:var(--font-cormorant)] text-[var(--navy)] text-[22px] font-medium leading-tight mb-3">
                {c.title}
              </h3>
              <p className="text-[15px] leading-[1.7] text-[var(--ink-soft)]">{c.body}</p>
            </article>
          ))}
        </div>
      </div>
    </RevealSection>
  );
}
