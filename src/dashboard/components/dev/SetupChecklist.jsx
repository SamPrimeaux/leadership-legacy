import { setupChecklist } from "../../data/devCockpitData.js";

export function SetupChecklist() {
  return (
    <section className="dev-panel">
      <div className="dev-panel-head">
        <div>
          <p className="dash-eyebrow">Connor Setup</p>
          <h2>Guided onboarding checklist</h2>
        </div>
        <span className="dev-badge">PowerShell-friendly</span>
      </div>

      <div className="setup-grid">
        {setupChecklist.map((group) => (
          <article className="setup-card" key={group.group}>
            <h3>{group.group}</h3>
            <div className="check-list">
              {group.items.map((item) => (
                <label key={item}>
                  <input type="checkbox" />
                  <span>{item}</span>
                </label>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
