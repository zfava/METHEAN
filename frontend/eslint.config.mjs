// ESLint 9 flat-config entry point. Ports the legacy .eslintrc.json
// rules exactly via @eslint/eslintrc's FlatCompat shim so we keep the
// `next/core-web-vitals` rule set from before the migration.
//
// TODO(methean-6-12): once the codebase has time for a wider lint
// pass, layer `next/typescript` on top of core-web-vitals to catch
// `any` usage, unused imports, and unsafe enum comparisons. Doing
// that here would surface dozens of unrelated errors.

import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const compat = new FlatCompat({ baseDirectory: __dirname });

export default [
  ...compat.extends("next/core-web-vitals"),
  {
    rules: {
      "react/no-unescaped-entities": "off",
      "react-hooks/exhaustive-deps": "warn",
      "@next/next/no-page-custom-font": "off",
    },
  },
  {
    ignores: ["node_modules/", ".next/", "out/", "build/", "dist/"],
  },
];
