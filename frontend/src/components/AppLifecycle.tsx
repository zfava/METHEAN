"use client";

import { useEffect } from "react";
import { isNative, configureStatusBar, hideSplash, configureKeyboard } from "@/lib/native";

export default function AppLifecycle() {
  useEffect(() => {
    if (!isNative()) return;

    configureStatusBar();
    configureKeyboard();

    // Hide splash after content is rendered
    const timer = setTimeout(() => hideSplash(), 500);
    return () => clearTimeout(timer);
  }, []);

  return null;
}
