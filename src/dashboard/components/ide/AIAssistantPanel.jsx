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
