import { expect, test } from "@playwright/test";

test("public homepage loads", async ({ page }) => {
  await page.goto("/");

  await expect(page.locator("body")).toContainText(/Connor|Leadership Legacy|engineering-grade|AI systems/i);
});

test("public services route loads", async ({ page }) => {
  await page.goto("/services/rag-systems");

  await expect(page.locator("body")).toContainText(/RAG|Leadership Legacy|AI|systems|engineering/i);
});
