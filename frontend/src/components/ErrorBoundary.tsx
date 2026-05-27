"use client";

import React from "react";

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
  message: string | null;
}

// Coerce any thrown value into a string. React Error #31 happens when an
// object is rendered as a child; guard against that even if a future
// throw site hands us a non-Error (e.g. a raw API payload).
function safeMessage(err: unknown): string {
  if (err instanceof Error) return err.message || err.name || "Unknown error";
  if (typeof err === "string") return err;
  if (err == null) return "Unknown error";
  try {
    return JSON.stringify(err);
  } catch {
    return String(err);
  }
}

export default class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, message: null };
  }

  static getDerivedStateFromError(error: unknown): State {
    return { hasError: true, message: safeMessage(error) };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-(--color-bg)">
          <div className="max-w-md w-full bg-(--color-surface) rounded-lg border border-(--color-border) p-8 text-center">
            <div className="text-2xl mb-3 text-(--color-text-secondary)">&#9888;</div>
            <h2 className="text-sm font-semibold mb-2">Something went wrong</h2>
            <p className="text-xs text-(--color-text-secondary) mb-4">
              Your data is safe. This error has been logged.
            </p>
            {this.state.message && (
              <pre className="text-[11px] font-mono bg-(--color-page) rounded p-3 mb-4 text-left overflow-auto max-h-24 text-(--color-text-secondary)">
                {this.state.message}
              </pre>
            )}
            <button
              onClick={() => this.setState({ hasError: false, message: null })}
              className="px-4 py-2 text-sm font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover) transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
