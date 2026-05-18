import { RevealSection } from "./RevealSection";

export function LandingFounderLetter() {
  return (
    <RevealSection
      ariaLabelledBy="letter-headline"
      className="parchment-noise bg-[var(--parchment-warm)] py-[120px] sm:py-[160px] px-6"
    >
      <div className="max-w-[760px] mx-auto">
        {/* Framed letter card with corner brackets */}
        <div
          className="relative bg-[var(--cream-warm)] border border-[var(--gold)]/20 shadow-[0_24px_56px_rgba(15,27,45,0.08)] px-7 py-12 sm:px-[72px] sm:py-[80px]"
        >
          {/* Corner brackets */}
          <span
            aria-hidden="true"
            className="absolute top-4 left-4 w-6 h-6 border-l-[1.5px] border-t-[1.5px] border-[var(--gold)]"
          />
          <span
            aria-hidden="true"
            className="absolute bottom-4 right-4 w-6 h-6 border-r-[1.5px] border-b-[1.5px] border-[var(--gold)]"
          />

          <div className="text-center mb-10">
            <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.32em] text-[var(--gold-deep)] mb-6">
              A Letter From the Founders
            </p>
            <h2
              id="letter-headline"
              className="font-[family-name:var(--font-cormorant)] font-medium text-[var(--navy)] tracking-[-0.02em] leading-[1.1] text-[clamp(32px,4.6vw,56px)]"
            >
              Built by parents who <span className="gold-em">actually homeschool.</span>
            </h2>
          </div>

          <div className="space-y-6 font-[family-name:var(--font-cormorant)] text-[19px] leading-[1.7] text-[var(--ink-soft)]">
            <p className="text-center italic text-[var(--gold-deep)] text-[20px]">
              To the family considering this work,
            </p>
            <p>
              We have been homeschooling our six children for over six years. Mathematics on the
              kitchen counter, Charlotte Mason at the dining table, hands-on science in the back
              yard, transcripts in a binder beside the stove. The tools we wanted did not exist.
              METHEAN is the platform we built so that they would.
            </p>
            <p>
              Every architectural decision started with a question we asked ourselves first:
              would we use this with our own kids? If the answer was no, the feature was rebuilt
              or removed. There is no telemetry pixel on a child's screen because we would not
              put one on our own child's screen. There is no opaque algorithm because we would
              not delegate our family's curriculum to a black box.
            </p>
            <p>
              The platform exists because the work of teaching our own children, deliberately and
              well, surfaced thousands of small decisions a year that nothing on the market made
              easier. METHEAN is the operating system that absorbs that overhead so the parent can
              spend their attention where it actually matters.
            </p>
            <p className="text-center italic text-[var(--navy)] text-[20px] pt-2">
              This is the system we built for our own family. We are launching it for yours.
            </p>
          </div>

          <div className="mt-12 text-center">
            <p className="font-[family-name:var(--font-cormorant)] italic text-[24px] text-[var(--navy)] leading-tight">
              Zack &amp; Angela Fava
            </p>
            <p className="mt-2 font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-[0.28em] text-[var(--ink-mute)]">
              Founders · Homeschoolers of Six
            </p>
          </div>
        </div>
      </div>
    </RevealSection>
  );
}
