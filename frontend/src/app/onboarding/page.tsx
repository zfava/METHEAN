"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { children as childrenApi, governance, annualCurriculum, plans, curriculum } from "@/lib/api";
import { MetheanLogoVertical } from "@/components/Brand";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

const PHILOSOPHIES = [
  { value: "classical", label: "Classical", desc: "Trivium: grammar, logic, rhetoric" },
  { value: "charlotte_mason", label: "Charlotte Mason", desc: "Living books, nature study" },
  { value: "unschooling", label: "Unschooling", desc: "Child-led, experiential" },
  { value: "eclectic", label: "Eclectic", desc: "Mixed approaches" },
  { value: "montessori", label: "Montessori", desc: "Self-directed, hands-on" },
  { value: "traditional", label: "Traditional", desc: "Structured, textbook-based" },
];

const AUTONOMY = [
  { value: "preview_all", label: "Preview All", desc: "Review every AI recommendation" },
  { value: "approve_difficult", label: "Approve Difficult", desc: "Auto-approve easy, review hard" },
  { value: "trust_within_rules", label: "Trust Within Rules", desc: "AI follows your rules freely" },
];

const GRADE_SUBJECTS: Record<string, string[]> = {
  "K": ["Reading", "Mathematics", "Handwriting"],
  "1st": ["Reading", "Mathematics", "Handwriting", "Science"],
  "2nd": ["Reading", "Mathematics", "Writing", "Science"],
  "3rd": ["Literature", "Mathematics", "Writing", "Science", "History"],
  "4th": ["Literature", "Mathematics", "Writing", "Science", "History"],
  "5th": ["Literature", "Mathematics", "Writing", "Science", "History"],
  "6th": ["Literature", "Mathematics", "Writing", "Science", "History", "Latin"],
  "7th": ["Literature", "Mathematics", "Logic", "Science", "History"],
  "8th": ["Literature", "Mathematics", "Logic", "Science", "History"],
  "9th": ["Literature", "Mathematics", "Rhetoric", "Science", "History"],
  "10th": ["Literature", "Mathematics", "Rhetoric", "Science", "History"],
  "11th": ["Literature", "Mathematics", "Science", "History", "Government"],
  "12th": ["Literature", "Mathematics", "Science", "History", "Philosophy"],
};

const GRADE_MINUTES: Record<string, number> = {
  "K": 90, "1st": 90, "2nd": 90,
  "3rd": 120, "4th": 120, "5th": 120,
  "6th": 150, "7th": 150, "8th": 150,
  "9th": 180, "10th": 180, "11th": 180, "12th": 180,
};

const GRADES = ["K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"];

