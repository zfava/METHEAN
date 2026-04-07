"use client";

import { useState } from "react";
import { tutor } from "@/lib/api";
import { cn } from "@/lib/cn";

interface TutorChatProps {
  activityId: string;
  childId: string;
  onClose: () => void;
}

interface Message {
  role: "child" | "tutor";
  text: string;
  hints?: string[];
}

export default function TutorChat({ activityId, childId, onClose }: TutorChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    { role: "tutor", text: "Hi! I'm here to help you learn. What are you working on, or what would you like to understand better?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [revealedHints, setRevealedHints] = useState<Set<number>>(new Set());

  async function send() {
    if (!input.trim() || loading) return;
    const msg = input.trim();
    setInput("");
    const updatedMessages: Message[] = [...messages, { role: "child", text: msg }];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      const history = updatedMessages.map((m) => ({ role: m.role, text: m.text }));
      const resp = await tutor.message(activityId, childId, msg, history);
      setMessages((prev) => [...prev, {
        role: "tutor",
        text: resp.message,
        hints: resp.hints || [],
      }]);
    } catch {
      setMessages((prev) => [...prev, { role: "tutor", text: "I'm having trouble thinking right now. Try again in a moment." }]);
    } finally {
      setLoading(false);
    }
  }

  function revealHint(msgIndex: number) {
    setRevealedHints((prev) => new Set([...prev, msgIndex]));
  }

  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-sm bg-(--color-surface) border-l border-(--color-border) shadow-lg z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-(--color-border)">
        <div>
          <h3 className="text-base font-semibold text-(--color-text)">Your Tutor</h3>
          <p className="text-xs text-(--color-text-tertiary)">Ask questions, think out loud</p>
        </div>
        <button onClick={onClose} className="text-sm text-(--color-text-tertiary) hover:text-(--color-text) transition-colors">Close</button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4">
        {messages.map((msg, i) => (
          <div key={i}>
            <div className={cn(
              "max-w-[85%] px-4 py-3 rounded-2xl text-sm leading-relaxed",
              msg.role === "child"
                ? "ml-auto bg-(--color-accent) text-white rounded-br-md"
                : "bg-(--color-page) text-(--color-text) rounded-bl-md"
            )}>
              {msg.text}
            </div>
            {msg.hints && msg.hints.length > 0 && !revealedHints.has(i) && (
              <button
                onClick={() => revealHint(i)}
                className="mt-1.5 text-xs text-(--color-accent) hover:underline"
              >
                Need a hint?
              </button>
            )}
            {msg.hints && revealedHints.has(i) && (
              <div className="mt-1.5 ml-2 text-xs text-(--color-text-secondary) italic">
                {msg.hints.map((h, hi) => <p key={hi}>{h}</p>)}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="max-w-[85%] px-4 py-3 rounded-2xl bg-(--color-page) text-(--color-text-tertiary) text-sm rounded-bl-md">
            Thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-(--color-border)">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="Type your question..."
            className="flex-1 px-4 py-3 text-sm border border-(--color-border) rounded-2xl bg-(--color-surface) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
          />
          <button
            onClick={send}
            disabled={!input.trim() || loading}
            className="px-4 py-3 text-sm font-medium text-white bg-(--color-accent) rounded-2xl hover:opacity-90 disabled:opacity-40 transition-opacity"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
