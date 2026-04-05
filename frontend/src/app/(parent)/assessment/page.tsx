"use client";

import { useEffect, useState } from "react";
import { assessment } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import StatusBadge from "@/components/StatusBadge";

const TYPES = ["parent_observation", "oral_narration", "written_work", "demonstration", "project", "discussion", "quiz"];
const JUDGMENTS = ["mastered", "proficient", "developing", "emerging", "needs_review"];

export default function AssessmentPage() {
  const { selectedChild } = useChild();
  const [tab, setTab] = useState<"assess" | "portfolio">("assess");
  const [assessments, setAssessments] = useState<any[]>([]);
  const [portfolio, setPortfolio] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showPortfolioForm, setShowPortfolioForm] = useState(false);
  const [transcript, setTranscript] = useState<any>(null);

  // Assessment form
  const [aType, setAType] = useState("parent_observation");
  const [aTitle, setATitle] = useState("");
  const [aNotes, setANotes] = useState("");
  const [aJudgment, setAJudgment] = useState("");
  const [aSubject, setASubject] = useState("");

  // Portfolio form
  const [pType, setPType] = useState("work_sample");
  const [pTitle, setPTitle] = useState("");
  const [pDesc, setPDesc] = useState("");
  const [pSubject, setPSubject] = useState("");
  const [pDate, setPDate] = useState("");

  useEffect(() => { if (selectedChild) load(); }, [selectedChild, tab]);

  async function load() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      if (tab === "assess") {
        const d = await assessment.list(selectedChild.id);
        setAssessments(d.items || []);
      } else {
        const d = await assessment.listPortfolio(selectedChild.id);
        setPortfolio(d.items || []);
      }
    } catch {} finally { setLoading(false); }
  }

  async function submitAssessment() {
    if (!selectedChild || !aTitle) return;
    await assessment.create(selectedChild.id, {
      assessment_type: aType, title: aTitle, qualitative_notes: aNotes,
      mastery_judgment: aJudgment || undefined, subject: aSubject || undefined,
    });
    setShowForm(false);
    setATitle(""); setANotes(""); setAJudgment(""); setASubject("");
    await load();
  }

  async function submitPortfolio() {
    if (!selectedChild || !pTitle) return;
    await assessment.createPortfolio(selectedChild.id, {
      entry_type: pType, title: pTitle, description: pDesc,
      subject: pSubject || undefined, date_completed: pDate || undefined,
    });
    setShowPortfolioForm(false);
    setPTitle(""); setPDesc(""); setPSubject(""); setPDate("");
    await load();
  }

  async function showTranscript() {
    if (!selectedChild) return;
    const t = await assessment.transcript(selectedChild.id);
    setTranscript(t);
  }

  if (!selectedChild) return <div className="text-sm text-slate-500">Select a child.</div>;

  return (
    <div className="max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold text-slate-800">Assessment &amp; Portfolio</h1>
        <div className="flex gap-2">
          <button onClick={() => setTab("assess")}
            className={`px-4 py-1.5 text-sm rounded-lg ${tab === "assess" ? "bg-slate-800 text-white" : "bg-slate-100"}`}>Assessments</button>
          <button onClick={() => setTab("portfolio")}
            className={`px-4 py-1.5 text-sm rounded-lg ${tab === "portfolio" ? "bg-slate-800 text-white" : "bg-slate-100"}`}>Portfolio</button>
        </div>
      </div>

      {tab === "assess" && (
        <>
          <div className="flex gap-2 mb-4">
            <button onClick={() => setShowForm(!showForm)}
              className="px-4 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              {showForm ? "Cancel" : "Record Assessment"}
            </button>
          </div>

          {showForm && (
            <div className="bg-white rounded-lg border border-slate-200 p-5 mb-6">
              <div className="space-y-3">
                <div className="flex flex-wrap gap-2">
                  {TYPES.map((t) => (
                    <button key={t} onClick={() => setAType(t)}
                      className={`px-3 py-1.5 text-xs rounded-lg border capitalize ${aType === t ? "border-blue-500 bg-blue-50" : "border-slate-200"}`}>
                      {t.replace(/_/g, " ")}
                    </button>
                  ))}
                </div>
                <input value={aTitle} onChange={(e) => setATitle(e.target.value)}
                  placeholder="Assessment title" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg" />
                <input value={aSubject} onChange={(e) => setASubject(e.target.value)}
                  placeholder="Subject (optional)" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg" />
                <textarea value={aNotes} onChange={(e) => setANotes(e.target.value)}
                  placeholder="What did you observe?" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg h-24 resize-none" />
                <div>
                  <label className="block text-xs text-slate-500 mb-1">Your mastery judgment (overrides AI)</label>
                  <div className="flex gap-2">
                    {JUDGMENTS.map((j) => (
                      <button key={j} onClick={() => setAJudgment(j === aJudgment ? "" : j)}
                        className={`px-3 py-1 text-xs rounded-lg border capitalize ${aJudgment === j ? "border-blue-500 bg-blue-50 font-medium" : "border-slate-200"}`}>
                        {j.replace(/_/g, " ")}
                      </button>
                    ))}
                  </div>
                </div>
                <button onClick={submitAssessment} disabled={!aTitle}
                  className="px-6 py-2 text-sm font-medium bg-slate-800 text-white rounded-lg disabled:opacity-50">Submit</button>
              </div>
            </div>
          )}

          <div className="space-y-2">
            {assessments.map((a: any) => (
              <div key={a.id} className="bg-white rounded-lg border border-slate-200 p-4 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-slate-800">{a.title}</span>
                    <StatusBadge status={a.assessment_type} />
                    {a.mastery_judgment && <StatusBadge status={a.mastery_judgment} />}
                  </div>
                  {a.qualitative_notes && <p className="text-xs text-slate-500 mt-1 line-clamp-1">{a.qualitative_notes}</p>}
                </div>
                <span className="text-xs text-slate-400">{a.assessed_at?.split("T")[0]}</span>
              </div>
            ))}
            {!loading && assessments.length === 0 && <p className="text-sm text-slate-400">No assessments recorded yet.</p>}
          </div>
        </>
      )}

      {tab === "portfolio" && (
        <>
          <div className="flex gap-2 mb-4">
            <button onClick={() => setShowPortfolioForm(!showPortfolioForm)}
              className="px-4 py-2 text-sm font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              {showPortfolioForm ? "Cancel" : "Add Entry"}
            </button>
            <button onClick={showTranscript} className="px-4 py-2 text-sm border border-slate-300 rounded-lg hover:bg-slate-50">
              Generate Transcript
            </button>
          </div>

          {showPortfolioForm && (
            <div className="bg-white rounded-lg border border-slate-200 p-5 mb-6 space-y-3">
              <div className="flex gap-2">
                {["work_sample", "narrative", "photo", "certificate", "reading_log", "field_trip"].map((t) => (
                  <button key={t} onClick={() => setPType(t)}
                    className={`px-3 py-1.5 text-xs rounded-lg border capitalize ${pType === t ? "border-blue-500 bg-blue-50" : "border-slate-200"}`}>
                    {t.replace(/_/g, " ")}
                  </button>
                ))}
              </div>
              <input value={pTitle} onChange={(e) => setPTitle(e.target.value)} placeholder="Title" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg" />
              <textarea value={pDesc} onChange={(e) => setPDesc(e.target.value)} placeholder="Description" className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg h-16 resize-none" />
              <div className="flex gap-3">
                <input value={pSubject} onChange={(e) => setPSubject(e.target.value)} placeholder="Subject" className="flex-1 px-3 py-2 text-sm border border-slate-200 rounded-lg" />
                <input type="date" value={pDate} onChange={(e) => setPDate(e.target.value)} className="px-3 py-2 text-sm border border-slate-200 rounded-lg" />
              </div>
              <button onClick={submitPortfolio} disabled={!pTitle}
                className="px-6 py-2 text-sm font-medium bg-slate-800 text-white rounded-lg disabled:opacity-50">Add Entry</button>
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            {portfolio.map((e: any) => (
              <div key={e.id} className="bg-white rounded-lg border border-slate-200 p-4">
                <div className="flex items-center gap-2 mb-1">
                  <StatusBadge status={e.entry_type} />
                  <span className="text-sm font-medium text-slate-800">{e.title}</span>
                </div>
                <div className="text-xs text-slate-400">
                  {e.subject && <span>{e.subject} &middot; </span>}
                  {e.date_completed || "No date"}
                </div>
              </div>
            ))}
          </div>
          {!loading && portfolio.length === 0 && <p className="text-sm text-slate-400">No portfolio entries yet.</p>}

          {transcript && (
            <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg w-[600px] max-h-[80vh] overflow-y-auto p-6 shadow-lg">
                <div className="flex justify-between mb-4">
                  <h2 className="text-sm font-bold text-slate-800 uppercase">Unofficial Transcript</h2>
                  <button onClick={() => setTranscript(null)} className="text-xs text-slate-400">Close</button>
                </div>
                <table className="w-full text-sm mb-4">
                  <thead><tr className="border-b text-xs text-slate-500">
                    <th className="text-left py-2">Subject</th><th>Grade</th><th>Mastered</th><th>Hours</th>
                  </tr></thead>
                  <tbody>
                    {((transcript as any).subjects || []).map((s: any, i: number) => (
                      <tr key={i} className="border-b border-slate-50">
                        <td className="py-2">{s.subject}</td>
                        <td className="text-center font-semibold">{s.grade}</td>
                        <td className="text-center text-xs">{s.nodes_mastered}/{s.nodes_total}</td>
                        <td className="text-center text-xs">{s.hours_logged}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <div className="text-xs text-slate-500">GPA: {(transcript as any).gpa}</div>
                <button onClick={() => window.print()} className="mt-3 text-xs text-blue-600">Print</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
