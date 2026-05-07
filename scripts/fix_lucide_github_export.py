#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path.cwd()
TARGET = ROOT / "src/dashboard/pages/AgentIDE.jsx"

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

def main():
    src = TARGET.read_text()

    # Remove missing Github icon from lucide import.
    src = src.replace(", Github,", ",")
    src = src.replace("Github,", "")
    src = src.replace(", Github", "")

    # Replace JSX usages with GitBranch, which is already imported and valid.
    src = src.replace("<Github size={15} />", "<GitBranch size={15} />")
    src = src.replace("<Github size={44} />", "<GitBranch size={44} />")

    TARGET.write_text(src)
    print("Patched AgentIDE.jsx: replaced missing Github icon export with GitBranch.")

    run(["npm", "run", "build"], check=True)

    run(["git", "add", "src/dashboard/pages/AgentIDE.jsx", "scripts/fix_lucide_github_export.py"], check=True)
    run(["git", "commit", "-m", "fix: replace missing lucide Github icon in dashboard"], check=False)

    print("\nDone.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")

if __name__ == "__main__":
    main()
