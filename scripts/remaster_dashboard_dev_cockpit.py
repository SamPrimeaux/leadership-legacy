#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
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
    path = ROOT / "package.json"
    pkg = json.loads(path.read_text())

    deps = pkg.setdefault("dependencies", {})
    deps["@monaco-editor/react"] = deps.get("@monaco-editor/react", "latest")
    deps["@xterm/xterm"] = deps.get("@xterm/xterm", "latest")
    deps["@xterm/addon-fit"] = deps.get("@xterm/addon-fit", "latest")
    deps["monaco-editor"] = deps.get("monaco-editor", "latest")

    scripts = pkg.setdefault("scripts", {})
    scripts["dev"] = scripts.get("dev", "vite")
    scripts["build"] = scripts.get("build", "vite build")
    scripts["deploy"] = scripts.get("deploy", "npm run build && wrangler deploy")
    scripts["cf:tunnel:help"] = "node scripts/print-cloudflare-tunnel-help.js"

    path.write_text(json.dumps(pkg, indent=2) + "\n")
    print("patched package.json with Monaco/xterm deps")

def patch_nav():
    nav_path = ROOT / "src/dashboard/data/dashboardNav.js"
    nav = nav_path.read_text()

    if "TerminalSquare" not in nav:
        nav = nav.replace(
            "BrainCircuit,",
            "BrainCircuit,\n      TerminalSquare,\n      Code2,\n      Network,"
        )

    if 'label: "Dev Cockpit"' not in nav:
        nav = nav.replace(
            '{ label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },',
            '{ label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },\n      { label: "Dev Cockpit", href: "/dashboard/dev", icon: TerminalSquare },\n      { label: "Editor", href: "/dashboard/dev/editor", icon: Code2 },\n      { label: "Tunnel", href: "/dashboard/dev/tunnel", icon: Network },'
        )

    nav_path.write_text(nav)
    print("patched dashboard nav")

def patch_routes():
    app_path = ROOT / "src/dashboard/DashboardApp.jsx"
    app = app_path.read_text()

    if 'DevCockpit' not in app:
        app = app.replace(
            'import { R2Storage } from "./pages/R2Storage.jsx";',
            'import { R2Storage } from "./pages/R2Storage.jsx";\nimport { DevCockpit } from "./pages/DevCockpit.jsx";'
        )

    if 'path="/dashboard/dev"' not in app:
        app = app.replace(
            '<Route path="/dashboard/storage" element={<R2Storage />} />',
            '<Route path="/dashboard/storage" element={<R2Storage />} />\n              <Route path="/dashboard/dev" element={<DevCockpit view="overview" />} />\n              <Route path="/dashboard/dev/editor" element={<DevCockpit view="editor" />} />\n              <Route path="/dashboard/dev/tunnel" element={<DevCockpit view="tunnel" />} />'
        )

    app_path.write_text(app)
    print("patched dashboard routes")

