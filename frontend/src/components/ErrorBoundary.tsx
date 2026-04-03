"use client";

import React from "react";

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-(--color-bg)">
          <div className="max-w-md w-full bg-white rounded-lg border border-(--color-border) p-8 text-center">
            <div className="text-2xl mb-3 text-(--color-text-secondary)">&#9888;</div>
            <h2 className="text-sm font-semibold mb-2">Something went wrong</h2>
            <p className="text-xs text-(--color-text-secondary) mb-4">
              Your data is safe. This error has been logged.
            </p>
            {this.state.error && (
              <pre className="text-[11px] font-mono bg-gray-50 rounded p-3 mb-4 text-left overflow-auto max-h-24 text-(--color-text-secondary)">
                {this.state.error.message}
              </pre>
            )}
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
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
