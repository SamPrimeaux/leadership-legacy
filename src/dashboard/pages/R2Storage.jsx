import { useEffect, useState } from "react";

export function R2Storage() {
  const [status, setStatus] = useState(null);
  const [objects, setObjects] = useState([]);

  useEffect(() => {
    async function load() {
      const statusRes = await fetch("/api/r2/status");
      const statusJson = await statusRes.json();
      setStatus(statusJson);

      const listRes = await fetch("/api/r2/list?prefix=");
      const listJson = await listRes.json();
      setObjects(listJson.objects || []);
    }

    load().catch((error) => {
      setStatus({ ok: false, error: error.message });
    });
  }, []);

  return (
    <section>
      <p className="dash-eyebrow">R2 Storage</p>
      <h1>Leadership Legacy bucket</h1>
      <p className="dash-subtitle">
        R2 stores CMS assets, generated media, page snapshots, code snapshots, docs,
        analytics exports, downloads, and dashboard-managed files.
      </p>

      <div className="metric-grid">
        <article className="metric-card">
          <span>Binding</span>
          <strong>WEBSITE</strong>
          <small>Cloudflare Worker R2 binding</small>
        </article>
        <article className="metric-card">
          <span>Bucket</span>
          <strong>leadership-legacy</strong>
          <small>Western North America</small>
        </article>
        <article className="metric-card">
          <span>Status</span>
          <strong>{status?.ok ? "Online" : "Check"}</strong>
          <small>{status?.error || "R2 API reachable"}</small>
        </article>
        <article className="metric-card">
          <span>Objects</span>
          <strong>{objects.length}</strong>
          <small>First 100 listed</small>
        </article>
      </div>

      <article className="dash-panel">
        <h2>Bucket metadata</h2>
        <code>Public dev URL: {status?.publicDevelopmentUrl || "loading"}</code>
        <code>S3 endpoint: {status?.s3Endpoint || "loading"}</code>
        <code>Catalog URI: {status?.catalogUri || "loading"}</code>
        <code>Warehouse: {status?.warehouseName || "loading"}</code>
      </article>

      <div className="dash-table" role="table" style={{ marginTop: 18 }}>
        <div className="dash-table-head" role="row">
          <span>Key</span>
          <span>Size</span>
          <span>Uploaded</span>
          <span>Preview</span>
          <span>ETag</span>
        </div>
        {objects.map((object) => (
          <div className="dash-table-row" role="row" key={object.key}>
            <span>{object.key}</span>
            <span>{object.size}</span>
            <span>{object.uploaded ? new Date(object.uploaded).toLocaleString() : "—"}</span>
            <span><a href={`/api/r2/object/${encodeURIComponent(object.key)}`} target="_blank" rel="noreferrer">Open</a></span>
            <span>{object.etag?.slice(0, 16) || "—"}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
