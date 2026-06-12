import { test, expect } from "@playwright/test";
import { registerAndLogin } from "./helpers";

/**
 * The backend gates child-data routes for unverified accounts with a
 * 403 whose detail is "email_not_verified". This used to leak onto
 * parent pages as a raw error card with a Retry button. The api client
 * now maps that response to a dedicated verification banner.
 *
 * CI registers auto-verify (no RESEND_API_KEY in the test env), so we
 * reproduce the gate by forcing the 403 on child-data calls while
 * leaving /auth/* on the real backend, which keeps the session live and
 * lets the banner greet the user by the address the link was sent to.
 */
test("an unverified account sees the verification banner, not the raw gate code", async ({
  page,
}) => {
  await registerAndLogin(page);

  await page.route("**/api/v1/**", async (route) => {
    if (route.request().url().includes("/api/v1/auth/")) {
      return route.fallback();
    }
    return route.fulfill({
      status: 403,
      contentType: "application/json",
      body: JSON.stringify({ detail: "email_not_verified" }),
    });
  });

  await page.goto("/dashboard");

  await expect(page.getByText("Verify your email to continue")).toBeVisible();
  await expect(page.getByText("email_not_verified")).toHaveCount(0);
});
