"use client";

import { useRouter } from "next/navigation";
import { MetheanLogo } from "@/components/Brand";
import Button from "@/components/ui/Button";

export function LandingHeader() {
  const router = useRouter();
  return (
    <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-[rgba(250,250,248,0.85)] border-b border-[rgba(0,0,0,0.04)]">
      <div className="max-w-[1200px] mx-auto px-6 py-3 flex items-center justify-between">
        <MetheanLogo markSize={24} wordmarkHeight={12} color="#0F1B2D" gap={8} />
        <nav className="hidden sm:flex items-center gap-8" aria-label="Primary">
          <a
            href="#features"
            className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--gold) focus-visible:ring-offset-2 rounded-sm"
          >
            Features
          </a>
          <a
            href="#pricing"
            className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--gold) focus-visible:ring-offset-2 rounded-sm"
          >
            Pricing
          </a>
          <a
            href="#faq"
            className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--gold) focus-visible:ring-offset-2 rounded-sm"
          >
            FAQ
          </a>
        </nav>
        <div className="flex items-center gap-4">
          <a
            href="/auth"
            className="text-sm text-(--color-text-secondary) hover:text-(--color-text) transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-(--gold) focus-visible:ring-offset-2 rounded-sm"
          >
            Sign In
          </a>
          <Button variant="gold" size="md" onClick={() => router.push("/auth?mode=register")}>
            Start Your Free Trial
          </Button>
        </div>
      </div>
    </header>
  );
}
