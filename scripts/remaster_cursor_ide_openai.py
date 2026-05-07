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
    deps["monaco-editor"] = deps.get("monaco-editor", "latest")
    deps["@xterm/xterm"] = deps.get("@xterm/xterm", "latest")
    deps["@xterm/addon-fit"] = deps.get("@xterm/addon-fit", "latest")
    deps["lucide-react"] = deps.get("lucide-react", "latest")
    scripts = pkg.setdefault("scripts", {})
    scripts["dev"] = "vite"
    scripts["build"] = "vite build"
    scripts["deploy"] = "npm run build && wrangler deploy"
    path.write_text(json.dumps(pkg, indent=2) + "\n")
    print("patched package.json")

def main():
    patch_package()

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

      return chunks.join("\\n").trim();
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
          "authorization": `Bearer ${env.OPENAI_API_KEY}`
        },
        body: JSON.stringify(payload)
      });

      const text = await response.text();
      let data;

      try {
        data = JSON.parse(text);
      } catch {
        data = { raw: text };
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

    function stripCodeFence(text) {
      if (!text) return "";
      return text
        .replace(/^```[a-zA-Z0-9_-]*\\s*/.trim(), "")
        .replace(/^```[a-zA-Z0-9_-]*\\s*/, "")
        .replace(/```\\s*$/, "")
        .trim();
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

        if (pathname === "/api/r2/status") {
          let readme = null;
          try {
            readme = await readR2Text(env, "README.txt");
          } catch (error) {
            return json({
              ok: false,
              binding: "WEBSITE",
              bucket: env.R2_BUCKET_NAME || "leadership-legacy",
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
          const mode = body.mode || "generate";
          const filename = body.filename || "src/App.jsx";
          const language = body.language || "javascript";
          const currentCode = body.code || "";
          const instruction = body.instruction || "Improve this file.";
          const model = body.model || "gpt-5.4-mini";

          if (["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"].includes(model)) {
            return json({
              ok: false,
              error: "This model is blocked by project policy.",
              blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
            }, 400);
          }

          const developer = [
            "You are the Leadership Legacy dashboard coding agent.",
            "Return only the final complete file contents unless the user explicitly asks for explanation.",
            "Do not include markdown fences.",
            "Do not invent secrets.",
            "Do not expose API keys.",
            "Prefer production-ready React, Vite, Cloudflare Worker, and CMS dashboard patterns.",
            "Use accessible markup and clean Cursor-like UI conventions."
          ].join("\\n");

          const user = [
            `Mode: ${mode}`,
            `Filename: ${filename}`,
            `Language: ${language}`,
            "",
            "Instruction:",
            instruction,
            "",
            "Current file contents:",
            currentCode || "(empty file)"
          ].join("\\n");

          const result = await callOpenAI(env, {
            model,
            instructions: developer,
            input: user,
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
            mode,
            code: stripCodeFence(result.text),
            responseId: result.data?.id || null,
            usage: result.data?.usage || null
          });
        }

        if (pathname === "/api/openai/chat" && request.method === "POST") {
          const body = await readJson(request);
          const model = body.model || "gpt-5.4-mini";
          const message = body.message || "Explain this project.";

          if (["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"].includes(model)) {
            return json({ ok: false, error: "Blocked model by policy." }, 400);
          }

          const result = await callOpenAI(env, {
            model,
            instructions: "You are a concise project assistant for the Leadership Legacy Digital dashboard. Never reveal secrets.",
            input: message,
            max_output_tokens: 2500
          });

          if (!result.ok) return json(result, result.status || 500);

          return json({
            ok: true,
            model,
            text: result.text,
            responseId: result.data?.id || null,
            usage: result.data?.usage || null
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
    import { IDELayout } from "./layouts/IDELayout.jsx";
    import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
    import { IDEHome } from "./pages/IDEHome.jsx";
    import { IDEWorkspace } from "./pages/IDEWorkspace.jsx";
    import { CMSPages } from "./pages/CMSPages.jsx";
    import { CMSPageEditor } from "./pages/CMSPageEditor.jsx";
    import { MediaLibrary } from "./pages/MediaLibrary.jsx";
    import { R2Storage } from "./pages/R2Storage.jsx";
    import { CaseStudies } from "./pages/CaseStudies.jsx";
    import { Services } from "./pages/Services.jsx";
    import { Leads } from "./pages/Leads.jsx";
    import { IntakeForms } from "./pages/IntakeForms.jsx";
    import { Analytics } from "./pages/Analytics.jsx";
    import { Publishing } from "./pages/Publishing.jsx";
    import { Settings } from "./pages/Settings.jsx";
    import { AIProviders } from "./pages/AIProviders.jsx";
    import { NotFoundDashboard } from "./pages/NotFoundDashboard.jsx";

    export default function DashboardApp() {
      return (
        <DashboardAuthGate>
          <IDELayout>
            <Routes>
              <Route path="/dashboard" element={<IDEHome />} />
              <Route path="/dashboard/dev" element={<IDEWorkspace />} />
              <Route path="/dashboard/dev/editor" element={<IDEWorkspace startTab="editor" />} />
              <Route path="/dashboard/dev/terminal" element={<IDEWorkspace startTab="terminal" />} />
              <Route path="/dashboard/dev/agent" element={<IDEWorkspace startTab="agent" />} />
              <Route path="/dashboard/pages" element={<CMSPages />} />
              <Route path="/dashboard/pages/:pageId" element={<CMSPageEditor />} />
              <Route path="/dashboard/sections" element={<CMSPages />} />
              <Route path="/dashboard/media" element={<MediaLibrary />} />
              <Route path="/dashboard/storage" element={<R2Storage />} />
              <Route path="/dashboard/case-studies" element={<CaseStudies />} />
              <Route path="/dashboard/case-studies/:caseStudyId" element={<CaseStudies />} />
              <Route path="/dashboard/services" element={<Services />} />
              <Route path="/dashboard/services/:serviceId" element={<Services />} />
              <Route path="/dashboard/leads" element={<Leads />} />
              <Route path="/dashboard/leads/:leadId" element={<Leads />} />
              <Route path="/dashboard/forms" element={<IntakeForms />} />
              <Route path="/dashboard/analytics" element={<Analytics />} />
              <Route path="/dashboard/publishing" element={<Publishing />} />
              <Route path="/dashboard/settings" element={<Settings />} />
              <Route path="/dashboard/settings/brand" element={<Settings section="brand" />} />
              <Route path="/dashboard/settings/navigation" element={<Settings section="navigation" />} />
              <Route path="/dashboard/settings/seo" element={<Settings section="seo" />} />
              <Route path="/dashboard/settings/ai-providers" element={<AIProviders />} />
              <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
              <Route path="*" element={<NotFoundDashboard />} />
            </Routes>
          </IDELayout>
        </DashboardAuthGate>
      );
    }
    ''')

    write("src/dashboard/data/ideFiles.js", r'''
    export const initialFiles = {
      "src/worker/index.js": {
        language: "javascript",
        content: `export default {
      async fetch(request, env) {
        const url = new URL(request.url);

        if (url.pathname === "/api/health") {
          return Response.json({
            ok: true,
            app: "leadership-legacy"
          });
        }

        return new Response("Leadership Legacy Worker online");
      }
    };`
      },
      "src/dashboard/components/HeroPanel.jsx": {
        language: "javascript",
        content: `export function HeroPanel() {
      return (
        <section className="hero-panel">
          <p className="eyebrow">Mechanical Engineer × AI Developer</p>
          <h1>Engineering-grade AI systems for technical businesses.</h1>
          <p>
            Connor McNeely builds AI systems, RAG tools, CAD automations,
            and full-stack applications for technical teams.
          </p>
        </section>
      );
    }`
      },
      "wrangler.jsonc": {
        language: "json",
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
      },
      "README_TASK.md": {
        language: "markdown",
        content: `# Current Task

    Use the AI panel to generate or refactor files.

    Good prompts:

    - Build a polished CMS page editor component.
    - Add a Cloudflare Worker route for saving CMS drafts.
    - Generate a D1 query helper for cms_pages.
    - Improve accessibility and mobile behavior.
    - Create a RAG ingestion endpoint outline.`
      }
    };
    ''')

    write("src/dashboard/data/ideNav.js", r'''
    import {
      Home,
      Code2,
      TerminalSquare,
      Bot,
      FileText,
      Image,
      Database,
      Briefcase,
      Wrench,
      Inbox,
      BarChart3,
      Rocket,
      Settings,
      BrainCircuit
    } from "lucide-react";

    export const idePrimaryNav = [
      { label: "Home", href: "/dashboard", icon: Home },
      { label: "IDE Workspace", href: "/dashboard/dev", icon: Code2 },
      { label: "Terminal", href: "/dashboard/dev/terminal", icon: TerminalSquare },
      { label: "AI Agent", href: "/dashboard/dev/agent", icon: Bot }
    ];

    export const ideCMSNav = [
      { label: "Pages", href: "/dashboard/pages", icon: FileText },
      { label: "Media", href: "/dashboard/media", icon: Image },
      { label: "R2 Storage", href: "/dashboard/storage", icon: Database },
      { label: "Case Studies", href: "/dashboard/case-studies", icon: Briefcase },
      { label: "Services", href: "/dashboard/services", icon: Wrench },
      { label: "Leads", href: "/dashboard/leads", icon: Inbox },
      { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
      { label: "Publishing", href: "/dashboard/publishing", icon: Rocket },
      { label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },
      { label: "Settings", href: "/dashboard/settings", icon: Settings }
    ];
    ''')

    write("src/dashboard/layouts/IDELayout.jsx", r'''
    import { NavLink } from "react-router-dom";
    import { idePrimaryNav, ideCMSNav } from "../data/ideNav.js";
    import { Search, ExternalLink, PanelRight, GitBranch } from "lucide-react";

    function NavGroup({ title, items }) {
      return (
        <div className="ide-nav-group">
          <span>{title}</span>
          {items.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.href} to={item.href} end={item.href === "/dashboard"}>
                <Icon size={17} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      );
    }

    export function IDELayout({ children }) {
      return (
        <div className="ide-shell">
          <aside className="ide-activity">
            <div className="ide-logo">LL</div>
            <NavLink to="/dashboard/dev" title="IDE Workspace"><PanelRight size={20} /></NavLink>
            <NavLink to="/dashboard/dev/agent" title="AI Agent"><Search size={20} /></NavLink>
            <NavLink to="/dashboard/settings/ai-providers" title="Providers"><GitBranch size={20} /></NavLink>
          </aside>

          <aside className="ide-sidebar">
            <div className="ide-brand">
              <strong>Leadership Legacy</strong>
              <small>Cursor-style CMS IDE</small>
            </div>

            <NavGroup title="Workspace" items={idePrimaryNav} />
            <NavGroup title="CMS" items={ideCMSNav} />
          </aside>

          <div className="ide-main">
            <header className="ide-topbar">
              <div className="ide-command">
                <Search size={16} />
                <input placeholder="Search files, pages, leads, commands" aria-label="Search dashboard" />
              </div>

              <div className="ide-top-actions">
                <span className="ide-branch"><GitBranch size={14} /> main</span>
                <a href="/" target="_blank" rel="noreferrer">View site <ExternalLink size={14} /></a>
                <span className="ide-status">OpenAI ready</span>
              </div>
            </header>

            <main className="ide-content">
              {children}
            </main>
          </div>
        </div>
      );
    }
    ''')

    write("src/dashboard/components/ide/FileExplorer.jsx", r'''
    import { FileCode2, FolderOpen } from "lucide-react";

    export function FileExplorer({ files, activeFile, onSelect }) {
      return (
        <aside className="ide-file-explorer">
          <div className="ide-pane-title">
            <FolderOpen size={15} />
            <span>Explorer</span>
          </div>

          <div className="ide-file-tree">
            {Object.keys(files).map((file) => (
              <button
                key={file}
                className={file === activeFile ? "selected" : ""}
                onClick={() => onSelect(file)}
              >
                <FileCode2 size={15} />
                <span>{file}</span>
              </button>
            ))}
          </div>
        </aside>
      );
    }
    ''')

    write("src/dashboard/components/ide/MonacoWorkspace.jsx", r'''
    import Editor from "@monaco-editor/react";

    export function MonacoWorkspace({ activeFile, file, onChange }) {
      return (
        <section className="ide-editor">
          <div className="ide-editor-tabs">
            <span>{activeFile}</span>
            <small>{file.language}</small>
          </div>

          <div className="ide-monaco-frame">
            <Editor
              height="100%"
              language={file.language}
              theme="vs-dark"
              value={file.content}
              onChange={(value) => onChange(value || "")}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineHeight: 23,
                wordWrap: "on",
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 2,
                padding: { top: 16, bottom: 16 }
              }}
            />
          </div>
        </section>
      );
    }
    ''')

    write("src/dashboard/components/ide/AIAssistantPanel.jsx", r'''
    import { useState } from "react";
    import { Bot, WandSparkles, Loader2, Clipboard, Replace } from "lucide-react";

    const promptTemplates = [
      "Improve this file for production quality and accessibility.",
      "Generate a Cloudflare Worker endpoint for this feature.",
      "Refactor this into clean reusable React components.",
      "Add CMS data loading and error states.",
      "Make this more Cursor-style and polished.",
      "Explain this file for Connor in beginner-friendly terms."
    ];

    export function AIAssistantPanel({ activeFile, file, onReplace }) {
      const [instruction, setInstruction] = useState(promptTemplates[0]);
      const [model, setModel] = useState("gpt-5.4-mini");
      const [mode, setMode] = useState("refactor");
      const [loading, setLoading] = useState(false);
      const [result, setResult] = useState("");
      const [error, setError] = useState("");

      async function runAgent() {
        setLoading(true);
        setError("");
        setResult("");

        try {
          const response = await fetch("/api/openai/code", {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({
              mode,
              model,
              filename: activeFile,
              language: file.language,
              code: file.content,
              instruction
            })
          });

          const data = await response.json();

          if (!response.ok || !data.ok) {
            throw new Error(data.error || "OpenAI code action failed.");
          }

          setResult(data.code || "");
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      }

      async function copyResult() {
        if (result) await navigator.clipboard.writeText(result);
      }

      return (
        <aside className="ide-ai-panel">
          <div className="ide-pane-title">
            <Bot size={15} />
            <span>AI Code Agent</span>
          </div>

          <label>
            Model
            <select value={model} onChange={(event) => setModel(event.target.value)}>
              <option value="gpt-5.4-mini">gpt-5.4-mini</option>
              <option value="gpt-5.4-nano">gpt-5.4-nano</option>
              <option value="gpt-5.4">gpt-5.4</option>
            </select>
          </label>

          <label>
            Mode
            <select value={mode} onChange={(event) => setMode(event.target.value)}>
              <option value="refactor">Refactor current file</option>
              <option value="generate">Generate file</option>
              <option value="explain">Explain file</option>
              <option value="worker-route">Worker route</option>
              <option value="cms-component">CMS component</option>
            </select>
          </label>

          <label>
            Instruction
            <textarea
              value={instruction}
              onChange={(event) => setInstruction(event.target.value)}
              rows={7}
            />
          </label>

          <div className="prompt-chips">
            {promptTemplates.map((prompt) => (
              <button key={prompt} onClick={() => setInstruction(prompt)}>
                {prompt}
              </button>
            ))}
          </div>

          <button className="ide-run-button" onClick={runAgent} disabled={loading}>
            {loading ? <Loader2 className="spin" size={16} /> : <WandSparkles size={16} />}
            {loading ? "Generating" : "Run OpenAI"}
          </button>

          {error ? <div className="ide-error">{error}</div> : null}

          {result ? (
            <div className="ai-result">
              <div className="ai-result-actions">
                <strong>Generated output</strong>
                <button onClick={copyResult}><Clipboard size={14} /> Copy</button>
                <button onClick={() => onReplace(result)}><Replace size={14} /> Replace editor</button>
              </div>
              <pre>{result}</pre>
            </div>
          ) : (
            <p className="ide-muted">
              The OpenAI API key stays inside the Worker. Monaco sends file content to `/api/openai/code`,
              and the response can replace the active editor file.
            </p>
          )}
        </aside>
      );
    }
    ''')

    write("src/dashboard/components/ide/TerminalDock.jsx", r'''
    import { useEffect, useRef } from "react";
    import { Terminal } from "@xterm/xterm";
    import { FitAddon } from "@xterm/addon-fit";
    import { TerminalSquare, Copy } from "lucide-react";

    const commands = [
      "npm install",
      "npm run dev",
      "npm run build",
      "npm run deploy",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
      "curl https://leadership-legacy.meauxbility.workers.dev/api/ai/providers",
      "npx wrangler secret put OPENAI_API_KEY"
    ];

    export function TerminalDock() {
      const terminalEl = useRef(null);
      const terminalRef = useRef(null);

      useEffect(() => {
        if (!terminalEl.current || terminalRef.current) return;

        const term = new Terminal({
          cursorBlink: true,
          convertEol: true,
          fontFamily: "JetBrains Mono, Consolas, monospace",
          fontSize: 13,
          theme: {
            background: "#080b12",
            foreground: "#f8fafc",
            cursor: "#38bdf8"
          }
        });

        const fit = new FitAddon();
        term.loadAddon(fit);
        term.open(terminalEl.current);
        fit.fit();

        term.writeln("Leadership Legacy integrated terminal");
        term.writeln("PowerShell-friendly command guide");
        term.writeln("");
        term.writeln("This xterm panel is live in-browser. Command execution is intentionally prepped, not enabled.");
        term.writeln("Future: Dashboard → Worker → Durable Object → PTY tunnel.");
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
      }, []);

      async function copy(command) {
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
        <section className="ide-terminal-dock">
          <div className="ide-terminal-head">
            <span><TerminalSquare size={15} /> Terminal</span>
            <small>PowerShell presets</small>
          </div>

          <div className="terminal-command-strip">
            {commands.map((command) => (
              <button key={command} onClick={() => copy(command)}>
                <Copy size={13} />
                {command}
              </button>
            ))}
          </div>

          <div className="xterm-host" ref={terminalEl} />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/IDEWorkspace.jsx", r'''
    import { useMemo, useState } from "react";
    import { initialFiles } from "../data/ideFiles.js";
    import { FileExplorer } from "../components/ide/FileExplorer.jsx";
    import { MonacoWorkspace } from "../components/ide/MonacoWorkspace.jsx";
    import { AIAssistantPanel } from "../components/ide/AIAssistantPanel.jsx";
    import { TerminalDock } from "../components/ide/TerminalDock.jsx";

    export function IDEWorkspace({ startTab = "editor" }) {
      const [files, setFiles] = useState(initialFiles);
      const [activeFile, setActiveFile] = useState(Object.keys(initialFiles)[0]);
      const [bottomOpen, setBottomOpen] = useState(startTab === "terminal");

      const file = useMemo(() => files[activeFile], [files, activeFile]);

      function updateActiveFile(content) {
        setFiles((current) => ({
          ...current,
          [activeFile]: {
            ...current[activeFile],
            content
          }
        }));
      }

      return (
        <section className="ide-workspace-page">
          <div className="ide-workspace-title">
            <div>
              <p className="dash-eyebrow">IDE Workspace</p>
              <h1>Cursor-style build cockpit</h1>
            </div>
            <div className="workspace-actions">
              <button onClick={() => setBottomOpen((value) => !value)}>
                {bottomOpen ? "Hide terminal" : "Show terminal"}
              </button>
              <a href="/dashboard/settings/ai-providers">Provider settings</a>
            </div>
          </div>

          <div className="ide-workbench">
            <FileExplorer files={files} activeFile={activeFile} onSelect={setActiveFile} />
            <MonacoWorkspace activeFile={activeFile} file={file} onChange={updateActiveFile} />
            <AIAssistantPanel activeFile={activeFile} file={file} onReplace={updateActiveFile} />
          </div>

          {bottomOpen ? <TerminalDock /> : null}
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/IDEHome.jsx", r'''
    import { Link } from "react-router-dom";
    import { Code2, Bot, TerminalSquare, Database, Rocket } from "lucide-react";

    export function IDEHome() {
      const cards = [
        {
          title: "IDE Workspace",
          body: "Open Monaco, edit starter files, and use OpenAI to generate or refactor code.",
          href: "/dashboard/dev",
          icon: Code2
        },
        {
          title: "AI Code Agent",
          body: "Use the installed OPENAI_API_KEY through secure Worker endpoints.",
          href: "/dashboard/dev/agent",
          icon: Bot
        },
        {
          title: "Terminal Dock",
          body: "PowerShell-friendly command presets with xterm prepared for future PTY execution.",
          href: "/dashboard/dev/terminal",
          icon: TerminalSquare
        },
        {
          title: "R2 Storage",
          body: "Browse the leadership-legacy bucket and prepare CMS assets.",
          href: "/dashboard/storage",
          icon: Database
        },
        {
          title: "Publishing",
          body: "Prepare deploy, CMS publish, and snapshot workflows.",
          href: "/dashboard/publishing",
          icon: Rocket
        }
      ];

      return (
        <section>
          <p className="dash-eyebrow">Leadership Legacy IDE</p>
          <h1>Cursor-style CMS command center</h1>
          <p className="dash-subtitle">
            A full dashboard cockpit for Connor: Monaco editor, xterm terminal prep, OpenAI-powered file generation,
            CMS management, R2 storage, AI provider settings, analytics, and deployment workflows.
          </p>

          <div className="ide-home-grid">
            {cards.map((card) => {
              const Icon = card.icon;
              return (
                <Link className="ide-home-card" to={card.href} key={card.title}>
                  <Icon size={22} />
                  <h2>{card.title}</h2>
                  <p>{card.body}</p>
                </Link>
              );
            })}
          </div>

          <article className="ide-callout">
            <p className="dash-eyebrow">OpenAI status</p>
            <h2>Worker-backed AI actions are enabled</h2>
            <p>
              The browser never sees the API key. Monaco sends the selected file and instruction to
              <code>/api/openai/code</code>, the Worker calls OpenAI’s Responses API, and the generated code can be copied
              or applied back into the editor.
            </p>
          </article>
        </section>
      );
    }
    ''')

    write("src/dashboard/dashboard.css", r'''
    @import "../shared/brand/tokens.css";

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: #05070d;
      color: #f8fafc;
      font-family: Inter, system-ui, sans-serif;
      overflow-x: hidden;
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

    .ide-shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 54px 260px minmax(0, 1fr);
      background:
        radial-gradient(circle at 20% 0%, rgba(56, 189, 248, 0.12), transparent 26rem),
        radial-gradient(circle at 90% 0%, rgba(34, 197, 94, 0.06), transparent 22rem),
        #05070d;
    }

    .ide-activity {
      border-right: 1px solid #1d2433;
      background: #080b12;
      display: grid;
      align-content: start;
      justify-items: center;
      gap: 12px;
      padding: 12px 0;
    }

    .ide-logo {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      border-radius: 10px;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      color: #04111f;
      font-weight: 950;
      letter-spacing: -0.08em;
      margin-bottom: 12px;
    }

    .ide-activity a {
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      border-radius: 11px;
      color: #8a94a8;
    }

    .ide-activity a:hover,
    .ide-activity a.active {
      background: #121827;
      color: #f8fafc;
    }

    .ide-sidebar {
      border-right: 1px solid #1d2433;
      background: #0b1020;
      padding: 18px 12px;
      overflow-y: auto;
    }

    .ide-brand {
      padding: 0 8px 18px;
      border-bottom: 1px solid #1d2433;
      margin-bottom: 18px;
    }

    .ide-brand strong,
    .ide-brand small {
      display: block;
    }

    .ide-brand small {
      color: #8a94a8;
      margin-top: 2px;
    }

    .ide-nav-group {
      display: grid;
      gap: 5px;
      margin-bottom: 22px;
    }

    .ide-nav-group > span {
      padding: 0 8px;
      color: #586174;
      text-transform: uppercase;
      letter-spacing: 0.11em;
      font-size: 0.72rem;
      font-weight: 900;
      margin-bottom: 5px;
    }

    .ide-nav-group a {
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 36px;
      color: #9ca8bd;
      padding: 0 10px;
      border-radius: 10px;
      font-weight: 750;
      font-size: 0.92rem;
    }

    .ide-nav-group a:hover,
    .ide-nav-group a.active {
      color: #f8fafc;
      background: #111827;
      box-shadow: inset 0 0 0 1px #263247;
    }

    .ide-main {
      min-width: 0;
      display: grid;
      grid-template-rows: 58px minmax(0, 1fr);
    }

    .ide-topbar {
      border-bottom: 1px solid #1d2433;
      background: rgba(8, 11, 18, 0.88);
      backdrop-filter: blur(18px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 0 18px;
      position: sticky;
      top: 0;
      z-index: 20;
    }

    .ide-command {
      width: min(560px, 100%);
      min-height: 38px;
      display: flex;
      align-items: center;
      gap: 10px;
      border: 1px solid #222b3d;
      background: #0e1321;
      border-radius: 12px;
      padding: 0 12px;
      color: #7d879a;
    }

    .ide-command input {
      width: 100%;
      border: 0;
      outline: 0;
      background: transparent;
      color: #f8fafc;
    }

    .ide-top-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }

    .ide-top-actions a,
    .ide-status,
    .ide-branch {
      min-height: 34px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid #222b3d;
      background: #0e1321;
      color: #cbd5e1;
      border-radius: 999px;
      padding: 0 11px;
      font-weight: 800;
      font-size: 0.82rem;
    }

    .ide-status {
      color: #bbf7d0;
      border-color: rgba(34, 197, 94, 0.28);
      background: rgba(34, 197, 94, 0.08);
    }

    .ide-content {
      min-width: 0;
      padding: 24px;
    }

    .dash-eyebrow {
      color: #38bdf8;
      font-family: "JetBrains Mono", Consolas, monospace;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font-size: 0.74rem;
      font-weight: 900;
      margin: 0 0 8px;
    }

    h1 {
      font-size: clamp(2.5rem, 5vw, 5rem);
      line-height: 0.94;
      letter-spacing: -0.065em;
      margin: 0 0 16px;
    }

    h2 {
      margin: 0 0 10px;
      letter-spacing: -0.04em;
    }

    .dash-subtitle {
      color: #9ca8bd;
      max-width: 920px;
      line-height: 1.65;
      margin-bottom: 24px;
    }

    .ide-home-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }

    .ide-home-card,
    .ide-callout,
    .dash-panel,
    .metric-card,
    .dash-table,
    .ai-policy-card {
      border: 1px solid #222b3d;
      background: rgba(14, 19, 33, 0.84);
      border-radius: 18px;
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.22);
    }

    .ide-home-card {
      padding: 18px;
      color: #f8fafc;
      transition: 160ms ease;
    }

    .ide-home-card:hover {
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.42);
      background: rgba(17, 24, 39, 0.95);
    }

    .ide-home-card svg {
      color: #38bdf8;
      margin-bottom: 14px;
    }

    .ide-home-card p,
    .ide-callout p,
    .dash-panel p {
      color: #9ca8bd;
      line-height: 1.6;
    }

    .ide-callout {
      padding: 22px;
    }

    .ide-callout code {
      color: #7dd3fc;
      font-family: "JetBrains Mono", Consolas, monospace;
      margin: 0 4px;
    }

    .ide-workspace-title {
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: flex-start;
      margin-bottom: 18px;
    }

    .workspace-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .workspace-actions button,
    .workspace-actions a {
      border: 1px solid #222b3d;
      background: #0e1321;
      color: #f8fafc;
      border-radius: 999px;
      padding: 9px 12px;
      font-weight: 850;
    }

    .ide-workbench {
      height: min(72vh, 760px);
      min-height: 620px;
      display: grid;
      grid-template-columns: 250px minmax(0, 1fr) 380px;
      border: 1px solid #222b3d;
      border-radius: 18px;
      overflow: hidden;
      background: #080b12;
    }

    .ide-file-explorer,
    .ide-ai-panel {
      min-width: 0;
      background: #0b1020;
      border-right: 1px solid #1d2433;
      overflow: auto;
    }

    .ide-ai-panel {
      border-right: 0;
      border-left: 1px solid #1d2433;
      padding: 14px;
      display: grid;
      align-content: start;
      gap: 12px;
    }

    .ide-pane-title {
      height: 42px;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0 12px;
      color: #cbd5e1;
      border-bottom: 1px solid #1d2433;
      font-weight: 900;
      font-size: 0.86rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .ide-file-tree {
      display: grid;
      gap: 4px;
      padding: 8px;
    }

    .ide-file-tree button {
      min-height: 34px;
      display: flex;
      align-items: center;
      gap: 8px;
      border: 0;
      color: #9ca8bd;
      background: transparent;
      border-radius: 9px;
      padding: 0 9px;
      text-align: left;
      font-size: 0.84rem;
    }

    .ide-file-tree button:hover,
    .ide-file-tree button.selected {
      color: #f8fafc;
      background: #111827;
    }

    .ide-editor {
      min-width: 0;
      display: grid;
      grid-template-rows: 42px minmax(0, 1fr);
      background: #080b12;
    }

    .ide-editor-tabs {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 1px solid #1d2433;
      background: #0b1020;
      padding: 0 14px;
    }

    .ide-editor-tabs span {
      color: #f8fafc;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.83rem;
    }

    .ide-editor-tabs small {
      color: #7d879a;
    }

    .ide-monaco-frame {
      min-height: 0;
    }

    .ide-ai-panel label {
      display: grid;
      gap: 6px;
      color: #cbd5e1;
      font-weight: 850;
      font-size: 0.86rem;
    }

    .ide-ai-panel select,
    .ide-ai-panel textarea {
      width: 100%;
      border: 1px solid #222b3d;
      background: #080b12;
      color: #f8fafc;
      border-radius: 10px;
      padding: 10px;
      outline: none;
    }

    .prompt-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
    }

    .prompt-chips button {
      border: 1px solid #222b3d;
      background: #0e1321;
      color: #9ca8bd;
      border-radius: 999px;
      padding: 6px 9px;
      font-size: 0.75rem;
      font-weight: 800;
    }

    .ide-run-button {
      width: 100%;
      min-height: 42px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: 0;
      border-radius: 12px;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      color: #04111f;
      font-weight: 950;
    }

    .spin {
      animation: spin 900ms linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .ide-error {
      color: #fecaca;
      border: 1px solid rgba(239, 68, 68, 0.28);
      background: rgba(239, 68, 68, 0.1);
      border-radius: 12px;
      padding: 10px;
      font-weight: 800;
    }

    .ide-muted {
      color: #7d879a;
      line-height: 1.55;
      font-size: 0.9rem;
    }

    .ai-result {
      min-height: 0;
      border: 1px solid #222b3d;
      border-radius: 14px;
      overflow: hidden;
      background: #080b12;
    }

    .ai-result-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 7px;
      padding: 10px;
      border-bottom: 1px solid #222b3d;
    }

    .ai-result-actions strong {
      font-size: 0.85rem;
    }

    .ai-result-actions button {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: 1px solid #222b3d;
      color: #cbd5e1;
      background: #0e1321;
      border-radius: 9px;
      padding: 6px 8px;
      font-size: 0.76rem;
      font-weight: 850;
    }

    .ai-result pre {
      max-height: 280px;
      overflow: auto;
      margin: 0;
      padding: 12px;
      color: #cbd5e1;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.78rem;
      line-height: 1.55;
      white-space: pre-wrap;
    }

    .ide-terminal-dock {
      margin-top: 14px;
      border: 1px solid #222b3d;
      border-radius: 18px;
      overflow: hidden;
      background: #080b12;
    }

    .ide-terminal-head {
      height: 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1d2433;
      background: #0b1020;
      padding: 0 12px;
      color: #cbd5e1;
      font-weight: 900;
    }

    .ide-terminal-head span {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .ide-terminal-head small {
      color: #7d879a;
    }

    .terminal-command-strip {
      display: flex;
      gap: 7px;
      overflow-x: auto;
      padding: 8px;
      border-bottom: 1px solid #1d2433;
    }

    .terminal-command-strip button {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      border: 1px solid #222b3d;
      background: #0e1321;
      color: #9ca8bd;
      border-radius: 999px;
      padding: 6px 9px;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 0.74rem;
    }

    .xterm-host {
      height: 260px;
      padding: 8px;
    }

    .dashboard-auth-page {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
      background:
        radial-gradient(circle at 20% 10%, rgba(56, 189, 248, 0.18), transparent 28rem),
        radial-gradient(circle at 80% 0%, rgba(34, 197, 94, 0.1), transparent 26rem),
        #050812;
    }

    .dashboard-auth-card {
      width: min(100%, 480px);
      display: grid;
      gap: 16px;
      padding: 34px;
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 28px;
      background: rgba(15, 23, 42, 0.78);
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.42);
      backdrop-filter: blur(22px);
    }

    .dashboard-auth-card h1 {
      margin: 0;
      font-size: clamp(2.1rem, 6vw, 4rem);
      line-height: 0.95;
      letter-spacing: -0.06em;
    }

    .dashboard-auth-card p,
    .dashboard-auth-card small {
      color: #94a3b8;
      line-height: 1.6;
    }

    .dashboard-auth-card label {
      display: grid;
      gap: 8px;
      color: #cbd5e1;
      font-weight: 800;
    }

    .dashboard-auth-card input {
      min-height: 48px;
      border: 1px solid #222b3d;
      background: #080b12;
      color: #f8fafc;
      border-radius: 16px;
      padding: 0 12px;
    }

    .auth-icon {
      width: 52px;
      height: 52px;
      display: grid;
      place-items: center;
      border-radius: 18px;
      color: #04111f;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
    }

    .auth-error {
      color: #fecaca;
      border: 1px solid rgba(239, 68, 68, 0.28);
      background: rgba(239, 68, 68, 0.1);
      border-radius: 14px;
      padding: 10px 12px;
      font-weight: 800;
    }

    .primary-action {
      border: 0;
      color: #04111f;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      border-radius: 999px;
      padding: 11px 14px;
      font-weight: 950;
    }

    .dash-panel,
    .metric-card,
    .dash-table,
    .ai-policy-card {
      padding: 20px;
    }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }

    .metric-card span,
    .metric-card small {
      color: #9ca8bd;
    }

    .metric-card strong {
      display: block;
      font-size: 2rem;
      margin: 8px 0;
    }

    .dashboard-grid-two,
    .provider-grid,
    .settings-grid,
    .field-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }

    .dash-table {
      overflow: hidden;
    }

    .dash-table-head,
    .dash-table-row {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      align-items: center;
      padding: 14px;
      border-bottom: 1px solid #1d2433;
    }

    .dash-table-head {
      color: #7d879a;
      font-weight: 900;
      text-transform: uppercase;
      font-size: 0.76rem;
      letter-spacing: 0.08em;
    }

    .dash-table-row {
      color: #f8fafc;
    }

    .status-badge {
      display: inline-flex;
      width: fit-content;
      min-height: 27px;
      align-items: center;
      padding: 0 9px;
      border-radius: 999px;
      border: 1px solid #263247;
      color: #cbd5e1;
      font-size: 0.77rem;
      font-weight: 900;
      text-transform: capitalize;
    }

    .status-published,
    .status-ready,
    .status-qualified,
    .status-proposal,
    .status-configured {
      color: #bbf7d0;
      border-color: rgba(34, 197, 94, 0.32);
      background: rgba(34, 197, 94, 0.08);
    }

    .status-draft,
    .status-review,
    .status-new,
    .status-needs-secret,
    .status-missing-secret,
    .status-needs-optimization {
      color: #fde68a;
      border-color: rgba(245, 158, 11, 0.32);
      background: rgba(245, 158, 11, 0.08);
    }

    input,
    textarea,
    select {
      border: 1px solid #222b3d;
      background: #080b12;
      color: #f8fafc;
      border-radius: 10px;
      padding: 10px;
      outline: none;
    }

    @media (max-width: 1180px) {
      .ide-shell {
        grid-template-columns: 54px minmax(0, 1fr);
      }

      .ide-sidebar {
        display: none;
      }

      .ide-workbench,
      .ide-home-grid,
      .metric-grid,
      .dashboard-grid-two,
      .provider-grid,
      .settings-grid,
      .field-grid {
        grid-template-columns: 1fr;
      }

      .ide-workbench {
        height: auto;
        min-height: 0;
      }

      .ide-file-explorer,
      .ide-ai-panel {
        max-height: 420px;
      }

      .ide-monaco-frame {
        height: 560px;
      }
    }
    ''')

    write("docs/CURSOR_IDE_OPENAI_DASHBOARD.md", r'''
    # Cursor-Style IDE Dashboard + OpenAI

    The dashboard has been remastered into a Cursor-style IDE cockpit.

    ## Routes

    ```txt
    /dashboard
    /dashboard/dev
    /dashboard/dev/editor
    /dashboard/dev/terminal
    /dashboard/dev/agent
    ```

    ## Features

    ```txt
    Cursor-style shell
    Activity bar
    Sidebar navigation
    Monaco editor
    File explorer
    xterm terminal dock
    PowerShell command presets
    OpenAI-backed code generation endpoint
    AI result copy/apply-to-editor workflow
    Provider settings
    R2/CMS/dashboard routes preserved
    ```

    ## OpenAI Endpoints

    ```txt
    POST /api/openai/code
    POST /api/openai/chat
    GET  /api/ai/providers
    GET  /api/health
    ```

    ## Security

    The OpenAI key stays in the Worker as:

    ```txt
    OPENAI_API_KEY
    ```

    The browser never receives the key.

    ## Example OpenAI Code Request

    ```json
    {
      "model": "gpt-5.4-mini",
      "mode": "refactor",
      "filename": "src/worker/index.js",
      "language": "javascript",
      "instruction": "Add a CMS save draft endpoint.",
      "code": "current file contents"
    }
    ```

    ## Production Notes

    The terminal is xterm-ready, but command execution is intentionally not enabled yet.

    Production terminal execution needs:

    ```txt
    Auth
    Durable Object session
    PTY bridge
    command allowlist
    audit logs
    timeout limits
    secret redaction
    ```
    ''')

    run(["npm", "install"], check=True)
    run(["npm", "run", "build"], check=True)
    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", "feat: remaster dashboard as Cursor IDE with Monaco xterm and OpenAI code actions"], check=False)

    print("\nCursor-style IDE dashboard complete.")
    print("Next:")
    print("npm run deploy")
    print("curl -s https://leadership-legacy.meauxbility.workers.dev/api/health")
    print("curl -s https://leadership-legacy.meauxbility.workers.dev/api/ai/providers")
    print("open https://leadership-legacy.meauxbility.workers.dev/dashboard/dev")

if __name__ == "__main__":
    main()
