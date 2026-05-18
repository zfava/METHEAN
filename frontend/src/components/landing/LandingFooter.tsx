import { MetheanLogo } from "@/components/Brand";

export function LandingFooter() {
  return (
    <footer className="border-t border-(--color-border) py-8 px-6 bg-(--color-page)">
      <div className="max-w-[1100px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <MetheanLogo markSize={18} wordmarkHeight={9} color="#9A9A9A" gap={6} />
        <div className="flex items-center gap-4 text-[12px] text-(--color-text-tertiary)">
          <a href="/privacy" className="hover:underline">
            Privacy
          </a>
          <a href="/terms" className="hover:underline">
            Terms
          </a>
          <span aria-hidden="true">·</span>
          <span>© 2026 METHEAN, Inc. · zack@methean.io</span>
        </div>
      </div>
    </footer>
  );
}
