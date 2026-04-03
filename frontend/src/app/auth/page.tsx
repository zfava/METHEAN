"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";

export default function AuthPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "register">("login");
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
    <div className="min-h-screen flex items-center justify-center bg-(--color-bg)">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-semibold tracking-tight">METHEAN</h1>
          <p className="text-sm text-(--color-text-secondary) mt-1">
            A learning operating system for families.
          </p>
        </div>

        <div className="bg-white rounded-lg border border-(--color-border) p-6">
          <div className="flex mb-6 border-b border-(--color-border)">
            <button
              onClick={() => setMode("login")}
              className={`flex-1 pb-3 text-sm font-medium border-b-2 transition-colors ${
                mode === "login" ? "border-(--color-accent) text-(--color-accent)" : "border-transparent text-(--color-text-secondary)"
              }`}
            >
              Sign In
            </button>
            <button
              onClick={() => setMode("register")}
              className={`flex-1 pb-3 text-sm font-medium border-b-2 transition-colors ${
                mode === "register" ? "border-(--color-accent) text-(--color-accent)" : "border-transparent text-(--color-text-secondary)"
              }`}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <>
                <input
                  type="text"
                  placeholder="Your name"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-md focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent)"
                  required
                />
                <input
                  type="text"
                  placeholder="Household name"
                  value={householdName}
                  onChange={(e) => setHouseholdName(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-md focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent)"
                  required
                />
              </>
            )}
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-md focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent)"
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-md focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent)"
              required
              minLength={8}
            />
            {error && <p className="text-xs text-(--color-danger)">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 text-sm font-medium text-white bg-(--color-accent) rounded-md hover:bg-(--color-accent-hover) disabled:opacity-50 transition-colors"
            >
              {loading ? "..." : mode === "login" ? "Sign In" : "Create Account"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
