import { MetheanMark } from "@/components/Brand";

const LINKS: Array<{ label: string; href: string }> = [
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
  { label: "Contact", href: "mailto:zack@methean.io" },
];

export function LandingFooter() {
  return (
    <footer
      className="px-6 pt-20 pb-12 text-center"
      style={{ background: "var(--navy-deep)" }}
    >
      <div className="max-w-[1100px] mx-auto flex flex-col items-center gap-7">
        <div style={{ opacity: 0.6 }}>
          <MetheanMark size={36} color="#C6A24E" />
        </div>
        <p className="font-[family-name:var(--font-cormorant)] italic text-white/70 text-[18px] leading-snug max-w-[520px]">
          METHEAN, the operating system for sovereign families.
        </p>
        <span
          aria-hidden="true"
          className="block h-[1px] w-[60px] bg-[var(--gold)] opacity-50"
        />
        <nav aria-label="Footer">
          <ul className="flex items-center gap-7">
            {LINKS.map((l) => (
              <li key={l.label}>
                <a
                  href={l.href}
                  className="cinematic-focus font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-white/50 hover:text-[var(--gold)] transition-colors"
                >
                  {l.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <p className="mt-4 font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.22em] text-white/30">
          © 2026 METHEAN, Inc. · Delaware · zack@methean.io
        </p>
      </div>
    </footer>
  );
}
