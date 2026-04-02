"use client";

import { useState } from "react";
import { tutor, attempts, type TutorResponse } from "@/lib/api";

interface ChatMessage {
  role: "child" | "tutor";
  content: string;
}

export default function ChildPage() {
  const [activityId, setActivityId] = useState("");
  const [childId, setChildId] = useState("");
  const [attemptId, setAttemptId] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [sessionActive, setSessionActive] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function startSession() {
    if (!activityId || !childId) return;
    try {
      const attempt = await attempts.start(activityId, childId);
      setAttemptId(attempt.id);
      setSessionActive(true);
      setMessages([
        { role: "tutor", content: "Hello! I'm your learning tutor. What would you like to explore today? Tell me what you're thinking!" },
      ]);
    } catch (err: any) {
      alert(err.detail || "Could not start session");
    }
  }

  async function sendMessage() {
    if (!input.trim() || sending) return;
    const msg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "child", content: msg }]);
    setSending(true);

    try {
      const resp = await tutor.message(activityId, childId, msg);
      setMessages((prev) => [...prev, { role: "tutor", content: resp.message }]);
      if (resp.hints.length > 0) {
        setMessages((prev) => [
          ...prev,
          { role: "tutor", content: `Hint: ${resp.hints[0]}` },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "tutor", content: "I had trouble thinking about that. Could you try rephrasing?" },
      ]);
    } finally {
      setSending(false);
    }
  }

  async function submitAttempt() {
    if (!attemptId) return;
    try {
      const result = await attempts.submit(attemptId, {
        confidence: 0.7,
        duration_minutes: 15,
      });
      setSubmitted(true);
      setSessionActive(false);
      setMessages((prev) => [
        ...prev,
        {
          role: "tutor",
          content: `Great work! Your session is complete. You've reached "${result.mastery_level.replace(/_/g, " ")}" level on this skill.`,
        },
      ]);
    } catch (err: any) {
      alert(err.detail || "Could not submit");
    }
  }

  return (
    <div className="min-h-screen bg-(--color-bg)">
      <header className="bg-white border-b border-(--color-border) px-6 py-4">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold">METHEAN</h1>
            <p className="text-xs text-(--color-text-secondary)">Learning Session</p>
          </div>
          {sessionActive && (
            <button
              onClick={submitAttempt}
              className="px-4 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)"
            >
              Submit Work
            </button>
          )}
        </div>
      </header>

      <div className="max-w-2xl mx-auto py-6 px-4">
        {!sessionActive && !submitted && (
          <div className="bg-white rounded-lg border border-(--color-border) p-6">
            <h2 className="text-sm font-semibold mb-4">Start a Learning Session</h2>
            <div className="space-y-3">
              <input
                type="text"
                placeholder="Activity ID"
                value={activityId}
                onChange={(e) => setActivityId(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-md"
              />
              <input
                type="text"
                placeholder="Child ID"
                value={childId}
                onChange={(e) => setChildId(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-md"
              />
              <button
                onClick={startSession}
                className="w-full py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)"
              >
                Start Session
              </button>
            </div>
          </div>
        )}

        {/* Chat */}
        {(sessionActive || submitted) && (
          <div className="bg-white rounded-lg border border-(--color-border)">
            <div className="h-96 overflow-y-auto p-4 space-y-3">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "child" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] px-4 py-2.5 rounded-xl text-sm ${
                      msg.role === "child"
                        ? "bg-(--color-accent) text-white rounded-br-sm"
                        : "bg-gray-100 text-(--color-text) rounded-bl-sm"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
              {sending && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-xl px-4 py-2.5 text-sm text-(--color-text-secondary)">
                    Thinking...
                  </div>
                </div>
              )}
            </div>
            {sessionActive && (
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
          </div>
        )}
      </div>
    </div>
  );
}
