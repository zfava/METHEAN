"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, curriculum, type MapState } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";

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

  if (!selectedChild) return <div className="text-sm text-slate-500">Select a child from the sidebar.</div>;

  return (
    <div className="max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          {buildPath && (
            <button onClick={resetBuild} className="text-slate-400 hover:text-slate-600">&larr;</button>
          )}
          <h1 className="text-xl font-semibold text-slate-800">Curriculum</h1>
        </div>
        <div className="flex gap-2">
          <button onClick={() => { setTab("my"); resetBuild(); }}
            className={`px-4 py-1.5 text-sm rounded-lg ${tab === "my" ? "bg-slate-800 text-white" : "bg-slate-100 text-slate-600"}`}>My Curriculum</button>
          <button onClick={() => setTab("build")}
            className={`px-4 py-1.5 text-sm rounded-lg ${tab === "build" ? "bg-slate-800 text-white" : "bg-slate-100 text-slate-600"}`}>Build New</button>
        </div>
      </div>

      {/* ── MY CURRICULUM ── */}
      {tab === "my" && (
        loading ? <LoadingSkeleton variant="card" count={3} /> : (
          maps.length === 0 ? (
            <div className="bg-white rounded-lg border border-slate-200 p-12 text-center">
              <p className="text-sm text-slate-500">No curriculum yet. Switch to &quot;Build New&quot; to get started.</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {maps.map((ms) => (
                <div key={ms.learning_map_id} className="bg-white rounded-lg border border-slate-200 p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-slate-800">{ms.map_name}</span>
                    <a href={`/curriculum/editor?map_id=${ms.learning_map_id}`}
                      className="text-xs text-blue-600 hover:underline">Edit</a>
                  </div>
                  <div className="flex items-center gap-2 mb-1">
                    <div className="flex-1 bg-slate-100 rounded-full h-1.5">
                      <div className="bg-green-500 h-1.5 rounded-full" style={{ width: `${Math.round(ms.progress_pct * 100)}%` }} />
                    </div>
                    <span className="text-xs text-slate-500">{Math.round(ms.progress_pct * 100)}%</span>
                  </div>
                  <span className="text-xs text-slate-400">{ms.nodes.length} nodes</span>
                </div>
              ))}
            </div>
          )
        )
      )}

      {/* ── BUILD: PATH SELECTOR ── */}
      {tab === "build" && !buildPath && (
        <div className="grid grid-cols-3 gap-4">
          <button onClick={() => setBuildPath("philosophy")}
            className="text-left bg-white rounded-lg border border-slate-200 p-5 hover:border-blue-400 transition-colors">
            <div className="text-sm font-semibold text-slate-800 mb-1">Build from Philosophy</div>
            <p className="text-xs text-slate-500">AI generates curriculum based on your educational profile</p>
          </button>
          <button onClick={() => setBuildPath("existing")}
            className="text-left bg-white rounded-lg border border-slate-200 p-5 hover:border-blue-400 transition-colors">
            <div className="text-sm font-semibold text-slate-800 mb-1">Map Existing Materials</div>
            <p className="text-xs text-slate-500">Import Saxon Math, Story of the World, etc.</p>
          </button>
          <button onClick={loadTemplates}
            className="text-left bg-white rounded-lg border border-slate-200 p-5 hover:border-blue-400 transition-colors">
            <div className="text-sm font-semibold text-slate-800 mb-1">Start from Template</div>
            <p className="text-xs text-slate-500">Use a pre-built starter curriculum</p>
          </button>
        </div>
      )}

      {/* ── BUILD: PHILOSOPHY — Step 1: Subject Selection ── */}
      {tab === "build" && buildPath === "philosophy" && !selectedSubject && !proposal && !approved && (
        <div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 mb-6 text-sm text-blue-800">
            Generating for: <strong className="capitalize">{philosophyLabel}</strong> approach, <strong>{selectedChild.first_name}</strong> ({selectedChild.grade_level || "K"})
          </div>
          <h2 className="text-sm font-semibold text-slate-800 mb-3">Choose a subject to build</h2>
          <div className="grid grid-cols-2 gap-3">
            {subjects.map((subj) => (
              <button key={subj.s} onClick={() => setSelectedSubject(subj)}
                className="text-left bg-white rounded-lg border border-slate-200 p-4 hover:border-blue-400 transition-colors">
                <div className="text-sm font-medium text-slate-800">{subj.s}</div>
                <p className="text-xs text-slate-500 mt-1">{subj.d}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── BUILD: PHILOSOPHY — Step 2: Scope Customization ── */}
      {tab === "build" && buildPath === "philosophy" && selectedSubject && !generating && !proposal && !approved && (
        <div className="bg-white rounded-lg border border-slate-200 p-6 max-w-2xl">
          <h2 className="text-sm font-semibold text-slate-800 mb-1">{selectedSubject.s}</h2>
          <p className="text-xs text-slate-500 mb-4">{selectedSubject.d}</p>
          <textarea value={scopeNotes} onChange={(e) => setScopeNotes(e.target.value)}
            placeholder="Optional: customize the scope (e.g., 'Focus on fractions this semester', 'Include Latin roots')"
            className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg h-24 resize-none mb-4" />
          <div className="flex gap-2">
            <button onClick={generateFromPhilosophy}
              className="px-6 py-2 text-sm font-medium bg-slate-800 text-white rounded-lg hover:bg-slate-900">
              Generate Curriculum
            </button>
            <button onClick={() => setSelectedSubject(null)}
              className="px-4 py-2 text-xs text-slate-500 hover:text-slate-700">Back</button>
          </div>
        </div>
      )}

      {/* ── BUILD: PHILOSOPHY — Generating indicator ── */}
      {tab === "build" && buildPath === "philosophy" && generating && !proposal && (
        <div className="bg-white rounded-lg border border-slate-200 p-12 text-center">
          <div className="text-lg mb-2 text-slate-300 animate-pulse">&#9881;</div>
          <p className="text-sm text-slate-600">Building your {selectedSubject?.s} curriculum based on your {philosophyLabel} approach...</p>
        </div>
      )}

      {/* ── BUILD: EXISTING MATERIALS ── */}
      {tab === "build" && buildPath === "existing" && !proposal && (
        <div className="bg-white rounded-lg border border-slate-200 p-6 max-w-2xl">
          <h2 className="text-sm font-semibold text-slate-800 mb-4">Map Your Existing Curriculum</h2>
          <div className="space-y-3">
            <input value={materialName} onChange={(e) => setMaterialName(e.target.value)}
              placeholder="Material name (e.g., Saxon Math 5/4)" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg" />
            <textarea value={materialDesc} onChange={(e) => setMaterialDesc(e.target.value)}
              placeholder="Brief description" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg h-16 resize-none" />
            <textarea value={toc} onChange={(e) => setToc(e.target.value)}
              placeholder="Paste your table of contents, chapter list, or unit list..." className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg h-32 resize-none" />
            <input value={position} onChange={(e) => setPosition(e.target.value)}
              placeholder="Current position (e.g., Chapter 14, Lesson 47)" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg" />
            <input value={subjectArea} onChange={(e) => setSubjectArea(e.target.value)}
              placeholder="Subject area (e.g., Mathematics)" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg" />
            <button onClick={mapExisting} disabled={generating || !materialName || !toc || !subjectArea}
              className="px-6 py-2 text-sm font-medium bg-slate-800 text-white rounded-lg hover:bg-slate-900 disabled:opacity-50">
              {generating ? "Mapping..." : "Map My Curriculum"}
            </button>
          </div>
        </div>
      )}

      {/* ── BUILD: TEMPLATE ── */}
      {tab === "build" && buildPath === "template" && (
        <div className="space-y-3">
          {templates.map((t) => (
            <div key={t.template_id} className="bg-white rounded-lg border border-slate-200 p-4 flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-slate-800">{t.name}</div>
                <p className="text-xs text-slate-500">{t.description} &middot; {t.node_count} nodes</p>
              </div>
              <button onClick={() => copyTemplate(t.template_id)} disabled={generating}
                className="px-4 py-1.5 text-xs font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
                {generating ? "..." : "Use Template"}
              </button>
            </div>
          ))}
        </div>
      )}

      {/* ── PROPOSAL REVIEW (shared by philosophy and existing paths) ── */}
      {proposal && !approved && (
        <div className="bg-white rounded-lg border border-slate-200 p-6 mt-4">
          <div className="bg-green-50 border border-green-200 rounded-lg px-4 py-2 mb-4 text-sm text-green-800">
            Curriculum generated! Review the proposal below.
          </div>
          <h2 className="text-sm font-semibold text-slate-800 mb-2">
            {proposal.source_material || proposal.material_name}
          </h2>
          <p className="text-xs text-slate-500 mb-4">{proposal.nodes?.length || 0} nodes &middot; {proposal.edges?.length || 0} edges</p>

          {/* Node preview */}
          <div className="space-y-1 mb-4 max-h-64 overflow-y-auto">
            {(proposal.nodes || []).map((n: any, i: number) => (
              <div key={i} className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded">
                <span className="text-[9px] font-bold uppercase text-slate-500 w-16">{n.node_type}</span>
                <span className="text-xs text-slate-700">{n.title}</span>
                {n.description && <span className="text-[10px] text-slate-400 truncate">{n.description}</span>}
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <button onClick={approveProposal} disabled={generating}
              className="px-5 py-2 text-sm font-medium bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50">
              {generating ? "Creating..." : "Approve & Create Map"}
            </button>
            <button onClick={() => { setProposal(null); setSelectedSubject(null); }}
              className="px-4 py-2 text-xs text-slate-500 border border-slate-300 rounded-lg hover:bg-slate-50">Regenerate</button>
            <button onClick={resetBuild}
              className="px-4 py-2 text-xs text-slate-400 hover:text-slate-600">Cancel</button>
          </div>
        </div>
      )}

      {/* ── CONFIRMATION ── */}
      {approved && (
        <div className="bg-white rounded-lg border border-slate-200 p-8 text-center mt-4">
          <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-green-100 flex items-center justify-center">
            <span className="text-green-600 text-xl">&#10003;</span>
          </div>
          <h2 className="text-sm font-semibold text-slate-800 mb-1">Curriculum Created!</h2>
          <p className="text-xs text-slate-500 mb-4">
            {proposal?.material_name || selectedSubject?.s || "Your curriculum"} with {proposal?.nodes?.length || 0} nodes is now active for {selectedChild.first_name}.
          </p>
          <div className="flex gap-2 justify-center">
            <a href="/maps" className="px-5 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700">View Map</a>
            <button onClick={() => { resetBuild(); setApproved(false); }}
              className="px-4 py-2 text-xs text-slate-500 border border-slate-300 rounded-lg hover:bg-slate-50">Build Another</button>
          </div>
        </div>
      )}
    </div>
  );
}
