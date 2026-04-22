"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, account, academicCalendar, household, familyInvites, dataExport, compliance, betaFeedback, type BetaFeedbackItem, type User } from "@/lib/api";
import { useMobile } from "@/lib/useMobile";
import { useToast } from "@/components/Toast";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";


export default function SettingsPage() {
  useEffect(() => { document.title = "Settings | METHEAN"; }, []);
  const { toast } = useToast();

  const [user, setUser] = useState<User | null>(null);
  const isMobile = useMobile();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Academic Calendar
  const [calType, setCalType] = useState("traditional");
  const [calWeeks, setCalWeeks] = useState(36);
  const [calDaysPerWeek, setCalDaysPerWeek] = useState(5);
  const [calDays, setCalDays] = useState(["monday", "tuesday", "wednesday", "thursday", "friday"]);
  const [calStart, setCalStart] = useState("");
  const [calSaved, setCalSaved] = useState(false);

  // Notification preferences
  const [notifPrefs, setNotifPrefs] = useState<Record<string, boolean>>({});

  // Family members
  const [invites, setInvites] = useState<any[]>([]);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("parent");
  const [inviting, setInviting] = useState(false);

  // Household
  const [hhName, setHhName] = useState("");
  const [hhTimezone, setHhTimezone] = useState("America/New_York");
  const [hhState, setHhState] = useState("");
  const [hhSaved, setHhSaved] = useState(false);
  const [statesList, setStatesList] = useState<{code: string; name: string}[]>([]);

  // Beta feedback submissions
  const [myFeedback, setMyFeedback] = useState<BetaFeedbackItem[]>([]);

  // Password
  const [currentPw, setCurrentPw] = useState("");
  const [newPw, setNewPw] = useState("");
  const [confirmPw, setConfirmPw] = useState("");
  const [pwError, setPwError] = useState("");
  const [pwSuccess, setPwSuccess] = useState(false);

  useEffect(() => {
    Promise.all([
      auth.me().then(setUser),
      household.get()
        .then((d) => { if (d.name) setHhName(d.name); if (d.timezone) setHhTimezone(d.timezone); if (d.home_state) setHhState(d.home_state); })
        .catch(() => {}),
      compliance.states().then((s: any[]) => setStatesList(s.map((x: any) => ({ code: x.code, name: x.name })))).catch(() => {}),
      academicCalendar.get().then((c) => {
        if (c.schedule_type) setCalType(c.schedule_type);
        if (c.total_instructional_weeks) setCalWeeks(c.total_instructional_weeks);
        if (c.instruction_days_per_week) setCalDaysPerWeek(c.instruction_days_per_week);
        if (c.instruction_days) setCalDays(c.instruction_days);
        if (c.start_date) setCalStart(c.start_date);
      }).catch(() => {}),
      account.getNotificationPreferences().then(setNotifPrefs).catch(() => {}),
      familyInvites.list().then(setInvites).catch(() => {}),
      betaFeedback.list().then(setMyFeedback).catch(() => {}),
    ]).catch(() => {}).finally(() => setLoading(false));
  }, []);

  async function saveHousehold() {
    await household.update({ name: hhName, timezone: hhTimezone, home_state: hhState || null });
    setHhSaved(true);
    toast("Settings saved", "success");
    setTimeout(() => setHhSaved(false), 2000);
  }

  async function saveCalendar() {
    setCalSaved(false);
    try {
      await academicCalendar.update({
        schedule_type: calType,
        total_instructional_weeks: calWeeks,
        instruction_days_per_week: calDaysPerWeek,
        instruction_days: calDays,
        start_date: calStart || undefined,
      });
      setCalSaved(true);
      toast("Calendar saved", "success");
      setTimeout(() => setCalSaved(false), 2000);
    } catch (err: any) {
      toast(err?.detail || "Couldn't save calendar", "error");
      setError(err?.detail || "Couldn't save calendar.");
    }
  }

  function toggleCalDay(day: string) {
    setCalDays((prev) => prev.includes(day) ? prev.filter((d) => d !== day) : [...prev, day]);
  }

  async function changePassword() {
    setPwError(""); setPwSuccess(false);
    if (newPw !== confirmPw) { setPwError("Passwords don't match."); return; }
    if (newPw.length < 8) { setPwError("Password must be at least 8 characters."); return; }
    try {
      await account.changePassword(currentPw, newPw);
      setPwSuccess(true);
      toast("Password changed", "success");
      setCurrentPw(""); setNewPw(""); setConfirmPw("");
    } catch (err: any) {
      toast(err?.detail || err?.message || "Couldn't change password", "error");
      setPwError(err?.detail || err?.message || "Couldn't change password.");
    }
  }

  if (loading) return <div className="max-w-3xl"><PageHeader title="Settings" /><LoadingSkeleton variant="card" count={3} /></div>;

  return (
    <div className="max-w-3xl">
      <PageHeader title="Settings" subtitle="Manage your household and account." />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => setError("")}>Dismiss</Button>
          </div>
        </Card>
      )}

      {/* Academic Calendar */}
      <Card className="mb-6">
        <SectionHeader title="Academic Calendar" />
        <p className="text-xs text-(--color-text-secondary) mt-1 mb-3">How does your family schedule the school year?</p>
        <div className="space-y-3">
          <div className="flex gap-2">
            {(["traditional", "year_round", "custom"] as const).map((t) => (
              <button key={t} onClick={() => { setCalType(t); if (t === "traditional") { setCalWeeks(36); setCalDaysPerWeek(5); setCalDays(["monday","tuesday","wednesday","thursday","friday"]); } }}
                className={`px-3 py-1.5 text-xs rounded-[10px] border capitalize transition-colors ${calType === t ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)" : "border-(--color-border) text-(--color-text-secondary)"}`}>
                {t.replace("_", " ")}
              </button>
            ))}
          </div>
          {calType !== "traditional" && (
            <>
              <div>
                <label className="block text-xs text-(--color-text-secondary) mb-1">Start date</label>
                <input type="date" value={calStart} onChange={(e) => setCalStart(e.target.value)}
                  className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
              </div>
              <div>
                <label className="block text-xs text-(--color-text-secondary) mb-1">Instructional weeks</label>
                <input type="number" value={calWeeks} onChange={(e) => setCalWeeks(Number(e.target.value))} min={1} max={52}
                  className="w-24 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
              </div>
              <div>
                <label className="block text-xs text-(--color-text-secondary) mb-1">Instruction days</label>
                <div className="flex gap-1.5 flex-wrap">
                  {["monday","tuesday","wednesday","thursday","friday","saturday","sunday"].map((d) => (
                    <button key={d} onClick={() => toggleCalDay(d)}
                      className={`w-9 h-9 text-[10px] rounded-[10px] border capitalize transition-colors ${calDays.includes(d) ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)" : "border-(--color-border) text-(--color-text-tertiary)"}`}>
                      {d.slice(0, 2)}
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}
          <div className="flex items-center gap-2">
            <Button variant="primary" size="sm" onClick={saveCalendar}>Save Calendar</Button>
            {calSaved && <span className="text-xs text-(--color-success)">Saved</span>}
          </div>
          {calType === "traditional" && (
            <p className="text-[10px] text-(--color-text-tertiary)">Traditional: September to May, 36 weeks, Monday through Friday.</p>
          )}
        </div>
      </Card>

      {/* Household */}
      <Card className="mb-6">
        <SectionHeader title="Household" />
        <div className="mt-3 space-y-3">
          <div>
            <label className="block text-xs text-(--color-text-secondary) mb-1">Household name</label>
            <input value={hhName} onChange={(e) => setHhName(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
          </div>
          <div>
            <label className="block text-xs text-(--color-text-secondary) mb-1">Timezone</label>
            <select value={hhTimezone} onChange={(e) => setHhTimezone(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              {["America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles", "America/Anchorage", "Pacific/Honolulu", "UTC"].map((tz) => (
                <option key={tz} value={tz}>{tz}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-medium text-(--color-text-secondary) block mb-1">Home State</label>
            <select value={hhState} onChange={(e) => setHhState(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="">Not set</option>
              {statesList.map((s) => (
                <option key={s.code} value={s.code}>{s.name} ({s.code})</option>
              ))}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="primary" size="sm" onClick={saveHousehold}>Save</Button>
            {hhSaved && <span className="text-xs text-(--color-success)">Saved</span>}
          </div>
        </div>
      </Card>

      {/* Account */}
      <Card className="mb-6">
        <SectionHeader title="Account" />
        <div className="mt-3 space-y-3">
          <div>
            <label className="block text-xs text-(--color-text-secondary) mb-1">Email</label>
            <input value={user?.email || ""} disabled
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-page) text-(--color-text-tertiary)" />
            <p className="text-[10px] text-(--color-text-tertiary) mt-0.5">Contact support to change your email.</p>
          </div>
          <div>
            <label className="block text-xs text-(--color-text-secondary) mb-1">Display name</label>
            <input value={user?.display_name || ""} disabled
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-page) text-(--color-text-tertiary)" />
          </div>
        </div>
      </Card>

      {/* Password */}
      <Card className="mb-6">
        <SectionHeader title="Change Password" />
        <div className="mt-3 space-y-3">
          <input type="password" value={currentPw} onChange={(e) => setCurrentPw(e.target.value)} placeholder="Current password"
            className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
          <input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} placeholder="New password (min 8 characters)"
            className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
          <input type="password" value={confirmPw} onChange={(e) => setConfirmPw(e.target.value)} placeholder="Confirm new password"
            className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
          {pwError && <p className="text-xs text-(--color-danger)">{pwError}</p>}
          {pwSuccess && <p className="text-xs text-(--color-success)">Password changed successfully.</p>}
          <Button variant="primary" size="sm" onClick={changePassword} disabled={!currentPw || !newPw || !confirmPw}>
            Change Password
          </Button>
        </div>
      </Card>

      {/* Data */}
      <Card className="mb-6">
        <SectionHeader title="Your Data" />
        <p className="text-xs text-(--color-text-secondary) mt-2 mb-3">Your data belongs to you. Export it anytime.</p>
        <div className="flex flex-wrap gap-2">
          <a href={dataExport.download()} target="_blank" rel="noopener"
            className="px-3 py-1.5 text-xs font-medium border border-(--color-border) rounded-[10px] text-(--color-text-secondary) hover:bg-(--color-page) transition-colors">
            Export All Data (ZIP)
          </a>
        </div>
      </Card>

      {/* My Feedback */}
      <Card className="mb-6">
        <SectionHeader title="My Feedback" />
        <p className="text-xs text-(--color-text-secondary) mt-1 mb-3">
          Beta feedback you've sent us. Status updates as we review each item.
        </p>
        {myFeedback.length === 0 ? (
          <p className="text-xs text-(--color-text-tertiary)">
            You haven't submitted any feedback yet. Use the feedback button in the bottom-right corner of any page.
          </p>
        ) : (
          <div className="space-y-2">
            {myFeedback.map((fb) => (
              <div
                key={fb.id}
                className="px-3 py-2.5 bg-(--color-page) rounded-[10px] border border-(--color-border)"
              >
                <div className="flex items-start justify-between gap-3 mb-1">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="text-[11px] text-(--color-text-tertiary) capitalize">
                      {fb.feedback_type.replace("_", " ")}
                    </span>
                    {fb.rating !== null && (
                      <span className="text-[11px] text-(--color-text-tertiary)">
                        {"★".repeat(fb.rating)}
                      </span>
                    )}
                  </div>
                  <StatusBadge status={fb.status} />
                </div>
                <p className="text-sm text-(--color-text) whitespace-pre-wrap break-words">
                  {fb.message}
                </p>
                <div className="flex items-center justify-between gap-2 mt-1.5 text-[10px] text-(--color-text-tertiary)">
                  <span className="truncate">{fb.page_context || ""}</span>
                  <span className="shrink-0">
                    {fb.created_at ? new Date(fb.created_at).toLocaleDateString() : ""}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* About */}
      <Card>
        <SectionHeader title="About" />
        <div className="mt-2 text-xs text-(--color-text-tertiary) space-y-1">
          <p>METHEAN v0.1.0</p>
          <p>Built by METHEAN, Inc.</p>
          <Link href="/" className="text-(--color-accent) hover:underline">Visit landing page</Link>
        </div>
      </Card>

      {/* Family Members */}
      <Card className="mb-6">
        <SectionHeader title="Family Members" />
        <p className="text-xs text-(--color-text-secondary) mt-1 mb-3">Invite a co-parent or observer to your household.</p>

        {invites.length > 0 && (
          <div className="space-y-2 mb-4">
            {invites.map((inv: any) => (
              <div key={inv.id} className="flex items-center justify-between px-3 py-2 bg-(--color-page) rounded-[10px]">
                <div>
                  <span className="text-sm text-(--color-text)">{inv.email}</span>
                  <span className="text-[10px] text-(--color-text-tertiary) ml-2 capitalize">{inv.role} · Pending</span>
                </div>
                <button onClick={async () => {
                  await familyInvites.revoke(inv.id);
                  toast("Invite revoked", "info");
                  setInvites(invites.filter((i: any) => i.id !== inv.id));
                }} className="text-xs text-(--color-danger) hover:underline">Revoke</button>
              </div>
            ))}
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-2">
          <input value={inviteEmail} onChange={(e) => setInviteEmail(e.target.value)} placeholder="Email address"
            className="flex-1 px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]" />
          <select value={inviteRole} onChange={(e) => setInviteRole(e.target.value)}
            className="px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px]">
            <option value="parent">Parent</option>
            <option value="viewer">Observer</option>
          </select>
          <Button variant="primary" size="sm" disabled={!inviteEmail.trim() || inviting} onClick={async () => {
            setInviting(true);
            try {
              await familyInvites.invite(inviteEmail, inviteRole);
              toast("Invitation sent", "success");
              setInviteEmail("");
              const updated = await familyInvites.list();
              setInvites(updated);
            } catch (err: any) { toast(err?.detail || "Couldn't send invite", "error"); }
            finally { setInviting(false); }
          }}>Invite</Button>
        </div>
      </Card>

      {/* Notification Preferences */}
      <Card className="mb-6">
        <SectionHeader title="Notification Preferences" />
        <p className="text-xs text-(--color-text-secondary) mt-1 mb-4">Choose which emails METHEAN sends you.</p>
        <div className="space-y-3">
          {([
            ["email_daily_summary", "Daily morning summary", "Today's plan per child + pending reviews"],
            ["email_milestones", "Mastery milestones", "When your child masters a concept"],
            ["email_governance_alerts", "Governance alerts", "When a rule blocks or flags an activity"],
            ["email_weekly_digest", "Weekly digest", "End-of-week summary of learning progress"],
            ["email_compliance_warnings", "Compliance warnings", "Hours shortfall or approaching deadlines"],
          ] as const).map(([key, label, desc]) => (
            <div key={key} className="flex items-center justify-between py-2">
              <div>
                <div className="text-sm text-(--color-text)">{label}</div>
                <div className="text-[10px] text-(--color-text-tertiary)">{desc}</div>
              </div>
              <button
                onClick={async () => {
                  const newVal = !notifPrefs[key];
                  const updated = { ...notifPrefs, [key]: newVal };
                  setNotifPrefs(updated);
                  try {
                    await account.updateNotificationPreferences({ [key]: newVal });
                    toast(newVal ? "Enabled" : "Disabled", "success");
                  } catch { toast("Couldn't save preference", "error"); }
                }}
                className={`w-10 h-6 rounded-full transition-colors duration-200 relative ${notifPrefs[key] !== false ? "bg-(--color-success)" : "bg-(--color-border-strong)"}`}
              >
                <span className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200 ${notifPrefs[key] !== false ? "left-[18px]" : "left-0.5"}`} />
              </button>
            </div>
          ))}
        </div>
      </Card>

      {/* ── Data Export ── */}
      <Card className="mb-6">
        <SectionHeader title="Your Data" />
        <p className="text-xs text-(--color-text-secondary) mb-3">
          You own your data. Export everything METHEAN knows about your family at any time.
        </p>
        <Button
          variant="secondary"
          size="sm"
          className={isMobile ? "w-full" : ""}
          onClick={async () => {
            try {
              const link = document.createElement("a");
              link.href = "/api/v1/household/export";
              link.download = `methean-export-${new Date().toISOString().split("T")[0]}.zip`;
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
              toast("Export started. Check your downloads.", "success");
            } catch {
              toast("Export failed. Try again.", "error");
            }
          }}
        >
          Export All Data
        </Button>
      </Card>
    </div>
  );
}
