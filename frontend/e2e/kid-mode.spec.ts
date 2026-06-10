import { test, expect, Page } from "@playwright/test";
import { registerAndLogin } from "./helpers";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const PIN = "2468";

async function csrfHeader(page: Page): Promise<Record<string, string>> {
  const cookies = await page.context().cookies();
  const csrf = cookies.find((c) => c.name === "csrf_token");
  return csrf ? { "X-CSRF-Token": csrf.value } : {};
}

async function apiPost(page: Page, path: string, body: object) {
  return page.request.post(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(await csrfHeader(page)) },
    data: body,
  });
}

test("kid mode locks the parent surface behind the PIN gate", async ({ page }) => {
  test.setTimeout(120000);
  await registerAndLogin(page);

  // Create a child and set the kid-mode PIN through the API (the
  // session cookies and CSRF token come from the real login above).
  const childResp = await apiPost(page, "/children", { first_name: "Kiddo" });
  expect(childResp.status()).toBe(201);

  const pinResp = await apiPost(page, "/auth/pin", {
    current_password: "TestPass123!",
    new_pin: PIN,
  });
  expect(pinResp.ok()).toBeTruthy();

  // Entering /child swaps the session for a child-scoped token.
  const [enterResponse] = await Promise.all([
    page.waitForResponse(
      (resp) => resp.url().includes("/auth/child-session/enter") && resp.request().method() === "POST",
      { timeout: 20000 },
    ),
    page.goto("/child"),
  ]);
  expect(enterResponse.status()).toBe(200);

  // Parent navigation bounces back to the kid surface.
  await page.goto("/governance/queue");
  await page.waitForURL(/\/child/, { timeout: 15000 });

  // The child-scoped cookie is rejected on parent APIs server-side.
  const queueResp = await page.request.get(`${API_BASE}/governance/queue`);
  expect(queueResp.status()).toBe(403);
  expect((await queueResp.json()).detail).toBe("child_session_forbidden");

  // Open the exit gate.
  await page.goto("/child");
  await page.getByRole("button", { name: /exit kid mode/i }).click();
  await expect(page.getByText(/for grown-ups/i)).toBeVisible({ timeout: 10000 });

  // Wrong PIN shakes and stays in kid mode.
  for (const digit of ["1", "1", "1", "1"]) {
    await page.getByRole("button", { name: `Digit ${digit}`, exact: true }).click();
  }
  await page.getByRole("button", { name: "Unlock", exact: true }).click();
  await expect(page.getByText(/didn't work/i)).toBeVisible({ timeout: 10000 });
  expect(page.url()).toContain("/child");

  // Correct PIN restores the parent session and lands on the parent
  // dashboard.
  for (const digit of PIN.split("")) {
    await page.getByRole("button", { name: `Digit ${digit}`, exact: true }).click();
  }
  await Promise.all([
    page.waitForURL(/\/dashboard/, { timeout: 20000 }),
    page.getByRole("button", { name: "Unlock", exact: true }).click(),
  ]);

  // Parent API access works again.
  const afterExit = await page.request.get(`${API_BASE}/governance/queue`);
  expect(afterExit.status()).toBe(200);
});
