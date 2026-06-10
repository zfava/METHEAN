"use client";

import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import SectionHeader from "@/components/ui/SectionHeader";
import type { FamilyRecordData } from "@/lib/api";

/** Transcript preview: the same data the exported transcript PDF
 *  carries, rendered as a table. */
export default function TranscriptTable({ transcript }: { transcript: FamilyRecordData["transcript"] }) {
  return (
    <div data-testid="transcript-table">
    <Card className="mb-6">
      <SectionHeader title="Transcript" />
      {transcript.courses.length === 0 ? (
        <p className="text-xs text-(--color-text-tertiary) mt-2">
          Courses appear here once an annual curriculum exists. The exported transcript carries exactly this table.
        </p>
      ) : (
        <div className="overflow-x-auto mt-3">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[11px] uppercase tracking-wide text-(--color-text-tertiary) border-b border-(--color-border)">
                <th className="py-2 pr-4 font-medium">Year</th>
                <th className="py-2 pr-4 font-medium">Subject</th>
                <th className="py-2 pr-4 font-medium">Grade</th>
                <th className="py-2 pr-4 font-medium">Progress</th>
                <th className="py-2 font-medium">Level</th>
              </tr>
            </thead>
            <tbody>
              {transcript.courses.map((c, i) => (
                <tr key={`${c.academic_year}-${c.subject_name}-${i}`} className="border-b border-(--color-border)/60 last:border-0">
                  <td className="py-2.5 pr-4 text-(--color-text-secondary) whitespace-nowrap">{c.academic_year}</td>
                  <td className="py-2.5 pr-4 text-(--color-text) font-medium">{c.subject_name}</td>
                  <td className="py-2.5 pr-4 text-(--color-text-secondary)">{c.grade_level || "-"}</td>
                  <td className="py-2.5 pr-4 text-(--color-text-secondary) whitespace-nowrap">
                    {c.weeks_completed}/{c.total_weeks ?? "?"} weeks
                  </td>
                  <td className="py-2.5">
                    {c.overall_mastery ? (
                      <Badge variant={c.overall_mastery === "mastered" ? "mastered" : "progressing"}>
                        {c.translated_grade || c.overall_mastery}
                      </Badge>
                    ) : (
                      <span className="text-xs text-(--color-text-tertiary)">in progress</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p className="text-[11px] text-(--color-text-tertiary) mt-3">
        Cumulative hours: {transcript.cumulative_hours.total_hours}h
        {Object.keys(transcript.cumulative_hours.by_subject).length > 0 &&
          ` (${Object.entries(transcript.cumulative_hours.by_subject)
            .map(([s, h]) => `${s} ${h}h`)
            .join(", ")})`}
      </p>
    </Card>
    </div>
  );
}
