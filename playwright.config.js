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
