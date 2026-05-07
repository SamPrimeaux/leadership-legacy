#!/usr/bin/env python3
from pathlib import Path
import subprocess
import json
import textwrap

ROOT = Path.cwd()

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

def patch_package():
    p = ROOT / "package.json"
    pkg = json.loads(p.read_text())

    scripts = pkg.setdefault("scripts", {})
    scripts["r2:publish"] = "node scripts/publish-dist-to-r2.mjs"
    scripts["r2:prune"] = "node scripts/prune-r2-deployments.mjs"
    scripts["deploy:full"] = "npm run build && npm run r2:publish && npm run r2:prune && wrangler deploy"

    p.write_text(json.dumps(pkg, indent=2) + "\n")
    print("patched package.json")

def patch_worker_r2_list_cursor():
    p = ROOT / "src/worker/index.js"
    if not p.exists():
        print("src/worker/index.js not found, skipping Worker cursor patch")
        return

    s = p.read_text()

    old = '''        if (pathname === "/api/r2/list") {
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
        }'''

    new = '''        if (pathname === "/api/r2/list") {
          if (!env.WEBSITE) return json({ ok: false, error: "WEBSITE R2 binding missing." }, 500);

          const prefix = url.searchParams.get("prefix") || "";
          const cursor = url.searchParams.get("cursor") || undefined;
          const limit = Math.min(Number(url.searchParams.get("limit") || 100), 1000);

          const options = {
            prefix,
            limit
          };

          if (cursor) {
            options.cursor = cursor;
          }

          const listed = await env.WEBSITE.list(options);

          return json({
            ok: true,
            prefix,
            limit,
            objects: listed.objects.map((object) => ({
              key: object.key,
              size: object.size,
              uploaded: object.uploaded,
              etag: object.etag
            })),
            truncated: listed.truncated,
            cursor: listed.cursor || null
          });
        }'''

    if old in s:
        s = s.replace(old, new)
        p.write_text(s)
        print("patched /api/r2/list cursor support")
    elif 'pathname === "/api/r2/list"' in s and "url.searchParams.get(\"cursor\")" not in s:
        print("WARNING: Found /api/r2/list but exact block differed. Cursor support not patched automatically.")
    else:
        print("Worker /api/r2/list already appears patched or missing")

