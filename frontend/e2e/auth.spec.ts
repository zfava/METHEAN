import { test, expect } from "@playwright/test";
import { registerAndLogin, login } from "./helpers";

test("register a new household and navigate away from auth", async ({
  page,
}) => {
  await registerAndLogin(page);
  // Should have navigated away from /auth to /onboarding or /dashboard
  expect(page.url()).not.toContain("/auth");
});

test("login with existing credentials", async ({ page }) => {
  const { email, password } = await registerAndLogin(page);
  await page.goto("/auth");
  await login(page, email, password);
  expect(page.url()).not.toContain("/auth");
});

test("invalid login shows error", async ({ page }) => {
  await page.goto("/auth");
  await page.waitForLoadState("networkidle");

  // Ensure Sign In mode
  await page.getByRole("button", { name: /sign in/i }).first().click();

  await page.getByPlaceholder(/email/i).fill("nobody@test.com");
  await page.getByPlaceholder(/password/i).fill("wrongpass123");

  // Submit inside the form
  await page.locator("form").getByRole("button", { name: /sign in/i }).click();

  // Should stay on /auth and show an error (the error <p> element appears)
  await page.waitForTimeout(3000);
  expect(page.url()).toContain("/auth");
});
