"use client";

import { useEffect, useState } from "react";
import { educationPlan, annualCurriculum } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

const POST_GRAD_PATHS = [
  { value: "college_prep", label: "College Prep", desc: "Four-year university track" },
  { value: "vocational", label: "Vocational / Trades", desc: "Apprenticeship or trade school" },
  { value: "entrepreneurial", label: "Entrepreneurial", desc: "Business, self-directed" },
  { value: "undecided", label: "Undecided", desc: "Keeping options open" },
];

const COLLEGE_LEVELS = ["Standard", "Honors", "AP-equivalent"];

const TARGET_SKILLS = [
  "Critical thinking", "Public speaking", "Leadership", "Financial literacy",
  "Foreign language", "STEM", "Arts", "Athletics", "Trade skills",
  "Writing", "Research", "Community service", "Technology",
];

const LEVEL_OPTIONS = ["Below grade", "At grade", "Above grade", "Well above grade"];
const PRIOR_ED = ["Always homeschooled", "Transitioned from public school", "Transitioned from private school", "Hybrid"];

function MultiInput({ items, onChange, placeholder }: { items: string[]; onChange: (v: string[]) => void; placeholder: string }) {
  const [val, setVal] = useState("");
  return (
    <div>
      <div className="flex gap-2 mb-2">
        <input value={val} onChange={(e) => setVal(e.target.value)}
          placeholder={placeholder}
          className="flex-1 px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]"
          onKeyDown={(e) => { if (e.key === "Enter" && val.trim()) { onChange([...items, val.trim()]); setVal(""); } }}
        />
        <Button variant="secondary" size="sm" disabled={!val.trim()} onClick={() => { onChange([...items, val.trim()]); setVal(""); }}>Add</Button>
      </div>
      {items.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {items.map((item, i) => (
            <span key={i} className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-(--color-page) text-(--color-text-secondary)">
              {item}
              <button onClick={() => onChange(items.filter((_, j) => j !== i))} className="opacity-40 hover:opacity-80">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default function EducationPlanPage() {
  useEffect(() => { document.title = "Education Plan | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const { toast } = useToast();

  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mode, setMode] = useState<"view" | "wizard">("view");
  const [step, setStep] = useState(1);
  const [generating, setGenerating] = useState(false);
  const [generatingCurricula, setGeneratingCurricula] = useState<string | null>(null);

  // Step 1: Goals
  const [postGrad, setPostGrad] = useState("undecided");
  const [collegeLevel, setCollegeLevel] = useState("Standard");
  const [targetSkills, setTargetSkills] = useState<string[]>([]);
  const [vision, setVision] = useState("");

  // Step 2: Baseline
  const [readingLevel, setReadingLevel] = useState("At grade");
  const [mathLevel, setMathLevel] = useState("At grade");
  const [strengths, setStrengths] = useState<string[]>([]);
  const [struggles, setStruggles] = useState<string[]>([]);
  const [conditions, setConditions] = useState<string[]>([]);
  const [priorEd, setPriorEd] = useState("Always homeschooled");
  const [weeklyHours, setWeeklyHours] = useState(25);

  useEffect(() => { if (selectedChild) loadPlan(); }, [selectedChild]);

  async function loadPlan() {
    if (!selectedChild) return;
    setLoading(true);
    setError("");
    try {
      const p = await educationPlan.get(selectedChild.id);
      if (p && (p as any).year_plans) {
        setPlan(p);
        setMode("view");
      } else {
        setPlan(null);
        setMode("wizard");
      }
    } catch {
      setPlan(null);
      setMode("wizard");
    } finally {
      setLoading(false);
    }
  }

  async function generate() {
    if (!selectedChild) return;
    setGenerating(true);
    setError("");
    try {
      const result = await educationPlan.generate(selectedChild.id, {
        post_graduation_path: postGrad,
        college_prep_level: postGrad === "college_prep" ? collegeLevel : undefined,
        target_skills: targetSkills,
        parent_vision: vision || undefined,
        reading_level: readingLevel,
        math_level: mathLevel,
        strengths,
        struggles,
        diagnosed_conditions: conditions.length > 0 ? conditions : undefined,
        prior_education: priorEd,
        weekly_hours: weeklyHours,
      });
      setPlan(result);
      setStep(4);
    } catch (err: any) {
      toast(err?.detail || "Couldn't generate plan", "error");
      setError(err?.detail || err?.message || "Failed to generate education plan.");
    } finally {
      setGenerating(false);
    }
  }

  async function approve() {
    if (!selectedChild) return;
    try {
      await educationPlan.approve(selectedChild.id);
      toast("Education plan approved", "success");
      await loadPlan();
    } catch (err: any) {
      toast(err?.detail || "Couldn't approve plan", "error");
    }
  }

  async function generateYearCurricula(year: string) {
    if (!selectedChild) return;
    setGeneratingCurricula(year);
    try {
      const yearPlan = (plan as any).year_plans[year];
      if (!yearPlan?.subjects) return;
      for (const subj of yearPlan.subjects) {
        await annualCurriculum.generate(selectedChild.id, {
          subject_name: subj.name || subj.subject,
          academic_year: year,
          hours_per_week: subj.hours_per_week || 4,
          total_weeks: 36,
        });
      }
      toast(`Curricula generated for ${year}`, "success");
    } catch (err: any) {
      toast(err?.detail || "Couldn't generate curricula", "error");
    } finally {
      setGeneratingCurricula(null);
    }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;
  if (loading) return <div className="max-w-4xl"><PageHeader title="Education Plan" /><LoadingSkeleton variant="card" count={3} /></div>;

  const childName = selectedChild.first_name;
  const yearPlans = (plan as any)?.year_plans || {};
  const isApproved = (plan as any)?.status === "approved";
  const currentYear = `${new Date().getFullYear()}-${new Date().getFullYear() + 1}`;

  // ── VIEW MODE: Show approved plan ──
  if (mode === "view" && plan) {
    return (
      <div className="max-w-4xl">
        <PageHeader
          title={`${childName}'s Education Plan`}
          subtitle={(plan as any).graduation_pathway || "Multi-year educational roadmap"}
          actions={
            <Button variant="secondary" size="sm" onClick={() => { setMode("wizard"); setStep(4); }}>
              Revise Plan
            </Button>
          }
        />

        {error && (
          <Card className="mb-4" borderLeft="border-l-(--color-danger)">
            <p className="text-sm text-(--color-danger)">{error}</p>
          </Card>
        )}

        <YearTimeline
          yearPlans={yearPlans}
          currentYear={currentYear}
          generatingCurricula={generatingCurricula}
          onGenerateCurricula={generateYearCurricula}
          isApproved={isApproved}
        />

        {(plan as any).graduation_pathway && (
          <Card className="mt-5" borderLeft="border-l-(--gold)">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-lg">🎓</span>
              <span className="text-sm font-semibold text-(--color-text)">Graduation Pathway</span>
            </div>
            <p className="text-xs text-(--color-text-secondary)">{(plan as any).graduation_pathway}</p>
          </Card>
        )}
      </div>
    );
  }

  // ── WIZARD MODE ──
  return (
    <div className="max-w-2xl">
      <PageHeader
        title={`${childName}'s Education Plan`}
        subtitle="Build a multi-year educational roadmap."
      />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => setError("")}>Dismiss</Button>
          </div>
        </Card>
      )}

      {/* Progress */}
      {step < 4 && (
        <div className="flex items-center gap-2 mb-6">
          {[1, 2, 3].map((s) => (
            <div key={s} className={cn("flex-1 h-1 rounded-full transition-colors", step >= s ? "bg-(--color-accent)" : "bg-(--color-border)")} />
          ))}
        </div>
      )}

      {/* ── Step 1: Goals ── */}
      {step === 1 && (
        <Card animate>
          <h3 className="text-sm font-semibold text-(--color-text) mb-1">What are your goals for {childName}'s education?</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">This shapes the entire roadmap — subjects, rigor, and milestones.</p>

          <div className="space-y-5">
            <div>
              <label className="text-xs font-medium text-(--color-text) block mb-2">Post-graduation path</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {POST_GRAD_PATHS.map((p) => (
                  <button key={p.value} onClick={() => setPostGrad(p.value)}
                    className={cn("text-left p-3 rounded-[10px] border transition-colors",
                      postGrad === p.value ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border) hover:border-(--color-border-strong)")}>
                    <div className="text-xs font-medium text-(--color-text)">{p.label}</div>
                    <div className="text-[10px] text-(--color-text-tertiary)">{p.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {postGrad === "college_prep" && (
              <div>
                <label className="text-xs font-medium text-(--color-text) block mb-2">College prep level</label>
                <div className="flex gap-2">
                  {COLLEGE_LEVELS.map((l) => (
                    <button key={l} onClick={() => setCollegeLevel(l)}
                      className={cn("px-3 py-1.5 text-xs rounded-[10px] border transition-colors",
                        collegeLevel === l ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                      {l}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div>
              <label className="text-xs font-medium text-(--color-text) block mb-2">Target skills</label>
              <div className="flex flex-wrap gap-1.5">
                {TARGET_SKILLS.map((skill) => (
                  <button key={skill} onClick={() => setTargetSkills((prev) => prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill])}
                    className={cn("px-2.5 py-1 text-xs rounded-full border transition-colors",
                      targetSkills.includes(skill) ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)" : "border-(--color-border) text-(--color-text-secondary)")}>
                    {skill}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-(--color-text) block mb-1">Your vision (optional)</label>
              <textarea
                value={vision}
                onChange={(e) => setVision(e.target.value)}
                placeholder={`What does educational success look like for ${childName}?`}
                rows={3}
                className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px] resize-none"
              />
            </div>
          </div>

          <Button variant="primary" size="lg" className="w-full mt-5" onClick={() => setStep(2)}>
            Continue
          </Button>
        </Card>
      )}

      {/* ── Step 2: Baseline ── */}
      {step === 2 && (
        <Card animate>
          <h3 className="text-sm font-semibold text-(--color-text) mb-1">Where is {childName} right now?</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">This helps the AI calibrate the starting point and pace.</p>

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-(--color-text-secondary) block mb-1">Reading level</label>
                <select value={readingLevel} onChange={(e) => setReadingLevel(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]">
                  {LEVEL_OPTIONS.map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs text-(--color-text-secondary) block mb-1">Math level</label>
                <select value={mathLevel} onChange={(e) => setMathLevel(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]">
                  {LEVEL_OPTIONS.map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs text-(--color-text-secondary) block mb-1">Strengths</label>
              <MultiInput items={strengths} onChange={setStrengths} placeholder="e.g., loves reading, strong verbal skills" />
            </div>

            <div>
              <label className="text-xs text-(--color-text-secondary) block mb-1">Struggles</label>
              <MultiInput items={struggles} onChange={setStruggles} placeholder="e.g., attention span, math facts" />
            </div>

            <div>
              <label className="text-xs text-(--color-text-secondary) block mb-1">Diagnosed conditions (optional)</label>
              <MultiInput items={conditions} onChange={setConditions} placeholder="e.g., ADHD, dyslexia" />
              <p className="text-[10px] text-(--color-text-tertiary) mt-1">Helps the AI provide appropriate accommodations. Never shared externally.</p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-(--color-text-secondary) block mb-1">Prior education</label>
                <select value={priorEd} onChange={(e) => setPriorEd(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]">
                  {PRIOR_ED.map((p) => <option key={p} value={p}>{p}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs text-(--color-text-secondary) block mb-1">Hours per week</label>
                <input type="number" value={weeklyHours} min={5} max={50}
                  onChange={(e) => setWeeklyHours(Math.max(5, Math.min(50, +e.target.value)))}
                  className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]"
                />
              </div>
            </div>
          </div>

          <div className="flex gap-2 mt-5">
            <Button variant="ghost" size="md" onClick={() => setStep(1)}>Back</Button>
            <Button variant="primary" size="lg" className="flex-1" onClick={() => setStep(3)}>Continue</Button>
          </div>
        </Card>
      )}

      {/* ── Step 3: Generate ── */}
      {step === 3 && !generating && (
        <Card animate>
          <h3 className="text-sm font-semibold text-(--color-text) mb-1">Generate {childName}'s education roadmap</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">The AI will create a multi-year plan based on your goals and {childName}'s current level.</p>

          <div className="bg-(--color-page) rounded-[10px] p-4 space-y-2 mb-5 text-xs text-(--color-text-secondary)">
            <div className="flex justify-between"><span>Path:</span><span className="font-medium text-(--color-text) capitalize">{postGrad.replace(/_/g, " ")}</span></div>
            {postGrad === "college_prep" && <div className="flex justify-between"><span>Level:</span><span className="font-medium text-(--color-text)">{collegeLevel}</span></div>}
            <div className="flex justify-between"><span>Skills:</span><span className="font-medium text-(--color-text)">{targetSkills.length > 0 ? targetSkills.join(", ") : "None selected"}</span></div>
            <div className="flex justify-between"><span>Reading:</span><span className="font-medium text-(--color-text)">{readingLevel}</span></div>
            <div className="flex justify-between"><span>Math:</span><span className="font-medium text-(--color-text)">{mathLevel}</span></div>
            <div className="flex justify-between"><span>Hours/week:</span><span className="font-medium text-(--color-text)">{weeklyHours}h</span></div>
          </div>

          <div className="flex gap-2">
            <Button variant="ghost" size="md" onClick={() => setStep(2)}>Back</Button>
            <Button variant="gold" size="lg" className="flex-1" onClick={generate}>Generate Plan</Button>
          </div>
        </Card>
      )}

      {/* ── Step 3: Loading ── */}
      {step === 3 && generating && (
        <Card>
          <div className="text-center py-8">
            <div className="w-10 h-10 mx-auto mb-4 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
            <p className="text-sm text-(--color-text) mb-1">Building {childName}'s educational roadmap...</p>
            <p className="text-xs text-(--color-text-tertiary)">Analyzing goals, calibrating pace, mapping subjects across years.</p>
          </div>
        </Card>
      )}

      {/* ── Step 4: Review ── */}
      {step === 4 && plan && (
        <div className="max-w-4xl">
          <Card className="mb-4" animate>
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">Review {childName}'s education roadmap</h3>
            <p className="text-xs text-(--color-text-secondary)">
              {Object.keys(yearPlans).length} years planned. Review each year, then approve to make it official.
            </p>
          </Card>

          <YearTimeline
            yearPlans={yearPlans}
            currentYear={currentYear}
            generatingCurricula={null}
            onGenerateCurricula={() => {}}
            isApproved={false}
          />

          {(plan as any).graduation_pathway && (
            <Card className="mt-4" borderLeft="border-l-(--gold)">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">🎓</span>
                <span className="text-sm font-semibold text-(--color-text)">Graduation Pathway</span>
              </div>
              <p className="text-xs text-(--color-text-secondary)">{(plan as any).graduation_pathway}</p>
            </Card>
          )}

          <div className="flex gap-2 mt-5">
            <Button variant="ghost" size="md" onClick={() => { setStep(1); setPlan(null); }}>Start Over</Button>
            <Button variant="gold" size="lg" className="flex-1" onClick={approve}>Approve Plan</Button>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Year Timeline Component ──
function YearTimeline({
  yearPlans,
  currentYear,
  generatingCurricula,
  onGenerateCurricula,
  isApproved,
}: {
  yearPlans: Record<string, any>;
  currentYear: string;
  generatingCurricula: string | null;
  onGenerateCurricula: (year: string) => void;
  isApproved: boolean;
}) {
  const years = Object.entries(yearPlans).sort(([a], [b]) => a.localeCompare(b));

  return (
    <div className="space-y-4">
      {years.map(([year, data], idx) => {
        const isCurrent = year === currentYear;
        const subjects = data.subjects || [];
        const milestones = data.milestones || [];
        const stage = data.developmental_stage || data.stage;

        return (
          <div key={year} className="relative">
            {/* Timeline connector */}
            {idx < years.length - 1 && (
              <div className="absolute left-5 top-full w-0.5 h-4 bg-(--color-border)" style={{ zIndex: 0 }} />
            )}

            <Card
              className={cn(isCurrent && "ring-2 ring-(--color-accent)/20")}
              borderLeft={isCurrent ? "border-l-(--color-accent)" : undefined}
              animate
            >
              {/* Year header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold shrink-0",
                    isCurrent ? "bg-(--color-accent) text-white" : "bg-(--color-page) text-(--color-text-secondary)"
                  )}>
                    {year.split("-")[0].slice(-2)}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-(--color-text)">{year}</h4>
                    <div className="flex items-center gap-2">
                      {data.grade_level && <span className="text-[10px] text-(--color-text-tertiary)">{data.grade_level}</span>}
                      {stage && <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-accent-light) text-(--color-accent)">{stage}</span>}
                      {isCurrent && <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-success-light) text-(--color-success) font-medium">Current</span>}
                    </div>
                  </div>
                </div>
                {isApproved && (
                  <Button
                    variant="secondary" size="sm"
                    disabled={generatingCurricula === year}
                    onClick={() => onGenerateCurricula(year)}
                  >
                    {generatingCurricula === year ? "Generating..." : "Generate Curricula"}
                  </Button>
                )}
              </div>

              {/* Subjects grid */}
              {subjects.length > 0 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 mb-3">
                  {subjects.map((subj: any, i: number) => (
                    <div key={i} className="bg-(--color-page) rounded-[10px] p-3">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-medium text-(--color-text)">{subj.name || subj.subject}</span>
                        {subj.priority && (
                          <span className={cn("text-[9px] px-1.5 py-0.5 rounded-full font-medium",
                            subj.priority === "core" ? "bg-(--color-accent-light) text-(--color-accent)" : "bg-(--color-page) text-(--color-text-tertiary)"
                          )}>{subj.priority}</span>
                        )}
                      </div>
                      {subj.hours_per_week && (
                        <span className="text-[10px] text-(--color-text-tertiary)">{subj.hours_per_week}h/week</span>
                      )}
                      {subj.approach && (
                        <p className="text-[10px] text-(--color-text-tertiary) mt-1 line-clamp-2">{subj.approach}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* Milestones */}
              {milestones.length > 0 && (
                <div>
                  <div className="text-[10px] font-medium text-(--color-text-tertiary) uppercase tracking-wide mb-1.5">Milestones</div>
                  <div className="space-y-1">
                    {milestones.map((m: any, i: number) => (
                      <div key={i} className="flex items-center gap-2 text-xs">
                        <span className="w-1.5 h-1.5 rounded-full bg-(--color-accent) shrink-0" />
                        <span className="text-(--color-text-secondary)">{typeof m === "string" ? m : m.description || m.title}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          </div>
        );
      })}
    </div>
  );
}
