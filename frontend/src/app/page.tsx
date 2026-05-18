"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";
import { MetheanMark } from "@/components/Brand";
import { LandingComparison } from "@/components/landing/LandingComparison";
import { LandingFAQ } from "@/components/landing/LandingFAQ";
import { LandingFeatures } from "@/components/landing/LandingFeatures";
import { LandingFooter } from "@/components/landing/LandingFooter";
import { LandingFounder } from "@/components/landing/LandingFounder";
import { LandingHeader } from "@/components/landing/LandingHeader";
import { LandingHero } from "@/components/landing/LandingHero";
import { LandingHowItWorks } from "@/components/landing/LandingHowItWorks";
import { LandingPricing } from "@/components/landing/LandingPricing";
import { LandingPrinciples } from "@/components/landing/LandingPrinciples";
import { LandingProductPreview } from "@/components/landing/LandingProductPreview";

export default function LandingPage() {
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
      <div className="min-h-screen bg-(--color-page) flex items-center justify-center">
        <MetheanMark size={48} color="#0F1B2D" />
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ fontFamily: "var(--font-sans)" }}>
      <LandingHeader />
      <main>
        <LandingHero />
        <LandingPrinciples />
        <LandingFounder />
        <LandingHowItWorks />
        <LandingProductPreview />
        <LandingComparison />
        <LandingFeatures />
        <LandingFAQ />
        <LandingPricing />
      </main>
      <LandingFooter />
    </div>
  );
}
