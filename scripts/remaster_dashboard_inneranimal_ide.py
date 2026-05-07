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
    pkg_path = ROOT / "package.json"
    pkg = json.loads(pkg_path.read_text())

    deps = pkg.setdefault("dependencies", {})
    deps["@monaco-editor/react"] = deps.get("@monaco-editor/react", "latest")
    deps["monaco-editor"] = deps.get("monaco-editor", "latest")
    deps["@xterm/xterm"] = deps.get("@xterm/xterm", "latest")
    deps["@xterm/addon-fit"] = deps.get("@xterm/addon-fit", "latest")
    deps["lucide-react"] = deps.get("lucide-react", "latest")

    scripts = pkg.setdefault("scripts", {})
    scripts["dev"] = "vite"
    scripts["build"] = "vite build"
    scripts["deploy"] = "npm run build && wrangler deploy"

    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")
    print("patched package.json")

def main():
    patch_package()

    write("src/dashboard/main.jsx", r'''
    import React from "react";
    import { createRoot } from "react-dom/client";
    import { BrowserRouter } from "react-router-dom";
    import DashboardApp from "./DashboardApp.jsx";
    import "./dashboard.css";
    import "@xterm/xterm/css/xterm.css";

    createRoot(document.getElementById("dashboard-root")).render(
      <React.StrictMode>
        <BrowserRouter>
          <DashboardApp />
        </BrowserRouter>
      </React.StrictMode>
    );
    ''')

    write("src/dashboard/DashboardApp.jsx", r'''
    import { Routes, Route, Navigate } from "react-router-dom";
    import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
    import { AgentIDE } from "./pages/AgentIDE.jsx";

    export default function DashboardApp() {
      return (
        <DashboardAuthGate>
          <Routes>
            <Route path="/dashboard" element={<AgentIDE />} />
            <Route path="/dashboard/agent" element={<AgentIDE />} />
            <Route path="/dashboard/dev" element={<AgentIDE />} />
            <Route path="/dashboard/dev/editor" element={<AgentIDE />} />
            <Route path="/dashboard/dev/terminal" element={<AgentIDE initialTerminalOpen />} />
            <Route path="/dashboard/dev/agent" element={<AgentIDE />} />
            <Route path="/dashboard/pages" element={<AgentIDE activeSidePanel="pages" />} />
            <Route path="/dashboard/media" element={<AgentIDE activeSidePanel="media" />} />
            <Route path="/dashboard/storage" element={<AgentIDE activeSidePanel="storage" />} />
            <Route path="/dashboard/case-studies" element={<AgentIDE activeSidePanel="work" />} />
            <Route path="/dashboard/services" element={<AgentIDE activeSidePanel="services" />} />
            <Route path="/dashboard/leads" element={<AgentIDE activeSidePanel="leads" />} />
            <Route path="/dashboard/analytics" element={<AgentIDE activeSidePanel="analytics" />} />
            <Route path="/dashboard/settings" element={<AgentIDE activeSidePanel="settings" />} />
            <Route path="/dashboard/settings/ai-providers" element={<AgentIDE activeSidePanel="providers" />} />
            <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<AgentIDE />} />
          </Routes>
        </DashboardAuthGate>
      );
    }
    ''')

    write("src/dashboard/data/agentIdeFiles.js", r'''
    export const workspaceFiles = {
      "routes/home.jsx": {
        language: "javascript",
        type: "REACT",
        content: `export function HomePage() {
      return (
        <main className="public-page">
          <section className="hero">
            <p className="eyebrow">Mechanical Engineer × AI Developer</p>
            <h1>Engineering-grade AI systems for technical businesses.</h1>
            <p>
              Connor McNeely builds AI systems, RAG workflows, CAD automations,
              and full-stack applications for technical teams.
            </p>
          </section>
        </main>
      );
    }`
      },
      "routes/services.jsx": {
        language: "javascript",
        type: "REACT",
        content: `export const services = [
      "AI Engineering",
      "RAG Systems",
      "Full-Stack Apps",
      "CAD Automation",
      "CAD-to-Video",
      "Business Automation",
      "Consulting"
    ];

    export function ServicesPage() {
      return (
        <main>
          {services.map((service) => (
            <article key={service}>
              <h2>{service}</h2>
            </article>
          ))}
        </main>
      );
    }`
      },
      "worker/index.js": {
        language: "javascript",
        type: "WORKER",
        content: `export default {
      async fetch(request, env) {
        const url = new URL(request.url);

        if (url.pathname === "/api/health") {
          return Response.json({
            ok: true,
            app: "leadership-legacy",
            openaiConfigured: Boolean(env.OPENAI_API_KEY)
          });
        }

        return env.ASSETS.fetch(request);
      }
    };`
      },
      "cms/schema.sql": {
        language: "sql",
        type: "SQL",
        content: `CREATE TABLE IF NOT EXISTS cms_pages (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      route_path TEXT NOT NULL UNIQUE,
      status TEXT NOT NULL DEFAULT 'draft',
      draft_json TEXT NOT NULL DEFAULT '{}',
      published_json TEXT NOT NULL DEFAULT '{}',
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );`
      },
      "cloudflare/wrangler.jsonc": {
        language: "json",
        type: "CONFIG",
        content: `{
      "name": "leadership-legacy",
      "main": "src/worker/index.js",
      "compatibility_date": "2026-05-06",
      "assets": {
        "directory": "./dist",
        "binding": "ASSETS"
      },
      "r2_buckets": [
        {
          "binding": "WEBSITE",
          "bucket_name": "leadership-legacy"
        }
      ]
    }`
      }
    };

    export const localTree = [
      {
        name: "routes",
        kind: "folder",
        children: ["home.jsx", "services.jsx", "work.jsx", "contact.jsx"]
      },
      {
        name: "components",
        kind: "folder",
        children: ["Header.jsx", "Footer.jsx", "Hero.jsx", "ServiceCard.jsx"]
      },
      {
        name: "cms",
        kind: "folder",
        children: ["schema.sql", "pages.json", "sections.json"]
      },
      {
        name: "worker",
        kind: "folder",
        children: ["index.js", "openai.js", "r2.js"]
      }
    ];

    export const r2Objects = [
      "cms/pages/home.json",
      "cms/themes/leadership-legacy-dark.css",
      "assets/brand/mark.svg",
      "assets/models/engineering-system.glb",
      "snapshots/code/latest.zip",
      "docs/onboarding.md"
    ];

    export const commandPresets = [
      "npm install",
      "npm run dev",
      "npm run build",
      "npm run deploy",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/ai/providers",
      "npx wrangler secret put OPENAI_API_KEY",
      "npx wrangler d1 execute leadership-legacy-cms --remote --command \"SELECT id,title FROM cms_pages;\""
    ];
    ''')

    write("src/dashboard/pages/AgentIDE.jsx", r'''
    import { useEffect, useMemo, useRef, useState } from "react";
    import Editor from "@monaco-editor/react";
    import { Terminal } from "@xterm/xterm";
    import { FitAddon } from "@xterm/addon-fit";
    import {
      Activity,
      Bot,
      Box,
      ChevronDown,
      Circle,
      Cloud,
      Code2,
      Copy,
      Database,
      ExternalLink,
      Eye,
      FileCode2,
      FilePlus2,
      Folder,
      FolderOpen,
      GitBranch,
      Github,
      Globe2,
      HardDrive,
      Home,
      Image,
      KeyRound,
      Layers,
      Mail,
      MessageSquare,
      MoreHorizontal,
      Play,
      Search,
      Send,
      Settings,
      Sparkles,
      TerminalSquare,
      Wrench,
      X
    } from "lucide-react";
    import { commandPresets, localTree, r2Objects, workspaceFiles } from "../data/agentIdeFiles.js";

    function ActivityRail({ terminalOpen, setTerminalOpen }) {
      const icons = [
        { icon: Home, label: "Home" },
        { icon: Code2, label: "Workspace" },
        { icon: Search, label: "Search" },
        { icon: GitBranch, label: "Source Control" },
        { icon: Bot, label: "Agent" },
        { icon: Cloud, label: "Cloudflare" },
        { icon: Database, label: "Database" },
        { icon: Image, label: "Media" },
        { icon: Mail, label: "Mail" },
        { icon: Settings, label: "Settings" }
      ];

      return (
        <aside className="ia-activity">
          <a className="ia-logo" href="/dashboard" aria-label="Dashboard">LL</a>

          <div className="ia-activity-icons">
            {icons.map(({ icon: Icon, label }, index) => (
              <button className={index === 1 ? "active" : ""} key={label} title={label}>
                <Icon size={18} />
              </button>
            ))}
          </div>

          <button
            className={terminalOpen ? "active terminal-toggle" : "terminal-toggle"}
            title="Toggle terminal"
            onClick={() => setTerminalOpen((value) => !value)}
          >
            <TerminalSquare size={18} />
          </button>
        </aside>
      );
    }

    function Explorer({ files, activeFile, setActiveFile }) {
      const [githubOpen, setGithubOpen] = useState(true);
      const [driveOpen, setDriveOpen] = useState(true);

      return (
        <aside className="ia-explorer">
          <div className="ia-explorer-title">
            <span>EXPLORER</span>
            <div>
              <button title="New file"><FilePlus2 size={14} /></button>
              <button title="More"><MoreHorizontal size={14} /></button>
            </div>
          </div>

          <div className="ia-panel-block">
            <div className="ia-section-label">
              <ChevronDown size={14} />
              <span>LOCAL WORKSPACE</span>
              <small>Connected</small>
            </div>

            <div className="ia-tree">
              {localTree.map((folder) => (
                <details open key={folder.name}>
                  <summary>
                    <Folder size={14} />
                    <span>{folder.name}</span>
                  </summary>
                  {folder.children.map((child) => {
                    const key = `${folder.name}/${child}`;
                    const exists = files[key];
                    return (
                      <button
                        key={child}
                        className={activeFile === key ? "active" : ""}
                        onClick={() => exists && setActiveFile(key)}
                        disabled={!exists}
                      >
                        <FileCode2 size={13} />
                        <span>{child}</span>
                      </button>
                    );
                  })}
                </details>
              ))}
            </div>
          </div>

          <div className="ia-panel-block">
            <div className="ia-section-label">
              <ChevronDown size={14} />
              <span>CLOUDFLARE R2</span>
              <small>WEBSITE</small>
            </div>

            <div className="ia-r2-card">
              <div className="ia-r2-head">
                <HardDrive size={14} />
                <span>leadership-legacy</span>
              </div>
              <div className="ia-r2-actions">
                <button>Refresh</button>
                <button>Upload</button>
                <button>Open</button>
              </div>
              <div className="ia-r2-list">
                {r2Objects.map((key) => (
                  <span key={key}>{key}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="ia-connect-card">
            <button className="ia-card-toggle" onClick={() => setGithubOpen(!githubOpen)}>
              <Github size={15} />
              <span>GITHUB SYNC</span>
              <ChevronDown size={14} />
            </button>
            {githubOpen ? (
              <div className="ia-service-card">
                <div className="ia-orb"><Github size={44} /></div>
                <h3>GITHUB</h3>
                <p>Connect GitHub OAuth to list repos, browse, create, save, and delete files.</p>
                <button>Connect GitHub</button>
              </div>
            ) : null}
          </div>

          <div className="ia-connect-card">
            <button className="ia-card-toggle" onClick={() => setDriveOpen(!driveOpen)}>
              <FolderOpen size={15} />
              <span>GOOGLE DRIVE</span>
              <ChevronDown size={14} />
            </button>
            {driveOpen ? (
              <div className="ia-service-card">
                <div className="ia-orb"><Cloud size={44} /></div>
                <h3>GOOGLE DRIVE</h3>
                <p>Authorize Drive to browse folders, upload, create folders, open files, save from editor, and index docs.</p>
                <button>Connect Google Drive</button>
              </div>
            ) : null}
          </div>
        </aside>
      );
    }

    function Topbar() {
      return (
        <header className="ia-topbar">
          <div className="ia-search">
            <Search size={14} />
            <input placeholder="workspace: Leadership Legacy" aria-label="Workspace search" />
            <kbd>Cmd+K</kbd>
          </div>

          <div className="ia-top-actions">
            <button title="Public site"><Globe2 size={16} /></button>
            <button title="Preview"><Eye size={16} /></button>
            <button title="Terminal"><TerminalSquare size={16} /></button>
            <button title="Settings"><Settings size={16} /></button>
            <button title="More"><MoreHorizontal size={16} /></button>
          </div>
        </header>
      );
    }

    function EditorTabs({ activeFile, file }) {
      return (
        <div className="ia-tabs">
          <button className="active">
            <FileCode2 size={14} />
            <span>{activeFile.split("/").pop()}</span>
            <X size={13} />
          </button>
          <button>
            <Eye size={14} />
            <span>Preview</span>
          </button>
          <button>
            <Globe2 size={14} />
            <span>Browser</span>
          </button>
          <div className="ia-file-meta">
            <span>{file.type}</span>
            <span>UTF-8</span>
            <span>{file.language}</span>
          </div>
        </div>
      );
    }

    function CodeEditor({ activeFile, file, updateFile }) {
      return (
        <section className="ia-editor">
          <EditorTabs activeFile={activeFile} file={file} />

          <div className="ia-editor-frame">
            <Editor
              height="100%"
              language={file.language}
              theme="vs-dark"
              value={file.content}
              onChange={(value) => updateFile(value || "")}
              options={{
                minimap: { enabled: true },
                fontSize: 13,
                lineHeight: 21,
                wordWrap: "off",
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 2,
                renderLineHighlight: "line",
                overviewRulerBorder: false,
                padding: { top: 14, bottom: 14 }
              }}
            />
          </div>
        </section>
      );
    }

    function TerminalDock({ open }) {
      const elRef = useRef(null);
      const terminalRef = useRef(null);

      useEffect(() => {
        if (!open || !elRef.current || terminalRef.current) return;

        const term = new Terminal({
          cursorBlink: true,
          convertEol: true,
          fontFamily: "JetBrains Mono, Consolas, monospace",
          fontSize: 12,
          theme: {
            background: "#06292d",
            foreground: "#b8eef0",
            cursor: "#20e3f0",
            black: "#001316",
            blue: "#20e3f0",
            cyan: "#24f2ff",
            green: "#d1f85b",
            yellow: "#ffd43b",
            red: "#ff5c7a"
          }
        });

        const fit = new FitAddon();
        term.loadAddon(fit);
        term.open(elRef.current);
        fit.fit();

        term.writeln("");
        term.writeln("        ██████╗  █████╗  ██████╗ ███████╗███╗   ██╗");
        term.writeln("       ██╔════╝ ██╔══██╗██╔════╝ ██╔════╝████╗  ██║");
        term.writeln("       ██║  ███╗███████║██║  ███╗█████╗  ██╔██╗ ██║");
        term.writeln("       ██║   ██║██╔══██║██║   ██║██╔══╝  ██║╚██╗██║");
        term.writeln("       ╚██████╔╝██║  ██║╚██████╔╝███████╗██║ ╚████║");
        term.writeln("        ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝");
        term.writeln("");
        term.writeln("             L E A D E R S H I P   L E G A C Y");
        term.writeln("");
        term.writeln("  1. Start workspace");
        term.writeln("  2. Open Agent");
        term.writeln("  3. Activate tools");
        term.writeln("  4. Switch theme");
        term.writeln("  5. Run diagnostics");
        term.writeln("");
        term.writeln("Enter a number to get started...");
        term.writeln("");
        term.write("PS leadership-legacy> ");

        terminalRef.current = term;

        const onResize = () => fit.fit();
        window.addEventListener("resize", onResize);

        return () => {
          window.removeEventListener("resize", onResize);
          term.dispose();
          terminalRef.current = null;
        };
      }, [open]);

      useEffect(() => {
        const term = terminalRef.current;
        if (!term) return;
        commandPresets.forEach((command, index) => {
          if (index === 0) {
            term.writeln("");
            term.writeln("# PowerShell quick commands are ready in the command strip.");
            term.write("PS leadership-legacy> ");
          }
        });
      }, []);

      if (!open) return null;

      async function copyCommand(command) {
        await navigator.clipboard.writeText(command);
        const term = terminalRef.current;
        if (term) {
          term.writeln("");
          term.writeln(`PS leadership-legacy> ${command}`);
          term.writeln("# copied to clipboard");
          term.write("PS leadership-legacy> ");
        }
      }

      return (
        <section className="ia-terminal">
          <div className="ia-terminal-tabs">
            <button className="active">TERMINAL</button>
            <button>OUTPUT</button>
            <button>PROBLEMS</button>
            <span><Circle size={8} fill="currentColor" /> Connected · local prep</span>
            <div className="ia-terminal-actions">
              <button><TerminalSquare size={14} /></button>
              <button><ChevronDown size={14} /></button>
              <button><X size={14} /></button>
            </div>
          </div>

          <div className="ia-command-strip">
            {commandPresets.map((command) => (
              <button key={command} onClick={() => copyCommand(command)}>
                <Copy size={12} />
                {command}
              </button>
            ))}
          </div>

          <div className="ia-terminal-host" ref={elRef} />
        </section>
      );
    }

    function AgentPanel({ activeFile, file, updateFile }) {
      const [message, setMessage] = useState("");
      const [busy, setBusy] = useState(false);
      const [chat, setChat] = useState([]);
      const [model, setModel] = useState("gpt-5.4-mini");

      async function send() {
        const trimmed = message.trim();
        if (!trimmed || busy) return;

        const userMessage = {
          role: "user",
          text: trimmed
        };

        setChat((current) => [...current, userMessage]);
        setMessage("");
        setBusy(true);

        try {
          const response = await fetch("/api/openai/code", {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({
              model,
              mode: "refactor",
              filename: activeFile,
              language: file.language,
              code: file.content,
              instruction: trimmed
            })
          });

          const data = await response.json();

          if (!response.ok || !data.ok) {
            throw new Error(data.error || "Agent request failed.");
          }

          setChat((current) => [
            ...current,
            {
              role: "assistant",
              text: "Generated an updated file. Apply it when ready.",
              code: data.code,
              usage: data.usage
            }
          ]);
        } catch (error) {
          setChat((current) => [
            ...current,
            {
              role: "assistant",
              text: error.message
            }
          ]);
        } finally {
          setBusy(false);
        }
      }

      async function copy(text) {
        await navigator.clipboard.writeText(text);
      }

      return (
        <aside className="ia-agent">
          <div className="ia-agent-head">
            <span>AGENT CONNOR</span>
            <button><MoreHorizontal size={15} /></button>
          </div>

          <div className="ia-agent-tabs">
            <button className="active">Chat</button>
            <button>Chats</button>
            <button>New Chat</button>
          </div>

          <div className="ia-agent-body">
            {chat.length === 0 ? (
              <div className="ia-empty-agent">
                <div className="ia-agent-orb">
                  <Bot size={24} />
                </div>
                <h3>What should we work on?</h3>
                <p>Ask the agent to edit the active Monaco file, create Worker routes, improve CMS logic, or explain PowerShell steps.</p>
              </div>
            ) : (
              <div className="ia-chat-list">
                {chat.map((item, index) => (
                  <article className={`ia-chat ${item.role}`} key={`${item.role}-${index}`}>
                    <p>{item.text}</p>
                    {item.code ? (
                      <div className="ia-code-result">
                        <div>
                          <button onClick={() => copy(item.code)}>Copy</button>
                          <button onClick={() => updateFile(item.code)}>Apply to editor</button>
                        </div>
                        <pre>{item.code}</pre>
                      </div>
                    ) : null}
                  </article>
                ))}
              </div>
            )}
          </div>

          <div className="ia-agent-compose">
            <button title="Attach"><FilePlus2 size={16} /></button>
            <textarea
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  send();
                }
              }}
              placeholder="Message Agent Connor..."
            />
            <select value={model} onChange={(event) => setModel(event.target.value)}>
              <option value="gpt-5.4-mini">AUTO · GPT-5.4 mini</option>
              <option value="gpt-5.4-nano">FAST · GPT-5.4 nano</option>
              <option value="gpt-5.4">DEEP · GPT-5.4</option>
            </select>
            <button className="send" onClick={send} disabled={busy}>
              {busy ? <Sparkles size={16} /> : <Send size={16} />}
            </button>
          </div>
        </aside>
      );
    }

    function StatusBar({ activeFile }) {
      return (
        <footer className="ia-status">
          <span><GitBranch size={13} /> main</span>
          <span>Leadership Legacy</span>
          <span>Ln 1, Col 1</span>
          <span>Spaces: 2</span>
          <span>UTF-8</span>
          <span>{activeFile}</span>
          <span className="auto">Auto</span>
        </footer>
      );
    }

    export function AgentIDE({ initialTerminalOpen = false }) {
      const [files, setFiles] = useState(workspaceFiles);
      const [activeFile, setActiveFile] = useState("routes/services.jsx");
      const [terminalOpen, setTerminalOpen] = useState(initialTerminalOpen);

      const file = useMemo(() => files[activeFile] || Object.values(files)[0], [files, activeFile]);

      function updateFile(content) {
        setFiles((current) => ({
          ...current,
          [activeFile]: {
            ...current[activeFile],
            content
          }
        }));
      }

      return (
        <div className={terminalOpen ? "ia-shell terminal-open" : "ia-shell"}>
          <ActivityRail terminalOpen={terminalOpen} setTerminalOpen={setTerminalOpen} />
          <Explorer files={files} activeFile={activeFile} setActiveFile={setActiveFile} />

          <main className="ia-workspace">
            <Topbar />

            <div className="ia-main-grid">
              <div className="ia-center">
                <CodeEditor activeFile={activeFile} file={file} updateFile={updateFile} />
                <TerminalDock open={terminalOpen} />
              </div>

              <AgentPanel activeFile={activeFile} file={file} updateFile={updateFile} />
            </div>

            <StatusBar activeFile={activeFile} />
          </main>
        </div>
      );
    }
    ''')

    write("src/dashboard/dashboard.css", r'''
    @import "../shared/brand/tokens.css";

    * {
      box-sizing: border-box;
    }

    html,
    body,
    #dashboard-root {
      min-height: 100%;
    }

    body {
      margin: 0;
      background: #041316;
      color: #d9fbff;
      font-family: Inter, system-ui, sans-serif;
      overflow: hidden;
    }

    button,
    input,
    textarea,
    select {
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    .ia-shell {
      height: 100vh;
      display: grid;
      grid-template-columns: 48px 214px minmax(0, 1fr);
      background: #041316;
      color: #d9fbff;
    }

    .ia-activity {
      min-width: 0;
      border-right: 1px solid rgba(69, 228, 238, 0.18);
      background: #062226;
      display: grid;
      grid-template-rows: auto 1fr auto;
      justify-items: center;
      gap: 12px;
      padding: 10px 0;
    }

    .ia-logo {
      width: 32px;
      height: 32px;
      display: grid;
      place-items: center;
      border-radius: 10px;
      background: linear-gradient(135deg, #29d8e5, #53f4cf);
      color: #022024;
      font-weight: 950;
      letter-spacing: -0.08em;
    }

    .ia-activity-icons {
      display: grid;
      gap: 8px;
      align-content: start;
    }

    .ia-activity button,
    .ia-top-actions button,
    .ia-explorer button,
    .ia-agent button,
    .ia-terminal button {
      border: 0;
      background: transparent;
      color: inherit;
    }

    .ia-activity button {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      color: #72c8cf;
      border-radius: 9px;
    }

    .ia-activity button:hover,
    .ia-activity button.active {
      color: #d9fbff;
      background: rgba(69, 228, 238, 0.12);
      box-shadow: inset 2px 0 0 #23dcec;
    }

    .terminal-toggle {
      margin-bottom: 8px;
    }

    .ia-explorer {
      overflow-y: auto;
      border-right: 1px solid rgba(69, 228, 238, 0.18);
      background: #06282c;
      color: #b7e9ee;
      padding-bottom: 22px;
      scrollbar-color: rgba(69, 228, 238, .28) transparent;
    }

    .ia-explorer-title {
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 12px;
      color: #8ecdd4;
      font-size: 0.72rem;
      letter-spacing: 0.16em;
      font-weight: 900;
      text-transform: uppercase;
    }

    .ia-explorer-title div {
      display: flex;
      gap: 4px;
    }

    .ia-panel-block {
      border-top: 1px solid rgba(69, 228, 238, 0.12);
      padding: 10px 10px 8px;
    }

    .ia-section-label {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #86d4dc;
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      font-weight: 900;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .ia-section-label small {
      margin-left: auto;
      color: #5d9fa7;
      font-size: 0.62rem;
      letter-spacing: 0;
      text-transform: none;
      font-weight: 700;
    }

    .ia-tree {
      display: grid;
      gap: 2px;
    }

    .ia-tree details {
      display: grid;
      gap: 2px;
    }

    .ia-tree summary {
      list-style: none;
      min-height: 26px;
      display: flex;
      align-items: center;
      gap: 7px;
      color: #b3e4e9;
      font-size: 0.8rem;
      user-select: none;
    }

    .ia-tree summary::-webkit-details-marker {
      display: none;
    }

    .ia-tree button {
      width: 100%;
      min-height: 27px;
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 0 8px 0 24px;
      border-radius: 5px;
      color: #9fd7dd;
      text-align: left;
      font-size: 0.78rem;
    }

    .ia-tree button:hover,
    .ia-tree button.active {
      color: #f3feff;
      background: rgba(69, 228, 238, 0.11);
      outline: 1px solid rgba(198, 255, 251, 0.75);
    }

    .ia-tree button:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }

    .ia-r2-card {
      border-radius: 10px;
      background: rgba(4, 19, 22, 0.38);
      border: 1px solid rgba(69, 228, 238, 0.12);
      padding: 8px;
    }

    .ia-r2-head {
      display: flex;
      align-items: center;
      gap: 7px;
      color: #2ee9f2;
      font-size: 0.76rem;
      margin-bottom: 7px;
    }

    .ia-r2-actions {
      display: flex;
      gap: 4px;
      margin-bottom: 8px;
    }

    .ia-r2-actions button {
      border: 1px solid rgba(69, 228, 238, 0.14);
      background: rgba(69, 228, 238, 0.06);
      color: #b7e9ee;
      border-radius: 5px;
      padding: 3px 6px;
      font-size: 0.64rem;
      font-weight: 800;
    }

    .ia-r2-list {
      display: grid;
      gap: 4px;
      max-height: 110px;
      overflow: auto;
    }

    .ia-r2-list span {
      color: #87cbd2;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.65rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .ia-connect-card {
      padding: 0 10px 10px;
    }

    .ia-card-toggle {
      width: 100%;
      display: flex;
      align-items: center;
      gap: 7px;
      color: #93d9df;
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      font-weight: 900;
      text-transform: uppercase;
      padding: 8px 0;
    }

    .ia-card-toggle svg:last-child {
      margin-left: auto;
    }

    .ia-service-card {
      text-align: center;
      border-radius: 18px;
      border: 1px dashed rgba(69, 228, 238, 0.24);
      background: rgba(6, 45, 50, 0.44);
      padding: 18px 12px;
    }

    .ia-orb {
      width: 92px;
      height: 92px;
      display: grid;
      place-items: center;
      margin: 0 auto 12px;
      border-radius: 999px;
      border: 1px dashed rgba(194, 255, 250, 0.25);
      color: #a4dfe3;
      background: radial-gradient(circle, rgba(69, 228, 238, 0.1), transparent 68%);
    }

    .ia-service-card h3 {
      margin: 0 0 8px;
      color: #f3feff;
      letter-spacing: 0.18em;
      font-size: 0.86rem;
    }

    .ia-service-card p {
      margin: 0 0 12px;
      color: #8fc8cf;
      line-height: 1.45;
      font-size: 0.72rem;
    }

    .ia-service-card button {
      border-radius: 6px;
      background: #cdfcff;
      color: #05272b;
      padding: 8px 12px;
      font-size: 0.72rem;
      font-weight: 900;
    }

    .ia-workspace {
      min-width: 0;
      display: grid;
      grid-template-rows: 32px minmax(0, 1fr) 20px;
      background: #031013;
    }

    .ia-topbar {
      min-width: 0;
      border-bottom: 1px solid rgba(69, 228, 238, 0.18);
      background: #05282c;
      display: grid;
      grid-template-columns: minmax(240px, 1fr) auto;
      align-items: center;
      gap: 12px;
      padding: 0 12px;
    }

    .ia-search {
      width: min(520px, 100%);
      height: 22px;
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 0 auto;
      color: #7ecad2;
      border: 1px solid rgba(69, 228, 238, 0.12);
      background: rgba(0, 0, 0, 0.14);
      border-radius: 5px;
      padding: 0 8px;
    }

    .ia-search input {
      flex: 1;
      min-width: 0;
      border: 0;
      outline: 0;
      background: transparent;
      color: #c8f8fc;
      font-size: 0.72rem;
    }

    .ia-search kbd {
      color: #7cbcc4;
      font-size: 0.58rem;
      font-family: "JetBrains Mono", Consolas, monospace;
    }

    .ia-top-actions {
      display: flex;
      gap: 6px;
      color: #95dce2;
    }

    .ia-top-actions button {
      width: 24px;
      height: 24px;
      border-radius: 5px;
      display: grid;
      place-items: center;
    }

    .ia-top-actions button:hover {
      background: rgba(69, 228, 238, 0.11);
      color: #eaffff;
    }

    .ia-main-grid {
      min-height: 0;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 330px;
    }

    .ia-center {
      min-width: 0;
      min-height: 0;
      display: grid;
      grid-template-rows: minmax(0, 1fr);
      border-right: 1px solid rgba(69, 228, 238, 0.18);
    }

    .terminal-open .ia-center {
      grid-template-rows: minmax(0, 1fr) 42%;
    }

    .ia-editor {
      min-width: 0;
      min-height: 0;
      display: grid;
      grid-template-rows: 58px minmax(0, 1fr);
      background: #05181b;
    }

    .ia-tabs {
      min-width: 0;
      display: flex;
      align-items: stretch;
      border-bottom: 1px solid rgba(69, 228, 238, 0.18);
      background: #05282c;
    }

    .ia-tabs button {
      min-width: 112px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      border: 0;
      border-right: 1px solid rgba(69, 228, 238, 0.14);
      background: transparent;
      color: #87cfd6;
      font-size: 0.72rem;
      font-weight: 800;
    }

    .ia-tabs button.active {
      color: #eaffff;
      background: #073b40;
      box-shadow: inset 0 2px 0 #14d9e9;
    }

    .ia-file-meta {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 0 12px;
      color: #75b8c0;
      font-size: 0.68rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .ia-editor-frame {
      min-width: 0;
      min-height: 0;
      background: #041316;
    }

    .ia-editor-frame .monaco-editor,
    .ia-editor-frame .monaco-editor-background,
    .ia-editor-frame .monaco-editor .margin {
      background-color: #041316 !important;
    }

    .ia-terminal {
      min-height: 0;
      display: grid;
      grid-template-rows: 33px 34px minmax(0, 1fr);
      border-top: 2px solid rgba(32, 227, 240, 0.55);
      background: #06292d;
    }

    .ia-terminal-tabs {
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid rgba(69, 228, 238, 0.18);
      padding: 0 12px;
      color: #8cd8df;
    }

    .ia-terminal-tabs button {
      height: 100%;
      color: #8cd8df;
      font-size: 0.68rem;
      letter-spacing: 0.16em;
      font-weight: 900;
      border-bottom: 2px solid transparent;
    }

    .ia-terminal-tabs button.active {
      color: #eaffff;
      border-color: #20e3f0;
    }

    .ia-terminal-tabs span {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #d1f85b;
      font-size: 0.68rem;
      margin-left: 6px;
    }

    .ia-terminal-actions {
      margin-left: auto;
      display: flex;
      gap: 6px;
    }

    .ia-terminal-actions button {
      color: #8cd8df;
    }

    .ia-command-strip {
      display: flex;
      align-items: center;
      gap: 6px;
      overflow-x: auto;
      padding: 5px 10px;
      border-bottom: 1px solid rgba(69, 228, 238, 0.12);
    }

    .ia-command-strip button {
      flex: 0 0 auto;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: 1px solid rgba(69, 228, 238, 0.14);
      border-radius: 999px;
      background: rgba(3, 16, 19, 0.58);
      color: #91d9df;
      padding: 4px 8px;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.62rem;
    }

    .ia-terminal-host {
      min-height: 0;
      padding: 8px;
      overflow: hidden;
    }

    .ia-agent {
      min-width: 0;
      min-height: 0;
      display: grid;
      grid-template-rows: 42px 38px minmax(0, 1fr) 88px;
      background: #06282c;
    }

    .ia-agent-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(69, 228, 238, 0.18);
      padding: 0 12px;
      color: #8cd8df;
      font-size: 0.72rem;
      letter-spacing: 0.16em;
      font-weight: 900;
    }

    .ia-agent-tabs {
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid rgba(69, 228, 238, 0.12);
      padding: 0 12px;
    }

    .ia-agent-tabs button {
      color: #89cfd6;
      font-size: 0.72rem;
      font-weight: 800;
    }

    .ia-agent-tabs button.active {
      color: #eaffff;
    }

    .ia-agent-body {
      min-height: 0;
      overflow: auto;
      display: grid;
    }

    .ia-empty-agent {
      margin: auto;
      width: min(260px, calc(100% - 36px));
      text-align: center;
      color: #9ddbe1;
    }

    .ia-agent-orb {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      margin: 0 auto 16px;
      border-radius: 14px;
      background: rgba(28, 220, 232, 0.12);
      color: #35e7f5;
      border: 1px solid rgba(69, 228, 238, 0.18);
    }

    .ia-empty-agent h3 {
      margin: 0 0 8px;
      color: #eaffff;
      font-size: 0.92rem;
    }

    .ia-empty-agent p {
      margin: 0;
      color: #81c1c8;
      line-height: 1.5;
      font-size: 0.72rem;
    }

    .ia-chat-list {
      display: grid;
      align-content: start;
      gap: 12px;
      padding: 14px;
    }

    .ia-chat {
      border-radius: 12px;
      padding: 10px 12px;
      border: 1px solid rgba(69, 228, 238, 0.14);
      background: rgba(3, 16, 19, 0.38);
      color: #c9f4f7;
      line-height: 1.45;
      font-size: 0.78rem;
    }

    .ia-chat.user {
      background: rgba(69, 228, 238, 0.08);
    }

    .ia-code-result {
      margin-top: 10px;
      border: 1px solid rgba(69, 228, 238, 0.16);
      border-radius: 10px;
      overflow: hidden;
      background: #041316;
    }

    .ia-code-result div {
      display: flex;
      gap: 8px;
      padding: 8px;
      border-bottom: 1px solid rgba(69, 228, 238, 0.12);
    }

    .ia-code-result button {
      border-radius: 6px;
      background: rgba(69, 228, 238, 0.1);
      color: #d9fbff;
      padding: 5px 8px;
      font-size: 0.7rem;
      font-weight: 900;
    }

    .ia-code-result pre {
      max-height: 240px;
      overflow: auto;
      margin: 0;
      padding: 10px;
      color: #b8eef0;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.68rem;
      white-space: pre-wrap;
    }

    .ia-agent-compose {
      display: grid;
      grid-template-columns: 30px minmax(0, 1fr) 86px 30px;
      gap: 8px;
      align-items: end;
      border-top: 1px solid rgba(69, 228, 238, 0.18);
      padding: 10px;
      background: #052226;
    }

    .ia-agent-compose > button,
    .ia-agent-compose select {
      height: 34px;
      border-radius: 8px;
      border: 1px solid rgba(69, 228, 238, 0.14);
      background: rgba(3, 16, 19, 0.52);
      color: #a3e6ec;
    }

    .ia-agent-compose textarea {
      height: 42px;
      resize: none;
      border: 1px solid rgba(69, 228, 238, 0.14);
      background: rgba(3, 16, 19, 0.52);
      color: #eaffff;
      border-radius: 10px;
      padding: 11px 10px;
      outline: none;
      font-size: 0.76rem;
    }

    .ia-agent-compose select {
      font-size: 0.58rem;
      font-weight: 900;
      padding: 0 4px;
    }

    .ia-agent-compose .send {
      color: #062226;
      background: #20e3f0;
    }

    .ia-status {
      min-width: 0;
      height: 20px;
      display: flex;
      align-items: center;
      gap: 14px;
      border-top: 1px solid rgba(69, 228, 238, 0.18);
      background: #0a5961;
      color: #b9f9fd;
      padding: 0 8px;
      font-size: 0.64rem;
      overflow: hidden;
    }

    .ia-status span {
      flex: 0 0 auto;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .ia-status .auto {
      margin-left: auto;
      font-size: 0.82rem;
    }

    .dashboard-auth-page {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 28px;
      background:
        radial-gradient(circle at 18% 8%, rgba(32, 227, 240, 0.18), transparent 30rem),
        radial-gradient(circle at 84% 0%, rgba(34, 197, 94, 0.12), transparent 28rem),
        #041316;
    }

    .dashboard-auth-layout {
      width: min(1080px, 100%);
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 22px;
      align-items: stretch;
    }

    .dashboard-auth-intro,
    .dashboard-auth-card {
      border: 1px solid rgba(69, 228, 238, 0.18);
      border-radius: 28px;
      background: rgba(6, 40, 44, 0.78);
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.42);
      backdrop-filter: blur(22px);
    }

    .dashboard-auth-intro {
      padding: clamp(28px, 5vw, 54px);
      display: grid;
      align-content: center;
      gap: 18px;
    }

    .dashboard-auth-intro h1 {
      margin: 0;
      font-size: clamp(2.8rem, 7vw, 6rem);
      line-height: 0.9;
      letter-spacing: -0.075em;
    }

    .dashboard-auth-intro p,
    .dashboard-auth-card p,
    .dashboard-auth-card small {
      color: #9ddbe1;
      line-height: 1.65;
    }

    .dash-eyebrow {
      color: #20e3f0;
      font-family: "JetBrains Mono", Consolas, monospace;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-size: 0.72rem;
      font-weight: 900;
      margin: 0;
    }

    .auth-icon {
      width: 56px;
      height: 56px;
      display: grid;
      place-items: center;
      border-radius: 19px;
      color: #041316;
      background: linear-gradient(135deg, #20e3f0, #53f4cf);
    }

    .auth-feature-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }

    .auth-feature-grid span {
      border: 1px solid rgba(69, 228, 238, 0.2);
      border-radius: 14px;
      background: rgba(69, 228, 238, 0.07);
      color: #d9fbff;
      padding: 10px 12px;
      font-size: 0.86rem;
      font-weight: 850;
    }

    .dashboard-auth-card {
      padding: clamp(22px, 4vw, 34px);
      display: grid;
      gap: 16px;
    }

    .dashboard-auth-card h2 {
      margin: 0 0 8px;
      font-size: clamp(1.8rem, 4vw, 2.8rem);
      line-height: 0.96;
      letter-spacing: -0.055em;
    }

    .auth-tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      border: 1px solid rgba(69, 228, 238, 0.14);
      background: rgba(3, 16, 19, 0.52);
      border-radius: 999px;
      padding: 6px;
    }

    .auth-tabs button {
      min-height: 40px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: 0;
      border-radius: 999px;
      background: transparent;
      color: #8fc8cf;
      font-weight: 900;
    }

    .auth-tabs button.active {
      color: #041316;
      background: linear-gradient(135deg, #20e3f0, #53f4cf);
    }

    .dashboard-auth-card label {
      display: grid;
      gap: 8px;
      color: #d9fbff;
      font-weight: 850;
    }

    .auth-input-wrap {
      min-height: 48px;
      display: flex;
      align-items: center;
      gap: 10px;
      border: 1px solid rgba(69, 228, 238, 0.18);
      border-radius: 16px;
      background: rgba(3, 16, 19, 0.72);
      color: #20e3f0;
      padding: 0 13px;
    }

    .auth-input-wrap input {
      width: 100%;
      min-height: 46px;
      border: 0;
      outline: 0;
      background: transparent;
      color: #f3feff;
      padding: 0;
    }

    .auth-submit,
    .primary-action {
      min-height: 48px;
      width: 100%;
      border: 0;
      border-radius: 16px;
      color: #041316;
      background: linear-gradient(135deg, #20e3f0, #53f4cf);
      font-weight: 950;
    }

    .auth-error {
      color: #ffd6d6;
      border: 1px solid rgba(255, 92, 122, 0.28);
      background: rgba(255, 92, 122, 0.1);
      border-radius: 14px;
      padding: 10px 12px;
      font-weight: 850;
    }

    @media (max-width: 1120px) {
      .ia-shell {
        grid-template-columns: 48px 210px minmax(0, 1fr);
      }

      .ia-main-grid {
        grid-template-columns: minmax(0, 1fr);
      }

      .ia-agent {
        display: none;
      }
    }

    @media (max-width: 780px) {
      body {
        overflow: auto;
      }

      .ia-shell {
        min-height: 100vh;
        height: auto;
        grid-template-columns: 48px minmax(0, 1fr);
      }

      .ia-explorer {
        display: none;
      }

      .ia-workspace {
        min-height: 100vh;
      }

      .dashboard-auth-layout,
      .auth-feature-grid {
        grid-template-columns: 1fr;
      }
    }
    ''')

    write("src/worker/index.js", r'''
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

    async function callOpenAI(env, payload) {
      if (!env.OPENAI_API_KEY) {
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
          authorization: `Bearer ${env.OPENAI_API_KEY}`
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
            openaiConfigured: Boolean(env.OPENAI_API_KEY),
            r2Binding: Boolean(env.WEBSITE),
            timestamp: new Date().toISOString()
          });
        }

        if (pathname === "/api/ai/providers") {
          return json({
            ok: true,
            openaiConfigured: Boolean(env.OPENAI_API_KEY),
            providers: [
              {
                key: "openai",
                displayName: "OpenAI",
                secretName: "OPENAI_API_KEY",
                status: env.OPENAI_API_KEY ? "configured" : "missing_secret",
                models: ["gpt-5.4-mini", "gpt-5.4-nano", "gpt-5.4"]
              },
              {
                key: "anthropic",
                displayName: "Anthropic",
                secretName: "ANTHROPIC_API_KEY",
                status: env.ANTHROPIC_API_KEY ? "configured" : "missing_secret",
                models: ["claude-sonnet", "claude-haiku"]
              }
            ],
            blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
          });
        }

        if (pathname === "/api/openai/code" && request.method === "POST") {
          const body = await readJson(request);
          const model = body.model || "gpt-5.4-mini";
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
            return json({
              ok: false,
              binding: "WEBSITE",
              error: error.message
            }, 500);
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
            }))
          });
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
    ''')

    write("docs/INNERANIMAL_STYLE_DASHBOARD_REMASTER.md", r'''
    # InnerAnimal-Style Dashboard Remaster

    This remaster removes the oversized dashboard headers and replaces the experience with a full-height IDE workspace.

    ## Design Direction

    ```txt
    Activity rail
    Explorer sidebar
    Cloudflare R2 panel
    GitHub/Drive connection cards
    Editor tabs
    Monaco center editor
    Right Agent panel
    Bottom terminal drawer
    Thin status bar
    No fake marketing hero headers inside dashboard
    No iframe-style card wrapper
    ```

    ## Main Route

    ```txt
    /dashboard
    /dashboard/agent
    /dashboard/dev
    ```

    ## OpenAI

    Agent panel calls:

    ```txt
    POST /api/openai/code
    ```

    The OpenAI key remains server-side as:

    ```txt
    OPENAI_API_KEY
    ```

    ## Terminal

    The terminal is xterm-prepped and command-copy enabled. It does not execute shell commands yet.

    Production terminal execution still needs:

    ```txt
    Worker auth
    Durable Object session
    PTY service
    command allowlist
    audit logs
    secret redaction
    ```
    ''')

    run(["npm", "install"], check=True)
    run(["npm", "run", "build"], check=True)
    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", "feat: remaster dashboard as InnerAnimal-style IDE workspace"], check=False)

    print("\nInnerAnimal-style dashboard remaster complete.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")
    print("Open: https://leadership-legacy.meauxbility.workers.dev/dashboard")

if __name__ == "__main__":
    main()
