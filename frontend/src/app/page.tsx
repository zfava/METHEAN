"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";
import { MetheanMark } from "@/components/Brand";
import { LandingClosing } from "@/components/landing/LandingClosing";
import { LandingComparison } from "@/components/landing/LandingComparison";
import { LandingCurriculumBuilder } from "@/components/landing/LandingCurriculumBuilder";
import { LandingFAQ } from "@/components/landing/LandingFAQ";
import { LandingFeatures } from "@/components/landing/LandingFeatures";
import { LandingFooter } from "@/components/landing/LandingFooter";
import { LandingFounderLetter } from "@/components/landing/LandingFounderLetter";
import { LandingHeader } from "@/components/landing/LandingHeader";
import { LandingHero } from "@/components/landing/LandingHero";
import { LandingHowItWorks } from "@/components/landing/LandingHowItWorks";
import { LandingPhilosophies } from "@/components/landing/LandingPhilosophies";
import { LandingPricing } from "@/components/landing/LandingPricing";
import { LandingPrinciples } from "@/components/landing/LandingPrinciples";
import { LandingStats } from "@/components/landing/LandingStats";

export default function HomePage() {
  const router = useRouter();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    document.title = "METHEAN, a learning operating system for families";
    auth.me()
      .then(() => router.replace("/dashboard"))
      .catch(() => setChecking(false));
  }, [router]);

  if (checking) {
    return (
      <div
        className="min-h-screen flex items-center justify-center"
        style={{ background: "var(--parchment)" }}
      >
        <MetheanMark size={48} color="#C6A24E" />
      </div>
    );
  }

  return (
    <main
      className="bg-[var(--parchment)] text-[var(--color-text)]"
      style={{ fontFamily: "var(--font-sans)" }}
    >
      <LandingHeader />
      <LandingHero />
      <LandingHowItWorks />
      <LandingPrinciples />
      <LandingFounderLetter />
      <LandingCurriculumBuilder />
      <LandingStats />
      <LandingComparison />
      <LandingPhilosophies />
      <LandingFeatures />
      <LandingFAQ />
      <LandingPricing />
      <LandingClosing />
      <LandingFooter />
    </main>
  );
}
