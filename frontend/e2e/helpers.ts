import { Page } from "@playwright/test";

export async function registerAndLogin(page: Page) {
  const email = `test-${Date.now()}@methean.test`;
  const password = "TestPass123!";

  await page.goto("/auth");

  // Switch to register mode by clicking the "Register" tab button
  await page.getByRole("button", { name: /register/i }).click();

  // Fill registration fields (order: name, household, email, password)
  await page.getByPlaceholder(/your name/i).fill("Test User");
  await page.getByPlaceholder(/household/i).fill("Test Family");
  await page.getByPlaceholder(/email/i).fill(email);
  await page.getByPlaceholder(/password/i).fill(password);

  // Click "Create Account" submit button inside the form
  await page.locator("form").getByRole("button", { name: /create account/i }).click();

  // Register redirects to /onboarding
  await page.waitForURL(/onboarding|dashboard/, { timeout: 15000 });

  return { email, password };
}

export async function login(page: Page, email: string, password: string) {
  await page.goto("/auth");

  // Ensure we're on the Sign In tab (default, but be explicit)
  const signInTab = page.getByRole("button", { name: /sign in/i }).first();
  await signInTab.click();

  await page.getByPlaceholder(/email/i).fill(email);
  await page.getByPlaceholder(/password/i).fill(password);

  // Click submit inside the form (not the tab switcher)
  await page.locator("form").getByRole("button", { name: /sign in/i }).click();

  await page.waitForURL(/dashboard/, { timeout: 15000 });
}
