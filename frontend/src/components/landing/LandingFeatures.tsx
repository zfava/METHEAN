import Card from "@/components/ui/Card";
import {
  FeatureChart,
  FeatureDoc,
  FeatureFamily,
  FeatureLightbulb,
  FeatureShield,
  FeatureWrench,
} from "./icons";

const FEATURES = [
  {
    icon: <FeatureShield />,
    title: "Your Educational Philosophy",
    body: "Classical, Charlotte Mason, Montessori, traditional. Every lesson respects your approach, not ours.",
  },
  {
    icon: <FeatureDoc />,
    title: "All 50 States Plus DC",
    body: "Hour tracking, mastery records, and required state documents generated automatically.",
  },
  {
    icon: <FeatureFamily />,
    title: "Built for Multi-Kid Families",
    body: "Unlimited children. Each tracked separately, all visible on one screen.",
  },
  {
    icon: <FeatureChart />,
    title: "Mastery Over Memorization",
    body: "The system remembers what your child has learned and brings back what they're forgetting. No grade levels. No busywork.",
  },
  {
    icon: <FeatureWrench />,
    title: "Trades and Apprenticeships",
    body: "Welding, electrical, automotive, and other vocational paths. Certification milestones tracked alongside academics.",
  },
  {
    icon: <FeatureLightbulb />,
    title: "Optional Child Tutor",
    body: "An AI tutor your child can talk to, only if you turn it on. Themed for their age. Always inside your rules.",
  },
];

export function LandingFeatures() {
  return (
    <section id="features" className="fade-up px-6 py-24 scroll-mt-24" style={{ background: "#0F1B2D" }}>
      <div className="max-w-[1100px] mx-auto">
        <p className="text-[13px] uppercase tracking-[0.1em] text-white/60 text-center mb-3">
          Features
        </p>
        <h2 className="text-[22px] sm:text-[28px] font-medium text-white text-center max-w-[600px] mx-auto mb-12 tracking-tight">
          Navigate your family's education with confidence.
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card padding="p-7" className="md:row-span-2">
            <div className="mb-3 text-[color:var(--gold)]">
              <FeatureShield />
            </div>
            <h3 className="text-(--color-text) font-medium text-[17px] mb-2">Parent Sovereignty</h3>
            <p className="text-(--color-text-secondary) text-[14px] leading-relaxed">
              You set rules the AI cannot override. The system enforces them on every
              recommendation. Every decision logged. Full transparency.
            </p>
          </Card>
          {FEATURES.map((f) => (
            <Card key={f.title} padding="p-6">
              <div className="mb-2 text-[color:var(--gold)]">{f.icon}</div>
              <h3 className="text-(--color-text) font-medium text-[15px] mb-1">{f.title}</h3>
              <p className="text-(--color-text-secondary) text-[13px] leading-relaxed">{f.body}</p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
