import { DataTable } from "../components/DataTable.jsx";
import { StatusBadge } from "../components/StatusBadge.jsx";
import { mediaAssets } from "../data/cmsData.js";

export function MediaLibrary() {
  return (
    <section>
      <p className="dash-eyebrow">Assets</p>
      <h1>Media library</h1>
      <p className="dash-subtitle">Manage images, textures, downloads, Open Graph assets, and CAD/GLB files.</p>

      <div className="action-row">
        <button className="primary-action">Upload asset</button>
        <button>Optimize images</button>
        <button>Sync R2 metadata</button>
      </div>

      <DataTable
        columns={[
          { key: "name", label: "Asset" },
          { key: "type", label: "Type" },
          { key: "usage", label: "Usage" },
          { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
          { key: "size", label: "Size" }
        ]}
        rows={mediaAssets}
      />
    </section>
  );
}
