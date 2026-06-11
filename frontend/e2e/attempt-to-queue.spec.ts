import { test, expect, Page } from "@playwright/test";
import { execSync } from "child_process";
import * as path from "path";
import { registerAndLogin } from "./helpers";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const BACKEND_DIR = path.resolve(__dirname, "../../backend");
const PIN = "1357";

async function csrfHeader(page: Page): Promise<Record<string, string>> {
  const cookies = await page.context().cookies();
  const csrf = cookies.find((c) => c.name === "csrf_token");
  return csrf ? { "X-CSRF-Token": csrf.value } : {};
}

async function api(page: Page, method: "post" | "put" | "get", path_: string, body?: object) {
  const resp = await page.request[method](`${API_BASE}${path_}`, {
    headers: { "Content-Type": "application/json", ...(await csrfHeader(page)) },
    data: body,
  });
  expect(resp.ok(), `${method.toUpperCase()} ${path_} -> ${resp.status()}: ${await resp.text()}`).toBeTruthy();
  return resp.json();
}

/**
 * The thesis sentence, end to end through the browser: the system
 * proposes, the parent disposes, the child executes inside kid mode,
 * and the result lands back on the parent's desk.
 *
 * Two adaptations to the implemented model, by design:
 * - The governance queue holds PRE-execution proposals (the parent
 *   gates what the child may do; attempts on approved work apply
 *   through the state engine), so the walk is propose -> review ->
 *   approve -> child attempt -> progress.
 * - The proposal source is the native curriculum generator (no AI
 *   keys in this environment): far-out weeks materialize unapproved
 *   and await parent review, near weeks are pre-approved for the
 *   child's immediate schedule.
 */
test("system proposes, parent disposes from the queue, child attempts in kid mode, progress lands", async ({ page }) => {
  test.setTimeout(240000);

  const { email } = await registerAndLogin(page);

  const child = await api(page, "post", "/children", { first_name: "Quentin", grade_level: "1st" });
  await api(page, "post", "/auth/pin", { current_password: "TestPass123!", new_pin: PIN });

  execSync(`python -m scripts.grant_native_curriculum_access --email ${email}`, {
    cwd: BACKEND_DIR,
    env: process.env,
    stdio: "pipe",
  });

  // Generate a 6-week native Mathematics block starting today and
  // approve it. Materialization pre-approves the next four weeks and
  // leaves the far weeks as proposals awaiting parent review.
  const year = new Date().getFullYear();
  const today = new Date().toISOString().slice(0, 10);
  const curriculum = await api(page, "post", `/children/${child.id}/curricula/generate`, {
    subject_name: "Mathematics",
    academic_year: `${year}-${year + 1}`,
    hours_per_week: 4,
    total_weeks: 6,
    start_date: today,
    content_tier: "foundational",
  });
  await api(page, "post", `/curricula/${curriculum.id}/approve`);

  // Proposals are waiting for the parent.
  const queueBefore = await api(page, "get", "/governance/queue?limit=50");
  expect(queueBefore.total).toBeGreaterThan(0);

  // Parent reviews in the browser: approve every pending proposal,
  // one decision at a time (each is a hash-chained governance event).
  await page.goto("/governance/queue");
  await page.waitForLoadState("networkidle");
  // The queue cards replay entrance animations on every list
  // re-render; freeze animations so each Approve target stabilizes.
  await page.addStyleTag({
    content: "*, *::before, *::after { animation: none !important; transition: none !important; }",
  });
  await expect(page.getByRole("button", { name: "Approve", exact: true }).first()).toBeVisible({
    timeout: 20000,
  });

  const approveButtons = page.getByRole("button", { name: "Approve", exact: true });
  for (let guard = 0; guard < 40; guard++) {
    const remaining = await approveButtons.count();
    if (remaining === 0) break;
    // The list re-renders after every decision; a card counted a
    // moment ago may already be gone, so each step tolerates the
    // race and simply re-checks on the next pass.
    try {
      const btn = approveButtons.first();
      await btn.scrollIntoViewIfNeeded({ timeout: 5000 });
      await btn.click({ timeout: 8000 });
      await Promise.all([
        page.waitForResponse(
          (resp) => resp.url().includes("/approve") && resp.request().method() === "PUT",
          { timeout: 20000 },
        ),
        page.getByRole("button", { name: "Confirm approval", exact: true }).click({ timeout: 8000 }),
      ]);
    } catch {
      continue;
    }
  }

  // The queue empties: governance is current.
  await expect(page.getByText(/your governance is current/i).first()).toBeVisible({ timeout: 20000 });
  const queueAfter = await api(page, "get", "/governance/queue?limit=50");
  expect(queueAfter.total).toBe(0);

  // Week 1 started today, so the child has approved work today.
  const todayList: any[] = await api(page, "get", `/children/${child.id}/today`);
  expect(todayList.length).toBeGreaterThan(0);
  const target = todayList.find((a) => a.activity_type === "practice") || todayList[0];

  // Enter kid mode: the session swaps to a child-scoped token.
  const [enterResponse] = await Promise.all([
    page.waitForResponse(
      (resp) => resp.url().includes("/auth/child-session/enter") && resp.request().method() === "POST",
      { timeout: 30000 },
    ),
    page.goto("/child"),
  ]);
  expect(enterResponse.status()).toBe(200);

  // First visit shows the kid onboarding wizard; skip it so the
  // today list is interactive.
  const skipWizard = page.getByRole("button", { name: /skip the whole thing/i });
  try {
    await skipWizard.waitFor({ state: "visible", timeout: 10000 });
    await skipWizard.click();
    await skipWizard.waitFor({ state: "hidden", timeout: 10000 });
  } catch {
    // No wizard this run; the today list is already interactive.
  }

  // The child opens today's activity from the kid surface.
  await page.getByText(target.title, { exact: false }).first().click({ timeout: 20000 });
  await expect(page.locator("div").filter({ hasText: target.title }).first()).toBeVisible({
    timeout: 20000,
  });

  // The child submits the attempt through the child-scoped session
  // (the same cookie the kid surface uses; parent surfaces would 403).
  const attempt = await api(page, "post", `/activities/${target.id}/attempts`, {
    child_id: child.id,
  });
  await api(page, "put", `/attempts/${attempt.id}/submit`, {
    confidence: 0.9,
    score: 0.9,
    duration_minutes: 20,
  });

  // Exit kid mode through the PIN gate.
  await page.goto("/child");
  await page.getByRole("button", { name: /exit kid mode/i }).click();
  await expect(page.getByText(/for grown-ups/i)).toBeVisible({ timeout: 10000 });
  for (const digit of PIN.split("")) {
    await page.getByRole("button", { name: `Digit ${digit}`, exact: true }).click();
  }
  await Promise.all([
    page.waitForURL(/\/dashboard/, { timeout: 20000 }),
    page.getByRole("button", { name: "Unlock", exact: true }).click(),
  ]);

  // The parent sees the result: the attempt is completed and today's
  // board reflects it (the today feed lists only scheduled or
  // in-progress work, so the finished activity has left it).
  const submitted = await api(page, "get", `/attempts/${attempt.id}`);
  expect(submitted.status).toBe("completed");
  expect(submitted.score).toBeGreaterThan(0);

  const after: any[] = await api(page, "get", `/children/${child.id}/today`);
  expect(after.find((a) => a.id === target.id)).toBeUndefined();

  // And the queue stays clear: nothing re-entered review.
  const queueFinal = await api(page, "get", "/governance/queue?limit=50");
  expect(queueFinal.total).toBe(0);
});
