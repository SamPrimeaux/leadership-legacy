#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import textwrap

ROOT = Path.cwd()

def run(cmd, check=True):
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

def patch_wrangler():
    path = ROOT / "wrangler.jsonc"
    raw = path.read_text()

    # Strip simple // comments if present before json parsing.
    cleaned = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("//"))
    data = json.loads(cleaned)

    data["name"] = "leadership-legacy"
    data["main"] = "src/worker/index.js"
    data.setdefault("compatibility_date", "2026-05-06")

    data["assets"] = {
        "directory": "./dist",
        "binding": "ASSETS",
        "run_worker_first": [
            "/dashboard",
            "/dashboard/*",
            "/api/*",
            "/services/*",
            "/work/*",
            "/resources/*",
            "/about",
            "/contact",
            "/privacy",
            "/terms"
        ]
    }

    # Add/normalize R2 binding.
    buckets = data.setdefault("r2_buckets", [])
    buckets = [b for b in buckets if b.get("binding") != "WEBSITE"]
    buckets.append({
        "binding": "WEBSITE",
        "bucket_name": "leadership-legacy"
    })
    data["r2_buckets"] = buckets

    data.setdefault("vars", {})
    data["vars"].update({
        "R2_PUBLIC_DEV_URL": "https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev",
        "R2_BUCKET_NAME": "leadership-legacy",
        "R2_S3_ENDPOINT": "https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy",
        "R2_CATALOG_URI": "https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy",
        "R2_WAREHOUSE_NAME": "ede6590ac0d2fb7daf155b35653457b2_leadership-legacy"
    })

    path.write_text(json.dumps(data, indent=2) + "\n")
    print("patched wrangler.jsonc with WEBSITE R2 binding")

