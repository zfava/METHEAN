"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { MetheanLogo, MetheanMark, MetheanWordmark } from "@/components/Brand";

export default function LandingPage() {
  const router = useRouter();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    document.title = "METHEAN — A Learning Operating System for Families";
    // Check if already authenticated
    const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    fetch(`${API}/auth/me`, { credentials: "include" })
      .then((r) => { if (r.ok) router.replace("/dashboard"); else setChecking(false); })
      .catch(() => setChecking(false));
  }, [router]);

  if (checking) return <div className="min-h-screen bg-(--color-page)" />;

  return (
    <div className="min-h-screen bg-(--color-page)" style={{ fontFamily: "var(--font-sans)" }}>
      {/* ── Header ── */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-(--color-page)/90 backdrop-blur border-b border-(--color-border)/50">
        <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
          <MetheanLogo markSize={24} wordmarkHeight={12} color="#0F1B2D" gap={8} />
          <div className="flex items-center gap-4">
            <a href="/auth" className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors">Sign In</a>
            <a href="/auth?mode=register"
              className="px-4 py-2 text-sm font-medium text-white rounded-[6px] hover:opacity-90 transition-opacity"
              style={{ background: "#C6A24E" }}>
              Get Started Free
            </a>
          </div>
        </div>
      </header>

      {/* ── Hero ── */}
      <section className="pt-28 pb-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-(--color-text) leading-tight mb-4">
            A learning operating system<br className="hidden sm:block" /> for families who homeschool.
          </h1>
          <p className="text-lg sm:text-xl text-(--color-text-secondary) mb-8 max-w-xl mx-auto">
            You set the rules. AI follows them. Every decision is yours.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="/auth?mode=register"
              className="px-8 py-3.5 text-base font-semibold text-white rounded-[10px] hover:opacity-90 transition-opacity shadow-sm"
              style={{ background: "#C6A24E" }}>
              Start Free — 30 Day Trial
            </a>
            <a href="#how-it-works" className="text-sm font-medium text-(--color-accent) hover:underline">
              See How It Works ↓
            </a>
          </div>

          {/* Dashboard preview */}
          <div className="mt-16 mx-auto max-w-2xl bg-(--color-surface) rounded-[16px] border border-(--color-border) shadow-lg p-6 text-left">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-3 h-3 rounded-full bg-(--color-danger)" />
              <div className="w-3 h-3 rounded-full bg-(--color-warning)" />
              <div className="w-3 h-3 rounded-full bg-(--color-success)" />
              <span className="text-[10px] text-(--color-text-tertiary) ml-2">Governance Dashboard</span>
            </div>
            <div className="grid grid-cols-4 gap-3 mb-4">
              {[
                { label: "Parent Control", value: "87%", color: "#2D6A4F" },
                { label: "AI Oversight", value: "Full", color: "#4A6FA5" },
                { label: "Pending", value: "0", color: "#2D6A4F" },
                { label: "Constitutional", value: "3", color: "#8B7355" },
              ].map((m) => (
                <div key={m.label} className="bg-(--color-page) rounded-[8px] p-3 text-center">
                  <div className="text-lg font-bold" style={{ color: m.color }}>{m.value}</div>
                  <div className="text-[9px] text-(--color-text-tertiary)">{m.label}</div>
                </div>
              ))}
            </div>
            <div className="flex gap-3">
              <div className="flex-1 bg-(--color-success-light) rounded-[6px] p-2 text-center">
                <div className="text-xs font-bold text-(--color-success)">24</div>
                <div className="text-[8px] text-(--color-success)">Auto-approved</div>
              </div>
              <div className="flex-1 bg-(--color-warning-light) rounded-[6px] p-2 text-center">
                <div className="text-xs font-bold text-(--color-warning)">0</div>
                <div className="text-[8px] text-(--color-warning)">Queued</div>
              </div>
              <div className="flex-1 bg-(--color-success-light) rounded-[6px] p-2 text-center">
                <div className="text-xs font-bold text-(--color-success)">8</div>
                <div className="text-[8px] text-(--color-success)">Parent OK</div>
              </div>
              <div className="flex-1 bg-(--color-danger-light) rounded-[6px] p-2 text-center">
                <div className="text-xs font-bold text-(--color-danger)">1</div>
                <div className="text-[8px] text-(--color-danger)">Rejected</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section id="how-it-works" className="py-20 px-6 bg-(--color-surface)">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-semibold text-(--color-text) text-center mb-12">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { num: "1", title: "Set your philosophy", desc: "Classical, Charlotte Mason, Montessori, or your own blend. Your values shape every AI recommendation.", icon: "📖" },
              { num: "2", title: "AI builds your plan", desc: "Year-long curriculum tailored to your values and each child's pace, age, and learning style.", icon: "🗓️" },
              { num: "3", title: "You govern every decision", desc: "Constitutional rules, approval queue, full audit trail. AI advises, you decide.", icon: "🛡️" },
            ].map((step) => (
              <div key={step.num} className="text-center">
                <div className="text-4xl mb-3">{step.icon}</div>
                <div className="text-xs font-bold text-(--color-accent) uppercase tracking-widest mb-1">Step {step.num}</div>
                <h3 className="text-base font-semibold text-(--color-text) mb-2">{step.title}</h3>
                <p className="text-sm text-(--color-text-secondary) leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-semibold text-(--color-text) text-center mb-12">Built for Real Families</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { icon: "🛡️", title: "Parent Sovereignty", desc: "Constitutional rules that AI cannot override. You define the boundaries." },
              { icon: "📚", title: "Philosophy-Driven AI", desc: "Your educational values shape every curriculum, activity, and assessment." },
              { icon: "📋", title: "51-State Compliance", desc: "Automatic hour tracking, document generation, and state-specific requirements." },
              { icon: "👨‍👩‍👧‍👦", title: "Multi-Child Family", desc: "See everyone's schedule on one screen. Manage 1 child or 10." },
              { icon: "🧒", title: "Child Learning Space", desc: "Personalized themes, Socratic AI tutor, 6 activity views." },
              { icon: "📊", title: "Mastery Tracking", desc: "FSRS v6 spaced repetition with DAG-based curriculum maps." },
            ].map((f) => (
              <div key={f.title} className="bg-(--color-surface) rounded-[10px] border border-(--color-border) p-5">
                <div className="text-2xl mb-2">{f.icon}</div>
                <h3 className="text-sm font-semibold text-(--color-text) mb-1">{f.title}</h3>
                <p className="text-xs text-(--color-text-secondary) leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Founder ── */}
      <section className="py-20 px-6 bg-(--color-surface)">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-2xl font-semibold text-(--color-text) mb-6">Built by a homeschool father of six.</h2>
          <p className="text-sm text-(--color-text-secondary) leading-relaxed mb-4">
            METHEAN was born from the conviction that families, not institutions, should control
            their children's education. After years of homeschooling and building mission-critical
            systems, I built the platform I wished existed.
          </p>
          <p className="text-sm text-(--color-text-secondary) leading-relaxed mb-6">
            Every line of code is written with one principle: AI advises, parents govern.
            Your values are not suggestions to the algorithm — they are constitutional law.
          </p>
          <p className="text-sm font-medium text-(--color-text)">— Zack Fava, Founder</p>
        </div>
      </section>

      {/* ── Pricing ── */}
      <section id="pricing" className="py-20 px-6">
        <div className="max-w-lg mx-auto text-center">
          <h2 className="text-2xl font-semibold text-(--color-text) mb-2">Simple pricing. No surprises.</h2>
          <p className="text-sm text-(--color-text-secondary) mb-8">One plan. Everything included. 30-day free trial.</p>

          <div className="bg-(--color-surface) rounded-[16px] border-2 border-(--color-border) p-8 text-left">
            <div className="text-center mb-6">
              <span className="text-3xl font-bold text-(--color-text)">$29</span>
              <span className="text-sm text-(--color-text-secondary)">/month</span>
              <div className="text-xs text-(--color-text-tertiary) mt-1">Family Plan</div>
            </div>

            <div className="space-y-3 mb-8">
              {[
                "Unlimited children",
                "All 51 states compliance",
                "AI curriculum builder",
                "Full governance suite",
                "Document generation (IHIP, transcripts)",
                "Reading log and resource library",
                "30-day free trial",
              ].map((f) => (
                <div key={f} className="flex items-center gap-2.5 text-sm text-(--color-text)">
                  <svg className="w-4 h-4 text-(--color-success) shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  {f}
                </div>
              ))}
            </div>

            <a href="/auth?mode=register"
              className="block w-full text-center px-6 py-3.5 text-base font-semibold text-white rounded-[10px] hover:opacity-90 transition-opacity"
              style={{ background: "#C6A24E" }}>
              Start Your Free Trial
            </a>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-(--color-border) py-10 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <MetheanLogo markSize={20} wordmarkHeight={10} color="#9A9A9A" gap={6} />
            <div className="flex items-center gap-6 text-xs text-(--color-text-tertiary)">
              <a href="#how-it-works" className="hover:text-(--color-text-secondary)">Features</a>
              <a href="#pricing" className="hover:text-(--color-text-secondary)">Pricing</a>
              <a href="/auth" className="hover:text-(--color-text-secondary)">Sign In</a>
              <a href="/auth?mode=register" className="hover:text-(--color-text-secondary)">Register</a>
            </div>
            <p className="text-[10px] text-(--color-text-tertiary) italic">Built with conviction. Governed by families.</p>
          </div>
          <div className="text-center mt-6 text-[10px] text-(--color-text-tertiary)">
            © 2026 Spartan Solutions · zack@spartansolutions.co
          </div>
        </div>
      </footer>
    </div>
  );
}
