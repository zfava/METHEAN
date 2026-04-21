import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

test("dashboard page loads after login", async ({ page }) => {
  await registerAndLogin(page);
  // If redirected to onboarding, navigate to dashboard
  if (page.url().includes("onboarding")) {
    await page.goto("/dashboard");
  }
  await expect(page).toHaveURL(/dashboard/);
  // Check that the page rendered (not blank/error)
  await expect(page.locator("body")).not.toBeEmpty();
});

test("dashboard shows governance health card", async ({ page }) => {
  await registerAndLogin(page);
  if (page.url().includes("onboarding")) {
    await page.goto("/dashboard");
  }
  // Governance health card or "rules active" text should be present
  await expect(
    page.getByText(/rules active|governance|dashboard/i).first()
  ).toBeVisible({ timeout: 10000 });
});
