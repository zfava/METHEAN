"use client";

import { useEffect, useState } from "react";
import { auth, account, academicCalendar, household, dataExport, type User } from "@/lib/api";
import { useToast } from "@/components/Toast";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSkeleton from "@/components/LoadingSkeleton";


export default function SettingsPage() {
  useEffect(() => { document.title = "Settings | METHEAN"; }, []);
  const { toast } = useToast();

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Academic Calendar
  const [calType, setCalType] = useState("traditional");
  const [calWeeks, setCalWeeks] = useState(36);
  const [calDaysPerWeek, setCalDaysPerWeek] = useState(5);
  const [calDays, setCalDays] = useState(["monday", "tuesday", "wednesday", "thursday", "friday"]);
  const [calStart, setCalStart] = useState("");
  const [calSaved, setCalSaved] = useState(false);

  // Household
  const [hhName, setHhName] = useState("");
  const [hhTimezone, setHhTimezone] = useState("America/New_York");
  const [hhSaved, setHhSaved] = useState(false);

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
        .then((d) => { if (d.name) setHhName(d.name); if (d.timezone) setHhTimezone(d.timezone); })
        .catch(() => {}),
      academicCalendar.get().then((c) => {
        if (c.schedule_type) setCalType(c.schedule_type);
        if (c.total_instructional_weeks) setCalWeeks(c.total_instructional_weeks);
        if (c.instruction_days_per_week) setCalDaysPerWeek(c.instruction_days_per_week);
        if (c.instruction_days) setCalDays(c.instruction_days);
        if (c.start_date) setCalStart(c.start_date);
      }).catch(() => {}),
    ]).catch(() => {}).finally(() => setLoading(false));
  }, []);

  async function saveHousehold() {
    await household.update({ name: hhName, timezone: hhTimezone });
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

      {/* About */}
      <Card>
        <SectionHeader title="About" />
        <div className="mt-2 text-xs text-(--color-text-tertiary) space-y-1">
          <p>METHEAN v0.1.0</p>
          <p>Built by Spartan Solutions</p>
          <a href="/" className="text-(--color-accent) hover:underline">Visit landing page</a>
        </div>
      </Card>
    </div>
  );
}
