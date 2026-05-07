export function Settings({ section = "overview" }) {
  return (
    <section>
      <p className="dash-eyebrow">Settings</p>
      <h1>Site settings</h1>
      <p className="dash-subtitle">Manage brand tokens, navigation, SEO defaults, and CMS runtime configuration.</p>

      <div className="settings-grid">
        <article className="dash-panel">
          <h2>Brand</h2>
          <label>Brand Name<input defaultValue="Leadership Legacy Digital" /></label>
          <label>Founder Name<input defaultValue="Connor McNeely" /></label>
          <label>Primary Color<input defaultValue="#38bdf8" /></label>
        </article>

        <article className="dash-panel">
          <h2>SEO</h2>
          <label>Default Title<input defaultValue="Connor McNeely | Leadership Legacy Digital" /></label>
          <label>Default Description<textarea defaultValue="Engineering-grade AI systems for technical businesses." /></label>
        </article>

        <article className="dash-panel">
          <h2>Navigation</h2>
          <label>Primary CTA<input defaultValue="Start a Project" /></label>
          <label>CTA Route<input defaultValue="/contact" /></label>
        </article>

        <article className="dash-panel">
          <h2>Current section</h2>
          <code>{section}</code>
        </article>
      </div>
    </section>
  );
}
