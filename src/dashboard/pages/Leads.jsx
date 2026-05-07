import { DataTable } from "../components/DataTable.jsx";
import { StatusBadge } from "../components/StatusBadge.jsx";
import { leads } from "../data/cmsData.js";

export function Leads() {
  return (
    <section>
      <p className="dash-eyebrow">CRM</p>
      <h1>Project leads</h1>
      <p className="dash-subtitle">Review intake submissions and move prospects through the project pipeline.</p>

      <DataTable
        columns={[
          { key: "name", label: "Name" },
          { key: "company", label: "Company" },
          { key: "projectType", label: "Project Type" },
          { key: "budget", label: "Budget" },
          { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
          { key: "source", label: "Source" }
        ]}
        rows={leads}
      />
    </section>
  );
}
