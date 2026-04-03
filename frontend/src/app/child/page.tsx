"use client";

import { useEffect, useState } from "react";
import { auth, tutor, attempts, type User } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TodayActivity {
  id: string;
  title: string;
  activity_type: string;
  status: string;
  estimated_minutes: number | null;
  node_id: string | null;
}

interface ChatMessage {
  role: "child" | "tutor";
  content: string;
}

export default function ChildPage() {
  const [user, setUser] = useState<User | null>(null);
  const [children, setChildren] = useState<{ id: string; first_name: string }[]>([]);
  const [selectedChildId, setSelectedChildId] = useState("");
  const [todayActivities, setTodayActivities] = useState<TodayActivity[]>([]);
  const [activeActivity, setActiveActivity] = useState<TodayActivity | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    init();
  }, []);

  useEffect(() => {
    if (selectedChildId) loadToday();
  }, [selectedChildId]);

  async function init() {
    try {
      const me = await auth.me();
      setUser(me);
      const resp = await fetch(`${API_BASE}/children`, { credentials: "include" });
      if (resp.ok) {
        const data = await resp.json();
        setChildren(data);
        if (data.length > 0) setSelectedChildId(data[0].id);
      }
    } catch {
      window.location.href = "/auth";
    } finally {
      setLoading(false);
    }
  }

  async function loadToday() {
    try {
      const resp = await fetch(`${API_BASE}/children/${selectedChildId}/today`, { credentials: "include" });
      if (resp.ok) setTodayActivities(await resp.json());
    } catch {}
  }

  async function startActivity(activity: TodayActivity) {
    try {
      const attempt = await attempts.start(activity.id, selectedChildId);
      setAttemptId(attempt.id);
      setActiveActivity(activity);
      setSubmitted(false);
      setFeedback("");
      setMessages([
        { role: "tutor", content: `Let's work on "${activity.title}". What do you know about this topic so far?` },
      ]);
    } catch (err: any) {
      alert(err.detail || "Could not start");
    }
  }

  async function sendMessage() {
    if (!input.trim() || sending || !activeActivity) return;
    const msg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "child", content: msg }]);
    setSending(true);
    try {
      const resp = await tutor.message(activeActivity.id, selectedChildId, msg);
      setMessages((prev) => [...prev, { role: "tutor", content: resp.message }]);
    } catch {
      setMessages((prev) => [...prev, { role: "tutor", content: "I had trouble with that. Could you try again?" }]);
    } finally {
      setSending(false);
    }
  }

  async function submitWork() {
    if (!attemptId) return;
    try {
      const result = await attempts.submit(attemptId, { confidence: 0.7, duration_minutes: 15 });
      setSubmitted(true);
      const mastery = result.mastery_level?.replace(/_/g, " ") || "recorded";
      setFeedback(`Great work! You've reached "${mastery}" level.`);
      setMessages((prev) => [...prev, { role: "tutor", content: `Session complete! ${mastery === "recorded" ? "Your work has been recorded." : `You've reached ${mastery} level. Keep going!`}` }]);
    } catch (err: any) {
      alert(err.detail || "Could not submit");
    }
  }

  if (loading) return <div className="min-h-screen flex items-center justify-center text-sm text-(--color-text-secondary)">Loading...</div>;

  const childName = children.find((c) => c.id === selectedChildId)?.first_name || "Student";

  return (
    <div className="min-h-screen bg-(--color-bg)">
      <header className="bg-white border-b border-(--color-border) px-6 py-4">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold">METHEAN</h1>
            <p className="text-xs text-(--color-text-secondary)">{childName}&apos;s Learning</p>
          </div>
          <div className="flex items-center gap-3">
            {children.length > 1 && (
              <select
                value={selectedChildId}
                onChange={(e) => { setSelectedChildId(e.target.value); setActiveActivity(null); }}
                className="text-sm border border-(--color-border) rounded px-2 py-1"
              >
                {children.map((c) => <option key={c.id} value={c.id}>{c.first_name}</option>)}
              </select>
            )}
            {activeActivity && !submitted && (
              <button onClick={submitWork} className="px-4 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)">
                Submit Work
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-2xl mx-auto py-6 px-4">
        {!activeActivity ? (
          <div>
            <h2 className="text-sm font-semibold mb-4">Today&apos;s Activities</h2>
            {todayActivities.length === 0 ? (
              <div className="bg-white rounded-lg border border-(--color-border) p-8 text-center text-sm text-(--color-text-secondary)">
                No activities scheduled for today. Check back tomorrow!
              </div>
            ) : (
              <div className="space-y-3">
                {todayActivities.map((a) => (
                  <div key={a.id} className="bg-white rounded-lg border border-(--color-border) p-4 flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium">{a.title}</div>
                      <div className="flex items-center gap-2 mt-1">
                        <StatusBadge status={a.activity_type} />
                        {a.estimated_minutes && <span className="text-xs text-(--color-text-secondary)">{a.estimated_minutes} min</span>}
                      </div>
                    </div>
                    {a.status === "scheduled" && (
                      <button onClick={() => startActivity(a)} className="px-4 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)">
                        Start
                      </button>
                    )}
                    {a.status === "completed" && <StatusBadge status="completed" />}
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-lg border border-(--color-border)">
            <div className="px-4 py-3 border-b border-(--color-border)">
              <div className="text-sm font-semibold">{activeActivity.title}</div>
              <button onClick={() => setActiveActivity(null)} className="text-xs text-(--color-accent) hover:underline mt-0.5">Back to activities</button>
            </div>
            <div className="h-96 overflow-y-auto p-4 space-y-3">
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === "child" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[80%] px-4 py-2.5 rounded-xl text-sm ${
                    msg.role === "child"
                      ? "bg-(--color-accent) text-white rounded-br-sm"
                      : "bg-gray-100 text-(--color-text) rounded-bl-sm"
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              {sending && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-xl px-4 py-2.5 text-sm text-(--color-text-secondary)">Thinking...</div>
                </div>
              )}
            </div>
            {!submitted && (
              <div className="border-t border-(--color-border) p-3 flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                  placeholder="Type your answer..."
                  className="flex-1 px-3 py-2 text-sm border border-(--color-border) rounded-md focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
                />
                <button
                  onClick={sendMessage}
                  disabled={sending || !input.trim()}
                  className="px-4 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover) disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            )}
            {submitted && feedback && (
              <div className="border-t border-(--color-border) p-4 text-center">
                <div className="text-sm font-medium text-emerald-700">{feedback}</div>
                <button onClick={() => { setActiveActivity(null); loadToday(); }} className="mt-2 text-xs text-(--color-accent) hover:underline">Back to activities</button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
