"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, curriculum, type MapState } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Tabs from "@/components/ui/Tabs";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

// Classical subjects by grade band (fallback if library endpoint unavailable)
const CLASSICAL_SUBJECTS: Record<string, { s: string; d: string }[]> = {
  "K-2": [
    { s: "Phonics & Reading", d: "Systematic phonics through reading fluency" },
    { s: "Mathematics", d: "Number sense through basic operations" },
    { s: "Handwriting & Copywork", d: "Letter formation, penmanship, copywork from quality literature" },
    { s: "History & Bible", d: "Ancient civilizations and Scripture narratives" },
    { s: "Nature Study", d: "Seasonal observation, nature journaling" },
    { s: "Music & Art", d: "Hymn singing, folk songs, drawing fundamentals" },
  ],
  "3-5": [
    { s: "Literature", d: "Classic children's literature and mythology" },
    { s: "Mathematics", d: "Multiplication through fractions" },
    { s: "Writing & Grammar", d: "Paragraph construction, dictation, grammar" },
    { s: "History", d: "Ancients through Renaissance with primary sources" },
    { s: "Science", d: "Life, earth, and physical sciences with experiments" },
    { s: "Latin", d: "Systematic grammar and vocabulary" },
  ],
  "6-8": [
    { s: "Literature & Composition", d: "Great books, essay writing, rhetoric foundations" },
    { s: "Mathematics", d: "Pre-algebra through algebra" },
    { s: "Logic", d: "Formal logic, syllogisms, argument analysis" },
    { s: "History", d: "World and American history with historiography" },
    { s: "Science", d: "Biology, chemistry foundations, scientific method" },
    { s: "Latin", d: "Reading and translation" },
  ],
  "9-12": [
    { s: "Literature", d: "Great books seminar, literary analysis" },
    { s: "Mathematics", d: "Algebra II, Geometry, Precalculus" },
    { s: "Rhetoric & Composition", d: "Persuasive writing, public speaking" },
    { s: "History & Government", d: "American government, economics, worldview studies" },
    { s: "Science", d: "Biology, Chemistry, Physics" },
    { s: "Theology & Philosophy", d: "Systematic theology, philosophical foundations" },
  ],
};

function gradeToRange(grade: string | null): string {
  if (!grade) return "K-2";
  const g = grade.toLowerCase();
  if (g.includes("k") || g.includes("1") || g.includes("2")) return "K-2";
  if (g.includes("3") || g.includes("4") || g.includes("5")) return "3-5";
  if (g.includes("6") || g.includes("7") || g.includes("8")) return "6-8";
  return "9-12";
}

