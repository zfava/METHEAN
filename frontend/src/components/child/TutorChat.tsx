"use client";

import { useState, useEffect, useRef, useCallback } from "react";
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
  time: string;
}

function timeStr(): string {
  return new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
}

export default function TutorChat({ activityId, childId, onClose }: TutorChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    { role: "tutor", text: "Hi! I'm here to help you learn. What are you working on, or what would you like to understand better?", time: timeStr() },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [revealedHints, setRevealedHints] = useState<Set<number>>(new Set());
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll on new messages or loading change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, loading]);

  // Auto-grow textarea
  const resizeTextarea = useCallback(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 96) + "px"; // max ~4 rows
  }, []);

  useEffect(() => { resizeTextarea(); }, [input, resizeTextarea]);

  async function send() {
    if (!input.trim() || loading) return;
    const msg = input.trim();
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";

    const updatedMessages: Message[] = [...messages, { role: "child", text: msg, time: timeStr() }];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      const history = updatedMessages.map((m) => ({ role: m.role, text: m.text }));
      const resp = await tutor.message(activityId, childId, msg, history);
      setMessages((prev) => [...prev, {
        role: "tutor",
        text: resp.message,
        hints: resp.hints || [],
        time: timeStr(),
      }]);
    } catch {
      setMessages((prev) => [...prev, { role: "tutor", text: "I'm having trouble thinking right now. Try again in a moment.", time: timeStr() }]);
    } finally {
      setLoading(false);
    }
  }

  function revealHint(msgIndex: number) {
    setRevealedHints((prev) => new Set([...prev, msgIndex]));
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-sm bg-(--color-surface) border-l border-(--color-border) shadow-lg z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-(--color-border)">
        <div>
          <h3 className="text-base font-semibold text-(--color-text)">Your Tutor</h3>
          <p className="text-[10px] text-(--color-text-tertiary) italic">Socratic mode — I'll guide you with questions, not answers</p>
        </div>
        <button
          onClick={onClose}
          className="w-8 h-8 rounded-full flex items-center justify-center text-(--color-text-tertiary) hover:bg-(--color-page) hover:text-(--color-text) transition-colors shrink-0"
        >
          <svg className="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-5 space-y-3">
        {messages.map((msg, i) => (
          <div key={i} className="msg-enter" style={{ animationDelay: `${i === messages.length - 1 ? "0ms" : "0ms"}` }}>
            {msg.role === "tutor" ? (
              /* ── Tutor message ── */
              <div className="flex items-start gap-2 max-w-[80%]">
                <div className="w-7 h-7 rounded-full bg-(--color-accent-light) flex items-center justify-center text-sm shrink-0 mt-0.5">
                  🦉
                </div>
                <div>
                  <div className="bg-(--color-page) text-(--color-text) rounded-[16px] rounded-bl-[4px] px-4 py-2.5 text-sm leading-relaxed">
                    {msg.text}
                  </div>
                  <div className="text-[10px] text-(--color-text-tertiary) mt-1 ml-1">{msg.time}</div>

                  {/* Hint button */}
                  {msg.hints && msg.hints.length > 0 && !revealedHints.has(i) && (
                    <button
                      onClick={() => revealHint(i)}
                      className="flex items-center gap-1 mt-1.5 ml-1 text-xs text-(--color-accent) hover:underline"
                    >
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      Need a hint?
                    </button>
                  )}

                  {/* Revealed hint */}
                  {msg.hints && revealedHints.has(i) && (
                    <div className="mt-2 msg-enter">
                      <div className="bg-(--color-warning-light) text-(--color-warning) border-l-2 border-(--color-warning) rounded-r-[10px] px-3 py-2 text-xs leading-relaxed">
                        <span className="font-medium">💡 Hint: </span>
                        {msg.hints.map((h, hi) => <span key={hi}>{hi > 0 && " "}{h}</span>)}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              /* ── Child message ── */
              <div className="flex flex-col items-end">
                <div className="bg-(--color-accent) text-white rounded-[16px] rounded-br-[4px] px-4 py-2.5 text-sm leading-relaxed max-w-[80%]">
                  {msg.text}
                </div>
                <div className="text-[10px] text-(--color-text-tertiary) mt-1 mr-1">{msg.time}</div>
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="flex items-start gap-2 max-w-[80%] msg-enter">
            <div className="w-7 h-7 rounded-full bg-(--color-accent-light) flex items-center justify-center text-sm shrink-0 mt-0.5">
              🦉
            </div>
            <div className="bg-(--color-page) rounded-[16px] rounded-bl-[4px] px-4 py-3 flex items-center gap-1.5">
              <span className="typing-dot" style={{ animationDelay: "0ms" }} />
              <span className="typing-dot" style={{ animationDelay: "150ms" }} />
              <span className="typing-dot" style={{ animationDelay: "300ms" }} />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="p-3 border-t border-(--color-border)">
        <div className="flex items-end gap-2">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your question..."
            rows={1}
            className="flex-1 px-4 py-2.5 text-sm border border-(--color-border) rounded-[18px] bg-(--color-surface) text-(--color-text) resize-none focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 leading-relaxed"
            style={{ maxHeight: 96 }}
          />
          <button
            onClick={send}
            disabled={!input.trim() || loading}
            className="w-9 h-9 rounded-full bg-(--color-accent) text-white flex items-center justify-center shrink-0 hover:opacity-90 disabled:opacity-30 transition-opacity"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
          </button>
        </div>
      </div>

      {/* CSS animations */}
      <style>{`
        .msg-enter {
          animation: msg-slide-in 200ms ease-out both;
        }
        @keyframes msg-slide-in {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .typing-dot {
          display: inline-block;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: var(--color-text-tertiary);
          animation: typing-pulse 1s ease-in-out infinite;
        }
        @keyframes typing-pulse {
          0%, 60%, 100% { opacity: 0.3; }
          30% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}
