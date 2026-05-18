import { CheckIcon } from "./icons";

const NAV_ITEMS = ["Dashboard", "Plans", "Compliance"];
const CHILDREN = [
  { initial: "A", mastery: "82%" },
  { initial: "J", mastery: "74%" },
  { initial: "M", mastery: "91%" },
];
const WEEK_PLAN = [
  "Math: Long division",
  "Reading: Charlotte's Web ch. 8-10",
  "Science: Photosynthesis lab",
];
const APPROVALS = [
  "Update Jonah's reading philosophy",
  "Add new state hours target",
];

export function LandingProductPreview() {
  return (
    <section className="fade-up px-6 py-24" style={{ background: "#0F1B2D" }}>
      <div className="max-w-[1100px] mx-auto">
        <p className="text-[13px] uppercase tracking-[0.1em] text-white/60 text-center mb-3">
          What It Looks Like
        </p>
        <h2 className="text-[28px] sm:text-[32px] font-semibold text-white text-center tracking-tight mb-12">
          A single screen for the whole family.
        </h2>

        {/* Browser-style frame */}
        <div
          className="mx-auto max-w-[920px] rounded-[20px] border border-white/10 overflow-hidden shadow-2xl"
          style={{ background: "#1A2740" }}
          role="img"
          aria-label="Preview of the METHEAN parent dashboard"
        >
          {/* Title bar */}
          <div className="flex items-center gap-2 px-5 py-3 border-b border-white/[0.06]">
            <span className="w-2 h-2 rounded-full" style={{ background: "#E66E6E" }} aria-hidden="true" />
            <span className="w-2 h-2 rounded-full" style={{ background: "#E5C04E" }} aria-hidden="true" />
            <span className="w-2 h-2 rounded-full" style={{ background: "#5BB97D" }} aria-hidden="true" />
            <span className="ml-3 text-[11px] text-white/40">app.methean.io / dashboard</span>
          </div>

          {/* Body */}
          <div className="flex">
            {/* Sidebar (hidden on mobile) */}
            <aside
              className="hidden md:flex flex-col gap-2 p-4 border-r border-white/[0.06] w-[160px] shrink-0"
              aria-hidden="true"
            >
              {NAV_ITEMS.map((label, i) => (
                <div
                  key={label}
                  className="px-3 py-2 rounded-[8px] text-[12px]"
                  style={{
                    background: i === 0 ? "rgba(198,162,78,0.10)" : "transparent",
                    color: i === 0 ? "#C6A24E" : "rgba(255,255,255,0.55)",
                    fontWeight: i === 0 ? 500 : 400,
                  }}
                >
                  {label}
                </div>
              ))}
            </aside>

            {/* Main content */}
            <div className="flex-1 p-5 sm:p-7">
              {/* Child avatars */}
              <div className="flex items-end justify-around sm:justify-start sm:gap-10 mb-6">
                {CHILDREN.map((c) => (
                  <div key={c.initial} className="flex flex-col items-center">
                    <div
                      className="w-12 h-12 rounded-full flex items-center justify-center text-white text-[15px] font-medium"
                      style={{ background: "rgba(74,111,165,0.35)" }}
                    >
                      {c.initial}
                    </div>
                    <p className="text-[11px] mt-1.5" style={{ color: "#C6A24E" }}>
                      {c.mastery}
                    </p>
                  </div>
                ))}
              </div>

              {/* Two-column grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Week plan */}
                <div className="rounded-[12px] p-4 border border-white/[0.06]" style={{ background: "#142036" }}>
                  <p className="text-[12px] text-white/55 uppercase tracking-wide mb-3">
                    This Week's Plan
                  </p>
                  <ul className="space-y-2.5">
                    {WEEK_PLAN.map((item) => (
                      <li key={item} className="flex items-start gap-2 text-[12px] text-white/85">
                        <span style={{ color: "#5BB97D" }} className="mt-[2px]">
                          <CheckIcon size={14} />
                        </span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Approvals */}
                <div className="rounded-[12px] p-4 border border-white/[0.06]" style={{ background: "#142036" }}>
                  <p className="text-[12px] text-white/55 uppercase tracking-wide mb-3">
                    Pending Your Approval
                  </p>
                  <ul className="space-y-3">
                    {APPROVALS.map((item) => (
                      <li key={item} className="flex flex-col gap-2">
                        <span className="text-[12px] text-white/85">{item}</span>
                        <div className="flex gap-1.5">
                          <span
                            className="px-2 py-1 rounded-[6px] text-[10px] font-medium"
                            style={{ background: "#C6A24E", color: "#0F1B2D" }}
                          >
                            Approve
                          </span>
                          <span
                            className="px-2 py-1 rounded-[6px] text-[10px] font-medium text-white/70 border border-white/15"
                          >
                            Adjust
                          </span>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Progress bar */}
              <div className="mt-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] text-white/55 uppercase tracking-wide">
                    Week 12 progress
                  </span>
                  <span className="text-[11px] text-white/55">65%</span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.08)" }}>
                  <div className="h-full" style={{ width: "65%", background: "#C6A24E" }} />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Captions */}
        <div className="mt-10 grid grid-cols-1 sm:grid-cols-3 gap-4 text-center max-w-[820px] mx-auto">
          <p className="text-[14px] text-white/60">Multi-child overview, one screen.</p>
          <p className="text-[14px] text-white/60">Pending approvals always visible.</p>
          <p className="text-[14px] text-white/60">Mastery and compliance update in real time.</p>
        </div>
      </div>
    </section>
  );
}
