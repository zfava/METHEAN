"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { MetheanLogo } from "@/components/Brand";

const NAV: Array<{ label: string; href: string }> = [
  { label: "Manifesto", href: "#manifesto" },
  { label: "Features", href: "#features" },
  { label: "Pricing", href: "#pricing" },
  { label: "Questions", href: "#faq" },
];

export function LandingHeader() {
  const router = useRouter();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-xl transition-all duration-200 ${
        scrolled
          ? "bg-[rgba(245,241,232,0.95)] shadow-[0_1px_0_rgba(166,132,58,0.10),0_4px_24px_rgba(15,27,45,0.06)]"
          : "bg-[rgba(245,241,232,0.85)]"
      }`}
    >
      <div className="max-w-[1280px] mx-auto px-6 lg:px-8 py-[18px] flex items-center justify-between">
        <Link
          href="/"
          aria-label="METHEAN home"
          className="cinematic-focus inline-flex items-center"
        >
          <MetheanLogo markSize={32} wordmarkHeight={18} color="#0F1B2D" gap={10} />
        </Link>

        <nav className="hidden min-[900px]:flex items-center gap-10" aria-label="Primary">
          {NAV.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="cinematic-focus group relative font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.14em] text-[var(--ink-soft)] hover:text-[var(--gold-deep)] transition-colors"
            >
              {item.label}
              <span
                aria-hidden="true"
                className="absolute -bottom-1 left-0 h-[1px] w-full origin-left scale-x-0 bg-[var(--gold-deep)] transition-transform duration-[250ms] group-hover:scale-x-100"
              />
            </a>
          ))}
        </nav>

        <button
          type="button"
          onClick={() => router.push("/auth?mode=register")}
          className="cinematic-focus inline-flex items-center justify-center rounded-[4px] border border-[var(--gold)] bg-[var(--navy)] px-[22px] py-3 font-[family-name:var(--font-jetbrains)] text-[12px] uppercase tracking-[0.14em] text-[var(--gold)] transition-all duration-200 hover:-translate-y-[1px] hover:bg-[var(--gold)] hover:text-[var(--navy)] hover:shadow-[0_8px_24px_rgba(198,162,78,0.30)]"
        >
          Begin
        </button>
      </div>
    </header>
  );
}
