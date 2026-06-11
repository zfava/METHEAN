"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  CalendarDays,
  Check,
  FileCheck2,
  Layers3,
  Lightbulb,
  Shield,
  ShieldPlus,
  TrendingUp,
  Users,
  Wrench,
} from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";
import "./landing.css";

// Faithful port of frontend/design-reference/METHEAN_Demo_1.html (routes['/']).
// Defaults render in their final visible state. The .js class is added
// after mount so the JS-gated initial-hidden states only activate when
// JS is alive; if JS never loads or the observer fails, every animated
// element is already in its final visible position. CTAs point at the
// real Next routes, not the reference's hash routes.
//
// Every stat on this page is derived from the repository, not estimated:
//   - 51 jurisdictions: len(STATE_REQUIREMENTS) in services/compliance_engine.py
//   - 260 endpoints: route decorators across backend/app
//   - 57/62 tenant-isolated tables: RLS_COVERED_TABLES over models' __tablename__ count
//   - 8 AI roles: the AIRole enum in app/ai/gateway.py
//   - 155,476 content lines: wc -l backend/app/content/*.py
//   - 36 weeks: the annual curriculum generator's school-year default
//   - 5 native philosophies: the six selectable philosophies minus
//     eclectic, which is a per-subject mix of the other five
// Re-derive when these change; do not round up.

const AUTH_HREF = "/auth?mode=register";
const SIGNIN_HREF = "/auth";

const ShieldLogo = ({ height = 32 }: { height?: number }) => (
  <svg viewBox="0 0 100 115" width={height * 0.875} height={height} fill="none" aria-hidden="true">
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M 50 2 C 58 2, 80 11, 93 17 C 94 17.5, 94 18.5, 94 20 L 94 56 C 94 72, 88 86, 76 96 C 68 103, 58 109, 50 113 C 42 109, 32 103, 24 96 C 12 86, 6 72, 6 56 L 6 20 C 6 18.5, 6 17.5, 7 17 C 20 11, 42 2, 50 2 Z M 21.5 84.5 L 21 28 L 50 51 L 79 28 L 78.5 84.5 L 65.5 84.5 L 65 46 L 50 58.5 L 35 46 L 34.5 84.5 Z"
      fill="#C6A24E"
    />
  </svg>
);

const ArrowIcon = ({ className }: { className?: string }) => (
  <Icon icon={ArrowRight} size={16} strokeWidth={2} className={className} />
);

const CheckIcon = () => <Icon icon={Check} size={12} strokeWidth={2} />;

const FAQ_ITEMS: ReadonlyArray<{ q: string; a: string }> = [
  {
    q: "Does METHEAN work in my state?",
    a: "Yes. All fifty states and Washington DC are supported with automatic hour tracking, mastery records, and document generation matched to each state's homeschool requirements.",
  },
  {
    q: "Can I keep using my current curriculum?",
    a: "Yes. If you already use Sonlight, Saxon, My Father's World, Abeka, BJU, or any other curriculum, METHEAN tracks mastery from any source you log and complements rather than replaces your current materials.",
  },
  {
    q: "How does the curriculum builder actually work?",
    a: "You pick a subject and a child. METHEAN drafts a full thirty-six week scope and sequence, with three to five activities Monday through Friday, every sixth week designated a review week. The plan is tailored to your educational philosophy and to your child's current mastery profile. Nothing reaches your child until you approve the week. You can adjust any activity, swap any week, or override the entire plan at any time.",
  },
  {
    q: "What ages does METHEAN support?",
    a: "Kindergarten through twelfth grade today. Pre-K and adult learner modes are on the near-term roadmap.",
  },
  {
    q: "Will METHEAN work for my neurodivergent child?",
    a: "METHEAN does not replace specialist evaluation, but the mastery-based progression removes the grade-level pressure that many families with dyslexic, ADHD, or gifted children find unhelpful. Your child moves at their own pace, in their own depth, on their own time.",
  },
  {
    q: "How much screen time does METHEAN require?",
    a: "As little as you want. Many families use METHEAN entirely as a parent-side planning and tracking tool, and their children never look at the screen. Other families enable the optional AI tutor for older kids. The choice is yours, every day, for every child.",
  },
  {
    q: "Is my family's data private?",
    a: "Yes. We never sell data. We never use child data for advertising. Your family's information stays in your household. Full export and deletion are available at any time.",
  },
  {
    q: "Do I need to be technical to use it?",
    a: "No. If you can send email and use a web browser, you can use METHEAN. Onboarding is guided. Support is available.",
  },
  {
    q: "How many children does one subscription cover?",
    a: "Unlimited. One household, one subscription, every child included.",
  },
  {
    q: "Can I cancel?",
    a: "Yes. Cancel anytime from your account settings. No questions, no fees, no retention pressure.",
  },
  {
    q: "What about high school transcripts?",
    a: "METHEAN generates high school transcripts on demand, tracks credit hours per subject, and exports records in standard formats accepted by colleges and universities.",
  },
];

