import { RevealSection } from "./RevealSection";

const FAQS: Array<{ q: string; a: string }> = [
  {
    q: "Does METHEAN work in my state?",
    a: "Yes. All 50 states and Washington DC are supported with automatic hour tracking, mastery records, and document generation matched to each state's homeschool requirements.",
  },
  {
    q: "Can I use METHEAN alongside my existing curriculum?",
    a: "Yes. If you already use Sonlight, Saxon, My Father's World, Abeka, BJU, or another curriculum, METHEAN tracks mastery from any source you log and complements rather than replaces your current materials.",
  },
  {
    q: "Walk me through the Curriculum Builder.",
    a: "Pick a child, a subject, and your educational philosophy. METHEAN drafts thirty-six weeks of lessons, practice, review, and projects, paced Monday through Friday with built-in review weeks. Every activity is generated in your philosophy's voice. Nothing reaches your child until you have approved it. You can refine, swap, lock, or pause any block at any time.",
  },
  {
    q: "What ages does METHEAN support?",
    a: "Kindergarten through twelfth grade today. Pre-K and adult learner modes are on the near-term roadmap.",
  },
  {
    q: "Will METHEAN work for my child with dyslexia, ADHD, or other neurodivergence?",
    a: "METHEAN does not replace specialist evaluation, but the mastery-based progression removes the grade-level pressure that many neurodivergent families find unhelpful. Your child moves at their own pace, in their own depth, on their own time.",
  },
  {
    q: "How much screen time does METHEAN require?",
    a: "As little as you want. Many families use METHEAN entirely as a parent-side planning and tracking tool, and their children never look at the screen. Other families enable the optional AI tutor for older kids. The choice is yours, every day, for every child.",
  },
  {
    q: "Is my family's data private?",
    a: "Yes. We never sell data. We never use child data for advertising. We never train models on your child's work. Your family's information stays in your household. Full export and deletion are available at any time.",
  },
  {
    q: "Do I need to be technically inclined to use METHEAN?",
    a: "No. If you can send email and use a web browser, you can use METHEAN. Onboarding is guided. Support is available.",
  },
  {
    q: "How many children does one subscription cover?",
    a: "Unlimited. One household, one subscription, every child included.",
  },
  {
    q: "Can I cancel?",
    a: "Yes. Cancel anytime from your account settings. No questions, no fees, no retention pressure.",
  },
  {
    q: "What about high school transcripts and college applications?",
    a: "METHEAN generates high school transcripts on demand, tracks credit hours per subject, and exports records in standard formats accepted by colleges and universities.",
  },
];

function PlusMorph() {
  return (
    <span
      aria-hidden="true"
      className="relative inline-block w-7 h-7 shrink-0 text-[var(--gold-deep)]"
    >
      <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[14px] h-[1.5px] bg-current transition-all duration-300 group-open:w-[18px] group-open:h-[2px]" />
      <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[14px] w-[1.5px] bg-current transition-all duration-300 group-open:rotate-90 group-open:opacity-0" />
    </span>
  );
}

export function LandingFAQ() {
  return (
    <RevealSection
      id="faq"
      ariaLabelledBy="faq-headline"
      className="parchment-noise bg-[var(--parchment)] py-[120px] sm:py-[160px] px-6 scroll-mt-24"
    >
      <div className="max-w-[820px] mx-auto">
        <div className="text-center mb-12">
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-text)] mb-6">
            Before You Begin
          </p>
          <h2
            id="faq-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.4vw,64px)]"
          >
            Questions families ask <span className="gold-em">before they sign up.</span>
          </h2>
        </div>

        <div>
          {FAQS.map((item, i) => (
            <details
              key={item.q}
              className={`group border-t border-[rgba(15,27,45,0.12)] py-7 px-2 ${
                i === FAQS.length - 1 ? "border-b" : ""
              }`}
            >
              <summary className="cinematic-focus list-none cursor-pointer flex items-start justify-between gap-6 focus:outline-none">
                <h3 className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] text-[22px] sm:text-[24px] leading-snug">
                  {item.q}
                </h3>
                <PlusMorph />
              </summary>
              <p className="mt-4 font-[family-name:var(--font-cormorant)] text-[17px] leading-[1.7] text-[var(--ink-soft)] max-w-[680px]">
                {item.a}
              </p>
            </details>
          ))}
        </div>
      </div>
    </RevealSection>
  );
}
