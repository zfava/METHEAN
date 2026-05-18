import { ChevronIcon } from "./icons";

const FAQS: Array<{ q: string; a: string }> = [
  {
    q: "Does METHEAN work in my state?",
    a: "Yes. All 50 states and Washington DC are supported with automatic hour tracking, mastery records, and document generation matched to each state's homeschool requirements.",
  },
  {
    q: "Can I use METHEAN alongside my existing curriculum?",
    a: "Yes. If you already use Sonlight, Saxon, My Father's World, Abeka, BJU, or any other curriculum, METHEAN tracks mastery from any source you log and complements rather than replaces your current materials.",
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
    a: "Yes. We never sell data. We never use child data for advertising. Your family's information stays in your household. Full export and deletion are available at any time.",
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

export function LandingFAQ() {
  return (
    <section id="faq" className="fade-up py-24 px-6 bg-(--color-page) scroll-mt-24">
      <div className="max-w-[720px] mx-auto">
        <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) text-center mb-3">
          Frequently Asked
        </p>
        <h2 className="text-[28px] sm:text-[32px] font-semibold text-(--color-text) text-center tracking-tight mb-12">
          Questions families ask before they sign up.
        </h2>
        <div>
          {FAQS.map((item) => (
            <details
              key={item.q}
              className="group border-b border-(--color-border) py-5 px-1 focus-within:ring-2 focus-within:ring-(--gold)/40 rounded-sm"
            >
              <summary className="flex items-center justify-between gap-4 cursor-pointer list-none text-[17px] font-medium text-(--color-text) focus:outline-none">
                <h3 className="text-[17px] font-medium text-(--color-text)">{item.q}</h3>
                <span className="text-(--color-text-tertiary) transition-transform duration-200 group-open:rotate-90 shrink-0">
                  <ChevronIcon size={16} />
                </span>
              </summary>
              <p className="mt-3 text-[15px] text-(--color-text-secondary) leading-relaxed">
                {item.a}
              </p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}