interface CounterProps {
  target: number;
  unit?: string;
}

function Counter({ target, unit }: CounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const [value, setValue] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (typeof window === "undefined" || !("IntersectionObserver" in window)) {
      setValue(target);
      return;
    }
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const duration = 1600;
            const start = performance.now();
            const tick = (now: number) => {
              const elapsed = now - start;
              const progress = Math.min(elapsed / duration, 1);
              const eased = 1 - Math.pow(1 - progress, 3);
              setValue(Math.floor(eased * target));
              if (progress < 1) requestAnimationFrame(tick);
              else setValue(target);
            };
            requestAnimationFrame(tick);
            obs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.5 },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [target]);

  return (
    <span className="stat-n">
      <span ref={ref} className="counter">
        {value}
      </span>
      {unit ? <span className="unit">{unit}</span> : null}
    </span>
  );
}

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [jsActive, setJsActive] = useState(false);
  const heroVisualRef = useRef<HTMLDivElement>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const demoStopRef = useRef(false);

  useEffect(() => {
    document.title = "METHEAN, a learning operating system for families";
  }, []);

  // Activate the .js class on mount so SSR/no-JS users keep visible content.
  useEffect(() => {
    setJsActive(true);
  }, []);

  // Sticky header scroll state
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Reveal observers for .reveal and .reveal-stagger
  useEffect(() => {
    if (!rootRef.current) return;
    const root = rootRef.current;
    if (typeof window === "undefined" || !("IntersectionObserver" in window)) {
      root.querySelectorAll(".reveal, .reveal-stagger").forEach((el) => el.classList.add("in"));
      return;
    }
    const revealObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            revealObs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" },
    );
    root.querySelectorAll(".reveal, .reveal-stagger").forEach((el) => revealObs.observe(el));

    // Comparison row stagger
    const compObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const rows = e.target.querySelectorAll(".comp-row");
            rows.forEach((row, i) => {
              setTimeout(() => row.classList.add("in"), i * 80);
            });
            compObs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.15 },
    );
    root.querySelectorAll(".comp-card").forEach((el) => compObs.observe(el));

    return () => {
      revealObs.disconnect();
      compObs.disconnect();
    };
  }, []);

  // Mouse parallax on hero floating cards
  useEffect(() => {
    const heroVisual = heroVisualRef.current;
    if (!heroVisual) return;
    if (typeof window === "undefined") return;
    if (!window.matchMedia("(min-width: 1024px)").matches) return;
    const cards = heroVisual.querySelectorAll<HTMLElement>(".float-card");
    const onMove = (e: MouseEvent) => {
      if (!document.body.contains(heroVisual)) return;
      const rect = heroVisual.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) / window.innerWidth;
      const dy = (e.clientY - cy) / window.innerHeight;
      cards.forEach((card, i) => {
        const depth = (i + 1) * 6;
        card.style.setProperty("--mx", `${dx * depth}px`);
        card.style.setProperty("--my", `${dy * depth}px`);
      });
    };
    document.addEventListener("mousemove", onMove);
    return () => document.removeEventListener("mousemove", onMove);
  }, []);

  // Demo-step auto-cycling while the demo section is in view
  useEffect(() => {
    const demoSection = rootRef.current?.querySelector(".live-demo");
    if (!demoSection) return;
    if (typeof window === "undefined" || !("IntersectionObserver" in window)) return;
    let interval: number | null = null;
    const start = () => {
      if (interval) window.clearInterval(interval);
      interval = window.setInterval(() => {
        if (demoStopRef.current) return;
        setActiveStep((s) => (s + 1) % 3);
      }, 5500);
    };
    const stop = () => {
      if (interval) window.clearInterval(interval);
      interval = null;
    };
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) start();
          else stop();
        });
      },
      { threshold: 0.3 },
    );
    obs.observe(demoSection);
    return () => {
      stop();
      obs.disconnect();
    };
  }, []);

  const onStepClick = (i: number) => {
    demoStopRef.current = true;
    setActiveStep(i);
  };

  return (
    <div
      ref={rootRef}
      className={`cinematic-landing${jsActive ? " js" : ""}`}
    >
      {/* ───── HEADER ───── */}
      <header className={`site-header${scrolled ? " scrolled" : ""}`}>
        <div className="header-inner">
          <Link href="/" className="logo">
            <ShieldLogo />
            <span>METHEAN</span>
          </Link>
          <nav className="nav">
            <a href="#manifesto">Manifesto</a>
            <a href="#how">How It Works</a>
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
          </nav>
          <div className="actions">
            <a href={SIGNIN_HREF} className="signin">
              Sign In
            </a>
            <a href={AUTH_HREF} className="header-cta">
              Begin Trial
              <ArrowIcon />
            </a>
          </div>
        </div>
      </header>

      {/* ───── HERO ───── */}
      <section className="hero">
        <div className="hero-bg" aria-hidden />
        <div className="hero-grain" aria-hidden />
        <div className="hero-content wrap">
          <div className="hero-grid">
            <div className="hero-text">
              <div className="hero-status">
                <span className="live-dot" />
                <span>Now opening to founding families</span>
              </div>
              <h1 className="hero-headline">
                <span className="ln">Your children.</span>
                <span className="ln">Your rules.</span>
                <span className="ln">
                  <span className="gradient">Your</span> system.
                </span>
              </h1>
              <p className="hero-sub">
                The first learning operating system built on the conviction that the family, not the
                institution, is the rightful educational authority. A full year of curriculum,
                drafted for your philosophy. Every AI recommendation routed through you before it
                touches your child.
              </p>
              <div className="hero-ctas">
                <a href={AUTH_HREF} className="cin-btn cin-btn-gold">
                  Begin Your Trial
                  <ArrowIcon className="arrow" />
                </a>
                <a href="#how" className="cin-btn cin-btn-ghost">
                  See How It Works
                </a>
              </div>
              <div className="hero-trust">30-DAY TRIAL · NO CREDIT CARD · CANCEL ANY TIME</div>
            </div>

            <div className="hero-visual" ref={heroVisualRef}>
              <div className="float-card fc-approvals">
                <div className="fc-header">
                  <span className="fc-title">Pending Approvals</span>
                  <span className="count">
                    <span className="pulse" />3 new
                  </span>
                </div>
                {[
                  { initial: "A", name: "Avery, age 12", detail: "Geometry intro proposed" },
                  { initial: "J", name: "Jude, age 9", detail: "Writing prompt drafted" },
                  { initial: "M", name: "Mira, age 7", detail: "Phonics review" },
                ].map((row) => (
                  <div className="approval-item" key={row.name}>
                    <div className="appr-avatar">{row.initial}</div>
                    <div className="appr-meta">
                      <div className="appr-name">{row.name}</div>
                      <div className="appr-detail">{row.detail}</div>
                    </div>
                    <div className="appr-action">
                      <CheckIcon />
                    </div>
                  </div>
                ))}
              </div>

              <div className="float-card fc-mastery">
                <div className="fc-title">Family Mastery</div>
                <div className="mastery-stat">
                  <span className="mastery-num">74</span>
                  <span className="mastery-unit">/100</span>
                </div>
                <div className="mastery-bars">
                  <div className="mastery-bar">
                    <div className="fill" />
                  </div>
                  <div className="mastery-bar">
                    <div className="fill" />
                  </div>
                  <div className="mastery-bar">
                    <div className="fill" />
                  </div>
                </div>
              </div>

              <div className="float-card fc-audit">
                <div className="fc-title">Audit Trail</div>
                <div className="audit-row">
                  <span className="dot" style={{ background: "#C6A24E" }} />
                  <span className="time">2:14p</span>
                  <span className="what">Plan approved</span>
                </div>
                <div className="audit-row">
                  <span className="dot" style={{ background: "rgba(45, 106, 79, 0.7)" }} />
                  <span className="time">1:48p</span>
                  <span className="what">Rule applied</span>
                </div>
                <div className="audit-row">
                  <span className="dot" style={{ background: "rgba(74, 111, 165, 0.7)" }} />
                  <span className="time">1:22p</span>
                  <span className="what">AI proposed</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ───── HOW IT WORKS (live demo) ───── */}
      <section className="s live-demo" id="how">
        <div className="wrap">
          <div className="section-head reveal">
            <div className="section-eyebrow center light">How It Works</div>
            <h2 className="section-h light">
              Three steps to <span className="em">sovereign</span> education.
            </h2>
            <p className="section-sub light">
              The mechanics, plain. You set the rules. METHEAN proposes. You approve. The system
              records. Mastery builds.
            </p>
          </div>

          <div className="demo-stage">
            <div className="demo-narrative">
              {[
                {
                  num: "/ 01 · Set the rules",
                  h: "Encode your authority once.",
                  p: "Choose your educational philosophy. Define content boundaries. Set how much the AI may suggest. METHEAN converts your decisions into constitutional rules that govern every recommendation forever after.",
                },
                {
                  num: "/ 02 · AI proposes",
                  h: "Recommendations enter your queue.",
                  p: "The AI drafts weekly plans, lessons, and activities tailored to each child. Nothing reaches your children until you approve it. Adjust any item in one click. Reject anything in one click.",
                },
                {
                  num: "/ 03 · Mastery accumulates",
                  h: "The record builds itself.",
                  p: "Every completed activity feeds mastery tracking, retention scheduling, and the records your state requires. Years from now you will still have a complete audit trail of every decision made.",
                },
              ].map((step, i) => (
                <div
                  key={step.h}
                  className={`demo-step${activeStep === i ? " active" : ""}`}
                  onClick={() => onStepClick(i)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      onStepClick(i);
                    }
                  }}
                  role="button"
                  tabIndex={0}
                >
                  <div className="num">{step.num}</div>
                  <h3>{step.h}</h3>
                  <p>{step.p}</p>
                </div>
              ))}
            </div>

            <div className="demo-screen">
              <div className="demo-screen-chrome">
                <span className="cdot r" />
                <span className="cdot y" />
                <span className="cdot g" />
                <span className="cdot-url">methean.io/dashboard</span>
              </div>
              <div className="demo-screen-body">
                <div className={`demo-frame df-rules${activeStep === 0 ? " active" : ""}`}>
                  <div className="ttl">Governance Rules</div>
                  <div className="sub">Active · 12 rules in effect</div>
                  {[
                    { name: "Educational philosophy", detail: "CHARLOTTE_MASON" },
                    { name: "Daily approval required", detail: "ALL_AI_OUTPUTS" },
                    { name: "Screen time cap", detail: "2H_PER_CHILD_PER_DAY" },
                    { name: "Content boundaries", detail: "FAITH_BASED_FILTER" },
                  ].map((r) => (
                    <div className="rule-card" key={r.name}>
                      <div className="rule-icon">
                        <Icon icon={Shield} size={14} />
                      </div>
                      <div className="rule-content">
                        <div className="rule-name">{r.name}</div>
                        <div className="rule-detail">{r.detail}</div>
                      </div>
                      <div className="rule-toggle" />
                    </div>
                  ))}
                </div>

                <div className={`demo-frame df-recs${activeStep === 1 ? " active" : ""}`}>
                  <div className="ttl">Pending Approvals</div>
                  <div className="sub">3 recommendations awaiting your review</div>
                  {[
                    {
                      initial: "A",
                      name: "Avery, age 12",
                      activity: "Geometry intro: angles and parallel lines",
                    },
                    {
                      initial: "J",
                      name: "Jude, age 9",
                      activity: "Narration exercise on Wind in the Willows",
                    },
                    {
                      initial: "M",
                      name: "Mira, age 7",
                      activity: "Phonics review: digraphs and blends",
                    },
                  ].map((row) => (
                    <div className="rec-row" key={row.name}>
                      <div className="rec-avatar">{row.initial}</div>
                      <div className="rec-info">
                        <div className="rec-name">{row.name}</div>
                        <div className="rec-activity">{row.activity}</div>
                        <span className="rec-status">
                          <span className="pulse" />
                          Aligned with rules
                        </span>
                      </div>
                      <div className="rec-actions">
                        <button className="rec-btn approve" type="button">
                          Approve
                        </button>
                        <button className="rec-btn adjust" type="button">
                          Adjust
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                <div className={`demo-frame df-mastery${activeStep === 2 ? " active" : ""}`}>
                  <div className="ttl">Mastery, Avery</div>
                  <div className="sub">Q1 2026 · tracked across 4 subjects</div>
                  {[
                    { s: "Mathematics", p: "82%" },
                    { s: "Language Arts", p: "68%" },
                    { s: "History", p: "74%" },
                    { s: "Science", p: "91%" },
                  ].map((row) => (
                    <div className="mastery-row" key={row.s}>
                      <div className="m-head">
                        <span className="m-subject">{row.s}</span>
                        <span className="m-pct">{row.p}</span>
                      </div>
                      <div className="m-track">
                        <div className="m-fill" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ───── PRINCIPLES ───── */}
      <section className="s principles" id="manifesto">
        <div className="wrap-md">
          <div className="section-head reveal">
            <div className="section-eyebrow center">The Three Principles</div>
            <h2 className="section-h dark">
              Written before <span className="em dark">a single line</span> of code.
            </h2>
            <p className="section-sub dark">
              Three commitments encoded into the architecture itself. Not features, not settings.
              Load-bearing structure that cannot be overridden.
            </p>
          </div>
          <div className="principles-grid reveal-stagger">
            <div className="principle">
              <div className="principle-num">
                <em>I.</em>
              </div>
              <h3>Parents govern. AI serves.</h3>
              <p>
                Every AI recommendation routes through household authority before reaching the
                child. The system cannot write to learner state on its own. Your authority is the
                foundation, not a setting.
              </p>
            </div>
            <div className="principle">
              <div className="principle-num">
                <em>II.</em>
              </div>
              <h3>Every decision is auditable.</h3>
              <p>
                Every rule, every recommendation, every override is logged immutably. Years from
                now, you will still be able to answer the question, why did my child learn this and
                not that.
              </p>
            </div>
            <div className="principle">
              <div className="principle-num">
                <em>III.</em>
              </div>
              <h3>Your data stays in your household.</h3>
              <p>
                We never sell data. We never use child data for advertising. Your family&apos;s
                information is yours alone, exportable at any moment, deletable on demand.
                Infrastructure, not surveillance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ───── FOUNDER LETTER ───── */}
      <section className="s letter-section">
        <div className="letter-card reveal">
          <div className="letter-eyebrow">A Letter from the Founders</div>
          <h2 className="letter-h">
            Why we built <span className="em">METHEAN</span>.
          </h2>
          <p className="letter-greeting">To the family considering this work,</p>
          <div className="letter-body">
            <p>
              We have been homeschooling our six children for over six years. We have walked the
              road you are walking. We have stayed up late planning the week. We have grieved over
              the curriculum that worked for one child and failed another. We have rebuilt our
              entire approach more than once.
            </p>
            <p>
              What we kept noticing was this:{" "}
              <strong>every tool we tried treated us as users of a system.</strong> METHEAN is the
              first one that treats the parent as the system. The AI works inside our authority,
              not beside it. The curriculum honors our philosophy, not theirs. The records belong
              to us, not to a server in California we will never see.
            </p>
            <p>
              Every architectural decision in METHEAN started with one question we asked
              ourselves: <em>would we use this with our own children?</em> If the answer was no,
              the feature was rebuilt or removed. The platform exists because the tools we wanted
              did not.
            </p>
            <p>
              If you are still here at the end of this letter, you are probably the family we
              built this for. We hope you join us.
            </p>
          </div>
          <p className="letter-signoff">With sincere conviction,</p>
          <p className="letter-sig">Zack &amp; Angela Fava</p>
          <p className="letter-sig-meta">Founders · Homeschoolers of six</p>
        </div>
      </section>

      {/* ───── CURRICULUM BUILDER ───── */}
      <section className="s curriculum-section">
        <div className="wrap">
          <div className="section-head reveal">
            <div className="section-eyebrow center">The Curriculum Builder</div>
            <h2 className="section-h dark">
              Your year, drafted in minutes. <span className="em">Refined over years.</span>
            </h2>
            <p className="curriculum-sub">
              Thirty-six weeks of complete, philosophy-aware curriculum, generated for each
              subject and each child, then routed through your approval before it ever reaches
              their day.
            </p>
          </div>

          <div className="week-stage reveal">
            <div className="week-view">
              <div className="week-head">
                <div className="week-head-titles">
                  <div className="week-title-main">
                    Mathematics, Year 5 · Avery · Classical
                  </div>
                  <div className="week-title-meta">Week 12 of 36 · Long Division</div>
                </div>
                <div className="week-pending">3 pending your approval</div>
              </div>
              <div className="week-grid">
                {[
                  {
                    day: "Monday",
                    items: [
                      { tag: "Lesson", name: "Introduction to long division", min: "25 min", status: "approved" as const },
                      { tag: "Practice", name: "3-digit / 1-digit, manipulatives", min: "20 min", status: "approved" as const },
                    ],
                  },
                  {
                    day: "Tuesday",
                    items: [
                      { tag: "Practice", name: "Multi-step problems, written", min: "25 min", status: "approved" as const },
                      { tag: "Review", name: "Multiplication tables, sixes", min: "10 min", status: "pending" as const },
                    ],
                  },
                  {
                    day: "Wednesday",
                    items: [
                      { tag: "Lesson", name: "Long division with remainders", min: "30 min", status: "approved" as const },
                      { tag: "Practice", name: "Word problems, classical", min: "15 min", status: "approved" as const },
                    ],
                  },
                  {
                    day: "Thursday",
                    items: [
                      { tag: "Practice", name: "Mixed practice set", min: "25 min", status: "pending" as const },
                      { tag: "Project", name: "Build a division story", min: "20 min", status: "pending" as const },
                    ],
                  },
                  {
                    day: "Friday",
                    items: [
                      { tag: "Assessment", name: "Week 12 mastery check", min: "30 min", status: "approved" as const },
                      { tag: "Review", name: "Concept consolidation", min: "15 min", status: "approved" as const },
                    ],
                  },
                ].map((day) => (
                  <div className="week-day" key={day.day}>
                    <div className="day-label">{day.day}</div>
                    {day.items.map((it) => (
                      <div className={`activity-card ${it.status}`} key={`${day.day}-${it.name}`}>
                        <span className="activity-tag">{it.tag}</span>
                        <div className="activity-name">{it.name}</div>
                        <div className="activity-meta">
                          <span className="activity-min">{it.min}</span>
                          <span className={`activity-status ${it.status === "pending" ? "wait" : "ok"}`}>
                            {it.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
              <div className="week-foot">
                <div className="week-next">
                  Next: <strong>Week 13 · Review Week</strong>
                </div>
                <div className="week-cta-row">
                  <span className="week-mini-btn approve">Approve All Pending</span>
                  <span className="week-mini-btn adjust">Adjust Plan</span>
                </div>
              </div>
            </div>
          </div>

          <div className="curriculum-blocks reveal-stagger">
            <div className="curr-block">
              <div className="curr-num">I.</div>
              <h3>A full year, drafted at once.</h3>
              <p>
                Thirty-six weeks per subject. Daily activities Monday through Friday. Lesson,
                practice, review, and assessment cycles built in. Every sixth week, a review week.
                Generated to your family&apos;s philosophy and your child&apos;s current mastery,
                routed to you for approval.
              </p>
            </div>
            <div className="curr-block">
              <div className="curr-num">II.</div>
              <h3>Bring the books you already own.</h3>
              <p>
                Sonlight, Saxon, Story of the World, My Father&apos;s World, Abeka, BJU, any of it.
                METHEAN ingests the table of contents and maps it into the mastery graph. You keep
                the curriculum you love. You add the tracking, governance, and compliance you
                never had.
              </p>
            </div>
            <div className="curr-block">
              <div className="curr-num">III.</div>
              <h3>Your philosophy, in every lesson.</h3>
              <p>
                Pre-built scope and sequence for math, reading, writing, science, and history,
                with classical, Charlotte Mason, Montessori, traditional, and unschooling/trade
                alignment baked into every topic. Generate long division for a classical family,
                get classical long division. Not generic content with a label.
              </p>
            </div>
          </div>

          <div className="curriculum-stats reveal">
            <div className="cstat">
              <div className="cstat-n">155,476</div>
              <div className="cstat-l">
                Lines of pre-built
                <br />
                curriculum content
              </div>
            </div>
            <div className="cstat">
              <div className="cstat-n">36</div>
              <div className="cstat-l">
                Weeks of scope
                <br />
                per subject
              </div>
            </div>
            <div className="cstat">
              <div className="cstat-n">5</div>
              <div className="cstat-l">
                Philosophies
                <br />
                honored natively
              </div>
            </div>
            <div className="cstat">
              <div className="cstat-n">100%</div>
              <div className="cstat-l">
                Parent-approved
                <br />
                before child sees
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ───── STATS ───── */}
      <section className="s stats">
        <div className="wrap-md">
          <div className="section-head reveal">
            <div className="section-eyebrow center">The Substance Beneath</div>
            <h2 className="section-h dark">
              Built like <span className="em dark">infrastructure</span>. Because it is.
            </h2>
          </div>
          <div className="stats-grid reveal-stagger">
            <div className="stat">
              <Counter target={51} unit="/51" />
              <div className="stat-l">States &amp; DC supported</div>
            </div>
            <div className="stat">
              <Counter target={260} />
              <div className="stat-l">Governed endpoints</div>
            </div>
            <div className="stat">
              <Counter target={57} unit="/62" />
              <div className="stat-l">Tables isolated by tenant</div>
            </div>
            <div className="stat">
              <Counter target={8} />
              <div className="stat-l">AI roles, all governed</div>
            </div>
          </div>
        </div>
      </section>

      {/* ───── COMPARISON ───── */}
      <section className="s comparison-section">
        <div className="wrap-md">
          <div className="section-head reveal">
            <div className="section-eyebrow center light">A Different Category</div>
            <h2 className="section-h light">
              What sets METHEAN <span className="em">apart</span>.
            </h2>
          </div>
          <div className="comp-card">
            <div className="comp-head">
              <div className="q">The Question</div>
              <div className="other">Everyone Else</div>
              <div className="us">METHEAN</div>
            </div>
            {[
              {
                q: "Who decides what your child learns?",
                other: "The platform's algorithm",
                us: "The parent, every time",
              },
              {
                q: "Who builds the year of curriculum?",
                other: "You, after work and on weekends",
                us: "METHEAN drafts it, you approve",
              },
              {
                q: "What is being tracked?",
                other: "Completion of activities",
                us: "Actual mastery, with retention",
              },
              {
                q: "Whose values shape the content?",
                other: "The platform's defaults",
                us: "Your educational philosophy",
              },
              {
                q: "Who handles state compliance?",
                other: "You, with a spreadsheet",
                us: "All 51 jurisdictions, automatic",
              },
              {
                q: "Where does your data live?",
                other: "Their data warehouse",
                us: "Tenant-isolated, exportable",
              },
              {
                q: "Can you see why a decision was made?",
                other: "No, the model is a black box",
                us: "Yes, every decision logged",
              },
            ].map((row) => (
              <div className="comp-row" key={row.q}>
                <div className="q">{row.q}</div>
                <div className="other-cell">{row.other}</div>
                <div className="us-cell">{row.us}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ───── PHILOSOPHIES (5: matches real product) ───── */}
      <section className="s philos">
        <div className="wrap-md">
          <div className="section-head reveal">
            <div className="section-eyebrow center">For Whom We Built It</div>
            <h2 className="section-h dark">
              Whatever your <span className="em dark">approach</span>, METHEAN learns it.
            </h2>
            <p className="section-sub dark">
              One subscription. Many traditions. The system adapts to your conviction, not the
              other way around.
            </p>
          </div>
          <div className="philos-grid reveal-stagger">
            <div className="philo">
              <div className="philo-num">
                <em>i.</em>
              </div>
              <h3>The Classical Family</h3>
              <p>
                Trivium-anchored progression. Grammar, Logic, Rhetoric stages honored. Latin,
                Logic, and the Great Books folded into the weekly plan as first-class subjects.
              </p>
            </div>
            <div className="philo">
              <div className="philo-num">
                <em>ii.</em>
              </div>
              <h3>The Charlotte Mason Family</h3>
              <p>
                Living books, short lessons, narration, nature study. The system respects pace,
                depth, and atmosphere, refusing to industrialize what is meant to be lived.
              </p>
            </div>
            <div className="philo">
              <div className="philo-num">
                <em>iii.</em>
              </div>
              <h3>The Montessori Family</h3>
              <p>
                Self-directed work cycles. Materials-first sequencing. Three-year age windows. The
                platform tracks readiness, not grade.
              </p>
            </div>
            <div className="philo">
              <div className="philo-num">
                <em>iv.</em>
              </div>
              <h3>The Traditional Family</h3>
              <p>
                Structured, textbook-driven, grade-anchored. Daily scope honored. METHEAN keeps
                the rigor and removes the planning burden.
              </p>
            </div>
            <div className="philo">
              <div className="philo-num">
                <em>v.</em>
              </div>
              <h3>The Unschooling &amp; Trade-Bound Family</h3>
              <p>
                Child-led inquiry alongside apprenticeship work. Welding, electrical, automotive,
                agriculture. Certification milestones tracked alongside whatever the child is
                pursuing.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ───── FEATURES (bento) ───── */}
      <section className="s features" id="features">
        <div className="wrap">
          <div className="section-head reveal">
            <div className="section-eyebrow center light">What Is Inside</div>
            <h2 className="section-h light">
              Designed to be useful for <span className="em">a decade</span>, not a quarter.
            </h2>
          </div>
          <div className="feat-grid reveal-stagger">
            <div className="feat-cell large">
              <div className="feat-icon">
                <Icon icon={ShieldPlus} size={32} />
              </div>
              <h3>Parent Sovereignty</h3>
              <p>
                You set the boundaries the AI cannot cross. The system enforces them on every
                recommendation, every call, every output. Every decision is logged. Every
                override is recorded. Your authority is not a UI preference. It is encoded into
                the foundation of the platform, where it can never be removed without rewriting
                the system itself.
              </p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={Layers3} size={24} />
              </div>
              <h3>Your Philosophy</h3>
              <p>
                Classical, Charlotte Mason, Montessori, traditional, unschooling/trade. Every
                lesson respects your approach.
              </p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={CalendarDays} size={24} />
              </div>
              <h3>The Curriculum Builder</h3>
              <p>
                Thirty-six weeks of scope and sequence drafted for any subject, any child, any
                philosophy. Daily activities Mon to Fri. Review weeks built in. Your approval
                required before it ships.
              </p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={FileCheck2} size={24} />
              </div>
              <h3>All 51 Jurisdictions</h3>
              <p>
                Hour tracking, mastery records, and required documents, generated automatically.
              </p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={Users} size={24} />
              </div>
              <h3>Multi-Child Family</h3>
              <p>Unlimited children. Each tracked separately, all visible on one screen.</p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={TrendingUp} size={24} />
              </div>
              <h3>Mastery Over Memory</h3>
              <p>
                The system tracks what each child has learned and brings back what they&apos;re
                forgetting.
              </p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={Wrench} size={24} />
              </div>
              <h3>Trades &amp; Apprenticeships</h3>
              <p>
                Welding, electrical, automotive, agriculture. Certification milestones tracked.
              </p>
            </div>
            <div className="feat-cell">
              <div className="feat-icon">
                <Icon icon={Lightbulb} size={24} />
              </div>
              <h3>Optional Child Tutor</h3>
              <p>
                An AI tutor your child can talk to, only if you turn it on. Always inside your
                rules.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ───── FAQ ───── */}
      <section className="s faq-section">
        <div className="wrap-sm">
          <div className="section-head reveal">
            <div className="section-eyebrow center">Frequently Asked</div>
            <h2 className="section-h dark">
              Honest answers to <span className="em dark">honest questions</span>.
            </h2>
          </div>
          <div className="faq-list reveal">
            {FAQ_ITEMS.map((item) => (
              <details key={item.q}>
                <summary>
                  <span className="faq-q">{item.q}</span>
                  <span className="faq-icon" />
                </summary>
                <div className="faq-a">{item.a}</div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ───── PRICING ───── */}
      <section className="s pricing" id="pricing">
        <div className="wrap-sm">
          <div className="section-head reveal">
            <div className="section-eyebrow center light">A Single Plan</div>
            <h2 className="section-h light">
              One price. <span className="em">Everything included.</span>
            </h2>
            <p className="section-sub light">
              We refuse to nickel-and-dime homeschool families. One subscription covers every
              child in your household, every state, every feature.
            </p>
          </div>
          <div className="price-card reveal">
            <div className="price-label">Founding Family Plan</div>
            <div className="price-amount">
              <span className="currency">$</span>
              <span className="num">99</span>
              <span className="per">/mo</span>
            </div>
            <p className="price-trial">Thirty days free. Cancel any time.</p>
            <ul className="price-features">
              <li>Unlimited children</li>
              <li>All 51 jurisdictions</li>
              <li>AI curriculum builder</li>
              <li>Full governance suite</li>
              <li>Mastery tracking</li>
              <li>Document generation</li>
              <li>Trade pathways</li>
              <li>Multi-state reporting</li>
            </ul>
            <a href={AUTH_HREF} className="price-cta">
              Begin Your Trial
              <ArrowIcon />
            </a>
            <p className="price-foot">NO CREDIT CARD · CANCEL ANY TIME</p>
          </div>
        </div>
      </section>

      {/* ───── CLOSING ───── */}
      <section className="s closing">
        <div className="closing-content">
          <div className="closing-eyebrow reveal">For the family who has read this far</div>
          <h2 className="closing-h reveal">
            <span className="ln">Your children.</span>
            <span className="ln">Your rules.</span>
            <span className="ln">
              <span className="gradient">Your</span> system.
            </span>
          </h2>
          <div className="closing-ctas reveal">
            <a href={AUTH_HREF} className="cin-btn cin-btn-gold">
              Begin Your Trial
              <ArrowIcon className="arrow" />
            </a>
          </div>
          <p className="closing-trust">
            $99 / MONTH · UNLIMITED CHILDREN · 30-DAY TRIAL · CANCEL ANY TIME
          </p>
        </div>
      </section>

      {/* ───── FOOTER ───── */}
      <footer className="cin-footer">
        <div className="foot-inner">
          <div className="foot-top">
            <div className="foot-brand">
              <Link href="/" className="logo">
                <ShieldLogo />
                <span>METHEAN</span>
              </Link>
              <p>The first learning operating system for sovereign families.</p>
            </div>
            <div className="foot-col">
              <h4>Product</h4>
              <ul>
                <li>
                  <a href="#features">Features</a>
                </li>
                <li>
                  <a href="#pricing">Pricing</a>
                </li>
                <li>
                  <a href="#how">How It Works</a>
                </li>
              </ul>
            </div>
            <div className="foot-col">
              <h4>Company</h4>
              <ul>
                <li>
                  <Link href="/">About</Link>
                </li>
                <li>
                  <a href="#manifesto">Manifesto</a>
                </li>
                <li>
                  <a href="mailto:zack@methean.io">Contact</a>
                </li>
              </ul>
            </div>
            <div className="foot-col">
              <h4>Legal</h4>
              <ul>
                <li>
                  <a href="/privacy">Privacy</a>
                </li>
                <li>
                  <a href="/terms">Terms</a>
                </li>
                <li>
                  <a href="/privacy">COPPA</a>
                </li>
                <li>
                  <a href="/privacy">FERPA</a>
                </li>
              </ul>
            </div>
          </div>
          <div className="foot-bottom">
            <span>© 2026 METHEAN, INC. · DELAWARE</span>
            <span>BUILT BY HOMESCHOOL PARENTS, IN THE OPEN</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
