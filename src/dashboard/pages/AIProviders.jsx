import { aiProviders, routingPolicy } from "../data/aiProviders.js";
import { StatusBadge } from "../components/StatusBadge.jsx";

export function AIProviders() {
  return (
    <section>
      <p className="dash-eyebrow">AI Routing</p>
      <h1>OpenAI and Anthropic providers</h1>
      <p className="dash-subtitle">
        Configure model metadata, routing lanes, blocked models, and server-side secret requirements.
        API keys must be stored as Cloudflare secrets, never in browser code.
      </p>

      <div className="ai-policy-card">
        <h2>Routing policy</h2>
        <div className="policy-grid">
          {Object.entries(routingPolicy).map(([key, value]) => (
            <div key={key}>
              <span>{key}</span>
              <code>{Array.isArray(value) ? value.join(", ") : String(value)}</code>
            </div>
          ))}
        </div>
      </div>

      <div className="provider-grid">
        {aiProviders.map((provider) => (
          <article className="dash-panel" key={provider.key}>
            <div className="provider-head">
              <div>
                <p className="dash-eyebrow">{provider.key}</p>
                <h2>{provider.displayName}</h2>
              </div>
              <StatusBadge status={provider.status} />
            </div>

            <div className="secret-box">
              <span>Cloudflare secret</span>
              <code>{provider.secretName}</code>
            </div>

            <h3>Models</h3>
            <div className="model-list">
              {provider.models.map((model) => (
                <div key={model.key}>
                  <strong>{model.key}</strong>
                  <span>{model.lane}</span>
                  <small>{model.notes}</small>
                </div>
              ))}
            </div>

            {provider.blockedModels.length ? (
              <>
                <h3>Blocked models</h3>
                <div className="chip-row">
                  {provider.blockedModels.map((model) => <span key={model}>{model}</span>)}
                </div>
              </>
            ) : null}
          </article>
        ))}
      </div>

      <article className="dash-panel">
        <h2>Backend API contract</h2>
        <code>GET /api/ai/providers</code>
        <code>POST /api/agent/chat</code>
        <code>POST /api/agent/route</code>
        <code>POST /api/agent/image</code>
        <code>POST /api/agent/evals/run</code>
      </article>
    </section>
  );
}
