import { MetricCard } from "../components/MetricCard.jsx";
import { analyticsEvents, leads, cmsPages } from "../data/cmsData.js";

export function DashboardHome() {
  const draftCount = cmsPages.filter((page) => page.status !== "published").length;

  return (
    <section>
      <p className="dash-eyebrow">Overview</p>
      <h1>CMS command center</h1>
      <p className="dash-subtitle">
        Manage Connor’s public site, live CMS content, leads, analytics, publishing, and AI provider routing from one technical cockpit.
      </p>

      <div className="metric-grid">
        <MetricCard label="Published Pages" value={cmsPages.filter((p) => p.status === "published").length} detail="Public content online" />
        <MetricCard label="Draft Changes" value={draftCount} detail="Needs review or publish" />
        <MetricCard label="New Leads" value={leads.filter((lead) => lead.status === "new").length} detail="Project intake queue" />
        <MetricCard label="Tracked Views" value={analyticsEvents.reduce((sum, row) => sum + row.views, 0).toLocaleString()} detail="Mock analytics seed" />
      </div>

      <div className="dashboard-grid-two">
        <article className="dash-panel">
          <h2>Priority workflow</h2>
          <ol className="workflow-list">
            <li>Edit homepage hero and services grid.</li>
            <li>Review work pages for MechAssist AI and OpenClaw.</li>
            <li>Connect OpenAI and Anthropic secrets in Cloudflare.</li>
            <li>Publish CMS pages after QA.</li>
          </ol>
        </article>

        <article className="dash-panel">
          <h2>AI provider readiness</h2>
          <div className="readiness-list">
            <span>OpenAI routing metadata ready</span>
            <span>Anthropic routing metadata ready</span>
            <span>Secrets server-side only</span>
            <span>Blocked models policy enabled</span>
          </div>
        </article>
      </div>
    </section>
  );
}
