"use client";

import { useRouter } from "next/navigation";
import { RevealSection } from "./RevealSection";

export function LandingClosing() {
  const router = useRouter();
  return (
    <RevealSection
      ariaLabelledBy="closing-headline"
      className="dark-noise relative py-[160px] sm:py-[200px] px-6 text-center"
    >
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-0"
        style={{ background: "var(--navy)" }}
      />
      <div className="relative max-w-[1100px] mx-auto">
        <h2
          id="closing-headline"
          className="font-[family-name:var(--font-cormorant)] font-medium text-white leading-[1.02] tracking-[-0.02em] text-[clamp(40px,7vw,96px)]"
        >
          <span className="block">
            <span className="gold-em">Your</span> children.
          </span>
          <span className="block">
            <span className="gold-em">Your</span> rules.
          </span>
          <span className="block">
            <span className="gold-em">Your</span> operating system.
          </span>
        </h2>
        <div className="mt-16">
          <button
            type="button"
            onClick={() => router.push("/auth?mode=register")}
            className="cinematic-focus inline-flex items-center justify-center rounded-[4px] bg-[var(--gold)] px-10 py-[18px] font-[family-name:var(--font-jetbrains)] text-[14px] uppercase tracking-[0.14em] text-white shadow-[0_4px_16px_rgba(198,162,78,0.30)] transition-all duration-200 hover:-translate-y-[1px] hover:bg-[var(--gold-deep)] hover:shadow-[0_8px_28px_rgba(198,162,78,0.40)]"
          >
            Start Your Free Trial
          </button>
        </div>
      </div>
    </RevealSection>
  );
}
