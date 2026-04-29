"use client";

import { useEffect, useState } from "react";
import { assessment } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { useMobile } from "@/lib/useMobile";
import { useToast } from "@/components/Toast";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import EmptyState from "@/components/ui/EmptyState";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { cn } from "@/lib/cn";

const TYPES = ["parent_observation", "oral_narration", "written_work", "demonstration", "project", "discussion", "quiz"];
const JUDGMENTS: { id: string; label: string; description: string }[] = [
  { id: "mastered", label: "Mastered", description: "Has it down. Demonstrates consistent skill." },
  { id: "proficient", label: "Proficient", description: "Confident and capable. Working independently." },
  { id: "developing", label: "Developing", description: "Coming along. Needs occasional support." },
  { id: "emerging", label: "Emerging", description: "Just starting. Heavy support still needed." },
  { id: "needs_review", label: "Needs Review", description: "Concerned. Revisit before moving on." },
];
const PORTFOLIO_TYPES = ["work_sample", "narrative", "photo", "certificate", "reading_log", "field_trip"];

function FileIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  );
}

export default function AssessmentPage() {
  useEffect(() => { document.title = "Assessment | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const isMobile = useMobile();
  const { toast } = useToast();
  const [tab, setTab] = useState<"assess" | "portfolio">("assess");
  const [assessments, setAssessments] = useState<any[]>([]);
  const [portfolio, setPortfolio] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [showPortfolioForm, setShowPortfolioForm] = useState(false);
  const [transcript, setTranscript] = useState<any>(null);
  const [transcriptLoading, setTranscriptLoading] = useState(false);
  const [showTranscriptModal, setShowTranscriptModal] = useState(false);

  const [aType, setAType] = useState("parent_observation");
  const [aTitle, setATitle] = useState("");
  const [aNotes, setANotes] = useState("");
  const [aJudgment, setAJudgment] = useState("");
  const [aSubject, setASubject] = useState("");

  const [pType, setPType] = useState("work_sample");
  const [pTitle, setPTitle] = useState("");
  const [pDesc, setPDesc] = useState("");
  const [pSubject, setPSubject] = useState("");
  const [pDate, setPDate] = useState("");

  useEffect(() => { if (selectedChild) load(); }, [selectedChild, tab]);

  async function load() {
    if (!selectedChild) return;
    setLoading(true);
    setError("");
    try {
      if (tab === "assess") {
        const d = await assessment.list(selectedChild.id);
        setAssessments(d.items || []);
      } else {
        const d = await assessment.listPortfolio(selectedChild.id);
        setPortfolio(d.items || []);
      }
    } catch (err: any) {
      const msg = err?.detail || err?.message || "Failed to load assessments.";
      setError(msg);
      toast(msg, "error");
    } finally {
      setLoading(false);
    }
  }

  async function submitAssessment() {
    if (!selectedChild || !aTitle) return;
    try {
      await assessment.create(selectedChild.id, {
        assessment_type: aType, title: aTitle, qualitative_notes: aNotes,
        mastery_judgment: aJudgment || undefined, subject: aSubject || undefined,
      });
      setShowForm(false);
      setATitle(""); setANotes(""); setAJudgment(""); setASubject("");
      toast("Assessment recorded.", "success");
      await load();
    } catch (err: any) {
      const msg = err?.detail || err?.message || "Couldn't save assessment.";
      setError(msg);
      toast(msg, "error");
    }
  }

  async function submitPortfolio() {
    if (!selectedChild || !pTitle) return;
    try {
      await assessment.createPortfolio(selectedChild.id, {
        entry_type: pType, title: pTitle, description: pDesc,
        subject: pSubject || undefined, date_completed: pDate || undefined,
      });
      setShowPortfolioForm(false);
      setPTitle(""); setPDesc(""); setPSubject(""); setPDate("");
      toast("Portfolio entry added.", "success");
      await load();
    } catch (err: any) {
      const msg = err?.detail || err?.message || "Couldn't save portfolio entry.";
      setError(msg);
      toast(msg, "error");
    }
  }

  async function generateTranscript() {
    if (!selectedChild) return;
    setTranscriptLoading(true);
    try {
      const t = await assessment.transcript(selectedChild.id);
      setTranscript(t);
      toast("Transcript generated.", "success");
    } catch (err: any) {
      const msg = err?.detail || err?.message || "Couldn't generate transcript.";
      setError(msg);
      toast(msg, "error");
    } finally {
      setTranscriptLoading(false);
    }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;
  if (loading) return <div className="max-w-4xl"><PageHeader title="Assessment" /><LoadingSkeleton variant="card" count={3} /></div>;

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Assessment & Portfolio"
        subtitle={`${selectedChild.first_name}'s mastery record. AI advises, you decide.`}
      />

      {/* Transcript prominence — Card lives above the tabs so the
          formal record is always one tap away regardless of which
          tab the parent is on. */}
      <Card className="mb-5">
        <div className="flex items-start gap-4 flex-col sm:flex-row sm:items-center">
          <div className="flex-1 min-w-0">
            <h3 className="text-[15px] font-semibold text-(--color-text)">Formal Transcript</h3>
            <p className="text-xs text-(--color-text-secondary) mt-0.5">
              Cumulative academic record — GPA equivalent, mastery, and instruction hours per subject.
            </p>
            {transcript && (
              <div className="flex flex-wrap items-center gap-x-5 gap-y-1 mt-2.5">
                <Stat label="GPA" value={String((transcript as any).gpa ?? "—")} />
                <Stat label="Subjects" value={String((transcript as any).subjects?.length ?? 0)} />
                <Stat
                  label="Hours logged"
                  value={String(((transcript as any).subjects ?? []).reduce(
                    (sum: number, s: any) => sum + Number(s.hours_logged || 0), 0,
                  ))}
                />
              </div>
            )}
          </div>
          <div className={cn("flex gap-2", isMobile ? "w-full" : "shrink-0")}>
            {transcript ? (
              <Button
                variant="secondary"
                onClick={() => setShowTranscriptModal(true)}
                className={isMobile ? "flex-1 min-h-[44px]" : ""}
              >
                View Full Transcript
              </Button>
            ) : null}
            <Button
              variant={transcript ? "ghost" : "primary"}
              onClick={generateTranscript}
              disabled={transcriptLoading}
              className={isMobile ? "flex-1 min-h-[44px]" : ""}
            >
              {transcriptLoading ? "Generating…" : transcript ? "Regenerate" : "Generate"}
            </Button>
          </div>
        </div>
      </Card>

      {/* Tabs — full-width segmented control on mobile per spec.
          Each tab is min-h-[44px] for comfortable touch targets. */}
      <div
        role="tablist"
        className={cn(
          "flex gap-1 p-1 bg-(--color-page) rounded-[10px] border border-(--color-border) mb-5",
          isMobile ? "w-full" : "w-fit",
        )}
      >
        {([
          { key: "assess", label: "Assessments" },
          { key: "portfolio", label: "Portfolio" },
        ] as const).map((t) => (
          <button
            key={t.key}
            role="tab"
            aria-selected={tab === t.key}
            onClick={() => setTab(t.key)}
            className={cn(
              "px-4 text-[13px] rounded-[8px] transition-all duration-200 min-h-[44px] sm:min-h-0 sm:py-1.5",
              isMobile ? "flex-1" : "",
              tab === t.key
                ? "bg-(--color-surface) text-(--color-text) font-medium shadow-sm"
                : "text-(--color-text-secondary) hover:text-(--color-text)",
            )}
          >
            {t.label}
          </button>
        ))}
      </div>

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); load(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {tab === "assess" && (
        <>
          <div className="flex gap-2 mb-4">
            <Button
              onClick={() => setShowForm(!showForm)}
              className={isMobile ? "w-full min-h-[44px]" : ""}
            >
              {showForm ? "Cancel" : "Record Assessment"}
            </Button>
          </div>

          {showForm && (
            // Constitutional-tinted form area: this is the
            // governance moment where a parent overrides the AI's
            // mastery call. Brown left border + tinted background
            // signal that significance.
            <Card
              padding={isMobile ? "p-4" : "p-5"}
              className="mb-6 bg-(--color-constitutional-light)"
              borderLeft="border-l-(--color-constitutional)"
            >
              <div className="flex items-center gap-2 mb-4">
                <ShieldIcon size={18} className="text-(--color-constitutional)" />
                <h3 className="text-[15px] font-semibold text-(--color-text)">Parent Assessment</h3>
              </div>
              <p className="text-xs text-(--color-text-secondary) mb-4 leading-relaxed">
                Your judgment overrides AI-generated mastery scores. Every override is logged in the decision trace.
              </p>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-(--color-text-secondary) mb-1.5">Assessment type</label>
                  <div className="flex flex-wrap gap-2">
                    {TYPES.map((t) => (
                      <button
                        key={t}
                        onClick={() => setAType(t)}
                        className={cn(
                          "px-3 py-2 text-xs rounded-[10px] border capitalize min-h-[44px] sm:min-h-0 sm:py-1.5 transition-colors",
                          aType === t
                            ? "border-(--color-constitutional) bg-(--color-surface) text-(--color-text) font-medium"
                            : "border-(--color-border) bg-(--color-surface) text-(--color-text-secondary) hover:border-(--color-border-strong)",
                        )}
                      >
                        {t.replace(/_/g, " ")}
                      </button>
                    ))}
                  </div>
                </div>

                <input
                  value={aTitle}
                  onChange={(e) => setATitle(e.target.value)}
                  placeholder="Assessment title"
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) min-h-[44px] sm:min-h-0"
                />
                <input
                  value={aSubject}
                  onChange={(e) => setASubject(e.target.value)}
                  placeholder="Subject (optional)"
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) min-h-[44px] sm:min-h-0"
                />
                <textarea
                  value={aNotes}
                  onChange={(e) => setANotes(e.target.value)}
                  placeholder="What did you observe? Strengths, gaps, the way they explained it back to you…"
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) h-24 resize-none leading-relaxed"
                />

                {/* Judgment selector as tappable Cards. This is the
                    actual override moment — make it weighty, not
                    a dropdown. */}
                <div>
                  <label className="block text-xs font-medium text-(--color-text-secondary) mb-2">
                    Your mastery judgment{" "}
                    <span className="text-(--color-text-tertiary)">(overrides AI)</span>
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    {JUDGMENTS.map((j) => (
                      <button
                        key={j.id}
                        type="button"
                        onClick={() => setAJudgment(j.id === aJudgment ? "" : j.id)}
                        aria-pressed={aJudgment === j.id}
                        className={cn(
                          "text-left rounded-[12px] border p-3 transition-all min-h-[64px]",
                          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--color-accent)/30",
                          aJudgment === j.id
                            ? "border-(--color-constitutional) bg-(--color-surface) shadow-[var(--shadow-card)]"
                            : "border-(--color-border) bg-(--color-surface)/70 hover:border-(--color-border-strong)",
                        )}
                      >
                        <div className="flex items-center justify-between gap-2 mb-1">
                          <StatusBadge status={j.id} />
                          {aJudgment === j.id && (
                            <span className="text-(--color-constitutional)">
                              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="20 6 9 17 4 12" />
                              </svg>
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-(--color-text-secondary) leading-snug">{j.description}</p>
                      </button>
                    ))}
                  </div>
                </div>

                <Button
                  onClick={submitAssessment}
                  disabled={!aTitle}
                  size="lg"
                  className={isMobile ? "w-full" : ""}
                >
                  Submit Assessment
                </Button>
              </div>
            </Card>
          )}

          {/* Assessment list — single column, comfortable padding. */}
          <div className="space-y-2.5">
            {assessments.map((a: any) => (
              <Card key={a.id} padding={isMobile ? "p-4" : "p-4 sm:p-5"}>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm font-medium text-(--color-text)">{a.title}</span>
                      <StatusBadge status={a.assessment_type} />
                      {a.mastery_judgment && <StatusBadge status={a.mastery_judgment} />}
                    </div>
                    {a.qualitative_notes && (
                      <p className="text-xs text-(--color-text-secondary) mt-1.5 leading-relaxed line-clamp-2">
                        {a.qualitative_notes}
                      </p>
                    )}
                    {a.subject && (
                      <p className="text-[11px] text-(--color-text-tertiary) mt-1 capitalize">{a.subject}</p>
                    )}
                  </div>
                  <span className="shrink-0 text-xs text-(--color-text-tertiary) tabular-nums">
                    {a.assessed_at?.split("T")[0]}
                  </span>
                </div>
              </Card>
            ))}
            {!loading && assessments.length === 0 && (
              <EmptyState
                icon="empty"
                title="No assessments recorded yet"
                description={`Record your first observation to start building ${selectedChild?.first_name || "your child"}'s portfolio.`}
              />
            )}
          </div>
        </>
      )}

      {tab === "portfolio" && (
        <>
          <div className="flex gap-2 mb-4">
            <Button
              onClick={() => setShowPortfolioForm(!showPortfolioForm)}
              className={isMobile ? "w-full min-h-[44px]" : ""}
            >
              {showPortfolioForm ? "Cancel" : "Add Entry"}
            </Button>
          </div>

          {showPortfolioForm && (
            <Card padding={isMobile ? "p-4" : "p-5"} className="mb-6">
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-(--color-text-secondary) mb-1.5">Entry type</label>
                  <div className="flex flex-wrap gap-2">
                    {PORTFOLIO_TYPES.map((t) => (
                      <button
                        key={t}
                        onClick={() => setPType(t)}
                        className={cn(
                          "px-3 py-2 text-xs rounded-[10px] border capitalize min-h-[44px] sm:min-h-0 sm:py-1.5 transition-colors",
                          pType === t
                            ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-text) font-medium"
                            : "border-(--color-border) text-(--color-text-secondary) hover:border-(--color-border-strong)",
                        )}
                      >
                        {t.replace(/_/g, " ")}
                      </button>
                    ))}
                  </div>
                </div>
                <input
                  value={pTitle}
                  onChange={(e) => setPTitle(e.target.value)}
                  placeholder="Title"
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) min-h-[44px] sm:min-h-0"
                />
                <textarea
                  value={pDesc}
                  onChange={(e) => setPDesc(e.target.value)}
                  placeholder="Description"
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) h-20 resize-none leading-relaxed"
                />
                <div className="flex flex-col sm:flex-row gap-3">
                  <input
                    value={pSubject}
                    onChange={(e) => setPSubject(e.target.value)}
                    placeholder="Subject"
                    className="flex-1 px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) min-h-[44px] sm:min-h-0"
                  />
                  <input
                    type="date"
                    value={pDate}
                    onChange={(e) => setPDate(e.target.value)}
                    className="px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) min-h-[44px] sm:min-h-0"
                  />
                </div>
                <Button
                  onClick={submitPortfolio}
                  disabled={!pTitle}
                  size="lg"
                  className={isMobile ? "w-full" : ""}
                >
                  Add Entry
                </Button>
              </div>
            </Card>
          )}

          {/* Portfolio cards — single col on mobile, 2 col on md+
              with the file-icon thumbnail when artifact_id is
              present. The model exposes artifact_id (uuid) but
              not a direct image URL, so we surface a file icon
              rather than fabricate a thumbnail. */}
          <div className={cn("grid gap-3", isMobile ? "grid-cols-1" : "grid-cols-1 md:grid-cols-2")}>
            {portfolio.map((e: any) => {
              const hasArtifact = !!e.artifact_id;
              return (
                <Card key={e.id} padding={isMobile ? "p-4" : "p-4 sm:p-5"}>
                  <div className="flex items-start gap-3">
                    {hasArtifact && (
                      <div className="shrink-0 w-10 h-10 rounded-[8px] bg-(--color-page) border border-(--color-border) flex items-center justify-center text-(--color-text-secondary)">
                        <FileIcon />
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <StatusBadge status={e.entry_type} />
                      </div>
                      <h4 className="text-sm font-semibold text-(--color-text) leading-tight">{e.title}</h4>
                      {e.description && (
                        <p className="text-xs text-(--color-text-secondary) mt-1 leading-relaxed line-clamp-2">{e.description}</p>
                      )}
                      <div className="text-[11px] text-(--color-text-tertiary) mt-2">
                        {e.subject && <span className="capitalize">{e.subject}</span>}
                        {e.subject && e.date_completed && <span> · </span>}
                        {e.date_completed && <span>{e.date_completed}</span>}
                        {!e.subject && !e.date_completed && <span>No date</span>}
                      </div>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
          {!loading && portfolio.length === 0 && (
            <EmptyState
              icon="empty"
              title="No portfolio entries yet"
              description="Add work samples, photos, or descriptions to build a portfolio."
            />
          )}
        </>
      )}

      {/* Transcript modal — opens from the prominent Card up top. */}
      {showTranscriptModal && transcript && (
        <div
          className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
          role="dialog"
          aria-modal="true"
          onClick={() => setShowTranscriptModal(false)}
        >
          <Card
            padding="p-0"
            className="w-full max-w-[640px] max-h-[85vh] overflow-hidden shadow-lg animate-scale-in flex flex-col"
          >
            <div onClick={(e) => e.stopPropagation()} className="flex flex-col h-full">
              <div className="flex items-center justify-between px-5 py-4 border-b border-(--color-border)">
                <h2 className="text-sm font-semibold text-(--color-text) uppercase tracking-[0.06em]">Unofficial Transcript</h2>
                <button
                  onClick={() => setShowTranscriptModal(false)}
                  className="text-xs text-(--color-text-secondary) hover:text-(--color-text) min-h-[44px] sm:min-h-0 px-2"
                >
                  Close
                </button>
              </div>
              <div className="flex-1 overflow-y-auto px-5 py-4">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-(--color-border) text-xs text-(--color-text-secondary)">
                        <th className="text-left py-2 font-medium">Subject</th>
                        <th className="font-medium">Grade</th>
                        <th className="font-medium">Mastered</th>
                        <th className="font-medium">Hours</th>
                      </tr>
                    </thead>
                    <tbody>
                      {((transcript as any).subjects || []).map((s: any, i: number) => (
                        <tr key={i} className="border-b border-(--color-page)">
                          <td className="py-2.5 text-(--color-text)">{s.subject}</td>
                          <td className="text-center font-semibold text-(--color-text)">{s.grade}</td>
                          <td className="text-center text-xs text-(--color-text-secondary)">{s.nodes_mastered}/{s.nodes_total}</td>
                          <td className="text-center text-xs text-(--color-text-secondary) tabular-nums">{s.hours_logged}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="text-xs text-(--color-text-secondary) mt-4">GPA: <span className="font-semibold text-(--color-text)">{(transcript as any).gpa}</span></div>
              </div>
              <div className="flex items-center justify-end gap-2 px-5 py-3 border-t border-(--color-border)">
                <Button variant="ghost" size="sm" onClick={() => window.print()}>Print</Button>
                <Button variant="secondary" size="sm" onClick={() => setShowTranscriptModal(false)}>Done</Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-[11px] uppercase tracking-[0.06em] text-(--color-text-tertiary)">{label}</div>
      <div className="text-sm font-semibold text-(--color-text) tabular-nums">{value}</div>
    </div>
  );
}
