const STEPS = [
  {
    num: "01",
    title: "Set Your Rules.",
    body: "Choose your educational philosophy. Define the boundaries the AI cannot cross. Set how much authority you delegate. METHEAN encodes your decisions as constitutional rules the system honors on every call.",
  },
  {
    num: "02",
    title: "AI Proposes, You Approve.",
    body: "METHEAN drafts curriculum, weekly plans, and teaching prompts tailored to your family. Every recommendation routes through your governance rules before reaching your child. Nothing happens without your authorization.",
  },
  {
    num: "03",
    title: "Watch Mastery Grow.",
    body: "The system tracks what each child has actually learned and remembers what they're forgetting. A family at month three gets a noticeably different experience than day one. METHEAN learns alongside you.",
  },
];

export function LandingHowItWorks() {
  return (
    <section id="how-it-works" className="fade-up py-24 px-6 bg-(--color-page) scroll-mt-24">
      <div className="max-w-[1100px] mx-auto">
        <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) text-center mb-3">
          How It Works
        </p>
        <h2 className="text-[22px] sm:text-[28px] font-medium text-(--color-text) text-center mb-12 tracking-tight">
          Three steps to sovereign education.
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {STEPS.map((s) => (
            <div
              key={s.num}
              className="bg-(--color-surface) rounded-[16px] p-7 border border-(--color-border)"
            >
              <div className="relative w-14 h-14 mb-4">
                <div
                  className="absolute inset-0 rounded-full"
                  style={{ background: "rgba(74,111,165,0.08)" }}
                />
                <span className="absolute inset-0 flex items-center justify-center text-[28px] font-bold text-(--color-accent)">
                  {s.num}
                </span>
              </div>
              <h3 className="text-[17px] font-semibold text-(--color-text) mb-2">{s.title}</h3>
              <p className="text-[14px] text-(--color-text-secondary) leading-relaxed">{s.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