def main():
    patch_package()

    write("src/dashboard/data/devCockpitData.js", r'''
    export const powershellCommands = [
      {
        id: "clone",
        label: "Clone repo",
        command: "git clone git@github.com:SamPrimeaux/leadership-legacy.git",
        notes: "Use this once on Connor's machine after SSH is connected."
      },
      {
        id: "enter-repo",
        label: "Enter repo",
        command: "cd leadership-legacy",
        notes: "PowerShell uses cd the same way zsh does."
      },
      {
        id: "install",
        label: "Install packages",
        command: "npm install",
        notes: "Installs React, Vite, Monaco, xterm, and dashboard dependencies."
      },
      {
        id: "dev",
        label: "Run local dev server",
        command: "npm run dev",
        notes: "Starts the local Vite server."
      },
      {
        id: "build",
        label: "Build app",
        command: "npm run build",
        notes: "Validates production build before deploy."
      },
      {
        id: "deploy",
        label: "Deploy to Cloudflare",
        command: "npm run deploy",
        notes: "Builds and deploys through Wrangler."
      },
      {
        id: "health",
        label: "Check deployed Worker health",
        command: "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
        notes: "Verifies the Worker is responding."
      },
      {
        id: "r2-status",
        label: "Check R2 status",
        command: "curl https://leadership-legacy.meauxbility.workers.dev/api/r2/status",
        notes: "Verifies R2 binding and metadata."
      }
    ];

    export const tunnelCommands = [
      {
        id: "install-cloudflared-winget",
        label: "Install cloudflared with winget",
        command: "winget install --id Cloudflare.cloudflared",
        notes: "Recommended for PowerShell on Windows."
      },
      {
        id: "login",
        label: "Login to Cloudflare Tunnel",
        command: "cloudflared tunnel login",
        notes: "Opens browser auth. Connor should log into his Cloudflare account."
      },
      {
        id: "create",
        label: "Create named tunnel",
        command: "cloudflared tunnel create leadership-legacy-dev",
        notes: "Creates a reusable tunnel for local dev previews."
      },
      {
        id: "route",
        label: "Route DNS to tunnel",
        command: "cloudflared tunnel route dns leadership-legacy-dev dev.leadershiplegacydigital.com",
        notes: "Only run after the real domain/DNS is ready."
      },
      {
        id: "run-local",
        label: "Expose local Vite server",
        command: "cloudflared tunnel --url http://localhost:5173",
        notes: "Quick temporary tunnel for sharing local preview."
      }
    ];

    export const setupChecklist = [
      {
        group: "Local machine",
        items: [
          "Install Git",
          "Install Node.js LTS",
          "Install VS Code or Cursor",
          "Install Wrangler",
          "Install cloudflared",
          "Confirm PowerShell can run npm and git"
        ]
      },
      {
        group: "Repo",
        items: [
          "Clone leadership-legacy repo",
          "Run npm install",
          "Run npm run dev",
          "Open localhost public app",
          "Open localhost dashboard.html"
        ]
      },
      {
        group: "Cloudflare",
        items: [
          "Login with npx wrangler login",
          "Confirm Worker access",
          "Confirm R2 bucket",
          "Confirm D1 database",
          "Add secrets",
          "Run npm run deploy"
        ]
      },
      {
        group: "AI providers",
        items: [
          "Replace Sam's temporary OpenAI key with Connor's key",
          "Add Anthropic key",
          "Add Gemini key if available",
          "Confirm blocked model policy",
          "Confirm routing table"
        ]
      }
    ];

    export const starterFiles = {
      "src/worker/index.js": `export default {
      async fetch(request, env) {
        return new Response("Leadership Legacy Worker online");
      }
    };`,
      "src/dashboard/lib/providerRouter.js": `export function selectModel(task) {
      if (task.risk === "high") return "gpt-5.4";
      if (task.mode === "cheap") return "gpt-5.4-nano";
      return "gpt-5.4-mini";
    }`,
      "wrangler.jsonc": `{
      "name": "leadership-legacy",
      "main": "src/worker/index.js",
      "compatibility_date": "2026-05-06"
    }`,
      "cloudflared/config.yml": `tunnel: leadership-legacy-dev
    credentials-file: C:\\\\Users\\\\Connor\\\\.cloudflared\\\\leadership-legacy-dev.json

    ingress:
      - hostname: dev.leadershiplegacydigital.com
        service: http://localhost:5173
      - service: http_status:404`
    };
    ''')

    write("src/dashboard/components/dev/MonacoPanel.jsx", r'''
    import { useMemo, useState } from "react";
    import Editor from "@monaco-editor/react";
    import { starterFiles } from "../../data/devCockpitData.js";

    export function MonacoPanel() {
      const fileNames = Object.keys(starterFiles);
      const [activeFile, setActiveFile] = useState(fileNames[0]);
      const [files, setFiles] = useState(starterFiles);

      const language = useMemo(() => {
        if (activeFile.endsWith(".js") || activeFile.endsWith(".jsx")) return "javascript";
        if (activeFile.endsWith(".json") || activeFile.endsWith(".jsonc")) return "json";
        if (activeFile.endsWith(".yml") || activeFile.endsWith(".yaml")) return "yaml";
        return "plaintext";
      }, [activeFile]);

      return (
        <section className="dev-panel editor-cockpit">
          <div className="dev-panel-head">
            <div>
              <p className="dash-eyebrow">Monaco Editor</p>
              <h2>Guided code workspace</h2>
            </div>
            <span className="dev-badge">Browser draft editor</span>
          </div>

          <div className="editor-shell">
            <aside className="file-list">
              {fileNames.map((name) => (
                <button
                  key={name}
                  className={name === activeFile ? "selected" : ""}
                  onClick={() => setActiveFile(name)}
                >
                  {name}
                </button>
              ))}
            </aside>

            <div className="monaco-wrap">
              <Editor
                height="560px"
                language={language}
                theme="vs-dark"
                value={files[activeFile]}
                onChange={(value) => {
                  setFiles((current) => ({
                    ...current,
                    [activeFile]: value || ""
                  }));
                }}
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineHeight: 22,
                  wordWrap: "on",
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  tabSize: 2
                }}
              />
            </div>
          </div>

          <p className="dev-note">
            This Monaco surface is prepared for future file-backed editing through the Worker,
            GitHub, R2 snapshots, and Agent Sam style code actions. It is currently safe as a browser-side draft editor.
          </p>
        </section>
      );
    }
    ''')

    write("src/dashboard/components/dev/TerminalPanel.jsx", r'''
    import { useEffect, useRef, useState } from "react";
    import { Terminal } from "@xterm/xterm";
    import { FitAddon } from "@xterm/addon-fit";
    import "@xterm/xterm/css/xterm.css";
    import { powershellCommands } from "../../data/devCockpitData.js";

    export function TerminalPanel() {
      const ref = useRef(null);
      const terminalRef = useRef(null);
      const [activeCommand, setActiveCommand] = useState(powershellCommands[0]);

      useEffect(() => {
        if (!ref.current || terminalRef.current) return;

        const terminal = new Terminal({
          cursorBlink: true,
          convertEol: true,
          fontFamily: "JetBrains Mono, Consolas, monospace",
          fontSize: 13,
          theme: {
            background: "#050812",
            foreground: "#f8fafc",
            cursor: "#38bdf8",
            selectionBackground: "#1e3a5f"
          }
        });

        const fit = new FitAddon();
        terminal.loadAddon(fit);
        terminal.open(ref.current);
        fit.fit();

        terminal.writeln("Leadership Legacy Dev Terminal");
        terminal.writeln("PowerShell-friendly command cockpit");
        terminal.writeln("");
        terminal.writeln("This browser terminal is prepared for a future Worker/DO/PTY tunnel.");
        terminal.writeln("For now, copy commands into PowerShell.");
        terminal.writeln("");
        terminal.write("PS leadership-legacy> ");

        terminalRef.current = terminal;

        const onResize = () => fit.fit();
        window.addEventListener("resize", onResize);

        return () => {
          window.removeEventListener("resize", onResize);
          terminal.dispose();
          terminalRef.current = null;
        };
      }, []);

      function writeCommand(command) {
        setActiveCommand(command);
        const terminal = terminalRef.current;
        if (!terminal) return;

        terminal.writeln("");
        terminal.writeln(`PS leadership-legacy> ${command.command}`);
        terminal.writeln(`# ${command.notes}`);
        terminal.write("PS leadership-legacy> ");
      }

      async function copyCommand(command) {
        await navigator.clipboard.writeText(command.command);
        writeCommand({ ...command, notes: `${command.notes} Copied to clipboard.` });
      }

      return (
        <section className="dev-panel terminal-cockpit">
          <div className="dev-panel-head">
            <div>
              <p className="dash-eyebrow">xterm + PowerShell</p>
              <h2>Command cockpit</h2>
            </div>
            <span className="dev-badge">Prepared for DO/PTY</span>
          </div>

          <div className="terminal-layout">
            <aside className="command-list">
              {powershellCommands.map((command) => (
                <button key={command.id} onClick={() => copyCommand(command)}>
                  <strong>{command.label}</strong>
                  <code>{command.command}</code>
                </button>
              ))}
            </aside>

            <div className="terminal-wrap" ref={ref} />
          </div>

          <div className="command-detail">
            <strong>{activeCommand.label}</strong>
            <code>{activeCommand.command}</code>
            <p>{activeCommand.notes}</p>
          </div>
        </section>
      );
    }
    ''')

    write("src/dashboard/components/dev/TunnelPanel.jsx", r'''
    import { tunnelCommands } from "../../data/devCockpitData.js";

    export function TunnelPanel() {
      async function copy(text) {
        await navigator.clipboard.writeText(text);
      }

      return (
        <section className="dev-panel">
          <div className="dev-panel-head">
            <div>
              <p className="dash-eyebrow">Cloudflare Tunnel</p>
              <h2>Remote preview prep</h2>
            </div>
            <span className="dev-badge">cloudflared-ready</span>
          </div>

          <p className="dev-copy">
            This area teaches Connor how to expose a local PowerShell/Vite dev server through Cloudflare Tunnel
            without needing to deeply understand terminal workflows on day one.
          </p>

          <div className="tunnel-grid">
            {tunnelCommands.map((command) => (
              <article className="tunnel-card" key={command.id}>
                <strong>{command.label}</strong>
                <code>{command.command}</code>
                <p>{command.notes}</p>
                <button onClick={() => copy(command.command)}>Copy command</button>
              </article>
            ))}
          </div>

          <article className="dash-panel">
            <h3>Future dashboard integration</h3>
            <p>
              The next production step is a Worker Durable Object terminal bridge. The browser dashboard will request
              a session, the Worker will authorize it, and a local or hosted PTY service will stream output into xterm.
            </p>
            <code>Browser Dashboard → Worker → Durable Object → PTY/Tunnel Service → PowerShell</code>
          </article>
        </section>
      );
    }
    ''')

    write("src/dashboard/components/dev/SetupChecklist.jsx", r'''
    import { setupChecklist } from "../../data/devCockpitData.js";

    export function SetupChecklist() {
      return (
        <section className="dev-panel">
          <div className="dev-panel-head">
            <div>
              <p className="dash-eyebrow">Connor Setup</p>
              <h2>Guided onboarding checklist</h2>
            </div>
            <span className="dev-badge">PowerShell-friendly</span>
          </div>

          <div className="setup-grid">
            {setupChecklist.map((group) => (
              <article className="setup-card" key={group.group}>
                <h3>{group.group}</h3>
                <div className="check-list">
                  {group.items.map((item) => (
                    <label key={item}>
                      <input type="checkbox" />
                      <span>{item}</span>
                    </label>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/DevCockpit.jsx", r'''
    import { MonacoPanel } from "../components/dev/MonacoPanel.jsx";
    import { TerminalPanel } from "../components/dev/TerminalPanel.jsx";
    import { TunnelPanel } from "../components/dev/TunnelPanel.jsx";
    import { SetupChecklist } from "../components/dev/SetupChecklist.jsx";

    export function DevCockpit({ view = "overview" }) {
      return (
        <section>
          <p className="dash-eyebrow">Developer Cockpit</p>
          <h1>Built-in editor, terminal, and tunnel prep</h1>
          <p className="dash-subtitle">
            A guided technical workspace for Connor: Monaco for code, xterm for terminal-style guidance,
            PowerShell command presets, and Cloudflare Tunnel preparation for shareable local previews.
          </p>

          {view === "editor" ? (
            <MonacoPanel />
          ) : view === "tunnel" ? (
            <TunnelPanel />
          ) : (
            <>
              <div className="dev-hero-grid">
                <article className="dash-panel">
                  <h2>Why this matters</h2>
                  <p>
                    Connor can run, build, deploy, and inspect the platform without needing to memorize every CLI command.
                    The dashboard becomes a training cockpit and future control surface for real terminal sessions.
                  </p>
                </article>
                <article className="dash-panel">
                  <h2>Production path</h2>
                  <p>
                    This is prepared for a Worker Durable Object session bridge, Cloudflare Tunnel,
                    repo-aware commands, R2 snapshots, and safe AI-assisted code actions.
                  </p>
                </article>
              </div>

              <SetupChecklist />
              <TerminalPanel />
              <MonacoPanel />
              <TunnelPanel />
            </>
          )}
        </section>
      );
    }
    ''')

    css_path = ROOT / "src/dashboard/dashboard.css"
    existing = css_path.read_text() if css_path.exists() else ""
    dev_css = r'''
    .dev-hero-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
      margin-bottom: 18px;
    }

    .dev-panel {
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 24px;
      background: rgba(17, 24, 39, 0.72);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.22);
      padding: 22px;
      margin-bottom: 18px;
    }

    .dev-panel-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
    }

    .dev-panel-head h2 {
      margin: 0;
      font-size: clamp(1.5rem, 3vw, 2.4rem);
      letter-spacing: -0.04em;
    }

    .dev-badge {
      display: inline-flex;
      width: fit-content;
      min-height: 30px;
      align-items: center;
      border: 1px solid rgba(56, 189, 248, 0.32);
      color: #7dd3fc;
      background: rgba(56, 189, 248, 0.08);
      border-radius: 999px;
      padding: 0 10px;
      font-size: 0.78rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .dev-copy,
    .dev-note,
    .dash-panel p {
      color: #94a3b8;
      line-height: 1.65;
    }

    .editor-shell {
      display: grid;
      grid-template-columns: 260px minmax(0, 1fr);
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 18px;
      overflow: hidden;
      background: #050812;
    }

    .file-list {
      border-right: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(5, 8, 18, 0.78);
      padding: 10px;
      display: grid;
      align-content: start;
      gap: 7px;
    }

    .file-list button {
      width: 100%;
      border-radius: 12px;
      text-align: left;
      color: #94a3b8;
      background: transparent;
      border: 1px solid transparent;
      padding: 10px;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.82rem;
    }

    .file-list button:hover,
    .file-list button.selected {
      color: #f8fafc;
      border-color: rgba(56, 189, 248, 0.28);
      background: rgba(56, 189, 248, 0.1);
    }

    .monaco-wrap {
      min-width: 0;
    }

    .terminal-layout {
      display: grid;
      grid-template-columns: 340px minmax(0, 1fr);
      gap: 14px;
    }

    .command-list {
      display: grid;
      gap: 8px;
      max-height: 540px;
      overflow-y: auto;
    }

    .command-list button,
    .tunnel-card {
      border: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(255, 255, 255, 0.035);
      color: #f8fafc;
      border-radius: 16px;
      padding: 12px;
      text-align: left;
    }

    .command-list button strong,
    .command-list button code,
    .command-detail strong,
    .command-detail code,
    .tunnel-card strong,
    .tunnel-card code {
      display: block;
    }

    .command-list code,
    .command-detail code,
    .tunnel-card code,
    .dash-panel code {
      color: #7dd3fc;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.78rem;
      margin-top: 5px;
      white-space: normal;
    }

    .terminal-wrap {
      min-height: 540px;
      overflow: hidden;
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 16px;
      background: #050812;
      padding: 8px;
    }

    .command-detail {
      display: grid;
      gap: 8px;
      margin-top: 14px;
      border: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(255, 255, 255, 0.035);
      border-radius: 16px;
      padding: 14px;
    }

    .command-detail p {
      margin: 0;
      color: #94a3b8;
    }

    .tunnel-grid,
    .setup-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }

    .tunnel-card p {
      color: #94a3b8;
      line-height: 1.55;
    }

    .tunnel-card button {
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #7dd3fc;
      background: rgba(56, 189, 248, 0.08);
      border-radius: 999px;
      padding: 8px 12px;
      font-weight: 900;
    }

    .setup-card {
      border: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(255, 255, 255, 0.035);
      border-radius: 18px;
      padding: 16px;
    }

    .setup-card h3 {
      margin-top: 0;
    }

    .check-list {
      display: grid;
      gap: 9px;
    }

    .check-list label {
      display: flex;
      align-items: flex-start;
      gap: 9px;
      color: #cbd5e1;
      line-height: 1.4;
    }

    .check-list input {
      width: auto;
      margin-top: 3px;
    }

    @media (max-width: 1100px) {
      .dev-hero-grid,
      .editor-shell,
      .terminal-layout,
      .tunnel-grid,
      .setup-grid {
        grid-template-columns: 1fr;
      }

      .terminal-wrap {
        min-height: 420px;
      }
    }
    '''
    if ".dev-panel" not in existing:
      css_path.write_text(existing + "\n\n" + textwrap.dedent(dev_css), encoding="utf-8")
      print("patched dashboard.css with dev cockpit styles")

    write("scripts/print-cloudflare-tunnel-help.js", r'''
    console.log(`
    Leadership Legacy Cloudflare Tunnel Help

    PowerShell setup:

      winget install --id Cloudflare.cloudflared
      cloudflared tunnel login
      cloudflared tunnel --url http://localhost:5173

    Named tunnel flow:

      cloudflared tunnel create leadership-legacy-dev
      cloudflared tunnel route dns leadership-legacy-dev dev.leadershiplegacydigital.com
      cloudflared tunnel run leadership-legacy-dev

    Vite local app:

      npm install
      npm run dev

    Local URLs:

      http://localhost:5173/
      http://localhost:5173/dashboard.html
    `);
    ''')

    write("docs/DEV_COCKPIT.md", r'''
    # Developer Cockpit

    The dashboard now includes a developer cockpit for Connor.

    Routes:

    ```txt
    /dashboard/dev
    /dashboard/dev/editor
    /dashboard/dev/tunnel
    ```

    ## Features

    ```txt
    Monaco Editor draft workspace
    xterm browser terminal surface
    PowerShell command presets
    Cloudflare Tunnel setup commands
    Local machine onboarding checklist
    Worker/DO/PTY preparation notes
    ```

    ## Why this exists

    Connor is newer to CLI/terminal workflows and uses PowerShell. The cockpit makes commands copyable, visible, and explained inside the dashboard.

    ## Current limitation

    The terminal is currently browser-side and instructional. It does not execute commands yet.

    ## Production path

    Future architecture:

    ```txt
    Dashboard
    → Worker auth
    → Durable Object session
    → PTY/tunnel service
    → PowerShell/local or hosted shell
    → xterm stream
    ```

    ## Security

    Do not allow arbitrary terminal execution in production without:

    ```txt
    authentication
    authorization
    command allowlist
    audit logging
    timeout limits
    workspace isolation
    secret redaction
    ```
    ''')

    patch_nav()
    patch_routes()

    run(["npm", "install"], check=True)
    run(["npm", "run", "build"], check=True)

    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", "feat: add dashboard developer cockpit with Monaco xterm and tunnel prep"], check=False)

    print("\nDeveloper cockpit added.")
    print("Next:")
    print("npm run deploy")
    print("Open /dashboard/dev")
    print("Open /dashboard/dev/editor")
    print("Open /dashboard/dev/tunnel")

if __name__ == "__main__":
    main()
