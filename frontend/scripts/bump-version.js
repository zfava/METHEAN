#!/usr/bin/env node

/**
 * Bump version across all targets:
 * - package.json
 * - ios/App/App/Info.plist (if exists)
 * - android/app/build.gradle (if exists)
 *
 * Usage: node scripts/bump-version.js [patch|minor|major]
 * Default: patch
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const bumpType = process.argv[2] || "patch";

if (!["patch", "minor", "major"].includes(bumpType)) {
  console.error("Usage: node scripts/bump-version.js [patch|minor|major]");
  process.exit(1);
}

// Read current version from package.json
const pkgPath = path.join(ROOT, "package.json");
const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf-8"));
const [major, minor, patch] = pkg.version.split(".").map(Number);

let newVersion;
switch (bumpType) {
  case "major": newVersion = `${major + 1}.0.0`; break;
  case "minor": newVersion = `${major}.${minor + 1}.0`; break;
  case "patch": newVersion = `${major}.${minor}.${patch + 1}`; break;
}

console.log(`Bumping ${bumpType}: ${pkg.version} → ${newVersion}`);

// 1. Update package.json
pkg.version = newVersion;
fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + "\n");
console.log("  ✓ package.json");

// 2. Update iOS Info.plist (if exists)
const plistPath = path.join(ROOT, "ios", "App", "App", "Info.plist");
if (fs.existsSync(plistPath)) {
  let plist = fs.readFileSync(plistPath, "utf-8");
  // CFBundleShortVersionString
  plist = plist.replace(
    /(<key>CFBundleShortVersionString<\/key>\s*<string>)[^<]*/,
    `$1${newVersion}`
  );
  // CFBundleVersion (use integer: major*10000 + minor*100 + patch)
  const buildNum = (major + (bumpType === "major" ? 1 : 0)) * 10000 +
    (minor + (bumpType === "minor" ? 1 : 0)) * 100 +
    (patch + (bumpType === "patch" ? 1 : 0));
  plist = plist.replace(
    /(<key>CFBundleVersion<\/key>\s*<string>)[^<]*/,
    `$1${buildNum}`
  );
  fs.writeFileSync(plistPath, plist);
  console.log("  ✓ ios/App/App/Info.plist");
} else {
  console.log("  - ios/App/App/Info.plist (not found, skipping)");
}

// 3. Update Android build.gradle (if exists)
const gradlePath = path.join(ROOT, "android", "app", "build.gradle");
if (fs.existsSync(gradlePath)) {
  let gradle = fs.readFileSync(gradlePath, "utf-8");
  gradle = gradle.replace(/versionName "[^"]*"/, `versionName "${newVersion}"`);
  // versionCode: integer, increment by 1
  const match = gradle.match(/versionCode (\d+)/);
  if (match) {
    const newCode = parseInt(match[1]) + 1;
    gradle = gradle.replace(/versionCode \d+/, `versionCode ${newCode}`);
  }
  fs.writeFileSync(gradlePath, gradle);
  console.log("  ✓ android/app/build.gradle");
} else {
  console.log("  - android/app/build.gradle (not found, skipping)");
}

console.log(`\nVersion bumped to ${newVersion}`);
console.log("Next: commit, tag, and push:");
console.log(`  git commit -am "v${newVersion}"`);
console.log(`  git tag v${newVersion}`);
console.log(`  git push && git push --tags`);