export default function CurriculumPage() {
  const { selectedChild } = useChild();
  const [tab, setTab] = useState<"my" | "build">("my");
  const [maps, setMaps] = useState<MapState[]>([]);
  const [loading, setLoading] = useState(true);

  // Build state (shared)
  const [buildPath, setBuildPath] = useState<"philosophy" | "existing" | "template" | null>(null);
  const [templates, setTemplates] = useState<{ template_id: string; name: string; description: string; node_count: number }[]>([]);
  const [generating, setGenerating] = useState(false);
  const [proposal, setProposal] = useState<any>(null);

  // Existing materials state
  const [materialName, setMaterialName] = useState("");
  const [materialDesc, setMaterialDesc] = useState("");
  const [toc, setToc] = useState("");
  const [position, setPosition] = useState("");
  const [subjectArea, setSubjectArea] = useState("");

  // Philosophy builder state
  const [philosophyLabel, setPhilosophyLabel] = useState("Eclectic");
  const [subjects, setSubjects] = useState<{ s: string; d: string }[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<{ s: string; d: string } | null>(null);
  const [scopeNotes, setScopeNotes] = useState("");
  const [approved, setApproved] = useState(false);

  useEffect(() => { if (selectedChild) loadMaps(); }, [selectedChild]);

  // Load philosophy data when entering philosophy path
  useEffect(() => {
    if (buildPath === "philosophy" && selectedChild) {
      fetch(`${API}/household/philosophy`, { credentials: "include" })
        .then((r) => r.ok ? r.json() : {})
        .then((p) => {
          const phil = p.educational_philosophy?.replace(/_/g, " ") || "Eclectic";
          setPhilosophyLabel(phil);
        })
        .catch(() => {});

      // Set subjects based on grade
      const range = gradeToRange(selectedChild.grade_level);
      setSubjects(CLASSICAL_SUBJECTS[range] || CLASSICAL_SUBJECTS["K-2"]);
    }
  }, [buildPath, selectedChild]);

  async function loadMaps() {
    if (!selectedChild) return;
    setLoading(true);
    try { setMaps(await childrenApi.allMapState(selectedChild.id)); }
    catch {} finally { setLoading(false); }
  }

  async function loadTemplates() {
    setTemplates(await curriculum.templates());
    setBuildPath("template");
  }

  function resetBuild() {
    setBuildPath(null);
    setProposal(null);
    setSelectedSubject(null);
    setScopeNotes("");
    setApproved(false);
    setMaterialName(""); setMaterialDesc(""); setToc(""); setPosition(""); setSubjectArea("");
  }

  async function generateFromPhilosophy() {
    if (!selectedChild || !selectedSubject) return;
    setGenerating(true);
    try {
      const csrf = getCsrf();
      // Use map-existing as the backend endpoint, with subject as material
      const resp = await fetch(`${API}/children/${selectedChild.id}/curriculum/map-existing`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify({
          material_name: selectedSubject.s,
          material_description: selectedSubject.d + (scopeNotes ? `\n\nParent notes: ${scopeNotes}` : ""),
          table_of_contents: `Subject: ${selectedSubject.s}\nGrade: ${selectedChild.grade_level || "K"}\nApproach: ${philosophyLabel}\nScope: ${selectedSubject.d}`,
          current_position: "Beginning of course",
          subject_area: selectedSubject.s,
        }),
      });
      if (resp.ok) setProposal(await resp.json());
    } catch {} finally { setGenerating(false); }
  }

  async function mapExisting() {
    if (!selectedChild || !materialName || !toc || !subjectArea) return;
    setGenerating(true);
    try {
      const csrf = getCsrf();
      const resp = await fetch(`${API}/children/${selectedChild.id}/curriculum/map-existing`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify({ material_name: materialName, material_description: materialDesc,
          table_of_contents: toc, current_position: position, subject_area: subjectArea }),
      });
      if (resp.ok) setProposal(await resp.json());
    } catch {} finally { setGenerating(false); }
  }

  async function approveProposal() {
    if (!selectedChild || !proposal) return;
    setGenerating(true);
    try {
      const csrf = getCsrf();
      await fetch(`${API}/children/${selectedChild.id}/curriculum/apply-mapping`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify(proposal),
      });
      setApproved(true);
      await loadMaps();
    } catch {} finally { setGenerating(false); }
  }

  async function copyTemplate(tid: string) {
    setGenerating(true);
    try {
      await curriculum.copyTemplate(tid);
      resetBuild();
      setTab("my");
      await loadMaps();
    } catch {} finally { setGenerating(false); }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;

  return (
    <div className="max-w-5xl">
      <PageHeader
        title="Curriculum"
        actions={
          <Tabs
            tabs={[
              { key: "my" as const, label: "My Curriculum" },
              { key: "build" as const, label: "Build New" },
            ]}
            active={tab}
            onChange={(key) => { if (key === "my") { setTab("my"); resetBuild(); } else { setTab("build"); } }}
          />
        }
        className={buildPath ? undefined : "mb-6"}
      />

      {buildPath && (
        <div className="mb-4">
          <button onClick={resetBuild} className="text-(--color-text-secondary) hover:text-(--color-text) text-sm">&larr; Back</button>
        </div>
      )}

      {/* ── MY CURRICULUM ── */}
      {tab === "my" && (
        loading ? <LoadingSkeleton variant="card" count={3} /> : (
          maps.length === 0 ? (
            <EmptyState
              icon="empty"
              title="No curriculum yet"
              description='Switch to "Build New" to get started.'
            />
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {maps.map((ms) => (
                <Card key={ms.learning_map_id} padding="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-(--color-text)">{ms.map_name}</span>
                    <a href={`/curriculum/editor?map_id=${ms.learning_map_id}`}
                      className="text-xs text-(--color-accent) hover:underline">Edit</a>
                  </div>
                  <div className="flex items-center gap-2 mb-1">
                    <div className="flex-1 bg-(--color-page) rounded-full h-1.5">
                      <div className="bg-(--color-success) h-1.5 rounded-full" style={{ width: `${Math.round(ms.progress_pct * 100)}%` }} />
                    </div>
                    <span className="text-xs text-(--color-text-secondary)">{Math.round(ms.progress_pct * 100)}%</span>
                  </div>
                  <span className="text-xs text-(--color-text-secondary)">{ms.nodes.length} nodes</span>
                </Card>
              ))}
            </div>
          )
        )
      )}

      {/* ── BUILD: PATH SELECTOR ── */}
      {tab === "build" && !buildPath && (
        <div className="grid grid-cols-3 gap-4">
          <Card onClick={() => setBuildPath("philosophy")} padding="p-5" className="text-left hover:border-(--color-accent) transition-colors">
            <div className="text-sm font-semibold text-(--color-text) mb-1">Build from Philosophy</div>
            <p className="text-xs text-(--color-text-secondary)">AI generates curriculum based on your educational profile</p>
          </Card>
          <Card onClick={() => setBuildPath("existing")} padding="p-5" className="text-left hover:border-(--color-accent) transition-colors">
            <div className="text-sm font-semibold text-(--color-text) mb-1">Map Existing Materials</div>
            <p className="text-xs text-(--color-text-secondary)">Import Saxon Math, Story of the World, etc.</p>
          </Card>
          <Card onClick={loadTemplates} padding="p-5" className="text-left hover:border-(--color-accent) transition-colors">
            <div className="text-sm font-semibold text-(--color-text) mb-1">Start from Template</div>
            <p className="text-xs text-(--color-text-secondary)">Use a pre-built starter curriculum</p>
          </Card>
        </div>
      )}

      {/* ── BUILD: PHILOSOPHY — Step 1: Subject Selection ── */}
      {tab === "build" && buildPath === "philosophy" && !selectedSubject && !proposal && !approved && (
        <div>
          <div className="bg-(--color-accent-light) border border-(--color-accent)/30 rounded-[10px] px-4 py-3 mb-6 text-sm text-(--color-accent)">
            Generating for: <strong className="capitalize">{philosophyLabel}</strong> approach, <strong>{selectedChild.first_name}</strong> ({selectedChild.grade_level || "K"})
          </div>
          <h2 className="text-sm font-semibold text-(--color-text) mb-3">Choose a subject to build</h2>
          <div className="grid grid-cols-2 gap-3">
            {subjects.map((subj) => (
              <Card key={subj.s} onClick={() => setSelectedSubject(subj)} padding="p-4" className="text-left hover:border-(--color-accent) transition-colors">
                <div className="text-sm font-medium text-(--color-text)">{subj.s}</div>
                <p className="text-xs text-(--color-text-secondary) mt-1">{subj.d}</p>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* ── BUILD: PHILOSOPHY — Step 2: Scope Customization ── */}
      {tab === "build" && buildPath === "philosophy" && selectedSubject && !generating && !proposal && !approved && (
        <Card padding="p-6" className="max-w-2xl">
          <h2 className="text-sm font-semibold text-(--color-text) mb-1">{selectedSubject.s}</h2>
          <p className="text-xs text-(--color-text-secondary) mb-4">{selectedSubject.d}</p>
          <textarea value={scopeNotes} onChange={(e) => setScopeNotes(e.target.value)}
            placeholder="Optional: customize the scope (e.g., 'Focus on fractions this semester', 'Include Latin roots')"
            className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[6px] h-24 resize-none mb-4" />
          <div className="flex gap-2">
            <Button onClick={generateFromPhilosophy} size="lg">
              Generate Curriculum
            </Button>
            <Button onClick={() => setSelectedSubject(null)} variant="ghost" size="sm">Back</Button>
          </div>
        </Card>
      )}

      {/* ── BUILD: PHILOSOPHY — Generating indicator ── */}
      {tab === "build" && buildPath === "philosophy" && generating && !proposal && (
        <Card padding="p-12" className="text-center">
          <div className="text-lg mb-2 text-(--color-text-tertiary) animate-pulse">&#9881;</div>
          <p className="text-sm text-(--color-text-secondary)">Building your {selectedSubject?.s} curriculum based on your {philosophyLabel} approach...</p>
        </Card>
      )}

      {/* ── BUILD: EXISTING MATERIALS ── */}
      {tab === "build" && buildPath === "existing" && !proposal && (
        <Card padding="p-6" className="max-w-2xl">
          <h2 className="text-sm font-semibold text-(--color-text) mb-4">Map Your Existing Curriculum</h2>
          <div className="space-y-3">
            <input value={materialName} onChange={(e) => setMaterialName(e.target.value)}
              placeholder="Material name (e.g., Saxon Math 5/4)" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[6px]" />
            <textarea value={materialDesc} onChange={(e) => setMaterialDesc(e.target.value)}
              placeholder="Brief description" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[6px] h-16 resize-none" />
            <textarea value={toc} onChange={(e) => setToc(e.target.value)}
              placeholder="Paste your table of contents, chapter list, or unit list..." className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[6px] h-32 resize-none" />
            <input value={position} onChange={(e) => setPosition(e.target.value)}
              placeholder="Current position (e.g., Chapter 14, Lesson 47)" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[6px]" />
            <input value={subjectArea} onChange={(e) => setSubjectArea(e.target.value)}
              placeholder="Subject area (e.g., Mathematics)" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[6px]" />
            <Button onClick={mapExisting} disabled={generating || !materialName || !toc || !subjectArea} size="lg">
              {generating ? "Mapping..." : "Map My Curriculum"}
            </Button>
          </div>
        </Card>
      )}

      {/* ── BUILD: TEMPLATE ── */}
      {tab === "build" && buildPath === "template" && (
        <div className="space-y-3">
          {templates.map((t) => (
            <Card key={t.template_id} padding="p-4" className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-(--color-text)">{t.name}</div>
                <p className="text-xs text-(--color-text-secondary)">{t.description} &middot; {t.node_count} nodes</p>
              </div>
              <Button onClick={() => copyTemplate(t.template_id)} disabled={generating} size="sm">
                {generating ? "..." : "Use Template"}
              </Button>
            </Card>
          ))}
        </div>
      )}

      {/* ── PROPOSAL REVIEW (shared by philosophy and existing paths) ── */}
      {proposal && !approved && (
        <Card padding="p-6" className="mt-4">
          <div className="bg-(--color-success-light) border border-(--color-success)/30 rounded-[6px] px-4 py-2 mb-4 text-sm text-(--color-success)">
            Curriculum generated! Review the proposal below.
          </div>
          <h2 className="text-sm font-semibold text-(--color-text) mb-2">
            {proposal.source_material || proposal.material_name}
          </h2>
          <p className="text-xs text-(--color-text-secondary) mb-4">{proposal.nodes?.length || 0} nodes &middot; {proposal.edges?.length || 0} edges</p>

          {/* Node preview */}
          <div className="space-y-1 mb-4 max-h-64 overflow-y-auto">
            {(proposal.nodes || []).map((n: any, i: number) => (
              <div key={i} className="flex items-center gap-2 px-3 py-1.5 bg-(--color-page) rounded-[6px]">
                <span className="text-[9px] font-bold uppercase text-(--color-text-secondary) w-16">{n.node_type}</span>
                <span className="text-xs text-(--color-text)">{n.title}</span>
                {n.description && <span className="text-[10px] text-(--color-text-secondary) truncate">{n.description}</span>}
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <Button onClick={approveProposal} disabled={generating} variant="success" size="lg">
              {generating ? "Creating..." : "Approve & Create Map"}
            </Button>
            <Button onClick={() => { setProposal(null); setSelectedSubject(null); }} variant="secondary" size="sm">
              Regenerate
            </Button>
            <Button onClick={resetBuild} variant="ghost" size="sm">Cancel</Button>
          </div>
        </Card>
      )}

      {/* ── CONFIRMATION ── */}
      {approved && (
        <Card padding="p-8" className="text-center mt-4">
          <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-(--color-success-light) flex items-center justify-center">
            <span className="text-(--color-success) text-xl">&#10003;</span>
          </div>
          <h2 className="text-sm font-semibold text-(--color-text) mb-1">Curriculum Created!</h2>
          <p className="text-xs text-(--color-text-secondary) mb-4">
            {proposal?.material_name || selectedSubject?.s || "Your curriculum"} with {proposal?.nodes?.length || 0} nodes is now active for {selectedChild.first_name}.
          </p>
          <div className="flex gap-2 justify-center">
            <a href="/maps" className="px-5 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-[6px] hover:bg-(--color-accent-hover)">View Map</a>
            <Button onClick={() => { resetBuild(); setApproved(false); }} variant="secondary" size="sm">
              Build Another
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
