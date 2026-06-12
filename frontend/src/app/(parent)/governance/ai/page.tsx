"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { aiGovernance, tutorProfile, type AIRoleSetting, type AIStatusData, type TutorProfileData, type TutorProfileEntryData } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { useToast } from "@/components/Toast";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import { cn } from "@/lib/cn";

const ROLE_LABELS: Record<string, string> = {
  planner: "Planner",
  tutor: "Tutor",
  evaluator: "Evaluator",
  advisor: "Advisor",
  cartographer: "Cartographer",
  education_architect: "Education Architect",
  content_architect: "Content Architect",
  curriculum_mapper: "Curriculum Mapper",
};

const AUTONOMY_LABELS: Record<string, string> = {
  off: "Off",
  standard: "Approve each change",
  autonomous: "Autonomous",
};

const PROVIDER_LABELS: Record<string, string> = {
  anthropic: "Claude",
  openai: "OpenAI",
  native: "Native",
  mock: "Practice mode",
};

function centsToDollars(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`;
}

const CATEGORY_LABELS: Record<string, string> = {
  explanation_style: "How to explain",
  motivation: "What motivates",
  pacing: "Pacing",
  interest: "Interests",
  other: "Other",
};

// Conservative words, never scores. These read for a parent with no
// statistics background: an honest signal, not a verdict.
const EFFICACY_LABELS: Record<string, string> = {
  working_well: "Seems to be working",
  no_clear_effect: "No clear effect yet",
  may_have_outgrown: "May have outgrown this",
  insufficient_data: "Still learning whether this helps",
};

const EFFICACY_BADGE_CLASS: Record<string, string> = {
  working_well: "bg-(--color-success-light) text-(--color-mastered) border-(--color-success)/25",
  no_clear_effect: "bg-(--color-page) text-(--color-text-secondary) border-(--color-border)",
  may_have_outgrown: "bg-(--color-warning-light)/60 text-(--color-warning) border-(--color-warning)/40",
  insufficient_data: "bg-(--color-page) text-(--color-text-tertiary) border-(--color-border)",
};

/**
 * A quiet efficacy badge on an active entry card. Tap to open the one
 * detail line, which never shows a number without the sample size it
 * came from, and always says "signal, not proof" in plain language.
 */
function EfficacyBadge({ entry }: { entry: TutorProfileEntryData }) {
  const [open, setOpen] = useState(false);
  const label = entry.efficacy_label;
  if (!label) return null;

  const word = EFFICACY_LABELS[label] || label;
  const cls = EFFICACY_BADGE_CLASS[label] || EFFICACY_BADGE_CLASS.no_clear_effect;
  const pendingRetirement = label === "may_have_outgrown" && entry.retirement_pending;

  return (
    <div className="mt-1.5">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className={cn(
          "px-2 py-0.5 rounded-full text-[10px] font-medium border transition-colors",
          cls,
        )}
        data-testid={`efficacy-badge-${entry.id}`}
        aria-expanded={open}
      >
        {word}
      </button>
      {pendingRetirement && (
        <span
          className="ml-2 px-2 py-0.5 rounded-full text-[10px] font-medium border border-(--color-warning)/40 bg-(--color-warning-light)/40 text-(--color-warning)"
          data-testid={`retirement-pending-${entry.id}`}
        >
          Retirement suggested, waiting for you
        </span>
      )}
      {open && (
        <p className="text-[10px] text-(--color-text-tertiary) mt-1" data-testid={`efficacy-detail-${entry.id}`}>
          {label === "insufficient_data" || entry.active_attempts === null || entry.baseline_attempts === null
            ? "Still learning whether this helps."
            : `Based on ${entry.active_attempts} attempts with this strategy vs ${entry.baseline_attempts} before it. This is a signal, not proof.`}
        </p>
      )}
    </div>
  );
}

function entryAppliedLine(entry: TutorProfileEntryData): string {
  const date = entry.decided_at
    ? new Date(entry.decided_at).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })
    : "";
  if (entry.grant_event_hash) {
    return `applied under your standing grant (${entry.grant_event_hash.slice(0, 12)}) ${date}`;
  }
  return `you approved on ${date}`;
}

/**
 * "How your tutor is learning": the per-child tutor memory, with the
 * parent in full control. Active entries with how they came to apply,
 * pending proposals with inline approve and reject, history collapsed.
 */
function TutorMemorySection({ tutorPolicy }: { tutorPolicy: string }) {
  const { toast } = useToast();
  const { selectedChild } = useChild();
  const [profile, setProfile] = useState<TutorProfileData | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);

  const load = () => {
    if (!selectedChild) return;
    tutorProfile.get(selectedChild.id).then(setProfile).catch(() => setProfile(null));
  };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(load, [selectedChild?.id]);

  async function act(entryId: string, action: "approve" | "reject" | "revoke") {
    if (!selectedChild) return;
    setBusy(entryId);
    try {
      if (action === "revoke") await tutorProfile.revoke(selectedChild.id, entryId);
      else await tutorProfile.decide(selectedChild.id, entryId, action);
      load();
      if (action === "approve") toast("Approved. The tutor will use this from the next session.", "success");
      if (action === "reject") toast("Rejected. The tutor will not remember this.", "info");
      if (action === "revoke") toast("Removed. The tutor stops using this immediately.", "success");
    } catch (err: unknown) {
      const detail = (err as { detail?: string })?.detail;
      toast(detail || "That didn't go through. Nothing was changed.", "error");
    } finally {
      setBusy(null);
    }
  }

  if (!selectedChild) return null;
  const history = profile ? [...profile.rejected, ...profile.revoked] : [];

  return (
    <Card className="mb-6">
      <SectionHeader title="How your tutor is learning" />
      <p className="text-xs text-(--color-text-secondary) mt-1 mb-4">
        Over time the tutor notices what works for {selectedChild.first_name}: how to explain things, what
        keeps them motivated, what pace fits. It remembers strategies, never what your child said. You decide
        every entry below.
      </p>

      {tutorPolicy === "off" && (
        <p className="text-sm text-(--color-text-secondary)" data-testid="tutor-memory-off">
          Tutor memory is off. Your tutor starts fresh every session.
        </p>
      )}

      {tutorPolicy !== "off" && profile && (
        <div className="space-y-4">
          {profile.proposed.length > 0 ? (
            <div>
              <div className="type-eyebrow-md text-(--color-text-tertiary) mb-2">Waiting for your review</div>
              <div className="space-y-2">
                {profile.proposed.map((entry) => (
                  <div key={entry.id} className="px-3 py-2.5 rounded-[10px] border border-(--color-warning)/40 bg-(--color-warning-light)/40">
                    <div className="flex items-start justify-between gap-3 flex-wrap">
                      <div className="min-w-0">
                        <span className="text-[10px] uppercase tracking-wide text-(--color-text-tertiary)">
                          {CATEGORY_LABELS[entry.category] || entry.category}
                        </span>
                        <p className="text-sm text-(--color-text)">{entry.content}</p>
                      </div>
                      <div className="flex gap-2 shrink-0">
                        <Button variant="primary" size="sm" disabled={busy === entry.id} onClick={() => act(entry.id, "approve")}>
                          Approve
                        </Button>
                        <Button variant="ghost" size="sm" disabled={busy === entry.id} onClick={() => act(entry.id, "reject")}>
                          Reject
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            tutorPolicy === "standard" && (
              <p className="text-xs text-(--color-text-tertiary)">Nothing waiting for review.</p>
            )
          )}

          {tutorPolicy === "autonomous" && (
            <p className="text-xs text-(--color-text-secondary)">
              Your standing grant is active: new entries apply immediately and are recorded in your family
              record. Switch the tutor back to Approve each change above to review entries before they apply.
            </p>
          )}

          <div>
            <div className="type-eyebrow-md text-(--color-text-tertiary) mb-2">What the tutor remembers</div>
            {profile.active.length === 0 ? (
              <p className="text-xs text-(--color-text-tertiary)">
                Nothing yet. As {selectedChild.first_name} works with the tutor, what works will land here for
                you to see.
              </p>
            ) : (
              <div className="space-y-2">
                {profile.active.map((entry) => (
                  <div key={entry.id} className="px-3 py-2.5 rounded-[10px] bg-(--color-page) border border-(--color-border)">
                    <div className="flex items-start justify-between gap-3 flex-wrap">
                      <div className="min-w-0">
                        <span className="text-[10px] uppercase tracking-wide text-(--color-text-tertiary)">
                          {CATEGORY_LABELS[entry.category] || entry.category}
                        </span>
                        <p className="text-sm text-(--color-text)">{entry.content}</p>
                        <p className="text-[10px] text-(--color-text-tertiary) mt-0.5 font-mono">
                          {entryAppliedLine(entry)}
                        </p>
                        <EfficacyBadge entry={entry} />
                      </div>
                      <Button variant="ghost" size="sm" disabled={busy === entry.id} onClick={() => act(entry.id, "revoke")}>
                        Remove
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {history.length > 0 && (
            <div>
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="text-xs text-(--color-text-tertiary) hover:text-(--color-text) underline"
              >
                {showHistory ? "Hide" : "Show"} declined and removed entries ({history.length})
              </button>
              {showHistory && (
                <div className="space-y-1.5 mt-2">
                  {history.map((entry) => (
                    <div key={entry.id} className="px-3 py-2 rounded-[10px] bg-(--color-page) opacity-70">
                      <span className="text-[10px] uppercase tracking-wide text-(--color-text-tertiary) mr-2">
                        {entry.status === "rejected" ? "Declined" : "Removed"}
                      </span>
                      <span className="text-xs text-(--color-text-secondary)">{entry.content}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </Card>
  );
}

/**
 * The AI governance panel: the parent sets exactly how long the AI's
 * leash is, per role, and can prove what it did on that leash. Policy,
 * not a switch: every change here is a hash-chained governance event.
 */
export default function AIGovernancePage() {
  useEffect(() => {
    document.title = "AI Governance | METHEAN";
  }, []);

  const { toast } = useToast();
  const [roles, setRoles] = useState<AIRoleSetting[]>([]);
  const [status, setStatus] = useState<AIStatusData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [confirmGrant, setConfirmGrant] = useState<string | null>(null);
  const [saving, setSaving] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      aiGovernance.settings().then((d) => setRoles(d.roles)),
      aiGovernance.status().then(setStatus),
    ])
      .catch((err: unknown) => {
        const detail = (err as { detail?: string })?.detail;
        setError(detail || "Couldn't load AI governance. Try again in a moment.");
      })
      .finally(() => setLoading(false));
  }, []);

  async function applyPolicy(role: string, autonomy: string) {
    const previous = roles.find((r) => r.role === role)?.autonomy;
    if (!previous || previous === autonomy) return;
    // Optimistic update with loud revert on failure.
    setSaving(role);
    setRoles((rs) => rs.map((r) => (r.role === role ? { ...r, autonomy: autonomy as AIRoleSetting["autonomy"] } : r)));
    try {
      await aiGovernance.update(role, autonomy);
      const fresh = await aiGovernance.settings();
      setRoles(fresh.roles);
      if (autonomy === "autonomous") {
        toast("Standing autonomy granted. It is recorded in your family record and revocable any time.", "info");
      } else if (previous === "autonomous") {
        toast("Autonomy revoked. The grant and its revocation are both in your family record.", "success");
      }
    } catch (err: unknown) {
      setRoles((rs) => rs.map((r) => (r.role === role ? { ...r, autonomy: previous } : r)));
      const detail = (err as { detail?: string })?.detail;
      toast(detail || `Couldn't change the ${ROLE_LABELS[role] || role} policy. Nothing was changed.`, "error");
    } finally {
      setSaving(null);
    }
  }

  function requestChange(role: string, autonomy: string) {
    if (autonomy === "autonomous") {
      // Granting requires informed confirmation. Revoking never does:
      // leaving must always be easier than granting.
      setConfirmGrant(role);
      return;
    }
    applyPolicy(role, autonomy);
  }

  if (loading) {
    return (
      <div className="max-w-4xl">
        <PageHeader title="AI Governance" subtitle="How much the AI may do, role by role." />
        <LoadingSkeleton variant="card" count={4} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl">
        <PageHeader title="AI Governance" />
        <Card borderLeft="border-l-(--color-danger)">
          <p className="text-sm text-(--color-danger)">{error}</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="AI Governance"
        subtitle="You set exactly how much the AI may do, role by role. Every change you make here is sealed into your family record."
      />

      {/* Provider chain */}
      {status && (
        <Card className="mb-6">
          <SectionHeader title="Provider Chain" />
          <div className="flex items-center gap-2 mt-3 flex-wrap" data-testid="provider-chain">
            {status.chain_order.map((provider, i) => (
              <div key={provider} className="flex items-center gap-2">
                {i > 0 && <span className="text-(--color-text-tertiary) text-xs">then</span>}
                <span
                  className={cn(
                    "px-3 py-1.5 rounded-full text-xs font-medium border",
                    provider === "native"
                      ? "bg-(--color-accent-light) text-(--color-accent) border-(--color-accent)/30"
                      : status.providers[provider]?.configured
                        ? "bg-(--color-success-light) text-(--color-mastered) border-(--color-success)/25"
                        : "bg-(--color-page) text-(--color-text-tertiary) border-(--color-border)",
                  )}
                >
                  {PROVIDER_LABELS[provider] || provider}
                  {provider !== "native" && !status.providers[provider]?.configured && " (not configured)"}
                </span>
              </div>
            ))}
          </div>
          <p className="text-xs text-(--color-text-secondary) mt-3">
            Your curriculum runs natively. AI is an enhancement, never a dependency.
          </p>
        </Card>
      )}

      {/* Role policy board */}
      <Card className="mb-6">
        <SectionHeader title="Role Policies" />
        <p className="text-xs text-(--color-text-secondary) mt-1 mb-4">
          Off means no AI calls at all for that role. Approve each change is today&apos;s METHEAN: the AI
          advises, you approve. Autonomous is a standing grant, recorded and revocable in one tap.
        </p>
        <div className="space-y-3" data-testid="role-board">
          {roles.map((role) => (
            <div
              key={role.role}
              className="px-3 py-3 rounded-[10px] bg-(--color-page) border border-(--color-border)"
              data-testid={`role-row-${role.role}`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="min-w-0">
                  <div className="text-sm font-medium text-(--color-text)">{ROLE_LABELS[role.role] || role.role}</div>
                  <p className="text-xs text-(--color-text-secondary) mt-0.5 max-w-md">{role.description}</p>
                  {role.updated_at && (
                    <p className="text-[10px] text-(--color-text-tertiary) mt-1">
                      Last changed{" "}
                      {new Date(role.updated_at).toLocaleDateString(undefined, {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </p>
                  )}
                </div>
                <div className="flex rounded-[10px] border border-(--color-border-strong) overflow-hidden shrink-0" role="group" aria-label={`${ROLE_LABELS[role.role]} autonomy`}>
                  {role.allowed.map((level) => (
                    <button
                      key={level}
                      disabled={saving === role.role}
                      onClick={() => requestChange(role.role, level)}
                      aria-pressed={role.autonomy === level}
                      className={cn(
                        "px-3 py-1.5 text-xs font-medium transition-colors min-h-[36px]",
                        role.autonomy === level
                          ? level === "off"
                            ? "bg-(--color-text-secondary) text-white"
                            : level === "autonomous"
                              ? "bg-(--color-constitutional) text-white"
                              : "bg-(--color-accent) text-white"
                          : "bg-(--color-surface) text-(--color-text-secondary) hover:bg-(--color-page)",
                      )}
                    >
                      {AUTONOMY_LABELS[level]}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <TutorMemorySection tutorPolicy={roles.find((r) => r.role === "tutor")?.autonomy || "standard"} />

      {/* Spend */}
      {status && (
        <Card className="mb-6">
          <SectionHeader title="AI Spend" />
          <div className="mt-3 flex items-baseline gap-3">
            <span className="type-heading-lg text-(--color-text)">{centsToDollars(status.today.spend_cents)}</span>
            <span className="text-xs text-(--color-text-secondary)">
              today &middot; {status.today.calls} calls &middot; {status.today.tokens.toLocaleString()} tokens
            </span>
          </div>
          <div className="mt-2 h-2 rounded-full bg-(--color-page) overflow-hidden max-w-md">
            <div
              className={cn(
                "h-full rounded-full transition-all",
                status.today.pct_tokens >= 80 ? "bg-(--color-warning)" : "bg-(--color-accent)",
              )}
              style={{ width: `${Math.min(Math.max(status.today.pct_tokens, status.today.pct_cost), 100)}%` }}
            />
          </div>
          <p className="text-[10px] text-(--color-text-tertiary) mt-1">
            Daily allowance: {status.today.daily_token_limit.toLocaleString()} tokens. When it runs out, the AI
            pauses until tomorrow; your curriculum keeps running.
          </p>

          {status.last_30_days.length > 0 && (
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-sm max-w-lg">
                <thead>
                  <tr className="text-left text-[11px] uppercase tracking-wide text-(--color-text-tertiary) border-b border-(--color-border)">
                    <th className="py-1.5 pr-4 font-medium">Role (30 days)</th>
                    <th className="py-1.5 pr-4 font-medium">Calls</th>
                    <th className="py-1.5 font-medium">Est. cost</th>
                  </tr>
                </thead>
                <tbody>
                  {status.last_30_days.map((row) => (
                    <tr key={row.role} className="border-b border-(--color-border)/60 last:border-0">
                      <td className="py-1.5 pr-4 text-(--color-text)">{ROLE_LABELS[row.role] || row.role}</td>
                      <td className="py-1.5 pr-4 text-(--color-text-secondary)">{row.calls}</td>
                      <td className="py-1.5 text-(--color-text-secondary)">{centsToDollars(row.estimated_cost_cents)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      )}

      {/* Trace link */}
      <Card>
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <div>
            <div className="text-sm font-medium text-(--color-text)">Every AI decision is on the record</div>
            <p className="text-xs text-(--color-text-secondary) mt-0.5">
              Full inputs, outputs, and the rules that applied, for every single call.
            </p>
          </div>
          <Link
            href="/governance/trace"
            className="text-sm text-(--color-accent) hover:underline font-medium shrink-0"
          >
            See every decision the AI has made
          </Link>
        </div>
      </Card>

      {/* Autonomous grant confirmation */}
      {confirmGrant && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50" role="dialog" aria-modal="true">
          <Card padding="p-6" className="w-full max-w-md mx-4 shadow-lg animate-scale-in">
            <h3 className="text-sm font-semibold text-(--color-text) mb-2">
              Grant standing autonomy to the {ROLE_LABELS[confirmGrant] || confirmGrant}?
            </h3>
            <p className="text-xs text-(--color-text-secondary) leading-relaxed mb-2">
              This lets the {ROLE_LABELS[confirmGrant]?.toLowerCase() || confirmGrant} apply its specific,
              named adjustments without asking you each time. It does not unlock anything beyond those named
              actions, and it changes nothing else about your approval settings.
            </p>
            <p className="text-xs text-(--color-text-secondary) leading-relaxed mb-4">
              Every action taken under this grant is recorded in your sealed family record, citing this exact
              grant. You can revoke it at any moment with one tap, and revoking never asks for confirmation.
            </p>
            <div className="flex gap-2 justify-end">
              <Button variant="ghost" size="sm" onClick={() => setConfirmGrant(null)}>
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={() => {
                  const role = confirmGrant;
                  setConfirmGrant(null);
                  if (role) applyPolicy(role, "autonomous");
                }}
              >
                Grant autonomy
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
