"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { curriculum, governance, type Template } from "@/lib/api";

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

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

  function finish() {
    router.push("/dashboard");
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-(--color-bg)">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-semibold tracking-tight">Welcome to METHEAN</h1>
          <p className="text-sm text-(--color-text-secondary) mt-1">
            Let&apos;s set up your learning environment.
          </p>
        </div>

        {/* Progress */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`w-8 h-1 rounded-full ${
                step >= s ? "bg-(--color-accent)" : "bg-gray-200"
              }`}
            />
          ))}
        </div>

        <div className="bg-white rounded-lg border border-(--color-border) p-6">
          {step === 1 && (
            <div className="text-center">
              <h2 className="text-sm font-semibold mb-2">Choose a Curriculum Template</h2>
              <p className="text-xs text-(--color-text-secondary) mb-4">
                Start with a proven structure. You can customize everything later.
              </p>
              <button
                onClick={loadTemplates}
                className="px-4 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)"
              >
                Browse Templates
              </button>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-sm font-semibold mb-4">Select a Template</h2>
              <div className="space-y-3 mb-4">
                {templates.map((t) => (
                  <button
                    key={t.template_id}
                    onClick={() => setSelectedTemplate(t.template_id)}
                    className={`w-full text-left p-4 rounded-md border transition-colors ${
                      selectedTemplate === t.template_id
                        ? "border-(--color-accent) bg-blue-50"
                        : "border-(--color-border) hover:border-gray-300"
                    }`}
                  >
                    <div className="text-sm font-medium">{t.name}</div>
                    <p className="text-xs text-(--color-text-secondary) mt-1">{t.description}</p>
                    <p className="text-xs text-(--color-text-secondary) mt-1">{t.node_count} learning nodes</p>
                  </button>
                ))}
              </div>
              <button
                onClick={applyTemplate}
                disabled={!selectedTemplate || loading}
                className="w-full py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover) disabled:opacity-50"
              >
                {loading ? "Setting up..." : "Apply Template"}
              </button>
            </div>
          )}

          {step === 3 && (
            <div className="text-center">
              <div className="text-3xl mb-3">&#10003;</div>
              <h2 className="text-sm font-semibold mb-2">You&apos;re All Set</h2>
              <p className="text-xs text-(--color-text-secondary) mb-4">
                Your curriculum map is ready and default governance rules are active.
                Head to the dashboard to generate your first weekly plan.
              </p>
              <button
                onClick={finish}
                className="px-6 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)"
              >
                Go to Dashboard
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
