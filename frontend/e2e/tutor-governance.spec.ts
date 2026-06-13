import { test, expect, Page } from "@playwright/test";
import { execSync } from "child_process";
import * as path from "path";
import { registerAndLogin } from "./helpers";

/**
 * The parent governed tutor, end to end through the browser.
 *
 * One continuous journey across the tutor governance surface: a parent
 * sets the tutor policy, disposes of a memory proposal, grants and revokes
 * a standing autonomy grant, chooses the developmental voice, opts into and
 * out of relationship memory, and finally turns the tutor off and confirms
 * the child sees a kind unavailable state rather than a broken one.
 *
 * Seeding convention: the two artifacts that the mock AI environment cannot
 * produce on its own (a tutor memory proposal and a derived milestone) are
 * seeded through the real backend services, run with execSync the same way
 * attempt-to-queue.spec.ts seeds through scripts. The write paths under test
 * (route_proposal, the streak that derives a milestone) are the production
 * ones, so the browser journey exercises the true contracts.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const BACKEND_DIR = path.resolve(__dirname, "../../backend");
const PIN = "2468";

async function csrfHeader(page: Page): Promise<Record<string, string>> {
  const cookies = await page.context().cookies();
  const csrf = cookies.find((c) => c.name === "csrf_token");
  return csrf ? { "X-CSRF-Token": csrf.value } : {};
}

async function api(page: Page, method: "post" | "put" | "get", path_: string, body?: object) {
  const resp = await page.request[method](`${API_BASE}${path_}`, {
    headers: { "Content-Type": "application/json", ...(await csrfHeader(page)) },
    data: body,
  });
  expect(resp.ok(), `${method.toUpperCase()} ${path_} -> ${resp.status()}: ${await resp.text()}`).toBeTruthy();
  return resp.json();
}

/** Run a small async snippet against the backend's real services and DB. */
function backend(py: string, ...args: string[]) {
  const escaped = args.map((a) => `'${a.replace(/'/g, "")}'`).join(" ");
  execSync(`python -c "${py.replace(/"/g, '\\"')}" ${escaped}`, {
    cwd: BACKEND_DIR,
    env: process.env,
    stdio: "pipe",
  });
}

const SEED_PROPOSAL = `
import asyncio, sys, uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.core.database import set_tenant
from app.models.identity import Child
from app.services.tutor_profile import route_proposal
async def main(child_id, content):
    engine = create_async_engine(settings.DATABASE_URL)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as db:
        child = (await db.execute(select(Child).where(Child.id == uuid.UUID(child_id)))).scalar_one()
        await set_tenant(db, child.household_id)
        await route_proposal(db, child.household_id, child.id, {'category': 'pacing', 'content': content})
        await db.commit()
    await engine.dispose()
asyncio.run(main(sys.argv[1], sys.argv[2]))
`;

const SEED_STREAK = `
import asyncio, sys, uuid
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.core.database import set_tenant
from app.models.identity import Child
from app.models.achievements import Streak
async def main(child_id):
    engine = create_async_engine(settings.DATABASE_URL)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as db:
        child = (await db.execute(select(Child).where(Child.id == uuid.UUID(child_id)))).scalar_one()
        await set_tenant(db, child.household_id)
        db.add(Streak(child_id=child.id, household_id=child.household_id, current_streak=7, longest_streak=14, last_activity_date=date(2026, 6, 12)))
        await db.commit()
    await engine.dispose()
asyncio.run(main(sys.argv[1]))
`;

