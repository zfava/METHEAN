"use client";

import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { CheckIcon } from "./icons";

const FEATURES = [
  "Unlimited children",
  "All 50 states + DC compliance",
  "AI curriculum builder",
  "Full governance suite",
  "Document generation",
  "Vocational pathways",
  "Multi-state compliance reporting",
];

export function LandingPricing() {
  const router = useRouter();
  return (
    <section id="pricing" className="fade-up px-6 py-24 bg-(--color-surface) scroll-mt-24">
      <div className="max-w-[440px] mx-auto text-center">
        <h2 className="text-[24px] sm:text-[28px] font-semibold tracking-tight text-(--color-text) mb-2">
          Simple pricing.
        </h2>
        <p className="text-[15px] text-(--color-text-secondary) mb-8">One plan. Everything included.</p>
        <Card padding="p-10" className="text-center">
          <div className="text-[40px] font-bold tracking-tight text-(--color-text)">
            $99
            <span className="text-[18px] font-normal text-(--color-text-secondary)">/month</span>
          </div>
          <div className="text-[14px] text-(--color-text-tertiary) mt-1 mb-6">30-day free trial</div>
          <ul className="space-y-2 text-left max-w-[300px] mx-auto mb-8">
            {FEATURES.map((f) => (
              <li key={f} className="text-[14px] text-(--color-text) flex items-center gap-2.5">
                <span className="text-(--color-success) shrink-0">
                  <CheckIcon size={14} />
                </span>
                {f}
              </li>
            ))}
          </ul>
          <Button
            variant="gold"
            size="lg"
            className="w-full"
            onClick={() => router.push("/auth?mode=register")}
          >
            Start Your Free Trial
          </Button>
          <p className="mt-4 text-[13px] text-(--color-text-tertiary)">
            30-day free trial. No credit card required.
          </p>
        </Card>
      </div>
    </section>
  );
}
