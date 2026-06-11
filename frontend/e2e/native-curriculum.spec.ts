import { test, expect, Page } from "@playwright/test";
import { execSync } from "child_process";
import * as path from "path";
import { registerAndLogin } from "./helpers";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const BACKEND_DIR = path.resolve(__dirname, "../../backend");

async function csrfHeader(page: Page): Promise<Record<string, string>> {
  const cookies = await page.context().cookies();
  const csrf = cookies.find((c) => c.name === "csrf_token");
  return csrf ? { "X-CSRF-Token": csrf.value } : {};
}

async function api(page: Page, method: "post" | "get", path_: string, body?: object) {
  const resp = await page.request[method](`${API_BASE}${path_}`, {
    headers: { "Content-Type": "application/json", ...(await csrfHeader(page)) },
    data: body,
  });
  expect(resp.ok(), `${method.toUpperCase()} ${path_} -> ${resp.status()}: ${await resp.text()}`).toBeTruthy();
  return resp.json();
}

/**
 * The company's core architectural claim: a full year of curriculum
 * generates from the native authored library with NO AI keys
 * configured, and every activity carries real authored content.
 *
 * The native entitlement is a per-household data write with no API
 * surface by design; the test flips it through the real ops script
 * (scripts/grant_native_curriculum_access.py), exactly as production
 * grants do.
 */
test("native curriculum generates a real year with authored content and no AI keys", async ({ page }) => {
  test.setTimeout(300000);

  const { email } = await registerAndLogin(page);

  // A young learner: Foundational tier mathematics.
  const child = await api(page, "post", "/children", {
    first_name: "Nattie",
    grade_level: "1st",
  });

  // Grant the native-curriculum entitlement via the canonical ops
  // script (a data write; there is intentionally no API for it).
  execSync(`python -m scripts.grant_native_curriculum_access --email ${email}`, {
    cwd: BACKEND_DIR,
    env: process.env,
    stdio: "pipe",
  });

  // Generate the annual Mathematics curriculum through the public
  // API the curriculum page calls. No AI keys are configured in this
  // environment: this exercises the native library end to end.
  const year = new Date().getFullYear();
  const curriculum = await api(page, "post", `/children/${child.id}/curricula/generate`, {
    subject_name: "Mathematics",
    academic_year: `${year}-${year + 1}`,
    hours_per_week: 4,
    total_weeks: 36,
    content_tier: "foundational",
  });
  expect(curriculum.id).toBeTruthy();

  await api(page, "post", `/curricula/${curriculum.id}/approve`);

  // Drill the year view: 36 weeks render.
  await page.goto(`/curriculum/year?id=${curriculum.id}`);
  await page.waitForLoadState("networkidle");
  await expect(page.getByText(/36 weeks/i).first()).toBeVisible({ timeout: 20000 });

  const weekRows = page.locator("button", { hasText: /activities/ });
  await expect(weekRows).toHaveCount(36, { timeout: 20000 });

  // The empty-container regression: no week may show zero activities.
  await expect(page.getByText(/^0 activities/)).toHaveCount(0);

  // Open week 1 and see its activity list.
  await weekRows.first().click();
  await expect(page.getByText(/^Activities$/i)).toBeVisible({ timeout: 15000 });

  // Pull week 1 through the same API the view uses and find the day's
  // lesson activity (the year surface lists activities by scheduled
  // day inside the week detail).
  const week1 = await api(page, "get", `/curricula/${curriculum.id}/weeks/1`);
  const activities: any[] = week1.activities || [];
  expect(activities.length).toBeGreaterThan(0);
  const lesson = activities.find((a) => a.type === "lesson") || activities[0];

  // THE assertion that would have caught the empty-container bug:
  // the lesson opens with real authored content, not a hollow shell.
  const ctx = await api(page, "get", `/activities/${lesson.id}/learn?child_id=${child.id}`);
  expect(typeof ctx.lesson.introduction).toBe("string");
  expect(ctx.lesson.introduction.trim().length).toBeGreaterThan(0);

  const items: any[] = ctx.practice?.items || [];
  expect(items.length).toBeGreaterThanOrEqual(1);
  const hints = items[0].hints || (items[0].hint ? [items[0].hint] : []);
  expect(hints.length).toBeGreaterThanOrEqual(1);
  expect(String(hints[0]).trim().length).toBeGreaterThan(0);
});
