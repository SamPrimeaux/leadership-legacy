import { NavLink } from "react-router-dom";
import { dashboardNav } from "../data/dashboardNav.js";
import { Search, ExternalLink } from "lucide-react";

export function DashboardShell({ children }) {
  return (
    <div className="dash-shell">
      <aside className="dash-sidebar">
        <a className="dash-brand" href="/dashboard" aria-label="Dashboard home">
          <span>LL</span>
          <div>
            <strong>Leadership Legacy</strong>
            <small>CMS Dashboard</small>
          </div>
        </a>

        <nav className="dash-nav" aria-label="Dashboard navigation">
          {dashboardNav.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.href} to={item.href} end={item.href === "/dashboard"}>
                <Icon size={17} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <div className="dash-main">
        <header className="dash-topbar">
          <div className="dash-search">
            <Search size={16} />
            <input aria-label="Search dashboard" placeholder="Search pages, leads, media, models" />
          </div>
          <div className="dash-top-actions">
            <a href="/" target="_blank" rel="noreferrer">
              View site <ExternalLink size={14} />
            </a>
            <span className="save-pill">Saved</span>
          </div>
        </header>

        <main className="dash-content">{children}</main>
      </div>
    </div>
  );
}
