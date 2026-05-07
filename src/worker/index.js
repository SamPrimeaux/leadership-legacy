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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    if (pathname.startsWith("/api/health")) {
      return json({
        ok: true,
        app: "leadership-legacy",
        surface: "worker",
        timestamp: new Date().toISOString()
      });
    }

    if (pathname.startsWith("/api/ai/providers")) {
      return json({
        providers: [
          {
            key: "openai",
            displayName: "OpenAI",
            status: "configured_by_secret",
            secretName: "OPENAI_API_KEY",
            dashboardUse: ["chat", "routing", "image_generation", "evals"]
          },
          {
            key: "anthropic",
            displayName: "Anthropic",
            status: "configured_by_secret",
            secretName: "ANTHROPIC_API_KEY",
            dashboardUse: ["chat", "routing", "code_review", "evals"]
          }
        ],
        note: "Secrets are never exposed to the browser. This endpoint only reports provider capability metadata."
      });
    }

    // Hard fix for /dashboard redirect loops:
    // Never redirect. Always serve dashboard.html directly for /dashboard and /dashboard/*.
    if (pathname === "/dashboard" || pathname.startsWith("/dashboard/")) {
      return env.ASSETS.fetch(assetRequest(request, "/dashboard.html"));
    }

    const asset = await env.ASSETS.fetch(request);
    if (asset.status !== 404) return asset;

    // SPA fallback for public React routes.
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
