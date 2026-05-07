function assetRequest(request, assetPath) {
  const url = new URL(request.url);
  url.pathname = assetPath;
  url.search = "";
  return new Request(url.toString(), {
    method: "GET",
    headers: request.headers
  });
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
  });
}

async function readJson(request) {
  try {
    return await request.json();
  } catch {
    return {};
  }
}

function extractResponseText(data) {
  if (typeof data.output_text === "string" && data.output_text.trim()) {
    return data.output_text;
  }

  const chunks = [];

  for (const item of data.output || []) {
    for (const content of item.content || []) {
      if (content.type === "output_text" && content.text) chunks.push(content.text);
      if (content.type === "text" && content.text) chunks.push(content.text);
    }
  }

  return chunks.join("\n").trim();
}

function stripCodeFence(text) {
  if (!text) return "";
  return text
    .replace(/^```[a-zA-Z0-9_-]*\s*/, "")
    .replace(/```\s*$/, "")
    .trim();
}

async function callOpenAI(env, payload) {
  if (!env.OPENAI_API_KEY) {
    return {
      ok: false,
      status: 500,
      error: "OPENAI_API_KEY is not configured on this Worker."
    };
  }

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${env.OPENAI_API_KEY}`
    },
    body: JSON.stringify(payload)
  });

  const raw = await response.text();
  let data;

  try {
    data = JSON.parse(raw);
  } catch {
    data = { raw };
  }

  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: data?.error?.message || "OpenAI request failed.",
      details: data
    };
  }

  return {
    ok: true,
    status: response.status,
    data,
    text: extractResponseText(data)
  };
}

async function readR2Text(env, key) {
  if (!env.WEBSITE) return null;
  const object = await env.WEBSITE.get(key);
  if (!object) return null;
  return object.text();
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    if (pathname === "/api/health") {
      return json({
        ok: true,
        app: "leadership-legacy",
        worker: "online",
        openaiConfigured: Boolean(env.OPENAI_API_KEY),
        r2Binding: Boolean(env.WEBSITE),
        timestamp: new Date().toISOString()
      });
    }

    if (pathname === "/api/ai/providers") {
      return json({
        ok: true,
        openaiConfigured: Boolean(env.OPENAI_API_KEY),
        providers: [
          {
            key: "openai",
            displayName: "OpenAI",
            secretName: "OPENAI_API_KEY",
            status: env.OPENAI_API_KEY ? "configured" : "missing_secret",
            models: ["gpt-5.4-mini", "gpt-5.4-nano", "gpt-5.4"]
          },
          {
            key: "anthropic",
            displayName: "Anthropic",
            secretName: "ANTHROPIC_API_KEY",
            status: env.ANTHROPIC_API_KEY ? "configured" : "missing_secret",
            models: ["claude-sonnet", "claude-haiku"]
          }
        ],
        blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
      });
    }

    if (pathname === "/api/openai/code" && request.method === "POST") {
      const body = await readJson(request);
      const model = body.model || "gpt-5.4-mini";
      const filename = body.filename || "routes/services.jsx";
      const language = body.language || "javascript";
      const code = body.code || "";
      const instruction = body.instruction || "Improve this file.";

      if (["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"].includes(model)) {
        return json({
          ok: false,
          error: "This model is blocked by project policy."
        }, 400);
      }

      const result = await callOpenAI(env, {
        model,
        instructions: [
          "You are Agent Connor inside the Leadership Legacy IDE dashboard.",
          "Return only final complete file contents.",
          "Do not include markdown fences.",
          "Do not expose secrets.",
          "Prefer production-ready React/Vite/Cloudflare/CMS patterns.",
          "Keep UI tight, practical, and IDE-like."
        ].join("\n"),
        input: [
          `Filename: ${filename}`,
          `Language: ${language}`,
          "",
          "Instruction:",
          instruction,
          "",
          "Current file:",
          code || "(empty)"
        ].join("\n"),
        max_output_tokens: 6000
      });

      if (!result.ok) {
        return json(result, result.status || 500);
      }

      return json({
        ok: true,
        model,
        filename,
        language,
        code: stripCodeFence(result.text),
        responseId: result.data?.id || null,
        usage: result.data?.usage || null
      });
    }

    if (pathname === "/api/r2/status") {
      let readme = null;
      try {
        readme = await readR2Text(env, "README.txt");
      } catch (error) {
        return json({
          ok: false,
          binding: "WEBSITE",
          error: error.message
        }, 500);
      }

      return json({
        ok: true,
        binding: "WEBSITE",
        bucket: env.R2_BUCKET_NAME || "leadership-legacy",
        publicDevelopmentUrl: env.R2_PUBLIC_DEV_URL,
        readmeExists: Boolean(readme),
        readmePreview: readme ? readme.slice(0, 240) : null
      });
    }

    if (pathname === "/api/r2/list") {
      if (!env.WEBSITE) return json({ ok: false, error: "WEBSITE R2 binding missing." }, 500);
      const prefix = url.searchParams.get("prefix") || "";
      const listed = await env.WEBSITE.list({ prefix, limit: 100 });
      return json({
        ok: true,
        prefix,
        objects: listed.objects.map((object) => ({
          key: object.key,
          size: object.size,
          uploaded: object.uploaded,
          etag: object.etag
        }))
      });
    }

    if (pathname === "/dashboard" || pathname.startsWith("/dashboard/")) {
      return env.ASSETS.fetch(assetRequest(request, "/dashboard.html"));
    }

    const asset = await env.ASSETS.fetch(request);
    if (asset.status !== 404) return asset;

    if (
      request.method === "GET" &&
      (request.headers.get("accept") || "").includes("text/html") &&
      !pathname.includes(".")
    ) {
      return env.ASSETS.fetch(assetRequest(request, "/index.html"));
    }

    return asset;
  }
};
