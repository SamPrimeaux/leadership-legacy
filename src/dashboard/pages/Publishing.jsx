import { cmsPages } from "../data/cmsData.js";
import { StatusBadge } from "../components/StatusBadge.jsx";

export function Publishing() {
  const pending = cmsPages.filter((page) => page.status !== "published");

  return (
    <section>
      <p className="dash-eyebrow">Publishing</p>
      <h1>Publish center</h1>
      <p className="dash-subtitle">Review drafts, promote published JSON, and create version snapshots.</p>

      <div className="action-row">
        <button className="primary-action">Publish selected</button>
        <button>Preview all drafts</button>
        <button>Rollback version</button>
      </div>

      <div className="publish-list">
        {pending.map((page) => (
          <article className="dash-panel" key={page.id}>
            <div>
              <strong>{page.title}</strong>
              <small>{page.slug}</small>
            </div>
            <StatusBadge status={page.status} />
          </article>
        ))}
      </div>
    </section>
  );
}
