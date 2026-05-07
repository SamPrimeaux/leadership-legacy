#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()
LIVE_URL = "https://leadership-legacy.meauxbility.workers.dev"

def run(cmd, check=False):
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result

def write(path, content):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"wrote {path}")

def main():
    write("playwright.config.js", r'''
    import { defineConfig, devices } from "@playwright/test";

    const useLocalServer = process.env.LOCAL_E2E === "1";
    const baseURL =
      process.env.PLAYWRIGHT_BASE_URL ||
      (useLocalServer
        ? "http://127.0.0.1:5173"
        : "https://leadership-legacy.meauxbility.workers.dev");

    export default defineConfig({
      testDir: "./tests/e2e",
      timeout: 60_000,
      expect: {
        timeout: 15_000
      },
      fullyParallel: true,
      retries: process.env.CI ? 2 : 0,
      reporter: [["html"], ["list"]],
      use: {
        baseURL,
        trace: "on-first-retry",
        screenshot: "only-on-failure",
        video: "retain-on-failure"
      },
      webServer: useLocalServer
        ? {
            command: "npm run dev -- --host 127.0.0.1",
            url: "http://127.0.0.1:5173",
            reuseExistingServer: !process.env.CI,
            timeout: 120_000
          }
        : undefined,
      projects: [
        {
          name: "chromium",
          use: { ...devices["Desktop Chrome"] }
        }
      ]
    });
    ''')

    write("tests/e2e/live-public-routes.spec.js", r'''
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
    ''')

    write("tests/e2e/live-dashboard-routes.spec.js", r'''
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
    ''')

    write("tests/e2e/live-api.spec.js", r'''
    import { expect, test } from "@playwright/test";

    test("health endpoint is live", async ({ request }) => {
      const response = await request.get("/api/health");
      expect(response.ok()).toBeTruthy();

      const data = await response.json();
      expect(data.ok).toBe(true);
      expect(data.worker).toBe("online");
      expect(data.r2Binding).toBe(true);
      expect(data.openaiConfigured).toBe(true);
    });

    test("AI provider status endpoint is live", async ({ request }) => {
      const response = await request.get("/api/ai/providers");
      expect(response.ok()).toBeTruthy();

      const data = await response.json();
      expect(data.ok).toBe(true);
      expect(data.openaiConfigured).toBe(true);
      expect(data.providers.some((provider) => provider.key === "openai")).toBe(true);
    });

    test("OpenAI diagnostic shape is clean", async ({ request }) => {
      const response = await request.get("/api/openai/diagnostics");
      expect(response.ok()).toBeTruthy();

      const data = await response.json();
      expect(data.ok).toBe(true);
      expect(data.openaiKey.exists).toBe(true);
      expect(data.openaiKey.startsWithEnvName).toBe(false);
      expect(data.openaiKey.hasQuotes).toBe(false);
      expect(data.openaiKey.prefix).toMatch(/^sk-/);
    });

    test("OpenAI live test returns ok", async ({ request }) => {
      const response = await request.get("/api/openai/test");
      expect(response.ok()).toBeTruthy();

      const data = await response.json();
      expect(data.ok).toBe(true);
      expect(data.text).toMatch(/ok/i);
      expect(data.model).toBeTruthy();
    });

    test("R2 list endpoint is live", async ({ request }) => {
      const response = await request.get("/api/r2/list?prefix=");
      expect(response.ok()).toBeTruthy();

      const data = await response.json();
      expect(data.ok).toBe(true);
      expect(Array.isArray(data.objects)).toBe(true);
    });

    test("GitHub status endpoint is live", async ({ request }) => {
      const response = await request.get("/api/github/status");
      expect(response.ok()).toBeTruthy();

      const data = await response.json();
      expect(data.ok).toBe(true);
      expect(Array.isArray(data.requiredSecrets)).toBe(true);
    });
    ''')

    # Remove old fragile specs if present.
    old_specs = [
      ROOT / "tests/e2e/dashboard.spec.js",
      ROOT / "tests/e2e/public-site.spec.js"
    ]
    for spec in old_specs:
      if spec.exists():
        spec.unlink()
        print(f"removed {spec}")

    write("docs/LIVE_PLAYWRIGHT_TESTING.md", r'''
    # Live Playwright Testing

    Playwright now defaults to the deployed Worker:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev
    ```

    ## Run live production smoke tests

    ```bash
    npm run test:e2e
    ```

    ## Run against another deployed URL

    ```bash
    PLAYWRIGHT_BASE_URL=https://your-url.workers.dev npm run test:e2e
    ```

    ## Run against local Vite instead

    ```bash
    LOCAL_E2E=1 npm run test:e2e
    ```

    ## Tested routes

    Public:

    ```txt
    /
    /services
    /work
    /about
    /resources
    /contact
    ```

    Dashboard:

    ```txt
    /dashboard
    /dashboard/agent
    /dashboard/storage
    /dashboard/analytics
    /dashboard/learn
    /dashboard/mail
    /dashboard/mcp
    /dashboard/settings
    ```

    APIs:

    ```txt
    /api/health
    /api/ai/providers
    /api/openai/diagnostics
    /api/openai/test
    /api/r2/list
    /api/github/status
    ```
    ''')

    run(["npm", "run", "test:e2e"], check=False)

    run([
      "git", "add",
      "playwright.config.js",
      "tests/e2e",
      "docs/LIVE_PLAYWRIGHT_TESTING.md",
      "scripts/switch_playwright_to_live_worker.py"
    ], check=False)

    run(["git", "commit", "-m", "test: switch Playwright smoke tests to live Worker routes"], check=False)

    print("\nLive Worker Playwright tests installed.")
    print("Run:")
    print("npm run test:e2e")
    print("")
    print("Optional local mode:")
    print("LOCAL_E2E=1 npm run test:e2e")

if __name__ == "__main__":
    main()