def main():
    patch_package()
    patch_worker_r2_list_cursor()

    write("scripts/prune-r2-deployments.mjs", r'''
    import { execFileSync } from "node:child_process";

    const bucket = process.env.R2_BUCKET || "leadership-legacy";
    const keep = Number(process.env.R2_KEEP_DEPLOYMENTS || 3);
    const liveBaseUrl =
      process.env.LIVE_WORKER_URL ||
      process.env.PLAYWRIGHT_BASE_URL ||
      "https://leadership-legacy.meauxbility.workers.dev";

    const deploymentsPrefix = "deployments/";

    function run(cmd, args, options = {}) {
      return execFileSync(cmd, args, {
        encoding: options.encoding || "utf8",
        stdio: options.stdio || ["ignore", "pipe", "pipe"]
      });
    }

    async function fetchJson(url) {
      const response = await fetch(url);
      const text = await response.text();

      let data;
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(`Expected JSON from ${url}, got: ${text.slice(0, 500)}`);
      }

      if (!response.ok || !data.ok) {
        throw new Error(`Request failed for ${url}: ${JSON.stringify(data).slice(0, 500)}`);
      }

      return data;
    }

    async function listObjectsViaWorker(prefix) {
      const objects = [];
      let cursor = "";

      while (true) {
        const url = new URL("/api/r2/list", liveBaseUrl);
        url.searchParams.set("prefix", prefix);
        url.searchParams.set("limit", "1000");
        if (cursor) url.searchParams.set("cursor", cursor);

        const data = await fetchJson(url.toString());
        objects.push(...(data.objects || []));

        if (!data.truncated || !data.cursor) break;
        cursor = data.cursor;
      }

      return objects;
    }

    function deploymentNameFromKey(key) {
      if (!key.startsWith(deploymentsPrefix)) return null;

      const rest = key.slice(deploymentsPrefix.length);
      const first = rest.split("/")[0];

      if (!first) return null;
      if (first.startsWith("_")) return null;

      return first;
    }

    function deleteObject(key) {
      console.log(`R2 delete r2://${bucket}/${key}`);
      execFileSync(
        "npx",
        ["wrangler", "r2", "object", "delete", `${bucket}/${key}`, "--remote"],
        { stdio: "inherit" }
      );
    }

    console.log(`R2 prune using Worker API: ${liveBaseUrl}/api/r2/list`);
    console.log(`Bucket: ${bucket}`);
    console.log(`Keep latest deployments: ${keep}`);

    const objects = await listObjectsViaWorker(deploymentsPrefix);
    const deploymentMap = new Map();

    for (const object of objects) {
      const deployment = deploymentNameFromKey(object.key);
      if (!deployment) continue;

      const current = deploymentMap.get(deployment) || {
        deployment,
        uploaded: object.uploaded || "",
        keys: []
      };

      current.keys.push(object.key);

      if (object.uploaded && (!current.uploaded || object.uploaded > current.uploaded)) {
        current.uploaded = object.uploaded;
      }

      deploymentMap.set(deployment, current);
    }

    const deployments = [...deploymentMap.values()]
      .sort((a, b) => String(b.uploaded).localeCompare(String(a.uploaded)));

    const toKeep = deployments.slice(0, keep);
    const toDelete = deployments.slice(keep);

    console.log(`Found deployments: ${deployments.map((item) => item.deployment).join(", ") || "(none)"}`);
    console.log(`Keeping: ${toKeep.map((item) => item.deployment).join(", ") || "(none)"}`);
    console.log(`Deleting: ${toDelete.map((item) => item.deployment).join(", ") || "(none)"}`);

    for (const deployment of toDelete) {
      for (const key of deployment.keys) {
        deleteObject(key);
      }
    }

    console.log("R2 deployment prune complete.");
    ''')

    write("scripts/publish-dist-to-r2.mjs", r'''
    import { execFileSync } from "node:child_process";
    import { existsSync, readdirSync, statSync, writeFileSync } from "node:fs";
    import { join, relative } from "node:path";

    const bucket = process.env.R2_BUCKET || "leadership-legacy";
    const distDir = process.env.DIST_DIR || "dist";
    const sha =
      process.env.GITHUB_SHA ||
      execFileSync("git", ["rev-parse", "--short", "HEAD"], { encoding: "utf8" }).trim();

    const deploymentKey = `deployments/${sha}`;
    const liveKey = "live";
    const now = new Date().toISOString();

    if (!existsSync(distDir)) {
      console.error(`Missing ${distDir}/. Run npm run build first.`);
      process.exit(1);
    }

    function walk(dir) {
      const out = [];
      for (const name of readdirSync(dir)) {
        const full = join(dir, name);
        const stat = statSync(full);
        if (stat.isDirectory()) out.push(...walk(full));
        else out.push(full);
      }
      return out;
    }

    function putObject(localFile, key) {
      console.log(`R2 put ${localFile} -> r2://${bucket}/${key}`);
      execFileSync(
        "npx",
        ["wrangler", "r2", "object", "put", `${bucket}/${key}`, "--file", localFile, "--remote"],
        { stdio: "inherit" }
      );
    }

    const files = walk(distDir);
    const manifest = {
      app: "leadership-legacy",
      sha,
      created_at: now,
      bucket,
      deployment_prefix: deploymentKey,
      live_prefix: liveKey,
      files: files.map((file) => relative(distDir, file).replaceAll("\\", "/"))
    };

    writeFileSync(".r2-deployment-manifest.json", JSON.stringify(manifest, null, 2) + "\n");

    for (const file of files) {
      const rel = relative(distDir, file).replaceAll("\\", "/");
      putObject(file, `${deploymentKey}/${rel}`);
      putObject(file, `${liveKey}/${rel}`);
    }

    putObject(".r2-deployment-manifest.json", `${deploymentKey}/manifest.json`);
    putObject(".r2-deployment-manifest.json", `${liveKey}/manifest.json`);
    putObject(".r2-deployment-manifest.json", `deployments/_latest.json`);

    console.log(`Published dist to r2://${bucket}/${deploymentKey}/ and r2://${bucket}/${liveKey}/`);
    ''')

    write(".github/workflows/deploy.yml", r'''
    name: Deploy Leadership Legacy

    on:
      push:
        branches:
          - main
      workflow_dispatch:

    concurrency:
      group: leadership-legacy-production
      cancel-in-progress: true

    jobs:
      deploy:
        name: Build, upload R2 assets, prune, deploy Worker
        runs-on: ubuntu-latest

        permissions:
          contents: read

        env:
          R2_BUCKET: leadership-legacy
          R2_KEEP_DEPLOYMENTS: "3"
          LIVE_WORKER_URL: https://leadership-legacy.meauxbility.workers.dev

        steps:
          - name: Checkout
            uses: actions/checkout@v4

          - name: Setup Node
            uses: actions/setup-node@v4
            with:
              node-version: 22
              cache: npm

          - name: Install dependencies
            run: npm ci --include=dev

          - name: Audit
            run: npm audit

          - name: Build
            run: npm run build

          - name: Run live smoke tests
            env:
              PLAYWRIGHT_BASE_URL: https://leadership-legacy.meauxbility.workers.dev
            run: npm run test:e2e

          - name: Upload dist to R2
            env:
              CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
              CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
              R2_BUCKET: leadership-legacy
            run: npm run r2:publish

          - name: Prune old R2 deployments
            env:
              CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
              CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
              R2_BUCKET: leadership-legacy
              R2_KEEP_DEPLOYMENTS: "3"
              LIVE_WORKER_URL: https://leadership-legacy.meauxbility.workers.dev
            run: npm run r2:prune

          - name: Deploy Worker
            env:
              CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
              CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
            run: npx wrangler deploy
    ''')

    write("TO-DO.md", r'''
    # Leadership Legacy Digital Setup TO-DO

    This checklist is for Connor to finish setting up, learning, testing, and operating the Leadership Legacy Digital platform.

    ## Current Live URLs

    Public:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/
    https://leadership-legacy.meauxbility.workers.dev/services
    https://leadership-legacy.meauxbility.workers.dev/work
    https://leadership-legacy.meauxbility.workers.dev/about
    https://leadership-legacy.meauxbility.workers.dev/resources
    https://leadership-legacy.meauxbility.workers.dev/contact
    ```

    Dashboard:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/dashboard
    https://leadership-legacy.meauxbility.workers.dev/dashboard/agent
    https://leadership-legacy.meauxbility.workers.dev/dashboard/storage
    https://leadership-legacy.meauxbility.workers.dev/dashboard/settings
    https://leadership-legacy.meauxbility.workers.dev/dashboard/analytics
    https://leadership-legacy.meauxbility.workers.dev/dashboard/learn
    https://leadership-legacy.meauxbility.workers.dev/dashboard/mail
    https://leadership-legacy.meauxbility.workers.dev/dashboard/mcp
    ```

    API:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/health
    https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
    https://leadership-legacy.meauxbility.workers.dev/api/openai/diagnostics
    https://leadership-legacy.meauxbility.workers.dev/api/openai/test
    https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=
    https://leadership-legacy.meauxbility.workers.dev/api/github/status
    ```

    ## 1. Repo Setup

    - [ ] Clone the repo.
    - [ ] Open the repo in Cursor or VS Code.
    - [ ] Confirm Node 22+ is installed.
    - [ ] Install dependencies:

    ```bash
    npm install --include=dev
    ```

    - [ ] Confirm the repo is clean:

    ```bash
    git status --short
    ```

    Connor should understand:

    ```txt
    src/ = source code
    dist/ = generated build output, not committed
    node_modules/ = installed packages, not committed
    docs/ = setup guides and operating docs
    scripts/ = automation helpers
    tests/e2e/ = Playwright tests
    .github/workflows/ = GitHub Actions automation
    ```

    ## 2. Local Development

    Run local dev:

    ```bash
    npm run dev
    ```

    Build locally:

    ```bash
    npm run build
    ```

    Run live Playwright tests:

    ```bash
    npm run test:e2e
    ```

    Run local Playwright tests:

    ```bash
    LOCAL_E2E=1 npm run test:e2e
    ```

    Completion:

    - [ ] Connor can run the app locally.
    - [ ] Connor can run a production build.
    - [ ] Connor can run Playwright.
    - [ ] Connor understands local Vite vs deployed Worker.

    ## 3. Cloudflare Setup

    Required resources:

    - [ ] Worker: `leadership-legacy`
    - [ ] R2 bucket: `leadership-legacy`
    - [ ] Worker Assets binding: `ASSETS`
    - [ ] R2 binding: `WEBSITE -> leadership-legacy`
    - [ ] D1 database for CMS runtime.
    - [ ] KV namespace for OAuth state/session/cache.
    - [ ] Durable Object namespace for future realtime sessions.
    - [ ] Workers AI binding if using Cloudflare AI utilities.

    Verify:

    ```bash
    npx wrangler whoami
    npx wrangler r2 bucket list
    npx wrangler d1 list
    npm run deploy
    ```

    Health checks:

    ```bash
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/health
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=
    ```

    ## 4. OpenAI Setup

    Sam temporarily installed an OpenAI key. Connor should replace it later.

    Add or replace:

    ```bash
    npx wrangler secret put OPENAI_API_KEY
    ```

    Paste only:

    ```txt
    sk-proj-...
    ```

    Do not paste:

    ```txt
    OPENAI_API_KEY=sk-proj-...
    ```

    Verify:

    ```bash
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/diagnostics
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/test
    ```

    Expected:

    ```txt
    startsWithEnvName: false
    hasQuotes: false
    /api/openai/test returns ok
    ```

    ## 5. Anthropic Setup

    Add:

    ```bash
    npx wrangler secret put ANTHROPIC_API_KEY
    npm run deploy
    ```

    Use Anthropic for:

    ```txt
    architecture review
    code review
    second-opinion reasoning
    safety critique
    rubric evaluation
    ```

    ## 6. Gemini Setup

    Add:

    ```bash
    npx wrangler secret put GEMINI_API_KEY
    npm run deploy
    ```

    Use Gemini for:

    ```txt
    long-context comparison
    Google ecosystem workflows
    multimodal experiments
    provider benchmark testing
    ```

    ## 7. R2 Asset Deploy + Pruning

    R2 layout:

    ```txt
    leadership-legacy/
      live/
        index.html
        dashboard.html
        assets/
        manifest.json

      deployments/
        <git-sha>/
          index.html
          dashboard.html
          assets/
          manifest.json

        _latest.json
    ```

    Local commands:

    ```bash
    npm run build
    npm run r2:publish
    npm run r2:prune
    npm run deploy:full
    ```

    `npm run deploy:full` does:

    ```txt
    build
    upload dist to R2 deployments/<sha>/
    upload dist to R2 live/
    prune old deployments
    deploy Worker
    ```

    Pruning keeps latest 3 deployment snapshots by default:

    ```txt
    R2_KEEP_DEPLOYMENTS=3
    ```

    The prune script deletes only:

    ```txt
    deployments/<old-sha>/
    ```

    It does not delete:

    ```txt
    live/
    cms/
    assets/
    docs/
    analytics/
    ```

    ## 8. GitHub Actions Autodeploy

    Add GitHub repo secrets:

    ```txt
    CLOUDFLARE_ACCOUNT_ID
    CLOUDFLARE_API_TOKEN
    ```

    Cloudflare token permissions:

    ```txt
    Workers Scripts: Edit
    Account R2 Storage: Edit
    Account Settings: Read
    ```

    Optional if required:

    ```txt
    Workers Routes: Edit
    D1: Edit
    ```

    On push to `main`, GitHub Actions should:

    ```txt
    install dependencies
    audit
    build
    run live Playwright tests
    upload dist to R2
    prune old R2 deployments
    deploy Worker
    ```

    ## 9. Dashboard Routes

    Verify:

    ```txt
    /dashboard          command center
    /dashboard/agent    Monaco + Agent Connor IDE
    /dashboard/storage  R2 browser page
    /dashboard/settings integration/provider readiness
    /dashboard/analytics telemetry overview
    /dashboard/learn    Connor setup course
    /dashboard/mail     Gmail/Resend workflow planning
    /dashboard/mcp      MCP/tool registry planning
    ```

    ## 10. Agent Connor Modes

    Agent Connor should not rewrite code by default.

    Modes:

    ```txt
    Chat
    Code
    Auto
    ```

    Chat:

    ```txt
    default mode
    calls POST /api/openai/chat
    use for questions, learning, planning, debugging
    ```

    Code:

    ```txt
    intentionally edits the active Monaco file
    calls POST /api/openai/code
    ```

    Auto:

    ```txt
    chooses Code only for clear edit/refactor/patch prompts
    ```

    ## 11. GitHub Integration

    Choose OAuth App or GitHub App.

    OAuth callback:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/github/callback
    ```

    OAuth secrets:

    ```bash
    npx wrangler secret put GITHUB_CLIENT_ID
    npx wrangler secret put GITHUB_CLIENT_SECRET
    npm run deploy
    ```

    GitHub App secrets:

    ```bash
    npx wrangler secret put GITHUB_APP_ID
    npx wrangler secret put GITHUB_APP_PRIVATE_KEY
    npx wrangler secret put GITHUB_WEBHOOK_SECRET
    npm run deploy
    ```

    Planned features:

    ```txt
    list repos
    browse repo tree
    open file into Monaco
    ask Agent to edit
    preview diff
    save to branch
    open pull request
    run Playwright
    deploy after approval
    ```

    ## 12. Google Drive + Gmail

    Google callback:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/google/callback
    ```

    Secrets:

    ```bash
    npx wrangler secret put GOOGLE_CLIENT_ID
    npx wrangler secret put GOOGLE_CLIENT_SECRET
    npx wrangler secret put GOOGLE_REDIRECT_URI
    npm run deploy
    ```

    Recommended scopes:

    ```txt
    openid
    email
    profile
    https://www.googleapis.com/auth/drive.metadata.readonly
    https://www.googleapis.com/auth/drive.readonly
    https://www.googleapis.com/auth/gmail.readonly
    https://www.googleapis.com/auth/gmail.compose
    ```

    Planned Drive:

    ```txt
    browse Drive files
    import docs/PDFs
    store snapshots in R2
    chunk documents
    embed to Supabase
    power RAG answers
    ```

    Planned Gmail:

    ```txt
    read relevant threads
    summarize thread
    draft reply
    user approves
    send or save draft
    log CRM note
    ```

    ## 13. Resend Email

    Add:

    ```bash
    npx wrangler secret put RESEND_API_KEY
    npm run deploy
    ```

    Uses:

    ```txt
    contact form notification
    lead confirmation
    admin invite
    password reset or magic link later
    publish/deploy notifications
    ```

    ## 14. Supabase Setup

    Supabase should handle:

    ```txt
    analytics
    RAG documents
    pgvector embeddings
    eval runs
    model routing logs
    codebase chunks
    tool execution logs
    long-term telemetry
    ```

    Secrets:

    ```bash
    npx wrangler secret put SUPABASE_URL
    npx wrangler secret put SUPABASE_SERVICE_ROLE_KEY
    npm run deploy
    ```

    Service role key must stay server-side only.

    ## 15. D1 CMS Runtime

    D1 should hold fast runtime CMS data:

    ```txt
    pages
    sections
    navigation
    themes
    asset metadata
    leads
    provider config
    publishing status
    ```

    Commands:

    ```bash
    npx wrangler d1 list
    npx wrangler d1 execute <DB_NAME> --remote --file sql/d1/<file>.sql
    ```

    ## 16. KV + Durable Objects

    KV uses:

    ```txt
    OAuth state
    short-lived sessions
    rate limits
    temporary flags
    cache entries
    ```

    Durable Object uses:

    ```txt
    realtime CMS editing
    agent sessions
    terminal sessions
    collaboration
    live preview bridge
    ```

    ## 17. MCP Tool Registry

    First tools:

    ```txt
    github.listRepos
    github.getFile
    github.commitFile
    r2.listObjects
    r2.getObject
    r2.putObject
    d1.query
    openai.chat
    openai.codeAction
    anthropic.review
    gmail.createDraft
    drive.importFile
    resend.sendEmail
    playwright.runSmoke
    ```

    Approval required for:

    ```txt
    send email
    delete file
    write to main branch
    deploy production
    change DNS
    rotate secrets
    execute terminal command
    delete R2 object
    delete database row
    ```

    ## 18. Playwright Live Testing

    Tests default to:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev
    ```

    Run:

    ```bash
    npm run test:e2e
    ```

    Local mode:

    ```bash
    LOCAL_E2E=1 npm run test:e2e
    ```

    ## 19. Security Rules

    Never commit:

    ```txt
    .env
    API keys
    private keys
    OAuth secrets
    service role keys
    refresh tokens
    passwords
    ```

    Browser must never see:

    ```txt
    OPENAI_API_KEY
    ANTHROPIC_API_KEY
    GEMINI_API_KEY
    SUPABASE_SERVICE_ROLE_KEY
    GITHUB_CLIENT_SECRET
    GOOGLE_CLIENT_SECRET
    RESEND_API_KEY
    AWS_SECRET_ACCESS_KEY
    ```

    ## 20. Production Handoff Rubric

    Scoring:

    ```txt
    0 = Not present
    1 = Started but not usable
    2 = Partially usable with manual work
    3 = Usable for internal testing
    4 = Production-ready with guardrails
    5 = Production-ready, monitored, documented, and tested
    ```

    Targets:

    | Area | Target | Current | Pass |
    |---|---:|---:|---|
    | Repo setup | 4 |  | [ ] |
    | Cloudflare deploy | 4 |  | [ ] |
    | R2 storage | 4 |  | [ ] |
    | OpenAI | 4 |  | [ ] |
    | Anthropic | 3 |  | [ ] |
    | Gemini | 3 |  | [ ] |
    | GitHub integration | 4 |  | [ ] |
    | Google Drive/Gmail | 4 |  | [ ] |
    | Resend | 4 |  | [ ] |
    | Supabase | 4 |  | [ ] |
    | D1 CMS | 4 |  | [ ] |
    | MCP tools | 4 |  | [ ] |
    | Playwright | 4 |  | [ ] |
    | Security/secrets | 5 |  | [ ] |
    | Connor readiness | 4 |  | [ ] |

    Production ready only if:

    - [ ] No category below target.
    - [ ] No exposed secrets.
    - [ ] Build passes.
    - [ ] Live Playwright tests pass.
    - [ ] Worker deploys.
    - [ ] OpenAI test passes.
    - [ ] R2 list works.
    - [ ] GitHub Actions deploy works.
    - [ ] R2 pruning works.
    - [ ] Destructive tools require approval.

    ## 21. Daily Workflow

    Connor’s normal workflow:

    ```bash
    git pull origin main
    npm install --include=dev
    npm run build
    npm run test:e2e
    npm run deploy
    git status --short
    ```

    Ship workflow:

    ```bash
    git add .
    git commit -m "describe the change"
    git push origin main
    ```
    ''')

    write("docs/R2_AUTODEPLOY_AND_PRUNE.md", r'''
    # R2 Autodeploy and Prune

    The previous prune implementation attempted to call:

    ```bash
    npx wrangler r2 object list leadership-legacy --prefix deployments/ --remote --json
    ```

    Wrangler v4.88.0 does not support that `object list` command shape.

    The fixed prune flow now uses the deployed Worker API:

    ```txt
    GET /api/r2/list?prefix=deployments/
    ```

    Then it deletes old deployment objects using the supported command:

    ```bash
    npx wrangler r2 object delete leadership-legacy/<key> --remote
    ```

    ## R2 Layout

    ```txt
    leadership-legacy/
      live/
        index.html
        dashboard.html
        assets/
        manifest.json

      deployments/
        <git-sha>/
          index.html
          dashboard.html
          assets/
          manifest.json

        _latest.json
    ```

    ## Commands

    Publish fresh build:

    ```bash
    npm run build
    npm run r2:publish
    ```

    Prune old deployment snapshots:

    ```bash
    npm run r2:prune
    ```

    Full local deployment:

    ```bash
    npm run deploy:full
    ```

    ## Safety

    Pruning deletes only old objects under:

    ```txt
    deployments/<old-sha>/
    ```

    It does not delete:

    ```txt
    live/
    cms/
    assets/
    docs/
    analytics/
    ```
    ''')

    run(["npm", "run", "build"], check=True)

    run([
        "git", "add",
        "package.json",
        "src/worker/index.js",
        "scripts/publish-dist-to-r2.mjs",
        "scripts/prune-r2-deployments.mjs",
        "scripts/fix_r2_prune_and_write_connor_todo.py",
        ".github/workflows/deploy.yml",
        "docs/R2_AUTODEPLOY_AND_PRUNE.md",
        "TO-DO.md"
    ], check=False)

    run(["git", "commit", "-m", "fix: prune R2 deployments via Worker API and add Connor setup todo"], check=False)

    print("\nDone.")
    print("Next run:")
    print("npm run deploy")
    print("npm run r2:prune")
    print("git push origin main")

if __name__ == "__main__":
    main()
