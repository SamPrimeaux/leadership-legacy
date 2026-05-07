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

def patch_worker():
    p = ROOT / "src/worker/index.js"
    s = p.read_text()

    chat_route = r'''
        if (pathname === "/api/openai/chat" && request.method === "POST") {
          const body = await readJson(request);
          const model = body.model || env.OPENAI_DEFAULT_MODEL || "gpt-5.4-mini";
          const message = body.message || "";
          const context = body.context || "";

          if (["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"].includes(model)) {
            return json({
              ok: false,
              error: "This model is blocked by project policy."
            }, 400);
          }

          const result = await callOpenAI(env, {
            model,
            instructions: [
              "You are Agent Connor inside the Leadership Legacy dashboard.",
              "Default to conversational help unless the user explicitly asks to edit, rewrite, generate, refactor, replace, or patch code.",
              "Be practical and concise.",
              "Do not expose secrets.",
              "Help Connor learn the platform, Cloudflare, GitHub, R2, D1, Supabase, OpenAI, Anthropic, Gmail, Google Drive, Resend, MCP tools, and PowerShell workflows."
            ].join("\n"),
            input: [
              context ? `Dashboard context:\n${context}` : "",
              "",
              "User message:",
              message
            ].join("\n"),
            max_output_tokens: 1800
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
'''

    if 'pathname === "/api/openai/chat"' not in s:
        marker = '        if (pathname === "/api/openai/code" && request.method === "POST") {'
        s = s.replace(marker, chat_route + "\n" + marker)

    p.write_text(s)

def patch_agent():
    p = ROOT / "src/dashboard/pages/AgentIDE.jsx"
    s = p.read_text()

    old = r'''    function AgentPanel({ activeFile, file, updateFile }) {
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
    }'''

    new = r'''    function AgentPanel({ activeFile, file, updateFile }) {
      const [message, setMessage] = useState("");
      const [busy, setBusy] = useState(false);
      const [chat, setChat] = useState([]);
      const [model, setModel] = useState("gpt-5.4-mini");
      const [agentMode, setAgentMode] = useState("chat");

      function shouldUseCodeMode(text) {
        const lowered = text.toLowerCase();
        return /\b(edit|rewrite|refactor|patch|replace|generate code|create component|fix this file|update this file|apply|write code|make this file)\b/.test(lowered);
      }

      async function send() {
        const trimmed = message.trim();
        if (!trimmed || busy) return;

        const effectiveMode = agentMode === "auto"
          ? shouldUseCodeMode(trimmed) ? "code" : "chat"
          : agentMode;

        setChat((current) => [...current, { role: "user", text: trimmed }]);
        setMessage("");
        setBusy(true);

        try {
          const endpoint = effectiveMode === "code" ? "/api/openai/code" : "/api/openai/chat";

          const payload = effectiveMode === "code"
            ? {
                model,
                mode: "refactor",
                filename: activeFile,
                language: file.language,
                code: file.content,
                instruction: trimmed
              }
            : {
                model,
                message: trimmed,
                context: `Active file: ${activeFile}\nLanguage: ${file.language}\nSource: ${file.source || "local"}`
              };

          const response = await fetch(endpoint, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify(payload)
          });

          const data = await response.json();

          if (!response.ok || !data.ok) {
            throw new Error(data.error || "Agent request failed.");
          }

          setChat((current) => [
            ...current,
            effectiveMode === "code"
              ? {
                  role: "assistant",
                  text: "Generated an updated file. Apply it when ready.",
                  code: data.code,
                  usage: data.usage
                }
              : {
                  role: "assistant",
                  text: data.text || "Done.",
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
            <button className={agentMode === "chat" ? "active" : ""} onClick={() => setAgentMode("chat")}>Chat</button>
            <button className={agentMode === "code" ? "active" : ""} onClick={() => setAgentMode("code")}>Code</button>
            <button className={agentMode === "auto" ? "active" : ""} onClick={() => setAgentMode("auto")}>Auto</button>
          </div>

          <div className="ia-agent-body">
            {chat.length === 0 ? (
              <div className="ia-empty-agent">
                <div className="ia-agent-orb"><Bot size={24} /></div>
                <h3>What should we work on?</h3>
                <p>Chat is the default. Switch to Code when you want Agent Connor to edit the active Monaco file.</p>
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
              placeholder={agentMode === "code" ? "Tell Agent Connor what to change in this file..." : "Message Agent Connor..."}
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
    }'''

    if old not in s:
        raise SystemExit("Could not find old AgentPanel block. File may have changed; patch manually.")
    s = s.replace(old, new)
    p.write_text(s)

def patch_css():
    p = ROOT / "src/dashboard/dashboard.css"
    s = p.read_text()

    if ".ia-agent-tabs button.active" in s and "cursor: pointer" not in s[s.find(".ia-agent-tabs button"):s.find(".ia-agent-body")]:
        s = s.replace(
            """.ia-agent-tabs button {
      color: #89cfd6;
      font-size: 0.72rem;
      font-weight: 800;
    }""",
            """.ia-agent-tabs button {
      color: #89cfd6;
      font-size: 0.72rem;
      font-weight: 800;
      cursor: pointer;
      border-radius: 999px;
      padding: 4px 8px;
    }"""
        )

        s = s.replace(
            """.ia-agent-tabs button.active { color: #eaffff; }""",
            """.ia-agent-tabs button.active {
      color: #041316;
      background: #20e3f0;
    }"""
        )

    p.write_text(s)

def main():
    patch_worker()
    patch_agent()
    patch_css()

    write("docs/AGENT_CHAT_VS_CODE_MODE.md", r'''
    # Agent Chat vs Code Mode

    Agent Connor now has three modes:

    ```txt
    Chat
    Code
    Auto
    ```

    ## Chat

    Default mode.

    Use for:

    ```txt
    asking questions
    learning Cloudflare/PowerShell/GitHub/R2
    debugging conceptually
    planning integrations
    explaining files
    discussing next steps
    ```

    Calls:

    ```txt
    POST /api/openai/chat
    ```

    ## Code

    Use when the user explicitly wants to edit the active Monaco file.

    Calls:

    ```txt
    POST /api/openai/code
    ```

    The response includes generated file contents and can be applied to the editor.

    ## Auto

    Auto uses simple intent detection. It chooses code mode only when the message includes edit/refactor/patch/generate-code type language.

    This prevents casual messages like `wyd` from rewriting the active file.
    ''')

    run(["npm", "run", "build"], check=True)
    run(["git", "add", "src/worker/index.js", "src/dashboard/pages/AgentIDE.jsx", "src/dashboard/dashboard.css", "docs/AGENT_CHAT_VS_CODE_MODE.md", "scripts/fix_agent_default_chat_mode.py"], check=False)
    run(["git", "commit", "-m", "feat: default Agent Connor to chat mode with explicit code actions"], check=False)

    print("\nAgent default chat mode fixed.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")
    print("Then hard refresh /dashboard/agent")

if __name__ == "__main__":
    main()
