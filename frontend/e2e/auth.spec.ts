import { test, expect } from "@playwright/test";
import { registerAndLogin, login } from "./helpers";

test("register a new household and reach dashboard or onboarding", async ({
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
  await page.getByPlaceholder(/email/i).fill("nobody@test.com");
  await page.getByPlaceholder(/password/i).first().fill("wrongpass");
  await page.getByRole("button", { name: /log in|sign in/i }).click();
  // Should see an error message, not redirect
  await expect(
    page.getByText(/invalid|incorrect|error|wrong/i)
  ).toBeVisible({ timeout: 5000 });
});
