#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()
AGENT_FILE = ROOT / "src/dashboard/pages/AgentIDE.jsx"
WORKER_FILE = ROOT / "src/worker/index.js"
CSS_FILE = ROOT / "src/dashboard/dashboard.css"

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

def replace_function(source, function_name, replacement):
    start = source.find(f"function {function_name}(")
    if start == -1:
        raise SystemExit(f"Could not find function {function_name}")

    brace_start = source.find("{", start)
    if brace_start == -1:
        raise SystemExit(f"Could not find opening brace for {function_name}")

    depth = 0
    in_string = None
    escaped = False
    in_line_comment = False
    in_block_comment = False

    i = brace_start
    while i < len(source):
        ch = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue

        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            i += 2
            continue

        if ch == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue

        if ch in ("'", '"', "`"):
            in_string = ch
            i += 1
            continue

        if ch == "{":
            depth += 1

        if ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                return source[:start] + replacement.rstrip() + source[end:]

        i += 1

    raise SystemExit(f"Could not find end of function {function_name}")

def patch_worker():
    s = WORKER_FILE.read_text()

    if 'pathname === "/api/openai/chat"' in s:
        print("Worker already has /api/openai/chat")
        return

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

    marker = '        if (pathname === "/api/openai/code" && request.method === "POST") {'
    if marker not in s:
        raise SystemExit("Could not find /api/openai/code route marker in worker")

    s = s.replace(marker, chat_route + "\n" + marker)
    WORKER_FILE.write_text(s)
    print("Added /api/openai/chat route")

def patch_agent():
    s = AGENT_FILE.read_text()

    new_agent_panel = r'''
function AgentPanel({ activeFile, file, updateFile }) {
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

  function startNewChat() {
    setChat([]);
    setMessage("");
  }

  return (
    <aside className="ia-agent">
      <div className="ia-agent-head">
        <span>AGENT CONNOR</span>
        <button onClick={startNewChat} title="New chat"><MoreHorizontal size={15} /></button>
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
}
'''

    s = replace_function(s, "AgentPanel", new_agent_panel)
    AGENT_FILE.write_text(s)
    print("Replaced AgentPanel with chat/code/auto mode version")

def patch_css():
    s = CSS_FILE.read_text()

    s += r'''

/* Agent mode tabs */
.ia-agent-tabs button {
  cursor: pointer;
  border-radius: 999px;
  padding: 4px 8px;
}

.ia-agent-tabs button.active {
  color: #041316;
  background: #20e3f0;
}

.ia-chat.assistant p {
  white-space: pre-wrap;
}
'''
    CSS_FILE.write_text(s)

def main():
    patch_worker()
    patch_agent()
    patch_css()

    docs = ROOT / "docs/AGENT_CHAT_VS_CODE_MODE.md"
    docs.write_text(textwrap.dedent(r'''
    # Agent Chat vs Code Mode

    Agent Connor now has three modes:

    ```txt
    Chat
    Code
    Auto
    ```

    Chat is the default and calls:

    ```txt
    POST /api/openai/chat
    ```

    Code intentionally edits the active Monaco file and calls:

    ```txt
    POST /api/openai/code
    ```

    Auto uses intent detection and only chooses code mode for explicit file-edit requests.

    This prevents casual messages like `wyd` from rewriting the active file.
    ''').lstrip())

    run(["npm", "run", "build"], check=True)
    run(["git", "add", "src/worker/index.js", "src/dashboard/pages/AgentIDE.jsx", "src/dashboard/dashboard.css", "docs/AGENT_CHAT_VS_CODE_MODE.md", "scripts/fix_agent_default_chat_mode_safe.py"], check=False)
    run(["git", "commit", "-m", "feat: default Agent Connor to chat with explicit code mode"], check=False)

    print("\nDone.")
    print("Next:")
    print("npm run deploy")
    print("git push origin main")
    print("Hard refresh /dashboard/agent after deploy.")

if __name__ == "__main__":
    main()
