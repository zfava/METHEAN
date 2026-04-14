import { Page } from "@playwright/test";

export async function registerAndLogin(page: Page) {
  const email = `test-${Date.now()}@methean.test`;
  const password = "TestPass123!";

  await page.goto("/auth");

  // Switch to register tab if needed
  const registerTab = page.getByRole("tab", { name: /register|sign up/i });
  if (await registerTab.isVisible().catch(() => false)) await registerTab.click();

  // Try to find register-specific fields
  const nameInput = page.getByPlaceholder(/name|household|family/i).first();
  if (await nameInput.isVisible().catch(() => false)) {
    await nameInput.fill("Test Family");
  }

  await page.getByPlaceholder(/email/i).fill(email);
  await page.getByPlaceholder(/password/i).first().fill(password);

  // Click register/create button
  const registerBtn = page.getByRole("button", { name: /register|sign up|create account/i });
  if (await registerBtn.isVisible().catch(() => false)) {
    await registerBtn.click();
  }

  // Wait for redirect to onboarding or dashboard
  await page.waitForURL(/onboarding|dashboard/, { timeout: 10000 });

  return { email, password };
}

export async function login(page: Page, email: string, password: string) {
  await page.goto("/auth");
  await page.getByPlaceholder(/email/i).fill(email);
  await page.getByPlaceholder(/password/i).first().fill(password);

  const loginBtn = page.getByRole("button", { name: /log in|sign in/i });
  await loginBtn.click();

  await page.waitForURL(/dashboard/, { timeout: 10000 });
}
