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

async function readR2Text(env, key) {
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
        assetsBinding: "ASSETS",
        r2Binding: "WEBSITE",
        r2Bucket: env.R2_BUCKET_NAME || "leadership-legacy",
        timestamp: new Date().toISOString()
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
          bucket: env.R2_BUCKET_NAME || "leadership-legacy",
          error: error.message
        }, 500);
      }

      return json({
        ok: true,
        binding: "WEBSITE",
        bucket: env.R2_BUCKET_NAME || "leadership-legacy",
        publicDevelopmentUrl: env.R2_PUBLIC_DEV_URL,
        s3Endpoint: env.R2_S3_ENDPOINT,
        catalogUri: env.R2_CATALOG_URI,
        warehouseName: env.R2_WAREHOUSE_NAME,
        readmeExists: Boolean(readme),
        readmePreview: readme ? readme.slice(0, 240) : null
      });
    }

    if (pathname === "/api/r2/list") {
      const prefix = url.searchParams.get("prefix") || "";
      const listed = await env.WEBSITE.list({
        prefix,
        limit: 100
      });

      return json({
        ok: true,
        bucket: env.R2_BUCKET_NAME || "leadership-legacy",
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

    if (pathname.startsWith("/api/r2/object/")) {
      const key = decodeURIComponent(pathname.replace("/api/r2/object/", ""));
      const object = await env.WEBSITE.get(key);

      if (!object) {
        return json({ ok: false, error: "R2 object not found", key }, 404);
      }

      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("etag", object.httpEtag);
      headers.set("cache-control", "public, max-age=300");

      return new Response(object.body, { headers });
    }

    if (pathname.startsWith("/api/ai/providers")) {
      return json({
        providers: [
          {
            key: "openai",
            displayName: "OpenAI",
            secretName: "OPENAI_API_KEY",
            dashboardUse: ["chat", "routing", "image_generation", "evals"]
          },
          {
            key: "anthropic",
            displayName: "Anthropic",
            secretName: "ANTHROPIC_API_KEY",
            dashboardUse: ["chat", "routing", "code_review", "evals"]
          }
        ],
        note: "Provider secrets stay server-side as Cloudflare Worker secrets."
      });
    }

    // Dashboard app shell. Serve directly; do not redirect.
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
