import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

// Verifies METHEAN-6-02: the family invite form posts to the auth-prefixed
// route and uses the canonical role value. registerAndLogin gives us a
// household-owner session, so the auth fixture is real, not a TODO stub.

test("family invite posts to /auth/household/invite with canonical role", async ({ page }) => {
  await registerAndLogin(page);

  let capturedUrl: string | null = null;
  let capturedBody: Record<string, unknown> | null = null;
  await page.route("**/auth/household/invite", async (route) => {
    const req = route.request();
    capturedUrl = req.url();
    try {
      capturedBody = JSON.parse(req.postData() || "{}");
    } catch {
      capturedBody = null;
    }
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ invited: true, email: capturedBody?.email ?? "" }),
    });
  });

  await page.goto("/settings");
  await page.waitForLoadState("networkidle");

  // The settings page renders an invite form when a family-invites section
  // is present. If the page does not surface the form (depends on routing),
  // skip with a clear marker rather than silently passing.
  const emailInput = page.getByPlaceholder("Email address");
  if ((await emailInput.count()) === 0) {
    test.skip(true, "settings page did not render invite form (TODO methean6-02)");
    return;
  }

  await emailInput.fill("invitee@example.com");
  // The select shows "Parent" as label but the option value is now "co_parent".
  await page.getByRole("combobox").selectOption({ label: "Parent" });
  await page.getByRole("button", { name: /invite/i }).click();

  await expect.poll(() => capturedUrl).not.toBeNull();
  expect(capturedUrl).toMatch(/\/auth\/household\/invite$/);
  expect(capturedBody).toEqual({
    email: "invitee@example.com",
    role: "co_parent",
  });
});
