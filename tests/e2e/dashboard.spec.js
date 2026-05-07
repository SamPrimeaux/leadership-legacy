import { expect, test } from "@playwright/test";

async function signIn(page) {
  await page.goto("/dashboard");

  const body = page.locator("body");

  // If already authenticated in this browser context, skip login.
  if (await body.getByText(/EXPLORER|Leadership Legacy operating system|AGENT CONNOR/i).count()) {
    return;
  }

  await expect(body).toContainText(/Leadership Legacy Dashboard|Protected Workspace|Sign in/i);
  await expect(body).not.toContainText("1234");

  await page.getByLabel(/email/i).fill(process.env.DASHBOARD_TEST_EMAIL || "connor@example.com");
  await page.getByLabel(/^password$/i).fill(process.env.DASHBOARD_TEST_PASSWORD || "1234");
  await page.getByRole("button", { name: /sign in/i }).click();
}

test("dashboard auth screen loads without exposing draft password", async ({ page }) => {
  await page.goto("/dashboard");

  const body = page.locator("body");

  // The draft password should never be visible as UI copy.
  await expect(body).not.toContainText("1234");

  // Either auth screen or authenticated shell is acceptable depending on session state.
  await expect(body).toContainText(/Leadership Legacy|Sign in|Protected Workspace|EXPLORER|operating system/i);
});

test("dashboard unlocks and shows command center", async ({ page }) => {
  await signIn(page);

  await expect(page.locator("body")).toContainText(/Leadership Legacy operating system|Command Center|EXPLORER/i);
});

test("agent route shows Monaco IDE shell", async ({ page }) => {
  await signIn(page);

  await page.goto("/dashboard/agent");

  await expect(page.locator("body")).toContainText(/EXPLORER|LOCAL WORKSPACE|AGENT CONNOR/i);
  await expect(page.locator("body")).toContainText(/worker|index\.js|Message Agent Connor/i);
});

test("storage route shows R2 dashboard page", async ({ page }) => {
  await signIn(page);

  await page.goto("/dashboard/storage");

  await expect(page.locator("body")).toContainText(/R2 assets and snapshots|Storage|leadership-legacy/i);
});
