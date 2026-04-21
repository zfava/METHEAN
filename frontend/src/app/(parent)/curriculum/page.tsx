"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, curriculum, annualCurriculum, household, type MapState } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import SubjectLevelPicker from "@/components/SubjectLevelPicker";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Tabs from "@/components/ui/Tabs";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

export default function CurriculumPage() {
  useEffect(() => { document.title = "Curriculum | METHEAN"; }, []);
  const { toast } = useToast();

  const { selectedChild } = useChild();
  const [tab, setTab] = useState<"my" | "build">("my");
  const [maps, setMaps] = useState<MapState[]>([]);
  const [curricula, setCurricula] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [subjectLevels, setSubjectLevels] = useState<Record<string, string>>({});

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
      household.getPhilosophy().catch(() => ({}))
        .then((p: any) => {
          const phil = p.educational_philosophy?.replace(/_/g, " ") || "Eclectic";
          setPhilosophyLabel(phil);
        })
        .catch(() => {});

      // Set subjects based on grade
      // Default subjects (user can change via SubjectLevelPicker)
      setSubjects([
        { s: "Phonics & Reading", d: "" }, { s: "Mathematics", d: "" },
        { s: "Science", d: "" }, { s: "History", d: "" },
      ]);
    }
  }, [buildPath, selectedChild]);

  async function loadMaps() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      const [mapData, curricData] = await Promise.all([
        childrenApi.allMapState(selectedChild.id),
        annualCurriculum.list(selectedChild.id),
      ]);
      setMaps(mapData);
      setCurricula(curricData);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load curriculum data.");
    } finally { setLoading(false); }
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
      const year = new Date().getFullYear();
      const result = await annualCurriculum.generate(selectedChild.id, {
        subject_name: selectedSubject.s,
        academic_year: `${year}-${year + 1}`,
        hours_per_week: 4,
        total_weeks: 36,
        scope_notes: scopeNotes || undefined,
      });
      setProposal(result);
      toast("Curriculum generated", "success");
    } catch (err: any) {
      toast(err.detail || "Failed to generate curriculum", "error");
    } finally { setGenerating(false); }
  }

  async function mapExisting() {
    if (!selectedChild || !materialName || !toc || !subjectArea) return;
    setGenerating(true);
    try {
      const result = await curriculum.mapExisting(selectedChild.id, {
        material_name: materialName, material_description: materialDesc,
        table_of_contents: toc, current_position: position, subject_area: subjectArea,
      });
      setProposal(result);
    } catch (err: any) { setError(err?.detail || err?.message || "Something went wrong."); } finally { setGenerating(false); }
  }

  async function approveProposal() {
    if (!proposal?.id) return;
    setGenerating(true);
    try {
      await annualCurriculum.approve(proposal.id);
      setApproved(true);
      toast("Curriculum approved", "success");
      await loadMaps();
    } catch (err: any) { toast(err?.detail || "Something went wrong", "error"); setError(err?.detail || err?.message || "Something went wrong."); } finally { setGenerating(false); }
  }

  async function copyTemplate(tid: string) {
    setGenerating(true);
    try {
      await curriculum.copyTemplate(tid);
      toast("Template applied", "success");
      resetBuild();
      setTab("my");
      await loadMaps();
    } catch (err: any) { toast(err?.detail || "Something went wrong", "error"); setError(err?.detail || err?.message || "Something went wrong."); } finally { setGenerating(false); }
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

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); loadMaps(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── MY CURRICULUM ── */}
      {tab === "my" && (
        loading ? <LoadingSkeleton variant="card" count={3} /> : (
          curricula.length === 0 && maps.length === 0 ? (
            <EmptyState
              icon="empty"
              title="No curriculum yet"
              description='Switch to "Build New" to get started.'
            />
          ) : (
            <div className="space-y-6">
              {/* Annual Curricula (primary) */}
              {curricula.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider mb-3">Annual Curricula</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {curricula.map((c: any) => (
                      <Card key={c.id} href={`/curriculum/year?id=${c.id}`} padding="p-4">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium text-(--color-text)">{c.subject_name}</span>
                          <StatusBadge status={c.status} />
                        </div>
                        <div className="text-xs text-(--color-text-secondary) mb-2">{c.academic_year} · {c.grade_level || ""}</div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-(--color-text-tertiary)">{c.total_weeks} weeks · {c.hours_per_week}h/week</span>
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {/* Learning Maps (secondary) */}
              {maps.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider mb-3">Learning Maps</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {maps.map((ms) => (
                      <Card key={ms.learning_map_id} href={`/curriculum/editor?map_id=${ms.learning_map_id}`} padding="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-(--color-text)">{ms.map_name}</span>
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
                </div>
              )}
            </div>
          )
        )
      )}

      {/* ── BUILD: PATH SELECTOR ── */}
      {tab === "build" && !buildPath && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
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
          <div className="bg-(--color-accent-light) border border-(--color-accent)/30 rounded-[14px] px-4 py-3 mb-6 text-sm text-(--color-accent)">
            Generating for: <strong className="capitalize">{philosophyLabel}</strong> approach, <strong>{selectedChild.first_name}</strong>
          </div>
          <h3 className="text-sm font-medium mb-2">Select subjects</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">All subjects available regardless of age.</p>
          <SubjectLevelPicker
            selected={subjectLevels}
            onChange={(levels) => {
              setSubjectLevels(levels);
              setSubjects(Object.keys(levels).map(id => ({
                s: id.replace(/_/g, " ").replace(/\b\w/g, (c: string) => c.toUpperCase()), d: "",
              })));
            }}
            showCustom={true}
          />
          {Object.keys(subjectLevels).length > 0 && (
            <div className="mt-4">
              <p className="text-xs text-(--color-text-secondary) mb-2">Now select which subject to build:</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {subjects.map((subj) => (
                  <Card key={subj.s} onClick={() => setSelectedSubject(subj)} padding="p-3" className="text-left">
                    <div className="text-sm font-medium">{subj.s}</div>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── BUILD: PHILOSOPHY — Step 2: Scope Customization ── */}
      {tab === "build" && buildPath === "philosophy" && selectedSubject && !generating && !proposal && !approved && (
        <Card padding="p-6" className="max-w-2xl">
          <h2 className="text-sm font-semibold text-(--color-text) mb-1">{selectedSubject.s}</h2>
          <p className="text-xs text-(--color-text-secondary) mb-4">{selectedSubject.d}</p>
          <textarea value={scopeNotes} onChange={(e) => setScopeNotes(e.target.value)}
            placeholder="Optional: customize the scope (e.g., 'Focus on fractions this semester', 'Include Latin roots')"
            className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] h-24 resize-none mb-4" />
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
              placeholder="Material name (e.g., Saxon Math 5/4)" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px]" />
            <textarea value={materialDesc} onChange={(e) => setMaterialDesc(e.target.value)}
              placeholder="Brief description" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] h-16 resize-none" />
            <textarea value={toc} onChange={(e) => setToc(e.target.value)}
              placeholder="Paste your table of contents, chapter list, or unit list..." className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] h-32 resize-none" />
            <input value={position} onChange={(e) => setPosition(e.target.value)}
              placeholder="Current position (e.g., Chapter 14, Lesson 47)" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px]" />
            <input value={subjectArea} onChange={(e) => setSubjectArea(e.target.value)}
              placeholder="Subject area (e.g., Mathematics)" className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px]" />
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
          <div className="bg-(--color-success-light) border border-(--color-success)/30 rounded-[10px] px-4 py-2 mb-4 text-sm text-(--color-success)">
            {proposal.id ? "Annual curriculum generated! Review and approve to create all 36 weeks." : "Curriculum generated! Review the proposal below."}
          </div>
          <h2 className="text-sm font-semibold text-(--color-text) mb-2">
            {proposal.subject || proposal.source_material || proposal.material_name || selectedSubject?.s}
          </h2>
          <p className="text-xs text-(--color-text-secondary) mb-4">
            {proposal.id
              ? `Status: ${proposal.status} · Approving will create a full year of activities.`
              : `${proposal.nodes?.length || 0} nodes · ${proposal.edges?.length || 0} edges`}
          </p>

          {/* Node preview for map proposals */}
          {proposal.nodes && (
            <div className="space-y-1 mb-4 max-h-64 overflow-y-auto">
              {(proposal.nodes || []).map((n: any, i: number) => (
                <div key={i} className="flex items-center gap-2 px-3 py-1.5 bg-(--color-page) rounded-[10px]">
                  <span className="text-[9px] font-bold uppercase text-(--color-text-secondary) w-16">{n.node_type}</span>
                  <span className="text-xs text-(--color-text)">{n.title}</span>
                </div>
              ))}
            </div>
          )}

          <div className="flex gap-2">
            <Button onClick={approveProposal} disabled={generating} variant="success" size="lg">
              {generating ? "Creating..." : proposal.id ? "Approve & Create Year Plan" : "Approve & Create Map"}
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
            {proposal?.id ? (
              <a href={`/curriculum/year?id=${proposal.id}`} className="px-5 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-[10px] hover:bg-(--color-accent-hover)">View Year Plan</a>
            ) : (
              <a href="/maps" className="px-5 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-[10px] hover:bg-(--color-accent-hover)">View Map</a>
            )}
            <Button onClick={() => { resetBuild(); setApproved(false); }} variant="secondary" size="sm">
              Build Another
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
