"use client";

import { useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

const PHILOSOPHIES = [
  { value: "classical", label: "Classical", desc: "Trivium-based: grammar, logic, rhetoric stages" },
  { value: "charlotte_mason", label: "Charlotte Mason", desc: "Living books, narration, nature study, habit training" },
  { value: "unschooling", label: "Unschooling", desc: "Child-led, interest-driven, experiential" },
  { value: "eclectic", label: "Eclectic", desc: "Best practices from multiple approaches" },
  { value: "montessori", label: "Montessori", desc: "Prepared environment, self-directed, hands-on" },
  { value: "traditional", label: "Traditional", desc: "Structured curriculum, textbook-based, grade-level standards" },
  { value: "custom", label: "Custom", desc: "Define your own approach" },
];

const RELIGIONS = [
  { value: "christian", label: "Christian" },
  { value: "catholic", label: "Catholic" },
  { value: "jewish", label: "Jewish" },
  { value: "islamic", label: "Islamic" },
  { value: "secular", label: "Secular" },
  { value: "other", label: "Other" },
];

const STANCES = [
  { value: "exclude", label: "Exclude" },
  { value: "present_alternative", label: "Present Alternative" },
  { value: "parent_led_only", label: "Parent-Led Only" },
  { value: "allow", label: "Allow" },
];

const AUTONOMY_LEVELS = [
  { value: "preview_all", label: "Preview All", desc: "You review every AI recommendation before your child sees it. Maximum control, most parent involvement." },
  { value: "approve_difficult", label: "Approve Difficult", desc: "Easy activities are auto-approved. Challenging or sensitive content requires your review. Recommended for most families." },
  { value: "trust_within_rules", label: "Trust Within Rules", desc: "The AI operates freely within your governance rules. You only see items that violate a rule." },
  { value: "full_autonomy", label: "Full Autonomy", desc: "The AI handles day-to-day decisions. You review weekly summaries. Least parent involvement." },
];

const stancePreview: Record<string, (topic: string) => string> = {
  exclude: (t) => `The AI will never include content about "${t}".`,
  present_alternative: (t) => `The AI will present both mainstream and alternative perspectives on "${t}".`,
  parent_led_only: (t) => `The AI will not teach "${t}" directly — only if you explicitly assign it.`,
  allow: (t) => `The AI may include content about "${t}" without restrictions.`,
};

interface Boundary {
  topic: string;
  stance: string;
  notes: string;
}

export default function PhilosophyPage() {
  const [philosophy, setPhilosophy] = useState("eclectic");
  const [philosophyDesc, setPhilosophyDesc] = useState("");
  const [religion, setReligion] = useState("secular");
  const [religionNotes, setReligionNotes] = useState("");
  const [boundaries, setBoundaries] = useState<Boundary[]>([]);
  const [autonomy, setAutonomy] = useState("approve_difficult");
  const [prefs, setPrefs] = useState({
    socratic_method: true,
    memorization_valued: false,
    standardized_testing: false,
    competitive_grading: false,
    collaborative_learning: true,
  });
  const [customs, setCustoms] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const resp = await fetch(`${API}/household/philosophy`, { credentials: "include" });
      if (resp.ok) {
        const data = await resp.json();
        if (data.educational_philosophy) setPhilosophy(data.educational_philosophy);
        if (data.philosophy_description) setPhilosophyDesc(data.philosophy_description);
        if (data.religious_framework) setReligion(data.religious_framework);
        if (data.religious_notes) setReligionNotes(data.religious_notes);
        if (data.content_boundaries) setBoundaries(data.content_boundaries);
        if (data.ai_autonomy_level) setAutonomy(data.ai_autonomy_level);
        if (data.pedagogical_preferences) setPrefs({ ...prefs, ...data.pedagogical_preferences });
        if (data.custom_constraints) setCustoms(data.custom_constraints);
      }
    } catch {} finally { setLoading(false); }
  }

  async function save() {
    setSaving(true);
    setSaved(false);
    const csrf = getCsrf();
    await fetch(`${API}/household/philosophy`, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body: JSON.stringify({
        educational_philosophy: philosophy,
        philosophy_description: philosophyDesc || undefined,
        religious_framework: religion,
        religious_notes: religionNotes || undefined,
        content_boundaries: boundaries.filter((b) => b.topic.trim()),
        ai_autonomy_level: autonomy,
        pedagogical_preferences: prefs,
        custom_constraints: customs.filter((c) => c.trim()),
      }),
    });
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 4000);
  }

  function addBoundary() { setBoundaries([...boundaries, { topic: "", stance: "exclude", notes: "" }]); }
  function updateBoundary(i: number, field: keyof Boundary, value: string) {
    const next = [...boundaries]; next[i] = { ...next[i], [field]: value }; setBoundaries(next);
  }
  function removeBoundary(i: number) { setBoundaries(boundaries.filter((_, j) => j !== i)); }

  if (loading) return <div className="max-w-3xl text-sm text-slate-400">Loading...</div>;

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-xl font-semibold text-slate-800">Educational Philosophy</h1>
        <p className="text-sm text-slate-500 mt-1">
          Your family&apos;s foundational principles. These guide every AI recommendation.
        </p>
      </div>

      {/* ── Section 1: Educational Approach ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">
          1. Educational Approach
        </h2>
        <div className="grid grid-cols-2 gap-2">
          {PHILOSOPHIES.map((p) => (
            <button key={p.value} onClick={() => setPhilosophy(p.value)}
              className={`text-left p-3.5 rounded-lg border-2 transition-colors ${
                philosophy === p.value
                  ? "border-blue-500 bg-blue-50"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >
              <div className="text-sm font-medium text-slate-800">{p.label}</div>
              <div className="text-xs text-slate-500 mt-0.5">{p.desc}</div>
            </button>
          ))}
        </div>
        <textarea
          value={philosophyDesc} onChange={(e) => setPhilosophyDesc(e.target.value)}
          placeholder="Describe your approach in your own words (optional)"
          className="w-full mt-3 px-3 py-2 text-sm border border-slate-200 rounded-lg resize-none h-20 focus:outline-none focus:ring-1 focus:ring-blue-400"
        />
      </section>

      {/* ── Section 2: Faith & Worldview ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">
          2. Faith &amp; Worldview
        </h2>
        <div className="flex flex-wrap gap-2 mb-3">
          {RELIGIONS.map((r) => (
            <button key={r.value} onClick={() => setReligion(r.value)}
              className={`px-4 py-2 text-sm rounded-lg border-2 transition-colors ${
                religion === r.value
                  ? "border-blue-500 bg-blue-50 font-medium"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >{r.label}</button>
          ))}
        </div>
        <textarea
          value={religionNotes} onChange={(e) => setReligionNotes(e.target.value)}
          placeholder="Any specifics (denomination, traditions, etc.)"
          className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg resize-none h-16 focus:outline-none focus:ring-1 focus:ring-blue-400"
        />
        <p className="text-xs text-slate-400 mt-1">This informs how the AI presents topics with worldview implications.</p>
      </section>

      {/* ── Section 3: Content Boundaries ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">
          3. Content Boundaries
        </h2>
        {boundaries.length === 0 && (
          <p className="text-xs text-slate-400 mb-3">No boundaries set. The AI will use its default judgment on all topics.</p>
        )}
        <div className="space-y-3">
          {boundaries.map((b, i) => (
            <div key={i} className="bg-white border border-slate-200 rounded-lg p-3">
              <div className="flex gap-2 mb-2">
                <input type="text" value={b.topic} onChange={(e) => updateBoundary(i, "topic", e.target.value)}
                  placeholder="Topic (e.g. evolution)" className="flex-1 px-2 py-1.5 text-sm border border-slate-200 rounded" />
                <select value={b.stance} onChange={(e) => updateBoundary(i, "stance", e.target.value)}
                  className="px-2 py-1.5 text-sm border border-slate-200 rounded">
                  {STANCES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
                <button onClick={() => removeBoundary(i)} className="text-xs text-red-500 hover:text-red-700 px-2">Remove</button>
              </div>
              <input type="text" value={b.notes} onChange={(e) => updateBoundary(i, "notes", e.target.value)}
                placeholder="Notes (optional)" className="w-full px-2 py-1 text-xs border border-slate-100 rounded mb-1" />
              {b.topic && b.stance && (
                <p className="text-[11px] text-blue-600 italic">
                  {stancePreview[b.stance]?.(b.topic) || ""}
                </p>
              )}
            </div>
          ))}
        </div>
        <button onClick={addBoundary}
          className="mt-2 px-3 py-1.5 text-xs font-medium text-blue-600 border border-blue-300 rounded-lg hover:bg-blue-50">
          + Add Boundary
        </button>
      </section>

      {/* ── Section 4: AI Autonomy ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">
          4. AI Autonomy Level
        </h2>
        <div className="space-y-2">
          {AUTONOMY_LEVELS.map((a) => (
            <button key={a.value} onClick={() => setAutonomy(a.value)}
              className={`w-full text-left p-4 rounded-lg border-2 transition-colors ${
                autonomy === a.value
                  ? "border-blue-500 bg-blue-50"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >
              <div className="text-sm font-medium text-slate-800">{a.label}</div>
              <div className="text-xs text-slate-500 mt-0.5">{a.desc}</div>
            </button>
          ))}
        </div>
      </section>

      {/* ── Section 5: Pedagogical Preferences ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">
          5. Pedagogical Preferences
        </h2>
        <div className="space-y-3">
          {([
            ["socratic_method", "Socratic Method", "AI asks guiding questions rather than giving answers"],
            ["memorization_valued", "Memorization Valued", "Drills, repetition, and recitation are positive tools"],
            ["standardized_testing", "Standardized Testing", "Content aligns with state standards and test formats"],
            ["competitive_grading", "Competitive Grading", "Scores and rankings are shown to the child"],
            ["collaborative_learning", "Collaborative Learning", "AI encourages group and sibling activities"],
          ] as const).map(([key, label, desc]) => (
            <label key={key} className="flex items-start gap-3 cursor-pointer">
              <input type="checkbox" checked={(prefs as any)[key]}
                onChange={(e) => setPrefs({ ...prefs, [key]: e.target.checked })}
                className="mt-0.5 rounded" />
              <div>
                <div className="text-sm text-slate-800">{label}</div>
                <div className="text-xs text-slate-500">{desc}</div>
              </div>
            </label>
          ))}
        </div>
      </section>

      {/* ── Section 6: Custom Constraints ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4">
          6. Custom Constraints
        </h2>
        <div className="space-y-2">
          {customs.map((c, i) => (
            <div key={i} className="flex gap-2">
              <input type="text" value={c}
                onChange={(e) => { const next = [...customs]; next[i] = e.target.value; setCustoms(next); }}
                placeholder="e.g. All history content should include primary sources"
                className="flex-1 px-3 py-2 text-sm border border-slate-200 rounded-lg" />
              <button onClick={() => setCustoms(customs.filter((_, j) => j !== i))}
                className="text-xs text-red-500 hover:text-red-700 px-2">Remove</button>
            </div>
          ))}
        </div>
        <button onClick={() => setCustoms([...customs, ""])}
          className="mt-2 px-3 py-1.5 text-xs font-medium text-blue-600 border border-blue-300 rounded-lg hover:bg-blue-50">
          + Add Constraint
        </button>
      </section>

      {/* ── Save ── */}
      <div className="border-t border-slate-200 pt-6">
        <button onClick={save} disabled={saving}
          className="px-8 py-3 text-sm font-semibold bg-slate-800 text-white rounded-lg hover:bg-slate-900 disabled:opacity-50 transition-colors">
          {saving ? "Saving..." : "Save Philosophy"}
        </button>
        {saved && (
          <p className="text-sm text-green-600 mt-3">
            Philosophy updated. These constraints are now active across all AI interactions.
          </p>
        )}
      </div>
    </div>
  );
}
