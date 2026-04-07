"use client";

import { useEffect, useState } from "react";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import LoadingSkeleton from "@/components/LoadingSkeleton";

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

  if (loading) return <div className="max-w-3xl"><PageHeader title="Educational Philosophy" /><LoadingSkeleton variant="card" count={3} /></div>;

  return (
    <div className="max-w-3xl">
      <PageHeader
        title="Educational Philosophy"
        subtitle="Your family's foundational principles. These guide every AI recommendation."
      />

      {/* ── Section 1: Educational Approach ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-4">
          1. Educational Approach
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {PHILOSOPHIES.map((p) => (
            <Card key={p.value} onClick={() => setPhilosophy(p.value)} padding="p-3.5"
              selected={philosophy === p.value}
              className={philosophy !== p.value ? "hover:border-(--color-border-strong)" : ""}
            >
              <div className="text-sm font-medium text-(--color-text)">{p.label}</div>
              <div className="text-xs text-(--color-text-secondary) mt-0.5">{p.desc}</div>
            </Card>
          ))}
        </div>
        <textarea
          value={philosophyDesc} onChange={(e) => setPhilosophyDesc(e.target.value)}
          placeholder="Describe your approach in your own words (optional)"
          className="w-full mt-3 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] resize-none h-20 focus:outline-none focus:ring-1 focus:ring-(--color-accent) bg-(--color-surface) text-(--color-text)"
        />
      </section>

      {/* ── Section 2: Faith & Worldview ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-4">
          2. Faith &amp; Worldview
        </h2>
        <div className="flex flex-wrap gap-2 mb-3">
          {RELIGIONS.map((r) => (
            <Card key={r.value} onClick={() => setReligion(r.value)} padding="px-4 py-2"
              selected={religion === r.value}
              className={religion !== r.value ? "hover:border-(--color-border-strong)" : ""}
            >
              <span className={`text-sm ${religion === r.value ? "font-medium" : ""} text-(--color-text)`}>{r.label}</span>
            </Card>
          ))}
        </div>
        <textarea
          value={religionNotes} onChange={(e) => setReligionNotes(e.target.value)}
          placeholder="Any specifics (denomination, traditions, etc.)"
          className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] resize-none h-16 focus:outline-none focus:ring-1 focus:ring-(--color-accent) bg-(--color-surface) text-(--color-text)"
        />
        <p className="text-xs text-(--color-text-tertiary) mt-1">This informs how the AI presents topics with worldview implications.</p>
      </section>

      {/* ── Section 3: Content Boundaries ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-4">
          3. Content Boundaries
        </h2>
        {boundaries.length === 0 && (
          <p className="text-xs text-(--color-text-tertiary) mb-3">No boundaries set. The AI will use its default judgment on all topics.</p>
        )}
        <div className="space-y-3">
          {boundaries.map((b, i) => (
            <Card key={i} padding="p-3">
              <div className="flex gap-2 mb-2">
                <input type="text" value={b.topic} onChange={(e) => updateBoundary(i, "topic", e.target.value)}
                  placeholder="Topic (e.g. evolution)" className="flex-1 px-2 py-1.5 text-sm border border-(--color-border) rounded-[6px] bg-(--color-surface) text-(--color-text)" />
                <select value={b.stance} onChange={(e) => updateBoundary(i, "stance", e.target.value)}
                  className="px-2 py-1.5 text-sm border border-(--color-border) rounded-[6px] bg-(--color-surface) text-(--color-text)">
                  {STANCES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
                <button onClick={() => removeBoundary(i)} className="text-xs text-(--color-danger) hover:opacity-80 px-2">Remove</button>
              </div>
              <input type="text" value={b.notes} onChange={(e) => updateBoundary(i, "notes", e.target.value)}
                placeholder="Notes (optional)" className="w-full px-2 py-1 text-xs border border-(--color-border)/50 rounded-[6px] mb-1 bg-(--color-surface) text-(--color-text)" />
              {b.topic && b.stance && (
                <p className="text-[11px] text-(--color-accent) italic">
                  {stancePreview[b.stance]?.(b.topic) || ""}
                </p>
              )}
            </Card>
          ))}
        </div>
        <Button variant="secondary" size="sm" className="mt-2 text-(--color-accent) border-(--color-accent)/30" onClick={addBoundary}>
          + Add Boundary
        </Button>
      </section>

      {/* ── Section 4: AI Autonomy ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-4">
          4. AI Autonomy Level
        </h2>
        <div className="space-y-2">
          {AUTONOMY_LEVELS.map((a) => (
            <Card key={a.value} onClick={() => setAutonomy(a.value)} padding="p-4"
              selected={autonomy === a.value}
              className={`w-full ${autonomy !== a.value ? "hover:border-(--color-border-strong)" : ""}`}
            >
              <div className="text-sm font-medium text-(--color-text)">{a.label}</div>
              <div className="text-xs text-(--color-text-secondary) mt-0.5">{a.desc}</div>
            </Card>
          ))}
        </div>
      </section>

      {/* ── Section 5: Pedagogical Preferences ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-4">
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
                <div className="text-sm text-(--color-text)">{label}</div>
                <div className="text-xs text-(--color-text-secondary)">{desc}</div>
              </div>
            </label>
          ))}
        </div>
      </section>

      {/* ── Section 6: Custom Constraints ── */}
      <section className="mb-10">
        <h2 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-4">
          6. Custom Constraints
        </h2>
        <div className="space-y-2">
          {customs.map((c, i) => (
            <div key={i} className="flex gap-2">
              <input type="text" value={c}
                onChange={(e) => { const next = [...customs]; next[i] = e.target.value; setCustoms(next); }}
                placeholder="e.g. All history content should include primary sources"
                className="flex-1 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
              <button onClick={() => setCustoms(customs.filter((_, j) => j !== i))}
                className="text-xs text-(--color-danger) hover:opacity-80 px-2">Remove</button>
            </div>
          ))}
        </div>
        <Button variant="secondary" size="sm" className="mt-2 text-(--color-accent) border-(--color-accent)/30" onClick={() => setCustoms([...customs, ""])}>
          + Add Constraint
        </Button>
      </section>

      {/* ── Save ── */}
      <div className="border-t border-(--color-border) pt-6">
        <Button variant="primary" size="lg" onClick={save} disabled={saving}
          className="bg-(--color-text) hover:opacity-90 px-8 py-3">
          {saving ? "Saving..." : "Save Philosophy"}
        </Button>
        {saved && (
          <p className="text-sm text-(--color-success) mt-3">
            Philosophy updated. These constraints are now active across all AI interactions.
          </p>
        )}
      </div>
    </div>
  );
}
