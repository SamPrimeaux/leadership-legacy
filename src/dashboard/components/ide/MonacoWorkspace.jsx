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
