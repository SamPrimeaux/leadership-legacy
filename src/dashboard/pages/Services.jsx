import { DataTable } from "../components/DataTable.jsx";
import { StatusBadge } from "../components/StatusBadge.jsx";
import { services } from "../data/cmsData.js";

export function Services() {
  return (
    <section>
      <p className="dash-eyebrow">Offers</p>
      <h1>Services</h1>
      <p className="dash-subtitle">Manage offer pages, pricing notes, deliverables, use cases, and SEO.</p>

      <DataTable
        columns={[
          { key: "title", label: "Service" },
          { key: "slug", label: "Route" },
          { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
          { key: "price", label: "Starting" },
          { key: "summary", label: "Summary" }
        ]}
        rows={services}
      />
    </section>
  );
}
