import { expect, test } from "@playwright/test";

const dashboardRoutes = [
  { path: "/dashboard", text: /Leadership Legacy operating system|Command Center|EXPLORER/i },
  { path: "/dashboard/agent", text: /EXPLORER|LOCAL WORKSPACE|AGENT CONNOR|Message Agent Connor/i },
  { path: "/dashboard/storage", text: /R2 assets and snapshots|Storage|leadership-legacy/i },
  { path: "/dashboard/analytics", text: /Telemetry|Analytics|page views|agent runs/i },
  { path: "/dashboard/learn", text: /Connor setup course|Learning Center|PowerShell|rubric/i },
  { path: "/dashboard/mail", text: /Gmail|Resend|Mail|lead communication/i },
  { path: "/dashboard/mcp", text: /MCP Tools|Tool registry|github\.listRepos|r2\.listObjects/i },
  { path: "/dashboard/settings", text: /Integrations and provider readiness|Settings|OpenAI|Anthropic/i }
];

for (const route of dashboardRoutes) {
  test(`dashboard route loads: ${route.path}`, async ({ page }) => {
    const response = await page.goto(route.path, { waitUntil: "domcontentloaded" });

    expect(response?.status(), `${route.path} should not return an HTTP error`).toBeLessThan(500);
    await expect(page.locator("body")).toContainText(route.text);
  });
}

test("dashboard does not expose draft password", async ({ page }) => {
  await page.goto("/dashboard", { waitUntil: "domcontentloaded" });
  await expect(page.locator("body")).not.toContainText("1234");
});
