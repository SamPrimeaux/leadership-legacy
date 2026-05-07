import { tunnelCommands } from "../../data/devCockpitData.js";

export function TunnelPanel() {
  async function copy(text) {
    await navigator.clipboard.writeText(text);
  }

  return (
    <section className="dev-panel">
      <div className="dev-panel-head">
        <div>
          <p className="dash-eyebrow">Cloudflare Tunnel</p>
          <h2>Remote preview prep</h2>
        </div>
        <span className="dev-badge">cloudflared-ready</span>
      </div>

      <p className="dev-copy">
        This area teaches Connor how to expose a local PowerShell/Vite dev server through Cloudflare Tunnel
        without needing to deeply understand terminal workflows on day one.
      </p>

      <div className="tunnel-grid">
        {tunnelCommands.map((command) => (
          <article className="tunnel-card" key={command.id}>
            <strong>{command.label}</strong>
            <code>{command.command}</code>
            <p>{command.notes}</p>
            <button onClick={() => copy(command.command)}>Copy command</button>
          </article>
        ))}
      </div>

      <article className="dash-panel">
        <h3>Future dashboard integration</h3>
        <p>
          The next production step is a Worker Durable Object terminal bridge. The browser dashboard will request
          a session, the Worker will authorize it, and a local or hosted PTY service will stream output into xterm.
        </p>
        <code>Browser Dashboard → Worker → Durable Object → PTY/Tunnel Service → PowerShell</code>
      </article>
    </section>
  );
}
