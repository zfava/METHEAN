"use client";

import { useRouter } from "next/navigation";
import { MetheanMark } from "@/components/Brand";
import { RevealSection } from "./RevealSection";
import { FourPointStar } from "./icons";

const FEATURES = [
  "Unlimited children, one subscription",
  "All 50 states and DC compliance",
  "AI curriculum builder, parent-governed",
  "Full governance and audit trail",
  "Document and transcript generation",
  "Vocational and trade pathways",
  "Optional age-themed child tutor",
];

export function LandingPricing() {
  const router = useRouter();
  return (
    <RevealSection
      id="pricing"
      ariaLabelledBy="pricing-headline"
      className="parchment-noise bg-[var(--parchment)] py-[120px] sm:py-[160px] px-6 scroll-mt-24"
    >
      <div className="max-w-[640px] mx-auto">
        <div className="text-center mb-14">
          <p className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-deep)] mb-6">
            Membership
          </p>
          <h2
            id="pricing-headline"
            className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.05] text-[clamp(36px,5.4vw,64px)] mb-5"
          >
            One plan. <span className="gold-em">Everything included.</span>
          </h2>
          <p className="font-[family-name:var(--font-cormorant)] italic text-[20px] leading-[1.55] text-[var(--ink-soft)]">
            No tiers, no upsells, no surprises. Every family gets every feature.
          </p>
        </div>

        <div className="relative max-w-[520px] mx-auto bg-[var(--cream-warm)] border border-[var(--gold)] px-7 py-12 sm:px-14 sm:py-16">
          {/* Corner brackets */}
          <span
            aria-hidden="true"
            className="absolute top-3 left-3 w-4 h-4 border-l-[1.5px] border-t-[1.5px] border-[var(--gold)]"
          />
          <span
            aria-hidden="true"
            className="absolute bottom-3 right-3 w-4 h-4 border-r-[1.5px] border-b-[1.5px] border-[var(--gold)]"
          />

          <div className="flex justify-center mb-6">
            <MetheanMark size={56} color="#C6A24E" />
          </div>

          <p className="text-center font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.28em] text-[var(--gold-deep)] mb-8">
            METHEAN Family
          </p>

          <div className="text-center">
            <p className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] leading-none">
              <span className="align-top text-[44px] sm:text-[56px] mr-1">$</span>
              <span className="text-[80px] sm:text-[96px]">99</span>
            </p>
            <p className="mt-3 font-[family-name:var(--font-cormorant)] italic text-[22px] text-[var(--ink-mute)]">
              per month, per family
            </p>
          </div>

          <span
            aria-hidden="true"
            className="block h-[1px] w-12 bg-[var(--gold)] mx-auto my-10"
          />

          <ul className="max-w-[360px] mx-auto">
            {FEATURES.map((f, i) => (
              <li
                key={f}
                className={`flex items-start gap-3 py-3.5 ${
                  i < FEATURES.length - 1 ? "border-b border-[rgba(166,132,58,0.12)]" : ""
                }`}
              >
                <span className="text-[var(--gold-deep)] mt-1.5 shrink-0">
                  <FourPointStar size={12} />
                </span>
                <span className="font-[family-name:var(--font-cormorant)] text-[17px] text-[var(--navy)] leading-snug">
                  {f}
                </span>
              </li>
            ))}
          </ul>

          <button
            type="button"
            onClick={() => router.push("/auth?mode=register")}
            className="cinematic-focus mt-10 w-full inline-flex items-center justify-center rounded-[4px] bg-[var(--gold)] px-9 py-4 font-[family-name:var(--font-jetbrains)] text-[14px] uppercase tracking-[0.14em] text-white shadow-[0_4px_16px_rgba(198,162,78,0.30)] transition-all duration-200 hover:-translate-y-[1px] hover:bg-[var(--gold-deep)] hover:shadow-[0_8px_28px_rgba(198,162,78,0.40)]"
          >
            Start Your Free Trial
          </button>

          <p className="mt-5 text-center font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.22em] text-[var(--ink-mute)]">
            30 day trial · No credit card · Cancel anytime
          </p>
        </div>
      </div>
    </RevealSection>
  );
}
