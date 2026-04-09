"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceRule } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import ConstitutionalCeremony, { ShieldIcon } from "@/components/ConstitutionalCeremony";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import EmptyState from "@/components/ui/EmptyState";
import StatusBadge from "@/components/StatusBadge";
import { cn } from "@/lib/cn";

// ── Humanize rule parameters ──

function humanize(rule: GovernanceRule): string {
  const p = rule.parameters as Record<string, unknown>;
  switch (rule.rule_type) {
    case "pace_limit": {
      const mins = Number(p.max_daily_minutes || 240);
      return mins >= 60 && mins % 60 === 0
        ? `No more than ${mins / 60} hours of learning per day`
        : `No more than ${mins} minutes of learning per day`;
    }
    case "approval_required":
      if (p.action === "auto_approve" && p.max_difficulty)
        return `Activities under difficulty ${p.max_difficulty} are auto-approved`;
      if (p.action === "require_review" && p.min_difficulty)
        return `Activities at difficulty ${p.min_difficulty}+ require your review`;
      return "Requires your approval for activities";
    case "schedule_constraint":
      return p.allowed_days ? `Learning on ${(p.allowed_days as string[]).join(", ")} only` : "Schedule constraints active";
    case "content_filter":
      return p.topic ? `"${p.topic}": ${(p.stance as string || "filtered").replace(/_/g, " ")}` : "Content filtering active";
    case "ai_boundary":
      return `AI transparency: ${p.ai_transparency || "full"}`;
    default:
      return rule.description || "Rule active";
  }
}

const RULE_TYPES = [
  { value: "approval_required", label: "Approval Rules", desc: "Control which activities need your review", icon: "🛡️" },
  { value: "pace_limit", label: "Pace Limits", desc: "Set daily and weekly time boundaries", icon: "⏱️" },
  { value: "content_filter", label: "Content Filters", desc: "Manage topics and content boundaries", icon: "📋" },
  { value: "schedule_constraint", label: "Schedule Constraints", desc: "Define when learning can happen", icon: "📅" },
  { value: "ai_boundary", label: "AI Boundaries", desc: "Control what the AI can and cannot do", icon: "🤖" },
];

const DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
const ACTIVITY_TYPES = ["lesson", "practice", "assessment", "review", "project", "field_trip"];
const AI_ROLES = ["planner", "tutor", "evaluator", "advisor", "cartographer", "education_architect", "content_architect", "curriculum_mapper"];

type BuilderStep = null | "type" | "tier" | "params" | "details" | "review";

