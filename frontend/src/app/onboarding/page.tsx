"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { children as childrenApi, governance, annualCurriculum, plans, curriculum, household } from "@/lib/api";
import { MetheanLogoVertical } from "@/components/Brand";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { useToast } from "@/components/Toast";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { cn } from "@/lib/cn";
import SubjectLevelPicker from "@/components/SubjectLevelPicker";

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

const GRADES = ["K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"];

const CEREMONY_AFFIRMATIONS = [
  "I understand that AI in METHEAN advises but never decides. Every recommendation flows through my governance rules.",
  "I understand that I can inspect every AI interaction, including the full prompt and response, at any time.",
  "I understand that constitutional rules require a formal amendment process to change, protecting my family's values from casual modification.",
] as const;

const STEP_LABELS = [
  "Welcome",
  "Children",
  "Learning",
  "Philosophy",
  "Constitution",
  "Curriculum",
  "Plan",
  "Ready",
] as const;

/** Hash a string to a stable hue so each child's avatar gets a
 *  consistent color across renders without hardcoding a palette per
 *  name. djb2 keeps the distribution wide enough that two siblings
 *  rarely collide. */
function avatarHueFor(name: string): number {
  let h = 5381;
  for (let i = 0; i < name.length; i++) h = ((h << 5) + h + name.charCodeAt(i)) | 0;
  return Math.abs(h) % 360;
}

interface OnboardingChild { id: string; firstName: string; grade: string }

