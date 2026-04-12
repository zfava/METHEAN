"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { tutor } from "@/lib/api";

interface TutorChatProps {
  activityId: string;
  childId: string;
  onClose: () => void;
  activityTitle?: string;
  subjectColor?: string;
  isStuck?: boolean;        // Opened via "I'm stuck" button
  currentStep?: number;     // Current step/question index
  totalSteps?: number;
}

interface Message {
  role: "child" | "tutor";
  text: string;
  hints?: string[];
  ts: number;              // Unix timestamp for gap detection
}

export default function TutorChat({
  activityId, childId, onClose,
  activityTitle, subjectColor, isStuck, currentStep, totalSteps,
}: TutorChatProps) {
  // Context-aware opening
  const openingMsg = isStuck
    ? `I can see this is tricky. Let's work through it together. What part is confusing you?`
    : activityTitle
      ? `I see you're working on ${activityTitle}. What would you like help with?`
      : "What would you like help with?";

  const [messages, setMessages] = useState<Message[]>([
    { role: "tutor", text: openingMsg, ts: Date.now() },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [revealedHints, setRevealedHints] = useState<Set<number>>(new Set());
  const [userScrolled, setUserScrolled] = useState(false);
  const [sendTimes, setSendTimes] = useState<number[]>([]);
  const [rateLimited, setRateLimited] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const openerRef = useRef<HTMLElement | null>(null);

  // Focus textarea on mount, save opener for focus restore
  useEffect(() => {
    openerRef.current = document.activeElement as HTMLElement;
    textareaRef.current?.focus();
    return () => { openerRef.current?.focus(); };
  }, []);

  // Auto-scroll (respect user scroll position)
  useEffect(() => {
    if (!userScrolled) bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length, loading, userScrolled]);

  function handleScroll() {
    const el = scrollRef.current;
    if (!el) return;
    const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 40;
    setUserScrolled(!atBottom);
  }

  // Auto-grow textarea
  const resize = useCallback(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 96) + "px";
  }, []);
  useEffect(() => { resize(); }, [input, resize]);

  // Rate limiting
  function checkRate(): boolean {
    const now = Date.now();
    const recent = sendTimes.filter(t => now - t < 30000);
    if (recent.length >= 5) {
      setRateLimited(true);
      setTimeout(() => setRateLimited(false), 5000);
      return false;
    }
    setSendTimes([...recent, now]);
    return true;
  }

  async function send(text?: string) {
    const msg = (text || input).trim();
    if (!msg || loading) return;
    if (!checkRate()) return;
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    setUserScrolled(false);

    const updated: Message[] = [...messages, { role: "child", text: msg, ts: Date.now() }];
    setMessages(updated);
    setLoading(true);

    try {
      const history = updated.map(m => ({ role: m.role, text: m.text }));
      const resp = await tutor.message(activityId, childId, msg, history);
      setMessages(prev => [...prev, {
        role: "tutor", text: resp.message, hints: resp.hints || [], ts: Date.now(),
      }]);
    } catch {
      setMessages(prev => [...prev, {
        role: "tutor",
        text: "I'm having trouble thinking right now. Try asking again in a moment.",
        ts: Date.now(),
      }]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  }

  function handleClose() {
    const msgCount = messages.filter(m => m.role === "child").length;
    if (msgCount >= 5) {
      setMessages(prev => [...prev, { role: "tutor", text: "You asked great questions today. I'll be here if you need me.", ts: Date.now() }]);
      setTimeout(onClose, 1500);
    } else {
      onClose;
      onClose();
    }
  }

  // Should we show timestamp? Only if > 5 min gap from previous
  function showTime(idx: number): boolean {
    if (idx === 0) return false;
    return messages[idx].ts - messages[idx - 1].ts > 300000;
  }

  // Message grouping: same sender within 60s
  function isGrouped(idx: number): boolean {
    if (idx === 0) return false;
    return messages[idx].role === messages[idx - 1].role
      && messages[idx].ts - messages[idx - 1].ts < 60000;
  }

  const accent = subjectColor || "var(--color-accent)";

  // Quick replies for younger children
  const quickReplies = loading ? [] : [
    "I don't understand",
    "Can you explain differently?",
    "I think I got it",
  ];

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/20 z-40" onClick={handleClose} aria-hidden="true" />

      {/* Panel — slides up from bottom */}
      <div className="fixed inset-x-0 bottom-0 z-50 flex flex-col bg-[#FFFDF8] rounded-t-2xl shadow-2xl"
        style={{ height: "60vh", minHeight: 320 }}
        role="dialog" aria-label="Tutor chat">

        {/* Drag handle */}
        <div className="flex justify-center pt-2 pb-1">
          <div className="w-10 h-1 rounded-full bg-(--color-border)" />
        </div>

        {/* Header */}
        <div className="flex items-center justify-between px-5 py-2 border-b border-(--color-border)/50">
          <div>
            <h3 className="text-sm font-medium text-(--color-text)">Your Guide</h3>
            {activityTitle && (
              <p className="text-[10px] text-(--color-text-tertiary) truncate max-w-[200px]">
                Helping with: {activityTitle}
                {currentStep !== undefined && totalSteps ? ` (step ${currentStep + 1}/${totalSteps})` : ""}
              </p>
            )}
          </div>
          <button onClick={handleClose}
            className="w-10 h-10 rounded-full flex items-center justify-center text-(--color-text-tertiary) hover:bg-(--color-page) min-h-[44px] min-w-[44px]"
            aria-label="Close tutor">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages */}
        <div ref={scrollRef} onScroll={handleScroll}
          className="flex-1 overflow-y-auto px-5 py-4 space-y-1" role="log" aria-live="polite">
          {messages.map((msg, i) => {
            const grouped = isGrouped(i);
            const timeGap = showTime(i);

            return (
              <div key={i}>
                {/* Timestamp gap */}
                {timeGap && (
                  <div className="text-center text-[9px] text-(--color-text-tertiary) py-2">
                    {new Date(msg.ts).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })}
                  </div>
                )}

                {msg.role === "tutor" ? (
                  <div className={`max-w-[85%] ${grouped ? "mt-0.5" : "mt-3"}`} role="status">
                    <div className="bg-[#F5F0E6] text-(--color-text) rounded-2xl rounded-bl-md px-4 py-3 text-[15px] leading-relaxed">
                      {msg.text}
                    </div>

                    {/* Hint blocks */}
                    {msg.hints && msg.hints.length > 0 && !revealedHints.has(i) && (
                      <button onClick={() => setRevealedHints(p => new Set([...p, i]))}
                        className="flex items-center gap-1.5 mt-2 ml-1 text-xs text-(--color-warning) hover:underline min-h-[36px]"
                        aria-label="Reveal hint">
                        <span aria-hidden="true">{"\uD83D\uDCA1"}</span> Hint available
                      </button>
                    )}
                    {msg.hints && revealedHints.has(i) && (
                      <div className="mt-2 bg-(--color-warning-light) border-l-2 border-(--color-warning) rounded-r-xl px-3 py-2 text-xs text-(--color-warning) leading-relaxed">
                        {msg.hints.map((h, hi) => <span key={hi}>{hi > 0 && " "}{h}</span>)}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className={`flex justify-end ${grouped ? "mt-0.5" : "mt-3"}`}>
                    <div className="max-w-[85%] rounded-2xl rounded-br-md px-4 py-3 text-[15px] leading-relaxed text-white"
                      style={{ background: accent }}>
                      {msg.text}
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {/* Typing indicator */}
          {loading && (
            <div className="max-w-[85%] mt-3">
              <div className="bg-[#F5F0E6] rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-1.5 w-16">
                {[0, 150, 300].map(d => (
                  <span key={d} className="w-1.5 h-1.5 rounded-full bg-(--color-text-tertiary)"
                    style={{ animation: "typing-pulse 1s ease-in-out infinite", animationDelay: `${d}ms` }} />
                ))}
              </div>
            </div>
          )}

          {/* Rate limit message */}
          {rateLimited && (
            <div className="text-center text-xs text-(--color-text-secondary) py-2 italic">
              Take a breath. I'm reading what you wrote.
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Quick replies */}
        {quickReplies.length > 0 && messages.length < 6 && (
          <div className="px-5 pb-2 flex gap-2 overflow-x-auto">
            {quickReplies.map(qr => (
              <button key={qr} onClick={() => send(qr)}
                className="shrink-0 px-3 py-1.5 text-xs border border-(--color-border) rounded-full text-(--color-text-secondary) hover:bg-(--color-page) min-h-[36px]">
                {qr}
              </button>
            ))}
          </div>
        )}

        {/* Input */}
        <div className="p-3 border-t border-(--color-border)/50 bg-white">
          <div className="flex items-end gap-2">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your question or answer..."
              rows={1}
              className="flex-1 px-4 py-3 text-[15px] border border-(--color-border) rounded-2xl bg-white text-(--color-text) resize-none focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 leading-relaxed min-h-[44px]"
              style={{ maxHeight: 96 }}
              aria-label="Message to tutor"
            />
            <button onClick={() => send()} disabled={!input.trim() || loading || rateLimited}
              className="w-11 h-11 rounded-full flex items-center justify-center shrink-0 text-white disabled:opacity-30"
              style={{ background: accent }}
              aria-label="Send message">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
              </svg>
            </button>
          </div>
        </div>

        <style>{`
          @keyframes typing-pulse {
            0%, 60%, 100% { opacity: 0.3; }
            30% { opacity: 1; }
          }
          @media (prefers-reduced-motion: reduce) {
            @keyframes typing-pulse { from, to { opacity: 0.6; } }
          }
        `}</style>
      </div>
    </>
  );
}
