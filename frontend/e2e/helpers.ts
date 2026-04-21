import { Page, expect } from "@playwright/test";

export async function registerAndLogin(page: Page) {
  const email = `test-${Date.now()}@example.com`;
  const password = "TestPass123!";

  await page.goto("/auth");
  await page.waitForLoadState("networkidle");

  // Switch to register mode
  await page.getByRole("button", { name: /register/i }).click();

  // Wait for register fields to appear
  await expect(page.getByPlaceholder("Your name")).toBeVisible({ timeout: 5000 });

  // Fill all required fields
  await page.getByPlaceholder("Your name").fill("Test User");
  await page.getByPlaceholder("Household name").fill("Test Family");
  await page.getByPlaceholder("Email").fill(email);
  await page.getByPlaceholder("Password").fill(password);

  // Click submit and wait for the API response
  const [response] = await Promise.all([
    page.waitForResponse(
      (resp) => resp.url().includes("/auth/register") && resp.request().method() === "POST",
      { timeout: 15000 },
    ),
    page.locator("form").getByRole("button", { name: /create account/i }).click(),
  ]);

  const status = response.status();
  if (status !== 201 && status !== 200) {
    const body = await response.text();
    throw new Error(`Registration failed with ${status}: ${body}`);
  }

  // Wait for client-side navigation, or navigate manually if router.push didn't fire
  try {
    await page.waitForURL((url) => !url.pathname.startsWith("/auth"), { timeout: 5000 });
  } catch {
    // router.push may not have triggered — navigate manually
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
  }

  return { email, password };
}

export async function login(page: Page, email: string, password: string) {
  await page.goto("/auth");
  await page.waitForLoadState("networkidle");

  // Ensure Sign In tab is active
  await page.getByRole("button", { name: /sign in/i }).first().click();

  await page.getByPlaceholder("Email").fill(email);
  await page.getByPlaceholder("Password").fill(password);

  // Click submit and wait for the API response
  const [response] = await Promise.all([
    page.waitForResponse(
      (resp) => resp.url().includes("/auth/login") && resp.request().method() === "POST",
      { timeout: 15000 },
    ),
    page.locator("form").getByRole("button", { name: /sign in/i }).click(),
  ]);

  const status = response.status();
  if (status !== 200) {
    const body = await response.text();
    throw new Error(`Login failed with ${status}: ${body}`);
  }

  // Wait for client-side navigation
  try {
    await page.waitForURL((url) => !url.pathname.startsWith("/auth"), { timeout: 5000 });
  } catch {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
  }
}
