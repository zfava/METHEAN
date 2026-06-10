"use client";

import MetricCard from "@/components/ui/MetricCard";
import type { FamilyRecordData } from "@/lib/api";

function firstEvidenceDate(record: FamilyRecordData): Date | null {
  let earliest: Date | null = null;
  const consider = (iso: string | null) => {
    if (!iso) return;
    const d = new Date(iso);
    if (!earliest || d < earliest) earliest = d;
  };
  for (const m of record.mastery_evidence) {
    consider(m.achieved_at);
    for (const a of m.attempts) consider(a.started_at);
    for (const g of m.governance_events) consider(g.created_at);
  }
  return earliest;
}

/** Counts pulled straight from the record JSON. Nothing fabricated:
 *  every number here is derivable from the record alone. */
export default function SummaryBand({ record }: { record: FamilyRecordData }) {
  const masteredCount = record.mastery_evidence.length;
  const evidenceEvents = record.mastery_evidence.reduce(
    (sum, m) => sum + m.attempts.length + m.assessments.length + m.governance_events.length,
    0,
  );
  const subjects = new Set(
    record.mastery_evidence.map((m) => m.subject).filter((s): s is string => Boolean(s)),
  );
  for (const course of record.transcript.courses) subjects.add(course.subject_name);
  const began = firstEvidenceDate(record);

  return (
    <div data-testid="summary-band" className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-6">
      <MetricCard label="Skills mastered" value={masteredCount} />
      <MetricCard label="Evidence entries" value={evidenceEvents} subtitle="attempts, assessments, approvals" />
      <MetricCard label="Subjects" value={subjects.size} />
      <MetricCard label="Hours logged" value={`${record.attendance.total_hours}h`} subtitle="all time" />
      <MetricCard
        label="Record began"
        value={began ? began.toLocaleDateString(undefined, { month: "long", year: "numeric" }) : "Not yet"}
        subtitle={began ? undefined : "builds with first evidence"}
      />
    </div>
  );
}
