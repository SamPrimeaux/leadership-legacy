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
