export function LandingFounder() {
  return (
    <section className="fade-up py-20 px-6 bg-(--color-page)">
      <div className="max-w-[720px] mx-auto text-center">
        <h2 className="text-[28px] sm:text-[32px] font-semibold tracking-tight text-(--color-text) mb-8">
          Built by parents who actually homeschool.
        </h2>
        <div className="max-w-[640px] mx-auto space-y-5 text-[16px] text-(--color-text-secondary) leading-relaxed">
          <p>
            Zack and Angela Fava have been homeschooling their six children for over six years.
            METHEAN was built in their kitchen, refined at their dining table, and tested against
            the real days of teaching multiple kids across multiple subjects across multiple ages.
          </p>
          <p>
            Every architectural decision in METHEAN started with a question Zack and Angela asked
            themselves first: would we use this with our own kids? If the answer was no, the
            feature was rebuilt or removed. The platform exists because the tools we wanted did
            not.
          </p>
          <p className="italic text-[15px] text-(--color-text-tertiary)">
            This is the operating system we built for our own family. We are launching it for
            yours.
          </p>
        </div>
      </div>
    </section>
  );
}
