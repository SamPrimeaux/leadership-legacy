import { Link, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import { Menu, X, Moon, Sun, ChevronDown } from "lucide-react";
import { navItems } from "../../config/nav.config.js";
import "./core.css";

function getInitialTheme() {
  if (typeof window === "undefined") return "dark";
  const stored = window.localStorage.getItem("ll-theme");
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

export function Header() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem("ll-theme", theme);
  }, [theme]);

  useEffect(() => {
    document.body.style.overflow = drawerOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [drawerOpen]);

  function closeDrawer() {
    setDrawerOpen(false);
  }

  function toggleTheme() {
    setTheme((current) => (current === "dark" ? "light" : "dark"));
  }

  return (
    <>
      <header className="site-header">
        <div className="container header-inner">
          <Link className="brand" to="/" aria-label="Leadership Legacy home">
            <span className="brand-mark">LL</span>
            <span className="brand-copy">
              <strong>Leadership Legacy</strong>
              <small>Connor McNeely</small>
            </span>
          </Link>

          <nav className="desktop-nav" aria-label="Primary navigation">
            {navItems.map((item) => (
              <div className="nav-item" key={item.href}>
                <NavLink to={item.href}>
                  {item.label}
                  {item.children ? <ChevronDown size={14} /> : null}
                </NavLink>

                {item.children ? (
                  <div className="nav-dropdown">
                    {item.children.map((child) => (
                      <NavLink key={child.href} to={child.href}>
                        {child.label}
                      </NavLink>
                    ))}
                  </div>
                ) : null}
              </div>
            ))}
          </nav>

          <div className="header-actions">
            <button className="theme-toggle" type="button" onClick={toggleTheme} aria-label="Toggle light and dark theme">
              {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
              <span>{theme === "dark" ? "Light" : "Dark"}</span>
            </button>

            <Link className="header-cta" to="/contact">
              Start a Project
            </Link>

            <button
              className="hamburger"
              type="button"
              aria-label="Open navigation"
              aria-expanded={drawerOpen}
              onClick={() => setDrawerOpen(true)}
            >
              <Menu size={24} />
            </button>
          </div>
        </div>
      </header>

      <div className={`drawer-backdrop ${drawerOpen ? "is-open" : ""}`} onClick={closeDrawer} />

      <aside className={`mobile-drawer ${drawerOpen ? "is-open" : ""}`} aria-hidden={!drawerOpen}>
        <div className="drawer-head">
          <Link className="brand" to="/" onClick={closeDrawer}>
            <span className="brand-mark">LL</span>
            <span className="brand-copy">
              <strong>Leadership Legacy</strong>
              <small>AI engineering studio</small>
            </span>
          </Link>

          <button className="drawer-close" type="button" onClick={closeDrawer} aria-label="Close navigation">
            <X size={22} />
          </button>
        </div>

        <nav className="drawer-nav" aria-label="Mobile navigation">
          {navItems.map((item) => (
            <div className="drawer-group" key={item.href}>
              <NavLink to={item.href} onClick={closeDrawer}>
                {item.label}
              </NavLink>

              {item.children ? (
                <div className="drawer-children">
                  {item.children.map((child) => (
                    <NavLink key={child.href} to={child.href} onClick={closeDrawer}>
                      {child.label}
                    </NavLink>
                  ))}
                </div>
              ) : null}
            </div>
          ))}
        </nav>

        <div className="drawer-footer">
          <button className="theme-toggle drawer-theme" type="button" onClick={toggleTheme}>
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
            <span>{theme === "dark" ? "Switch to light" : "Switch to dark"}</span>
          </button>

          <Link className="btn" to="/contact" onClick={closeDrawer}>
            Start a Project
          </Link>

          <a className="drawer-dashboard" href="/dashboard">
            Dashboard
          </a>
        </div>
      </aside>
    </>
  );
}
