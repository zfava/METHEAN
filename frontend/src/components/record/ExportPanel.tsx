"use client";

import { useCallback, useEffect, useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import HashLine from "@/components/record/HashLine";
import { familyRecord, type RecordExportListItem, type RecordExportResult } from "@/lib/api";

/**
 * Sealed-bundle export: plain-language explainer, one button, then
 * the download link, the bundle seal, and the export history. Every
 * export is also written into the family's permanent record.
 */
export default function ExportPanel({ childId, childName }: { childId: string; childName: string }) {
  const [history, setHistory] = useState<RecordExportListItem[]>([]);
  const [result, setResult] = useState<RecordExportResult | null>(null);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState("");

  const loadHistory = useCallback(() => {
    familyRecord.listExports().then(setHistory).catch(() => {});
  }, []);

  useEffect(loadHistory, [loadHistory]);

  async function runExport() {
    setExporting(true);
    setError("");
    try {
      const r = await familyRecord.exportBundle(childId);
      setResult(r);
      loadHistory();
    } catch (err: unknown) {
      const detail = (err as { detail?: string })?.detail;
      setError(detail || "The export didn't complete. Try again in a moment.");
    } finally {
      setExporting(false);
    }
  }

  return (
    <div data-testid="export-panel">
    <Card className="mb-6">
      <SectionHeader title="Export Sealed Record" />
      <p className="text-xs text-(--color-text-secondary) mt-2 mb-4 max-w-xl">
        Produces a single file containing {childName}&apos;s full record: the transcript, every mastery claim
        with its evidence, attendance, and the documents schools ask for. The bundle is sealed: it carries a
        verification fingerprint tied to your family&apos;s decision history, so anyone you hand it to can
        confirm nothing was altered after export.
      </p>

      <div className="flex items-center gap-3 flex-wrap">
        <Button variant="primary" size="sm" onClick={runExport} disabled={exporting}>
          {exporting ? "Sealing record..." : "Export Sealed Record"}
        </Button>
        {error && <span className="text-xs text-(--color-danger)">{error}</span>}
      </div>

      {result && (
        <div
          data-testid="export-result"
          className="mt-4 px-4 py-3 rounded-[10px] bg-(--color-success-light) border border-(--color-success)/25 animate-fade-up"
        >
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div className="text-sm font-medium text-(--color-mastered)">Sealed bundle ready</div>
            {result.download_url && (
              <a
                href={result.download_url}
                className="text-sm text-(--color-accent) hover:underline font-medium"
                download
              >
                Download bundle
              </a>
            )}
          </div>
          <div className="mt-2">
            <HashLine value={result.bundle_hash} label="bundle seal" chars={16} />
          </div>
          {result.skipped_documents.length > 0 && (
            <p className="text-[11px] text-(--color-text-tertiary) mt-2">
              Not included: {result.skipped_documents.map((s) => `${s.name.replace(".pdf", "")} (${s.reason})`).join("; ")}
            </p>
          )}
        </div>
      )}

      <div className="mt-5">
        <div className="type-eyebrow-md text-(--color-text-tertiary) mb-2">Past exports</div>
        {history.length === 0 ? (
          <p className="text-xs text-(--color-text-tertiary)">
            No exports yet. Each export is dated, sealed, and remembered here.
          </p>
        ) : (
          <div data-testid="export-history" className="space-y-1.5">
            {history.map((h) => (
              <div
                key={h.artifact_id}
                className="flex items-center justify-between gap-3 px-3 py-2 rounded-[10px] bg-(--color-page) flex-wrap"
              >
                <span className="text-xs text-(--color-text-secondary)">
                  {h.created_at
                    ? new Date(h.created_at).toLocaleDateString(undefined, {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })
                    : "Unknown date"}
                </span>
                {h.bundle_hash && <HashLine value={h.bundle_hash} />}
              </div>
            ))}
          </div>
        )}
      </div>
    </Card>
    </div>
  );
}
