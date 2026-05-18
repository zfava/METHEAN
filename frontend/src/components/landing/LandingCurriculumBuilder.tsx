import { RevealSection } from "./RevealSection";

type ActivityKind = "Lesson" | "Practice" | "Review" | "Assessment" | "Project";
type ActivityStatus = "APPROVED" | "PENDING";

interface Activity {
  kind: ActivityKind;
  name: string;
  minutes: number;
  status: ActivityStatus;
}

const WEEK: Array<{ day: string; items: Activity[] }> = [
  {
    day: "Mon",
    items: [
      { kind: "Lesson", name: "Introduction to long division", minutes: 25, status: "APPROVED" },
      { kind: "Practice", name: "3-digit ÷ 1-digit, manipulatives", minutes: 20, status: "APPROVED" },
    ],
  },
  {
    day: "Tue",
    items: [
      { kind: "Practice", name: "Multi-step problems, written", minutes: 25, status: "APPROVED" },
      { kind: "Review", name: "Multiplication tables, sixes", minutes: 10, status: "PENDING" },
    ],
  },
  {
    day: "Wed",
    items: [
      { kind: "Lesson", name: "Long division with remainders", minutes: 30, status: "APPROVED" },
      { kind: "Practice", name: "Word problems, classical", minutes: 15, status: "APPROVED" },
    ],
  },
  {
    day: "Thu",
    items: [
      { kind: "Practice", name: "Mixed practice set", minutes: 25, status: "PENDING" },
      { kind: "Project", name: "Build a division story", minutes: 20, status: "PENDING" },
    ],
  },
  {
    day: "Fri",
    items: [
      { kind: "Assessment", name: "Week 12 mastery check", minutes: 30, status: "APPROVED" },
      { kind: "Review", name: "Concept consolidation", minutes: 15, status: "APPROVED" },
    ],
  },
];

const PILLARS = [
  {
    numeral: "I.",
    title: "A full year, drafted at once.",
    body: "Thirty-six weeks per subject, sequenced for your philosophy, balanced across Lesson, Practice, Review, and Project. The first draft is generated in minutes. The rest of the year is yours to refine.",
  },
  {
    numeral: "II.",
    title: "Bring the books you already own.",
    body: "Sonlight, Saxon, My Father's World, Abeka, BJU, Singapore. METHEAN tracks mastery from whatever curriculum you log, so the year you have already paid for gets stronger, not replaced.",
  },
  {
    numeral: "III.",
    title: "Your philosophy, in every lesson.",
    body: "Classical, Charlotte Mason, Montessori, Traditional, and Trade-bound modes shape vocabulary, pace, and the kind of work proposed. The builder writes for your tradition, not ours.",
  },
];

const STATS = [
  { value: "29,956", label: "Lines of pre-built curriculum content" },
  { value: "36", label: "Weeks of scope per subject" },
  { value: "4", label: "Philosophies honored natively" },
  { value: "100%", label: "Parent-approved before child sees" },
];

function ActivityCard({ activity }: { activity: Activity }) {
  const pending = activity.status === "PENDING";
  return (
    <div
      className={`rounded-[6px] px-3 py-2.5 border ${
        pending
          ? "bg-[rgba(198,162,78,0.05)] border-[rgba(198,162,78,0.15)] border-l-2 border-l-[var(--gold)]"
          : "bg-white/[0.03] border-white/[0.06] border-l-2 border-l-[rgba(45,106,79,0.6)]"
      }`}
    >
      <span className="inline-block font-[family-name:var(--font-jetbrains)] text-[9px] uppercase tracking-[0.16em] text-[var(--gold-soft)] bg-[rgba(198,162,78,0.08)] px-1.5 py-[2px] rounded-[3px] mb-1.5">
        {activity.kind}
      </span>
      <p className="text-[12px] text-white/[0.88] leading-snug font-medium">{activity.name}</p>
      <div className="mt-2 flex items-center justify-between font-[family-name:var(--font-jetbrains)] text-[9.5px] uppercase tracking-[0.12em]">
        <span className="text-white/40">{activity.minutes} min</span>
        <span className={pending ? "text-[var(--gold)]" : "text-white/35"}>{activity.status}</span>
      </div>
    </div>
  );
}

