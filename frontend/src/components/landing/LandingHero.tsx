"use client";

import { useRouter } from "next/navigation";
import { HeroOrnament } from "./icons";

export function LandingHero() {
  const router = useRouter();
  return (
    <section
      aria-labelledby="hero-headline"
      className="parchment-noise min-h-screen flex items-center justify-center px-6 pt-32 pb-28 bg-[var(--parchment)]"
    >
      <div className="max-w-[1100px] w-full text-center">
        {/* Rotating ornament */}
        <div className="flex justify-center mb-10 text-[var(--gold-deep)]">
          <span className="animate-subtle-rotate inline-flex">
            <HeroOrnament size={56} />
          </span>
        </div>

        {/* Eyebrow */}
        <div className="flex items-center justify-center gap-4 mb-12">
          <span
            aria-hidden="true"
            className="hidden sm:block h-[1px] w-7 bg-[var(--gold-deep)] opacity-50"
          />
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.32em] text-[var(--gold-deep)]">
            Established by Parents · For Parents
          </p>
          <span
            aria-hidden="true"
            className="hidden sm:block h-[1px] w-7 bg-[var(--gold-deep)] opacity-50"
          />
        </div>

        {/* Headline */}
        <h1
          id="hero-headline"
          className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] leading-[0.92] tracking-[-0.025em] text-[clamp(56px,13vw,156px)] mb-10"
        >
          <span className="block mb-1">
            <span className="gold-em">Your</span> children.
          </span>
          <span className="block mb-1">
            <span className="gold-em">Your</span> rules.
          </span>
          <span className="block mb-1">
            <span className="gold-em">Your</span> operating system.
          </span>
        </h1>

        {/* Subtitle */}
        <p className="font-[family-name:var(--font-cormorant)] italic text-[clamp(20px,2.4vw,28px)] leading-[1.45] text-[var(--ink-soft)] max-w-[680px] mx-auto mb-14">
          METHEAN is the first learning platform built so the family stays sovereign. A full year of
          curriculum, drafted for your philosophy. Curriculum, mastery, compliance, and AI tutoring,
          all under your authority. Always.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-7">
          <button
            type="button"
            onClick={() => router.push("/auth?mode=register")}
            className="cinematic-focus inline-flex items-center justify-center rounded-[4px] bg-[var(--gold)] px-9 py-[18px] font-[family-name:var(--font-jetbrains)] text-[14px] uppercase tracking-[0.12em] text-white shadow-[0_4px_16px_rgba(198,162,78,0.30)] transition-all duration-200 hover:-translate-y-[1px] hover:bg-[var(--gold-deep)] hover:shadow-[0_8px_28px_rgba(198,162,78,0.40)]"
          >
            Start Your Free Trial
          </button>
          <a
            href="#manifesto"
            className="cinematic-focus font-[family-name:var(--font-jetbrains)] text-[13px] uppercase tracking-[0.16em] text-[var(--ink-soft)] border-b border-[var(--gold-deep)]/40 pb-1 hover:text-[var(--gold-deep)] hover:border-[var(--gold-deep)] transition-colors"
          >
            Read the Manifesto
          </a>
        </div>

        {/* Trust line */}
        <p className="mt-14 font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.2em] text-[var(--ink-faint)]">
          No credit card · 30 day trial · Cancel anytime
        </p>

        {/* Pulsing vertical gold line */}
        <div className="mt-16 flex justify-center" aria-hidden="true">
          <span className="animate-pulse-line block w-[1px] bg-[var(--gold-deep)]" />
        </div>
      </div>
    </section>
  );
}