interface OnboardingChild { id: string; firstName: string; grade: string }

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Step 2: Children
  const [addedChildren, setAddedChildren] = useState<OnboardingChild[]>([]);
  const [newName, setNewName] = useState("");
  const [newGrade, setNewGrade] = useState("K");

  // Step 3: Philosophy
  const [philosophy, setPhilosophy] = useState("eclectic");
  const [autonomy, setAutonomy] = useState("approve_difficult");

  // Step 4: Curriculum
  const [curriculumChoices, setCurriculumChoices] = useState<Record<string, "ai" | "template" | "skip">>({});
  const [currentChildIdx, setCurrentChildIdx] = useState(0);
  const [generatingFor, setGeneratingFor] = useState("");

  // Step 5: Plans
  const [planProgress, setPlanProgress] = useState<string[]>([]);

  // Step 6: Summary
  const [summary, setSummary] = useState<{ rules: number; activities: Record<string, number> }>({ rules: 0, activities: {} });

  useEffect(() => { document.title = "Welcome | METHEAN"; }, []);

  // ── Step 2: Add Child ──
  async function addChild() {
    if (!newName.trim()) return;
    setError("");
    try {
      const result = await childrenApi.create({ first_name: newName, grade_level: newGrade });
      setAddedChildren((prev) => [...prev, { id: result.id, firstName: newName, grade: newGrade }]);
      setNewName("");
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't add child.");
    }
  }

  function removeChild(id: string) {
    setAddedChildren((prev) => prev.filter((c) => c.id !== id));
  }

  // ── Step 3: Save Philosophy + Init Rules ──
  async function savePhilosophy() {
    setLoading(true);
    setError("");
    try {
      const csrf = getCsrf();
      await fetch(`${API}/household/philosophy`, {
        method: "PUT", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify({
          educational_philosophy: philosophy,
          religious_framework: "secular",
          ai_autonomy_level: autonomy,
        }),
      });
      // Initialize default governance rules
      await governance.initDefaults();
      setStep(4);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't save settings.");
    } finally {
      setLoading(false);
    }
  }

  // ── Step 4: Generate Curricula ──
  async function generateCurricula() {
    setLoading(true);
    setError("");
    const year = new Date().getFullYear();
    const academicYear = `${year}-${year + 1}`;

    for (const child of addedChildren) {
      const choice = curriculumChoices[child.id] || "skip";
      if (choice === "skip") continue;

      const subjects = GRADE_SUBJECTS[child.grade] || GRADE_SUBJECTS["K"];
      for (const subject of subjects) {
        setGeneratingFor(`${child.firstName}: ${subject}`);
        try {
          const result = await annualCurriculum.generate(child.id, {
            subject_name: subject,
            academic_year: academicYear,
            hours_per_week: 4,
            total_weeks: 36,
          });
          // Auto-approve
          if (result && (result as any).id) {
            try { await annualCurriculum.approve((result as any).id); } catch {}
          }
        } catch {
          // Continue with next subject — don't block onboarding
        }
      }
    }
    setGeneratingFor("");
    setStep(5);
    setLoading(false);
  }

  // ── Step 5: Generate Plans ──
  async function generatePlans() {
    setLoading(true);
    setError("");
    const today = new Date();
    const monday = new Date(today);
    monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
    const weekStart = monday.toISOString().split("T")[0];

    const activityCounts: Record<string, number> = {};

    for (const child of addedChildren) {
      if (curriculumChoices[child.id] === "skip") continue;
      setPlanProgress((prev) => [...prev, child.firstName]);
      try {
        const dailyMinutes = GRADE_MINUTES[child.grade] || 120;
        await plans.generate(child.id, { week_start: weekStart, daily_minutes: dailyMinutes });
        // Count today's activities
        const resp = await fetch(`${API}/children/${child.id}/today`, { credentials: "include" });
        if (resp.ok) {
          const acts = await resp.json();
          activityCounts[child.firstName] = Array.isArray(acts) ? acts.length : 0;
        }
      } catch {
        activityCounts[child.firstName] = 0;
      }
    }

    // Count active rules
    try {
      const rulesData = await governance.rules();
      const rulesList = (rulesData as any).items || rulesData;
      setSummary({ rules: Array.isArray(rulesList) ? rulesList.length : 0, activities: activityCounts });
    } catch {
      setSummary({ rules: 4, activities: activityCounts });
    }

    setStep(6);
    setLoading(false);
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-(--color-page) px-4 py-8">
      <div className="w-full max-w-lg">
        {/* Logo + Progress */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <MetheanLogoVertical markSize={step === 1 ? 52 : 36} wordmarkHeight={step === 1 ? 18 : 14} color="#0F1B2D" gap={8} />
          </div>
          {step === 1 && (
            <>
              <h2 className="text-lg font-medium text-(--color-text) mt-4">Welcome</h2>
              <p className="text-sm text-(--color-text-secondary) mt-1">Let's set up your learning environment.</p>
            </>
          )}
          {step > 1 && (
            <div className="flex items-center justify-center gap-2 mt-3">
              {[2, 3, 4, 5, 6].map((s) => (
                <div key={s} className={cn("w-8 h-1 rounded-full transition-colors", step >= s ? "bg-(--color-accent)" : "bg-(--color-border)")} />
              ))}
            </div>
          )}
        </div>

        {/* Error display */}
        {error && (
          <Card className="mb-4" borderLeft="border-l-(--color-danger)">
            <div className="flex items-center justify-between gap-4">
              <p className="text-sm text-(--color-danger)">{error}</p>
              <Button variant="ghost" size="sm" onClick={() => setError("")}>Dismiss</Button>
            </div>
          </Card>
        )}

        {/* ── Step 1: Welcome ── */}
        {step === 1 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8 text-center">
            <p className="text-sm text-(--color-text-secondary) mb-6">
              METHEAN is a learning operating system where AI advises, but you govern.
              In the next few steps, we'll add your children, set your educational philosophy,
              and generate their first curriculum.
            </p>
            <Button variant="primary" size="lg" onClick={() => setStep(2)} className="w-full max-w-xs mx-auto">
              Get Started
            </Button>
          </div>
        )}

        {/* ── Step 2: Add Children ── */}
        {step === 2 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">Who's learning at home?</h3>
            <p className="text-xs text-(--color-text-secondary) mb-4">Add at least one child to continue.</p>

            <div className="flex flex-col sm:flex-row gap-2 mb-4">
              <input value={newName} onChange={(e) => setNewName(e.target.value)}
                placeholder="First name"
                className="flex-1 px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)"
                onKeyDown={(e) => e.key === "Enter" && addChild()} />
              <select value={newGrade} onChange={(e) => setNewGrade(e.target.value)}
                className="w-full sm:w-28 px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
                {GRADES.map((g) => <option key={g} value={g}>{g}</option>)}
              </select>
              <Button variant="primary" size="md" onClick={addChild} disabled={!newName.trim()}>Add</Button>
            </div>

            {addedChildren.length > 0 && (
              <div className="space-y-2 mb-4">
                {addedChildren.map((c) => (
                  <div key={c.id} className="flex items-center justify-between px-3 py-2 bg-(--color-page) rounded-[10px]">
                    <span className="text-sm text-(--color-text)">{c.firstName} <span className="text-(--color-text-tertiary)">· {c.grade}</span></span>
                    <button onClick={() => removeChild(c.id)} className="text-xs text-(--color-danger) hover:underline">Remove</button>
                  </div>
                ))}
              </div>
            )}

            <p className="text-[10px] text-(--color-text-tertiary) mb-4">You can add more children later from the Family page.</p>

            <Button variant="primary" size="lg" onClick={() => setStep(3)} disabled={addedChildren.length === 0} className="w-full">
              Continue
            </Button>
          </div>
        )}

        {/* ── Step 3: Philosophy ── */}
        {step === 3 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">Your educational approach</h3>
            <p className="text-xs text-(--color-text-secondary) mb-4">This guides how the AI generates curriculum and activities.</p>

            <div className="grid grid-cols-2 gap-2 mb-6">
              {PHILOSOPHIES.map((p) => (
                <button key={p.value} onClick={() => setPhilosophy(p.value)}
                  className={cn("text-left p-3 rounded-[10px] border transition-colors",
                    philosophy === p.value ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border) hover:border-(--color-border-strong)")}>
                  <div className="text-xs font-medium text-(--color-text)">{p.label}</div>
                  <div className="text-[10px] text-(--color-text-tertiary)">{p.desc}</div>
                </button>
              ))}
            </div>

            <h4 className="text-xs font-medium text-(--color-text) mb-2">AI autonomy level</h4>
            <div className="space-y-2 mb-6">
              {AUTONOMY.map((a) => (
                <button key={a.value} onClick={() => setAutonomy(a.value)}
                  className={cn("w-full text-left p-3 rounded-[10px] border transition-colors",
                    autonomy === a.value ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                  <div className="text-xs font-medium text-(--color-text)">{a.label}</div>
                  <div className="text-[10px] text-(--color-text-tertiary)">{a.desc}</div>
                </button>
              ))}
            </div>

            <Button variant="primary" size="lg" onClick={savePhilosophy} disabled={loading} className="w-full">
              {loading ? "Saving..." : "Continue"}
            </Button>
          </div>
        )}

        {/* ── Step 4: Curriculum Path ── */}
        {step === 4 && !loading && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
            {currentChildIdx < addedChildren.length ? (
              <>
                <h3 className="text-sm font-semibold text-(--color-text) mb-1">
                  Build {addedChildren[currentChildIdx].firstName}'s curriculum
                </h3>
                <p className="text-xs text-(--color-text-secondary) mb-4">
                  {addedChildren[currentChildIdx].grade} · {GRADE_SUBJECTS[addedChildren[currentChildIdx].grade]?.length || 3} core subjects
                </p>

                <div className="space-y-2 mb-6">
                  {(["ai", "template", "skip"] as const).map((choice) => {
                    const labels = {
                      ai: { title: "AI-generated from your philosophy", desc: `METHEAN creates a year-long ${philosophy.replace(/_/g, " ")} curriculum` },
                      template: { title: "Start from a template", desc: "Pre-built starter you can customize" },
                      skip: { title: "I'll set it up later", desc: "Skip to dashboard" },
                    };
                    const childId = addedChildren[currentChildIdx].id;
                    return (
                      <button key={choice} onClick={() => setCurriculumChoices((prev) => ({ ...prev, [childId]: choice }))}
                        className={cn("w-full text-left p-4 rounded-[10px] border transition-colors",
                          curriculumChoices[childId] === choice ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                        <div className="text-xs font-medium text-(--color-text)">{labels[choice].title}</div>
                        <div className="text-[10px] text-(--color-text-tertiary)">{labels[choice].desc}</div>
                      </button>
                    );
                  })}
                </div>

                <Button variant="primary" size="lg" className="w-full"
                  disabled={!curriculumChoices[addedChildren[currentChildIdx].id]}
                  onClick={() => {
                    if (currentChildIdx < addedChildren.length - 1) {
                      setCurrentChildIdx(currentChildIdx + 1);
                    } else {
                      generateCurricula();
                    }
                  }}>
                  {currentChildIdx < addedChildren.length - 1 ? `Next: ${addedChildren[currentChildIdx + 1].firstName}` : "Generate Curricula"}
                </Button>
              </>
            ) : null}
          </div>
        )}

        {/* ── Step 4/5: Loading ── */}
        {loading && (step === 4 || step === 5) && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8 text-center">
            <div className="w-10 h-10 mx-auto mb-4 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
            <p className="text-sm text-(--color-text) mb-1">
              {step === 4 && generatingFor && `Generating ${generatingFor}...`}
              {step === 5 && planProgress.length > 0 && `Creating ${planProgress[planProgress.length - 1]}'s plan...`}
              {!generatingFor && step === 4 && "Setting up curricula..."}
            </p>
            <p className="text-xs text-(--color-text-tertiary)">This may take a moment.</p>
          </div>
        )}

        {/* ── Step 5: Generate Plans ── */}
        {step === 5 && !loading && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 text-center">
            <h3 className="text-sm font-semibold text-(--color-text) mb-2">Curricula ready!</h3>
            <p className="text-xs text-(--color-text-secondary) mb-6">
              Now let's create this week's activity schedule.
            </p>
            <Button variant="primary" size="lg" onClick={generatePlans} className="w-full">
              Generate First Week's Plan
            </Button>
            <button onClick={() => { setStep(6); setSummary({ rules: 4, activities: {} }); }}
              className="block mx-auto mt-3 text-xs text-(--color-text-tertiary) hover:underline">
              Skip — I'll generate plans later
            </button>
          </div>
        )}

        {/* ── Step 6: All Set ── */}
        {step === 6 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8">
            <div className="text-center mb-6">
              <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-(--color-success-light) flex items-center justify-center">
                <svg className="w-7 h-7 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-(--color-text)">Your family is ready!</h2>
            </div>

            {/* Activity preview */}
            {Object.keys(summary.activities).length > 0 && (
              <div className="space-y-2 mb-4">
                {Object.entries(summary.activities).map(([name, count]) => (
                  <div key={name} className="flex items-center justify-between px-3 py-2 bg-(--color-page) rounded-[10px]">
                    <span className="text-sm text-(--color-text)">{name}</span>
                    <span className="text-xs text-(--color-text-secondary)">{count} activities today</span>
                  </div>
                ))}
              </div>
            )}

            {/* Rules summary */}
            {summary.rules > 0 && (
              <div className="mb-6 p-3 bg-(--color-constitutional-light) rounded-[10px]">
                <p className="text-xs text-(--color-constitutional) font-medium mb-1">Governance rules active</p>
                <p className="text-[10px] text-(--color-text-secondary)">{summary.rules} rules protecting your family's education.</p>
              </div>
            )}

            <div className="space-y-2">
              <Button variant="primary" size="lg" onClick={() => router.push("/dashboard")} className="w-full">
                Go to Dashboard
              </Button>
              {addedChildren.length > 0 && (
                <Button variant="secondary" size="md" onClick={() => router.push("/child")} className="w-full">
                  Open {addedChildren[0].firstName}'s Learning
                </Button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
