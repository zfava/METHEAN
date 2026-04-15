import Link from "next/link";
import { MetheanLogo } from "@/components/Brand";

const sections = [
  { id: "collect", title: "What We Collect" },
  { id: "storage", title: "How We Store It" },
  { id: "access", title: "Who Can Access Your Data" },
  { id: "third-party", title: "Third-Party Services" },
  { id: "coppa", title: "Children's Privacy (COPPA)" },
  { id: "retention", title: "Data Retention" },
  { id: "export", title: "Data Export" },
  { id: "cookies", title: "Cookies" },
  { id: "rights", title: "Your Rights" },
  { id: "contact", title: "Contact" },
];

function Section({ id, title, children }: { id: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} className="mb-10">
      <h2 className="text-[20px] font-semibold text-(--color-text) border-b border-(--color-border) pb-2 mb-4">{title}</h2>
      <div className="text-[15px] leading-relaxed text-(--color-text-secondary) space-y-3">{children}</div>
    </section>
  );
}

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-(--color-page)">
      <header className="border-b border-(--color-border) bg-(--color-surface)">
        <div className="max-w-[720px] mx-auto flex items-center justify-between h-14 px-6">
          <Link href="/"><MetheanLogo markSize={22} wordmarkHeight={11} color="#0F1B2D" gap={8} /></Link>
          <Link href="/" className="text-sm text-(--color-text-secondary) hover:text-(--color-text)">Back to home</Link>
        </div>
      </header>

      <main className="max-w-[720px] mx-auto px-6 py-12">
        <h1 className="text-[28px] font-bold text-(--color-text) mb-1">Privacy Policy</h1>
        <p className="text-sm text-(--color-text-tertiary) mb-6">Effective April 2026</p>

        <div className="bg-(--color-brand-cream) rounded-[12px] p-5 mb-8 text-sm text-(--color-text-secondary) leading-relaxed">
          This privacy policy was written to be understood by real people. If anything is unclear, email <a href="mailto:zack@spartansolutions.co" className="text-(--color-accent) hover:underline">zack@spartansolutions.co</a>.
        </div>

        <nav className="mb-10">
          <h3 className="text-xs font-semibold text-(--color-text-tertiary) uppercase tracking-wider mb-3">Contents</h3>
          <ol className="space-y-1">
            {sections.map((s, i) => (
              <li key={s.id}><a href={`#${s.id}`} className="text-sm text-(--color-accent) hover:underline">{i + 1}. {s.title}</a></li>
            ))}
          </ol>
        </nav>

        <Section id="collect" title="1. What We Collect">
          <p><strong>Parent account:</strong> Name, email address, password (bcrypt hashed, never stored in plain text).</p>
          <p><strong>Child profiles:</strong> First name, grade level, learning preferences. We do NOT collect child email addresses, social media accounts, photos, or biometric data.</p>
          <p><strong>Learning data:</strong> Activities completed, mastery levels, attempt transcripts, tutor conversations, FSRS retention metrics.</p>
          <p><strong>AI interaction logs:</strong> Prompts, responses, and timestamps — stored per household for your inspection via the AI Inspection page.</p>
          <p><strong>Governance records:</strong> Rules, events, overrides, and constitutional ceremony records.</p>
          <p><strong>Compliance records:</strong> State requirements, instruction hours logged, documents generated.</p>
          <p><strong>Billing:</strong> Processed by Stripe. METHEAN stores only your Stripe customer ID and subscription status. We never see or store card numbers.</p>
        </Section>

        <Section id="storage" title="2. How We Store It">
          <p>All data is stored in PostgreSQL with <strong>Row-Level Security (RLS)</strong> enforcing tenant isolation. Each household's data is cryptographically isolated at the database level — even with application bugs, one household cannot see another's data.</p>
          <p>Passwords are hashed with bcrypt (12 rounds). Sessions use JWTs with configurable expiration (default: 15-minute access tokens, 30-day refresh tokens).</p>
          <p>Data in transit is encrypted via TLS. Backups are encrypted at rest.</p>
        </Section>

        <Section id="access" title="3. Who Can Access Your Data">
          <p>Only authenticated parent accounts within your household. Co-parents you explicitly invite. METHEAN support (Zack Fava) for troubleshooting, only when you request it.</p>
          <p><strong>We do not:</strong> Sell your data. Use it for advertising. Share it with schools, governments, or other institutions — unless you explicitly export and share it yourself.</p>
        </Section>

        <Section id="third-party" title="4. Third-Party Services">
          <p><strong>Anthropic (Claude AI) and OpenAI:</strong> Process educational prompts. AI providers receive activity context and child first names only; they do not receive your email, address, or billing information.</p>
          <p><strong>Stripe:</strong> Payment processing. <a href="https://stripe.com/privacy" className="text-(--color-accent) hover:underline">Stripe Privacy Policy</a></p>
          <p><strong>Resend:</strong> Transactional email delivery. <a href="https://resend.com/legal/privacy-policy" className="text-(--color-accent) hover:underline">Resend Privacy Policy</a></p>
        </Section>

        <Section id="coppa" title="5. Children's Privacy (COPPA)">
          <p>METHEAN is designed for use by parents and guardians. All child accounts are created and managed by parents. Children do not create their own accounts or provide personal information directly to METHEAN.</p>
          <p>The child learning interface does not collect email addresses, social media handles, or contact information.</p>
          <p>Parents can review all data collected about their children at any time through the Intelligence, Inspection, and Governance pages. Parents can delete child data by contacting <a href="mailto:zack@spartansolutions.co" className="text-(--color-accent) hover:underline">zack@spartansolutions.co</a>.</p>
        </Section>

        <Section id="retention" title="6. Data Retention">
          <p><strong>Active accounts:</strong> Data retained for the duration of your subscription.</p>
          <p><strong>Canceled accounts:</strong> Data retained for 90 days after cancellation, then permanently deleted.</p>
          <p>Parents can request immediate deletion by emailing <a href="mailto:zack@spartansolutions.co" className="text-(--color-accent) hover:underline">zack@spartansolutions.co</a>.</p>
          <p>AI interaction logs are retained for the duration of your subscription for parent inspection.</p>
        </Section>

        <Section id="export" title="7. Data Export">
          <p>Parents can export all household data at any time via Settings → Export Data. The export includes all children, learning maps, mastery records, governance events, and compliance documents in JSON format.</p>
        </Section>

        <Section id="cookies" title="8. Cookies">
          <p>METHEAN uses only essential cookies: authentication tokens (<code>access_token</code>, <code>refresh_token</code>, <code>csrf_token</code>).</p>
          <p>No analytics cookies. No advertising cookies. No third-party tracking cookies.</p>
        </Section>

        <Section id="rights" title="9. Your Rights">
          <p><strong>Access:</strong> View all data through the platform.</p>
          <p><strong>Export:</strong> Download all data at any time.</p>
          <p><strong>Deletion:</strong> Request deletion by email.</p>
          <p><strong>Correction:</strong> Edit child profiles and household settings at any time through the platform.</p>
        </Section>

        <Section id="contact" title="10. Contact">
          <p>Zack Fava · <a href="mailto:zack@spartansolutions.co" className="text-(--color-accent) hover:underline">zack@spartansolutions.co</a> · Spartan Solutions</p>
        </Section>
      </main>

      <footer className="border-t border-(--color-border) py-8 px-6">
        <div className="max-w-[720px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <MetheanLogo markSize={18} wordmarkHeight={9} color="#9A9A9A" gap={6} />
          <div className="flex items-center gap-4 text-[12px] text-(--color-text-tertiary)">
            <Link href="/terms" className="hover:underline">Terms of Service</Link>
            <span>·</span>
            <span>© 2026 Spartan Solutions</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
