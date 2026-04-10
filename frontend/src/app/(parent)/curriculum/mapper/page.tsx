"use client";

import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "next/navigation";
import { curriculum, educationPlan, type MapNodeState } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import DagGraph from "@/components/DagGraph";
import { cn } from "@/lib/cn";

const SUBJECTS = [
  "Mathematics", "Reading", "Language Arts", "Writing", "Science",
  "History", "Social Studies", "Geography", "Latin", "Spanish",
  "French", "Art", "Music", "Physical Education", "Logic",
  "Bible / Religion", "Nature Study", "Handwriting", "Spelling", "Other",
];

const EXAMPLE_TOC = `Chapter 1: Addition Facts Review
Chapter 2: Subtraction Facts Review
Chapter 3: Place Value to Thousands
Chapter 4: Addition with Regrouping
Chapter 5: Subtraction with Borrowing
Chapter 6: Multiplication Concepts
Chapter 7: Multiplication Facts 0-5
Chapter 8: Multiplication Facts 6-9
Chapter 9: Division Concepts
Chapter 10: Fractions Introduction`;

export default function CurriculumMapperPage() {
  useEffect(() => { document.title = "Map Curriculum | METHEAN"; }, []);

  const params = useSearchParams();
  const paramSubject = params.get("subject") || "";
  const paramYear = params.get("year") || "";
  const paramChildId = params.get("child") || "";

  const { selectedChild } = useChild();
  const { toast } = useToast();

  const [step, setStep] = useState(1);
  const [error, setError] = useState("");

  // Step 1
  const [materialName, setMaterialName] = useState("");
  const [subjectArea, setSubjectArea] = useState(paramSubject);
  const [materialDesc, setMaterialDesc] = useState("");

  // Education plan awareness
  const [planMatch, setPlanMatch] = useState<string | null>(null); // year key if matched
  const [planExists, setPlanExists] = useState(false);

  // Step 2
  const [toc, setToc] = useState("");
  const [showExample, setShowExample] = useState(false);

  // Step 3
  const [currentPosition, setCurrentPosition] = useState("");

  // Step 4-5
  const [loading, setLoading] = useState(false);
  const [longWait, setLongWait] = useState(false);
  const [proposal, setProposal] = useState<any>(null);
  const [proposalNodes, setProposalNodes] = useState<Array<{
    id: string; title: string; type: string; mastered: boolean; included: boolean;
    prerequisite_ids: string[];
  }>>([]);
  const [editingIdx, setEditingIdx] = useState<number | null>(null);
  const longWaitTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;

  const childName = selectedChild.first_name;

  async function runMapping() {
    setLoading(true);
    setError("");
    setLongWait(false);
    setStep(4);

    longWaitTimer.current = setTimeout(() => setLongWait(true), 30000);

    try {
      const result = await curriculum.mapExisting(selectedChild!.id, {
        material_name: materialName,
        material_description: materialDesc || undefined,
        table_of_contents: toc,
        current_position: currentPosition || undefined,
        subject_area: subjectArea,
      });

      if (longWaitTimer.current) clearTimeout(longWaitTimer.current);

      setProposal(result);

      // Parse the result into editable nodes
      const nodes = (result.nodes || result.learning_map?.nodes || []).map((n: any, i: number) => ({
        id: n.id || n.node_id || `node_${i}`,
        title: n.title || `Node ${i + 1}`,
        type: n.node_type || "concept",
        mastered: n.mastery_level === "mastered" || n.is_mastered || false,
        included: true,
        prerequisite_ids: n.prerequisite_node_ids || n.prerequisites || [],
      }));

      if (nodes.length === 0) {
        setError("We couldn't identify a clear structure. Try pasting the table of contents more explicitly.");
        setStep(2);
        setLoading(false);
        return;
      }

      setProposalNodes(nodes);
      setStep(5);
    } catch (err: any) {
      if (longWaitTimer.current) clearTimeout(longWaitTimer.current);
      setError(err?.detail || err?.message || "Couldn't map your curriculum. Try again with more detail.");
      setStep(3);
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setStep(1);
    setMaterialName("");
    setSubjectArea("");
    setMaterialDesc("");
    setToc("");
    setCurrentPosition("");
    setProposal(null);
    setProposalNodes([]);
    setError("");
  }

  // Build DagGraph-compatible nodes from proposal for preview
  const previewNodes: MapNodeState[] = proposalNodes
    .filter((n) => n.included)
    .map((n) => ({
      node_id: n.id,
      node_type: n.type,
      title: n.title,
      mastery_level: n.mastered ? "mastered" : "not_started",
      status: n.mastered ? "completed" : "available",
      is_unlocked: true,
      prerequisites_met: true,
      prerequisite_node_ids: n.prerequisite_ids.filter((pid) => proposalNodes.some((pn) => pn.id === pid && pn.included)),
      attempts_count: 0,
      time_spent_minutes: 0,
    }));

  const includedCount = proposalNodes.filter((n) => n.included).length;
  const masteredCount = proposalNodes.filter((n) => n.included && n.mastered).length;
  const edgeCount = previewNodes.reduce((s, n) => s + n.prerequisite_node_ids.length, 0);

  return (
    <div className="max-w-2xl">
      <PageHeader
        title="Map Your Curriculum"
        subtitle="Bring your existing materials into METHEAN's tracking system."
      />

      {/* Contextual banner when linked from education plan */}
      {paramSubject && paramYear && (
        <div className="bg-(--color-accent-light) border border-(--color-accent)/15 rounded-[10px] px-4 py-2.5 mb-4 text-xs text-(--color-accent)">
          Mapping curriculum for <strong>{childName}'s {paramSubject}</strong> ({paramYear})
        </div>
      )}

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => setError("")}>Dismiss</Button>
          </div>
        </Card>
      )}

      {/* Progress */}
      {step < 6 && (
        <div className="flex items-center gap-2 mb-6">
          {[1, 2, 3].map((s) => (
            <div key={s} className={cn("flex-1 h-1 rounded-full transition-colors", step >= s ? "bg-(--color-accent)" : "bg-(--color-border)")} />
          ))}
        </div>
      )}

      {/* ── Step 1: Material info ── */}
      {step === 1 && (
        <Card animate>
          <h3 className="text-sm font-semibold text-(--color-text) mb-1">What are you teaching from?</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">
            Tell us about the curriculum or textbook you're using with {childName}.
          </p>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-(--color-text-secondary) block mb-1">Material name *</label>
              <input
                value={materialName}
                onChange={(e) => setMaterialName(e.target.value)}
                placeholder="Saxon Math 5/4, Story of the World Vol. 1, etc."
                className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px]"
              />
            </div>
            <div>
              <label className="text-xs text-(--color-text-secondary) block mb-1">Subject area *</label>
              <select
                value={subjectArea}
                onChange={(e) => setSubjectArea(e.target.value)}
                className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px]"
              >
                <option value="">Select a subject</option>
                {SUBJECTS.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-(--color-text-secondary) block mb-1">Description (optional)</label>
              <textarea
                value={materialDesc}
                onChange={(e) => setMaterialDesc(e.target.value)}
                placeholder="A mastery-based math program covering..."
                rows={2}
                className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px] resize-none"
              />
            </div>
          </div>
          <Button
            variant="primary" size="lg" className="w-full mt-5"
            disabled={!materialName.trim() || !subjectArea}
            onClick={() => setStep(2)}
          >
            Continue
          </Button>
        </Card>
      )}

      {/* ── Step 2: Table of Contents ── */}
      {step === 2 && (
        <Card animate>
          <h3 className="text-sm font-semibold text-(--color-text) mb-1">Paste the structure</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">
            Paste the table of contents, chapter list, or lesson sequence from your curriculum. The more detail, the better the map.
          </p>
          <textarea
            value={toc}
            onChange={(e) => setToc(e.target.value)}
            placeholder="Chapter 1: Addition Facts&#10;Chapter 2: Subtraction Facts&#10;Chapter 3: Place Value&#10;..."
            rows={12}
            className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px] resize-none font-mono"
          />
          <button
            onClick={() => setShowExample(!showExample)}
            className="mt-2 text-xs text-(--color-accent) hover:underline"
          >
            {showExample ? "Hide example" : "Show example"}
          </button>
          {showExample && (
            <pre className="mt-2 text-[11px] text-(--color-text-tertiary) bg-(--color-page) rounded-[10px] p-3 overflow-auto max-h-40 font-mono whitespace-pre-wrap">
              {EXAMPLE_TOC}
            </pre>
          )}
          <div className="flex gap-2 mt-4">
            <Button variant="ghost" size="md" onClick={() => setStep(1)}>Back</Button>
            <Button
              variant="primary" size="lg" className="flex-1"
              disabled={toc.trim().length < 10}
              onClick={() => setStep(3)}
            >
              Continue
            </Button>
          </div>
        </Card>
      )}

      {/* ── Step 3: Current position ── */}
      {step === 3 && (
        <Card animate>
          <h3 className="text-sm font-semibold text-(--color-text) mb-1">Where are you now?</h3>
          <p className="text-xs text-(--color-text-secondary) mb-4">
            Everything before this point will be marked as mastered. Everything after is upcoming.
          </p>
          <input
            value={currentPosition}
            onChange={(e) => setCurrentPosition(e.target.value)}
            placeholder="Chapter 5, Lesson 23, Unit 3, etc."
            className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px]"
          />
          <p className="text-[10px] text-(--color-text-tertiary) mt-1.5">Leave blank if you're starting from the beginning.</p>
          <div className="flex gap-2 mt-5">
            <Button variant="ghost" size="md" onClick={() => setStep(2)}>Back</Button>
            <Button variant="gold" size="lg" className="flex-1" onClick={runMapping}>
              Map It
            </Button>
          </div>
        </Card>
      )}

      {/* ── Step 4: Loading ── */}
      {step === 4 && loading && (
        <Card>
          <div className="text-center py-8">
            <div className="w-10 h-10 mx-auto mb-4 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
            <p className="text-sm text-(--color-text) mb-1">
              METHEAN is analyzing your curriculum structure...
            </p>
            <p className="text-xs text-(--color-text-tertiary)">
              {longWait
                ? "This is taking longer than usual. Complex curricula need more time."
                : `Mapping ${materialName} for ${childName}`}
            </p>
          </div>
        </Card>
      )}

      {/* ── Step 5: Review proposed map ── */}
      {step === 5 && (
        <>
          <Card className="mb-4" animate>
            <h3 className="text-sm font-semibold text-(--color-text) mb-1">Review your curriculum map</h3>
            <p className="text-xs text-(--color-text-secondary) mb-3">
              METHEAN analyzed <strong>{materialName}</strong> and created the following structure. Review, edit, then approve.
            </p>
            <div className="flex items-center gap-4 text-xs text-(--color-text-tertiary)">
              <span><strong className="text-(--color-text)">{includedCount}</strong> nodes</span>
              <span><strong className="text-(--color-text)">{edgeCount}</strong> connections</span>
              <span><strong className="text-(--color-success)">{masteredCount}</strong> already mastered</span>
            </div>
          </Card>

          {/* DAG Preview */}
          {previewNodes.length > 0 && (
            <div className="mb-4">
              <DagGraph nodes={previewNodes} />
            </div>
          )}

          {/* Editable node list */}
          <Card className="mb-4">
            <SectionHeaderInline title="Proposed Nodes" count={proposalNodes.length} />
            <div className="space-y-1 mt-3 max-h-[400px] overflow-y-auto">
              {proposalNodes.map((node, idx) => (
                <div key={node.id} className={cn(
                  "flex items-center gap-2 px-3 py-2 rounded-[8px] text-sm transition-colors",
                  node.included ? "bg-(--color-page)" : "bg-(--color-page) opacity-40"
                )}>
                  <input
                    type="checkbox"
                    checked={node.included}
                    onChange={() => {
                      setProposalNodes((prev) => prev.map((n, i) => i === idx ? { ...n, included: !n.included } : n));
                    }}
                    className="rounded shrink-0"
                  />
                  {editingIdx === idx ? (
                    <input
                      value={node.title}
                      onChange={(e) => {
                        setProposalNodes((prev) => prev.map((n, i) => i === idx ? { ...n, title: e.target.value } : n));
                      }}
                      onBlur={() => setEditingIdx(null)}
                      onKeyDown={(e) => e.key === "Enter" && setEditingIdx(null)}
                      autoFocus
                      className="flex-1 px-2 py-0.5 text-sm border border-(--color-accent) rounded-[6px] bg-(--color-surface)"
                    />
                  ) : (
                    <span
                      className="flex-1 cursor-pointer hover:text-(--color-accent) transition-colors"
                      onClick={() => setEditingIdx(idx)}
                      title="Click to edit"
                    >
                      {node.title}
                    </span>
                  )}
                  <span className={cn(
                    "text-[10px] px-1.5 py-0.5 rounded-full font-medium capitalize shrink-0",
                    node.type === "milestone" ? "bg-(--color-accent-light) text-(--color-accent)" : "bg-(--color-page) text-(--color-text-tertiary)"
                  )}>
                    {node.type}
                  </span>
                  <button
                    onClick={() => {
                      setProposalNodes((prev) => prev.map((n, i) => i === idx ? { ...n, mastered: !n.mastered } : n));
                    }}
                    className={cn(
                      "text-[10px] px-1.5 py-0.5 rounded-full font-medium shrink-0 transition-colors",
                      node.mastered
                        ? "bg-(--color-success-light) text-(--color-success)"
                        : "bg-(--color-border) text-(--color-text-tertiary) hover:bg-(--color-success-light) hover:text-(--color-success)"
                    )}
                    title={node.mastered ? "Click to mark as upcoming" : "Click to mark as mastered"}
                  >
                    {node.mastered ? "mastered" : "upcoming"}
                  </button>
                </div>
              ))}
            </div>
          </Card>

          <div className="flex gap-2">
            <Button variant="ghost" size="md" onClick={reset}>Start Over</Button>
            <Button
              variant="primary" size="lg" className="flex-1"
              disabled={includedCount === 0}
              onClick={async () => {
                toast("Curriculum mapped! Enrolling...", "success");
                // Check education plan for subject match
                if (selectedChild) {
                  try {
                    const plan = await educationPlan.get(selectedChild.id);
                    const yp = (plan as any)?.year_plans;
                    if (yp && typeof yp === "object") {
                      setPlanExists(true);
                      const subLower = subjectArea.toLowerCase();
                      for (const [yr, data] of Object.entries(yp)) {
                        const subjects = (data as any).subjects || [];
                        if (subjects.some((s: any) => (s.name || s.subject || "").toLowerCase().includes(subLower))) {
                          setPlanMatch(yr);
                          break;
                        }
                      }
                    }
                  } catch { /* no plan */ }
                }
                setStep(6);
              }}
            >
              Approve & Create Map ({includedCount} nodes)
            </Button>
          </div>
        </>
      )}

      {/* ── Step 6: Confirmation ── */}
      {step === 6 && (
        <Card animate>
          <div className="text-center py-6">
            <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-(--color-success-light) flex items-center justify-center animate-scale-in">
              <svg className="w-7 h-7 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-lg font-semibold text-(--color-text) mb-1">Your curriculum is mapped!</h2>
            <p className="text-sm text-(--color-text-secondary) mb-6">
              {childName} is enrolled and tracking from {currentPosition || "the beginning"}.
              <br />
              <span className="text-xs text-(--color-text-tertiary)">{includedCount} nodes, {masteredCount} already mastered</span>
            </p>
            {/* Education plan connection */}
            {planMatch && (
              <div className="bg-(--color-success-light) rounded-[10px] px-4 py-2.5 mb-4 text-xs text-(--color-success) max-w-xs mx-auto">
                This curriculum has been connected to {childName}'s education plan for {planMatch}.
              </div>
            )}
            {planExists && !planMatch && (
              <div className="bg-(--color-warning-light) rounded-[10px] px-4 py-2.5 mb-4 text-xs text-(--color-warning) max-w-xs mx-auto">
                This subject isn't in {childName}'s education plan yet.{" "}
                <a href="/plans/vision" className="underline">Update their plan</a>
              </div>
            )}

            <div className="space-y-2 max-w-xs mx-auto">
              <Button variant="primary" size="lg" className="w-full" onClick={() => window.location.href = "/maps"}>
                View {materialName} map
              </Button>
              <Button variant="secondary" size="md" className="w-full" onClick={() => window.location.href = "/dashboard"}>
                Back to Dashboard
              </Button>
              <button onClick={reset} className="text-xs text-(--color-text-tertiary) hover:underline mt-2">
                Map another curriculum
              </button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}

// ── Inline section header for the node list ──
function SectionHeaderInline({ title, count }: { title: string; count: number }) {
  return (
    <div className="flex items-center justify-between">
      <h4 className="text-xs font-semibold text-(--color-text-secondary) uppercase tracking-wider">{title}</h4>
      <span className="text-[10px] text-(--color-text-tertiary)">{count} total</span>
    </div>
  );
}
