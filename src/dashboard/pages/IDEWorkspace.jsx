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
