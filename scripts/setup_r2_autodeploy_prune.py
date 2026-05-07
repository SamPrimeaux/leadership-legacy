#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap
import json

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
    print("patched package.json scripts")

def main():
    patch_package()

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

    write("scripts/prune-r2-deployments.mjs", r'''
    import { execFileSync } from "node:child_process";

    const bucket = process.env.R2_BUCKET || "leadership-legacy";
    const keep = Number(process.env.R2_KEEP_DEPLOYMENTS || 3);
    const prefix = "deployments/";

    function wrangler(args, opts = {}) {
      return execFileSync("npx", ["wrangler", ...args], {
        encoding: opts.encoding || "utf8",
        stdio: opts.stdio || ["ignore", "pipe", "pipe"]
      });
    }

    function listObjects() {
      const raw = wrangler(["r2", "object", "list", bucket, "--prefix", prefix, "--remote", "--json"]);
      return JSON.parse(raw);
    }

    function deploymentNameFromKey(key) {
      const rest = key.slice(prefix.length);
      const first = rest.split("/")[0];
      if (!first || first.startsWith("_")) return null;
      return first;
    }

    const objects = listObjects();
    const deploymentMap = new Map();

    for (const object of objects) {
      const deployment = deploymentNameFromKey(object.key);
      if (!deployment) continue;

      const current = deploymentMap.get(deployment) || {
        deployment,
        uploaded: object.uploaded || object.created || "",
        keys: []
      };

      current.keys.push(object.key);

      const objectTime = object.uploaded || object.created || "";
      if (objectTime && (!current.uploaded || objectTime > current.uploaded)) {
        current.uploaded = objectTime;
      }

      deploymentMap.set(deployment, current);
    }

    const deployments = [...deploymentMap.values()]
      .sort((a, b) => String(b.uploaded).localeCompare(String(a.uploaded)));

    const toKeep = deployments.slice(0, keep);
    const toDelete = deployments.slice(keep);

    console.log(`R2 prune bucket=${bucket} keep=${keep}`);
    console.log(`Keeping: ${toKeep.map((item) => item.deployment).join(", ") || "(none)"}`);
    console.log(`Deleting: ${toDelete.map((item) => item.deployment).join(", ") || "(none)"}`);

    for (const deployment of toDelete) {
      for (const key of deployment.keys) {
        console.log(`R2 delete r2://${bucket}/${key}`);
        execFileSync(
          "npx",
          ["wrangler", "r2", "object", "delete", `${bucket}/${key}`, "--remote"],
          { stdio: "inherit" }
        );
      }
    }

    console.log("R2 deployment prune complete.");
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
            run: npm run r2:prune

          - name: Deploy Worker
            env:
              CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
              CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
            run: npx wrangler deploy
    ''')

    write("docs/R2_AUTODEPLOY_AND_PRUNE.md", r'''
    # R2 Autodeploy and Prune

    This repo is configured so pushes to `main` can build, upload fresh app assets to R2, prune old deployments, and deploy the Worker.

    ## R2 Layout

    ```txt
    leadership-legacy/
      live/
        index.html
        dashboard.html
        assets/...
        manifest.json

      deployments/
        <git-sha>/
          index.html
          dashboard.html
          assets/...
          manifest.json

        _latest.json
    ```

    ## What Gets Uploaded

    The script uploads every file from:

    ```txt
    dist/
    ```

    to both:

    ```txt
    r2://leadership-legacy/deployments/<git-sha>/
    r2://leadership-legacy/live/
    ```

    ## Pruning

    By default, pruning keeps the latest 3 deployment snapshots:

    ```txt
    R2_KEEP_DEPLOYMENTS=3
    ```

    It deletes older objects under:

    ```txt
    deployments/<old-sha>/
    ```

    It does not delete:

    ```txt
    live/
    deployments/_latest.json
    cms/
    assets/
    docs/
    analytics/
    ```

    ## Local Commands

    Build and upload:

    ```bash
    npm run build
    npm run r2:publish
    ```

    Prune old deployment snapshots:

    ```bash
    npm run r2:prune
    ```

    Full deploy:

    ```bash
    npm run deploy:full
    ```

    ## GitHub Secrets Required

    Add these to GitHub repo secrets:

    ```txt
    CLOUDFLARE_API_TOKEN
    CLOUDFLARE_ACCOUNT_ID
    ```

    The token needs permission for:

    ```txt
    Workers Scripts: Edit
    Account R2 Storage: Edit
    Account Settings: Read
    ```

    Depending on the Cloudflare token UI, you may also need:

    ```txt
    Workers Routes: Edit
    D1: Edit
    ```

    ## Important

    `dist/` remains gitignored. Built assets live in R2 and Worker Assets, not Git.

    `node_modules/` remains gitignored.

    Source of truth remains:

    ```txt
    src/
    public/
    docs/
    scripts/
    sql/
    package.json
    wrangler config
    ```
    ''')

    run(["chmod", "+x", "scripts/setup_r2_autodeploy_prune.py"], check=False)
    run(["npm", "run", "build"], check=True)

    run([
      "git", "add",
      "package.json",
      "scripts/publish-dist-to-r2.mjs",
      "scripts/prune-r2-deployments.mjs",
      "scripts/setup_r2_autodeploy_prune.py",
      ".github/workflows/deploy.yml",
      "docs/R2_AUTODEPLOY_AND_PRUNE.md"
    ], check=False)

    run(["git", "commit", "-m", "ci: upload build assets to R2 and prune old deployments"], check=False)

    print("\nR2 autodeploy/prune setup complete.")
    print("Next:")
    print("1. Add GitHub secrets CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID")
    print("2. git push origin main")
    print("3. Watch GitHub Actions")
    print("")
    print("Local full deploy:")
    print("npm run deploy:full")

if __name__ == "__main__":
    main()
