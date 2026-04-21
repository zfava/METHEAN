"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { auth, account } from "@/lib/api";
import { MetheanLogoVertical } from "@/components/Brand";

export default function AuthPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "register" | "forgot">("login");
  const [forgotSent, setForgotSent] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [householdName, setHouseholdName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "login") {
        await auth.login(email, password);
        router.push("/dashboard");
      } else {
        await auth.register({ email, password, display_name: displayName, household_name: householdName });
        router.push("/onboarding");
      }
    } catch (err: any) {
      setError(err.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-(--color-page)">
      <div className="w-full max-w-[380px]">
        <div className="text-center mb-10">
          <div className="flex justify-center mb-3">
            <MetheanLogoVertical markSize={52} wordmarkHeight={18} color="#0F1B2D" gap={10} />
          </div>
          <p className="text-sm text-(--color-text-secondary) mt-3">A learning operating system for families</p>
        </div>

        <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-6">
          {/* Tab switcher */}
          <div className="flex mb-6 p-1 bg-(--color-page) rounded-lg border border-(--color-border)">
            <button onClick={() => setMode("login")}
              className={`flex-1 py-1.5 text-sm rounded-md transition-colors duration-150 ${
                mode === "login" ? "bg-(--color-surface) text-(--color-text) font-medium shadow-sm" : "text-(--color-text-secondary)"
              }`}>Sign In</button>
            <button onClick={() => setMode("register")}
              className={`flex-1 py-1.5 text-sm rounded-md transition-colors duration-150 ${
                mode === "register" ? "bg-(--color-surface) text-(--color-text) font-medium shadow-sm" : "text-(--color-text-secondary)"
              }`}>Register</button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3">
            {mode === "register" && (
              <>
                <input type="text" placeholder="Your name" value={displayName} onChange={(e) => setDisplayName(e.target.value)}
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent) placeholder:text-(--color-text-tertiary)" required />
                <input type="text" placeholder="Household name" value={householdName} onChange={(e) => setHouseholdName(e.target.value)}
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent) placeholder:text-(--color-text-tertiary)" required />
              </>
            )}
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent) placeholder:text-(--color-text-tertiary)" required />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent) placeholder:text-(--color-text-tertiary)" required minLength={8} />
            {error && <p className="text-xs text-(--color-danger)">{error}</p>}
            <button type="submit" disabled={loading}
              className="w-full py-2.5 text-sm font-medium text-white bg-(--color-accent) rounded-[10px] hover:bg-(--color-accent-hover) disabled:opacity-50 transition-colors duration-150">
              {loading ? "..." : mode === "login" ? "Sign In" : "Create Account"}
            </button>
            {mode === "login" && (
              <button type="button" onClick={() => setMode("forgot")} className="w-full text-center text-xs text-(--color-text-tertiary) hover:text-(--color-accent) mt-2">
                Forgot password?
              </button>
            )}
          </form>
        {mode === "forgot" && (
          <div className="space-y-3">
            {forgotSent ? (
              <div className="text-center py-4">
                <p className="text-sm text-(--color-success) font-medium mb-1">Check your email</p>
                <p className="text-xs text-(--color-text-secondary)">If that email is registered, we sent a reset link.</p>
                <button onClick={() => { setMode("login"); setForgotSent(false); }} className="text-xs text-(--color-accent) mt-3 hover:underline">Back to sign in</button>
              </div>
            ) : (
              <>
                <p className="text-xs text-(--color-text-secondary) mb-2">Enter your email and we&apos;ll send a reset link.</p>
                <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                {error && <p className="text-xs text-(--color-danger)">{error}</p>}
                <button
                  disabled={loading || !email}
                  onClick={async () => { setLoading(true); try { await account.forgotPassword(email); setForgotSent(true); } catch { setError("Something went wrong"); } finally { setLoading(false); } }}
                  className="w-full py-2.5 text-sm font-medium text-white bg-(--color-accent) rounded-[10px] hover:bg-(--color-accent-hover) disabled:opacity-50">
                  {loading ? "..." : "Send Reset Link"}
                </button>
                <button onClick={() => setMode("login")} className="w-full text-center text-xs text-(--color-text-tertiary) hover:text-(--color-accent) mt-1">
                  Back to sign in
                </button>
              </>
            )}
          </div>
        )}
        </div>
      </div>
    </div>
  );
}
