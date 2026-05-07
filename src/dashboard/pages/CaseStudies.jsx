import { DataTable } from "../components/DataTable.jsx";
import { StatusBadge } from "../components/StatusBadge.jsx";
import { caseStudies } from "../data/cmsData.js";

export function CaseStudies() {
  return (
    <section>
      <p className="dash-eyebrow">Work</p>
      <h1>Case studies</h1>
      <p className="dash-subtitle">Edit project proof, outcomes, technical stacks, and conversion CTAs.</p>

      <DataTable
        columns={[
          { key: "title", label: "Title" },
          { key: "category", label: "Category" },
          { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
          { key: "stack", label: "Stack", render: (row) => row.stack.join(", ") },
          { key: "outcome", label: "Outcome" }
        ]}
        rows={caseStudies}
      />
    </section>
  );
}
