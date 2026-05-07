#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
from datetime import datetime

ROOT = Path.cwd()
SCRIPTS = ROOT / "scripts"

# Scripts that should stay in root for the duration of this run.
SELF = Path(__file__).name

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
    SCRIPTS.mkdir(parents=True, exist_ok=True)

    root_py_files = sorted([
        path for path in ROOT.glob("*.py")
        if path.name != SELF
    ])

    moved = []

    for src in root_py_files:
        dst = SCRIPTS / src.name

        if dst.exists():
            backup = SCRIPTS / f"{src.stem}.backup-{datetime.now().strftime('%Y%m%d%H%M%S')}.py"
            print(f"existing script found, backing up: {dst.name} -> {backup.name}")
            shutil.copy2(dst, backup)

        shutil.move(str(src), str(dst))
        dst.chmod(0o755)
        moved.append(dst.name)
        print(f"moved {src.name} -> scripts/{dst.name}")

    # Also move this collector script itself into scripts after it finishes writing index.
    index_path = SCRIPTS / "PYTHON_SCRIPTS_INDEX.md"

    script_names = sorted([path.name for path in SCRIPTS.glob("*.py")])

    index = [
        "# Python Scripts Index",
        "",
        "This folder contains repo bootstrap, dashboard, CMS, R2, SQL, and deployment helper scripts used during the Leadership Legacy build.",
        "",
        "## Scripts",
        ""
    ]

    for name in script_names:
        index.append(f"- `{name}`")

    index.append("")
    index.append("## Usage")
    index.append("")
    index.append("Run scripts from the repo root unless a script says otherwise:")
    index.append("")
    index.append("```bash")
    index.append("cd ~/Downloads/leadership-legacy")
    index.append("python3 scripts/<script-name>.py")
    index.append("```")
    index.append("")

    index_path.write_text("\n".join(index), encoding="utf-8")
    print(f"wrote {index_path}")

    # Copy this collector into scripts too, then remove root copy if possible.
    self_src = ROOT / SELF
    self_dst = SCRIPTS / SELF
    if self_src.exists():
        shutil.copy2(self_src, self_dst)
        self_dst.chmod(0o755)
        print(f"copied {SELF} -> scripts/{SELF}")

    run(["git", "add", "scripts"])
    run(["git", "status", "--short"])

    commit = run(["git", "commit", "-m", "chore: organize python helper scripts under scripts"], check=False)
    if commit.returncode != 0:
        print("No commit created, likely no script changes.")

    push = run(["git", "push", "origin", "main"], check=False)
    if push.returncode != 0:
        print("Push failed. Check SSH/token auth, then run: git push origin main")

    print("\nDone.")
    if moved:
        print("Moved scripts:")
        for name in moved:
            print(f"- scripts/{name}")
    else:
        print("No root-level .py files found to move.")

if __name__ == "__main__":
    main()