def main():
    patch_wrangler()

    write("src/shared/r2/r2Registry.js", '''
    export const r2Registry = {
      bucket: "leadership-legacy",
      binding: "WEBSITE",
      publicDevelopmentUrl: "https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev",
      s3Endpoint: "https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy",
      catalogUri: "https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy",
      warehouseName: "ede6590ac0d2fb7daf155b35653457b2_leadership-legacy",
      prefixes: {
        publicAssets: "assets/",
        generatedImages: "assets/images/generated/",
        brand: "assets/brand/",
        models: "assets/models/",
        downloads: "downloads/",
        cmsPages: "cms/pages/",
        cmsSections: "cms/sections/",
        cmsThemes: "cms/themes/",
        cmsNavigation: "cms/navigation/",
        snapshots: "snapshots/",
        codeSnapshots: "snapshots/code/",
        pageSnapshots: "snapshots/pages/",
        analytics: "analytics/",
        dashboardExports: "exports/dashboard/",
        docs: "docs/",
        temp: "tmp/"
      }
    };
    ''')

    write("docs/R2_BUCKET.md", '''
    # Leadership Legacy R2 Bucket

    Bucket:

    ```txt
    leadership-legacy
    ```

    Worker binding:

    ```txt
    WEBSITE
    ```

    Static assets binding:

    ```txt
    ASSETS
    ```

    ## Important Difference

    `ASSETS` serves the built Vite `dist/` files as Worker Static Assets.

    `WEBSITE` is the R2 bucket used for CMS-managed assets, code snapshots, generated media, page snapshots, docs, exports, and dashboard-managed files.

    ## URLs

    Public development URL:

    ```txt
    https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev
    ```

    S3 API endpoint:

    ```txt
    https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy
    ```

    Catalog URI:

    ```txt
    https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy
    ```

    Warehouse name:

    ```txt
    ede6590ac0d2fb7daf155b35653457b2_leadership-legacy
    ```

    ## Recommended R2 Prefixes

    ```txt
    assets/
    assets/images/generated/
    assets/brand/
    assets/models/
    downloads/
    cms/pages/
    cms/sections/
    cms/themes/
    cms/navigation/
    snapshots/
    snapshots/code/
    snapshots/pages/
    analytics/
    exports/dashboard/
    docs/
    tmp/
    ```

    ## Production Note

    The `r2.dev` URL is useful for development but should not be the final production asset URL. For production, connect a custom domain such as:

    ```txt
    assets.leadershiplegacydigital.com
    ```

    or another domain controlled by the project.
    ''')

    write("scripts/seed-r2-structure.sh", '''
    #!/usr/bin/env bash
    set -euo pipefail

    BUCKET="leadership-legacy"

    put_text() {
      local key="$1"
      local content="$2"
      local tmp
      tmp="$(mktemp)"
      printf "%s\\n" "$content" > "$tmp"
      npx wrangler r2 object put "$BUCKET/$key" --file "$tmp" --remote
      rm -f "$tmp"
    }

    put_text "README.txt" "Leadership Legacy R2 bucket for CMS assets, snapshots, generated files, docs, exports, and analytics."
    put_text "assets/.keep" "reserved for public/CMS assets"
    put_text "assets/images/generated/.keep" "reserved for generated images"
    put_text "assets/brand/.keep" "reserved for logos, marks, and brand assets"
    put_text "assets/models/.keep" "reserved for GLB/3D model assets"
    put_text "downloads/.keep" "reserved for PDFs and downloadable files"
    put_text "cms/pages/.keep" "reserved for CMS page JSON"
    put_text "cms/sections/.keep" "reserved for CMS section JSON"
    put_text "cms/themes/.keep" "reserved for theme CSS/tokens"
    put_text "cms/navigation/.keep" "reserved for navigation snapshots"
    put_text "snapshots/.keep" "reserved for generated snapshots"
    put_text "snapshots/code/.keep" "reserved for codebase snapshots"
    put_text "snapshots/pages/.keep" "reserved for rendered page snapshots"
    put_text "analytics/.keep" "reserved for analytics exports"
    put_text "exports/dashboard/.keep" "reserved for dashboard exports"
    put_text "docs/.keep" "reserved for docs"
    put_text "tmp/.keep" "reserved for temporary generated artifacts"

    echo "R2 structure seeded into $BUCKET"
    ''')

    write("src/worker/index.js", '''
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
    ''')

    write("src/dashboard/pages/R2Storage.jsx", '''
    import { useEffect, useState } from "react";

    export function R2Storage() {
      const [status, setStatus] = useState(null);
      const [objects, setObjects] = useState([]);

      useEffect(() => {
        async function load() {
          const statusRes = await fetch("/api/r2/status");
          const statusJson = await statusRes.json();
          setStatus(statusJson);

          const listRes = await fetch("/api/r2/list?prefix=");
          const listJson = await listRes.json();
          setObjects(listJson.objects || []);
        }

        load().catch((error) => {
          setStatus({ ok: false, error: error.message });
        });
      }, []);

      return (
        <section>
          <p className="dash-eyebrow">R2 Storage</p>
          <h1>Leadership Legacy bucket</h1>
          <p className="dash-subtitle">
            R2 stores CMS assets, generated media, page snapshots, code snapshots, docs,
            analytics exports, downloads, and dashboard-managed files.
          </p>

          <div className="metric-grid">
            <article className="metric-card">
              <span>Binding</span>
              <strong>WEBSITE</strong>
              <small>Cloudflare Worker R2 binding</small>
            </article>
            <article className="metric-card">
              <span>Bucket</span>
              <strong>leadership-legacy</strong>
              <small>Western North America</small>
            </article>
            <article className="metric-card">
              <span>Status</span>
              <strong>{status?.ok ? "Online" : "Check"}</strong>
              <small>{status?.error || "R2 API reachable"}</small>
            </article>
            <article className="metric-card">
              <span>Objects</span>
              <strong>{objects.length}</strong>
              <small>First 100 listed</small>
            </article>
          </div>

          <article className="dash-panel">
            <h2>Bucket metadata</h2>
            <code>Public dev URL: {status?.publicDevelopmentUrl || "loading"}</code>
            <code>S3 endpoint: {status?.s3Endpoint || "loading"}</code>
            <code>Catalog URI: {status?.catalogUri || "loading"}</code>
            <code>Warehouse: {status?.warehouseName || "loading"}</code>
          </article>

          <div className="dash-table" role="table" style={{ marginTop: 18 }}>
            <div className="dash-table-head" role="row">
              <span>Key</span>
              <span>Size</span>
              <span>Uploaded</span>
              <span>Preview</span>
              <span>ETag</span>
            </div>
            {objects.map((object) => (
              <div className="dash-table-row" role="row" key={object.key}>
                <span>{object.key}</span>
                <span>{object.size}</span>
                <span>{object.uploaded ? new Date(object.uploaded).toLocaleString() : "—"}</span>
                <span><a href={`/api/r2/object/${encodeURIComponent(object.key)}`} target="_blank" rel="noreferrer">Open</a></span>
                <span>{object.etag?.slice(0, 16) || "—"}</span>
              </div>
            ))}
          </div>
        </section>
      );
    }
    ''')

    # Patch dashboard nav/routes to include Storage.
    nav_path = ROOT / "src/dashboard/data/dashboardNav.js"
    nav = nav_path.read_text()
    if "Database" not in nav:
      nav = nav.replace("BrainCircuit", "BrainCircuit,\n      Database")
      nav = nav.replace('from "lucide-react";', 'from "lucide-react";')
      nav = nav.replace(
          '{ label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },',
          '{ label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },\n      { label: "R2 Storage", href: "/dashboard/storage", icon: Database },'
      )
      nav_path.write_text(nav)
      print("patched dashboard nav with R2 Storage")

    app_path = ROOT / "src/dashboard/DashboardApp.jsx"
    app = app_path.read_text()
    if 'R2Storage' not in app:
      app = app.replace(
        'import { AIProviders } from "./pages/AIProviders.jsx";',
        'import { AIProviders } from "./pages/AIProviders.jsx";\n    import { R2Storage } from "./pages/R2Storage.jsx";'
      )
      app = app.replace(
        '<Route path="/dashboard/settings/ai-providers" element={<AIProviders />} />',
        '<Route path="/dashboard/settings/ai-providers" element={<AIProviders />} />\n            <Route path="/dashboard/storage" element={<R2Storage />} />'
      )
      app_path.write_text(app)
      print("patched dashboard routes with /dashboard/storage")

    write("sql/d1/003_r2_asset_registry.sql", '''
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS cms_r2_buckets (
      id TEXT PRIMARY KEY,
      binding_name TEXT NOT NULL UNIQUE,
      bucket_name TEXT NOT NULL,
      public_dev_url TEXT,
      s3_endpoint TEXT,
      catalog_uri TEXT,
      warehouse_name TEXT,
      location TEXT,
      status TEXT NOT NULL DEFAULT 'active',
      metadata_json TEXT NOT NULL DEFAULT '{}',
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS cms_r2_objects (
      id TEXT PRIMARY KEY,
      bucket_binding TEXT NOT NULL,
      object_key TEXT NOT NULL,
      object_type TEXT NOT NULL DEFAULT 'asset',
      content_type TEXT,
      size_bytes INTEGER,
      public_url TEXT,
      etag TEXT,
      usage_context TEXT,
      metadata_json TEXT NOT NULL DEFAULT '{}',
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      UNIQUE(bucket_binding, object_key)
    );

    INSERT OR IGNORE INTO cms_r2_buckets (
      id,
      binding_name,
      bucket_name,
      public_dev_url,
      s3_endpoint,
      catalog_uri,
      warehouse_name,
      location,
      metadata_json
    ) VALUES (
      'bucket_leadership_legacy',
      'WEBSITE',
      'leadership-legacy',
      'https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev',
      'https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy',
      'https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy',
      'ede6590ac0d2fb7daf155b35653457b2_leadership-legacy',
      'WNAM',
      json_object('created','2026-05-03','purpose','CMS assets, code snapshots, generated media, docs, exports, analytics')
    );
    ''')

    run(["chmod", "+x", "scripts/seed-r2-structure.sh"], check=False)
    run(["npm", "run", "build"])
    run(["git", "add", "."])
    run(["git", "commit", "-m", "feat: wire leadership legacy R2 bucket into worker and dashboard"], check=False)

    print("\\nR2 wiring complete.")
    print("Next:")
    print("./scripts/seed-r2-structure.sh")
    print("npm run deploy")
    print("curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/status")
    print("open https://leadership-legacy.meauxbility.workers.dev/dashboard/storage")

if __name__ == "__main__":
    main()
