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
