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
