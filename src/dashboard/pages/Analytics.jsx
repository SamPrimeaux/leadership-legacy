import { analyticsEvents } from "../data/cmsData.js";
import { DataTable } from "../components/DataTable.jsx";
import { MetricCard } from "../components/MetricCard.jsx";

export function Analytics() {
  const views = analyticsEvents.reduce((sum, row) => sum + row.views, 0);
  const leads = analyticsEvents.reduce((sum, row) => sum + row.leads, 0);
  const ctas = analyticsEvents.reduce((sum, row) => sum + row.cta, 0);

  return (
    <section>
      <p className="dash-eyebrow">Analytics</p>
      <h1>Site performance</h1>
      <p className="dash-subtitle">Prepared for D1 events, Supabase long-term analytics, and provider cost telemetry.</p>

      <div className="metric-grid">
        <MetricCard label="Views" value={views.toLocaleString()} />
        <MetricCard label="CTA Clicks" value={ctas.toLocaleString()} />
        <MetricCard label="Leads" value={leads.toLocaleString()} />
        <MetricCard label="Primary Source" value="RAG page" />
      </div>

      <DataTable
        columns={[
          { key: "page", label: "Page" },
          { key: "views", label: "Views" },
          { key: "cta", label: "CTA" },
          { key: "leads", label: "Leads" },
          { key: "conversion", label: "Conversion" }
        ]}
        rows={analyticsEvents.map((row) => ({ ...row, id: row.page }))}
      />
    </section>
  );
}
