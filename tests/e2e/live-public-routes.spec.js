import { expect, test } from "@playwright/test";

const publicRoutes = [
  { path: "/", text: /Leadership Legacy|Connor|AI systems|engineering/i },
  { path: "/services", text: /Services|AI Engineering|RAG|automation|Leadership Legacy/i },
  { path: "/work", text: /Work|case studies|MechAssist|OpenClaw|Leadership Legacy/i },
  { path: "/about", text: /Connor|Mechanical Engineer|AI Developer|Leadership Legacy/i },
  { path: "/resources", text: /Resources|playbook|checklist|automation|Leadership Legacy/i },
  { path: "/contact", text: /Contact|project|intake|Leadership Legacy/i }
];

for (const route of publicRoutes) {
  test(`public route loads: ${route.path}`, async ({ page }) => {
    const response = await page.goto(route.path, { waitUntil: "domcontentloaded" });

    expect(response?.status(), `${route.path} should not return an HTTP error`).toBeLessThan(500);
    await expect(page.locator("body")).toContainText(route.text);
  });
}
