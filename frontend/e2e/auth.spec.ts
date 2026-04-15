import { test, expect } from "@playwright/test";
import { registerAndLogin, login } from "./helpers";

test("register a new household and reach onboarding or dashboard", async ({
  page,
}) => {
  const { email } = await registerAndLogin(page);
  const url = page.url();
  expect(url.includes("onboarding") || url.includes("dashboard")).toBe(true);
});

test("login with existing credentials", async ({ page }) => {
  const { email, password } = await registerAndLogin(page);
  // Navigate away then back to login
  await page.goto("/auth");
  await login(page, email, password);
  expect(page.url()).toContain("dashboard");
});

test("invalid login shows error", async ({ page }) => {
  await page.goto("/auth");
  // Ensure Sign In tab is active
  await page.getByRole("button", { name: /sign in/i }).first().click();
  await page.getByPlaceholder(/email/i).fill("nobody@test.com");
  await page.getByPlaceholder(/password/i).fill("wrongpass123");
  // Click submit inside the form (not the tab button)
  await page.locator("form").getByRole("button", { name: /sign in/i }).click();
  // Should see an error message
  await expect(
    page.locator(".text-\\(--color-danger\\), [class*='danger']").first()
  ).toBeVisible({ timeout: 5000 });
});
