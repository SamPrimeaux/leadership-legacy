import { expect, test } from "@playwright/test";

test("public homepage loads", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("body")).toContainText(/Leadership Legacy|engineering-grade/i);
});

test("public services route loads", async ({ page }) => {
  await page.goto("/services/rag-systems");
  await expect(page.locator("body")).toContainText(/Leadership Legacy|Service|RAG/i);
});
