import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

// Regression for METHEAN-6-02. The frontend used to POST to
// /household/invite with role="parent"; the backend mounts these
// endpoints under /api/v1/auth/household/invite and the role enum
// only knows owner / co_parent / observer. This spec intercepts the
// outgoing request to confirm both the path prefix and the role
// string land on canonical values.

test.describe("Family invite", () => {
  test("submits POST /api/v1/auth/household/invite with role=co_parent when 'Parent' is selected", async ({ page }) => {
    await registerAndLogin(page);

    let capturedUrl = "";
    let capturedBody: Record<string, unknown> | null = null;

    // Intercept BEFORE navigating to settings so the route handler is
    // installed in time. Fulfill with a minimal success body so the UI
    // doesn't hang on the response.
    await page.route("**/api/v1/auth/household/invite", async (route) => {
      const req = route.request();
      capturedUrl = req.url();
      try {
        capturedBody = JSON.parse(req.postData() ?? "{}");
      } catch {
        capturedBody = null;
      }
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ invited: true }),
      });
    });

    await page.goto("/settings");
    await page.waitForLoadState("networkidle");

    // Fill the invite form. The settings page uses a plain input +
    // select pair; "Parent" is the display label for value="co_parent".
    const emailInput = page.getByPlaceholder("Email address");
    await emailInput.fill("invitee@example.com");

    // The role <select> is the immediate sibling of the email input.
    // Selecting by label "Parent" maps to the canonical co_parent value.
    const roleSelect = page.locator('select').filter({ hasText: "Parent" });
    await roleSelect.selectOption({ label: "Parent" });

    await page.getByRole("button", { name: /^invite$/i }).click();

    // Wait until our route handler captured the request.
    await expect.poll(() => capturedUrl).toContain("/auth/household/invite");

    expect(capturedUrl.endsWith("/auth/household/invite")).toBe(true);
    expect(capturedBody).not.toBeNull();
    expect(capturedBody!.role).toBe("co_parent");
    expect(capturedBody!.email).toBe("invitee@example.com");
  });
});
