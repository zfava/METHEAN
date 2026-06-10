"use client";

import { useEffect, useState } from "react";
import { familyRecord, type FamilyRecordData, type RecordMasteryEvidence } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";
import IntegrityBadge from "@/components/record/IntegrityBadge";
import SummaryBand from "@/components/record/SummaryBand";
import MasteryTimeline from "@/components/record/MasteryTimeline";
import EvidenceDrawer from "@/components/record/EvidenceDrawer";
import TranscriptTable from "@/components/record/TranscriptTable";
import ExportPanel from "@/components/record/ExportPanel";

/**
 * The Family Record: the page that answers "will this count."
 * Everything rendered here comes from the family-record endpoints;
 * nothing is computed client-side beyond grouping and counting what
 * the record already contains.
 */
export default function FamilyRecordPage() {
  useEffect(() => {
    document.title = "Family Record | METHEAN";
  }, []);

  const { selectedChild } = useChild();
  const [record, setRecord] = useState<FamilyRecordData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedEvidence, setSelectedEvidence] = useState<RecordMasteryEvidence | null>(null);

  useEffect(() => {
    if (!selectedChild) return;
    setLoading(true);
    setError("");
    setRecord(null);
    familyRecord
      .get(selectedChild.id)
      .then(setRecord)
      .catch((err: unknown) => {
        const detail = (err as { detail?: string })?.detail;
        setError(detail || "Couldn't load the record. Try again in a moment.");
      })
      .finally(() => setLoading(false));
  }, [selectedChild]);

  if (!selectedChild) {
    return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;
  }

  if (loading) {
    // Reserve the page's real shape so data load causes no layout shift.
    return (
      <div className="max-w-5xl">
        <PageHeader title="Family Record" subtitle="The cumulative, evidence-backed record." />
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-6">
          <LoadingSkeleton variant="card" count={5} />
        </div>
        <LoadingSkeleton variant="list" count={6} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-5xl">
        <PageHeader title="Family Record" />
        <Card borderLeft="border-l-(--color-danger)">
          <p className="text-sm text-(--color-danger)">{error}</p>
        </Card>
      </div>
    );
  }

  if (!record) return null;

  return (
    <div className="max-w-5xl">
      <PageHeader
        title="Family Record"
        subtitle={`${selectedChild.first_name}'s cumulative record: every mastered skill, the evidence behind it, and the seal that proves nothing was rewritten.`}
        actions={
          <IntegrityBadge
            verified={record.integrity.chain_verified}
            headHash={record.integrity.head_hash}
            eventCount={record.integrity.event_count}
          />
        }
      />

      <SummaryBand record={record} />

      <div className="mb-6">
        <SectionHeader title="Mastery Timeline" />
        <p className="text-xs text-(--color-text-secondary) mt-1 mb-3">
          Every skill {selectedChild.first_name} has proven, newest first. Open any entry to see the work,
          the assessment, and the decision that sealed it.
        </p>
        <MasteryTimeline evidence={record.mastery_evidence} onSelect={setSelectedEvidence} />
      </div>

      <TranscriptTable transcript={record.transcript} />

      <ExportPanel childId={selectedChild.id} childName={selectedChild.first_name} />

      <EvidenceDrawer item={selectedEvidence} onClose={() => setSelectedEvidence(null)} />
    </div>
  );
}
