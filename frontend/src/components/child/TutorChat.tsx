"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { streamTutorMessage } from "@/lib/api";
import { CompanionAvatar } from "@/components/CompanionAvatar";
import { VoiceModeUI } from "@/components/child/voice/VoiceModeUI";
import { usePersonalization } from "@/lib/PersonalizationProvider";
import { useTutorVoice } from "@/lib/useTutorVoice";
import { useVoiceConversation } from "@/lib/useVoiceConversation";

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
  // Companion identity from the kid's personalization profile.
  // Empty strings degrade to neutral fallbacks; the chat never
  // refers to a brand-named "Methean" voice now that personas
  // exist.
  const { profile } = usePersonalization();
  const [voiceState, voiceControls] = useTutorVoice();
  const companionName = profile.companion_name || "Your Companion";
  const companionVoice = profile.companion_voice || "default_warm";
  const dialogLabel = profile.companion_name
    ? `${profile.companion_name} chat`
    : "Companion chat";

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
  const [isStreaming, setIsStreaming] = useState(false);
  const [voiceMode, setVoiceMode] = useState(false);
  // Voice-mode interaction style. Reads from the kid's
  // ChildPreferences.personalization JSONB ("voice_mode_style" key);
  // defaults to tap-toggle, which is the easier path for kids who
  // can't reliably hold a button.
  const voiceModeStyle: "press_hold" | "tap_toggle" =
    ((profile as unknown as { voice_mode_style?: string }).voice_mode_style as
      | "press_hold"
      | "tap_toggle"
      | undefined) ?? "tap_toggle";
  const [revealedHints, setRevealedHints] = useState<Set<number>>(new Set());
  const [userScrolled, setUserScrolled] = useState(false);
  const [sendTimes, setSendTimes] = useState<number[]>([]);
  const [rateLimited, setRateLimited] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const openerRef = useRef<HTMLElement | null>(null);

  // Voice-mode orchestrator. Reuses the existing streamTutorMessage
  // path via a thin adapter so voice and text mode share one tutor
  // surface; the message list is updated in-place so switching back
  // to text mode reveals the full history.
  const sendToTutor = useCallback(
    async (transcript: string): Promise<string> => {
      // Append the kid's transcript and a placeholder tutor message
      // before kicking off the stream so the text history reflects
      // the voice exchange.
      let accumulatedText = "";
      const childMsg: Message = { role: "child", text: transcript, ts: Date.now() };
      const tutorMsg: Message = { role: "tutor", text: "", ts: Date.now() };
      setMessages((prev) => [...prev, childMsg, tutorMsg]);
      const history = [...messages, childMsg].map((m) => ({ role: m.role, text: m.text }));
      try {
        await streamTutorMessage(
          activityId,
          childId,
          transcript,
          history,
          (token) => {
            accumulatedText += token;
            setMessages((prev) => {
              const copy = [...prev];
              const last = copy[copy.length - 1];
              if (last?.role === "tutor") copy[copy.length - 1] = { ...last, text: accumulatedText };
              return copy;
            });
          },
          () => {
            /* completion handled by the orchestrator */
          },
          () => {
            /* error surfaces via the orchestrator's catch path */
          },
          { voiceMode: true },
        );
      } catch (e) {
        // Surface as the rejection the orchestrator expects.
        throw e instanceof Error ? e : new Error(String(e));
      }
      return accumulatedText.trim();
    },
    [activityId, childId, messages],
  );

  const [convState, convControls] = useVoiceConversation({
    childId,
    sendToTutor,
    onExit: () => setVoiceMode(false),
  });

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

    setIsStreaming(true);
    setMessages(prev => [...prev, { role: "tutor", text: "", ts: Date.now() }]);

    try {
      const history = updated.map(m => ({ role: m.role, text: m.text }));
      let accumulatedText = "";

      await streamTutorMessage(
        activityId, childId, msg, history,
        (token) => {
          accumulatedText += token;
          setMessages(prev => {
            const copy = [...prev];
            const last = copy[copy.length - 1];
            if (last?.role === "tutor") copy[copy.length - 1] = { ...last, text: accumulatedText };
            return copy;
          });
        },
        (hints) => {
          let finalText = "";
          setMessages(prev => {
            const copy = [...prev];
            const last = copy[copy.length - 1];
            if (last?.role === "tutor") {
              let cleanText = last.text;
              if (cleanText.includes("HINT:")) cleanText = cleanText.split("HINT:")[0].trim();
              finalText = cleanText;
              copy[copy.length - 1] = { ...last, text: cleanText, hints };
            }
            return copy;
          });
          setIsStreaming(false);
          setLoading(false);
          // Fire-and-forget TTS playback. The hook handles
          // policy/cap/session-mute and silently no-ops if voice
          // isn't enabled. Use the message timestamp as the
          // correlation id so the speaking indicator can target the
          // right bubble.
          if (finalText) {
            const messageId = `tutor-${Date.now()}`;
            void voiceControls.speak(messageId, finalText);
          }
        },
        (errorMsg) => {
          setMessages(prev => {
            const copy = [...prev];
            const last = copy[copy.length - 1];
            if (last?.role === "tutor") copy[copy.length - 1] = { ...last, text: errorMsg };
            return copy;
          });
          setIsStreaming(false);
          setLoading(false);
        },
      );
    } catch {
      setMessages(prev => {
        const copy = [...prev];
        const last = copy[copy.length - 1];
        if (last?.role === "tutor") copy[copy.length - 1] = { ...last, text: "I'm having trouble thinking right now. Try asking again in a moment." };
        return copy;
      });
      setIsStreaming(false);
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
        style={{ height: "min(80dvh, 600px)", minHeight: 320, paddingBottom: "var(--safe-bottom)" }}
        role="dialog" aria-label={dialogLabel}>

        {/* Drag handle */}
        <div className="flex justify-center pt-2 pb-1">
          <div className="w-10 h-1 rounded-full bg-(--color-border)" />
        </div>

        {voiceMode ? (
          <VoiceModeUI
            companionVoice={companionVoice}
            companionName={companionName}
            state={convState}
            controls={convControls}
            interactionStyle={voiceModeStyle}
            onExit={() => {
              convControls.cancel();
              setVoiceMode(false);
            }}
          />
        ) : (
        <>

        {/* Header */}
        <div className="flex items-center justify-between px-5 py-2 border-b border-(--color-border)/50">
          <div>
            <h3 className="text-sm font-medium text-(--color-text)">{companionName}</h3>
            {activityTitle && (
              <p className="text-[10px] text-(--color-text-tertiary) truncate max-w-[200px]">
                Helping with: {activityTitle}
                {currentStep !== undefined && totalSteps ? ` (step ${currentStep + 1}/${totalSteps})` : ""}
              </p>
            )}
          </div>
          {/* Session voice-mute toggle (in-memory; the kid silences
              TTS for this session without changing policy). */}
          <button
            type="button"
            onClick={() => {
              if (voiceState.isPlaying) voiceControls.stop();
              voiceControls.setSessionMuted(!voiceControls.sessionMuted);
            }}
            aria-pressed={voiceControls.sessionMuted}
            aria-label={voiceControls.sessionMuted ? "Turn voice on" : "Turn voice off"}
            className="w-10 h-10 mr-1 rounded-full flex items-center justify-center text-(--color-text-tertiary) hover:bg-(--color-page) min-h-[44px] min-w-[44px]"
          >
            {voiceControls.sessionMuted ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                <line x1="22" y1="9" x2="16" y2="15" />
                <line x1="16" y1="9" x2="22" y2="15" />
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07" />
              </svg>
            )}
          </button>
          {/* Voice-mode toggle. Hidden when either cap is fully
              exhausted; the conversation-state mirror would 403 the
              first turn anyway. */}
          <button
            type="button"
            onClick={() => setVoiceMode((v) => !v)}
            aria-pressed={voiceMode}
            aria-label={voiceMode ? "Exit voice mode" : "Enter voice mode"}
            className="w-10 h-10 mr-1 rounded-full flex items-center justify-center text-(--color-text-tertiary) hover:bg-(--color-page) min-h-[44px] min-w-[44px]"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
              <path d="M19 10a7 7 0 0 1-14 0" />
              <line x1="12" y1="19" x2="12" y2="23" />
              <line x1="8" y1="23" x2="16" y2="23" />
            </svg>
          </button>
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
                  <div className={`max-w-[85%] md:max-w-[60%] ${grouped ? "mt-0.5" : "mt-3"}`} role="status">
                    <div className="flex items-end gap-2">
                      {/* Persona avatar for the kid's chosen
                          companion. Hidden when the previous message
                          was also from the tutor so consecutive
                          bubbles read as one continuous turn. */}
                      <div
                        className={`shrink-0 h-7 w-7 rounded-full glass border border-(--color-border) flex items-center justify-center text-(--color-accent) ${grouped ? "opacity-0" : ""}`}
                        aria-hidden={grouped ? "true" : undefined}
                      >
                        <CompanionAvatar personaId={companionVoice} size={18} />
                      </div>
                      <div className="glass border border-(--color-border) text-(--color-text) rounded-2xl rounded-bl-md px-4 py-3 text-[15px] leading-relaxed shadow-[var(--shadow-card)]">
                        {msg.text}
                        {isStreaming && i === messages.length - 1 && (
                          <span className="inline-block w-0.5 h-4 bg-(--color-text) ml-0.5 align-text-bottom"
                                style={{ animation: "cursor-blink 0.8s step-end infinite" }} />
                        )}
                      </div>
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
                    <div className="max-w-[85%] md:max-w-[60%] rounded-2xl rounded-br-md px-4 py-3 text-[15px] leading-relaxed text-white"
                      style={{ background: accent }}>
                      {msg.text}
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {/* Typing indicator (hidden during streaming — live text replaces it) */}
          {loading && !isStreaming && (
            <div className="max-w-[85%] mt-3">
              <div className="flex items-end gap-2">
                <div className="shrink-0 h-7 w-7 rounded-full glass border border-(--color-border) flex items-center justify-center text-(--color-accent)" aria-hidden="true">
                  <CompanionAvatar personaId={companionVoice} size={18} />
                </div>
                <div className="glass border border-(--color-border) rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-1.5 w-16 shadow-[var(--shadow-card)]">
                  {[0, 150, 300].map(d => (
                    <span key={d} className="w-1.5 h-1.5 rounded-full bg-(--color-text-tertiary)"
                      style={{ animation: "typing-pulse 1s ease-in-out infinite", animationDelay: `${d}ms` }} />
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Rate limit message */}
          {rateLimited && (
            <div className="text-center text-xs text-(--color-text-secondary) py-2 italic">
              Take a breath. I&apos;m reading what you wrote.
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
              placeholder="Ask me anything about this lesson..."
              rows={1}
              className="flex-1 px-4 py-3 text-[16px] border border-(--color-border) rounded-2xl bg-white text-(--color-text) resize-none focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 leading-relaxed min-h-[44px]"
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
        </>
        )}

        <style>{`
          @keyframes typing-pulse {
            0%, 60%, 100% { opacity: 0.3; }
            30% { opacity: 1; }
          }
          @keyframes cursor-blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
          }
          @media (prefers-reduced-motion: reduce) {
            @keyframes typing-pulse { from, to { opacity: 0.6; } }
            @keyframes cursor-blink { from, to { opacity: 1; } }
          }
        `}</style>
      </div>
    </>
  );
}
