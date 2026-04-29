"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";
import { MetheanLogo, MetheanMark } from "@/components/Brand";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

// Minimal stroke-based feature icons. 24x24 viewBox, currentColor
// stroke at width 1.5, no fill — same visual weight as the rest of
// the design system.
const SVG_PROPS = {
  width: 24,
  height: 24,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.5,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
};

function FeatureShield() {
  // Philosophy-driven AI / governance
  return (
    <svg {...SVG_PROPS}>
      <path d="M12 2L4 6v6c0 5 3.5 9.5 8 11 4.5-1.5 8-6 8-11V6z" />
    </svg>
  );
}

function FeatureDoc() {
  // All 50 states — document with a checkmark
  return (
    <svg {...SVG_PROPS}>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <path d="M14 2v6h6" />
      <path d="M9 14l2 2 4-4" />
    </svg>
  );
}

function FeatureFamily() {
  // Multi-child family — two circles (heads) with shoulders
  return (
    <svg {...SVG_PROPS}>
      <circle cx="9" cy="9" r="3" />
      <circle cx="16" cy="9" r="3" />
      <path d="M4 20c0-3 2-5 5-5" />
      <path d="M20 20c0-3-2-5-5-5" />
    </svg>
  );
}

function FeatureChart() {
  // Mastery tracking — upward trending line
  return (
    <svg {...SVG_PROPS}>
      <polyline points="3 17 9 11 13 15 21 7" />
      <polyline points="14 7 21 7 21 14" />
    </svg>
  );
}

function FeatureWrench() {
  // Vocational & trades — wrench
  return (
    <svg {...SVG_PROPS}>
      <path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.7 2.7-2.6-.4-.4-2.6z" />
    </svg>
  );
}

function FeatureLightbulb() {
  // Child learning space — lightbulb
  return (
    <svg {...SVG_PROPS}>
      <path d="M12 2a7 7 0 0 1 4 12.7c-.7.5-1 1.3-1 2.1V18H9v-1.2c0-.8-.3-1.6-1-2.1A7 7 0 0 1 12 2z" />
      <path d="M9 18h6" />
      <path d="M10 22h4" />
    </svg>
  );
}

const features = [
  { icon: <FeatureShield />, title: "Philosophy-Driven AI", desc: "Your values shape every recommendation." },
  { icon: <FeatureDoc />, title: "All 50 States + DC", desc: "Automatic hour tracking and document generation." },
  { icon: <FeatureFamily />, title: "Multi-Child Family", desc: "See everyone on one screen." },
  { icon: <FeatureChart />, title: "Mastery Tracking", desc: "FSRS v6 spaced repetition knows what your child knows." },
  { icon: <FeatureWrench />, title: "Vocational & Trades", desc: "Welding, electrical, automotive. Certification tracking." },
  { icon: <FeatureLightbulb />, title: "Child Learning Space", desc: "Personalized themes, Socratic tutor." },
];

const steps = [
  { num: "01", title: "Set Your Rules.", body: "Choose your educational philosophy. Define content boundaries. Set how much authority you give the AI. The system creates constitutional governance rules that AI cannot override." },
  { num: "02", title: "AI Builds, You Approve.", body: "METHEAN generates curriculum, weekly plans, and teaching guidance tailored to your family. Everything routes through your governance rules before reaching your child. Nothing happens without your authorization." },
  { num: "03", title: "Watch Mastery Grow.", body: "Spaced repetition tracks what your child actually knows, not just what they completed. Five intelligence engines learn your child's patterns. A family at month three gets a qualitatively different experience than day one." },
];

const comparisons = [
  ["Track completion", "Track mastery with spaced repetition"],
  ["AI decides", "AI recommends, you decide"],
  ["Generic curriculum", "Philosophy-driven, tailored to your family"],
  ["No compliance help", "51-state compliance with document generation"],
  ["No audit trail", "Full governance trail, every decision logged"],
  ["Same experience forever", "Intelligence compounds over time"],
];

