#!/usr/bin/env python3
from pathlib import Path
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

def main():
    # 1. Ensure gitignore is correct.
    write(".gitignore", """
    # dependencies
    node_modules/

    # builds
    dist/
    .playwright/
    playwright-report/
    test-results/

    # env / secrets
    .env
    .env.*
    !.env.example

    # OS/editor
    .DS_Store
    .vscode/*
    !.vscode/extensions.json
    .idea/
    """)

    # 2. Remove generated/dependency folders from git tracking only.
    run(["git", "rm", "-r", "--cached", "node_modules"], check=False)
    run(["git", "rm", "-r", "--cached", "dist"], check=False)

    # 3. Make sure package scripts use local Playwright, not npx.
    pkg = ROOT / "package.json"
    if pkg.exists():
        text = pkg.read_text()
        text = text.replace('"test:e2e": "npx playwright test"', '"test:e2e": "playwright test"')
        text = text.replace('"test:e2e:ui": "npx playwright test --ui"', '"test:e2e:ui": "playwright test --ui"')
        text = text.replace('"test:e2e:headed": "npx playwright test --headed"', '"test:e2e:headed": "playwright test --headed"')
        text = text.replace('"test:e2e:report": "npx playwright show-report"', '"test:e2e:report": "playwright show-report"')
        pkg.write_text(text)

    # 4. Fresh install/build/test.
    run(["npm", "install", "--include=dev"])
    run(["npm", "audit"])
    run(["npm", "run", "build"])
    run(["npm", "run", "test:e2e"], check=False)

    # 5. Upload built app snapshot to R2.
    write("scripts/upload-dist-to-r2.sh", """
    #!/usr/bin/env bash
    set -euo pipefail

    BUCKET="leadership-legacy"
    PREFIX="snapshots/dist/latest"

    if [[ ! -d dist ]]; then
      echo "dist/ does not exist. Run npm run build first."
      exit 1
    fi

    find dist -type f | while read -r file; do
      key="$PREFIX/${file#dist/}"
      echo "Uploading $file -> r2://$BUCKET/$key"
      npx wrangler r2 object put "$BUCKET/$key" --file "$file" --remote
    done

    echo "Uploaded dist snapshot to r2://$BUCKET/$PREFIX/"
    """)

    run(["chmod", "+x", "scripts/upload-dist-to-r2.sh"])
    run(["./scripts/upload-dist-to-r2.sh"], check=False)

    # 6. Deploy Worker/static assets.
    run(["npm", "run", "deploy"])

    # 7. Stage only source/config/docs/scripts/tests/package files, not node_modules/dist.
    run([
        "git", "add",
        ".gitignore",
        "package.json",
        "package-lock.json",
        "playwright.config.js",
        "tests",
        "docs",
        "scripts",
        "src",
        "README.md",
        "wrangler.jsonc",
        "vite.config.js",
        "index.html",
        "dashboard.html",
        "sql"
    ], check=False)

    run(["git", "status", "--short"], check=False)

    # 8. Commit and push.
    run(["git", "commit", "-m", "feat: finalize clean IDE dashboard build and deployment workflow"], check=False)
    run(["git", "push", "origin", "main"], check=False)

    print("\\nDone.")
    print("Verify:")
    print("curl -s https://leadership-legacy.meauxbility.workers.dev/api/health")
    print("open https://leadership-legacy.meauxbility.workers.dev/dashboard")

if __name__ == "__main__":
    main()
