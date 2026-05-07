import { expect, test } from "@playwright/test";

test("dashboard auth screen loads without exposing draft password", async ({ page }) => {
  await page.goto("/dashboard");

  await expect(page.locator("body")).toContainText(/Sign in|Sign up|Dashboard/i);
  await expect(page.locator("body")).not.toContainText("1234");
});

test("dashboard unlocks and shows IDE shell", async ({ page }) => {
  await page.goto("/dashboard");

  await page.getByLabel(/email/i).fill("connor@example.com");
  await page.getByLabel(/^password$/i).fill("1234");
  await page.getByRole("button", { name: /sign in/i }).click();

  await expect(page.locator("body")).toContainText(/EXPLORER|AGENT CONNOR|LOCAL WORKSPACE/i);
});
