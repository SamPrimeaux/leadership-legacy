import { NavLink } from "react-router-dom";
import { idePrimaryNav, ideCMSNav } from "../data/ideNav.js";
import { Search, ExternalLink, PanelRight, GitBranch } from "lucide-react";

function NavGroup({ title, items }) {
  return (
    <div className="ide-nav-group">
      <span>{title}</span>
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink key={item.href} to={item.href} end={item.href === "/dashboard"}>
            <Icon size={17} />
            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </div>
  );
}

export function IDELayout({ children }) {
  return (
    <div className="ide-shell">
      <aside className="ide-activity">
        <div className="ide-logo">LL</div>
        <NavLink to="/dashboard/dev" title="IDE Workspace"><PanelRight size={20} /></NavLink>
        <NavLink to="/dashboard/dev/agent" title="AI Agent"><Search size={20} /></NavLink>
        <NavLink to="/dashboard/settings/ai-providers" title="Providers"><GitBranch size={20} /></NavLink>
      </aside>

      <aside className="ide-sidebar">
        <div className="ide-brand">
          <strong>Leadership Legacy</strong>
          <small>Cursor-style CMS IDE</small>
        </div>

        <NavGroup title="Workspace" items={idePrimaryNav} />
        <NavGroup title="CMS" items={ideCMSNav} />
      </aside>

      <div className="ide-main">
        <header className="ide-topbar">
          <div className="ide-command">
            <Search size={16} />
            <input placeholder="Search files, pages, leads, commands" aria-label="Search dashboard" />
          </div>

          <div className="ide-top-actions">
            <span className="ide-branch"><GitBranch size={14} /> main</span>
            <a href="/" target="_blank" rel="noreferrer">View site <ExternalLink size={14} /></a>
            <span className="ide-status">OpenAI ready</span>
          </div>
        </header>

        <main className="ide-content">
          {children}
        </main>
      </div>
    </div>
  );
}
