import { useEffect, useRef, useState } from "react";
import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";
import "@xterm/xterm/css/xterm.css";
import { powershellCommands } from "../../data/devCockpitData.js";

export function TerminalPanel() {
  const ref = useRef(null);
  const terminalRef = useRef(null);
  const [activeCommand, setActiveCommand] = useState(powershellCommands[0]);

  useEffect(() => {
    if (!ref.current || terminalRef.current) return;

    const terminal = new Terminal({
      cursorBlink: true,
      convertEol: true,
      fontFamily: "JetBrains Mono, Consolas, monospace",
      fontSize: 13,
      theme: {
        background: "#050812",
        foreground: "#f8fafc",
        cursor: "#38bdf8",
        selectionBackground: "#1e3a5f"
      }
    });

    const fit = new FitAddon();
    terminal.loadAddon(fit);
    terminal.open(ref.current);
    fit.fit();

    terminal.writeln("Leadership Legacy Dev Terminal");
    terminal.writeln("PowerShell-friendly command cockpit");
    terminal.writeln("");
    terminal.writeln("This browser terminal is prepared for a future Worker/DO/PTY tunnel.");
    terminal.writeln("For now, copy commands into PowerShell.");
    terminal.writeln("");
    terminal.write("PS leadership-legacy> ");

    terminalRef.current = terminal;

    const onResize = () => fit.fit();
    window.addEventListener("resize", onResize);

    return () => {
      window.removeEventListener("resize", onResize);
      terminal.dispose();
      terminalRef.current = null;
    };
  }, []);

  function writeCommand(command) {
    setActiveCommand(command);
    const terminal = terminalRef.current;
    if (!terminal) return;

    terminal.writeln("");
    terminal.writeln(`PS leadership-legacy> ${command.command}`);
    terminal.writeln(`# ${command.notes}`);
    terminal.write("PS leadership-legacy> ");
  }

  async function copyCommand(command) {
    await navigator.clipboard.writeText(command.command);
    writeCommand({ ...command, notes: `${command.notes} Copied to clipboard.` });
  }

  return (
    <section className="dev-panel terminal-cockpit">
      <div className="dev-panel-head">
        <div>
          <p className="dash-eyebrow">xterm + PowerShell</p>
          <h2>Command cockpit</h2>
        </div>
        <span className="dev-badge">Prepared for DO/PTY</span>
      </div>

      <div className="terminal-layout">
        <aside className="command-list">
          {powershellCommands.map((command) => (
            <button key={command.id} onClick={() => copyCommand(command)}>
              <strong>{command.label}</strong>
              <code>{command.command}</code>
            </button>
          ))}
        </aside>

        <div className="terminal-wrap" ref={ref} />
      </div>

      <div className="command-detail">
        <strong>{activeCommand.label}</strong>
        <code>{activeCommand.command}</code>
        <p>{activeCommand.notes}</p>
      </div>
    </section>
  );
}
