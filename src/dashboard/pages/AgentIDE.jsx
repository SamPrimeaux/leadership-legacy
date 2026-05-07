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
          <GitBranch size={15} />
          <span>GITHUB SYNC</span>
          <ChevronDown size={14} />
        </button>
        {githubOpen ? (
          <div className="ia-service-card">
            <div className="ia-orb"><GitBranch size={44} /></div>
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
