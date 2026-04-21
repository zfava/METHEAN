import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

test("governance rules page loads", async ({ page }) => {
  await registerAndLogin(page);
  await page.goto("/governance/rules");
  await expect(page).toHaveURL(/governance\/rules/);
  // Page should render without error
  await expect(page.locator("body")).not.toBeEmpty();
});

test("governance queue page loads", async ({ page }) => {
  await registerAndLogin(page);
  await page.goto("/governance/queue");
  await expect(page).toHaveURL(/governance\/queue/);
  // Should show either queue items or "all clear" empty state
  await expect(
    page.getByText(/queue|approval|all clear|review/i).first()
  ).toBeVisible({ timeout: 10000 });
});
