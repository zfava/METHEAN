import { test, expect } from "@playwright/test";
import { registerAndLogin, login } from "./helpers";

test("register a new household and navigate away from auth", async ({
  page,
}) => {
  await registerAndLogin(page);
  // Should have navigated away from /auth
  expect(page.url()).not.toContain("/auth");
});

test("login with existing credentials", async ({ page }) => {
  const { email, password } = await registerAndLogin(page);
  await login(page, email, password);
  expect(page.url()).not.toContain("/auth");
});

test("invalid login shows error or stays on auth", async ({ page }) => {
  await page.goto("/auth");
  await page.waitForLoadState("networkidle");

  // Ensure Sign In mode
  await page.getByRole("button", { name: /sign in/i }).first().click();

  await page.getByPlaceholder("Email").fill("nobody@example.com");
  await page.getByPlaceholder("Password").fill("wrongpass123");

  // Submit and wait for the API response
  const [response] = await Promise.all([
    page.waitForResponse(
      (resp) =>
        resp.url().includes("/auth/login") &&
        resp.request().method() === "POST",
      { timeout: 10000 },
    ),
    page
      .locator("form")
      .getByRole("button", { name: /sign in/i })
      .click(),
  ]);

  // Should get 401 (bad credentials) and stay on /auth
  expect(response.status()).toBe(401);
  expect(page.url()).toContain("/auth");
});
