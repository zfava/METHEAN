"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { children as childrenApi, governance, annualCurriculum, plans, curriculum } from "@/lib/api";
import { MetheanLogoVertical } from "@/components/Brand";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { useToast } from "@/components/Toast";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { cn } from "@/lib/cn";
import SubjectLevelPicker from "@/components/SubjectLevelPicker";

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

const GRADES = ["K", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"];

const CEREMONY_AFFIRMATIONS = [
  "I understand that AI in METHEAN advises but never decides. Every recommendation flows through my governance rules.",
  "I understand that I can inspect every AI interaction, including the full prompt and response, at any time.",
  "I understand that constitutional rules require a formal amendment process to change, protecting my family's values from casual modification.",
] as const;

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
        const resp = await fetch(`${API}/children/${child.id}/today`, { credentials: "include" });
        if (resp.ok) {
          const acts = await resp.json();
          activityCounts[child.firstName] = Array.isArray(acts) ? acts.length : 0;
        }
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
              {[2, 3, 4, 5, 6, 7, 8].map((s) => (
                <div key={s} className={cn("w-7 h-1 rounded-full transition-colors", step >= s ? "bg-(--color-accent)" : "bg-(--color-border)")} />
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
                <option value="">Optional</option>
                {GRADES.map((g) => <option key={g} value={g}>{g}</option>)}
              </select>
              <Button variant="primary" size="md" onClick={addChild} disabled={!newName.trim()}>Add</Button>
            </div>

            {addedChildren.length > 0 && (
              <div className="space-y-2 mb-4">
                {addedChildren.map((c) => (
                  <div key={c.id} className="flex items-center justify-between px-3 py-2 bg-(--color-page) rounded-[10px]">
                    <span className="text-sm text-(--color-text)">{c.firstName}{c.grade && <span className="text-(--color-text-tertiary)"> · {c.grade}</span>}</span>
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

        {/* ── Step 3: Learning Profile ── */}
        {step === 3 && addedChildren.length > 0 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">
              What is {addedChildren[profileChildIdx]?.firstName} studying?
            </h3>
            <p className="text-xs text-(--color-text-secondary) mb-4">
              Select subjects and set learning levels. All subjects available regardless of age.
            </p>
            <SubjectLevelPicker
              selected={childSubjectLevels[addedChildren[profileChildIdx]?.id] || {}}
              onChange={(levels) => setChildSubjectLevels(prev => ({
                ...prev,
                [addedChildren[profileChildIdx].id]: levels,
              }))}
              showCustom={false}
            />
            <div className="mt-4">
              <label className="text-xs text-(--color-text-secondary)">Daily learning target (minutes)</label>
              <div className="flex items-center gap-2 mt-1">
                <input
                  type="number"
                  value={childMinutes[addedChildren[profileChildIdx]?.id] || 120}
                  onChange={(e) => setChildMinutes(prev => ({
                    ...prev,
                    [addedChildren[profileChildIdx].id]: Math.max(30, Math.min(480, +e.target.value)),
                  }))}
                  className="w-24 px-3 py-2 text-sm border border-(--color-border) rounded-[10px]"
                />
                <span className="text-xs text-(--color-text-tertiary)">You decide. Suggested: 90-240.</span>
              </div>
            </div>
            <Button
              variant="primary"
              size="lg"
              className="w-full mt-6"
              onClick={async () => {
                const childId = addedChildren[profileChildIdx].id;
                const levels = childSubjectLevels[childId] || {};
                const minutes = childMinutes[childId] || 120;
                const csrf = getCsrf();
                try {
                  await fetch(`${API}/children/${childId}/preferences`, {
                    method: "PUT",
                    credentials: "include",
                    headers: {
                      "Content-Type": "application/json",
                      ...(csrf ? { "X-CSRF-Token": csrf } : {}),
                    },
                    body: JSON.stringify({
                      subject_levels: levels,
                      daily_duration_minutes: minutes,
                    }),
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
        )}

        {/* ── Step 4: Philosophy ── */}
        {step === 4 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">Your educational approach</h3>
            <p className="text-xs text-(--color-text-secondary) mb-4">This guides how the AI generates curriculum and activities.</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-6">
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

        {/* ── Step 5: Constitutional Ceremony ── */}
        {step === 5 && !ratified && (
          <Card padding="p-0" borderLeft="border-l-(--color-constitutional)">
            <div className="p-6">
              {/* Header */}
              <div className="flex items-start gap-3 mb-5">
                <div className="w-10 h-10 rounded-[10px] bg-(--color-constitutional-light) flex items-center justify-center shrink-0">
                  <ShieldIcon size={22} className="text-(--color-constitutional)" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-(--color-text)">
                    Establishing Your Family's AI Constitution
                  </h3>
                  <p className="text-xs text-(--color-text-secondary) mt-1 leading-relaxed">
                    These are the foundational rules that govern how AI interacts with your children.
                    Constitutional rules cannot be changed casually; they require a formal amendment process.
                  </p>
                </div>
              </div>

              {/* Constitutional rule display */}
              <div className="bg-(--color-constitutional-light) border border-(--color-constitutional)/15 rounded-[10px] p-4 mb-6">
                <div className="flex items-center gap-2 mb-2">
                  <ShieldIcon size={14} className="text-(--color-constitutional)" />
                  <span className="text-xs font-semibold text-(--color-constitutional) uppercase tracking-wide">AI Oversight Guarantee</span>
                </div>
                <p className="text-sm text-(--color-text) leading-relaxed">
                  All AI-generated content and recommendations are logged with full input/output for parent inspection.
                  AI cannot modify child state without governance approval.
                </p>
              </div>

              {/* Affirmation checkboxes */}
              <div className="space-y-3 mb-6">
                {CEREMONY_AFFIRMATIONS.map((text, i) => (
                  <label key={i} className="flex items-start gap-3 cursor-pointer group" onClick={() => {
                    setCeremonyChecks((prev) => { const next = [...prev]; next[i] = !next[i]; return next; });
                  }}>
                    <span className={cn(
                      "w-5 h-5 shrink-0 mt-0.5 rounded-[4px] border-2 flex items-center justify-center transition-all",
                      ceremonyChecks[i]
                        ? "bg-(--gold) border-(--gold)"
                        : "border-(--color-border-strong) group-hover:border-(--color-text-tertiary)"
                    )}>
                      {ceremonyChecks[i] && (
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3.5}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      )}
                    </span>
                    <span className="text-xs text-(--color-text) leading-relaxed">{text}</span>
                  </label>
                ))}
              </div>

              {/* Reason field */}
              <div className="mb-6">
                <label className="text-xs font-medium text-(--color-text) block mb-1.5">
                  In your own words, why are these protections important to your family?
                </label>
                <textarea
                  value={ceremonyReason}
                  onChange={(e) => setCeremonyReason(e.target.value)}
                  placeholder="This is your founding statement — what matters to your family..."
                  rows={3}
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) resize-none focus:outline-none focus:ring-1 focus:ring-(--color-constitutional) text-(--color-text)"
                />
                {ceremonyReason.length > 0 && ceremonyReason.trim().length < 20 && (
                  <p className="text-[10px] text-(--color-text-tertiary) mt-1">
                    {20 - ceremonyReason.trim().length} more characters needed
                  </p>
                )}
              </div>

              {/* Ratify button */}
              <Button
                variant="gold"
                size="lg"
                className="w-full"
                disabled={!allCeremonyChecked || !ceremonyReasonValid}
                onClick={handleRatify}
              >
                Ratify Constitution
              </Button>
            </div>
          </Card>
        )}

        {/* ── Step 5: Ratification confirmation ── */}
        {step === 5 && ratified && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8 text-center">
            <div className="flex justify-center mb-4">
              <div
                className="w-16 h-16 rounded-full bg-(--color-constitutional-light) flex items-center justify-center"
                style={{ animation: "ratify-glow 500ms ease-out forwards" }}
              >
                <ShieldIcon size={32} className="text-(--color-constitutional)" />
              </div>
            </div>
            <h2 className="text-lg font-semibold text-(--color-text) mb-1">
              Your family's AI constitution is established.
            </h2>
            <p className="text-xs text-(--color-text-secondary)">
              These protections are now active for every AI interaction.
            </p>
            <style>{`
              @keyframes ratify-glow {
                0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(184, 134, 11, 0.3); }
                50% { transform: scale(1.1); box-shadow: 0 0 24px 8px rgba(184, 134, 11, 0.2); }
                100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(184, 134, 11, 0); }
              }
            `}</style>
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
        {loading && (step === 6 || step === 7) && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8 text-center">
            <div className="w-10 h-10 mx-auto mb-4 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
            <p className="text-sm text-(--color-text) mb-1">
              {step === 6 && generatingFor && `Generating ${generatingFor}...`}
              {step === 7 && planProgress.length > 0 && `Creating ${planProgress[planProgress.length - 1]}'s plan...`}
              {!generatingFor && step === 6 && "Setting up curricula..."}
            </p>
            <p className="text-xs text-(--color-text-tertiary)">This may take a moment.</p>
          </div>
        )}

        {/* ── Step 7: Generate Plans ── */}
        {step === 7 && !loading && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6 text-center">
            <h3 className="text-sm font-semibold text-(--color-text) mb-2">Curricula ready!</h3>
            <p className="text-xs text-(--color-text-secondary) mb-6">
              Now let's create this week's activity schedule.
            </p>
            <Button variant="primary" size="lg" onClick={generatePlans} className="w-full">
              Generate First Week's Plan
            </Button>
            <button onClick={() => { setStep(8); setSummary({ rules: 4, activities: {} }); }}
              className="block mx-auto mt-3 text-xs text-(--color-text-tertiary) hover:underline">
              Skip — I'll generate plans later
            </button>
          </div>
        )}

        {/* ── Step 8: All Set ── */}
        {step === 8 && (
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-8">
            <div className="text-center mb-6">
              <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-(--color-success-light) flex items-center justify-center">
                <svg className="w-7 h-7 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-(--color-text)">Your family is ready!</h2>
            </div>

            {/* ── Your Constitution ── */}
            <div className="mb-5 p-4 bg-(--color-constitutional-light) border border-(--color-constitutional)/15 rounded-[10px]">
              <div className="flex items-center gap-2 mb-2">
                <ShieldIcon size={16} className="text-(--color-constitutional)" />
                <span className="text-xs font-semibold text-(--color-constitutional)">Constitutional Governance Established</span>
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
                <div className="border-t border-(--color-constitutional)/15 pt-2 mt-2">
                  <p className="text-[11px] text-(--color-text-secondary) italic leading-relaxed">
                    &ldquo;{ceremonyReason}&rdquo;
                  </p>
                </div>
              )}
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
              <div className="mb-6 p-3 bg-(--color-page) rounded-[10px]">
                <p className="text-xs text-(--color-text-secondary) font-medium">{summary.rules} governance rules protecting your family's education.</p>
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