export default function OnboardingPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [step, setStep] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Step 2: Children
  const [addedChildren, setAddedChildren] = useState<OnboardingChild[]>([]);
  const [newName, setNewName] = useState("");
  const [newGrade, setNewGrade] = useState("");

  // Step 3: Learning Profile
  const [childSubjectLevels, setChildSubjectLevels] = useState<Record<string, Record<string, string>>>({});
  const [childMinutes, setChildMinutes] = useState<Record<string, number>>({});
  const [profileChildIdx, setProfileChildIdx] = useState(0);

  // Step 4: Philosophy
  const [philosophy, setPhilosophy] = useState("eclectic");
  const [autonomy, setAutonomy] = useState("approve_difficult");

  // Step 5: Constitutional Ceremony
  const [ceremonyChecks, setCeremonyChecks] = useState([false, false, false]);
  const [ceremonyReason, setCeremonyReason] = useState("");
  const [ratified, setRatified] = useState(false);
  const [constitutionalRuleId, setConstitutionalRuleId] = useState<string | null>(null);
  const [constitutionalRules, setConstitutionalRules] = useState<string[]>([]);

  // Step 6: Curriculum
  const [curriculumChoices, setCurriculumChoices] = useState<Record<string, "ai" | "template" | "skip">>({});
  const [currentChildIdx, setCurrentChildIdx] = useState(0);
  const [generatingFor, setGeneratingFor] = useState("");

  // Step 7: Plans
  const [planProgress, setPlanProgress] = useState<string[]>([]);

  // Step 8: Summary
  const [summary, setSummary] = useState<{ rules: number; activities: Record<string, number> }>({ rules: 0, activities: {} });

  useEffect(() => { document.title = "Welcome | METHEAN"; }, []);

  // ── Step transition direction (forward / backward) ───────────────
  // Visual-only: tracks whether the most recent step change advanced
  // or retreated, so the wrapper can pick slide-in-left vs
  // slide-in-right. Doesn't touch step navigation logic.
  const prevStepRef = useRef(step);
  const [direction, setDirection] = useState<"forward" | "backward">("forward");
  useEffect(() => {
    if (step !== prevStepRef.current) {
      setDirection(step > prevStepRef.current ? "forward" : "backward");
      prevStepRef.current = step;
    }
  }, [step]);

  // ── Curriculum-generation observed-completion set ────────────────
  // Tracks every distinct ``${child}: ${subject}`` value generatingFor
  // has held during the current generation so the step-6 progress UI
  // can render checkmarks for completed subjects without modifying
  // the existing generateCurricula flow. The current generatingFor
  // is treated as "in progress" — only previously-seen values count
  // as done.
  const [doneSubjects, setDoneSubjects] = useState<Set<string>>(new Set());
  const prevGenForRef = useRef("");
  useEffect(() => {
    const prev = prevGenForRef.current;
    if (prev && prev !== generatingFor) {
      setDoneSubjects((s) => {
        const next = new Set(s);
        next.add(prev);
        return next;
      });
    }
    prevGenForRef.current = generatingFor;
  }, [generatingFor]);
  // Reset whenever we leave step 6 so a fresh run starts clean.
  useEffect(() => {
    if (step !== 6) {
      setDoneSubjects(new Set());
      prevGenForRef.current = "";
    }
  }, [step]);

  // ── Step 2: Add Child ──
  async function addChild() {
    if (!newName.trim()) return;
    setError("");
    try {
      const result = await childrenApi.create({ first_name: newName, grade_level: newGrade || undefined });
      setAddedChildren((prev) => [...prev, { id: result.id, firstName: newName, grade: newGrade }]);
      setNewName("");
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't add child.");
    }
  }

  function removeChild(id: string) {
    setAddedChildren((prev) => prev.filter((c) => c.id !== id));
  }

  // ── Step 4: Save Philosophy + Init Rules ──
  async function savePhilosophy() {
    setLoading(true);
    setError("");
    try {
      await household.updatePhilosophy({
        educational_philosophy: philosophy,
        religious_framework: "secular",
        ai_autonomy_level: autonomy,
      });
      const rulesResult = await governance.initDefaults();
      const rulesList = (rulesResult as any).items || rulesResult;
      if (Array.isArray(rulesList)) {
        const constRules = rulesList.filter((r: any) => r.tier === "constitutional" || r.rule_type === "ai_boundary");
        setConstitutionalRules(constRules.map((r: any) => r.name || r.rule_type));
        if (constRules.length > 0) setConstitutionalRuleId(constRules[0].id);
      }
      setStep(5);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't save settings.");
    } finally {
      setLoading(false);
    }
  }

  // ── Step 5: Ratify Constitution ──
  async function handleRatify() {
    setRatified(true);
    toast("Your family's constitution is established", "success");
    // Persist ratification reason to the constitutional rule
    if (constitutionalRuleId) {
      try {
        await governance.updateRule(constitutionalRuleId, {
          description: `AI Oversight Guarantee — Ratified during onboarding. Parent's reason: "${ceremonyReason.trim()}"`,
        });
      } catch { /* Non-blocking: ceremony proceeds even if persistence fails */ }
    }
    setTimeout(() => setStep(6), 2000);
  }

  // ── Step 6: Generate Curricula ──
  async function generateCurricula() {
    setLoading(true);
    setError("");
    const year = new Date().getFullYear();
    const academicYear = `${year}-${year + 1}`;

    for (const child of addedChildren) {
      const choice = curriculumChoices[child.id] || "skip";
      if (choice === "skip") continue;

      const levels = childSubjectLevels[child.id] || {};
      const subjects = Object.keys(levels).length > 0
        ? Object.keys(levels).map(id => id.replace(/_/g, " ").replace(/\b\w/g, (c: string) => c.toUpperCase()))
        : ["Reading", "Mathematics"];
      for (const subject of subjects) {
        setGeneratingFor(`${child.firstName}: ${subject}`);
        try {
          const result = await annualCurriculum.generate(child.id, {
            subject_name: subject,
            academic_year: academicYear,
            hours_per_week: 4,
            total_weeks: 36,
          });
          if (result && (result as any).id) {
            try { await annualCurriculum.approve((result as any).id); } catch {}
          }
        } catch {}
      }
    }
    setGeneratingFor("");
    toast("Curricula generated", "success");
    setStep(7);
    setLoading(false);
  }

  // ── Step 7: Generate Plans ──
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
        const dailyMinutes = childMinutes[child.id] || 120;
        await plans.generate(child.id, { week_start: weekStart, daily_minutes: dailyMinutes });
        const acts = await childrenApi.today(child.id).catch(() => []);
        activityCounts[child.firstName] = Array.isArray(acts) ? acts.length : 0;
      } catch {
        activityCounts[child.firstName] = 0;
      }
    }

    try {
      const rulesData = await governance.rules();
      const rulesList = (rulesData as any).items || rulesData;
      setSummary({ rules: Array.isArray(rulesList) ? rulesList.length : 0, activities: activityCounts });
    } catch {
      setSummary({ rules: 4, activities: activityCounts });
    }

    toast("First week's plan created", "success");
    setStep(8);
    setLoading(false);
  }

  const allCeremonyChecked = ceremonyChecks.every(Boolean);
  const ceremonyReasonValid = ceremonyReason.trim().length >= 20;

  return (
    <div className="min-h-screen bg-(--color-page)">
      {/* ── Sticky progress bar ───────────────────────────────────── */}
      <div
        className="sticky top-0 z-30 bg-(--color-surface)/95 backdrop-blur supports-[backdrop-filter]:bg-(--color-surface)/80 border-b border-(--color-border)"
        style={{ paddingTop: "var(--safe-top)" }}
      >
        <div className="max-w-lg mx-auto px-4 py-3">
          <div className="flex items-center justify-between gap-1.5" aria-label={`Step ${step} of ${STEP_LABELS.length}: ${STEP_LABELS[step - 1]}`}>
            {STEP_LABELS.map((_, i) => {
              const stepNum = i + 1;
              const isComplete = stepNum < step;
              const isCurrent = stepNum === step;
              return (
                <div key={stepNum} className="flex items-center flex-1 last:flex-none">
                  <div
                    className={cn(
                      "h-6 w-6 shrink-0 rounded-full flex items-center justify-center text-[10px] font-semibold transition-all duration-300",
                      isComplete && "bg-(--color-accent) text-white",
                      isCurrent && "bg-(--color-accent) text-white ring-4 ring-(--color-accent)/15",
                      !isComplete && !isCurrent &&
                        "bg-(--color-surface) border border-(--color-border) text-(--color-text-tertiary)",
                    )}
                    aria-current={isCurrent ? "step" : undefined}
                  >
                    {isComplete ? (
                      <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3} aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      stepNum
                    )}
                  </div>
                  {stepNum < STEP_LABELS.length && (
                    <div className="flex-1 h-px mx-1 relative overflow-hidden bg-(--color-border)">
                      <div
                        className="absolute inset-y-0 left-0 bg-(--color-accent) transition-all duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)]"
                        style={{ width: stepNum < step ? "100%" : "0%" }}
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-[11px] text-(--color-text-tertiary) uppercase tracking-wide">
              Step {step} of {STEP_LABELS.length}
            </span>
            <span className="text-sm font-medium text-(--color-text)">{STEP_LABELS[step - 1]}</span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-center px-4 py-8">
        <div className="w-full max-w-lg">
        {/* Step 1 wordmark / hero only on the first step. */}
        {step === 1 && (
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <MetheanLogoVertical markSize={52} wordmarkHeight={18} color="#0F1B2D" gap={8} />
            </div>
            <h2 className="text-lg font-medium text-(--color-text) mt-4">Welcome</h2>
            <p className="text-sm text-(--color-text-secondary) mt-1">Let&apos;s set up your learning environment.</p>
          </div>
        )}

        {/* Error display lives outside the slide container so the
            slide animation doesn't replay on dismissal. */}
        {error && (
          <Card className="mb-4" borderLeft="border-l-(--color-danger)">
            <div className="flex items-center justify-between gap-4">
              <p className="text-sm text-(--color-danger)">{error}</p>
              <Button variant="ghost" size="sm" onClick={() => setError("")}>Dismiss</Button>
            </div>
          </Card>
        )}

        {/* Step content slide container. Re-keyed on every step
            change so the slide animation re-fires; direction picks
            slide-in-left when advancing and slide-in-right when
            navigating backward. */}
        <div
          key={`step-${step}`}
          className={cn(
            direction === "forward" ? "animate-slide-left" : "animate-slide-right",
          )}
        >

        {/* ── Step 1: Welcome ── */}
        {step === 1 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8 text-center">
            <p className="text-sm text-(--color-text-secondary) mb-6">
              METHEAN is a learning operating system where AI advises, but you govern.
              In the next few steps, we&apos;ll add your children, set your educational philosophy,
              and generate their first curriculum.
            </p>
            <Button variant="primary" size="lg" onClick={() => setStep(2)} className="w-full max-w-xs mx-auto">
              Get Started
            </Button>
          </div>
        )}

        {/* ── Step 2: Add Children ── */}
        {step === 2 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 animate-fade-up">
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">Who&apos;s learning at home?</h3>
            <p className="text-xs text-(--color-text-secondary) mb-4">Add at least one child to continue.</p>

            {addedChildren.length > 0 && (
              <div className="space-y-2 mb-4">
                {addedChildren.map((c) => {
                  const hue = avatarHueFor(c.firstName || c.id);
                  return (
                    <div
                      key={c.id}
                      className="animate-scale-in flex items-center gap-3 pl-2 pr-3 py-2 bg-(--color-page) rounded-[12px] border border-(--color-border)"
                    >
                      <div
                        className="h-9 w-9 shrink-0 rounded-full flex items-center justify-center text-sm font-semibold"
                        style={{
                          background: `hsl(${hue}, 55%, 92%)`,
                          color: `hsl(${hue}, 55%, 32%)`,
                        }}
                        aria-hidden="true"
                      >
                        {(c.firstName || "?").charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-(--color-text) truncate">{c.firstName}</div>
                        {c.grade && (
                          <div className="text-[11px] text-(--color-text-tertiary)">{c.grade}</div>
                        )}
                      </div>
                      <button
                        onClick={() => removeChild(c.id)}
                        className="text-xs text-(--color-text-tertiary) hover:text-(--color-danger) px-2 py-1 rounded-md min-h-[36px]"
                        aria-label={`Remove ${c.firstName}`}
                      >
                        Remove
                      </button>
                    </div>
                  );
                })}
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-2 mb-3">
              <input
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder={addedChildren.length === 0 ? "First name" : "Add another child's name"}
                className="flex-1 px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)"
                onKeyDown={(e) => e.key === "Enter" && addChild()}
              />
              <select
                value={newGrade}
                onChange={(e) => setNewGrade(e.target.value)}
                className="w-full sm:w-28 px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)"
              >
                <option value="">Grade</option>
                {GRADES.map((g) => <option key={g} value={g}>{g}</option>)}
              </select>
              <Button
                variant={addedChildren.length === 0 ? "primary" : "ghost"}
                size="md"
                onClick={addChild}
                disabled={!newName.trim()}
              >
                {addedChildren.length === 0 ? (
                  "Add"
                ) : (
                  <span className="inline-flex items-center gap-1.5">
                    <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5} aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                    </svg>
                    Add another
                  </span>
                )}
              </Button>
            </div>

            <p className="text-[10px] text-(--color-text-tertiary) mb-4">You can add more children later from the Family page.</p>

            <Button
              variant="primary"
              size="lg"
              onClick={() => setStep(3)}
              disabled={addedChildren.length === 0}
              className={cn(
                "w-full transition-opacity",
                addedChildren.length === 0 && "opacity-60",
              )}
            >
              Continue
            </Button>
          </div>
        )}

        {/* ── Step 3: Learning Profile ── */}
        {step === 3 && addedChildren.length > 0 && (() => {
          const activeChild = addedChildren[profileChildIdx];
          const grade = activeChild?.grade || "";
          // Grade-aware daily-minutes recommendation. Mirrors the
          // legacy "Suggested: 90-240" hint but specialized so the
          // copy is meaningful when a grade is set.
          const recForGrade = (() => {
            if (grade === "K") return { lo: 60, hi: 120, label: "Kindergarten" };
            if (["1st", "2nd", "3rd"].includes(grade)) return { lo: 90, hi: 180, label: "Lower elementary" };
            if (["4th", "5th"].includes(grade)) return { lo: 120, hi: 210, label: "Upper elementary" };
            if (["6th", "7th", "8th"].includes(grade)) return { lo: 150, hi: 240, label: "Middle school" };
            if (["9th", "10th", "11th", "12th"].includes(grade)) return { lo: 180, hi: 300, label: "High school" };
            return { lo: 90, hi: 240, label: "All grades" };
          })();
          const currentMinutes = childMinutes[activeChild?.id] || 120;
          return (
            <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 animate-fade-up">
              {/* Child tabs — only shown when there's more than one. */}
              {addedChildren.length > 1 && (
                <div className="flex items-center gap-1.5 mb-4 overflow-x-auto pb-1" role="tablist">
                  {addedChildren.map((c, i) => {
                    const hue = avatarHueFor(c.firstName || c.id);
                    const active = i === profileChildIdx;
                    return (
                      <button
                        key={c.id}
                        role="tab"
                        aria-selected={active}
                        onClick={() => setProfileChildIdx(i)}
                        className={cn(
                          "shrink-0 inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200",
                          active
                            ? "bg-(--color-accent) text-white"
                            : "bg-(--color-page) text-(--color-text-secondary) hover:text-(--color-text) border border-(--color-border)",
                        )}
                      >
                        <span
                          className="h-4 w-4 rounded-full flex items-center justify-center text-[10px] font-semibold"
                          style={{
                            background: active ? "rgba(255,255,255,0.18)" : `hsl(${hue}, 55%, 88%)`,
                            color: active ? "white" : `hsl(${hue}, 55%, 32%)`,
                          }}
                          aria-hidden="true"
                        >
                          {(c.firstName || "?").charAt(0).toUpperCase()}
                        </span>
                        {c.firstName}
                      </button>
                    );
                  })}
                </div>
              )}

              {/* Animate the body re-mount on tab switch using a key
                  derived from the active child. The .animate-fade-in
                  class re-runs on each remount because every tab
                  yields a fresh subtree. */}
              <div key={activeChild?.id} className="animate-fade-in">
                <h3 className="text-sm font-semibold text-(--color-text) mb-1">
                  What is {activeChild?.firstName} studying?
                </h3>
                <p className="text-xs text-(--color-text-secondary) mb-4">
                  Select subjects and set learning levels. All subjects available regardless of age.
                </p>
                <SubjectLevelPicker
                  selected={childSubjectLevels[activeChild?.id] || {}}
                  onChange={(levels) => setChildSubjectLevels(prev => ({
                    ...prev,
                    [activeChild.id]: levels,
                  }))}
                  showCustom={false}
                />
                <div className="mt-4">
                  <label className="text-xs text-(--color-text-secondary)">Daily learning target (minutes)</label>
                  <div className="flex items-center gap-2 mt-1">
                    <input
                      type="number"
                      value={currentMinutes}
                      onChange={(e) => setChildMinutes(prev => ({
                        ...prev,
                        [activeChild.id]: Math.max(30, Math.min(480, +e.target.value)),
                      }))}
                      className="w-24 px-3 py-2 text-sm border border-(--color-border) rounded-[10px]"
                    />
                    <span className="text-xs text-(--color-text-tertiary)">
                      You decide. {recForGrade.label}: <span className="text-(--color-text-secondary) font-medium">{recForGrade.lo}-{recForGrade.hi} min</span>.
                    </span>
                  </div>
                  {/* Visual range guide — a thin track with the
                      recommended window highlighted and the current
                      value as a dot. Helps the parent locate
                      themselves on the spectrum at a glance. */}
                  <div className="mt-2 h-1.5 rounded-full bg-(--color-border) relative overflow-hidden" aria-hidden="true">
                    <div
                      className="absolute inset-y-0 bg-(--color-accent-light)"
                      style={{
                        left: `${(recForGrade.lo / 480) * 100}%`,
                        width: `${((recForGrade.hi - recForGrade.lo) / 480) * 100}%`,
                      }}
                    />
                    <div
                      className="absolute top-1/2 -translate-y-1/2 h-3 w-3 rounded-full bg-(--color-accent) ring-2 ring-(--color-surface)"
                      style={{
                        left: `calc(${Math.min(100, (currentMinutes / 480) * 100)}% - 6px)`,
                        transition: "left 200ms var(--ease)",
                      }}
                    />
                  </div>
                </div>
              </div>

              <Button
                variant="primary"
                size="lg"
                className="w-full mt-6"
                onClick={async () => {
                  const childId = activeChild.id;
                  const levels = childSubjectLevels[childId] || {};
                  const minutes = childMinutes[childId] || 120;
                  try {
                    await childrenApi.updatePreferences(childId, {
                      subject_levels: levels,
                      daily_duration_minutes: minutes,
                    });
                  } catch { /* preferences can be set later from family page */ }
                  if (profileChildIdx < addedChildren.length - 1) {
                    setProfileChildIdx(profileChildIdx + 1);
                  } else {
                    setStep(4);
                  }
                }}
              >
                {profileChildIdx < addedChildren.length - 1
                  ? `Next: ${addedChildren[profileChildIdx + 1].firstName}`
                  : "Continue to Philosophy"}
              </Button>
            </div>
          );
        })()}

        {/* ── Step 4: Philosophy ── */}
        {step === 4 && (() => {
          // Tiny inline SVG glyphs that evoke each philosophy's
          // character without dragging in a full icon set. Currents
          // are 16px stroke icons; rendered inside a tinted square so
          // the visual language matches the dashboard's bento icons.
          const PHIL_GLYPHS: Record<string, React.ReactNode> = {
            classical: (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                <path d="M4 21h16M5 21V8M19 21V8M9 21V8M15 21V8M3 8h18M5 4h14l-1 4H6z" />
              </svg>
            ),
            charlotte_mason: (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M12 21V8" />
                <path d="M12 8c0-3 2-5 5-5 0 4-2 7-5 7" />
                <path d="M12 13c0-2-1.5-4-4-4 0 3 1.5 5 4 5" />
              </svg>
            ),
            unschooling: (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="9" />
                <path d="M16 8l-3 5-5 3 3-5z" fill="currentColor" stroke="none" />
              </svg>
            ),
            eclectic: (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <circle cx="9" cy="12" r="6" />
                <circle cx="15" cy="12" r="6" />
              </svg>
            ),
            montessori: (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <rect x="4" y="14" width="6" height="6" rx="1" />
                <rect x="14" y="14" width="6" height="6" rx="1" />
                <rect x="9" y="6" width="6" height="6" rx="1" />
              </svg>
            ),
            traditional: (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M4 5h7a3 3 0 0 1 3 3v12H7a3 3 0 0 1-3-3z" />
                <path d="M20 5h-7a3 3 0 0 0-3 3v12h7a3 3 0 0 0 3-3z" />
              </svg>
            ),
          };

          // Autonomy descriptions tailored for the segmented control —
          // they replace the previous separate description block with
          // a single explanatory paragraph that updates with the
          // active selection.
          const AUTONOMY_DETAIL: Record<string, string> = {
            preview_all: "Every AI recommendation lands in your queue before it reaches your child. Highest oversight; expect a daily review.",
            approve_difficult: "AI auto-approves routine recommendations and routes only the harder calls (constitutional concerns, big shifts) to you.",
            trust_within_rules: "AI operates freely inside the rules you've ratified. You see the audit trail; you don't approve every step.",
          };

          return (
            <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 animate-fade-up">
              <h3 className="text-sm font-semibold text-(--color-text) mb-1">Your educational approach</h3>
              <p className="text-xs text-(--color-text-secondary) mb-4">This guides how the AI generates curriculum and activities.</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-6">
                {PHILOSOPHIES.map((p) => {
                  const isSelected = philosophy === p.value;
                  return (
                    <button
                      key={p.value}
                      onClick={() => setPhilosophy(p.value)}
                      aria-pressed={isSelected}
                      className={cn(
                        "text-left p-3 rounded-[12px] border bg-(--color-surface) flex items-start gap-3",
                        "transition-all duration-200 ease-[cubic-bezier(0.25,0.1,0.25,1)]",
                        isSelected
                          ? "border-(--color-accent) ring-2 ring-(--color-accent)/20 scale-[1.02] shadow-[var(--shadow-card)]"
                          : "border-(--color-border) hover:border-(--color-border-strong) hover:scale-[1.01]",
                      )}
                    >
                      <div
                        className={cn(
                          "h-8 w-8 rounded-[8px] flex items-center justify-center shrink-0 transition-colors",
                          isSelected
                            ? "bg-(--color-accent-light) text-(--color-accent)"
                            : "bg-(--color-page) text-(--color-text-tertiary)",
                        )}
                      >
                        {PHIL_GLYPHS[p.value]}
                      </div>
                      <div className="min-w-0">
                        <div className="text-[13px] font-medium text-(--color-text)">{p.label}</div>
                        <div className="text-[11px] text-(--color-text-tertiary) leading-snug">{p.desc}</div>
                      </div>
                    </button>
                  );
                })}
              </div>

              <h4 className="text-xs font-medium text-(--color-text) mb-2">AI autonomy level</h4>
              {/* Segmented control: three equal-width segments share a
                  rounded outer track. The active segment lifts via
                  shadow + accent text; inactive segments stay flat. */}
              <div
                className="grid grid-cols-3 rounded-[10px] border border-(--color-border) bg-(--color-page) p-1 mb-2"
                role="tablist"
                aria-label="AI autonomy level"
              >
                {AUTONOMY.map((a) => {
                  const isActive = autonomy === a.value;
                  return (
                    <button
                      key={a.value}
                      role="tab"
                      aria-selected={isActive}
                      onClick={() => setAutonomy(a.value)}
                      className={cn(
                        "px-2 py-2 text-[11px] font-medium rounded-[8px] transition-all duration-200",
                        isActive
                          ? "bg-(--color-surface) text-(--color-accent) shadow-[var(--shadow-card)]"
                          : "text-(--color-text-secondary) hover:text-(--color-text)",
                      )}
                    >
                      {a.label}
                    </button>
                  );
                })}
              </div>
              <p className="text-[11px] text-(--color-text-secondary) leading-relaxed mb-6 min-h-[3em]">
                {AUTONOMY_DETAIL[autonomy] || AUTONOMY.find((a) => a.value === autonomy)?.desc}
              </p>

              <Button variant="primary" size="lg" onClick={savePhilosophy} disabled={loading} className="w-full">
                {loading ? "Saving..." : "Continue"}
              </Button>
            </div>
          );
        })()}

        {/* ── Step 5: Constitutional Ceremony ── */}
        {step === 5 && !ratified && (
          <div
            className="rounded-[14px] overflow-hidden shadow-[var(--shadow-lg)] animate-fade-up"
            style={{ background: "var(--color-brand-navy)", color: "white" }}
          >
            {/* Gold accent line at the top — reads as the "seal" on a
                founding document. */}
            <div className="h-[3px]" style={{ background: "var(--gold)" }} aria-hidden="true" />

            <div className="p-6 sm:p-7">
              {/* Header */}
              <div className="flex items-start gap-3 mb-5">
                <div
                  className="w-11 h-11 rounded-[10px] flex items-center justify-center shrink-0"
                  style={{ background: "rgba(198,162,78,0.15)" }}
                >
                  <ShieldIcon size={22} className="text-[color:var(--gold)]" />
                </div>
                <div>
                  <h3 className="text-[18px] font-semibold tracking-tight text-white">
                    Establishing your family&apos;s AI constitution
                  </h3>
                  <p className="text-xs text-white/70 mt-1 leading-relaxed">
                    These are the foundational rules that govern how AI interacts with your children.
                    Constitutional rules cannot be changed casually; they require a formal amendment process.
                  </p>
                </div>
              </div>

              {/* Constitutional rule display — translucent gold panel */}
              <div
                className="rounded-[10px] p-4 mb-6 border"
                style={{
                  background: "rgba(198,162,78,0.10)",
                  borderColor: "rgba(198,162,78,0.30)",
                }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <ShieldIcon size={14} className="text-[color:var(--gold)]" />
                  <span className="text-xs font-semibold uppercase tracking-wide text-[color:var(--gold)]">
                    AI Oversight Guarantee
                  </span>
                </div>
                <p className="text-sm text-white/90 leading-relaxed">
                  All AI-generated content and recommendations are logged with full input/output for parent inspection.
                  AI cannot modify child state without governance approval.
                </p>
              </div>

              {/* Affirmations — sequential fade-up. Each parent
                  affirmation appears one at a time so the parent
                  reads them deliberately. */}
              <div className="space-y-3 mb-6">
                {CEREMONY_AFFIRMATIONS.map((text, i) => {
                  const checked = ceremonyChecks[i];
                  return (
                    <label
                      key={i}
                      className={cn(
                        "flex items-start gap-3 cursor-pointer group rounded-[10px] p-3 transition-colors",
                        "animate-fade-up",
                        i === 0 ? "stagger-2" : i === 1 ? "stagger-3" : "stagger-4",
                        checked ? "bg-white/5" : "hover:bg-white/5",
                      )}
                      onClick={() => {
                        setCeremonyChecks((prev) => { const next = [...prev]; next[i] = !next[i]; return next; });
                      }}
                    >
                      <span
                        className={cn(
                          "w-5 h-5 shrink-0 mt-0.5 rounded-[4px] border-2 flex items-center justify-center transition-all",
                          checked
                            ? "border-transparent"
                            : "border-white/40 group-hover:border-white/60",
                        )}
                        style={checked ? { background: "var(--gold)", borderColor: "var(--gold)" } : undefined}
                      >
                        {checked && (
                          <svg className="w-3 h-3 text-(--color-brand-navy)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3.5} aria-hidden="true">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </span>
                      <span className="text-sm leading-relaxed text-white/95">{text}</span>
                    </label>
                  );
                })}
              </div>

              {/* Reason field — significant copy, larger text, more
                  comfortable line height. The textarea uses a dark
                  translucent fill so it reads as part of the navy
                  document, not a popped-in form control. */}
              <div className="mb-6">
                <label className="text-sm font-medium text-white block mb-2">
                  Why are you homeschooling?
                </label>
                <p className="text-xs text-white/60 mb-2 leading-relaxed">
                  This shapes how METHEAN serves your family.
                </p>
                <textarea
                  value={ceremonyReason}
                  onChange={(e) => setCeremonyReason(e.target.value)}
                  placeholder="This is your founding statement — what matters to your family..."
                  rows={4}
                  className="w-full px-4 py-3 text-[15px] leading-[1.7] rounded-[10px] resize-none focus:outline-none text-white placeholder:text-white/35"
                  style={{
                    background: "rgba(255,255,255,0.06)",
                    border: "1px solid rgba(255,255,255,0.18)",
                  }}
                />
                {ceremonyReason.length > 0 && ceremonyReason.trim().length < 20 && (
                  <p className="text-[11px] text-white/55 mt-1.5">
                    {20 - ceremonyReason.trim().length} more characters needed
                  </p>
                )}
              </div>

              {/* Ratify button — appears with scale-in once all three
                  affirmations are checked AND the reason is valid.
                  Wrapped in a min-height container so the layout
                  doesn't jump when the button materializes. */}
              <div className="min-h-[52px]">
                {allCeremonyChecked && ceremonyReasonValid ? (
                  <Button
                    variant="gold"
                    size="lg"
                    className="w-full animate-scale-in shadow-[0_0_24px_rgba(198,162,78,0.35)]"
                    onClick={handleRatify}
                  >
                    Ratify Constitution
                  </Button>
                ) : (
                  <div className="w-full h-[52px] rounded-[10px] flex items-center justify-center text-xs text-white/45"
                    style={{ border: "1px dashed rgba(255,255,255,0.18)" }}>
                    {!allCeremonyChecked
                      ? `Affirm all three above (${ceremonyChecks.filter(Boolean).length}/3)`
                      : "Add your founding statement above"}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ── Step 5: Ratification confirmation ── */}
        {step === 5 && ratified && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8 text-center animate-scale-in overflow-hidden">
            {/* Gold accent line at the very top mirrors the document
                "seal" on the ceremony itself — visual continuity
                from "ratifying" to "ratified". */}
            <div className="h-[2px] -mx-8 -mt-8 mb-6" style={{ background: "var(--gold)" }} aria-hidden="true" />
            <div className="flex justify-center mb-4">
              <div
                className="w-16 h-16 rounded-full flex items-center justify-center"
                style={{
                  background:
                    "radial-gradient(circle, rgba(198,162,78,0.20) 0%, rgba(198,162,78,0) 65%)",
                }}
              >
                <ShieldIcon size={36} className="text-[color:var(--gold)]" />
              </div>
            </div>
            <h2 className="text-[20px] font-semibold tracking-tight text-(--color-text) mb-1">
              Your family&apos;s constitution is ratified.
            </h2>
            <p className="text-sm text-(--color-text-secondary) leading-relaxed">
              METHEAN now operates under your authority.
            </p>
          </div>
        )}

        {/* ── Step 6: Curriculum Path ── */}
        {step === 6 && !loading && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
            {currentChildIdx < addedChildren.length ? (
              <>
                <h3 className="text-sm font-semibold text-(--color-text) mb-1">
                  Build {addedChildren[currentChildIdx].firstName}'s curriculum
                </h3>
                <p className="text-xs text-(--color-text-secondary) mb-4">
                  {Object.keys(childSubjectLevels[addedChildren[currentChildIdx]?.id] || {}).length || 0} subjects selected
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

        {/* ── Step 6/7: Loading ── */}
        {/* ── Step 6 progress: per-(child, subject) checklist ── */}
        {loading && step === 6 && (() => {
          // Reconstruct the same per-child subject lists that
          // generateCurricula() iterates over so the UI mirrors the
          // backend's exact sequence. We don't change the API call —
          // we just observe its side effects via generatingFor.
          const eligible = addedChildren.filter(
            (c) => (curriculumChoices[c.id] || "skip") !== "skip",
          );
          const totalSubjects = eligible.reduce((sum, c) => {
            const levels = childSubjectLevels[c.id] || {};
            const subjects = Object.keys(levels).length > 0
              ? Object.keys(levels)
              : ["reading", "mathematics"];
            return sum + subjects.length;
          }, 0);
          const completedCount = doneSubjects.size;
          const pct = totalSubjects > 0
            ? Math.min(100, Math.round((completedCount / totalSubjects) * 100))
            : 0;
          return (
            <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 animate-fade-up">
              <h3 className="text-sm font-semibold text-(--color-text) mb-1">Building your curricula</h3>
              <p className="text-xs text-(--color-text-secondary) mb-4">
                METHEAN is scaffolding each subject under your governance. This may take a moment.
              </p>

              {/* Progress bar */}
              <div className="h-1.5 rounded-full bg-(--color-border) overflow-hidden mb-1">
                <div
                  className="h-full bg-(--color-accent) transition-all duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)]"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <p className="text-[11px] text-(--color-text-tertiary) mb-4">
                {completedCount} of {totalSubjects} subjects scaffolded
              </p>

              {/* Per-(child, subject) checklist */}
              <div className="space-y-3">
                {eligible.map((c) => {
                  const levels = childSubjectLevels[c.id] || {};
                  const subjects = Object.keys(levels).length > 0
                    ? Object.keys(levels).map((id) =>
                        id.replace(/_/g, " ").replace(/\b\w/g, (ch) => ch.toUpperCase()),
                      )
                    : ["Reading", "Mathematics"];
                  const hue = avatarHueFor(c.firstName || c.id);
                  return (
                    <div key={c.id} className="rounded-[10px] border border-(--color-border) bg-(--color-page) p-3">
                      <div className="flex items-center gap-2 mb-2">
                        <span
                          className="h-6 w-6 rounded-full flex items-center justify-center text-[11px] font-semibold"
                          style={{
                            background: `hsl(${hue}, 55%, 88%)`,
                            color: `hsl(${hue}, 55%, 32%)`,
                          }}
                          aria-hidden="true"
                        >
                          {(c.firstName || "?").charAt(0).toUpperCase()}
                        </span>
                        <span className="text-[13px] font-medium text-(--color-text)">{c.firstName}</span>
                      </div>
                      <ul className="space-y-1.5 pl-1">
                        {subjects.map((subject) => {
                          const key = `${c.firstName}: ${subject}`;
                          const isCurrent = generatingFor === key;
                          const isDone = doneSubjects.has(key);
                          return (
                            <li key={subject} className="flex items-center gap-2 text-[12px]">
                              {isDone ? (
                                <span
                                  className="h-4 w-4 rounded-full bg-(--color-success) flex items-center justify-center shrink-0 animate-fade-in"
                                  aria-hidden="true"
                                >
                                  <svg className="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3.5}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                                  </svg>
                                </span>
                              ) : isCurrent ? (
                                <span className="h-4 w-4 rounded-full border-2 border-(--color-accent)/30 border-t-(--color-accent) animate-spin shrink-0" aria-hidden="true" />
                              ) : (
                                <span className="h-4 w-4 rounded-full border border-(--color-border) shrink-0" aria-hidden="true" />
                              )}
                              <span className={cn(
                                isDone && "text-(--color-text-tertiary)",
                                isCurrent && "text-(--color-text) font-medium",
                                !isDone && !isCurrent && "text-(--color-text-secondary)",
                              )}>
                                {subject}
                              </span>
                            </li>
                          );
                        })}
                      </ul>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })()}

        {/* ── Step 7 progress: per-child plan generation ── */}
        {loading && step === 7 && (() => {
          const eligible = addedChildren.filter(
            (c) => (curriculumChoices[c.id] || "skip") !== "skip",
          );
          // planProgress is appended to as each child starts; the
          // last entry is "in-progress" while loading is true.
          const lastIdx = planProgress.length - 1;
          const currentName = lastIdx >= 0 ? planProgress[lastIdx] : "";
          const completedNames = new Set(planProgress.slice(0, lastIdx));
          const pct = eligible.length > 0
            ? Math.min(100, Math.round(((completedNames.size + (currentName ? 0.5 : 0)) / eligible.length) * 100))
            : 0;
          return (
            <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 animate-fade-up">
              <h3 className="text-sm font-semibold text-(--color-text) mb-1">Building this week&apos;s plans</h3>
              <p className="text-xs text-(--color-text-secondary) mb-4">
                Translating curricula into daily activities. This is the last step.
              </p>
              <div className="h-1.5 rounded-full bg-(--color-border) overflow-hidden mb-1">
                <div
                  className="h-full bg-(--color-accent) transition-all duration-500 ease-[cubic-bezier(0.25,0.1,0.25,1)]"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <p className="text-[11px] text-(--color-text-tertiary) mb-4">
                {completedNames.size} of {eligible.length} {eligible.length === 1 ? "child" : "children"} planned
              </p>
              <ul className="space-y-2">
                {eligible.map((c) => {
                  const isDone = completedNames.has(c.firstName);
                  const isCurrent = !isDone && currentName === c.firstName;
                  const hue = avatarHueFor(c.firstName || c.id);
                  return (
                    <li key={c.id} className="flex items-center gap-3 rounded-[10px] border border-(--color-border) bg-(--color-page) px-3 py-2">
                      <span
                        className="h-7 w-7 rounded-full flex items-center justify-center text-[12px] font-semibold shrink-0"
                        style={{
                          background: `hsl(${hue}, 55%, 88%)`,
                          color: `hsl(${hue}, 55%, 32%)`,
                        }}
                        aria-hidden="true"
                      >
                        {(c.firstName || "?").charAt(0).toUpperCase()}
                      </span>
                      <span className="flex-1 text-[13px] text-(--color-text) font-medium">{c.firstName}</span>
                      {isDone ? (
                        <span className="h-5 w-5 rounded-full bg-(--color-success) flex items-center justify-center shrink-0 animate-fade-in" aria-hidden="true">
                          <svg className="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                          </svg>
                        </span>
                      ) : isCurrent ? (
                        <span className="h-5 w-5 rounded-full border-2 border-(--color-accent)/30 border-t-(--color-accent) animate-spin shrink-0" aria-hidden="true" />
                      ) : (
                        <span className="h-5 w-5 rounded-full border border-(--color-border) shrink-0" aria-hidden="true" />
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })()}

        {/* ── Step 7: Generate Plans (idle) ── */}
        {step === 7 && !loading && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 text-center animate-fade-up">
            <div
              className="w-14 h-14 mx-auto mb-4 rounded-full flex items-center justify-center"
              style={{ background: "rgba(45,106,79,0.10)" }}
            >
              <svg className="h-7 w-7 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5} aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-base font-semibold text-(--color-text) mb-1">Curricula ready</h3>
            <p className="text-xs text-(--color-text-secondary) mb-6">
              Now let&apos;s create this week&apos;s activity schedule.
            </p>
            <Button variant="primary" size="lg" onClick={generatePlans} className="w-full">
              Generate First Week&apos;s Plan
            </Button>
            <button
              onClick={() => { setStep(8); setSummary({ rules: 4, activities: {} }); }}
              className="block mx-auto mt-3 text-xs text-(--color-text-tertiary) hover:underline"
            >
              Skip — I&apos;ll generate plans later
            </button>
          </div>
        )}

        {/* ── Step 8: All Set — dashboard preview ── */}
        {step === 8 && (() => {
          const totalActivities = Object.values(summary.activities).reduce(
            (s, n) => s + (n || 0),
            0,
          );
          const ratifiedCount = constitutionalRules.length;
          return (
            <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 sm:p-8">
              <div className="text-center mb-6 animate-fade-up">
                <div
                  className="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center"
                  style={{
                    background:
                      "radial-gradient(circle, rgba(198,162,78,0.20) 0%, rgba(198,162,78,0) 65%)",
                  }}
                >
                  <ShieldIcon size={32} className="text-[color:var(--gold)]" />
                </div>
                <h2 className="text-[22px] font-semibold tracking-tight text-(--color-text)">
                  Your family is ready
                </h2>
                <p className="text-sm text-(--color-text-secondary) mt-1">
                  Here&apos;s what we built together.
                </p>
              </div>

              {/* Bento metric tiles — same visual language as the
                  parent dashboard so the transition feels continuous. */}
              <div className="grid grid-cols-2 gap-3 mb-5">
                <div className="bg-(--color-page) rounded-[12px] border border-(--color-border) p-4 animate-fade-up stagger-1">
                  <div className="text-[10px] text-(--color-text-tertiary) uppercase tracking-wide mb-1">
                    Children
                  </div>
                  <div className="text-[22px] font-semibold tracking-tight text-(--color-text) leading-none">
                    {addedChildren.length}
                  </div>
                </div>
                <div className="bg-(--color-page) rounded-[12px] border border-(--color-border) p-4 animate-fade-up stagger-2">
                  <div className="text-[10px] text-(--color-text-tertiary) uppercase tracking-wide mb-1">
                    Governance rules
                  </div>
                  <div className="text-[22px] font-semibold tracking-tight text-(--color-text) leading-none">
                    {summary.rules}
                  </div>
                </div>
                <div className="bg-(--color-page) rounded-[12px] border border-(--color-border) p-4 animate-fade-up stagger-3">
                  <div className="text-[10px] text-(--color-text-tertiary) uppercase tracking-wide mb-1">
                    Activities this week
                  </div>
                  <div className="text-[22px] font-semibold tracking-tight text-(--color-text) leading-none">
                    {totalActivities}
                  </div>
                </div>
                <div className="bg-(--color-page) rounded-[12px] border border-(--color-border) p-4 animate-fade-up stagger-4">
                  <div className="text-[10px] text-(--color-text-tertiary) uppercase tracking-wide mb-1">
                    Constitutional
                  </div>
                  <div className="text-[22px] font-semibold tracking-tight text-(--color-text) leading-none">
                    {ratifiedCount > 0 ? ratifiedCount : "Ratified"}
                  </div>
                </div>
              </div>

              {/* Per-child activity breakdown */}
              {Object.keys(summary.activities).length > 0 && (
                <div className="space-y-1.5 mb-5 animate-fade-up stagger-5">
                  {Object.entries(summary.activities).map(([name, count]) => {
                    const hue = avatarHueFor(name);
                    return (
                      <div
                        key={name}
                        className="flex items-center gap-3 px-3 py-2 bg-(--color-page) rounded-[10px] border border-(--color-border)"
                      >
                        <span
                          className="h-7 w-7 rounded-full flex items-center justify-center text-[11px] font-semibold shrink-0"
                          style={{
                            background: `hsl(${hue}, 55%, 88%)`,
                            color: `hsl(${hue}, 55%, 32%)`,
                          }}
                          aria-hidden="true"
                        >
                          {name.charAt(0).toUpperCase()}
                        </span>
                        <span className="flex-1 text-sm text-(--color-text) font-medium">{name}</span>
                        <span className="text-xs text-(--color-text-secondary)">
                          {count} {count === 1 ? "activity" : "activities"} this week
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Constitution recap */}
              {(constitutionalRules.length > 0 || ceremonyReason) && (
                <div
                  className="mb-6 p-4 rounded-[10px] border animate-fade-up stagger-6"
                  style={{
                    background: "rgba(139,115,85,0.06)",
                    borderColor: "rgba(139,115,85,0.18)",
                  }}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <ShieldIcon size={14} className="text-(--color-constitutional)" />
                    <span className="text-[11px] font-semibold text-(--color-constitutional) uppercase tracking-wide">
                      Constitution ratified
                    </span>
                  </div>
                  {constitutionalRules.length > 0 && (
                    <ul className="space-y-1 mb-2">
                      {constitutionalRules.map((name, i) => (
                        <li key={i} className="flex items-center gap-1.5 text-[11px] text-(--color-text-secondary)">
                          <span className="w-1 h-1 rounded-full bg-(--color-constitutional) shrink-0" />
                          {name}
                        </li>
                      ))}
                    </ul>
                  )}
                  {ceremonyReason && (
                    <p className="text-[12px] text-(--color-text-secondary) italic leading-relaxed border-t border-(--color-constitutional)/15 pt-2 mt-2">
                      &ldquo;{ceremonyReason}&rdquo;
                    </p>
                  )}
                </div>
              )}

              <div className="space-y-2 animate-fade-up stagger-7">
                <Button
                  variant="gold"
                  size="lg"
                  onClick={() => router.push("/dashboard")}
                  className="w-full"
                >
                  Go to Dashboard
                </Button>
                {addedChildren.length > 0 && (
                  <Button
                    variant="secondary"
                    size="md"
                    onClick={() => router.push("/child")}
                    className="w-full"
                  >
                    Open {addedChildren[0].firstName}&apos;s learning
                  </Button>
                )}
              </div>
            </div>
          );
        })()}
        </div>{/* end step slide container */}
        </div>
      </div>
    </div>
  );
}
