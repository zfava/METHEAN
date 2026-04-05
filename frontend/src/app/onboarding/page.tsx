"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { curriculum, governance, type Template } from "@/lib/api";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

const PHILOSOPHIES = [
  { value: "classical", label: "Classical", desc: "Trivium: grammar, logic, rhetoric" },
  { value: "charlotte_mason", label: "Charlotte Mason", desc: "Living books, nature study" },
  { value: "unschooling", label: "Unschooling", desc: "Child-led, experiential" },
  { value: "eclectic", label: "Eclectic", desc: "Mixed approaches" },
  { value: "montessori", label: "Montessori", desc: "Self-directed, hands-on" },
  { value: "traditional", label: "Traditional", desc: "Structured, textbook-based" },
];

const AUTONOMY = [
  { value: "preview_all", label: "Preview All", desc: "Review every recommendation" },
  { value: "approve_difficult", label: "Approve Difficult", desc: "Auto-approve easy, review hard" },
  { value: "trust_within_rules", label: "Trust Within Rules", desc: "AI follows your rules freely" },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Philosophy state
  const [philosophy, setPhilosophy] = useState("eclectic");
  const [religion, setReligion] = useState("secular");
  const [autonomy, setAutonomy] = useState("approve_difficult");

  async function loadTemplates() {
    const t = await curriculum.templates();
    setTemplates(t);
    setStep(2);
  }

  async function applyTemplate() {
    if (!selectedTemplate) return;
    setLoading(true);
    try {
      await curriculum.copyTemplate(selectedTemplate);
      await governance.initDefaults();
      setStep(3);
    } catch (err: any) {
      alert(err.detail || "Failed");
    } finally {
      setLoading(false);
    }
  }

  async function savePhilosophy() {
    const csrf = getCsrf();
    await fetch(`${API}/household/philosophy`, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body: JSON.stringify({
        educational_philosophy: philosophy,
        religious_framework: religion,
        ai_autonomy_level: autonomy,
      }),
    });
    setStep(4);
  }

  function skipPhilosophy() {
    // Set reasonable defaults silently
    const csrf = getCsrf();
    fetch(`${API}/household/philosophy`, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body: JSON.stringify({
        educational_philosophy: "eclectic",
        religious_framework: "secular",
        ai_autonomy_level: "approve_difficult",
      }),
    }).catch(() => {});
    setStep(4);
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-semibold tracking-tight text-slate-800">Welcome to METHEAN</h1>
          <p className="text-sm text-slate-500 mt-1">Let&apos;s set up your learning environment.</p>
        </div>

        {/* Progress */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[1, 2, 3, 4].map((s) => (
            <div key={s} className={`w-8 h-1 rounded-full ${step >= s ? "bg-blue-600" : "bg-slate-200"}`} />
          ))}
        </div>

        <div className="bg-white rounded-lg border border-slate-200 p-6">

          {/* Step 1: Choose template */}
          {step === 1 && (
            <div className="text-center">
              <h2 className="text-sm font-semibold text-slate-800 mb-2">Choose a Curriculum Template</h2>
              <p className="text-xs text-slate-500 mb-4">Start with a proven structure. Customize everything later.</p>
              <button onClick={loadTemplates}
                className="px-4 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
                Browse Templates
              </button>
            </div>
          )}

          {/* Step 2: Select template */}
          {step === 2 && (
            <div>
              <h2 className="text-sm font-semibold text-slate-800 mb-4">Select a Template</h2>
              <div className="space-y-3 mb-4">
                {templates.map((t) => (
                  <button key={t.template_id} onClick={() => setSelectedTemplate(t.template_id)}
                    className={`w-full text-left p-4 rounded-md border transition-colors ${
                      selectedTemplate === t.template_id ? "border-blue-500 bg-blue-50" : "border-slate-200 hover:border-slate-300"
                    }`}
                  >
                    <div className="text-sm font-medium text-slate-800">{t.name}</div>
                    <p className="text-xs text-slate-500 mt-1">{t.description}</p>
                  </button>
                ))}
              </div>
              <button onClick={applyTemplate} disabled={!selectedTemplate || loading}
                className="w-full py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
                {loading ? "Setting up..." : "Apply Template"}
              </button>
            </div>
          )}

          {/* Step 3: Philosophy */}
          {step === 3 && (
            <div>
              <h2 className="text-sm font-semibold text-slate-800 mb-1">Your Educational Philosophy</h2>
              <p className="text-xs text-slate-500 mb-4">
                These guide every AI recommendation. You can refine this anytime.
              </p>

              <div className="mb-4">
                <label className="block text-xs font-medium text-slate-600 mb-2">Approach</label>
                <div className="grid grid-cols-3 gap-2">
                  {PHILOSOPHIES.map((p) => (
                    <button key={p.value} onClick={() => setPhilosophy(p.value)}
                      className={`text-left p-2.5 rounded border-2 transition-colors ${
                        philosophy === p.value ? "border-blue-500 bg-blue-50" : "border-slate-200"
                      }`}
                    >
                      <div className="text-xs font-medium text-slate-800">{p.label}</div>
                      <div className="text-[10px] text-slate-500">{p.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <label className="block text-xs font-medium text-slate-600 mb-2">Worldview</label>
                <div className="flex flex-wrap gap-2">
                  {["christian", "catholic", "jewish", "islamic", "secular", "other"].map((r) => (
                    <button key={r} onClick={() => setReligion(r)}
                      className={`px-3 py-1.5 text-xs rounded border-2 capitalize transition-colors ${
                        religion === r ? "border-blue-500 bg-blue-50 font-medium" : "border-slate-200"
                      }`}
                    >{r}</button>
                  ))}
                </div>
              </div>

              <div className="mb-5">
                <label className="block text-xs font-medium text-slate-600 mb-2">AI Autonomy</label>
                <div className="space-y-2">
                  {AUTONOMY.map((a) => (
                    <button key={a.value} onClick={() => setAutonomy(a.value)}
                      className={`w-full text-left p-3 rounded border-2 transition-colors ${
                        autonomy === a.value ? "border-blue-500 bg-blue-50" : "border-slate-200"
                      }`}
                    >
                      <div className="text-xs font-medium text-slate-800">{a.label}</div>
                      <div className="text-[10px] text-slate-500">{a.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex gap-2">
                <button onClick={savePhilosophy}
                  className="flex-1 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
                  Save &amp; Continue
                </button>
                <button onClick={skipPhilosophy}
                  className="px-4 py-2 text-xs text-slate-500 hover:text-slate-700">
                  Skip for now
                </button>
              </div>
            </div>
          )}

          {/* Step 4: Done */}
          {step === 4 && (
            <div className="text-center">
              <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-green-100 flex items-center justify-center">
                <span className="text-green-600 text-xl">&#10003;</span>
              </div>
              <h2 className="text-sm font-semibold text-slate-800 mb-2">You&apos;re All Set</h2>
              <p className="text-xs text-slate-500 mb-4">
                Your curriculum, governance rules, and educational philosophy are configured.
              </p>
              <button onClick={() => router.push("/dashboard")}
                className="px-6 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
                Go to Dashboard
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
