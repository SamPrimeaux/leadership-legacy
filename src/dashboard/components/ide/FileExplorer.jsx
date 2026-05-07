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