test("a parent governs the tutor end to end: policy, memory, grant, voice, relationship, off", async ({ page }) => {
  test.setTimeout(240000);

  const { email } = await registerAndLogin(page);
  const child = await api(page, "post", "/children", { first_name: "Devon", grade_level: "5th" });
  await api(page, "post", "/auth/pin", { current_password: "TestPass123!", new_pin: PIN });

  // A native curriculum gives the child a real, openable activity for the
  // unavailable check at the end.
  execSync(`python -m scripts.grant_native_curriculum_access --email ${email}`, {
    cwd: BACKEND_DIR,
    env: process.env,
    stdio: "pipe",
  });
  const year = new Date().getFullYear();
  const today = new Date().toISOString().slice(0, 10);
  const curriculum = await api(page, "post", `/children/${child.id}/curricula/generate`, {
    subject_name: "Mathematics",
    academic_year: `${year}-${year + 1}`,
    hours_per_week: 4,
    total_weeks: 2,
    start_date: today,
    content_tier: "foundational",
  });
  await api(page, "post", `/curricula/${curriculum.id}/approve`);

  await page.goto("/governance/ai");
  await page.waitForLoadState("networkidle");
  await page.addStyleTag({
    content: "*, *::before, *::after { animation: none !important; transition: none !important; }",
  });

  const tutorRow = page.getByTestId("role-row-tutor");
  await expect(tutorRow).toBeVisible();

  // 1. Set the tutor policy to standard (Approve each change).
  await tutorRow.getByRole("button", { name: "Approve each change" }).click();
  await expect(tutorRow.getByRole("button", { name: "Approve each change" })).toHaveAttribute("aria-pressed", "true");

  // 2. A memory proposal appears in the review queue (seeded through the
  //    real route_proposal service), and the parent approves it.
  backend(SEED_PROPOSAL, child.id, "Short timed bursts with an early easy win keep this learner moving.");
  await page.reload();
  await page.waitForLoadState("networkidle");
  const proposalCard = page.getByText("Short timed bursts with an early easy win keep this learner moving.");
  await expect(proposalCard).toBeVisible();
  await page.getByRole("button", { name: "Approve", exact: true }).first().click();
  // It moves out of review and into what the tutor remembers.
  await expect(page.getByText("What the tutor remembers", { exact: false })).toBeVisible();

  // 3. Switch to autonomous and confirm the standing grant dialog.
  await tutorRow.getByRole("button", { name: "Autonomous" }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await expect(dialog.getByText(/Grant standing autonomy/i)).toBeVisible();
  await dialog.getByRole("button", { name: "Grant autonomy" }).click();

  // The standing grant line is shown while autonomous.
  await expect(page.getByText("Your standing grant is active", { exact: false })).toBeVisible();
  await expect(tutorRow.getByRole("button", { name: "Autonomous" })).toHaveAttribute("aria-pressed", "true");

  // 4. Revoke the grant with one tap (returning to Approve each change needs
  //    no confirmation), and the standing grant line clears.
  await tutorRow.getByRole("button", { name: "Approve each change" }).click();
  await expect(tutorRow.getByRole("button", { name: "Approve each change" })).toHaveAttribute("aria-pressed", "true");
  await expect(page.getByText("Your standing grant is active", { exact: false })).toHaveCount(0);

  // 5. Set the developmental voice override.
  const registerSelect = page.getByTestId("register-override-select");
  await expect(registerSelect).toBeVisible();
  await registerSelect.selectOption("advanced");
  await expect(page.getByText("you chose this", { exact: false })).toBeVisible();

  // 6. Enable relationship memory and watch the preview populate. A seeded
  //    streak gives the child a derivable milestone, so the preview shows a
  //    real line (exactly what the tutor would see), not just the empty copy.
  //    The control renders nothing until its relationship-memory GET resolves,
  //    so wait for the control itself before touching the toggle inside it.
  backend(SEED_STREAK, child.id);
  const memoryControl = page.getByTestId("relationship-memory-control");
  await expect(memoryControl).toBeVisible();
  const memoryToggle = memoryControl.getByTestId("relationship-memory-toggle");
  // Off is the default: no preview yet, and the toggle invites turning it on.
  await expect(page.getByTestId("relationship-memory-preview")).toHaveCount(0);
  await expect(memoryToggle).toHaveText("Turn on");

  // The off to on transition: the preview appears and populates with the
  // seeded milestone, which is exactly what the tutor would see.
  await memoryToggle.click();
  await expect(page.getByTestId("relationship-memory-preview")).toBeVisible();
  await expect(page.getByTestId("relationship-memory-milestone").first()).toBeVisible();
  await expect(memoryToggle).toHaveText("Turn off");

  // 7. Disable it and the preview is gone.
  await memoryToggle.click();
  await expect(page.getByTestId("relationship-memory-preview")).toHaveCount(0);

  // 8. Turn the tutor off entirely; the memory surface confirms the role is off.
  await tutorRow.getByRole("button", { name: "Off", exact: true }).click();
  await expect(page.getByTestId("tutor-memory-off")).toBeVisible();

  // 9. The child tutor surface shows a kind unavailable state, not an error.
  //    Enter kid mode, open the first activity, ask the tutor, and the reply
  //    is the gentle fallback rather than a broken screen.
  await page.goto("/child");
  await page.waitForLoadState("networkidle");
  const enter = await page.request.post(`${API_BASE}/auth/child-session/enter`, {
    headers: { "Content-Type": "application/json", ...(await csrfHeader(page)) },
    data: { child_id: child.id },
  });
  expect(enter.ok(), `enter kid mode -> ${enter.status()}`).toBeTruthy();
  await page.reload();
  await page.waitForLoadState("networkidle");

  const skip = page.getByRole("button", { name: /skip the whole thing/i });
  if (await skip.isVisible().catch(() => false)) {
    await skip.click();
  }

  const stuck = page.getByRole("button", { name: /i'?m stuck|talk to your tutor/i }).first();
  await expect(stuck).toBeVisible({ timeout: 20000 });
  await stuck.click();

  const tutorInput = page.getByRole("textbox").first();
  await expect(tutorInput).toBeVisible();
  await tutorInput.fill("Can you help me with this problem?");
  await tutorInput.press("Enter");

  // The tutor is off: the child gets a calm, kind message, never a crash.
  await expect(page.getByText(/having trouble thinking right now/i)).toBeVisible({ timeout: 20000 });
});
