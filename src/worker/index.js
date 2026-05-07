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

function cleanOpenAIKey(value) {
  if (!value) return "";
  let key = String(value).trim();

  if (key.startsWith("OPENAI_API_KEY=")) {
    key = key.replace(/^OPENAI_API_KEY=/, "").trim();
  }

  key = key.replace(/^["']|["']$/g, "").trim();
  return key;
}

function keyShape(value) {
  const raw = String(value || "");
  const cleaned = cleanOpenAIKey(raw);
  return {
    exists: Boolean(raw),
    rawLength: raw.length,
    cleanedLength: cleaned.length,
    startsWithEnvName: raw.trim().startsWith("OPENAI_API_KEY="),
    hasQuotes: /^["']|["']$/.test(raw.trim()),
    prefix: cleaned.slice(0, 7),
    suffix: cleaned.slice(-4)
  };
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

function isLikelyTextKey(key) {
  return /\.(txt|md|json|jsonc|js|jsx|ts|tsx|css|html|svg|xml|yml|yaml|sql|csv|toml|env|log)$/i.test(key);
}

async function callOpenAI(env, payload) {
  const apiKey = cleanOpenAIKey(env.OPENAI_API_KEY);

  if (!apiKey) {
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
      authorization: `Bearer ${apiKey}`
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
        openaiConfigured: Boolean(cleanOpenAIKey(env.OPENAI_API_KEY)),
        r2Binding: Boolean(env.WEBSITE),
        timestamp: new Date().toISOString()
      });
    }

    if (pathname === "/api/openai/diagnostics") {
      return json({
        ok: true,
        openaiKey: keyShape(env.OPENAI_API_KEY),
        defaultModel: env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini",
        note: "This endpoint intentionally exposes only key shape, never the full key."
      });
    }

    if (pathname === "/api/openai/test") {
      const model = url.searchParams.get("model") || env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini";
      const result = await callOpenAI(env, {
        model,
        instructions: "Reply with exactly: ok",
        input: "health check",
        max_output_tokens: 20
      });

      if (!result.ok) {
        return json(result, result.status || 500);
      }

      return json({
        ok: true,
        model,
        text: result.text,
        responseId: result.data?.id || null,
        usage: result.data?.usage || null
      });
    }

    if (pathname === "/api/ai/providers") {
      return json({
        ok: true,
        openaiConfigured: Boolean(cleanOpenAIKey(env.OPENAI_API_KEY)),
        providers: [
          {
            key: "openai",
            displayName: "OpenAI",
            secretName: "OPENAI_API_KEY",
            status: cleanOpenAIKey(env.OPENAI_API_KEY) ? "configured" : "missing_secret",
            models: ["gpt-5.4-mini", "gpt-5.4-nano", "gpt-5.4"]
          },
          {
            key: "anthropic",
            displayName: "Anthropic",
            secretName: "ANTHROPIC_API_KEY",
            status: env.ANTHROPIC_API_KEY ? "configured" : "missing_secret",
            models: ["claude-sonnet", "claude-haiku"]
          },
          {
            key: "gemini",
            displayName: "Gemini",
            secretName: "GEMINI_API_KEY",
            status: env.GEMINI_API_KEY ? "configured" : "missing_secret",
            models: ["gemini-pro", "gemini-flash"]
          }
        ],
        blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
      });
    }

    if (pathname === "/api/github/status") {
      return json({
        ok: true,
        configured: Boolean(env.GITHUB_CLIENT_ID || env.GITHUB_APP_ID),
        oauthConfigured: Boolean(env.GITHUB_CLIENT_ID && env.GITHUB_CLIENT_SECRET),
        appConfigured: Boolean(env.GITHUB_APP_ID && env.GITHUB_APP_PRIVATE_KEY),
        requiredSecrets: [
          "GITHUB_CLIENT_ID",
          "GITHUB_CLIENT_SECRET",
          "GITHUB_APP_ID",
          "GITHUB_APP_PRIVATE_KEY",
          "GITHUB_WEBHOOK_SECRET"
        ]
      });
    }

    if (pathname === "/api/oauth/github/start") {
      if (!env.GITHUB_CLIENT_ID) {
        return json({
          ok: false,
          error: "GitHub OAuth is not configured yet.",
          requiredSecret: "GITHUB_CLIENT_ID"
        }, 501);
      }

      const redirect = new URL("https://github.com/login/oauth/authorize");
      redirect.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
      redirect.searchParams.set("redirect_uri", `${url.origin}/api/oauth/github/callback`);
      redirect.searchParams.set("scope", "repo read:user user:email");
      redirect.searchParams.set("state", crypto.randomUUID());
      return Response.redirect(redirect.toString(), 302);
    }

    if (pathname === "/api/oauth/google/start") {
      if (!env.GOOGLE_CLIENT_ID) {
        return json({
          ok: false,
          error: "Google OAuth is not configured yet.",
          requiredSecret: "GOOGLE_CLIENT_ID"
        }, 501);
      }

      const redirect = new URL("https://accounts.google.com/o/oauth2/v2/auth");
      redirect.searchParams.set("client_id", env.GOOGLE_CLIENT_ID);
      redirect.searchParams.set("redirect_uri", env.GOOGLE_REDIRECT_URI || `${url.origin}/api/oauth/google/callback`);
      redirect.searchParams.set("response_type", "code");
      redirect.searchParams.set("scope", [
        "openid",
        "email",
        "profile",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.compose"
      ].join(" "));
      redirect.searchParams.set("access_type", "offline");
      redirect.searchParams.set("prompt", "consent");
      redirect.searchParams.set("state", crypto.randomUUID());
      return Response.redirect(redirect.toString(), 302);
    }

    if (pathname === "/api/openai/code" && request.method === "POST") {
      const body = await readJson(request);
      const model = body.model || env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini";
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
        return json({ ok: false, binding: "WEBSITE", error: error.message }, 500);
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
        })),
        truncated: listed.truncated,
        cursor: listed.cursor || null
      });
    }

    if (pathname === "/api/r2/text") {
      if (!env.WEBSITE) return json({ ok: false, error: "WEBSITE R2 binding missing." }, 500);
      const key = url.searchParams.get("key") || "";
      if (!key) return json({ ok: false, error: "Missing key." }, 400);
      if (!isLikelyTextKey(key)) {
        return json({ ok: false, error: "This object does not look like a text/code file.", key }, 415);
      }

      const object = await env.WEBSITE.get(key);
      if (!object) return json({ ok: false, error: "Object not found.", key }, 404);

      const text = await object.text();
      return json({
        ok: true,
        key,
        size: object.size,
        uploaded: object.uploaded,
        httpEtag: object.httpEtag,
        text
      });
    }

    if (pathname.startsWith("/api/r2/object/")) {
      if (!env.WEBSITE) return json({ ok: false, error: "WEBSITE R2 binding missing." }, 500);
      const key = decodeURIComponent(pathname.replace("/api/r2/object/", ""));
      const object = await env.WEBSITE.get(key);
      if (!object) return json({ ok: false, error: "R2 object not found", key }, 404);
      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("etag", object.httpEtag);
      headers.set("cache-control", "public, max-age=300");
      return new Response(object.body, { headers });
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
