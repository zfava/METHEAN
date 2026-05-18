import Card from "@/components/ui/Card";
import { CheckIcon, CrossIcon } from "./icons";

const ROWS: Array<[string, string]> = [
  ["Track completion", "Track mastery with spaced repetition"],
  ["AI decides", "AI recommends, you decide"],
  ["Generic curriculum", "Philosophy-driven, tailored to your family"],
  ["No compliance help", "51-state compliance with document generation"],
  ["No audit trail", "Full governance trail, every decision logged"],
  ["Same experience forever", "Intelligence compounds over time"],
];

export function LandingComparison() {
  return (
    <section className="fade-up py-20 px-6 bg-(--color-page)">
      <div className="max-w-[900px] mx-auto">
        <p className="text-[13px] uppercase tracking-[0.1em] text-(--color-text-tertiary) text-center mb-3">
          Built Different
        </p>
        <h2 className="text-[22px] sm:text-[28px] font-medium text-(--color-text) text-center tracking-tight mb-10">
          What changes when the family is in charge.
        </h2>
        <Card padding="p-0" className="overflow-x-auto">
          <div className="grid grid-cols-2 gap-0 min-w-[480px]">
            <div className="px-6 py-4 border-b border-(--color-border) bg-(--color-page)">
              <p className="text-[15px] font-medium text-(--color-text-secondary)">Other platforms</p>
            </div>
            <div className="px-6 py-4 border-b border-(--color-border) bg-(--color-page)">
              <p className="text-[15px] font-medium" style={{ color: "#C6A24E" }}>
                METHEAN
              </p>
            </div>
            {ROWS.map(([left, right], i) => (
              <div key={left} className="contents">
                <div
                  className={`px-6 py-3.5 flex items-center gap-2.5 text-[14px] text-(--color-text-secondary) ${
                    i < ROWS.length - 1 ? "border-b border-(--color-border)" : ""
                  }`}
                >
                  <span className="text-(--color-text-tertiary) shrink-0">
                    <CrossIcon size={14} />
                  </span>
                  {left}
                </div>
                <div
                  className={`px-6 py-3.5 flex items-center gap-2.5 text-[14px] text-(--color-text) ${
                    i < ROWS.length - 1 ? "border-b border-(--color-border)" : ""
                  }`}
                >
                  <span style={{ color: "#C6A24E" }} className="shrink-0">
                    <CheckIcon size={14} />
                  </span>
                  {right}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </section>
  );
}
