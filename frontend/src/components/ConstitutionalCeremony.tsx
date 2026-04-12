"use client";

import { useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import { cn } from "@/lib/cn";

export function ShieldIcon({ size = 16, className }: { size?: number; className?: string }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor" strokeWidth={2} className={className}>
      <path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.25C17.25 22.15 21 17.25 21 12V7l-9-5z" />
    </svg>
  );
}

interface CeremonyProps {
  mode: "create" | "amend" | "suspend";
  ruleName?: string;
  ruleType?: string;
  ruleParams?: Record<string, unknown>;
  originalReason?: string;
  createdAt?: string;
  proposedChanges?: Record<string, unknown>;
  onConfirm: (reason: string) => void;
  onCancel: () => void;
  loading?: boolean;
}

export default function ConstitutionalCeremony({
  mode, ruleName, ruleType, ruleParams, originalReason, createdAt,
  proposedChanges, onConfirm, onCancel, loading,
}: CeremonyProps) {
  const [step, setStep] = useState(mode === "suspend" ? 1 : 0);
  const [checks, setChecks] = useState([false, false, false]);
  const [reason, setReason] = useState("");

  const allChecked = checks.every(Boolean);
  const reasonValid = reason.trim().length >= 20;
  const canSubmit = mode === "create" ? allChecked && reasonValid : reasonValid;

  function toggleCheck(i: number) {
    setChecks((prev) => prev.map((v, j) => j === i ? !v : v));
  }

  function formatParams(params: Record<string, unknown>): Array<[string, string]> {
    return Object.entries(params || {}).map(([k, v]) => [
      k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
      typeof v === "boolean" ? (v ? "Yes" : "No") : Array.isArray(v) ? v.join(", ") : String(v ?? "—"),
    ]);
  }

  function computeDiff(): Array<[string, string, string]> {
    if (!proposedChanges || !ruleParams) return [];
    const diffs: Array<[string, string, string]> = [];
    for (const [key, newVal] of Object.entries(proposedChanges)) {
      const oldVal = (ruleParams as any)[key];
      if (JSON.stringify(oldVal) !== JSON.stringify(newVal)) {
        diffs.push([
          key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
          String(oldVal ?? "—"),
          String(newVal ?? "—"),
        ]);
      }
    }
    return diffs;
  }

  // ── CREATE CEREMONY ──
  if (mode === "create") {
    return (
      <div className="space-y-4">
        {/* Step 0: Declaration */}
        {step === 0 && (
          <Card borderLeft="border-l-(--color-constitutional)" className="border-l-4">
            <div className="flex items-start gap-3">
              <ShieldIcon size={24} className="text-(--color-constitutional) shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-bold text-(--color-constitutional) mb-2">You are creating a CONSTITUTIONAL RULE.</h3>
                <p className="text-xs text-(--color-text-secondary) leading-relaxed">
                  Constitutional rules are your family&apos;s foundational governance principles. They are protected by ceremony:
                  once created, they cannot be deleted and require documented justification to modify.
                  This rule will be permanently recorded in your governance history.
                </p>
                <div className="flex gap-2 mt-4">
                  <Button variant="primary" size="sm" onClick={() => setStep(1)}
                    className="bg-(--color-constitutional) hover:opacity-90">I understand — proceed</Button>
                  <Button variant="ghost" size="sm" onClick={onCancel}>Cancel</Button>
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Step 1: Review */}
        {step === 1 && (
          <>
            <Card borderLeft="border-l-(--color-constitutional)" className="border-l-4" padding="p-6">
              <div className="text-[10px] font-bold text-(--color-constitutional) uppercase tracking-widest mb-3">
                Proposed Constitutional Rule
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-(--color-text-secondary)">Name</span>
                  <span className="font-medium text-(--color-text)">{ruleName}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-(--color-text-secondary)">Type</span>
                  <span className="font-medium text-(--color-text) capitalize">{ruleType?.replace(/_/g, " ")}</span>
                </div>
                {ruleParams && formatParams(ruleParams).map(([label, value]) => (
                  <div key={label} className="flex justify-between text-xs">
                    <span className="text-(--color-text-secondary)">{label}</span>
                    <span className="font-medium text-(--color-text)">{value}</span>
                  </div>
                ))}
              </div>
              <div className="mt-3 pt-3 border-t border-(--color-border) text-[10px] text-(--color-text-tertiary)">
                This rule will take effect immediately and cannot be deleted.
              </div>
            </Card>
            <Button variant="primary" size="sm" onClick={() => setStep(2)}
              className="bg-(--color-constitutional) hover:opacity-90">Continue to affirmation</Button>
          </>
        )}

        {/* Step 2: Affirmation */}
        {step === 2 && (
          <Card borderLeft="border-l-(--color-constitutional)" className="border-l-4" padding="p-6">
            <div className="text-xs font-medium text-(--color-text) mb-4">I understand that:</div>
            <div className="space-y-3 mb-5">
              {[
                "This rule becomes a permanent part of my family's governance framework",
                "It cannot be deleted, only suspended with documented justification",
                "Modifying it will require a formal amendment process",
              ].map((text, i) => (
                <label key={i} className="flex items-start gap-2.5 text-xs text-(--color-text-secondary) cursor-pointer">
                  <input type="checkbox" checked={checks[i]} onChange={() => toggleCheck(i)}
                    className="mt-0.5 rounded border-(--color-constitutional)" />
                  {text}
                </label>
              ))}
            </div>
            <div className="mb-4">
              <label className="block text-xs font-medium text-(--color-text) mb-1.5">
                Reason for establishing this principle:
              </label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Explain why this is foundational to your family's education. (minimum 20 characters)"
                className="w-full h-20 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface) text-(--color-text)"
              />
              {reason.length > 0 && reason.length < 20 && (
                <p className="text-[10px] text-(--color-danger) mt-1">{20 - reason.length} more characters needed</p>
              )}
            </div>
            <div className="flex gap-2">
              <Button
                disabled={!canSubmit || loading}
                onClick={() => onConfirm(reason)}
                className="bg-(--color-constitutional) text-white hover:opacity-90 disabled:opacity-40"
                size="md"
              >
                {loading ? "Establishing..." : "Establish Constitutional Rule"}
              </Button>
              <Button variant="ghost" size="sm" onClick={onCancel}>Cancel</Button>
            </div>
          </Card>
        )}
      </div>
    );
  }

  // ── AMEND CEREMONY ──
  if (mode === "amend") {
    const diffs = computeDiff();
    return (
      <div className="space-y-4">
        {step === 0 && (
          <>
            {/* Current rule */}
            <Card borderLeft="border-l-(--color-constitutional)" className="border-l-4" padding="p-5">
              <div className="flex items-center gap-2 mb-3">
                <ShieldIcon size={16} className="text-(--color-constitutional)" />
                <span className="text-[10px] font-bold text-(--color-constitutional) uppercase tracking-widest">Current Constitutional Rule</span>
                {createdAt && <span className="text-[10px] text-(--color-text-tertiary)">Established {new Date(createdAt).toLocaleDateString()}</span>}
              </div>
              <div className="text-sm font-medium text-(--color-text) mb-2">{ruleName}</div>
              {ruleParams && formatParams(ruleParams).map(([label, value]) => (
                <div key={label} className="flex justify-between text-xs py-0.5">
                  <span className="text-(--color-text-secondary)">{label}</span>
                  <span className="text-(--color-text)">{value}</span>
                </div>
              ))}
            </Card>

            {/* Amendment summary */}
            {diffs.length > 0 && (
              <Card padding="p-4" className="bg-(--color-warning-light) border-(--color-warning)/20">
                <div className="text-xs font-medium text-(--color-warning) mb-2">Amendment Summary</div>
                {diffs.map(([field, oldVal, newVal]) => (
                  <div key={field} className="text-xs text-(--color-text-secondary) py-0.5">
                    <span className="font-medium">{field}:</span>{" "}
                    <span className="line-through text-(--color-danger)">{oldVal}</span>{" → "}
                    <span className="font-medium text-(--color-success)">{newVal}</span>
                  </div>
                ))}
              </Card>
            )}
            <Button variant="primary" size="sm" onClick={() => setStep(1)}
              className="bg-(--color-constitutional) hover:opacity-90">Continue to justification</Button>
          </>
        )}

        {step === 1 && (
          <Card borderLeft="border-l-(--color-constitutional)" className="border-l-4" padding="p-6">
            <div className="flex items-center gap-2 mb-3">
              <ShieldIcon size={16} className="text-(--color-constitutional)" />
              <span className="text-xs font-bold text-(--color-constitutional)">Constitutional Amendment</span>
            </div>
            <p className="text-xs text-(--color-text-secondary) mb-4">
              You are modifying a foundational governance principle. This change will be permanently recorded.
            </p>
            <div className="mb-4">
              <label className="block text-xs font-medium text-(--color-text) mb-1.5">Reason for this amendment:</label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Explain why this change is necessary. (minimum 20 characters)"
                className="w-full h-20 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface) text-(--color-text)"
              />
              {reason.length > 0 && reason.length < 20 && (
                <p className="text-[10px] text-(--color-danger) mt-1">{20 - reason.length} more characters needed</p>
              )}
            </div>
            <div className="flex gap-2">
              <Button disabled={!reasonValid || loading} onClick={() => onConfirm(reason)}
                className="bg-(--color-constitutional) text-white hover:opacity-90 disabled:opacity-40" size="md">
                {loading ? "Ratifying..." : "Ratify Amendment"}
              </Button>
              <Button variant="ghost" size="sm" onClick={onCancel}>Cancel</Button>
            </div>
          </Card>
        )}
      </div>
    );
  }

  // ── SUSPEND CEREMONY ──
  return (
    <Card borderLeft="border-l-(--color-warning)" className="border-l-4" padding="p-6">
      <div className="flex items-center gap-2 mb-3">
        <ShieldIcon size={16} className="text-(--color-warning)" />
        <span className="text-xs font-bold text-(--color-warning)">Suspending Constitutional Rule</span>
      </div>
      <p className="text-xs text-(--color-text-secondary) mb-2">
        This rule was established{createdAt ? ` on ${new Date(createdAt).toLocaleDateString()}` : ""}
        {originalReason ? " with the following justification:" : "."}
      </p>
      {originalReason && (
        <div className="bg-(--color-page) rounded-[10px] px-3 py-2 mb-3 text-xs text-(--color-text) italic">
          "{originalReason}"
        </div>
      )}
      <p className="text-xs text-(--color-text-secondary) mb-4">
        Suspending does not delete the rule. It suspends enforcement. The rule and its full history remain in your governance record.
      </p>
      <div className="mb-4">
        <label className="block text-xs font-medium text-(--color-text) mb-1.5">Reason for suspending this principle:</label>
        <textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Explain your reason. (minimum 20 characters)"
          className="w-full h-20 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface) text-(--color-text)"
        />
        {reason.length > 0 && reason.length < 20 && (
          <p className="text-[10px] text-(--color-danger) mt-1">{20 - reason.length} more characters needed</p>
        )}
      </div>
      <div className="flex gap-2">
        <Button disabled={!reasonValid || loading} onClick={() => onConfirm(reason)}
          variant="danger" size="md">
          {loading ? "Suspending..." : "Suspend Rule"}
        </Button>
        <Button variant="ghost" size="sm" onClick={onCancel}>Cancel</Button>
      </div>
    </Card>
  );
}
