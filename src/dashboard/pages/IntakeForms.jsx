export function IntakeForms() {
  const fields = [
    "Name",
    "Email",
    "Company",
    "Project Type",
    "Budget Range",
    "Timeline",
    "Existing Assets",
    "Current Bottleneck",
    "Desired Outcome",
    "Message"
  ];

  return (
    <section>
      <p className="dash-eyebrow">Forms</p>
      <h1>Project intake form</h1>
      <p className="dash-subtitle">Configure the public contact form and map submissions into lead records.</p>

      <div className="field-grid">
        {fields.map((field) => (
          <article className="dash-panel" key={field}>
            <strong>{field}</strong>
            <small>Enabled · maps to cms_leads</small>
          </article>
        ))}
      </div>
    </section>
  );
}