export function LandingCurriculumBuilder() {
  return (
    <RevealSection
      ariaLabelledBy="curriculum-headline"
      className="parchment-noise bg-[var(--cream-warm)] py-[120px] sm:py-[160px] px-4 sm:px-6"
    >
      <div className="max-w-[1200px] mx-auto">
        {/* Section header */}
        <div className="text-center max-w-[820px] mx-auto mb-16">
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-deep)] mb-6">
            The Curriculum Builder
          </p>
          <h2
            id="curriculum-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.05] text-[clamp(40px,5.4vw,64px)] mb-6"
          >
            Your year, drafted in minutes. <span className="gold-em">Refined over years.</span>
          </h2>
          <p className="font-[family-name:var(--font-cormorant)] italic text-[20px] sm:text-[22px] leading-[1.55] text-[var(--ink-soft)]">
            Thirty-six weeks of complete, philosophy-aware curriculum, generated for each subject
            and each child, then routed through your approval before it ever reaches their day.
          </p>
        </div>

        {/* Week view mockup */}
        <div className="relative max-w-[1040px] mx-auto my-16 sm:my-20">
          {/* Radial gold glow halo */}
          <div
            aria-hidden="true"
            className="absolute -inset-12 pointer-events-none"
            style={{
              background:
                "radial-gradient(ellipse at center, rgba(198,162,78,0.14) 0%, rgba(198,162,78,0) 65%)",
            }}
          />

          <div
            className="dark-noise relative rounded-2xl overflow-hidden border border-[rgba(198,162,78,0.18)] shadow-[0_30px_80px_rgba(15,27,45,0.18),0_8px_20px_rgba(15,27,45,0.10)]"
            style={{ background: "var(--navy)" }}
            role="img"
            aria-label="METHEAN Curriculum Builder, week 12 of Mathematics Year 5"
          >
            {/* Header row */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 px-6 sm:px-8 py-6 border-b border-white/[0.06]">
              <div>
                <p className="font-[family-name:var(--font-cormorant)] text-white text-[22px] leading-tight">
                  Mathematics, Year 5 · Avery · Classical
                </p>
                <p className="mt-1 font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-[var(--gold-soft)]">
                  Week 12 of 36 · Long Division
                </p>
              </div>
              <div className="inline-flex items-center gap-2 self-start sm:self-auto rounded-full bg-[rgba(198,162,78,0.12)] border border-[rgba(198,162,78,0.30)] px-3 py-1.5">
                <span
                  aria-hidden="true"
                  className="animate-pulse-dot w-1.5 h-1.5 rounded-full bg-[var(--gold)]"
                />
                <span className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.14em] text-[var(--gold)]">
                  3 pending your approval
                </span>
              </div>
            </div>

            {/* Week grid */}
            <div
              className="grid gap-px"
              style={{
                background: "rgba(255,255,255,0.04)",
                gridTemplateColumns: "repeat(1, 1fr)",
              }}
            >
              <div className="grid gap-px min-[540px]:grid-cols-2 min-[900px]:grid-cols-5">
                {WEEK.map((d) => (
                  <div
                    key={d.day}
                    className="bg-[var(--navy)] px-3.5 py-5 min-h-[220px]"
                  >
                    <p className="border-b border-white/[0.05] pb-2 mb-3 font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.18em] text-white/40">
                      {d.day}
                    </p>
                    <div className="space-y-2.5">
                      {d.items.map((act) => (
                        <ActivityCard key={`${d.day}-${act.name}`} activity={act} />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Footer row */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 px-6 sm:px-8 py-5 border-t border-white/[0.06]">
              <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.14em] text-white/55">
                Next: <strong className="text-[var(--gold)] font-medium">Week 13 · Review Week</strong>
              </p>
              <div className="flex items-center gap-2">
                <span className="rounded-full bg-[var(--gold)] text-[var(--navy)] px-3.5 py-1.5 font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.14em] font-medium">
                  Approve All Pending
                </span>
                <span className="rounded-full border border-white/15 text-white/70 px-3.5 py-1.5 font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.14em]">
                  Adjust Plan
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Editorial blocks */}
        <ol className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-24 max-w-[1080px] mx-auto">
          {PILLARS.map((p) => (
            <li key={p.numeral} className="text-center md:text-left max-w-[320px] mx-auto">
              <div
                aria-hidden="true"
                className="font-[family-name:var(--font-cormorant)] italic text-[var(--gold-deep)] text-[48px] leading-none mb-3"
              >
                {p.numeral}
              </div>
              <span
                aria-hidden="true"
                className="block h-[1px] w-10 bg-[var(--gold-deep)] opacity-50 mx-auto md:mx-0 mb-6"
              />
              <h3 className="font-[family-name:var(--font-cormorant)] text-[26px] text-[var(--navy)] font-medium leading-[1.2] mb-3">
                {p.title}
              </h3>
              <p className="text-[16px] leading-[1.7] text-[var(--ink-soft)]">{p.body}</p>
            </li>
          ))}
        </ol>

        {/* Stats band */}
        <div className="border-t border-b border-[rgba(166,132,58,0.25)] py-10">
          <dl className="grid grid-cols-2 md:grid-cols-4 gap-y-8">
            {STATS.map((s, i) => (
              <div
                key={s.label}
                className={`text-center px-4 ${
                  i < STATS.length - 1
                    ? "md:border-r md:border-[rgba(166,132,58,0.18)]"
                    : ""
                }`}
              >
                <dt className="sr-only">{s.label}</dt>
                <dd className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--gold-deep)] text-[clamp(36px,4.5vw,56px)] leading-none mb-3">
                  {s.value}
                </dd>
                <dd className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.16em] text-[var(--ink-mute)] leading-snug max-w-[180px] mx-auto">
                  {s.label}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </RevealSection>
  );
}
