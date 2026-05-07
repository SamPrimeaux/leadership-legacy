import { DataTable } from "../components/DataTable.jsx";
import { StatusBadge } from "../components/StatusBadge.jsx";
import { cmsPages } from "../data/cmsData.js";

export function CMSPages() {
  return (
    <section>
      <p className="dash-eyebrow">CMS</p>
      <h1>Pages</h1>
      <p className="dash-subtitle">Draft, preview, edit, and publish public website pages.</p>

      <DataTable
        columns={[
          { key: "title", label: "Page" },
          { key: "slug", label: "Route" },
          { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
          { key: "seoScore", label: "SEO" },
          { key: "updatedAt", label: "Updated" }
        ]}
        rows={cmsPages}
        getRowHref={(row) => `/dashboard/pages/${row.id}`}
      />
    </section>
  );
}
