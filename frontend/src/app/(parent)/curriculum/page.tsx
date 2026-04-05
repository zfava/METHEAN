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

export default function CurriculumPage() {
  const { selectedChild } = useChild();
  const [tab, setTab] = useState<"my" | "build">("my");
  const [maps, setMaps] = useState<MapState[]>([]);
  const [loading, setLoading] = useState(true);

  // Build state
  const [buildPath, setBuildPath] = useState<"philosophy" | "existing" | "template" | null>(null);
  const [templates, setTemplates] = useState<{ template_id: string; name: string; description: string; node_count: number }[]>([]);
  const [generating, setGenerating] = useState(false);
  const [materialName, setMaterialName] = useState("");
  const [materialDesc, setMaterialDesc] = useState("");
  const [toc, setToc] = useState("");
  const [position, setPosition] = useState("");
  const [subjectArea, setSubjectArea] = useState("");
  const [proposal, setProposal] = useState<any>(null);

  useEffect(() => { if (selectedChild) loadMaps(); }, [selectedChild]);

  async function loadMaps() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      setMaps(await childrenApi.allMapState(selectedChild.id));
    } catch {} finally { setLoading(false); }
  }

  async function loadTemplates() {
    setTemplates(await curriculum.templates());
    setBuildPath("template");
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

  async function copyTemplate(tid: string) {
    setGenerating(true);
    try {
      await curriculum.copyTemplate(tid);
      setBuildPath(null);
      setTab("my");
      await loadMaps();
    } catch {} finally { setGenerating(false); }
  }

  if (!selectedChild) return <div className="text-sm text-slate-500">Select a child from the sidebar.</div>;

  return (
    <div className="max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold text-slate-800">Curriculum</h1>
        <div className="flex gap-2">
          <button onClick={() => { setTab("my"); setBuildPath(null); }}
            className={`px-4 py-1.5 text-sm rounded-lg ${tab === "my" ? "bg-slate-800 text-white" : "bg-slate-100 text-slate-600"}`}>My Curriculum</button>
          <button onClick={() => setTab("build")}
            className={`px-4 py-1.5 text-sm rounded-lg ${tab === "build" ? "bg-slate-800 text-white" : "bg-slate-100 text-slate-600"}`}>Build New</button>
        </div>
      </div>

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

      {proposal && (
        <div className="bg-white rounded-lg border border-slate-200 p-6 mt-4">
          <h2 className="text-sm font-semibold text-slate-800 mb-2">Curriculum Proposal</h2>
          <p className="text-xs text-slate-500 mb-4">{proposal.source_material || proposal.material_name} &middot; {proposal.nodes?.length || 0} nodes</p>
          <div className="flex gap-2">
            <button onClick={() => setProposal(null)} className="px-4 py-1.5 text-xs text-slate-600 border border-slate-300 rounded-lg">Dismiss</button>
          </div>
        </div>
      )}
    </div>
  );
}
