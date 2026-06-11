import { test, expect, Page } from "@playwright/test";
import { registerAndLogin } from "./helpers";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function csrfHeader(page: Page): Promise<Record<string, string>> {
  const cookies = await page.context().cookies();
  const csrf = cookies.find((c) => c.name === "csrf_token");
  return csrf ? { "X-CSRF-Token": csrf.value } : {};
}

async function api(page: Page, method: "post" | "put" | "get", path: string, body?: object) {
  const resp = await page.request[method](`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(await csrfHeader(page)) },
    data: body,
  });
  expect(resp.ok(), `${method.toUpperCase()} ${path} -> ${resp.status()}: ${await resp.text()}`).toBeTruthy();
  return resp.json();
}

/**
 * Seed real mastery history through the public API only (the same
 * seed philosophy as family-record.spec.ts): child, subject, map,
 * node, approved activity, strong attempt driving mastery through the
 * real state engine.
 */
async function seedMasteryHistory(page: Page) {
  const child = await api(page, "post", "/children", { first_name: "Expo" });
  const subject = await api(page, "post", "/subjects", { name: "Science" });
  const map = await api(page, "post", "/learning-maps", { subject_id: subject.id, name: "Science Map" });
  const node = await api(page, "post", `/learning-maps/${map.id}/nodes`, {
    node_type: "concept",
    title: "States of Matter",
  });

  const today = new Date().toISOString().slice(0, 10);
  const activity = await api(page, "post", "/activities", {
    child_id: child.id,
    title: "States of matter practice",
    activity_type: "practice",
    scheduled_date: today,
    estimated_minutes: 20,
    node_id: node.id,
  });

  const plans = await api(page, "get", `/children/${child.id}/plans`);
  const planId = (plans.items || plans)[0].id;
  await api(page, "put", `/plans/${planId}/activities/${activity.id}/approve`, {
    reason: "Watched the experiment together and approved it",
  });

  const attempt = await api(page, "post", `/activities/${activity.id}/attempts`, { child_id: child.id });
  await api(page, "put", `/attempts/${attempt.id}/submit`, {
    confidence: 0.95,
    score: 0.95,
    duration_minutes: 20,
  });

  return { child, node };
}

/**
 * The full export and record surface: a family with mastery history
 * opens the Family Record, the integrity badge verifies, an evidence
 * drawer shows the sealed event hash, and a sealed export produces a
 * bundle hash with a download link while the export history grows.
 */
test("record page verifies, evidence shows its hash, export seals with a download link", async ({ page }) => {
  test.setTimeout(180000);
  await registerAndLogin(page);
  await seedMasteryHistory(page);

  await page.goto("/record");
  await page.waitForLoadState("networkidle");

  // Integrity badge: verified against the household hash chain.
  const badge = page.getByTestId("integrity-badge");
  await expect(badge).toBeVisible({ timeout: 15000 });
  await expect(badge).toHaveAttribute("data-verified", "true");

  // One evidence drawer open: the sealed event hash renders.
  await page.getByTestId("mastery-timeline").getByText("States of Matter").click();
  const drawer = page.getByTestId("evidence-drawer");
  await expect(drawer).toBeVisible();
  const hashLine = drawer.getByTestId("hash-line").first();
  await expect(hashLine).toBeVisible();
  const eventHash = await hashLine.getAttribute("data-full-hash");
  expect(eventHash).toMatch(/^[0-9a-f]{64}$/);
  await drawer.getByRole("button", { name: /close evidence panel/i }).click();

  // Export: bundle hash + download link appear, history grows by one.
  const historyItems = page.getByTestId("export-history").locator("> div");
  const before = await historyItems.count();

  await page.getByRole("button", { name: /export sealed record/i }).click();
  const result = page.getByTestId("export-result");
  await expect(result).toBeVisible({ timeout: 30000 });

  const bundleHash = await result.getByTestId("hash-line").getAttribute("data-full-hash");
  expect(bundleHash).toMatch(/^[0-9a-f]{64}$/);
  await expect(result.getByRole("link", { name: /download bundle/i })).toBeVisible();

  await expect(historyItems).toHaveCount(before + 1, { timeout: 30000 });
});
