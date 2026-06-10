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
 * Seed a real evidence chain through the public API only: child,
 * subject, map, node, a manual activity, a parent approval (which
 * writes a hashed governance event), and a strong attempt submission
 * (which drives mastery to proficient or above through the real
 * state engine). No direct DB writes, no fabricated data.
 */
async function seedEvidence(page: Page) {
  const child = await api(page, "post", "/children", { first_name: "Recordo" });
  const subject = await api(page, "post", "/subjects", { name: "Mathematics" });
  const map = await api(page, "post", "/learning-maps", { subject_id: subject.id, name: "Math Map" });
  const node = await api(page, "post", `/learning-maps/${map.id}/nodes`, {
    node_type: "concept",
    title: "Addition Facts",
  });

  const today = new Date().toISOString().slice(0, 10);
  const activity = await api(page, "post", "/activities", {
    child_id: child.id,
    title: "Addition practice",
    activity_type: "practice",
    scheduled_date: today,
    estimated_minutes: 25,
    node_id: node.id,
  });

  const plans = await api(page, "get", `/children/${child.id}/plans`);
  const planId = (plans.items || plans)[0].id;
  await api(page, "put", `/plans/${planId}/activities/${activity.id}/approve`, {
    reason: "Reviewed the work together and approved it",
  });

  const attempt = await api(page, "post", `/activities/${activity.id}/attempts`, { child_id: child.id });
  await api(page, "put", `/attempts/${attempt.id}/submit`, {
    confidence: 0.95,
    score: 0.95,
    duration_minutes: 25,
  });

  return { child, node, activity };
}

test("family record shows verified seal, evidence drawer, and sealed export", async ({ page }) => {
  test.setTimeout(120000);
  await registerAndLogin(page);
  await seedEvidence(page);

  await page.goto("/record");
  await page.waitForLoadState("networkidle");

  // Integrity badge: calm, affirmative, verified.
  const badge = page.getByTestId("integrity-badge");
  await expect(badge).toBeVisible({ timeout: 15000 });
  await expect(badge).toHaveAttribute("data-verified", "true");
  await expect(page.getByText(/sealed and verified/i)).toBeVisible();

  // Timeline carries the mastered skill; open its evidence drawer.
  await expect(page.getByTestId("summary-band")).toBeVisible();
  const entry = page.getByTestId("mastery-timeline").getByText("Addition Facts");
  await expect(entry).toBeVisible();
  await entry.click();

  const drawer = page.getByTestId("evidence-drawer");
  await expect(drawer).toBeVisible();
  await expect(drawer.getByText("Addition practice")).toBeVisible();
  // The sealed parent decision renders with its verification line.
  await expect(drawer.getByTestId("drawer-seal").getByTestId("hash-line").first()).toBeVisible();
  await drawer.getByRole("button", { name: /close evidence panel/i }).click();
  await expect(drawer).not.toBeVisible();

  // Export: history is empty, then grows by one with a bundle hash.
  await expect(page.getByTestId("export-panel").getByText(/no exports yet/i)).toBeVisible();
  await page.getByRole("button", { name: /export sealed record/i }).click();

  const result = page.getByTestId("export-result");
  await expect(result).toBeVisible({ timeout: 30000 });
  const bundleHash = await result.getByTestId("hash-line").getAttribute("data-full-hash");
  expect(bundleHash).toMatch(/^[0-9a-f]{64}$/);

  const historyItems = page.getByTestId("export-history").locator("> div");
  await expect(historyItems).toHaveCount(1);

  // A second export grows the history again (and reseals a new head).
  await page.getByRole("button", { name: /export sealed record/i }).click();
  await expect(page.getByTestId("export-history").locator("> div")).toHaveCount(2, { timeout: 30000 });
});

test("empty record renders the encouraging empty state", async ({ page }) => {
  await registerAndLogin(page);
  await api(page, "post", "/children", { first_name: "Fresh" });

  await page.goto("/record");
  await expect(page.getByTestId("integrity-badge")).toBeVisible({ timeout: 15000 });
  await expect(page.getByText(/the record builds itself/i)).toBeVisible();
  await expect(page.getByText(/no exports yet/i)).toBeVisible();
});
