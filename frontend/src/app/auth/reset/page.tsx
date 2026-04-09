"use client";

import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { account } from "@/lib/api";
import { MetheanLogoVertical } from "@/components/Brand";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";

export default function ResetPasswordPage() {
  const params = useSearchParams();
  const router = useRouter();
  const token = params.get("token") || "";

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  async function handleReset() {
    if (password.length < 8) { setError("Password must be at least 8 characters"); return; }
    if (password !== confirm) { setError("Passwords don't match"); return; }
    setLoading(true);
    setError("");
    try {
      await account.resetPassword(token, password);
      setSuccess(true);
    } catch (err: any) {
      setError(err?.detail || "Invalid or expired reset link");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-(--color-page) px-4">
      <div className="w-full max-w-sm">
        <div className="flex justify-center mb-6">
          <MetheanLogoVertical markSize={40} wordmarkHeight={16} color="#0F1B2D" gap={8} />
        </div>

        {success ? (
          <Card>
            <div className="text-center py-4">
              <div className="w-12 h-12 rounded-full bg-(--color-success-light) flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-(--color-text) mb-1">Password reset!</h2>
              <p className="text-sm text-(--color-text-secondary) mb-4">You can now sign in with your new password.</p>
              <Button variant="primary" size="lg" className="w-full" onClick={() => router.push("/auth")}>
                Sign In
              </Button>
            </div>
          </Card>
        ) : (
          <Card>
            <h2 className="text-lg font-semibold text-(--color-text) mb-1">Set new password</h2>
            <p className="text-xs text-(--color-text-secondary) mb-4">Enter your new password below.</p>
            {error && <p className="text-xs text-(--color-danger) mb-3">{error}</p>}
            <div className="space-y-3">
              <input
                type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="New password (min 8 characters)"
                className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px]"
              />
              <input
                type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)}
                placeholder="Confirm password"
                className="w-full px-3 py-2.5 text-sm border border-(--color-border-strong) rounded-[10px]"
              />
              <Button variant="primary" size="lg" className="w-full" onClick={handleReset} disabled={loading || !password || !confirm}>
                {loading ? "Resetting..." : "Reset Password"}
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
