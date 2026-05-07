#!/usr/bin/env python3
from pathlib import Path
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

def main():
    write("src/dashboard/DashboardApp.jsx", r'''
    import { Routes, Route, Navigate } from "react-router-dom";
    import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
    import { AgentIDE } from "./pages/AgentIDE.jsx";

    export default function DashboardApp() {
      return (
        <DashboardAuthGate>
          <Routes>
            <Route path="/dashboard" element={<AgentIDE routeView="home" />} />
            <Route path="/dashboard/agent" element={<AgentIDE routeView="agent" />} />
            <Route path="/dashboard/dev" element={<AgentIDE routeView="agent" />} />
            <Route path="/dashboard/dev/editor" element={<AgentIDE routeView="agent" />} />
            <Route path="/dashboard/dev/terminal" element={<AgentIDE routeView="agent" initialTerminalOpen />} />

            <Route path="/dashboard/storage" element={<AgentIDE routeView="storage" />} />
            <Route path="/dashboard/settings" element={<AgentIDE routeView="settings" />} />
            <Route path="/dashboard/settings/ai-providers" element={<AgentIDE routeView="settings" />} />
            <Route path="/dashboard/analytics" element={<AgentIDE routeView="analytics" />} />
            <Route path="/dashboard/learn" element={<AgentIDE routeView="learn" />} />
            <Route path="/dashboard/mail" element={<AgentIDE routeView="mail" />} />
            <Route path="/dashboard/mcp" element={<AgentIDE routeView="mcp" />} />

            <Route path="/dashboard/pages" element={<AgentIDE routeView="cms" />} />
            <Route path="/dashboard/media" element={<AgentIDE routeView="storage" />} />
            <Route path="/dashboard/case-studies" element={<AgentIDE routeView="cms" />} />
            <Route path="/dashboard/services" element={<AgentIDE routeView="cms" />} />
            <Route path="/dashboard/leads" element={<AgentIDE routeView="analytics" />} />

            <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<AgentIDE routeView="agent" />} />
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
        source: "local",
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
        source: "local",
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
        source: "local",
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
        source: "local",
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
        source: "local",
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
      },
      {
        name: "cloudflare",
        kind: "folder",
        children: ["wrangler.jsonc"]
      }
    ];

    export const commandPresets = [
      "npm install --include=dev",
      "npm run dev",
      "npm run build",
      "npm run test:e2e",
      "npm run deploy",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/ai/providers",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=cms/",
      "npx wrangler secret put OPENAI_API_KEY",
      "npx wrangler secret put ANTHROPIC_API_KEY"
    ];

    export const dashboardViews = {
      home: {
        label: "Command Center",
        tab: "dashboard",
        title: "Leadership Legacy operating system",
        subtitle: "CMS, code, storage, AI providers, learning, mail, MCP tools, analytics, and deployment workflows."
      },
      agent: {
        label: "Agent",
        tab: "agent",
        title: "Agent Connor",
        subtitle: "Edit Monaco files, call OpenAI, inspect generated code, and prepare GitHub/R2 saves."
      },
      storage: {
        label: "Storage",
        tab: "storage",
        title: "R2 + assets",
        subtitle: "Browse R2 objects, open text assets into Monaco, and prepare uploads/snapshots."
      },
      settings: {
        label: "Settings",
        tab: "settings",
        title: "Provider + integration settings",
        subtitle: "OpenAI, Anthropic, Gemini, GitHub, Google, Resend, Cloudflare, Supabase, and AWS readiness."
      },
      analytics: {
        label: "Analytics",
        tab: "analytics",
        title: "Analytics + telemetry",
        subtitle: "Track page views, leads, agent runs, model costs, tool calls, errors, and deployment health."
      },
      learn: {
        label: "Learn",
        tab: "learn",
        title: "Connor learning path",
        subtitle: "Guided setup modules, CLI/PowerShell practice, integration study guide, and rubric scoring."
      },
      mail: {
        label: "Mail",
        tab: "mail",
        title: "Mail + lead communication",
        subtitle: "Prepare Gmail OAuth, Resend transactional email, lead drafts, and approved outbound workflows."
      },
      mcp: {
        label: "MCP",
        tab: "mcp",
        title: "MCP tools registry",
        subtitle: "Tool registry, permissions, execution logs, approval gates, and provider adapters."
      },
      cms: {
        label: "CMS",
        tab: "cms",
        title: "CMS runtime",
        subtitle: "Pages, sections, services, case studies, resources, navigation, SEO, and publishing."
      }
    };
    ''')

    write("src/dashboard/pages/AgentIDE.jsx", r'''
    import { useEffect, useMemo, useRef, useState } from "react";
    import Editor from "@monaco-editor/react";
    import { Terminal } from "@xterm/xterm";
    import { FitAddon } from "@xterm/addon-fit";
    import {
      Activity,
      Bot,
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
      Globe2,
      GraduationCap,
      HardDrive,
      Home,
      Image,
      Inbox,
      KeyRound,
      Layers,
      Mail,
      MoreHorizontal,
      RefreshCcw,
      Search,
      Send,
      Settings,
      ShieldCheck,
      Sparkles,
      TerminalSquare,
      Upload,
      Wrench,
      X
    } from "lucide-react";
    import {
      commandPresets,
      dashboardViews,
      localTree,
      workspaceFiles
    } from "../data/agentIdeFiles.js";

    function getLanguageFromKey(key = "") {
      if (key.endsWith(".js") || key.endsWith(".jsx")) return "javascript";
      if (key.endsWith(".ts") || key.endsWith(".tsx")) return "typescript";
      if (key.endsWith(".json") || key.endsWith(".jsonc")) return "json";
      if (key.endsWith(".css")) return "css";
      if (key.endsWith(".html")) return "html";
      if (key.endsWith(".md")) return "markdown";
      if (key.endsWith(".sql")) return "sql";
      if (key.endsWith(".yml") || key.endsWith(".yaml")) return "yaml";
      return "plaintext";
    }

    function useResizablePanels() {
      const [explorerWidth, setExplorerWidth] = useState(() => Number(localStorage.getItem("ll-explorer-width") || 250));
      const [agentWidth, setAgentWidth] = useState(() => Number(localStorage.getItem("ll-agent-width") || 340));
      const [terminalHeight, setTerminalHeight] = useState(() => Number(localStorage.getItem("ll-terminal-height") || 260));

      function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
      }

      function beginDrag(type, startEvent) {
        startEvent.preventDefault();
        const startX = startEvent.clientX;
        const startY = startEvent.clientY;
        const startExplorer = explorerWidth;
        const startAgent = agentWidth;
        const startTerminal = terminalHeight;

        function onMove(event) {
          if (type === "explorer") {
            const next = clamp(startExplorer + event.clientX - startX, 190, 430);
            setExplorerWidth(next);
            localStorage.setItem("ll-explorer-width", String(next));
          }

          if (type === "agent") {
            const next = clamp(startAgent - (event.clientX - startX), 280, 560);
            setAgentWidth(next);
            localStorage.setItem("ll-agent-width", String(next));
          }

          if (type === "terminal") {
            const next = clamp(startTerminal - (event.clientY - startY), 160, 520);
            setTerminalHeight(next);
            localStorage.setItem("ll-terminal-height", String(next));
          }
        }

        function onUp() {
          window.removeEventListener("mousemove", onMove);
          window.removeEventListener("mouseup", onUp);
          document.body.classList.remove("ia-resizing");
        }

        document.body.classList.add("ia-resizing");
        window.addEventListener("mousemove", onMove);
        window.addEventListener("mouseup", onUp);
      }

      return {
        explorerWidth,
        agentWidth,
        terminalHeight,
        beginDrag
      };
    }

    function ActivityRail({ routeView, terminalOpen, setTerminalOpen }) {
      const icons = [
        { icon: Home, label: "Dashboard", href: "/dashboard", key: "home" },
        { icon: Code2, label: "Agent", href: "/dashboard/agent", key: "agent" },
        { icon: HardDrive, label: "Storage", href: "/dashboard/storage", key: "storage" },
        { icon: Activity, label: "Analytics", href: "/dashboard/analytics", key: "analytics" },
        { icon: GraduationCap, label: "Learn", href: "/dashboard/learn", key: "learn" },
        { icon: Mail, label: "Mail", href: "/dashboard/mail", key: "mail" },
        { icon: Wrench, label: "MCP", href: "/dashboard/mcp", key: "mcp" },
        { icon: Settings, label: "Settings", href: "/dashboard/settings", key: "settings" }
      ];

      return (
        <aside className="ia-activity">
          <a className="ia-logo" href="/dashboard" aria-label="Dashboard">LL</a>

          <div className="ia-activity-icons">
            {icons.map(({ icon: Icon, label, href, key }) => (
              <a className={routeView === key ? "active" : ""} key={label} title={label} href={href}>
                <Icon size={18} />
              </a>
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

    function Explorer({
      files,
      activeFile,
      setActiveFile,
      r2Objects,
      loadR2Objects,
      openR2Object,
      r2Loading,
      githubStatus
    }) {
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
              <small>Seeded</small>
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
                <button onClick={() => loadR2Objects("")}>
                  <RefreshCcw size={12} />
                  {r2Loading ? "Loading" : "Refresh"}
                </button>
                <button>
                  <Upload size={12} />
                  Upload
                </button>
                <a href="/dashboard/storage">Open</a>
              </div>
              <div className="ia-r2-list">
                {r2Objects.length === 0 ? (
                  <span>Click refresh to load real R2 objects.</span>
                ) : (
                  r2Objects.slice(0, 24).map((object) => (
                    <button key={object.key} onClick={() => openR2Object(object.key)}>
                      {object.key}
                    </button>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="ia-connect-card">
            <button className="ia-card-toggle" onClick={() => setGithubOpen(!githubOpen)}>
              <GitBranch size={15} />
              <span>GITHUB SYNC</span>
              <ChevronDown size={14} />
            </button>
            {githubOpen ? (
              <div className="ia-service-card">
                <div className="ia-orb"><GitBranch size={44} /></div>
                <h3>GITHUB</h3>
                <p>{githubStatus?.configured ? "GitHub secrets detected. OAuth routes are prepared." : "Connect GitHub OAuth/App to list repos, browse, create, save, and open PRs."}</p>
                <a href="/api/oauth/github/start">Connect GitHub</a>
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
                <a href="/api/oauth/google/start">Connect Google</a>
              </div>
            ) : null}
          </div>
        </aside>
      );
    }

    function Topbar({ routeView }) {
      const view = dashboardViews[routeView] || dashboardViews.agent;

      return (
        <header className="ia-topbar">
          <div className="ia-search">
            <Search size={14} />
            <input placeholder={`workspace: Leadership Legacy / ${view.label}`} aria-label="Workspace search" />
            <kbd>Cmd+K</kbd>
          </div>

          <div className="ia-top-actions">
            <a href="/" title="Public site"><Globe2 size={16} /></a>
            <button title="Preview"><Eye size={16} /></button>
            <a href="/dashboard/storage" title="Storage"><HardDrive size={16} /></a>
            <a href="/dashboard/settings" title="Settings"><Settings size={16} /></a>
            <button title="More"><MoreHorizontal size={16} /></button>
          </div>
        </header>
      );
    }

    function EditorTabs({ activeFile, file, routeView }) {
      const view = dashboardViews[routeView] || dashboardViews.agent;

      return (
        <div className="ia-tabs">
          <button className="active">
            <FileCode2 size={14} />
            <span>{activeFile.split("/").pop()}</span>
            <X size={13} />
          </button>
          <a href="/dashboard/storage">
            <HardDrive size={14} />
            <span>Storage</span>
          </a>
          <a href="/dashboard/mcp">
            <Wrench size={14} />
            <span>MCP</span>
          </a>
          <a href="/dashboard/learn">
            <GraduationCap size={14} />
            <span>Learn</span>
          </a>
          <div className="ia-file-meta">
            <span>{view.tab}</span>
            <span>{file.type}</span>
            <span>{file.language}</span>
          </div>
        </div>
      );
    }

    function CodeEditor({ activeFile, file, updateFile, routeView }) {
      return (
        <section className="ia-editor">
          <EditorTabs activeFile={activeFile} file={file} routeView={routeView} />

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

    function TerminalDock({ open, height, beginDrag }) {
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

        term.writeln("LEADERSHIP LEGACY TERMINAL");
        term.writeln("");
        term.writeln("PowerShell-friendly command cockpit.");
        term.writeln("Future terminal execution path:");
        term.writeln("Dashboard → Worker Auth → Durable Object → PTY/Tunnel");
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
        <section className="ia-terminal" style={{ height }}>
          <div className="ia-terminal-resizer" onMouseDown={(event) => beginDrag("terminal", event)} />
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

    function ViewPanel({ routeView, r2Objects, loadR2Objects, openR2Object, providerStatus }) {
      const view = dashboardViews[routeView] || dashboardViews.agent;

      if (routeView === "agent") return null;

      if (routeView === "home") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">Dashboard</p>
            <h2>{view.title}</h2>
            <p>{view.subtitle}</p>
            <div className="ia-metric-grid">
              <article><strong>OpenAI</strong><span>{providerStatus?.openaiConfigured ? "Configured" : "Missing"}</span></article>
              <article><strong>R2</strong><span>{r2Objects.length} loaded objects</span></article>
              <article><strong>Routes</strong><span>8 dashboard sections</span></article>
              <article><strong>Tests</strong><span>Playwright ready</span></article>
            </div>
          </section>
        );
      }

      if (routeView === "storage") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">Storage</p>
            <h2>Cloudflare R2 browser</h2>
            <p>Load real objects from the `leadership-legacy` R2 bucket. Text/code-like files open directly into Monaco.</p>
            <div className="ia-toolbar">
              <button onClick={() => loadR2Objects("")}><RefreshCcw size={14} /> Load bucket root</button>
              <button onClick={() => loadR2Objects("cms/")}><Database size={14} /> cms/</button>
              <button onClick={() => loadR2Objects("assets/")}><Image size={14} /> assets/</button>
              <button onClick={() => loadR2Objects("snapshots/")}><Layers size={14} /> snapshots/</button>
            </div>
            <div className="ia-object-table">
              {r2Objects.map((object) => (
                <button key={object.key} onClick={() => openR2Object(object.key)}>
                  <span>{object.key}</span>
                  <small>{object.size ? `${object.size} bytes` : "object"}</small>
                </button>
              ))}
            </div>
          </section>
        );
      }

      if (routeView === "settings") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">Settings</p>
            <h2>Provider and integration readiness</h2>
            <p>{view.subtitle}</p>
            <div className="ia-settings-grid">
              {[
                ["OpenAI", providerStatus?.openaiConfigured ? "configured" : "missing", "OPENAI_API_KEY"],
                ["Anthropic", "pending Connor key", "ANTHROPIC_API_KEY"],
                ["Gemini", "planned", "GEMINI_API_KEY"],
                ["Resend", "planned", "RESEND_API_KEY"],
                ["GitHub", "OAuth/App planned", "GITHUB_CLIENT_ID"],
                ["Google", "Drive/Gmail OAuth planned", "GOOGLE_CLIENT_ID"],
                ["Supabase", "planned", "SUPABASE_SERVICE_ROLE_KEY"],
                ["AWS", "optional", "AWS_ACCESS_KEY_ID"]
              ].map(([name, status, secret]) => (
                <article key={name}>
                  <ShieldCheck size={18} />
                  <strong>{name}</strong>
                  <span>{status}</span>
                  <code>{secret}</code>
                </article>
              ))}
            </div>
          </section>
        );
      }

      if (routeView === "analytics") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">Analytics</p>
            <h2>Telemetry overview</h2>
            <p>{view.subtitle}</p>
            <div className="ia-metric-grid">
              <article><strong>2,188</strong><span>seed page views</span></article>
              <article><strong>1</strong><span>lead in queue</span></article>
              <article><strong>0</strong><span>critical errors</span></article>
              <article><strong>OpenAI</strong><span>provider live</span></article>
            </div>
          </section>
        );
      }

      if (routeView === "learn") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">Learn</p>
            <h2>Connor study path</h2>
            <p>{view.subtitle}</p>
            <div className="ia-learning-list">
              {[
                "Run the app locally with PowerShell",
                "Deploy the Worker",
                "Understand R2, D1, KV, and Durable Objects",
                "Connect OpenAI, Anthropic, Gemini, Resend",
                "Connect GitHub App/OAuth",
                "Connect Google Drive and Gmail OAuth",
                "Run Playwright and read failures",
                "Use the rubric to score readiness"
              ].map((item, index) => (
                <label key={item}>
                  <input type="checkbox" />
                  <span>{index + 1}. {item}</span>
                </label>
              ))}
            </div>
          </section>
        );
      }

      if (routeView === "mail") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">Mail</p>
            <h2>Gmail + Resend workflows</h2>
            <p>{view.subtitle}</p>
            <div className="ia-settings-grid">
              <article><Mail size={18} /><strong>Gmail OAuth</strong><span>Thread read + draft compose</span><code>/api/oauth/google/start</code></article>
              <article><Inbox size={18} /><strong>Lead Inbox</strong><span>Inbound project requests</span><code>/api/forms/contact</code></article>
              <article><Send size={18} /><strong>Resend</strong><span>Transactional email</span><code>RESEND_API_KEY</code></article>
              <article><ShieldCheck size={18} /><strong>Approval Gate</strong><span>No auto-send without approval</span><code>required</code></article>
            </div>
          </section>
        );
      }

      if (routeView === "mcp") {
        return (
          <section className="ia-view-panel">
            <p className="ia-view-kicker">MCP</p>
            <h2>Tools registry</h2>
            <p>{view.subtitle}</p>
            <div className="ia-tool-grid">
              {[
                "github.listRepos",
                "github.getFile",
                "github.commitFile",
                "r2.listObjects",
                "r2.getObject",
                "d1.query",
                "openai.codeAction",
                "anthropic.review",
                "gmail.createDraft",
                "drive.importFile",
                "playwright.runSmoke",
                "resend.sendEmail"
              ].map((tool) => (
                <article key={tool}>
                  <Wrench size={15} />
                  <strong>{tool}</strong>
                  <span>approval-aware</span>
                </article>
              ))}
            </div>
          </section>
        );
      }

      return (
        <section className="ia-view-panel">
          <p className="ia-view-kicker">{view.label}</p>
          <h2>{view.title}</h2>
          <p>{view.subtitle}</p>
        </section>
      );
    }

    function AgentPanel({ activeFile, file, updateFile, routeView }) {
      const [message, setMessage] = useState("");
      const [busy, setBusy] = useState(false);
      const [chat, setChat] = useState([]);
      const [model, setModel] = useState("gpt-5.4-mini");

      async function send() {
        const trimmed = message.trim();
        if (!trimmed || busy) return;

        setChat((current) => [...current, { role: "user", text: trimmed }]);
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
          setChat((current) => [...current, { role: "assistant", text: error.message }]);
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
            <span>{routeView === "agent" ? "AGENT CONNOR" : "ASSISTANT"}</span>
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
                <div className="ia-agent-orb"><Bot size={24} /></div>
                <h3>What should we work on?</h3>
                <p>Ask the agent to edit the active Monaco file, open real R2 assets, explain PowerShell steps, or prepare GitHub saves.</p>
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
              <option value="gpt-5.4-mini">AUTO · 5.4 mini</option>
              <option value="gpt-5.4-nano">FAST · 5.4 nano</option>
              <option value="gpt-5.4">DEEP · 5.4</option>
            </select>
            <button className="send" onClick={send} disabled={busy}>
              {busy ? <Sparkles size={16} /> : <Send size={16} />}
            </button>
          </div>
        </aside>
      );
    }

    function StatusBar({ activeFile, r2Objects }) {
      return (
        <footer className="ia-status">
          <span><GitBranch size={13} /> main</span>
          <span>Leadership Legacy</span>
          <span>R2: {r2Objects.length} objects</span>
          <span>UTF-8</span>
          <span>{activeFile}</span>
          <span className="auto">Auto</span>
        </footer>
      );
    }

    export function AgentIDE({ initialTerminalOpen = false, routeView = "agent" }) {
      const [files, setFiles] = useState(workspaceFiles);
      const [activeFile, setActiveFile] = useState("worker/index.js");
      const [terminalOpen, setTerminalOpen] = useState(initialTerminalOpen);
      const [r2Objects, setR2Objects] = useState([]);
      const [r2Loading, setR2Loading] = useState(false);
      const [providerStatus, setProviderStatus] = useState(null);
      const [githubStatus, setGithubStatus] = useState(null);

      const {
        explorerWidth,
        agentWidth,
        terminalHeight,
        beginDrag
      } = useResizablePanels();

      const file = useMemo(() => files[activeFile] || Object.values(files)[0], [files, activeFile]);
      const showViewPanel = routeView !== "agent";

      function updateFile(content) {
        setFiles((current) => ({
          ...current,
          [activeFile]: {
            ...current[activeFile],
            content
          }
        }));
      }

      async function loadR2Objects(prefix = "") {
        setR2Loading(true);
        try {
          const response = await fetch(`/api/r2/list?prefix=${encodeURIComponent(prefix)}`);
          const data = await response.json();
          if (data.ok) setR2Objects(data.objects || []);
        } finally {
          setR2Loading(false);
        }
      }

      async function openR2Object(key) {
        const response = await fetch(`/api/r2/text?key=${encodeURIComponent(key)}`);
        const data = await response.json();

        if (!data.ok) {
          const objectFile = `r2/${key}`;
          setFiles((current) => ({
            ...current,
            [objectFile]: {
              language: "plaintext",
              type: "R2",
              source: "r2",
              content: `Unable to open ${key}\n\n${data.error || "Object may be binary or unavailable."}`
            }
          }));
          setActiveFile(objectFile);
          return;
        }

        const objectFile = `r2/${key}`;
        setFiles((current) => ({
          ...current,
          [objectFile]: {
            language: getLanguageFromKey(key),
            type: "R2",
            source: "r2",
            content: data.text
          }
        }));
        setActiveFile(objectFile);
      }

      useEffect(() => {
        loadR2Objects("");
        fetch("/api/ai/providers")
          .then((res) => res.json())
          .then(setProviderStatus)
          .catch(() => {});
        fetch("/api/github/status")
          .then((res) => res.json())
          .then(setGithubStatus)
          .catch(() => {});
      }, []);

      const gridStyle = {
        gridTemplateColumns: `48px ${explorerWidth}px minmax(0, 1fr)`
      };

      const mainStyle = {
        gridTemplateColumns: showViewPanel
          ? `minmax(360px, 0.76fr) minmax(320px, 0.52fr) ${agentWidth}px`
          : `minmax(0, 1fr) ${agentWidth}px`
      };

      return (
        <div className={terminalOpen ? "ia-shell terminal-open" : "ia-shell"} style={gridStyle}>
          <ActivityRail routeView={routeView} terminalOpen={terminalOpen} setTerminalOpen={setTerminalOpen} />

          <Explorer
            files={files}
            activeFile={activeFile}
            setActiveFile={setActiveFile}
            r2Objects={r2Objects}
            loadR2Objects={loadR2Objects}
            openR2Object={openR2Object}
            r2Loading={r2Loading}
            githubStatus={githubStatus}
          />

          <div className="ia-resizer ia-resizer-explorer" onMouseDown={(event) => beginDrag("explorer", event)} />

          <main className="ia-workspace">
            <Topbar routeView={routeView} />

            <div className={showViewPanel ? "ia-main-grid has-view-panel" : "ia-main-grid"} style={mainStyle}>
              <div className="ia-center">
                <CodeEditor activeFile={activeFile} file={file} updateFile={updateFile} routeView={routeView} />
                <TerminalDock open={terminalOpen} height={terminalHeight} beginDrag={beginDrag} />
              </div>

              {showViewPanel ? (
                <ViewPanel
                  routeView={routeView}
                  r2Objects={r2Objects}
                  loadR2Objects={loadR2Objects}
                  openR2Object={openR2Object}
                  providerStatus={providerStatus}
                />
              ) : null}

              <div className="ia-resizer ia-resizer-agent" onMouseDown={(event) => beginDrag("agent", event)} />
              <AgentPanel activeFile={activeFile} file={file} updateFile={updateFile} routeView={routeView} />
            </div>

            <StatusBar activeFile={activeFile} r2Objects={r2Objects} />
          </main>
        </div>
      );
    }
    ''')

    write("src/dashboard/dashboard.css", r'''
    @import "../shared/brand/tokens.css";

    * { box-sizing: border-box; }

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

    button { cursor: pointer; }
    a { color: inherit; text-decoration: none; }

    .ia-resizing,
    .ia-resizing * {
      cursor: col-resize !important;
      user-select: none !important;
    }

    .ia-shell {
      height: 100vh;
      display: grid;
      background: #041316;
      color: #d9fbff;
      position: relative;
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
      z-index: 5;
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
    .ia-activity a,
    .ia-top-actions button,
    .ia-top-actions a,
    .ia-explorer button,
    .ia-agent button,
    .ia-terminal button {
      border: 0;
      background: transparent;
      color: inherit;
    }

    .ia-activity button,
    .ia-activity a {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      color: #72c8cf;
      border-radius: 9px;
    }

    .ia-activity button:hover,
    .ia-activity button.active,
    .ia-activity a:hover,
    .ia-activity a.active {
      color: #d9fbff;
      background: rgba(69, 228, 238, 0.12);
      box-shadow: inset 2px 0 0 #23dcec;
    }

    .terminal-toggle { margin-bottom: 8px; }

    .ia-explorer {
      overflow-y: auto;
      border-right: 1px solid rgba(69, 228, 238, 0.18);
      background: #06282c;
      color: #b7e9ee;
      padding-bottom: 22px;
      scrollbar-color: rgba(69, 228, 238, .28) transparent;
      min-width: 0;
    }

    .ia-resizer {
      position: absolute;
      z-index: 30;
      background: transparent;
    }

    .ia-resizer:hover {
      background: rgba(32, 227, 240, 0.26);
    }

    .ia-resizer-explorer {
      top: 0;
      bottom: 20px;
      width: 7px;
      left: calc(var(--explorer-left, 298px));
      display: none;
    }

    .ia-resizer-agent {
      top: 32px;
      bottom: 20px;
      width: 7px;
      right: var(--agent-right, 340px);
      cursor: col-resize;
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
      position: sticky;
      top: 0;
      background: rgba(6, 40, 44, 0.94);
      backdrop-filter: blur(12px);
      z-index: 4;
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

    .ia-tree summary::-webkit-details-marker { display: none; }

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
      flex-wrap: wrap;
      gap: 4px;
      margin-bottom: 8px;
    }

    .ia-r2-actions button,
    .ia-r2-actions a {
      display: inline-flex;
      align-items: center;
      gap: 4px;
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
      max-height: 160px;
      overflow: auto;
    }

    .ia-r2-list span,
    .ia-r2-list button {
      color: #87cbd2;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.65rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-align: left;
      padding: 0;
    }

    .ia-r2-list button:hover {
      color: #f3feff;
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

    .ia-card-toggle svg:last-child { margin-left: auto; }

    .ia-service-card {
      text-align: center;
      border-radius: 18px;
      border: 1px dashed rgba(69, 228, 238, 0.24);
      background: rgba(6, 45, 50, 0.44);
      padding: 18px 12px;
    }

    .ia-orb {
      width: 86px;
      height: 86px;
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

    .ia-service-card a {
      display: inline-flex;
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

    .ia-top-actions button,
    .ia-top-actions a {
      width: 24px;
      height: 24px;
      border-radius: 5px;
      display: grid;
      place-items: center;
    }

    .ia-top-actions button:hover,
    .ia-top-actions a:hover {
      background: rgba(69, 228, 238, 0.11);
      color: #eaffff;
    }

    .ia-main-grid {
      min-height: 0;
      display: grid;
      position: relative;
    }

    .ia-center {
      min-width: 0;
      min-height: 0;
      display: grid;
      grid-template-rows: minmax(0, 1fr);
      border-right: 1px solid rgba(69, 228, 238, 0.18);
    }

    .terminal-open .ia-center {
      grid-template-rows: minmax(0, 1fr) auto;
    }

    .ia-editor {
      min-width: 0;
      min-height: 0;
      display: grid;
      grid-template-rows: 48px minmax(0, 1fr);
      background: #05181b;
    }

    .ia-tabs {
      min-width: 0;
      display: flex;
      align-items: stretch;
      border-bottom: 1px solid rgba(69, 228, 238, 0.18);
      background: #05282c;
    }

    .ia-tabs button,
    .ia-tabs a {
      min-width: 102px;
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

    .ia-tabs button.active,
    .ia-tabs a:hover {
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
      min-height: 150px;
      display: grid;
      grid-template-rows: 30px 32px minmax(0, 1fr);
      border-top: 2px solid rgba(32, 227, 240, 0.55);
      background: #06292d;
      position: relative;
    }

    .ia-terminal-resizer {
      position: absolute;
      top: -5px;
      left: 0;
      right: 0;
      height: 8px;
      cursor: row-resize;
      z-index: 5;
    }

    .ia-terminal-resizer:hover {
      background: rgba(32, 227, 240, 0.25);
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

    .ia-view-panel {
      min-width: 0;
      min-height: 0;
      overflow: auto;
      padding: 22px;
      border-right: 1px solid rgba(69, 228, 238, 0.18);
      background:
        radial-gradient(circle at 20% 0%, rgba(32, 227, 240, 0.08), transparent 22rem),
        #04181b;
    }

    .ia-view-kicker {
      margin: 0 0 8px;
      color: #20e3f0;
      font-size: 0.68rem;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-weight: 900;
    }

    .ia-view-panel h2 {
      margin: 0 0 10px;
      color: #f3feff;
      font-size: clamp(1.8rem, 4vw, 3.7rem);
      line-height: 0.94;
      letter-spacing: -0.07em;
    }

    .ia-view-panel p {
      color: #98d6dc;
      line-height: 1.65;
    }

    .ia-metric-grid,
    .ia-settings-grid,
    .ia-tool-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }

    .ia-metric-grid article,
    .ia-settings-grid article,
    .ia-tool-grid article {
      min-width: 0;
      border: 1px solid rgba(69, 228, 238, 0.14);
      border-radius: 15px;
      background: rgba(3, 16, 19, 0.38);
      padding: 14px;
      display: grid;
      gap: 7px;
    }

    .ia-metric-grid strong,
    .ia-settings-grid strong,
    .ia-tool-grid strong {
      color: #f3feff;
      font-size: 1.05rem;
    }

    .ia-metric-grid span,
    .ia-settings-grid span,
    .ia-tool-grid span {
      color: #8fc8cf;
      font-size: 0.82rem;
    }

    .ia-settings-grid code {
      color: #20e3f0;
      font-size: 0.7rem;
      font-family: "JetBrains Mono", Consolas, monospace;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .ia-toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 16px 0;
    }

    .ia-toolbar button {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid rgba(69, 228, 238, 0.16);
      border-radius: 999px;
      background: rgba(69, 228, 238, 0.08);
      color: #d9fbff;
      padding: 8px 10px;
      font-size: 0.76rem;
      font-weight: 900;
    }

    .ia-object-table {
      display: grid;
      gap: 7px;
      margin-top: 12px;
    }

    .ia-object-table button {
      min-width: 0;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: center;
      border: 1px solid rgba(69, 228, 238, 0.13);
      border-radius: 11px;
      background: rgba(3, 16, 19, 0.38);
      color: #c8f8fc;
      padding: 10px;
      text-align: left;
    }

    .ia-object-table span {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.74rem;
    }

    .ia-object-table small {
      color: #8fc8cf;
      font-size: 0.7rem;
    }

    .ia-learning-list {
      display: grid;
      gap: 9px;
      margin-top: 18px;
    }

    .ia-learning-list label {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      border: 1px solid rgba(69, 228, 238, 0.13);
      border-radius: 12px;
      background: rgba(3, 16, 19, 0.38);
      padding: 10px;
      color: #c8f8fc;
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

    .ia-agent-tabs button.active { color: #eaffff; }

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

    .ia-chat.user { background: rgba(69, 228, 238, 0.08); }

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
      grid-template-columns: 30px minmax(0, 1fr) 88px 30px;
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

    @media (max-width: 1240px) {
      .ia-main-grid,
      .ia-main-grid.has-view-panel {
        grid-template-columns: minmax(0, 1fr) !important;
      }

      .ia-agent {
        display: none;
      }

      .ia-view-panel {
        display: none;
      }
    }

    @media (max-width: 820px) {
      body { overflow: auto; }

      .ia-shell {
        min-height: 100vh;
        height: auto;
        grid-template-columns: 48px minmax(0, 1fr) !important;
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

    function isLikelyTextKey(key) {
      return /\.(txt|md|json|jsonc|js|jsx|ts|tsx|css|html|svg|xml|yml|yaml|sql|csv|toml|env|log)$/i.test(key);
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
              },
              {
                key: "gemini",
                displayName: "Gemini",
                secretName: "GEMINI_API_KEY",
                status: env.GEMINI_API_KEY ? "configured" : "missing_secret",
                models: ["gemini-pro", "gemini-flash"]
              }
            ],
            blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
          });
        }

        if (pathname === "/api/github/status") {
          return json({
            ok: true,
            configured: Boolean(env.GITHUB_CLIENT_ID || env.GITHUB_APP_ID),
            oauthConfigured: Boolean(env.GITHUB_CLIENT_ID && env.GITHUB_CLIENT_SECRET),
            appConfigured: Boolean(env.GITHUB_APP_ID && env.GITHUB_APP_PRIVATE_KEY),
            requiredSecrets: [
              "GITHUB_CLIENT_ID",
              "GITHUB_CLIENT_SECRET",
              "GITHUB_APP_ID",
              "GITHUB_APP_PRIVATE_KEY",
              "GITHUB_WEBHOOK_SECRET"
            ]
          });
        }

        if (pathname === "/api/oauth/github/start") {
          if (!env.GITHUB_CLIENT_ID) {
            return json({
              ok: false,
              error: "GitHub OAuth is not configured yet.",
              requiredSecret: "GITHUB_CLIENT_ID"
            }, 501);
          }

          const redirect = new URL("https://github.com/login/oauth/authorize");
          redirect.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
          redirect.searchParams.set("redirect_uri", `${url.origin}/api/oauth/github/callback`);
          redirect.searchParams.set("scope", "repo read:user user:email");
          redirect.searchParams.set("state", crypto.randomUUID());
          return Response.redirect(redirect.toString(), 302);
        }

        if (pathname === "/api/oauth/google/start") {
          if (!env.GOOGLE_CLIENT_ID) {
            return json({
              ok: false,
              error: "Google OAuth is not configured yet.",
              requiredSecret: "GOOGLE_CLIENT_ID"
            }, 501);
          }

          const redirect = new URL("https://accounts.google.com/o/oauth2/v2/auth");
          redirect.searchParams.set("client_id", env.GOOGLE_CLIENT_ID);
          redirect.searchParams.set("redirect_uri", env.GOOGLE_REDIRECT_URI || `${url.origin}/api/oauth/google/callback`);
          redirect.searchParams.set("response_type", "code");
          redirect.searchParams.set("scope", [
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.compose"
          ].join(" "));
          redirect.searchParams.set("access_type", "offline");
          redirect.searchParams.set("prompt", "consent");
          redirect.searchParams.set("state", crypto.randomUUID());
          return Response.redirect(redirect.toString(), 302);
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
            })),
            truncated: listed.truncated,
            cursor: listed.cursor || null
          });
        }

        if (pathname === "/api/r2/text") {
          if (!env.WEBSITE) return json({ ok: false, error: "WEBSITE R2 binding missing." }, 500);
          const key = url.searchParams.get("key") || "";
          if (!key) return json({ ok: false, error: "Missing key." }, 400);
          if (!isLikelyTextKey(key)) {
            return json({
              ok: false,
              error: "This object does not look like a text/code file.",
              key
            }, 415);
          }

          const object = await env.WEBSITE.get(key);
          if (!object) return json({ ok: false, error: "Object not found.", key }, 404);

          const text = await object.text();
          return json({
            ok: true,
            key,
            size: object.size,
            uploaded: object.uploaded,
            httpEtag: object.httpEtag,
            text
          });
        }

        if (pathname.startsWith("/api/r2/object/")) {
          if (!env.WEBSITE) return json({ ok: false, error: "WEBSITE R2 binding missing." }, 500);
          const key = decodeURIComponent(pathname.replace("/api/r2/object/", ""));
          const object = await env.WEBSITE.get(key);
          if (!object) return json({ ok: false, error: "R2 object not found", key }, 404);
          const headers = new Headers();
          object.writeHttpMetadata(headers);
          headers.set("etag", object.httpEtag);
          headers.set("cache-control", "public, max-age=300");
          return new Response(object.body, { headers });
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

    write("docs/FLEXFIT_DASHBOARD_ROUTES.md", r'''
    # Flexfit Dashboard Routes

    The dashboard now supports routed IDE views:

    ```txt
    /dashboard
    /dashboard/agent
    /dashboard/storage
    /dashboard/settings
    /dashboard/analytics
    /dashboard/learn
    /dashboard/mail
    /dashboard/mcp
    ```

    ## Added Capabilities

    ```txt
    Resizable explorer width
    Resizable agent panel width
    Resizable terminal height
    Real R2 object listing
    Text/code R2 object open into Monaco
    GitHub status endpoint
    GitHub OAuth start placeholder
    Google OAuth start placeholder
    View-specific dashboard panels
    Route-aware activity rail
    ```

    ## Real R2 Access

    The dashboard calls:

    ```txt
    GET /api/r2/list?prefix=
    GET /api/r2/text?key=<r2-key>
    GET /api/r2/object/<r2-key>
    ```

    Text-like files open into Monaco.

    Binary files should be previewed/downloaded through `/api/r2/object/`.

    ## GitHub

    Prepared routes:

    ```txt
    GET /api/github/status
    GET /api/oauth/github/start
    ```

    Required secrets:

    ```txt
    GITHUB_CLIENT_ID
    GITHUB_CLIENT_SECRET
    GITHUB_APP_ID
    GITHUB_APP_PRIVATE_KEY
    GITHUB_WEBHOOK_SECRET
    ```

    ## Google Drive / Gmail

    Prepared route:

    ```txt
    GET /api/oauth/google/start
    ```

    Required secrets:

    ```txt
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
    GOOGLE_REDIRECT_URI
    ```

    ## Next Implementation Layer

    ```txt
    GitHub file tree
    GitHub file read into Monaco
    GitHub branch save
    GitHub PR creation
    R2 upload from Monaco
    R2 binary preview drawer
    D1 CMS read/write panels
    Gmail drafts
    Drive file import
    MCP tool execution log
    ```
    ''')

    run(["npm", "run", "build"], check=True)
    run(["git", "add", "src/dashboard/DashboardApp.jsx", "src/dashboard/data/agentIdeFiles.js", "src/dashboard/pages/AgentIDE.jsx", "src/dashboard/dashboard.css", "src/worker/index.js", "docs/FLEXFIT_DASHBOARD_ROUTES.md"], check=True)
    run(["git", "commit", "-m", "feat: add flexfit dashboard routes and real R2 Monaco access"], check=False)

    print("\nFlexfit dashboard upgrade complete.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")
    print("Open:")
    print("https://leadership-legacy.meauxbility.workers.dev/dashboard")
    print("https://leadership-legacy.meauxbility.workers.dev/dashboard/storage")
    print("https://leadership-legacy.meauxbility.workers.dev/dashboard/mcp")

if __name__ == "__main__":
    main()
