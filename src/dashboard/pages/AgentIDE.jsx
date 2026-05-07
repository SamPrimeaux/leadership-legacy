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