export default function RulesPage() {
  useEffect(() => { document.title = "Rules | METHEAN"; }, []);

  const { children: allChildren } = useChild();
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Builder state
  const [step, setStep] = useState<BuilderStep>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [ruleType, setRuleType] = useState("");
  const [ruleTier, setRuleTier] = useState<"policy" | "constitutional">("policy");
  const [ruleName, setRuleName] = useState("");
  const [ruleDesc, setRuleDesc] = useState("");
  const [ruleScope, setRuleScope] = useState<"household" | "child">("household");
  const [ruleScopeId, setRuleScopeId] = useState("");
  const [effectiveFrom, setEffectiveFrom] = useState("");
  const [effectiveUntil, setEffectiveUntil] = useState("");
  const [confirmConstitutional, setConfirmConstitutional] = useState(false);
  const [saving, setSaving] = useState(false);
  const [ceremonyMode, setCeremonyMode] = useState<"create" | "amend" | "suspend" | null>(null);
  const [ceremonyRuleId, setCeremonyRuleId] = useState<string | null>(null);

  // Type-specific params
  const [pMaxDaily, setPMaxDaily] = useState(240);
  const [pMaxWeekly, setPMaxWeekly] = useState(1200);
  const [pBreakAfter, setPBreakAfter] = useState(90);
  const [pEnforce, setPEnforce] = useState<"hard" | "soft">("soft");
  const [pMaxDiff, setPMaxDiff] = useState(3);
  const [pMinDiff, setPMinDiff] = useState(3);
  const [pApprovalAction, setPApprovalAction] = useState("require_review");
  const [pActivityTypes, setPActivityTypes] = useState<string[]>([]);
  const [pTopic, setPTopic] = useState("");
  const [pStance, setPStance] = useState("exclude");
  const [pContentNotes, setPContentNotes] = useState("");
  const [pAllowedDays, setPAllowedDays] = useState<string[]>(DAYS.slice(0, 5));
  const [pStartTime, setPStartTime] = useState("08:00");
  const [pEndTime, setPEndTime] = useState("15:00");
  const [pTransparency, setPTransparency] = useState("full");
  const [pAiDirectAction, setPAiDirectAction] = useState(false);
  const [pMaxAiCalls, setPMaxAiCalls] = useState(50);
  const [pAllowedRoles, setPAllowedRoles] = useState<string[]>(AI_ROLES.slice(0, 4));

  useEffect(() => { loadRules(); }, []);

  async function loadRules() {
    setLoading(true);
    setError("");
    try {
      const d = await governance.rules();
      setRules((d as any).items || d);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load rules.");
    } finally {
      setLoading(false);
    }
  }

  function resetBuilder() {
    setStep(null); setEditingId(null); setRuleType(""); setRuleTier("policy");
    setRuleName(""); setRuleDesc(""); setRuleScope("household"); setRuleScopeId("");
    setEffectiveFrom(""); setEffectiveUntil(""); setConfirmConstitutional(false);
    setPMaxDaily(240); setPMaxWeekly(1200); setPBreakAfter(90); setPEnforce("soft");
    setPMaxDiff(3); setPMinDiff(3); setPApprovalAction("require_review"); setPActivityTypes([]);
    setPTopic(""); setPStance("exclude"); setPContentNotes("");
    setPAllowedDays(DAYS.slice(0, 5)); setPStartTime("08:00"); setPEndTime("15:00");
    setPTransparency("full"); setPAiDirectAction(false); setPMaxAiCalls(50);
    setPAllowedRoles(AI_ROLES.slice(0, 4));
  }

  function buildParams(): object {
    switch (ruleType) {
      case "pace_limit":
        return { max_daily_minutes: pMaxDaily, max_weekly_minutes: pMaxWeekly, break_after_minutes: pBreakAfter, enforce: pEnforce };
      case "approval_required":
        return { max_difficulty: pMaxDiff, min_difficulty: pMinDiff, action: pApprovalAction, activity_types: pActivityTypes.length > 0 ? pActivityTypes : undefined };
      case "content_filter":
        return { topic: pTopic, stance: pStance, notes: pContentNotes || undefined };
      case "schedule_constraint":
        return { allowed_days: pAllowedDays, start_time: pStartTime, end_time: pEndTime, enforce: pEnforce };
      case "ai_boundary":
        return { ai_transparency: pTransparency, ai_direct_action: pAiDirectAction, require_human_review: !pAiDirectAction, max_ai_calls_per_day: pMaxAiCalls, allowed_roles: pAllowedRoles };
      default: return {};
    }
  }

  function autoName(): string {
    switch (ruleType) {
      case "pace_limit": return `${pMaxDaily} min/day pace limit`;
      case "approval_required": return `Review activities at difficulty ${pMinDiff}+`;
      case "content_filter": return `Content filter: ${pTopic}`;
      case "schedule_constraint": return `Schedule: ${pAllowedDays.length} days`;
      case "ai_boundary": return `AI boundary: ${pTransparency} transparency`;
      default: return "New rule";
    }
  }

  async function saveRule() {
    setSaving(true);
    setError("");
    try {
      const payload: any = {
        rule_type: ruleType,
        tier: ruleTier,
        scope: ruleScope,
        scope_id: ruleScope === "child" && ruleScopeId ? ruleScopeId : undefined,
        name: ruleName || autoName(),
        description: ruleDesc || undefined,
        parameters: buildParams(),
        effective_from: effectiveFrom || undefined,
        effective_until: effectiveUntil || undefined,
        confirm_constitutional: ruleTier === "constitutional" ? confirmConstitutional : undefined,
      };
      if (editingId) {
        await governance.updateRule(editingId, payload);
      } else {
        await governance.createRule(payload);
      }
      resetBuilder();
      await loadRules();
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't save rule.");
    } finally {
      setSaving(false);
    }
  }

  async function deleteRule(id: string) {
    if (!confirm("Delete this rule? This cannot be undone.")) return;
    try {
      await governance.deleteRule(id);
      await loadRules();
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't delete rule.");
    }
  }

  function startEdit(rule: GovernanceRule) {
    setEditingId(rule.id);
    setRuleType(rule.rule_type);
    setRuleTier((rule as any).tier || "policy");
    setRuleName(rule.name);
    setRuleDesc(rule.description || "");
    setRuleScope(rule.scope as any || "household");
    const p = rule.parameters as any;
    if (rule.rule_type === "pace_limit") {
      setPMaxDaily(p.max_daily_minutes ?? 240);
      setPMaxWeekly(p.max_weekly_minutes ?? 1200);
      setPBreakAfter(p.break_after_minutes ?? 90);
      setPEnforce(p.enforce ?? "soft");
    } else if (rule.rule_type === "approval_required") {
      setPMaxDiff(p.max_difficulty ?? 3); setPMinDiff(p.min_difficulty ?? 3);
      setPApprovalAction(p.action ?? "require_review");
      setPActivityTypes(p.activity_types ?? []);
    } else if (rule.rule_type === "content_filter") {
      setPTopic(p.topic ?? ""); setPStance(p.stance ?? "exclude"); setPContentNotes(p.notes ?? "");
    } else if (rule.rule_type === "schedule_constraint") {
      setPAllowedDays(p.allowed_days ?? DAYS.slice(0, 5));
      setPStartTime(p.start_time ?? "08:00"); setPEndTime(p.end_time ?? "15:00");
      setPEnforce(p.enforce ?? "soft");
    } else if (rule.rule_type === "ai_boundary") {
      setPTransparency(p.ai_transparency ?? "full");
      setPAiDirectAction(p.ai_direct_action ?? false);
      setPMaxAiCalls(p.max_ai_calls_per_day ?? 50);
      setPAllowedRoles(p.allowed_roles ?? AI_ROLES.slice(0, 4));
    }
    setStep("params");
  }

  function toggleArrayItem(arr: string[], item: string, setter: (v: string[]) => void) {
    setter(arr.includes(item) ? arr.filter((x) => x !== item) : [...arr, item]);
  }

  if (loading) return <div className="max-w-4xl"><PageHeader title="Governance Rules" /><LoadingSkeleton variant="list" count={5} /></div>;

  const constitutional = rules.filter((r) => (r as any).tier === "constitutional");
  const policy = rules.filter((r) => (r as any).tier !== "constitutional");

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Governance Rules"
        subtitle="You set these. You can change them anytime."
        actions={!step && <Button variant="primary" size="sm" onClick={() => setStep("type")}>Add Rule</Button>}
      />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); loadRules(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── RULE BUILDER ── */}
      {step && (
        <Card className="mb-6" padding="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-(--color-text)">{editingId ? "Edit Rule" : "Create Rule"}</h3>
            <Button variant="ghost" size="sm" onClick={resetBuilder}>Cancel</Button>
          </div>

          {/* Step: Choose Type */}
          {step === "type" && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {RULE_TYPES.map((rt) => (
                <button key={rt.value} onClick={() => { setRuleType(rt.value); setStep("tier"); }}
                  className="text-left p-4 rounded-[14px] border border-(--color-border) hover:border-(--color-accent) transition-colors">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg">{rt.icon}</span>
                    <span className="text-sm font-medium text-(--color-text)">{rt.label}</span>
                  </div>
                  <p className="text-xs text-(--color-text-secondary)">{rt.desc}</p>
                </button>
              ))}
            </div>
          )}

          {/* Step: Choose Tier */}
          {step === "tier" && (
            <div className="space-y-3">
              <button onClick={() => { setRuleTier("policy"); setStep("params"); }}
                className="w-full text-left p-4 rounded-[14px] border border-(--color-border) hover:border-(--color-accent) transition-colors">
                <span className="text-sm font-medium text-(--color-text)">Policy Rule</span>
                <p className="text-xs text-(--color-text-secondary) mt-0.5">Normal rule. Can be changed anytime.</p>
              </button>
              <button onClick={() => { setRuleTier("constitutional"); setStep("params"); }}
                className="w-full text-left p-4 rounded-[14px] border-2 border-(--color-constitutional)/30 hover:border-(--color-constitutional) transition-colors">
                <div className="flex items-center gap-2">
                  <span className="text-lg">🛡️</span>
                  <span className="text-sm font-medium text-(--color-constitutional)">Constitutional Rule</span>
                </div>
                <p className="text-xs text-(--color-text-secondary) mt-0.5">Foundational principle. Requires ceremony to change.</p>
              </button>
              <Button variant="ghost" size="sm" onClick={() => setStep("type")}>&larr; Back</Button>
            </div>
          )}

          {/* Step: Parameters */}
          {step === "params" && (
            <div className="space-y-4">
              <div className="text-xs text-(--color-text-tertiary) mb-2">
                {RULE_TYPES.find((t) => t.value === ruleType)?.icon} {RULE_TYPES.find((t) => t.value === ruleType)?.label}
                {ruleTier === "constitutional" && <StatusBadge status="constitutional" className="ml-2" />}
              </div>

              {ruleType === "pace_limit" && (
                <>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Maximum daily minutes</label>
                    <input type="number" value={pMaxDaily} onChange={(e) => setPMaxDaily(Number(e.target.value))} min={0} max={1440}
                      className="w-32 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Maximum weekly minutes</label>
                    <input type="number" value={pMaxWeekly} onChange={(e) => setPMaxWeekly(Number(e.target.value))} min={0}
                      className="w-32 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Suggest break after (minutes)</label>
                    <input type="number" value={pBreakAfter} onChange={(e) => setPBreakAfter(Number(e.target.value))} min={0}
                      className="w-32 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Enforcement</label>
                    <div className="flex gap-2">
                      {(["hard", "soft"] as const).map((v) => (
                        <button key={v} onClick={() => setPEnforce(v)}
                          className={cn("px-4 py-2 text-xs rounded-[10px] border capitalize", pEnforce === v ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)" : "border-(--color-border)")}>
                          {v} {v === "hard" ? "(block)" : "(warn)"}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {ruleType === "approval_required" && (
                <>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Auto-approve below difficulty</label>
                    <input type="range" min={1} max={5} value={pMaxDiff} onChange={(e) => setPMaxDiff(Number(e.target.value))}
                      className="w-48" />
                    <span className="ml-2 text-sm text-(--color-text)">{pMaxDiff}</span>
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Require review at or above</label>
                    <input type="range" min={1} max={5} value={pMinDiff} onChange={(e) => setPMinDiff(Number(e.target.value))}
                      className="w-48" />
                    <span className="ml-2 text-sm text-(--color-text)">{pMinDiff}</span>
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Activity types (empty = all)</label>
                    <div className="flex flex-wrap gap-2">
                      {ACTIVITY_TYPES.map((at) => (
                        <button key={at} onClick={() => toggleArrayItem(pActivityTypes, at, setPActivityTypes)}
                          className={cn("px-3 py-1.5 text-xs rounded-[10px] border capitalize", pActivityTypes.includes(at) ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                          {at.replace(/_/g, " ")}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {ruleType === "content_filter" && (
                <>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Topic *</label>
                    <input value={pTopic} onChange={(e) => setPTopic(e.target.value)} placeholder="e.g., evolution, violence"
                      className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Stance</label>
                    <select value={pStance} onChange={(e) => setPStance(e.target.value)}
                      className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)">
                      <option value="exclude">Exclude entirely</option>
                      <option value="present_alternative">Present alternatives</option>
                      <option value="parent_led_only">Parent-led discussion only</option>
                      <option value="age_appropriate">Age-appropriate only</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Notes for AI</label>
                    <textarea value={pContentNotes} onChange={(e) => setPContentNotes(e.target.value)}
                      placeholder="Additional guidance for the AI..."
                      className="w-full h-16 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface)" />
                  </div>
                </>
              )}

              {ruleType === "schedule_constraint" && (
                <>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Allowed days</label>
                    <div className="flex flex-wrap gap-2">
                      {DAYS.map((d) => (
                        <button key={d} onClick={() => toggleArrayItem(pAllowedDays, d, setPAllowedDays)}
                          className={cn("w-10 h-10 text-xs rounded-[10px] border capitalize", pAllowedDays.includes(d) ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                          {d.slice(0, 2)}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div>
                      <label className="block text-xs text-(--color-text-secondary) mb-1">Start time</label>
                      <input type="time" value={pStartTime} onChange={(e) => setPStartTime(e.target.value)}
                        className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                    </div>
                    <div>
                      <label className="block text-xs text-(--color-text-secondary) mb-1">End time</label>
                      <input type="time" value={pEndTime} onChange={(e) => setPEndTime(e.target.value)}
                        className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Enforcement</label>
                    <div className="flex gap-2">
                      {(["hard", "soft"] as const).map((v) => (
                        <button key={v} onClick={() => setPEnforce(v)}
                          className={cn("px-4 py-2 text-xs rounded-[10px] border capitalize", pEnforce === v ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                          {v}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {ruleType === "ai_boundary" && (
                <>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Transparency level</label>
                    <div className="flex gap-2">
                      {(["full", "summary", "minimal"] as const).map((v) => (
                        <button key={v} onClick={() => setPTransparency(v)}
                          className={cn("px-4 py-2 text-xs rounded-[10px] border capitalize", pTransparency === v ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                          {v}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <label className="text-xs text-(--color-text-secondary)">AI can act without review</label>
                    <button onClick={() => setPAiDirectAction(!pAiDirectAction)}
                      className={cn("w-10 h-6 rounded-full transition-colors", pAiDirectAction ? "bg-(--color-accent)" : "bg-(--color-border)")}>
                      <div className={cn("w-4 h-4 rounded-full bg-white transition-transform mx-1", pAiDirectAction ? "translate-x-4" : "")} />
                    </button>
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Max AI calls per day</label>
                    <input type="number" value={pMaxAiCalls} onChange={(e) => setPMaxAiCalls(Number(e.target.value))} min={1}
                      className="w-32 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                  </div>
                  <div>
                    <label className="block text-xs text-(--color-text-secondary) mb-1">Allowed AI roles</label>
                    <div className="flex flex-wrap gap-2">
                      {AI_ROLES.map((role) => (
                        <button key={role} onClick={() => toggleArrayItem(pAllowedRoles, role, setPAllowedRoles)}
                          className={cn("px-3 py-1.5 text-xs rounded-[10px] border capitalize", pAllowedRoles.includes(role) ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                          {role.replace(/_/g, " ")}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}

              <div className="flex gap-2 pt-2">
                <Button variant="primary" size="sm" onClick={() => setStep("details")}>Continue</Button>
                {!editingId && <Button variant="ghost" size="sm" onClick={() => setStep("tier")}>&larr; Back</Button>}
              </div>
            </div>
          )}

          {/* Step: Name and Scope */}
          {step === "details" && (
            <div className="space-y-4">
              <div>
                <label className="block text-xs text-(--color-text-secondary) mb-1">Rule name</label>
                <input value={ruleName} onChange={(e) => setRuleName(e.target.value)} placeholder={autoName()}
                  className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
              </div>
              <div>
                <label className="block text-xs text-(--color-text-secondary) mb-1">Description (optional)</label>
                <textarea value={ruleDesc} onChange={(e) => setRuleDesc(e.target.value)} placeholder="What does this rule do?"
                  className="w-full h-16 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface)" />
              </div>
              <div>
                <label className="block text-xs text-(--color-text-secondary) mb-1">Scope</label>
                <div className="flex gap-2">
                  <button onClick={() => setRuleScope("household")}
                    className={cn("px-4 py-2 text-xs rounded-[10px] border", ruleScope === "household" ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                    Entire household
                  </button>
                  <button onClick={() => setRuleScope("child")}
                    className={cn("px-4 py-2 text-xs rounded-[10px] border", ruleScope === "child" ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)")}>
                    Specific child
                  </button>
                </div>
                {ruleScope === "child" && allChildren.length > 0 && (
                  <select value={ruleScopeId} onChange={(e) => setRuleScopeId(e.target.value)}
                    className="mt-2 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)">
                    <option value="">Select child...</option>
                    {allChildren.map((c) => <option key={c.id} value={c.id}>{c.first_name}</option>)}
                  </select>
                )}
              </div>
              <div className="flex gap-4">
                <div>
                  <label className="block text-xs text-(--color-text-secondary) mb-1">Effective from (optional)</label>
                  <input type="date" value={effectiveFrom} onChange={(e) => setEffectiveFrom(e.target.value)}
                    className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                </div>
                <div>
                  <label className="block text-xs text-(--color-text-secondary) mb-1">Effective until (optional)</label>
                  <input type="date" value={effectiveUntil} onChange={(e) => setEffectiveUntil(e.target.value)}
                    className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                </div>
              </div>

              {/* Constitutional: launch ceremony instead of direct create */}
              {ruleTier === "constitutional" && !ceremonyMode && (
                <div className="flex gap-2 pt-2">
                  <Button size="sm" onClick={() => setCeremonyMode(editingId ? "amend" : "create")}
                    className="bg-(--color-constitutional) text-white hover:opacity-90"
                    disabled={ruleType === "content_filter" && !pTopic}>
                    {editingId ? "Begin Amendment" : "Begin Constitutional Ceremony"}
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => setStep("params")}>&larr; Back</Button>
                </div>
              )}

              {/* Policy: direct save */}
              {ruleTier !== "constitutional" && (
                <div className="flex gap-2 pt-2">
                  <Button variant="primary" size="sm" onClick={saveRule}
                    disabled={saving || (ruleType === "content_filter" && !pTopic)}>
                    {saving ? "Saving..." : editingId ? "Save Changes" : "Create Rule"}
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => setStep("params")}>&larr; Back</Button>
                </div>
              )}
            </div>
          )}

          {/* Constitutional ceremony */}
          {ceremonyMode && (
            <ConstitutionalCeremony
              mode={ceremonyMode}
              ruleName={ruleName || autoName()}
              ruleType={ruleType}
              ruleParams={buildParams() as Record<string, unknown>}
              proposedChanges={editingId ? buildParams() as Record<string, unknown> : undefined}
              onConfirm={async (reason) => {
                setSaving(true);
                setError("");
                try {
                  const payload: any = {
                    rule_type: ruleType, tier: "constitutional",
                    scope: ruleScope, scope_id: ruleScope === "child" && ruleScopeId ? ruleScopeId : undefined,
                    name: ruleName || autoName(), description: ruleDesc || reason,
                    parameters: buildParams(),
                    effective_from: effectiveFrom || undefined,
                    effective_until: effectiveUntil || undefined,
                    confirm_constitutional: true,
                    reason,
                  };
                  if (editingId) {
                    await governance.updateRule(editingId, { ...payload, reason });
                  } else {
                    await governance.createRule(payload);
                  }
                  resetBuilder();
                  setCeremonyMode(null);
                  await loadRules();
                } catch (err: any) {
                  setError(err?.detail || err?.message || "Couldn't save constitutional rule.");
                } finally {
                  setSaving(false);
                }
              }}
              onCancel={() => setCeremonyMode(null)}
              loading={saving}
            />
          )}
        </Card>
      )}

      {/* ── RULE LIST ── */}
      {!step && rules.length === 0 && (
        <EmptyState icon="empty" title="No governance rules defined yet"
          description="Rules control how the AI operates. Your constitutional rules protect your family's foundational principles." />
      )}

      {!step && rules.length > 0 && (
        <div className="space-y-8">
          {constitutional.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg">🛡️</span>
                <h3 className="text-sm font-semibold text-(--color-constitutional)">Constitutional Rules</h3>
              </div>
              <div className="space-y-2">
                {constitutional.map((r, idx) => (
                  <div key={r.id} className={`animate-fade-up stagger-${Math.min(idx + 1, 5)}`}>
                    <Card padding="p-4" borderLeft="border-l-(--color-constitutional)" className={cn("border-l-4", !r.is_active && "opacity-60")}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <ShieldIcon size={14} className="text-(--color-constitutional)" />
                          <span className="text-sm font-semibold text-(--color-text)">{r.name}</span>
                          <StatusBadge status="constitutional" />
                          {!r.is_active && <span className="text-[10px] font-bold text-(--color-warning) bg-(--color-warning-light) px-1.5 py-0.5 rounded">SUSPENDED</span>}
                        </div>
                        <div className="flex items-center gap-2">
                          <Button variant="ghost" size="sm" onClick={() => startEdit(r)}>Amend</Button>
                          {r.is_active ? (
                            <Button variant="ghost" size="sm" className="text-(--color-warning)"
                              onClick={() => { setCeremonyRuleId(r.id); setCeremonyMode("suspend"); }}>Suspend</Button>
                          ) : (
                            <Button variant="ghost" size="sm" className="text-(--color-success)"
                              onClick={async () => { await governance.updateRule(r.id, { is_active: true }); loadRules(); }}>Reactivate</Button>
                          )}
                        </div>
                      </div>
                      {r.description && <p className="text-xs text-(--color-text-secondary) mb-2">{r.description}</p>}
                      <div className="text-xs bg-(--color-constitutional-light) text-(--color-constitutional) rounded px-3 py-2">
                        {humanize(r)}
                      </div>
                      <p className="text-[10px] text-(--color-text-tertiary) mt-2 italic">
                        Cannot be deleted. Changes require formal amendment.
                      </p>
                    </Card>
                    {/* Suspend ceremony for this rule */}
                    {ceremonyMode === "suspend" && ceremonyRuleId === r.id && (
                      <div className="mt-2">
                        <ConstitutionalCeremony
                          mode="suspend"
                          ruleName={r.name}
                          originalReason={r.description || undefined}
                          createdAt={(r as any).created_at}
                          onConfirm={async (reason) => {
                            setSaving(true);
                            try {
                              await governance.updateRule(r.id, { is_active: false, reason });
                              setCeremonyMode(null);
                              setCeremonyRuleId(null);
                              await loadRules();
                            } catch (err: any) {
                              setError(err?.detail || err?.message || "Couldn't suspend rule.");
                            } finally {
                              setSaving(false);
                            }
                          }}
                          onCancel={() => { setCeremonyMode(null); setCeremonyRuleId(null); }}
                          loading={saving}
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {policy.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <h3 className="text-sm font-semibold text-(--color-text)">Policy Rules</h3>
                <span className="text-xs text-(--color-text-tertiary)">({policy.length})</span>
              </div>
              <div className="space-y-2">
                {policy.map((r, idx) => {
                  const info = RULE_TYPES.find((t) => t.value === r.rule_type);
                  return (
                    <Card key={r.id} padding="p-4" animate className={cn(!r.is_active ? "opacity-50" : "", `stagger-${Math.min(idx + 1, 5)}`)}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span>{info?.icon}</span>
                          <span className="text-sm font-semibold text-(--color-text)">{r.name}</span>
                          <span className="text-[10px] px-1.5 py-0.5 bg-(--color-page) text-(--color-text-secondary) rounded">{r.scope}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={cn("text-xs font-medium", r.is_active ? "text-(--color-success)" : "text-(--color-text-tertiary)")}>
                            {r.is_active ? "Active" : "Disabled"}
                          </span>
                          <Button variant="ghost" size="sm" onClick={() => startEdit(r)}>Edit</Button>
                          <Button variant="ghost" size="sm" className="text-(--color-danger)" onClick={() => deleteRule(r.id)}>Delete</Button>
                        </div>
                      </div>
                      {r.description && <p className="text-xs text-(--color-text-secondary) mb-2">{r.description}</p>}
                      <div className="text-xs bg-(--color-page) text-(--color-text-secondary) rounded px-3 py-2">
                        {humanize(r)}
                      </div>
                    </Card>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
