import { MonacoPanel } from "../components/dev/MonacoPanel.jsx";
import { TerminalPanel } from "../components/dev/TerminalPanel.jsx";
import { TunnelPanel } from "../components/dev/TunnelPanel.jsx";
import { SetupChecklist } from "../components/dev/SetupChecklist.jsx";

export function DevCockpit({ view = "overview" }) {
  return (
    <section>
      <p className="dash-eyebrow">Developer Cockpit</p>
      <h1>Built-in editor, terminal, and tunnel prep</h1>
      <p className="dash-subtitle">
        A guided technical workspace for Connor: Monaco for code, xterm for terminal-style guidance,
        PowerShell command presets, and Cloudflare Tunnel preparation for shareable local previews.
      </p>

      {view === "editor" ? (
        <MonacoPanel />
      ) : view === "tunnel" ? (
        <TunnelPanel />
      ) : (
        <>
          <div className="dev-hero-grid">
            <article className="dash-panel">
              <h2>Why this matters</h2>
              <p>
                Connor can run, build, deploy, and inspect the platform without needing to memorize every CLI command.
                The dashboard becomes a training cockpit and future control surface for real terminal sessions.
              </p>
            </article>
            <article className="dash-panel">
              <h2>Production path</h2>
              <p>
                This is prepared for a Worker Durable Object session bridge, Cloudflare Tunnel,
                repo-aware commands, R2 snapshots, and safe AI-assisted code actions.
              </p>
            </article>
          </div>

          <SetupChecklist />
          <TerminalPanel />
          <MonacoPanel />
          <TunnelPanel />
        </>
      )}
    </section>
  );
}
