#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()

def run(cmd, check=True):
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result

def write(path, content):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"wrote {path}")

def main():
    write("src/shared/brand/tokens.css", r'''
    :root {
      --font-display: "Satoshi", "Inter", system-ui, sans-serif;
      --font-body: "Inter", system-ui, sans-serif;
      --font-mono: "JetBrains Mono", "SFMono-Regular", monospace;

      --radius-sm: 10px;
      --radius-md: 16px;
      --radius-lg: 24px;
      --radius-xl: 32px;

      --container: 1180px;
      --header-height: 76px;

      --shadow-soft: 0 24px 80px rgba(0, 0, 0, 0.32);
      --shadow-glow: 0 0 70px rgba(56, 189, 248, 0.18);
    }

    :root,
    html[data-theme="dark"] {
      --color-bg: #070b12;
      --color-bg-soft: #0d1320;
      --color-surface: #111827;
      --color-surface-elevated: #172033;
      --color-text: #f5f7fb;
      --color-text-muted: #9ca8bd;
      --color-text-soft: #6f7d95;
      --color-primary: #38bdf8;
      --color-primary-strong: #0ea5e9;
      --color-accent: #22c55e;
      --color-accent-warm: #f59e0b;
      --color-border: rgba(148, 163, 184, 0.18);
      --color-glass: rgba(15, 23, 42, 0.72);
      --color-glass-strong: rgba(7, 11, 18, 0.9);
      --page-gradient-a: rgba(56, 189, 248, 0.16);
      --page-gradient-b: rgba(34, 197, 94, 0.08);
    }

    html[data-theme="light"] {
      --color-bg: #f7fafc;
      --color-bg-soft: #eef5f9;
      --color-surface: #ffffff;
      --color-surface-elevated: #eef6fb;
      --color-text: #07111f;
      --color-text-muted: #4b5f76;
      --color-text-soft: #6d7f93;
      --color-primary: #0284c7;
      --color-primary-strong: #0369a1;
      --color-accent: #16a34a;
      --color-accent-warm: #d97706;
      --color-border: rgba(15, 23, 42, 0.14);
      --color-glass: rgba(255, 255, 255, 0.74);
      --color-glass-strong: rgba(255, 255, 255, 0.92);
      --page-gradient-a: rgba(2, 132, 199, 0.15);
      --page-gradient-b: rgba(22, 163, 74, 0.09);
    }
    ''')

    write("src/styles/globals.css", r'''
    @import "../shared/brand/tokens.css";

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
      background: var(--color-bg);
    }

    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at 20% 10%, var(--page-gradient-a), transparent 28rem),
        radial-gradient(circle at 80% 0%, var(--page-gradient-b), transparent 26rem),
        var(--color-bg);
      color: var(--color-text);
      font-family: var(--font-body);
      transition: background 220ms ease, color 220ms ease;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: 0.34;
      background-image:
        linear-gradient(rgba(56, 189, 248, 0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.06) 1px, transparent 1px);
      background-size: 52px 52px;
      mask-image: radial-gradient(circle at 50% 0%, black, transparent 72%);
      z-index: -1;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    button,
    input,
    textarea,
    select {
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    img {
      max-width: 100%;
      display: block;
    }

    .container {
      width: min(var(--container), calc(100% - 40px));
      margin-inline: auto;
    }

    .section {
      padding: 104px 0;
      position: relative;
    }

    .section:nth-of-type(even) {
      background:
        linear-gradient(180deg, transparent, rgba(56, 189, 248, 0.035), transparent),
        rgba(148, 163, 184, 0.025);
      border-block: 1px solid var(--color-border);
    }

    .eyebrow {
      color: var(--color-primary);
      font-family: var(--font-mono);
      font-size: 0.78rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font-weight: 800;
    }

    .section-title {
      font-family: var(--font-display);
      font-size: clamp(2.4rem, 6vw, 6rem);
      line-height: 0.95;
      letter-spacing: -0.06em;
      max-width: 930px;
      margin: 14px 0 20px;
    }

    .muted,
    .rich-copy {
      color: var(--color-text-muted);
      font-size: 1.1rem;
      max-width: 790px;
      line-height: 1.7;
    }

    .gradient-text {
      background: linear-gradient(120deg, var(--color-text), var(--color-primary), var(--color-accent));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }

    .glass-card {
      background: var(--color-glass);
      border: 1px solid var(--color-border);
      box-shadow: var(--shadow-soft);
      backdrop-filter: blur(18px);
      border-radius: var(--radius-lg);
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 44px;
      padding: 0 18px;
      border-radius: 999px;
      font-weight: 850;
      border: 1px solid transparent;
      background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
      color: #04111f;
      transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .btn:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-glow);
    }

    .btn.secondary {
      color: var(--color-text);
      background: var(--color-glass);
      border-color: var(--color-border);
      backdrop-filter: blur(14px);
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }

    .card {
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      background: var(--color-glass);
      backdrop-filter: blur(16px);
      padding: 24px;
      box-shadow: var(--shadow-soft);
      transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
    }

    .card:hover {
      transform: translateY(-4px);
      border-color: rgba(56, 189, 248, 0.36);
    }

    .card p {
      color: var(--color-text-muted);
    }

    .chip-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 18px;
    }

    .chip-row span {
      border: 1px solid var(--color-border);
      border-radius: 999px;
      padding: 6px 10px;
      color: var(--color-text-muted);
      font-size: 0.82rem;
      font-weight: 800;
    }

    @media (max-width: 900px) {
      .card-grid {
        grid-template-columns: 1fr;
      }

      .section {
        padding: 76px 0;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        animation-duration: 0.001ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: 0.001ms !important;
      }
    }
    ''')

    write("src/config/nav.config.js", r'''
    export const navItems = [
      {
        label: "Services",
        href: "/services",
        children: [
          { label: "AI Engineering", href: "/services/ai-engineering" },
          { label: "RAG Systems", href: "/services/rag-systems" },
          { label: "Full-Stack Apps", href: "/services/full-stack-apps" },
          { label: "CAD Automation", href: "/services/cad-automation" },
          { label: "CAD-to-Video", href: "/services/cad-to-video" },
          { label: "Business Automation", href: "/services/business-automation" },
          { label: "Consulting", href: "/services/consulting" }
        ]
      },
      { label: "Work", href: "/work" },
      { label: "About", href: "/about" },
      { label: "Resources", href: "/resources" },
      { label: "Contact", href: "/contact" }
    ];
    ''')

    write("src/components/core/Header.jsx", r'''
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
    ''')

    write("src/components/core/Footer.jsx", r'''
    import { Link } from "react-router-dom";
    import { ArrowUpRight } from "lucide-react";
    import { navItems } from "../../config/nav.config.js";
    import "./core.css";

    export function Footer() {
      return (
        <footer className="site-footer">
          <div className="container footer-feature glass-card">
            <p className="eyebrow">Leadership Legacy Digital</p>
            <h2>Engineering-grade AI systems for technical businesses.</h2>
            <p>
              Connor McNeely blends mechanical engineering discipline with AI systems,
              automation, CAD workflows, RAG, and full-stack product development.
            </p>
            <div className="footer-feature-actions">
              <Link className="btn" to="/contact">Start a Project</Link>
              <Link className="btn secondary" to="/work">View Work</Link>
            </div>
          </div>

          <div className="container footer-grid">
            <div>
              <Link className="brand footer-brand" to="/">
                <span className="brand-mark">LL</span>
                <span className="brand-copy">
                  <strong>Leadership Legacy</strong>
                  <small>Connor McNeely</small>
                </span>
              </Link>
              <p>
                Mechanical engineering precision, AI workflow design, and production-minded
                software delivery for teams that need systems that hold up.
              </p>
            </div>

            <div className="footer-column">
              <h3>Site</h3>
              {navItems.map((item) => (
                <Link key={item.href} to={item.href}>{item.label}</Link>
              ))}
            </div>

            <div className="footer-column">
              <h3>Build lanes</h3>
              <Link to="/services/ai-engineering">AI Engineering</Link>
              <Link to="/services/rag-systems">RAG Systems</Link>
              <Link to="/services/cad-automation">CAD Automation</Link>
              <Link to="/services/full-stack-apps">Full-Stack Apps</Link>
            </div>

            <div className="footer-column">
              <h3>Operations</h3>
              <a href="/dashboard">Dashboard <ArrowUpRight size={13} /></a>
              <Link to="/privacy">Privacy</Link>
              <Link to="/terms">Terms</Link>
            </div>
          </div>

          <div className="container footer-bottom">
            <span>© {new Date().getFullYear()} Leadership Legacy Digital.</span>
            <span>Built for precision, clarity, and real-world systems.</span>
          </div>
        </footer>
      );
    }
    ''')

    write("src/components/core/core.css", r'''
    .site-header {
      position: sticky;
      top: 0;
      z-index: 80;
      border-bottom: 1px solid var(--color-border);
      background: var(--color-glass);
      backdrop-filter: blur(20px);
      box-shadow: 0 12px 34px rgba(0, 0, 0, 0.16);
    }

    .header-inner {
      min-height: var(--header-height);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      min-width: fit-content;
    }

    .brand-mark {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 14px;
      background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
      color: #04111f;
      font-weight: 950;
      letter-spacing: -0.08em;
      box-shadow: 0 0 36px rgba(56, 189, 248, 0.25);
    }

    .brand-copy strong,
    .brand-copy small {
      display: block;
      line-height: 1.1;
    }

    .brand-copy small {
      color: var(--color-text-muted);
      font-size: 0.76rem;
      font-weight: 700;
    }

    .desktop-nav {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 7px;
      border: 1px solid var(--color-border);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.035);
    }

    .nav-item {
      position: relative;
    }

    .nav-item > a {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: var(--color-text-muted);
      font-weight: 850;
      font-size: 0.9rem;
      min-height: 36px;
      padding: 0 12px;
      border-radius: 999px;
      transition: color 160ms ease, background 160ms ease;
    }

    .nav-item > a:hover,
    .nav-item > a.active {
      color: var(--color-text);
      background: rgba(56, 189, 248, 0.1);
    }

    .nav-dropdown {
      position: absolute;
      top: calc(100% + 12px);
      left: 0;
      width: 260px;
      padding: 10px;
      border: 1px solid var(--color-border);
      border-radius: 20px;
      background: var(--color-glass-strong);
      backdrop-filter: blur(20px);
      box-shadow: var(--shadow-soft);
      opacity: 0;
      pointer-events: none;
      transform: translateY(8px);
      transition: 160ms ease;
    }

    .nav-item:hover .nav-dropdown,
    .nav-item:focus-within .nav-dropdown {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }

    .nav-dropdown a {
      display: block;
      padding: 10px 12px;
      border-radius: 13px;
      color: var(--color-text-muted);
      font-weight: 800;
      transition: 160ms ease;
    }

    .nav-dropdown a:hover,
    .nav-dropdown a.active {
      color: var(--color-text);
      background: rgba(56, 189, 248, 0.1);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .theme-toggle,
    .hamburger,
    .drawer-close,
    .header-cta {
      min-height: 42px;
      border-radius: 999px;
      border: 1px solid var(--color-border);
      background: rgba(255, 255, 255, 0.04);
      color: var(--color-text);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 0 13px;
      font-weight: 850;
      backdrop-filter: blur(14px);
    }

    .theme-toggle span {
      font-size: 0.88rem;
    }

    .header-cta {
      color: #04111f;
      border-color: transparent;
      background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
    }

    .hamburger {
      display: none;
      width: 44px;
      padding: 0;
    }

    .drawer-backdrop {
      position: fixed;
      inset: 0;
      z-index: 90;
      background: rgba(0, 0, 0, 0.52);
      backdrop-filter: blur(4px);
      opacity: 0;
      pointer-events: none;
      transition: opacity 180ms ease;
    }

    .drawer-backdrop.is-open {
      opacity: 1;
      pointer-events: auto;
    }

    .mobile-drawer {
      position: fixed;
      inset: 0 0 0 auto;
      z-index: 100;
      width: min(50vw, 430px);
      min-width: 330px;
      padding: 20px;
      border-left: 1px solid var(--color-border);
      background: var(--color-glass-strong);
      backdrop-filter: blur(24px);
      box-shadow: -28px 0 80px rgba(0, 0, 0, 0.38);
      transform: translateX(104%);
      transition: transform 220ms ease;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 22px;
    }

    .mobile-drawer.is-open {
      transform: translateX(0);
    }

    .drawer-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--color-border);
    }

    .drawer-close {
      width: 42px;
      padding: 0;
    }

    .drawer-nav {
      display: grid;
      align-content: start;
      gap: 10px;
      overflow-y: auto;
    }

    .drawer-group {
      display: grid;
      gap: 7px;
    }

    .drawer-group > a {
      color: var(--color-text);
      font-size: 1.14rem;
      font-weight: 900;
      padding: 10px 0;
    }

    .drawer-children {
      display: grid;
      gap: 4px;
      padding: 0 0 8px 16px;
      border-left: 1px solid var(--color-border);
    }

    .drawer-children a {
      color: var(--color-text-muted);
      padding: 6px 0;
      font-weight: 750;
    }

    .drawer-footer {
      display: grid;
      gap: 12px;
      border-top: 1px solid var(--color-border);
      padding-top: 18px;
    }

    .drawer-theme {
      justify-content: flex-start;
      width: 100%;
    }

    .drawer-dashboard {
      color: var(--color-text-muted);
      font-family: var(--font-mono);
      font-size: 0.86rem;
      text-align: center;
    }

    .site-footer {
      padding: 88px 0 30px;
      border-top: 1px solid var(--color-border);
      background:
        radial-gradient(circle at 20% 10%, var(--page-gradient-a), transparent 26rem),
        var(--color-bg-soft);
    }

    .footer-feature {
      padding: clamp(28px, 6vw, 64px);
      margin-bottom: 46px;
    }

    .footer-feature h2 {
      font-family: var(--font-display);
      font-size: clamp(2rem, 5vw, 4.8rem);
      line-height: 0.95;
      letter-spacing: -0.06em;
      margin: 12px 0;
      max-width: 940px;
    }

    .footer-feature p:not(.eyebrow) {
      color: var(--color-text-muted);
      max-width: 780px;
      line-height: 1.7;
    }

    .footer-feature-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 24px;
    }

    .footer-grid {
      display: grid;
      grid-template-columns: 1.35fr repeat(3, 0.7fr);
      gap: 38px;
    }

    .footer-grid p {
      color: var(--color-text-muted);
      max-width: 440px;
      line-height: 1.7;
    }

    .footer-brand {
      margin-bottom: 18px;
    }

    .footer-column {
      display: grid;
      align-content: start;
      gap: 10px;
    }

    .footer-column h3 {
      margin: 0 0 6px;
      font-size: 0.9rem;
      color: var(--color-text);
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }

    .footer-column a {
      color: var(--color-text-muted);
      font-weight: 750;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .footer-column a:hover {
      color: var(--color-primary);
    }

    .footer-bottom {
      margin-top: 46px;
      padding-top: 20px;
      border-top: 1px solid var(--color-border);
      display: flex;
      justify-content: space-between;
      gap: 20px;
      color: var(--color-text-soft);
      font-size: 0.9rem;
    }

    @media (max-width: 1040px) {
      .desktop-nav,
      .header-cta,
      .theme-toggle span {
        display: none;
      }

      .hamburger {
        display: inline-flex;
      }

      .footer-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    @media (max-width: 680px) {
      .mobile-drawer {
        width: min(88vw, 430px);
        min-width: unset;
      }

      .brand-copy strong {
        font-size: 0.95rem;
      }

      .brand-copy small {
        display: none;
      }

      .footer-grid,
      .footer-bottom {
        grid-template-columns: 1fr;
        flex-direction: column;
      }
    }
    ''')

    write("src/dashboard/components/DashboardAuthGate.jsx", r'''
    import { useState } from "react";
    import { LockKeyhole } from "lucide-react";

    const STORAGE_KEY = "ll-dashboard-authenticated";
    const DRAFT_PASSWORD = "1234";

    function hasSession() {
      if (typeof window === "undefined") return false;
      return window.sessionStorage.getItem(STORAGE_KEY) === "true";
    }

    export function DashboardAuthGate({ children }) {
      const [authenticated, setAuthenticated] = useState(hasSession);
      const [password, setPassword] = useState("");
      const [error, setError] = useState("");

      function handleSubmit(event) {
        event.preventDefault();

        if (password === DRAFT_PASSWORD) {
          window.sessionStorage.setItem(STORAGE_KEY, "true");
          setAuthenticated(true);
          setError("");
          return;
        }

        setError("Incorrect draft password.");
      }

      if (authenticated) {
        return children;
      }

      return (
        <main className="dashboard-auth-page">
          <form className="dashboard-auth-card" onSubmit={handleSubmit}>
            <div className="auth-icon">
              <LockKeyhole size={24} />
            </div>

            <p className="dash-eyebrow">Protected Draft</p>
            <h1>Leadership Legacy Dashboard</h1>
            <p>
              This concept dashboard is password protected while the CMS, R2, AI routing,
              analytics, and publishing workflows are being drafted.
            </p>

            <label>
              Password
              <input
                autoFocus
                type="password"
                inputMode="numeric"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter draft password"
              />
            </label>

            {error ? <span className="auth-error">{error}</span> : null}

            <button className="primary-action" type="submit">
              Unlock Dashboard
            </button>

            <small>Draft password for concept review: 1234</small>
          </form>
        </main>
      );
    }
    ''')

    # Patch DashboardApp to wrap shell with auth gate.
    app_path = ROOT / "src/dashboard/DashboardApp.jsx"
    if app_path.exists():
      app = app_path.read_text()
      if "DashboardAuthGate" not in app:
        app = app.replace(
          'import { DashboardShell } from "./layouts/DashboardShell.jsx";',
          'import { DashboardShell } from "./layouts/DashboardShell.jsx";\nimport { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";'
        )
        app = app.replace(
          "return (\n        <DashboardShell>",
          "return (\n        <DashboardAuthGate>\n        <DashboardShell>"
        )
        app = app.replace(
          "        </DashboardShell>\n      );",
          "        </DashboardShell>\n        </DashboardAuthGate>\n      );"
        )
        app_path.write_text(app)
        print("patched DashboardApp.jsx with password auth gate")

    # If previous DashboardApp formatting differs, overwrite it safely with known full route shell.
    write("src/dashboard/DashboardApp.jsx", r'''
    import { Routes, Route, Navigate } from "react-router-dom";
    import { DashboardShell } from "./layouts/DashboardShell.jsx";
    import { DashboardAuthGate } from "./components/DashboardAuthGate.jsx";
    import { DashboardHome } from "./pages/DashboardHome.jsx";
    import { CMSPages } from "./pages/CMSPages.jsx";
    import { CMSPageEditor } from "./pages/CMSPageEditor.jsx";
    import { MediaLibrary } from "./pages/MediaLibrary.jsx";
    import { CaseStudies } from "./pages/CaseStudies.jsx";
    import { Services } from "./pages/Services.jsx";
    import { Leads } from "./pages/Leads.jsx";
    import { IntakeForms } from "./pages/IntakeForms.jsx";
    import { Analytics } from "./pages/Analytics.jsx";
    import { Publishing } from "./pages/Publishing.jsx";
    import { Settings } from "./pages/Settings.jsx";
    import { AIProviders } from "./pages/AIProviders.jsx";
    import { R2Storage } from "./pages/R2Storage.jsx";
    import { NotFoundDashboard } from "./pages/NotFoundDashboard.jsx";

    export default function DashboardApp() {
      return (
        <DashboardAuthGate>
          <DashboardShell>
            <Routes>
              <Route path="/dashboard" element={<DashboardHome />} />
              <Route path="/dashboard/pages" element={<CMSPages />} />
              <Route path="/dashboard/pages/:pageId" element={<CMSPageEditor />} />
              <Route path="/dashboard/sections" element={<CMSPages />} />
              <Route path="/dashboard/media" element={<MediaLibrary />} />
              <Route path="/dashboard/storage" element={<R2Storage />} />
              <Route path="/dashboard/case-studies" element={<CaseStudies />} />
              <Route path="/dashboard/case-studies/:caseStudyId" element={<CaseStudies />} />
              <Route path="/dashboard/services" element={<Services />} />
              <Route path="/dashboard/services/:serviceId" element={<Services />} />
              <Route path="/dashboard/leads" element={<Leads />} />
              <Route path="/dashboard/leads/:leadId" element={<Leads />} />
              <Route path="/dashboard/forms" element={<IntakeForms />} />
              <Route path="/dashboard/analytics" element={<Analytics />} />
              <Route path="/dashboard/publishing" element={<Publishing />} />
              <Route path="/dashboard/settings" element={<Settings />} />
              <Route path="/dashboard/settings/brand" element={<Settings section="brand" />} />
              <Route path="/dashboard/settings/navigation" element={<Settings section="navigation" />} />
              <Route path="/dashboard/settings/seo" element={<Settings section="seo" />} />
              <Route path="/dashboard/settings/ai-providers" element={<AIProviders />} />
              <Route path="/dashboard/login" element={<Navigate to="/dashboard" replace />} />
              <Route path="*" element={<NotFoundDashboard />} />
            </Routes>
          </DashboardShell>
        </DashboardAuthGate>
      );
    }
    ''')

    # Append dashboard auth CSS without destroying current dashboard.css.
    dash_css_path = ROOT / "src/dashboard/dashboard.css"
    existing = dash_css_path.read_text() if dash_css_path.exists() else ""
    auth_css = r'''
    .dashboard-auth-page {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
      background:
        radial-gradient(circle at 20% 10%, rgba(56, 189, 248, 0.18), transparent 28rem),
        radial-gradient(circle at 80% 0%, rgba(34, 197, 94, 0.1), transparent 26rem),
        #050812;
    }

    .dashboard-auth-card {
      width: min(100%, 480px);
      display: grid;
      gap: 16px;
      padding: 34px;
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 28px;
      background: rgba(15, 23, 42, 0.78);
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.42);
      backdrop-filter: blur(22px);
    }

    .dashboard-auth-card h1 {
      margin: 0;
      font-size: clamp(2.1rem, 6vw, 4rem);
      line-height: 0.95;
      letter-spacing: -0.06em;
    }

    .dashboard-auth-card p,
    .dashboard-auth-card small {
      color: #94a3b8;
      line-height: 1.6;
    }

    .dashboard-auth-card label {
      display: grid;
      gap: 8px;
      color: #cbd5e1;
      font-weight: 800;
    }

    .dashboard-auth-card input {
      min-height: 48px;
      border-radius: 16px;
    }

    .auth-icon {
      width: 52px;
      height: 52px;
      display: grid;
      place-items: center;
      border-radius: 18px;
      color: #04111f;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      box-shadow: 0 0 50px rgba(56, 189, 248, 0.24);
    }

    .auth-error {
      color: #fecaca;
      border: 1px solid rgba(239, 68, 68, 0.28);
      background: rgba(239, 68, 68, 0.1);
      border-radius: 14px;
      padding: 10px 12px;
      font-weight: 800;
    }
    '''
    if ".dashboard-auth-page" not in existing:
      dash_css_path.write_text(existing + "\n\n" + textwrap.dedent(auth_css), encoding="utf-8")
      print("patched dashboard.css with auth gate styles")

    write("docs/HEADER_FOOTER_AUTH.md", r'''
    # Header, Footer, Theme, and Dashboard Auth

    ## Public Header

    The public app now has a branded glassmorphic header with:

    - Leadership Legacy / Connor McNeely brand lockup
    - Desktop dropdown navigation
    - Light/dark theme toggle
    - Header CTA
    - Mobile hamburger
    - 50vw-style slide-out drawer navigation on tablet/mobile

    ## Public Footer

    The footer now has:

    - Large conversion band
    - Brand summary
    - Site navigation
    - Build lane navigation
    - Dashboard/legal links
    - Glassmorphic premium style

    ## Theme

    Theme is stored in:

    ```txt
    localStorage["ll-theme"]
    ```

    It toggles:

    ```txt
    html[data-theme="dark"]
    html[data-theme="light"]
    ```

    ## Dashboard Password Gate

    The dashboard concept is protected by a client-side draft password:

    ```txt
    1234
    ```

    This is only for concept/demo protection. Production should replace this with real auth:

    - Cloudflare Access
    - Supabase Auth
    - GitHub OAuth
    - Magic link
    - Session cookies
    - Server-side role checks
    ''')

    run(["npm", "run", "build"], check=True)
    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", "feat: add branded header footer theme drawer and dashboard password gate"], check=False)

    print("\nHeader/footer/theme/dashboard auth upgrade complete.")
    print("Next:")
    print("npm run deploy")
    print("open https://leadership-legacy.meauxbility.workers.dev/")
    print("open https://leadership-legacy.meauxbility.workers.dev/dashboard")
    print("Dashboard draft password: 1234")

if __name__ == "__main__":
    main()
