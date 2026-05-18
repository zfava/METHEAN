"use client";

import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";

export function LandingHero() {
  const router = useRouter();
  return (
    <section className="fade-up min-h-[92vh] flex items-center justify-center px-6 pt-32 pb-20 bg-(--color-page)">
      <div className="max-w-[820px] text-center">
        <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) mb-8">
          A learning operating system for families who homeschool
        </p>
        <h1 className="text-[40px] sm:text-[64px] lg:text-[80px] font-semibold leading-[1.05] tracking-[-0.04em] text-(--color-text) mb-8">
          <span className="block">You set the rules.</span>
          <span className="block">AI follows them.</span>
          <span className="block">Every decision is yours.</span>
        </h1>
        <p className="text-[17px] sm:text-[18px] text-(--color-text-secondary) leading-relaxed max-w-[560px] mx-auto mb-10">
          METHEAN gives homeschool families a single system for curriculum, mastery tracking, state
          compliance, and AI tutoring. Built so the family stays in charge.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6">
          <Button variant="gold" size="lg" onClick={() => router.push("/auth?mode=register")}>
            Start Your Free Trial
          </Button>
          <a
            href="#how-it-works"
            className="text-[15px] text-(--color-text-secondary) underline underline-offset-4 hover:text-(--color-text) transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--gold) focus-visible:ring-offset-2 rounded-sm"
          >
            See how it works
          </a>
        </div>
        <p className="mt-6 text-[13px] text-(--color-text-tertiary)">
          30-day free trial. No credit card required. Cancel anytime.
        </p>
      </div>
    </section>
  );
}
