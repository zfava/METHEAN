import { Page, expect } from "@playwright/test";

export async function registerAndLogin(page: Page) {
  const email = `test-${Date.now()}@methean.test`;
  const password = "TestPass123!";

  await page.goto("/auth");
  await page.waitForLoadState("networkidle");

  // Switch to register mode
  await page.getByRole("button", { name: /register/i }).click();

  // Wait for register fields to appear
  await expect(page.getByPlaceholder(/your name/i)).toBeVisible({ timeout: 5000 });

  // Fill registration fields
  await page.getByPlaceholder(/your name/i).fill("Test User");
  await page.getByPlaceholder(/household/i).fill("Test Family");
  await page.getByPlaceholder(/email/i).fill(email);
  await page.getByPlaceholder(/password/i).fill(password);

  // Submit
  await page.locator("form").getByRole("button", { name: /create account/i }).click();

  // Wait for navigation away from /auth (catches /onboarding, /dashboard, or any redirect)
  await page.waitForURL(
    (url) => !url.pathname.startsWith("/auth"),
    { timeout: 15000 },
  );

  return { email, password };
}

export async function login(page: Page, email: string, password: string) {
  await page.goto("/auth");
  await page.waitForLoadState("networkidle");

  // Ensure Sign In tab is active
  await page.getByRole("button", { name: /sign in/i }).first().click();

  await page.getByPlaceholder(/email/i).fill(email);
  await page.getByPlaceholder(/password/i).fill(password);

  // Submit inside the form
  await page.locator("form").getByRole("button", { name: /sign in/i }).click();

  // Wait for navigation away from /auth
  await page.waitForURL(
    (url) => !url.pathname.startsWith("/auth"),
    { timeout: 15000 },
  );
}