export default function LandingPage() {
  const router = useRouter();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    document.title = "METHEAN — A Learning Operating System for Families";
    auth.me()
      .then(() => router.replace("/dashboard"))
      .catch(() => setChecking(false));
  }, [router]);

  if (checking) return <div className="min-h-screen bg-(--color-page)" />;

  return (
    <div className="min-h-screen" style={{ fontFamily: "var(--font-sans)" }}>
      {/* ── Header ── */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-[rgba(250,250,248,0.85)] border-b border-[rgba(0,0,0,0.04)]">
        <div className="max-w-[1200px] mx-auto px-6 py-3 flex items-center justify-between">
          <MetheanLogo markSize={24} wordmarkHeight={12} color="#0F1B2D" gap={8} />
          <nav className="hidden sm:flex items-center gap-8">
            <a href="#features" className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors">Features</a>
            <a href="#pricing" className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors">Pricing</a>
          </nav>
          <div className="flex items-center gap-4">
            <a href="/auth" className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors">Sign In</a>
            <Button variant="gold" size="md" onClick={() => router.push("/auth?mode=register")}>Get Started</Button>
          </div>
        </div>
      </header>

      {/* ── Hero ── */}
      <section className="min-h-[90vh] flex items-center justify-center px-6 pt-20 bg-(--color-page)">
        <div className="max-w-[720px] text-center">
          <h1 className="text-[36px] sm:text-[48px] font-semibold leading-[1.08] tracking-[-0.035em] text-(--color-text) mb-5">
            A learning operating system<br className="hidden sm:block" /> for families who homeschool.
          </h1>
          <p className="text-[18px] sm:text-[20px] text-(--color-text-secondary) leading-[1.6] max-w-[520px] mx-auto mb-10">
            You set the rules. AI follows them. Every decision is yours.
          </p>
          <Button variant="gold" size="lg" onClick={() => router.push("/auth?mode=register")}>
            Start Free — 30 Day Trial
          </Button>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section className="py-24 px-6 bg-(--color-page)">
        <div className="max-w-[1100px] mx-auto">
          <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) text-center mb-3">How It Works</p>
          <p className="text-[22px] font-medium text-(--color-text) text-center mb-12 tracking-tight">Three steps to sovereign education.</p>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {steps.map((s) => (
              <div key={s.num} className="bg-(--color-surface) rounded-[16px] p-7 border border-(--color-border)">
                <div className="relative w-14 h-14 mb-4">
                  <div className="absolute inset-0 rounded-full" style={{ background: "rgba(74,111,165,0.08)" }} />
                  <span className="absolute inset-0 flex items-center justify-center text-[28px] font-bold text-(--color-accent)">{s.num}</span>
                </div>
                <h3 className="text-[17px] font-semibold text-(--color-text) mb-2">{s.title}</h3>
                <p className="text-[14px] text-(--color-text-secondary) leading-relaxed">{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Built by a Homeschool Family ── */}
      {/* Replaces the previous testimonials block. METHEAN is pre-
          revenue with no shipped users; instead of inventing quotes
          we lead with the founder's principles. */}
      <section className="py-20 px-6" style={{ background: "#F5F1E8" }}>
        <div className="max-w-[640px] mx-auto">
          <Card padding="p-8 sm:p-10" className="text-center">
            <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) mb-3">
              Built by a Homeschool Family
            </p>
            <h2
              className="text-[24px] sm:text-[28px] font-semibold tracking-tight mb-6"
              style={{ color: "var(--color-brand-navy)" }}
            >
              Three principles, written before a single line of code.
            </h2>
            <ul className="space-y-3 text-left max-w-[420px] mx-auto">
              {[
                "Parents govern. AI serves.",
                "Every decision is auditable.",
                "Your data stays in your household.",
              ].map((line) => (
                <li
                  key={line}
                  className="flex items-start gap-3 text-[15px] text-(--color-text-secondary) leading-relaxed"
                >
                  <span
                    className="mt-2 h-1.5 w-1.5 rounded-full shrink-0"
                    style={{ background: "var(--gold)" }}
                    aria-hidden="true"
                  />
                  {line}
                </li>
              ))}
            </ul>
          </Card>
        </div>
      </section>

      {/* ── See It In Action ── */}
      <section className="px-6 py-24" style={{ background: "#0F1B2D" }}>
        <div className="max-w-[1100px] mx-auto">
          <p className="text-[13px] uppercase tracking-[0.1em] text-white/40 text-center mb-3">See It In Action</p>
          <p className="text-[22px] font-medium text-white text-center mb-12 tracking-tight">Three experiences. One platform.</p>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Parent Dashboard mockup */}
            <div className="bg-[#1A2740] rounded-[16px] overflow-hidden border border-white/[0.05]">
              <div className="h-[200px] bg-[#0F1B2D] p-4 relative">
                <div className="h-2 w-full bg-[#1A2740] rounded mb-4" />
                <div className="flex gap-2 justify-center mb-4">
                  {[1,2,3].map(n => (
                    <div key={n} className="w-[60px] h-[40px] bg-[#1A2740] rounded-lg flex items-center justify-center">
                      <svg width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="none" stroke="rgba(74,111,165,0.4)" strokeWidth="2" /><circle cx="10" cy="10" r="8" fill="none" stroke="rgba(74,111,165,0.8)" strokeWidth="2" strokeDasharray={`${n*12} 50`} /></svg>
                    </div>
                  ))}
                </div>
                <div className="space-y-2 px-2">
                  <div className="h-2 w-[80%] bg-white/5 rounded" />
                  <div className="h-2 w-[60%] bg-white/5 rounded" />
                  <div className="h-2 w-[70%] bg-white/5 rounded" />
                </div>
                <div className="absolute top-3 right-3 w-2 h-2 rounded-full" style={{ background: "#C6A24E" }} />
              </div>
              <div className="p-5">
                <p className="text-[15px] text-white font-medium mb-1">Parent Dashboard</p>
                <p className="text-[13px] text-white/40 leading-relaxed">See every child&apos;s progress, pending approvals, alerts, and mastery trends. One screen. Complete control.</p>
              </div>
            </div>
            {/* Child Learning Space mockup */}
            <div className="bg-[#1A2740] rounded-[16px] overflow-hidden border border-white/[0.05]">
              <div className="h-[200px] p-4 relative" style={{ background: "linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%)" }}>
                <div className="flex justify-center mb-3">
                  <div className="w-8 h-8 rounded-full bg-white/30 flex items-center justify-center text-sm">🦉</div>
                </div>
                <div className="flex justify-center mb-4">
                  <svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="rgba(0,0,0,0.1)" strokeWidth="3" /><circle cx="20" cy="20" r="16" fill="none" stroke="rgba(45,106,79,0.5)" strokeWidth="3" strokeDasharray="60 100" transform="rotate(-90 20 20)" /></svg>
                </div>
                <div className="space-y-2 px-4">
                  {[1,2,3].map(n => (
                    <div key={n} className="h-8 bg-white/15 rounded-lg" />
                  ))}
                </div>
              </div>
              <div className="p-5">
                <p className="text-[15px] text-white font-medium mb-1">Child&apos;s Learning Space</p>
                <p className="text-[13px] text-white/40 leading-relaxed">Themed backgrounds, guided lessons, Socratic tutoring, and celebration on completion. Designed for children, not adults.</p>
              </div>
            </div>
            {/* Governance Trail mockup */}
            <div className="bg-[#1A2740] rounded-[16px] overflow-hidden border border-white/[0.05]">
              <div className="h-[200px] bg-[#0F1B2D] p-4">
                <div className="space-y-4 pt-4">
                  {[["#2D6A4F","80%"],["#C6A24E","65%"],["#A63D40","55%"]].map(([color,w],i) => (
                    <div key={i} className="flex items-center gap-3 px-2">
                      <div className="w-[6px] h-[6px] rounded-full shrink-0" style={{ background: color }} />
                      <div className="h-2 rounded" style={{ width: w, background: "rgba(255,255,255,0.08)" }} />
                      <span className="text-[8px] text-white/20 shrink-0">2:14pm</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="p-5">
                <p className="text-[15px] text-white font-medium mb-1">Governance Trail</p>
                <p className="text-[13px] text-white/40 leading-relaxed">Every AI decision logged. Every override recorded. Every rule enforcement visible. Your proof of sovereignty.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Features (dark bento) ── */}
      <section id="features" className="px-6 py-24" style={{ background: "#0F1B2D" }}>
        <div className="max-w-[1100px] mx-auto">
          <p className="text-[13px] uppercase tracking-[0.1em] text-white/40 text-center mb-3">Features</p>
          <p className="text-[22px] font-medium text-white text-center max-w-[600px] mx-auto mb-12 tracking-tight">
            Navigate your family&apos;s education with confidence.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Large sovereignty card */}
            <div className="sm:row-span-2 bg-[#1A2740] border border-white/[0.05] rounded-[16px] p-7 hover:border-white/[0.10] transition-all duration-200">
              <div className="text-2xl mb-3">🛡️</div>
              <div className="text-white font-medium text-[17px] mb-2">Parent Sovereignty</div>
              <div className="text-white/50 text-[14px] leading-relaxed">
                Constitutional rules that AI cannot override. You define the boundaries.
                The system respects them. Every decision logged. Full transparency.
              </div>
            </div>
            {features.map((f) => (
              <div key={f.title} className="bg-[#1A2740] border border-white/[0.05] rounded-[16px] p-6 hover:border-white/[0.10] transition-all duration-200">
                {/* Icon wrapper sets the gold currentColor that the
                    new stroke-based SVGs inherit; text-xl on the
                    previous emoji wrapper was a sizing tweak that
                    doesn't apply to a fixed-size 24x24 svg. */}
                <div className="mb-2 text-[color:var(--gold)]">{f.icon}</div>
                <div className="text-white font-medium text-[15px] mb-1">{f.title}</div>
                <div className="text-white/40 text-[13px] leading-relaxed">{f.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Built Different ── */}
      <section className="py-20 px-6 bg-(--color-page)">
        <div className="max-w-[900px] mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-0 border border-(--color-border) rounded-[16px] overflow-hidden bg-(--color-surface)">
            {/* Headers */}
            <div className="px-6 py-4 border-b border-(--color-border) bg-(--color-page)">
              <p className="text-[15px] font-medium text-(--color-text-secondary)">Other platforms</p>
            </div>
            <div className="px-6 py-4 border-b border-(--color-border) bg-(--color-page)">
              <p className="text-[15px] font-medium" style={{ color: "#C6A24E" }}>METHEAN</p>
            </div>
            {/* Rows */}
            {comparisons.map(([left, right], i) => (
              <div key={i} className="contents">
                <div className={`px-6 py-3.5 flex items-center gap-2 text-[14px] text-(--color-text-secondary) ${i < comparisons.length - 1 ? "border-b border-(--color-border)" : ""}`}>
                  <span className="text-(--color-text-tertiary)">✗</span> {left}
                </div>
                <div className={`px-6 py-3.5 flex items-center gap-2 text-[14px] text-(--color-text) ${i < comparisons.length - 1 ? "border-b border-(--color-border)" : ""}`}>
                  <span style={{ color: "#C6A24E" }}>✓</span> {right}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Founder ── */}
      <section className="py-24 px-6 bg-(--color-page)">
        <div className="max-w-2xl mx-auto text-center">
          <p className="text-[22px] font-medium text-(--color-text) mb-6 tracking-tight">Built by a homeschool father of six.</p>
          <p className="text-[15px] text-(--color-text-secondary) leading-relaxed mb-6">
            METHEAN was born from the conviction that families, not institutions, should control
            their children&apos;s education. Every line of code is written with one principle:
            AI advises, parents govern.
          </p>
          <p className="text-[15px] font-medium text-(--color-text)">— Zack Fava, Founder</p>
        </div>
      </section>

      {/* ── Pricing ── */}
      <section id="pricing" className="px-6 py-24 bg-(--color-surface)">
        <div className="max-w-[420px] mx-auto text-center">
          <h2 className="text-[24px] font-semibold tracking-tight text-(--color-text) mb-2">Simple pricing.</h2>
          <p className="text-[15px] text-(--color-text-secondary) mb-8">One plan. Everything included.</p>
          <Card padding="p-10" className="text-center">
            <div className="text-[40px] font-bold tracking-tight text-(--color-text)">
              $99<span className="text-[18px] font-normal text-(--color-text-secondary)">/month</span>
            </div>
            <div className="text-[14px] text-(--color-text-tertiary) mt-1 mb-6">30-day free trial</div>
            <div className="space-y-2 text-left max-w-[280px] mx-auto mb-8">
              {["Unlimited children", "All 50 states + DC compliance", "AI curriculum builder", "Full governance suite", "Document generation", "Vocational pathways"].map((f) => (
                <div key={f} className="text-[14px] text-(--color-text) flex items-center gap-2">
                  <span className="text-(--color-success)">✓</span> {f}
                </div>
              ))}
            </div>
            <Button variant="gold" size="lg" className="w-full" onClick={() => router.push("/auth?mode=register")}>
              Start Your Free Trial
            </Button>
          </Card>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-(--color-border) py-8 px-6 bg-(--color-page)">
        <div className="max-w-[1100px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <MetheanLogo markSize={18} wordmarkHeight={9} color="#9A9A9A" gap={6} />
          <div className="flex items-center gap-4 text-[12px] text-(--color-text-tertiary)">
            <a href="/privacy" className="hover:underline">Privacy</a>
            <a href="/terms" className="hover:underline">Terms</a>
            <span>·</span>
            <span>© 2026 METHEAN, Inc. · zack@methean.io</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
