"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";
import { MetheanLogo, MetheanMark } from "@/components/Brand";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

const features = [
  { icon: "📚", title: "Philosophy-Driven AI", desc: "Your values shape every recommendation." },
  { icon: "📋", title: "All 50 States + DC", desc: "Automatic hour tracking and document generation." },
  { icon: "👨‍👩‍👧‍👦", title: "Multi-Child Family", desc: "See everyone on one screen." },
  { icon: "📊", title: "Mastery Tracking", desc: "FSRS v6 spaced repetition knows what your child knows." },
  { icon: "🔧", title: "Vocational & Trades", desc: "Welding, electrical, automotive. Certification tracking." },
  { icon: "🧒", title: "Child Learning Space", desc: "Personalized themes, Socratic tutor." },
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

      {/* ── Features (dark bento) ── */}
      <section id="features" className="px-6 py-24" style={{ background: "#0F1B2D" }}>
        <div className="max-w-[1100px] mx-auto">
          <p className="text-[13px] uppercase tracking-[0.1em] text-white/40 text-center mb-3">Features</p>
          <p className="text-[22px] font-medium text-white text-center max-w-[600px] mx-auto mb-12 tracking-tight">
            Navigate your family's education with confidence.
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
                <div className="text-xl mb-2">{f.icon}</div>
                <div className="text-white font-medium text-[15px] mb-1">{f.title}</div>
                <div className="text-white/40 text-[13px] leading-relaxed">{f.desc}</div>
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
            their children's education. Every line of code is written with one principle:
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
          <div className="text-[12px] text-(--color-text-tertiary)">
            © 2026 Spartan Solutions · zack@spartansolutions.co
          </div>
        </div>
      </footer>
    </div>
  );
}
