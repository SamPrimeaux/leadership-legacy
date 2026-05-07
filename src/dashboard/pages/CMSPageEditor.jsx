import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { cmsPages } from "../data/cmsData.js";
import { StatusBadge } from "../components/StatusBadge.jsx";

export function CMSPageEditor() {
  const { pageId } = useParams();
  const source = useMemo(() => cmsPages.find((page) => page.id === pageId) || cmsPages[0], [pageId]);
  const [draft, setDraft] = useState(source);
  const [selectedSectionId, setSelectedSectionId] = useState(source.sections[0]?.id || null);

  const selected = draft.sections.find((section) => section.id === selectedSectionId) || draft.sections[0];

  function updateProp(key, value) {
    setDraft((current) => ({
      ...current,
      sections: current.sections.map((section) =>
        section.id === selected.id
          ? { ...section, props: { ...section.props, [key]: value } }
          : section
      )
    }));
  }

  return (
    <section>
      <div className="editor-header">
        <div>
          <p className="dash-eyebrow">Live Page Editor</p>
          <h1>{draft.title}</h1>
          <p className="dash-subtitle">{draft.slug} · <StatusBadge status={draft.status} /></p>
        </div>
        <div className="editor-actions">
          <button>Save Draft</button>
          <button>Preview</button>
          <button className="primary-action">Publish</button>
        </div>
      </div>

      <div className="editor-layout">
        <aside className="editor-panel">
          <strong>Section tree</strong>
          {draft.sections.map((section) => (
            <button
              className={section.id === selected?.id ? "selected" : ""}
              key={section.id}
              onClick={() => setSelectedSectionId(section.id)}
            >
              <span>{section.type}</span>
              <small>{section.id}</small>
            </button>
          ))}
        </aside>

        <main className="preview-panel">
          <p className="dash-eyebrow">{selected?.props?.eyebrow || "Preview"}</p>
          <h2>{selected?.props?.heading || selected?.type}</h2>
          <p>{selected?.props?.body || "This section is ready for CMS-rendered props and visual content."}</p>
          <div className="preview-cta-row">
            <span>{selected?.props?.primaryCta || "Primary CTA"}</span>
            <span>{selected?.props?.secondaryCta || "Secondary CTA"}</span>
          </div>
        </main>

        <aside className="editor-panel inspector">
          <strong>Inspector</strong>

          {selected ? (
            <>
              {Object.entries(selected.props).map(([key, value]) => (
                <label key={key}>
                  {key}
                  {String(value).length > 44 ? (
                    <textarea value={value} onChange={(event) => updateProp(key, event.target.value)} />
                  ) : (
                    <input value={value} onChange={(event) => updateProp(key, event.target.value)} />
                  )}
                </label>
              ))}
            </>
          ) : (
            <p>No section selected.</p>
          )}

          <div className="inspector-box">
            <strong>Backend path</strong>
            <code>PATCH /api/cms/pages/{draft.id}/draft</code>
            <code>POST /api/cms/pages/{draft.id}/publish</code>
          </div>
        </aside>
      </div>
    </section>
  );
}
