import React from "react";
import { createRoot } from "react-dom/client";
import "./dashboard.css";

function DashboardApp() {
  const cards = ["Pages", "Media", "Case Studies", "Services", "Leads", "Analytics", "Publishing", "Settings"];

  return (
    <div className="dash-shell">
      <aside className="dash-sidebar">
        <strong>Leadership Legacy</strong>
        <small>CMS Dashboard</small>
        <nav>
          {cards.map((card) => <a key={card} href="#">{card}</a>)}
        </nav>
      </aside>
      <main className="dash-main">
        <header className="dash-topbar">
          <div>
            <strong>Connor McNeely / Leadership Legacy</strong>
            <small>Live CMS, publishing, analytics, and intake operations</small>
          </div>
          <span>Saved</span>
        </header>
        <section className="dash-content">
          <p className="dash-eyebrow">Overview</p>
          <h1>CMS command center</h1>
          <div className="dash-grid">
            {cards.map((card) => (
              <article className="dash-card" key={card}>
                <span>{card}</span>
                <strong>Ready</strong>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

createRoot(document.getElementById("dashboard-root")).render(
  <React.StrictMode>
    <DashboardApp />
  </React.StrictMode>
);
