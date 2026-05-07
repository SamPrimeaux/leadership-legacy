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
            <Route path="*" element={<AgentIDE routeView="home" />} />
          </Routes>
        </DashboardAuthGate>
      );
    }
    ''')

    write("src/dashboard/data/dashboardPages.js", r'''
    import {
      Activity,
      Bot,
      Cloud,
      Code2,
      Database,
      FileText,
      GitBranch,
      GraduationCap,
      HardDrive,
      Inbox,
      KeyRound,
      Mail,
      Rocket,
      Server,
      Settings,
      ShieldCheck,
      Sparkles,
      TestTube2,
      Wrench
    } from "lucide-react";

    export const dashboardPageConfig = {
      home: {
        eyebrow: "Command Center",
        title: "Leadership Legacy operating system",
        body: "A focused cockpit for Connor to learn, build, test, deploy, and connect the tools behind Leadership Legacy Digital.",
        primaryAction: "Open Agent IDE",
        primaryHref: "/dashboard/agent",
        secondaryAction: "Review playbook",
        secondaryHref: "/dashboard/learn",
        cards: [
          { icon: Bot, label: "Agent IDE", value: "OpenAI live", body: "Use Monaco and Agent Connor for guided code work." },
          { icon: HardDrive, label: "R2 Storage", value: "Connected", body: "Browse real R2 files and open text/code assets." },
          { icon: Wrench, label: "MCP Tools", value: "Prepared", body: "Tool registry, approval gates, and execution logs." },
          { icon: TestTube2, label: "Playwright", value: "Ready", body: "Run smoke tests before deploys." }
        ],
        timeline: [
          "Confirm OpenAI model route and key shape",
          "Connect Connor GitHub OAuth/App",
          "Connect Google Drive and Gmail OAuth",
          "Wire real CMS writes through D1",
          "Add approval-gated GitHub save and PR creation"
        ]
      },
      storage: {
        eyebrow: "Storage",
        title: "R2 assets and snapshots",
        body: "Browse the real leadership-legacy R2 bucket, open text/code objects into Monaco, and prepare uploads, previews, and CMS asset mapping.",
        primaryAction: "Refresh R2",
        primaryActionType: "r2-refresh",
        secondaryAction: "Open Agent",
        secondaryHref: "/dashboard/agent",
        cards: [
          { icon: HardDrive, label: "Bucket", value: "leadership-legacy", body: "Primary object storage for assets, docs, exports, and snapshots." },
          { icon: FileText, label: "Text assets", value: "Monaco-ready", body: "Open code, JSON, markdown, SQL, CSS, and HTML into the editor." },
          { icon: Cloud, label: "Public assets", value: "R2-backed", body: "Use public object routes for previews and downloads." },
          { icon: Database, label: "CMS mapping", value: "Next", body: "Map assets to CMS records and section schemas." }
        ]
      },
      settings: {
        eyebrow: "Settings",
        title: "Integrations and provider readiness",
        body: "Track the secrets, OAuth apps, provider accounts, and Cloudflare resources Connor needs to fully own the platform.",
        primaryAction: "Check providers",
        primaryActionType: "provider-check",
        secondaryAction: "Study guide",
        secondaryHref: "/dashboard/learn",
        cards: [
          { icon: KeyRound, label: "OpenAI", value: "Configured", body: "Server-side Worker secret. Never exposed to the browser." },
          { icon: Sparkles, label: "Anthropic", value: "Pending", body: "Add Connor's Anthropic key when ready." },
          { icon: GitBranch, label: "GitHub", value: "OAuth/App", body: "Prepare repo browsing, branches, commits, and PRs." },
          { icon: Mail, label: "Google", value: "Drive/Gmail", body: "OAuth-driven Drive import and Gmail drafts." },
          { icon: Server, label: "Supabase", value: "Planned", body: "Analytics, RAG, evals, and codebase indexing." },
          { icon: Cloud, label: "Cloudflare", value: "Live", body: "Worker, R2, D1, KV, DO, and Workers AI." }
        ]
      },
      analytics: {
        eyebrow: "Analytics",
        title: "Telemetry and quality signals",
        body: "Track what matters: user activity, R2 access, lead flow, agent runs, model costs, tool calls, errors, and deploy health.",
        primaryAction: "Open tests",
        primaryHref: "/dashboard/learn",
        secondaryAction: "Review tools",
        secondaryHref: "/dashboard/mcp",
        cards: [
          { icon: Activity, label: "Views", value: "2,188", body: "Seed analytics until live event tracking is connected." },
          { icon: Inbox, label: "Leads", value: "1", body: "Project intake queue placeholder." },
          { icon: Bot, label: "Agent runs", value: "Live", body: "OpenAI calls are routed through Worker." },
          { icon: TestTube2, label: "E2E tests", value: "Playwright", body: "Smoke tests for public site and dashboard auth." }
        ]
      },
      learn: {
        eyebrow: "Learning Center",
        title: "Connor setup course",
        body: "A guided course for Connor to learn PowerShell, Cloudflare, GitHub, Google OAuth, AI provider routing, R2, D1, Supabase, MCP tools, and deploy discipline.",
        primaryAction: "Open rubric",
        primaryHref: "/dashboard/mcp",
        secondaryAction: "Open Agent",
        secondaryHref: "/dashboard/agent",
        modules: [
          "Run locally with PowerShell",
          "Understand source vs build output",
          "Deploy with Wrangler",
          "Read and open R2 assets",
          "Use Monaco safely",
          "Ask Agent Connor for code edits",
          "Connect GitHub OAuth/App",
          "Connect Google Drive and Gmail",
          "Add Anthropic and Gemini keys",
          "Run Playwright before deploys",
          "Use the readiness rubric"
        ]
      },
      mail: {
        eyebrow: "Mail",
        title: "Gmail and Resend workflows",
        body: "Prepare lead communication, Gmail drafts, Resend notifications, and approval-gated outbound messages.",
        primaryAction: "Connect Google",
        primaryHref: "/api/oauth/google/start",
        secondaryAction: "Open settings",
        secondaryHref: "/dashboard/settings",
        cards: [
          { icon: Mail, label: "Gmail", value: "OAuth", body: "Read threads and create drafts after user approval." },
          { icon: Inbox, label: "Lead inbox", value: "Planned", body: "Central queue for project inquiries and followups." },
          { icon: Rocket, label: "Resend", value: "Transactional", body: "Contact notifications, confirmations, and admin emails." },
          { icon: ShieldCheck, label: "Approval", value: "Required", body: "No autonomous sending without explicit review." }
        ]
      },
      mcp: {
        eyebrow: "MCP Tools",
        title: "Tool registry and execution layer",
        body: "A governed tool system for repo operations, R2, D1, Supabase, Drive, Gmail, OpenAI, Anthropic, Gemini, Resend, Playwright, and CAD workflows.",
        primaryAction: "Review settings",
        primaryHref: "/dashboard/settings",
        secondaryAction: "Open Agent",
        secondaryHref: "/dashboard/agent",
        tools: [
          { key: "github.listRepos", risk: "low", status: "planned" },
          { key: "github.getFile", risk: "low", status: "planned" },
          { key: "github.commitFile", risk: "approval", status: "planned" },
          { key: "r2.listObjects", risk: "low", status: "live" },
          { key: "r2.getTextObject", risk: "low", status: "live" },
          { key: "d1.query", risk: "approval", status: "planned" },
          { key: "openai.codeAction", risk: "medium", status: "live" },
          { key: "anthropic.review", risk: "medium", status: "pending key" },
          { key: "gmail.createDraft", risk: "approval", status: "planned" },
          { key: "drive.importFile", risk: "medium", status: "planned" },
          { key: "playwright.runSmoke", risk: "low", status: "ready" },
          { key: "resend.sendEmail", risk: "approval", status: "planned" }
        ]
      },
      cms: {
        eyebrow: "CMS",
        title: "Pages, sections, and publishing",
        body: "The CMS layer should manage page routes, section schemas, services, case studies, resources, SEO, navigation, assets, and publish snapshots.",
        primaryAction: "Open storage",
        primaryHref: "/dashboard/storage",
        secondaryAction: "Open Agent",
        secondaryHref: "/dashboard/agent",
        cards: [
          { icon: FileText, label: "Pages", value: "D1 runtime", body: "Draft and published page JSON." },
          { icon: Code2, label: "Sections", value: "Schema-driven", body: "Reusable content blocks." },
          { icon: HardDrive, label: "Assets", value: "R2-backed", body: "Media, models, downloads, and snapshots." },
          { icon: Rocket, label: "Publishing", value: "Snapshot flow", body: "Review, build, test, deploy." }
        ]
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
      Mail,
      MoreHorizontal,
      RefreshCcw,
      Search,
      Send,
      Settings,
      Sparkles,
      TerminalSquare,
      Upload,
      Wrench,
      X
    } from "lucide-react";
    import { dashboardPageConfig } from "../data/dashboardPages.js";
    import { commandPresets, localTree, workspaceFiles } from "../data/agentIdeFiles.js";

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
      const [terminalHeight, setTerminalHeight] = useState(() => Number(localStorage.getItem("ll-terminal-height") || 250));

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
            const next = clamp(startExplorer + event.clientX - startX, 190, 440);
            setExplorerWidth(next);
            localStorage.setItem("ll-explorer-width", String(next));
          }

          if (type === "agent") {
            // Natural behavior:
            // drag divider left -> agent gets wider
            // drag divider right -> agent gets narrower
            const next = clamp(startAgent + (startX - event.clientX), 280, 620);
            setAgentWidth(next);
            localStorage.setItem("ll-agent-width", String(next));
          }

          if (type === "terminal") {
            // Natural behavior:
            // drag divider up -> terminal gets taller
            // drag divider down -> terminal gets shorter
            const next = clamp(startTerminal + (startY - event.clientY), 150, 540);
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

      return { explorerWidth, agentWidth, terminalHeight, beginDrag };
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

    function Explorer({ files, activeFile, setActiveFile, r2Objects, loadR2Objects, openR2Object, r2Loading, githubStatus }) {
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
      const config = dashboardPageConfig[routeView] || dashboardPageConfig.agent || dashboardPageConfig.home;

      return (
        <header className="ia-topbar">
          <div className="ia-search">
            <Search size={14} />
            <input placeholder={`workspace: Leadership Legacy / ${config.eyebrow}`} aria-label="Workspace search" />
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

    function EditorTabs({ activeFile, file }) {
      return (
        <div className="ia-tabs">
          <button className="active">
            <FileCode2 size={14} />
            <span>{activeFile.split("/").pop()}</span>
            <X size={13} />
          </button>
          <a href="/dashboard/storage"><HardDrive size={14} /><span>Storage</span></a>
          <a href="/dashboard/mcp"><Wrench size={14} /><span>MCP</span></a>
          <a href="/dashboard/learn"><GraduationCap size={14} /><span>Learn</span></a>
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

    function DashboardPage({ routeView, r2Objects, loadR2Objects, openR2Object, providerStatus }) {
      const config = dashboardPageConfig[routeView] || dashboardPageConfig.home;

      function handlePrimary() {
        if (config.primaryActionType === "r2-refresh") {
          loadR2Objects("");
        }
        if (config.primaryActionType === "provider-check") {
          window.location.reload();
        }
      }

      return (
        <section className={`ia-page ia-page-${routeView}`}>
          <div className="ia-page-hero">
            <p className="ia-view-kicker">{config.eyebrow}</p>
            <h1>{config.title}</h1>
            <p>{config.body}</p>

            <div className="ia-page-actions">
              {config.primaryHref ? (
                <a className="ia-primary-link" href={config.primaryHref}>{config.primaryAction}</a>
              ) : (
                <button className="ia-primary-link" onClick={handlePrimary}>{config.primaryAction}</button>
              )}
              {config.secondaryHref ? (
                <a className="ia-secondary-link" href={config.secondaryHref}>{config.secondaryAction}</a>
              ) : null}
            </div>
          </div>

          {config.cards ? (
            <div className="ia-card-grid">
              {config.cards.map((card) => {
                const Icon = card.icon;
                let value = card.value;
                if (card.label === "OpenAI") value = providerStatus?.openaiConfigured ? "Configured" : "Missing";
                return (
                  <article key={card.label} className="ia-dashboard-card">
                    <Icon size={18} />
                    <span>{card.label}</span>
                    <strong>{value}</strong>
                    <p>{card.body}</p>
                  </article>
                );
              })}
            </div>
          ) : null}

          {routeView === "storage" ? (
            <div className="ia-storage-browser">
              <div className="ia-toolbar">
                <button onClick={() => loadR2Objects("")}><RefreshCcw size={14} /> Root</button>
                <button onClick={() => loadR2Objects("cms/")}><Database size={14} /> cms/</button>
                <button onClick={() => loadR2Objects("assets/")}><Image size={14} /> assets/</button>
                <button onClick={() => loadR2Objects("snapshots/")}><HardDrive size={14} /> snapshots/</button>
              </div>

              <div className="ia-object-table">
                {r2Objects.map((object) => (
                  <button key={object.key} onClick={() => openR2Object(object.key)}>
                    <span>{object.key}</span>
                    <small>{object.size ? `${object.size} bytes` : "object"}</small>
                  </button>
                ))}
              </div>
            </div>
          ) : null}

          {config.modules ? (
            <div className="ia-learning-list">
              {config.modules.map((item, index) => (
                <label key={item}>
                  <input type="checkbox" />
                  <span>{index + 1}. {item}</span>
                </label>
              ))}
            </div>
          ) : null}

          {config.tools ? (
            <div className="ia-tool-grid">
              {config.tools.map((tool) => (
                <article key={tool.key}>
                  <Wrench size={15} />
                  <strong>{tool.key}</strong>
                  <span>{tool.status}</span>
                  <code>{tool.risk}</code>
                </article>
              ))}
            </div>
          ) : null}

          {config.timeline ? (
            <div className="ia-timeline">
              {config.timeline.map((item, index) => (
                <article key={item}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <p>{item}</p>
                </article>
              ))}
            </div>
          ) : null}
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

    export function AgentIDE({ initialTerminalOpen = false, routeView = "home" }) {
      const [files, setFiles] = useState(workspaceFiles);
      const [activeFile, setActiveFile] = useState("worker/index.js");
      const [terminalOpen, setTerminalOpen] = useState(initialTerminalOpen);
      const [r2Objects, setR2Objects] = useState([]);
      const [r2Loading, setR2Loading] = useState(false);
      const [providerStatus, setProviderStatus] = useState(null);
      const [githubStatus, setGithubStatus] = useState(null);

      const { explorerWidth, agentWidth, terminalHeight, beginDrag } = useResizablePanels();

      const file = useMemo(() => files[activeFile] || Object.values(files)[0], [files, activeFile]);
      const isAgentRoute = routeView === "agent";

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
        const objectFile = `r2/${key}`;

        setFiles((current) => ({
          ...current,
          [objectFile]: {
            language: data.ok ? getLanguageFromKey(key) : "plaintext",
            type: "R2",
            source: "r2",
            content: data.ok ? data.text : `Unable to open ${key}\n\n${data.error || "Object may be binary or unavailable."}`
          }
        }));

        setActiveFile(objectFile);
      }

      useEffect(() => {
        loadR2Objects("");
        fetch("/api/ai/providers").then((res) => res.json()).then(setProviderStatus).catch(() => {});
        fetch("/api/github/status").then((res) => res.json()).then(setGithubStatus).catch(() => {});
      }, []);

      const gridStyle = {
        gridTemplateColumns: `48px ${explorerWidth}px minmax(0, 1fr)`
      };

      const mainStyle = {
        gridTemplateColumns: isAgentRoute ? `minmax(0, 1fr) ${agentWidth}px` : `minmax(0, 1fr) ${agentWidth}px`
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

            <div className={isAgentRoute ? "ia-main-grid" : "ia-main-grid page-mode"} style={mainStyle}>
              <div className="ia-center">
                {isAgentRoute ? (
                  <>
                    <CodeEditor activeFile={activeFile} file={file} updateFile={updateFile} />
                    <TerminalDock open={terminalOpen} height={terminalHeight} beginDrag={beginDrag} />
                  </>
                ) : (
                  <DashboardPage
                    routeView={routeView}
                    r2Objects={r2Objects}
                    loadR2Objects={loadR2Objects}
                    openR2Object={openR2Object}
                    providerStatus={providerStatus}
                  />
                )}
              </div>

              <div className="ia-resizer ia-resizer-agent" onMouseDown={(event) => beginDrag("agent", event)} />
              <AgentPanel activeFile={activeFile} file={file} updateFile={updateFile} />
            </div>

            <StatusBar activeFile={activeFile} r2Objects={r2Objects} />
          </main>
        </div>
      );
    }
    ''')

    css_path = ROOT / "src/dashboard/dashboard.css"
    css = css_path.read_text()

    # Direction fix already handled in JS. Now improve page mode.
    css += r'''

    /* Real dashboard pages: do not let Monaco dominate every route */
    .ia-main-grid.page-mode .ia-center {
      display: block;
      overflow: auto;
      border-right: 1px solid rgba(69, 228, 238, 0.18);
      background: #041316;
    }

    .ia-page {
      min-height: 100%;
      overflow: auto;
      padding: clamp(22px, 4vw, 44px);
      background:
        radial-gradient(circle at 16% 0%, rgba(32, 227, 240, 0.13), transparent 28rem),
        radial-gradient(circle at 84% 12%, rgba(83, 244, 207, 0.07), transparent 22rem),
        linear-gradient(135deg, #041316 0%, #051b1f 48%, #031013 100%);
    }

    .ia-page-hero {
      max-width: 920px;
      margin-bottom: 24px;
    }

    .ia-page-hero h1 {
      margin: 0 0 14px;
      color: #f3feff;
      font-size: clamp(2.8rem, 7vw, 7rem);
      line-height: 0.86;
      letter-spacing: -0.085em;
    }

    .ia-page-hero p {
      max-width: 760px;
      color: #a9e3e8;
      line-height: 1.7;
      font-size: clamp(0.94rem, 1.6vw, 1.1rem);
    }

    .ia-page-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
    }

    .ia-primary-link,
    .ia-secondary-link {
      min-height: 38px;
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 0 14px;
      font-weight: 950;
      font-size: 0.82rem;
      border: 1px solid rgba(69, 228, 238, 0.22);
    }

    .ia-primary-link {
      color: #031013;
      background: linear-gradient(135deg, #20e3f0, #53f4cf);
    }

    .ia-secondary-link {
      color: #d9fbff;
      background: rgba(69, 228, 238, 0.08);
    }

    .ia-card-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }

    .ia-dashboard-card {
      min-width: 0;
      min-height: 164px;
      display: grid;
      align-content: start;
      gap: 8px;
      border: 1px solid rgba(69, 228, 238, 0.15);
      border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(10, 89, 97, 0.22), rgba(3, 16, 19, 0.46));
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 24px 70px rgba(0, 0, 0, 0.18);
      padding: 16px;
    }

    .ia-dashboard-card svg {
      color: #20e3f0;
    }

    .ia-dashboard-card span {
      color: #86d4dc;
      font-size: 0.72rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-weight: 900;
    }

    .ia-dashboard-card strong {
      color: #f3feff;
      font-size: 1.35rem;
      letter-spacing: -0.04em;
    }

    .ia-dashboard-card p {
      margin: 0;
      color: #92cfd6;
      line-height: 1.55;
      font-size: 0.82rem;
    }

    .ia-timeline {
      display: grid;
      gap: 10px;
      max-width: 900px;
    }

    .ia-timeline article {
      display: grid;
      grid-template-columns: 44px minmax(0, 1fr);
      gap: 12px;
      align-items: center;
      border: 1px solid rgba(69, 228, 238, 0.13);
      border-radius: 14px;
      background: rgba(3, 16, 19, 0.36);
      padding: 12px;
    }

    .ia-timeline span {
      color: #20e3f0;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-weight: 950;
    }

    .ia-timeline p {
      margin: 0;
      color: #c8f8fc;
    }

    .ia-storage-browser {
      margin-top: 22px;
    }

    .ia-learning-list {
      max-width: 980px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-top: 20px;
    }

    .ia-learning-list label {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      border: 1px solid rgba(69, 228, 238, 0.13);
      border-radius: 14px;
      background: rgba(3, 16, 19, 0.4);
      padding: 12px;
      color: #c8f8fc;
      line-height: 1.5;
    }

    .ia-tool-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }

    .ia-tool-grid article {
      display: grid;
      gap: 7px;
      border: 1px solid rgba(69, 228, 238, 0.13);
      border-radius: 15px;
      background: rgba(3, 16, 19, 0.4);
      padding: 14px;
    }

    .ia-tool-grid strong {
      color: #f3feff;
      font-size: 0.9rem;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .ia-tool-grid span {
      color: #8fc8cf;
      font-size: 0.78rem;
    }

    .ia-tool-grid code {
      color: #20e3f0;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.72rem;
    }

    @media (max-width: 1240px) {
      .ia-card-grid,
      .ia-tool-grid,
      .ia-learning-list {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 760px) {
      .ia-card-grid,
      .ia-tool-grid,
      .ia-learning-list {
        grid-template-columns: 1fr;
      }

      .ia-page {
        padding: 24px;
      }
    }
    '''

    css_path.write_text(css)

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

    function cleanOpenAIKey(value) {
      if (!value) return "";
      let key = String(value).trim();

      if (key.startsWith("OPENAI_API_KEY=")) {
        key = key.replace(/^OPENAI_API_KEY=/, "").trim();
      }

      key = key.replace(/^["']|["']$/g, "").trim();
      return key;
    }

    function keyShape(value) {
      const raw = String(value || "");
      const cleaned = cleanOpenAIKey(raw);
      return {
        exists: Boolean(raw),
        rawLength: raw.length,
        cleanedLength: cleaned.length,
        startsWithEnvName: raw.trim().startsWith("OPENAI_API_KEY="),
        hasQuotes: /^["']|["']$/.test(raw.trim()),
        prefix: cleaned.slice(0, 7),
        suffix: cleaned.slice(-4)
      };
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
      const apiKey = cleanOpenAIKey(env.OPENAI_API_KEY);

      if (!apiKey) {
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
          authorization: `Bearer ${apiKey}`
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
            openaiConfigured: Boolean(cleanOpenAIKey(env.OPENAI_API_KEY)),
            r2Binding: Boolean(env.WEBSITE),
            timestamp: new Date().toISOString()
          });
        }

        if (pathname === "/api/openai/diagnostics") {
          return json({
            ok: true,
            openaiKey: keyShape(env.OPENAI_API_KEY),
            defaultModel: env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini",
            note: "This endpoint intentionally exposes only key shape, never the full key."
          });
        }

        if (pathname === "/api/openai/test") {
          const model = url.searchParams.get("model") || env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini";
          const result = await callOpenAI(env, {
            model,
            instructions: "Reply with exactly: ok",
            input: "health check",
            max_output_tokens: 20
          });

          if (!result.ok) {
            return json(result, result.status || 500);
          }

          return json({
            ok: true,
            model,
            text: result.text,
            responseId: result.data?.id || null,
            usage: result.data?.usage || null
          });
        }

        if (pathname === "/api/ai/providers") {
          return json({
            ok: true,
            openaiConfigured: Boolean(cleanOpenAIKey(env.OPENAI_API_KEY)),
            providers: [
              {
                key: "openai",
                displayName: "OpenAI",
                secretName: "OPENAI_API_KEY",
                status: cleanOpenAIKey(env.OPENAI_API_KEY) ? "configured" : "missing_secret",
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
          const model = body.model || env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini";
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
            return json({ ok: false, binding: "WEBSITE", error: error.message }, 500);
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
            return json({ ok: false, error: "This object does not look like a text/code file.", key }, 415);
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

    write("docs/DASHBOARD_PAGES_AND_OPENAI_FIX.md", r'''
    # Dashboard Pages and OpenAI Fix

    This update fixes three issues.

    ## 1. OpenAI Key Diagnostics

    Added:

    ```txt
    GET /api/openai/diagnostics
    GET /api/openai/test
    ```

    Diagnostics show only key shape, never the full key.

    This helps catch the common mistake of setting the Worker secret as:

    ```txt
    OPENAI_API_KEY=sk-...
    ```

    Instead of only:

    ```txt
    sk-...
    ```

    ## 2. Flexfit Drag Direction

    The right panel drag math is now natural:

    ```txt
    drag left = agent panel expands
    drag right = agent panel shrinks
    drag terminal divider up = terminal expands
    drag terminal divider down = terminal shrinks
    ```

    ## 3. True Dashboard Pages

    Monaco is now reserved for:

    ```txt
    /dashboard/agent
    /dashboard/dev
    /dashboard/dev/editor
    /dashboard/dev/terminal
    ```

    Designed dashboard pages now render for:

    ```txt
    /dashboard
    /dashboard/storage
    /dashboard/settings
    /dashboard/analytics
    /dashboard/learn
    /dashboard/mail
    /dashboard/mcp
    ```

    This keeps the interface Cursor-like, but gives Connor actual places to learn, monitor, configure, and operate.
    ''')

    run(["npm", "run", "build"], check=True)
    run(["git", "add", "src/dashboard/DashboardApp.jsx", "src/dashboard/data/dashboardPages.js", "src/dashboard/pages/AgentIDE.jsx", "src/dashboard/dashboard.css", "src/worker/index.js", "docs/DASHBOARD_PAGES_AND_OPENAI_FIX.md"], check=True)
    run(["git", "commit", "-m", "feat: add designed dashboard pages and fix OpenAI diagnostics flex drag"], check=False)

    print("\nDashboard page/drag/OpenAI diagnostic update complete.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")
    print("Then run:")
    print("curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/diagnostics")
    print("curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/test")

if __name__ == "__main__":
    main()
