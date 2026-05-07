#!/usr/bin/env python3
from pathlib import Path
import json
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

def update_package():
    pkg_path = ROOT / "package.json"
    pkg = json.loads(pkg_path.read_text())
    pkg.setdefault("scripts", {})
    pkg["scripts"]["dev"] = "vite"
    pkg["scripts"]["build"] = "vite build"
    pkg["scripts"]["preview"] = "vite preview"
    pkg["scripts"]["deploy"] = "npm run build && wrangler deploy"
    pkg["scripts"]["cf:preview"] = "npm run build && wrangler dev"
    pkg["scripts"]["sitemap"] = "node scripts/build-sitemap.js"
    deps = pkg.setdefault("dependencies", {})
    deps["@vitejs/plugin-react"] = deps.get("@vitejs/plugin-react", "latest")
    deps["vite"] = deps.get("vite", "latest")
    deps["react"] = deps.get("react", "latest")
    deps["react-dom"] = deps.get("react-dom", "latest")
    deps["react-router-dom"] = deps.get("react-router-dom", "latest")
    deps["lucide-react"] = deps.get("lucide-react", "latest")
    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")
    print("updated package.json")

def main():
    update_package()

    write("wrangler.jsonc", r'''
    {
      "$schema": "./node_modules/wrangler/config-schema.json",
      "name": "leadership-legacy",
      "main": "src/worker/index.js",
      "compatibility_date": "2026-05-06",
      "assets": {
        "directory": "./dist",
        "binding": "ASSETS",
        "run_worker_first": [
          "/dashboard",
          "/dashboard/*",
          "/api/*",
          "/services/*",
          "/work/*",
          "/resources/*",
          "/about",
          "/contact",
          "/privacy",
          "/terms"
        ]
      },
      "observability": {
        "enabled": true
      }
    }
    ''')

    write("src/worker/index.js", r'''
    function assetRequest(request, assetPath) {
      const url = new URL(request.url);
      url.pathname = assetPath;
      url.search = "";
      return new Request(url.toString(), {
        method: "GET",
        headers: request.headers
      });
    }

    function json(data, status = 200) {
      return new Response(JSON.stringify(data, null, 2), {
        status,
        headers: {
          "content-type": "application/json; charset=utf-8",
          "cache-control": "no-store"
        }
      });
    }

    export default {
      async fetch(request, env) {
        const url = new URL(request.url);
        const pathname = url.pathname;

        if (pathname.startsWith("/api/health")) {
          return json({
            ok: true,
            app: "leadership-legacy",
            surface: "worker",
            timestamp: new Date().toISOString()
          });
        }

        if (pathname.startsWith("/api/ai/providers")) {
          return json({
            providers: [
              {
                key: "openai",
                displayName: "OpenAI",
                status: "configured_by_secret",
                secretName: "OPENAI_API_KEY",
                dashboardUse: ["chat", "routing", "image_generation", "evals"]
              },
              {
                key: "anthropic",
                displayName: "Anthropic",
                status: "configured_by_secret",
                secretName: "ANTHROPIC_API_KEY",
                dashboardUse: ["chat", "routing", "code_review", "evals"]
              }
            ],
            note: "Secrets are never exposed to the browser. This endpoint only reports provider capability metadata."
          });
        }

        // Hard fix for /dashboard redirect loops:
        // Never redirect. Always serve dashboard.html directly for /dashboard and /dashboard/*.
        if (pathname === "/dashboard" || pathname.startsWith("/dashboard/")) {
          return env.ASSETS.fetch(assetRequest(request, "/dashboard.html"));
        }

        const asset = await env.ASSETS.fetch(request);
        if (asset.status !== 404) return asset;

        // SPA fallback for public React routes.
        if (
          request.method === "GET" &&
          (request.headers.get("accept") || "").includes("text/html") &&
          !pathname.includes(".")
        ) {
          return env.ASSETS.fetch(assetRequest(request, "/index.html"));
        }

        return asset;
      }
    };
    ''')

    write("dashboard.html", r'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="robots" content="noindex,nofollow" />
        <title>Dashboard | Leadership Legacy Digital</title>
      </head>
      <body>
        <div id="dashboard-root"></div>
        <script type="module" src="/src/dashboard/main.jsx"></script>
      </body>
    </html>
    ''')

    write("src/dashboard/main.jsx", r'''
    import React from "react";
    import { createRoot } from "react-dom/client";
    import { BrowserRouter } from "react-router-dom";
    import DashboardApp from "./DashboardApp.jsx";
    import "./dashboard.css";

    createRoot(document.getElementById("dashboard-root")).render(
      <React.StrictMode>
        <BrowserRouter>
          <DashboardApp />
        </BrowserRouter>
      </React.StrictMode>
    );
    ''')

    write("src/dashboard/DashboardApp.jsx", r'''
    import { Routes, Route, Navigate } from "react-router-dom";
    import { DashboardShell } from "./layouts/DashboardShell.jsx";
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
    import { NotFoundDashboard } from "./pages/NotFoundDashboard.jsx";

    export default function DashboardApp() {
      return (
        <DashboardShell>
          <Routes>
            <Route path="/dashboard" element={<DashboardHome />} />
            <Route path="/dashboard/pages" element={<CMSPages />} />
            <Route path="/dashboard/pages/:pageId" element={<CMSPageEditor />} />
            <Route path="/dashboard/sections" element={<CMSPages />} />
            <Route path="/dashboard/media" element={<MediaLibrary />} />
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
      );
    }
    ''')

    write("src/dashboard/data/dashboardNav.js", r'''
    import {
      LayoutDashboard,
      FileText,
      Layers,
      Image,
      Briefcase,
      Wrench,
      Inbox,
      ClipboardList,
      BarChart3,
      Rocket,
      Settings,
      BrainCircuit
    } from "lucide-react";

    export const dashboardNav = [
      { label: "Overview", href: "/dashboard", icon: LayoutDashboard },
      { label: "Pages", href: "/dashboard/pages", icon: FileText },
      { label: "Sections", href: "/dashboard/sections", icon: Layers },
      { label: "Media", href: "/dashboard/media", icon: Image },
      { label: "Case Studies", href: "/dashboard/case-studies", icon: Briefcase },
      { label: "Services", href: "/dashboard/services", icon: Wrench },
      { label: "Leads", href: "/dashboard/leads", icon: Inbox },
      { label: "Forms", href: "/dashboard/forms", icon: ClipboardList },
      { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
      { label: "Publishing", href: "/dashboard/publishing", icon: Rocket },
      { label: "AI Providers", href: "/dashboard/settings/ai-providers", icon: BrainCircuit },
      { label: "Settings", href: "/dashboard/settings", icon: Settings }
    ];
    ''')

    write("src/dashboard/data/cmsData.js", r'''
    export const cmsPages = [
      {
        id: "home",
        title: "Home",
        slug: "/",
        status: "published",
        seoScore: 96,
        updatedAt: "2026-05-06",
        sections: [
          {
            id: "hero-home",
            type: "Founder Hero",
            props: {
              eyebrow: "Mechanical Engineer × AI Developer",
              heading: "Engineering-grade AI systems for technical businesses.",
              body:
                "Connor McNeely helps engineering teams, SaaS founders, and operators turn complex workflows, documents, CAD assets, and business bottlenecks into production-ready AI tools, automations, and web applications.",
              primaryCta: "Start a Project",
              secondaryCta: "View Work"
            }
          },
          {
            id: "services-home",
            type: "Services Grid",
            props: {
              heading: "AI systems, automation, CAD, and full-stack builds."
            }
          },
          {
            id: "work-home",
            type: "Featured Work",
            props: {
              heading: "Technical systems with practical outcomes."
            }
          }
        ]
      },
      {
        id: "about",
        title: "About",
        slug: "/about",
        status: "published",
        seoScore: 91,
        updatedAt: "2026-05-06",
        sections: []
      },
      {
        id: "services",
        title: "Services",
        slug: "/services",
        status: "draft",
        seoScore: 84,
        updatedAt: "2026-05-06",
        sections: []
      },
      {
        id: "work",
        title: "Work",
        slug: "/work",
        status: "review",
        seoScore: 88,
        updatedAt: "2026-05-06",
        sections: []
      }
    ];

    export const services = [
      {
        id: "ai-engineering",
        title: "AI Engineering",
        slug: "/services/ai-engineering",
        status: "published",
        price: "$5,000+",
        summary: "Custom AI tools, copilots, LLM integrations, and multi-agent workflows."
      },
      {
        id: "rag-systems",
        title: "RAG Systems",
        slug: "/services/rag-systems",
        status: "published",
        price: "$5,000+",
        summary: "Source-cited document intelligence for manuals, SOPs, support docs, and standards."
      },
      {
        id: "full-stack-apps",
        title: "Full-Stack AI Apps",
        slug: "/services/full-stack-apps",
        status: "draft",
        price: "$8,000+",
        summary: "React/Vite apps, dashboards, APIs, auth, database, payments, and AI features."
      },
      {
        id: "cad-automation",
        title: "CAD Automation",
        slug: "/services/cad-automation",
        status: "published",
        price: "$75/hr",
        summary: "SolidWorks workflows, BOM automation, drawings, and engineering documentation."
      }
    ];

    export const caseStudies = [
      {
        id: "mechassist-ai",
        title: "MechAssist AI",
        category: "RAG / Engineering AI",
        status: "published",
        stack: ["RAG", "Vector Search", "LLM", "Engineering Docs"],
        outcome: "Faster source-backed answers for technical documentation."
      },
      {
        id: "openclaw",
        title: "OpenClaw",
        category: "Multi-Agent AI",
        status: "draft",
        stack: ["Agents", "Automation", "CRM", "LLM"],
        outcome: "A live outbound AI workflow foundation."
      },
      {
        id: "evergrow-landscaping",
        title: "Evergrow Landscaping",
        category: "Lead Generation / CRM",
        status: "published",
        stack: ["Website", "CRM", "Chatbot", "Automation"],
        outcome: "Improved lead capture and structured follow-up."
      }
    ];

    export const leads = [
      {
        id: "lead_001",
        name: "Jordan Blake",
        email: "jordan@example.com",
        company: "Precision Pump Group",
        projectType: "RAG System",
        budget: "$5k–$15k",
        status: "new",
        source: "/services/rag-systems",
        createdAt: "2026-05-06"
      },
      {
        id: "lead_002",
        name: "Maya Chen",
        email: "maya@example.com",
        company: "CADOps Studio",
        projectType: "CAD Automation",
        budget: "$2k–$8k",
        status: "qualified",
        source: "/contact",
        createdAt: "2026-05-06"
      },
      {
        id: "lead_003",
        name: "Elliot Hayes",
        email: "elliot@example.com",
        company: "Founder",
        projectType: "Full-Stack AI App",
        budget: "$8k–$25k",
        status: "proposal",
        source: "/services/full-stack-apps",
        createdAt: "2026-05-05"
      }
    ];

    export const mediaAssets = [
      {
        id: "asset_001",
        name: "Connor Founder Portrait",
        type: "image",
        usage: "Founder",
        status: "ready",
        size: "420 KB"
      },
      {
        id: "asset_002",
        name: "Engineering Blueprint Texture",
        type: "texture",
        usage: "Background",
        status: "ready",
        size: "180 KB"
      },
      {
        id: "asset_003",
        name: "Rotating Pump GLB",
        type: "model",
        usage: "Hero / CAD",
        status: "needs optimization",
        size: "4.8 MB"
      }
    ];

    export const analyticsEvents = [
      { page: "/", views: 1240, cta: 88, leads: 12, conversion: "0.97%" },
      { page: "/services/rag-systems", views: 420, cta: 44, leads: 7, conversion: "1.67%" },
      { page: "/work/mechassist-ai", views: 318, cta: 21, leads: 3, conversion: "0.94%" },
      { page: "/contact", views: 210, cta: 0, leads: 18, conversion: "8.57%" }
    ];
    ''')

    write("src/dashboard/data/aiProviders.js", r'''
    export const aiProviders = [
      {
        key: "openai",
        displayName: "OpenAI",
        secretName: "OPENAI_API_KEY",
        status: "needs secret",
        useCases: ["routing", "chat", "coding", "image generation", "evals"],
        models: [
          {
            key: "gpt-5.4-nano",
            lane: "cheap_fast_router",
            enabled: true,
            notes: "Routing, classification, short summaries, metadata extraction."
          },
          {
            key: "gpt-5.4-mini",
            lane: "default_workhorse",
            enabled: true,
            notes: "Normal coding, CMS tasks, tool calls, dashboard help."
          },
          {
            key: "gpt-5.4",
            lane: "senior_reasoning",
            enabled: true,
            notes: "Architecture, schema design, security-sensitive reviews."
          },
          {
            key: "gpt-image-1-mini",
            lane: "budget_image_generation",
            enabled: true,
            notes: "Draft mockups, thumbnails, quick creative variations."
          },
          {
            key: "gpt-image-1.5",
            lane: "standard_image_generation",
            enabled: true,
            notes: "Client-facing brand visuals and higher quality image work."
          }
        ],
        blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"]
      },
      {
        key: "anthropic",
        displayName: "Anthropic",
        secretName: "ANTHROPIC_API_KEY",
        status: "needs secret",
        useCases: ["code review", "architecture", "agent review", "long-form reasoning"],
        models: [
          {
            key: "claude-sonnet",
            lane: "standard_senior_review",
            enabled: true,
            notes: "Code review, system planning, route/schema reasoning."
          },
          {
            key: "claude-haiku",
            lane: "cheap_fast_fallback",
            enabled: true,
            notes: "Low-cost summaries, validation, lightweight automation."
          }
        ],
        blockedModels: []
      }
    ];

    export const routingPolicy = {
      defaultTextModel: "gpt-5.4-mini",
      cheapTextModel: "gpt-5.4-nano",
      seniorTextModel: "gpt-5.4",
      defaultImageModel: "gpt-image-1-mini",
      standardImageModel: "gpt-image-1.5",
      reviewProvider: "anthropic",
      blockedModels: ["gpt-5.5", "gpt-5.5-pro", "gpt-5.4-pro"],
      router: "deterministic_guardrails_then_thompson_sampling",
      notes:
        "Secrets stay server-side. Browser dashboard only edits metadata, preferences, and model routing policy."
    };
    ''')

    write("src/dashboard/layouts/DashboardShell.jsx", r'''
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
    ''')

    write("src/dashboard/components/DataTable.jsx", r'''
    export function DataTable({ columns, rows, getRowHref }) {
      return (
        <div className="dash-table" role="table">
          <div className="dash-table-head" role="row">
            {columns.map((column) => (
              <span key={column.key} role="columnheader">{column.label}</span>
            ))}
          </div>
          {rows.map((row) => {
            const content = columns.map((column) => (
              <span key={column.key} role="cell">
                {column.render ? column.render(row) : row[column.key]}
              </span>
            ));

            if (getRowHref) {
              return (
                <a className="dash-table-row" role="row" href={getRowHref(row)} key={row.id}>
                  {content}
                </a>
              );
            }

            return (
              <div className="dash-table-row" role="row" key={row.id}>
                {content}
              </div>
            );
          })}
        </div>
      );
    }
    ''')

    write("src/dashboard/components/StatusBadge.jsx", r'''
    export function StatusBadge({ status }) {
      return <span className={`status-badge status-${String(status).replaceAll(" ", "-")}`}>{status}</span>;
    }
    ''')

    write("src/dashboard/components/MetricCard.jsx", r'''
    export function MetricCard({ label, value, detail }) {
      return (
        <article className="metric-card">
          <span>{label}</span>
          <strong>{value}</strong>
          {detail ? <small>{detail}</small> : null}
        </article>
      );
    }
    ''')

    write("src/dashboard/pages/DashboardHome.jsx", r'''
    import { MetricCard } from "../components/MetricCard.jsx";
    import { analyticsEvents, leads, cmsPages } from "../data/cmsData.js";

    export function DashboardHome() {
      const draftCount = cmsPages.filter((page) => page.status !== "published").length;

      return (
        <section>
          <p className="dash-eyebrow">Overview</p>
          <h1>CMS command center</h1>
          <p className="dash-subtitle">
            Manage Connor’s public site, live CMS content, leads, analytics, publishing, and AI provider routing from one technical cockpit.
          </p>

          <div className="metric-grid">
            <MetricCard label="Published Pages" value={cmsPages.filter((p) => p.status === "published").length} detail="Public content online" />
            <MetricCard label="Draft Changes" value={draftCount} detail="Needs review or publish" />
            <MetricCard label="New Leads" value={leads.filter((lead) => lead.status === "new").length} detail="Project intake queue" />
            <MetricCard label="Tracked Views" value={analyticsEvents.reduce((sum, row) => sum + row.views, 0).toLocaleString()} detail="Mock analytics seed" />
          </div>

          <div className="dashboard-grid-two">
            <article className="dash-panel">
              <h2>Priority workflow</h2>
              <ol className="workflow-list">
                <li>Edit homepage hero and services grid.</li>
                <li>Review work pages for MechAssist AI and OpenClaw.</li>
                <li>Connect OpenAI and Anthropic secrets in Cloudflare.</li>
                <li>Publish CMS pages after QA.</li>
              </ol>
            </article>

            <article className="dash-panel">
              <h2>AI provider readiness</h2>
              <div className="readiness-list">
                <span>OpenAI routing metadata ready</span>
                <span>Anthropic routing metadata ready</span>
                <span>Secrets server-side only</span>
                <span>Blocked models policy enabled</span>
              </div>
            </article>
          </div>
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/CMSPages.jsx", r'''
    import { DataTable } from "../components/DataTable.jsx";
    import { StatusBadge } from "../components/StatusBadge.jsx";
    import { cmsPages } from "../data/cmsData.js";

    export function CMSPages() {
      return (
        <section>
          <p className="dash-eyebrow">CMS</p>
          <h1>Pages</h1>
          <p className="dash-subtitle">Draft, preview, edit, and publish public website pages.</p>

          <DataTable
            columns={[
              { key: "title", label: "Page" },
              { key: "slug", label: "Route" },
              { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
              { key: "seoScore", label: "SEO" },
              { key: "updatedAt", label: "Updated" }
            ]}
            rows={cmsPages}
            getRowHref={(row) => `/dashboard/pages/${row.id}`}
          />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/CMSPageEditor.jsx", r'''
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
    ''')

    write("src/dashboard/pages/MediaLibrary.jsx", r'''
    import { DataTable } from "../components/DataTable.jsx";
    import { StatusBadge } from "../components/StatusBadge.jsx";
    import { mediaAssets } from "../data/cmsData.js";

    export function MediaLibrary() {
      return (
        <section>
          <p className="dash-eyebrow">Assets</p>
          <h1>Media library</h1>
          <p className="dash-subtitle">Manage images, textures, downloads, Open Graph assets, and CAD/GLB files.</p>

          <div className="action-row">
            <button className="primary-action">Upload asset</button>
            <button>Optimize images</button>
            <button>Sync R2 metadata</button>
          </div>

          <DataTable
            columns={[
              { key: "name", label: "Asset" },
              { key: "type", label: "Type" },
              { key: "usage", label: "Usage" },
              { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
              { key: "size", label: "Size" }
            ]}
            rows={mediaAssets}
          />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/CaseStudies.jsx", r'''
    import { DataTable } from "../components/DataTable.jsx";
    import { StatusBadge } from "../components/StatusBadge.jsx";
    import { caseStudies } from "../data/cmsData.js";

    export function CaseStudies() {
      return (
        <section>
          <p className="dash-eyebrow">Work</p>
          <h1>Case studies</h1>
          <p className="dash-subtitle">Edit project proof, outcomes, technical stacks, and conversion CTAs.</p>

          <DataTable
            columns={[
              { key: "title", label: "Title" },
              { key: "category", label: "Category" },
              { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
              { key: "stack", label: "Stack", render: (row) => row.stack.join(", ") },
              { key: "outcome", label: "Outcome" }
            ]}
            rows={caseStudies}
          />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/Services.jsx", r'''
    import { DataTable } from "../components/DataTable.jsx";
    import { StatusBadge } from "../components/StatusBadge.jsx";
    import { services } from "../data/cmsData.js";

    export function Services() {
      return (
        <section>
          <p className="dash-eyebrow">Offers</p>
          <h1>Services</h1>
          <p className="dash-subtitle">Manage offer pages, pricing notes, deliverables, use cases, and SEO.</p>

          <DataTable
            columns={[
              { key: "title", label: "Service" },
              { key: "slug", label: "Route" },
              { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
              { key: "price", label: "Starting" },
              { key: "summary", label: "Summary" }
            ]}
            rows={services}
          />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/Leads.jsx", r'''
    import { DataTable } from "../components/DataTable.jsx";
    import { StatusBadge } from "../components/StatusBadge.jsx";
    import { leads } from "../data/cmsData.js";

    export function Leads() {
      return (
        <section>
          <p className="dash-eyebrow">CRM</p>
          <h1>Project leads</h1>
          <p className="dash-subtitle">Review intake submissions and move prospects through the project pipeline.</p>

          <DataTable
            columns={[
              { key: "name", label: "Name" },
              { key: "company", label: "Company" },
              { key: "projectType", label: "Project Type" },
              { key: "budget", label: "Budget" },
              { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> },
              { key: "source", label: "Source" }
            ]}
            rows={leads}
          />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/IntakeForms.jsx", r'''
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
    ''')

    write("src/dashboard/pages/Analytics.jsx", r'''
    import { analyticsEvents } from "../data/cmsData.js";
    import { DataTable } from "../components/DataTable.jsx";
    import { MetricCard } from "../components/MetricCard.jsx";

    export function Analytics() {
      const views = analyticsEvents.reduce((sum, row) => sum + row.views, 0);
      const leads = analyticsEvents.reduce((sum, row) => sum + row.leads, 0);
      const ctas = analyticsEvents.reduce((sum, row) => sum + row.cta, 0);

      return (
        <section>
          <p className="dash-eyebrow">Analytics</p>
          <h1>Site performance</h1>
          <p className="dash-subtitle">Prepared for D1 events, Supabase long-term analytics, and provider cost telemetry.</p>

          <div className="metric-grid">
            <MetricCard label="Views" value={views.toLocaleString()} />
            <MetricCard label="CTA Clicks" value={ctas.toLocaleString()} />
            <MetricCard label="Leads" value={leads.toLocaleString()} />
            <MetricCard label="Primary Source" value="RAG page" />
          </div>

          <DataTable
            columns={[
              { key: "page", label: "Page" },
              { key: "views", label: "Views" },
              { key: "cta", label: "CTA" },
              { key: "leads", label: "Leads" },
              { key: "conversion", label: "Conversion" }
            ]}
            rows={analyticsEvents.map((row) => ({ ...row, id: row.page }))}
          />
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/Publishing.jsx", r'''
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
    ''')

    write("src/dashboard/pages/Settings.jsx", r'''
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
    ''')

    write("src/dashboard/pages/AIProviders.jsx", r'''
    import { aiProviders, routingPolicy } from "../data/aiProviders.js";
    import { StatusBadge } from "../components/StatusBadge.jsx";

    export function AIProviders() {
      return (
        <section>
          <p className="dash-eyebrow">AI Routing</p>
          <h1>OpenAI and Anthropic providers</h1>
          <p className="dash-subtitle">
            Configure model metadata, routing lanes, blocked models, and server-side secret requirements.
            API keys must be stored as Cloudflare secrets, never in browser code.
          </p>

          <div className="ai-policy-card">
            <h2>Routing policy</h2>
            <div className="policy-grid">
              {Object.entries(routingPolicy).map(([key, value]) => (
                <div key={key}>
                  <span>{key}</span>
                  <code>{Array.isArray(value) ? value.join(", ") : String(value)}</code>
                </div>
              ))}
            </div>
          </div>

          <div className="provider-grid">
            {aiProviders.map((provider) => (
              <article className="dash-panel" key={provider.key}>
                <div className="provider-head">
                  <div>
                    <p className="dash-eyebrow">{provider.key}</p>
                    <h2>{provider.displayName}</h2>
                  </div>
                  <StatusBadge status={provider.status} />
                </div>

                <div className="secret-box">
                  <span>Cloudflare secret</span>
                  <code>{provider.secretName}</code>
                </div>

                <h3>Models</h3>
                <div className="model-list">
                  {provider.models.map((model) => (
                    <div key={model.key}>
                      <strong>{model.key}</strong>
                      <span>{model.lane}</span>
                      <small>{model.notes}</small>
                    </div>
                  ))}
                </div>

                {provider.blockedModels.length ? (
                  <>
                    <h3>Blocked models</h3>
                    <div className="chip-row">
                      {provider.blockedModels.map((model) => <span key={model}>{model}</span>)}
                    </div>
                  </>
                ) : null}
              </article>
            ))}
          </div>

          <article className="dash-panel">
            <h2>Backend API contract</h2>
            <code>GET /api/ai/providers</code>
            <code>POST /api/agent/chat</code>
            <code>POST /api/agent/route</code>
            <code>POST /api/agent/image</code>
            <code>POST /api/agent/evals/run</code>
          </article>
        </section>
      );
    }
    ''')

    write("src/dashboard/pages/NotFoundDashboard.jsx", r'''
    export function NotFoundDashboard() {
      return (
        <section>
          <p className="dash-eyebrow">404</p>
          <h1>Dashboard route not found</h1>
          <p className="dash-subtitle">Return to the CMS overview or use the sidebar navigation.</p>
        </section>
      );
    }
    ''')

    write("src/dashboard/dashboard.css", r'''
    @import "../shared/brand/tokens.css";

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background:
        radial-gradient(circle at 15% 0%, rgba(56, 189, 248, 0.12), transparent 28rem),
        radial-gradient(circle at 85% 0%, rgba(34, 197, 94, 0.07), transparent 26rem),
        #050812;
      color: #f8fafc;
      font-family: Inter, system-ui, sans-serif;
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

    .dash-shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 284px minmax(0, 1fr);
    }

    .dash-sidebar {
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      padding: 22px;
      border-right: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(11, 16, 32, 0.94);
      backdrop-filter: blur(18px);
    }

    .dash-brand {
      display: flex;
      gap: 12px;
      align-items: center;
      color: inherit;
      text-decoration: none;
      margin-bottom: 26px;
    }

    .dash-brand span {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 14px;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      color: #04111f;
      font-weight: 950;
      letter-spacing: -0.07em;
    }

    .dash-brand strong,
    .dash-brand small {
      display: block;
      line-height: 1.1;
    }

    .dash-brand small {
      color: #94a3b8;
      font-size: 0.78rem;
    }

    .dash-nav {
      display: grid;
      gap: 7px;
    }

    .dash-nav a {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #94a3b8;
      text-decoration: none;
      padding: 10px 12px;
      border-radius: 13px;
      font-weight: 800;
      transition: 160ms ease;
    }

    .dash-nav a:hover,
    .dash-nav a.active {
      color: #f8fafc;
      background: rgba(56, 189, 248, 0.12);
    }

    .dash-main {
      min-width: 0;
    }

    .dash-topbar {
      position: sticky;
      top: 0;
      z-index: 20;
      min-height: 74px;
      padding: 0 28px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(5, 8, 18, 0.82);
      backdrop-filter: blur(18px);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 18px;
    }

    .dash-search {
      width: min(520px, 100%);
      display: flex;
      align-items: center;
      gap: 10px;
      border: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(255, 255, 255, 0.035);
      border-radius: 999px;
      padding: 0 14px;
      min-height: 42px;
      color: #94a3b8;
    }

    .dash-search input {
      width: 100%;
      border: 0;
      outline: 0;
      color: #f8fafc;
      background: transparent;
    }

    .dash-top-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      white-space: nowrap;
    }

    .dash-top-actions a,
    .save-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 36px;
      padding: 0 12px;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 184, 0.16);
      color: #f8fafc;
      text-decoration: none;
      font-size: 0.86rem;
      font-weight: 800;
    }

    .save-pill {
      color: #22c55e;
      border-color: rgba(34, 197, 94, 0.36);
    }

    .dash-content {
      padding: 34px;
    }

    .dash-eyebrow {
      color: #38bdf8;
      font-family: "JetBrains Mono", monospace;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font-size: 0.76rem;
      margin: 0 0 8px;
    }

    h1 {
      font-size: clamp(2.2rem, 4vw, 4.2rem);
      line-height: 0.96;
      letter-spacing: -0.055em;
      margin: 0 0 18px;
    }

    h2 {
      margin-top: 0;
      letter-spacing: -0.03em;
    }

    .dash-subtitle {
      max-width: 820px;
      color: #94a3b8;
      line-height: 1.65;
      margin-bottom: 28px;
    }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
      margin-bottom: 26px;
    }

    .metric-card,
    .dash-panel,
    .dash-table,
    .ai-policy-card {
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 22px;
      background: rgba(17, 24, 39, 0.72);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.22);
    }

    .metric-card {
      padding: 22px;
    }

    .metric-card span,
    .metric-card small {
      color: #94a3b8;
    }

    .metric-card strong {
      display: block;
      font-size: 2.1rem;
      line-height: 1;
      margin: 9px 0 6px;
    }

    .dashboard-grid-two,
    .provider-grid,
    .settings-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }

    .dash-panel,
    .ai-policy-card {
      padding: 22px;
    }

    .workflow-list {
      color: #cbd5e1;
      line-height: 1.9;
      padding-left: 20px;
    }

    .readiness-list {
      display: grid;
      gap: 10px;
    }

    .readiness-list span {
      padding: 12px;
      border-radius: 14px;
      background: rgba(34, 197, 94, 0.08);
      border: 1px solid rgba(34, 197, 94, 0.18);
      color: #bbf7d0;
      font-weight: 700;
    }

    .dash-table {
      overflow: hidden;
    }

    .dash-table-head,
    .dash-table-row {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      align-items: center;
      padding: 14px 16px;
    }

    .dash-table-head {
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.035);
      font-size: 0.82rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .dash-table-row {
      color: #f8fafc;
      text-decoration: none;
      border-top: 1px solid rgba(148, 163, 184, 0.11);
      transition: background 160ms ease;
    }

    .dash-table-row:hover {
      background: rgba(56, 189, 248, 0.07);
    }

    .status-badge {
      display: inline-flex;
      width: fit-content;
      align-items: center;
      min-height: 28px;
      padding: 0 9px;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 184, 0.2);
      color: #cbd5e1;
      font-size: 0.78rem;
      font-weight: 900;
      text-transform: capitalize;
    }

    .status-published,
    .status-ready,
    .status-qualified,
    .status-proposal {
      border-color: rgba(34, 197, 94, 0.34);
      color: #bbf7d0;
      background: rgba(34, 197, 94, 0.08);
    }

    .status-draft,
    .status-review,
    .status-new,
    .status-needs-secret,
    .status-needs-optimization {
      border-color: rgba(245, 158, 11, 0.34);
      color: #fde68a;
      background: rgba(245, 158, 11, 0.08);
    }

    .editor-header {
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: flex-start;
      margin-bottom: 24px;
    }

    .editor-actions,
    .action-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 22px;
    }

    button,
    .editor-actions button,
    .action-row button {
      border: 1px solid rgba(148, 163, 184, 0.18);
      background: rgba(255, 255, 255, 0.04);
      color: #f8fafc;
      border-radius: 999px;
      padding: 10px 14px;
      font-weight: 900;
    }

    .primary-action {
      border-color: transparent !important;
      color: #04111f !important;
      background: linear-gradient(135deg, #38bdf8, #22c55e) !important;
    }

    .editor-layout {
      display: grid;
      grid-template-columns: 250px minmax(0, 1fr) 340px;
      gap: 18px;
      min-height: 660px;
    }

    .editor-panel,
    .preview-panel {
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 22px;
      background: rgba(17, 24, 39, 0.72);
      padding: 18px;
    }

    .editor-panel {
      display: grid;
      align-content: start;
      gap: 12px;
    }

    .editor-panel button {
      border-radius: 14px;
      text-align: left;
      display: grid;
      gap: 3px;
    }

    .editor-panel button.selected {
      border-color: rgba(56, 189, 248, 0.48);
      background: rgba(56, 189, 248, 0.12);
    }

    .editor-panel small,
    .editor-panel p {
      color: #94a3b8;
    }

    .inspector label,
    .settings-grid label {
      display: grid;
      gap: 7px;
      color: #94a3b8;
      font-weight: 800;
    }

    input,
    textarea,
    select {
      width: 100%;
      border: 1px solid rgba(148, 163, 184, 0.18);
      background: rgba(5, 8, 18, 0.72);
      color: #f8fafc;
      border-radius: 13px;
      padding: 11px 12px;
      outline: none;
    }

    textarea {
      min-height: 96px;
      resize: vertical;
    }

    input:focus,
    textarea:focus {
      border-color: #38bdf8;
    }

    .preview-panel {
      display: grid;
      align-content: center;
      padding: 48px;
      background:
        radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.16), transparent 20rem),
        rgba(7, 11, 18, 0.78);
    }

    .preview-panel h2 {
      font-size: clamp(2.3rem, 5vw, 5.2rem);
      line-height: 0.92;
      letter-spacing: -0.06em;
      margin: 0 0 20px;
    }

    .preview-panel p {
      color: #cbd5e1;
      max-width: 780px;
      line-height: 1.7;
    }

    .preview-cta-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 24px;
    }

    .preview-cta-row span {
      display: inline-flex;
      border-radius: 999px;
      padding: 10px 14px;
      border: 1px solid rgba(148, 163, 184, 0.2);
      color: #f8fafc;
      font-weight: 900;
    }

    .inspector-box,
    .secret-box {
      display: grid;
      gap: 8px;
      border: 1px solid rgba(148, 163, 184, 0.14);
      border-radius: 16px;
      padding: 12px;
      background: rgba(255, 255, 255, 0.035);
    }

    code {
      display: block;
      color: #7dd3fc;
      font-family: "JetBrains Mono", monospace;
      font-size: 0.82rem;
      white-space: normal;
    }

    .field-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }

    .publish-list {
      display: grid;
      gap: 12px;
    }

    .publish-list .dash-panel {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 18px;
    }

    .publish-list small {
      display: block;
      color: #94a3b8;
    }

    .ai-policy-card {
      margin-bottom: 18px;
    }

    .policy-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .policy-grid div {
      border: 1px solid rgba(148, 163, 184, 0.13);
      border-radius: 14px;
      padding: 12px;
      background: rgba(255, 255, 255, 0.03);
    }

    .policy-grid span {
      display: block;
      color: #94a3b8;
      margin-bottom: 6px;
      font-size: 0.82rem;
      font-weight: 900;
    }

    .provider-head {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
      margin-bottom: 14px;
    }

    .model-list {
      display: grid;
      gap: 10px;
    }

    .model-list div {
      border: 1px solid rgba(148, 163, 184, 0.14);
      border-radius: 14px;
      padding: 12px;
      background: rgba(255, 255, 255, 0.03);
    }

    .model-list strong,
    .model-list span,
    .model-list small {
      display: block;
    }

    .model-list span {
      color: #38bdf8;
      font-size: 0.86rem;
      font-family: "JetBrains Mono", monospace;
      margin: 4px 0;
    }

    .model-list small {
      color: #94a3b8;
      line-height: 1.5;
    }

    .chip-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .chip-row span {
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #fecaca;
      background: rgba(239, 68, 68, 0.08);
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 0.82rem;
      font-weight: 900;
    }

    @media (max-width: 1150px) {
      .dash-shell,
      .editor-layout {
        grid-template-columns: 1fr;
      }

      .dash-sidebar {
        position: static;
        height: auto;
      }

      .metric-grid,
      .dashboard-grid-two,
      .provider-grid,
      .settings-grid,
      .field-grid,
      .policy-grid {
        grid-template-columns: 1fr;
      }

      .dash-table-head,
      .dash-table-row {
        grid-template-columns: 1fr;
      }
    }
    ''')

    write("docs/DASHBOARD.md", r'''
    # Leadership Legacy Dashboard

    The dashboard is served through `dashboard.html` and mapped by the Cloudflare Worker:

    ```txt
    /dashboard
    /dashboard/*
    ```

    The Worker must never redirect `/dashboard`; it serves `/dashboard.html` directly to avoid redirect loops.

    ## AI Provider Prep

    The dashboard is prepared for:

    ```txt
    OPENAI_API_KEY
    ANTHROPIC_API_KEY
    ```

    These must be stored as Cloudflare secrets:

    ```bash
    npx wrangler secret put OPENAI_API_KEY
    npx wrangler secret put ANTHROPIC_API_KEY
    ```

    The browser dashboard must never receive raw provider secrets.

    ## API Contracts

    ```txt
    GET  /api/health
    GET  /api/ai/providers
    POST /api/agent/chat
    POST /api/agent/route
    POST /api/agent/image
    POST /api/agent/evals/run
    ```

    ## CMS Contracts

    ```txt
    GET   /api/cms/pages
    GET   /api/cms/pages/:id
    PATCH /api/cms/pages/:id/draft
    POST  /api/cms/pages/:id/publish
    GET   /api/cms/media
    GET   /api/leads
    GET   /api/analytics/overview
    ```
    ''')

    write("sql/d1/002_dashboard_ai_and_cms_runtime.sql", r'''
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS cms_ai_providers (
      id TEXT PRIMARY KEY,
      provider_key TEXT NOT NULL UNIQUE,
      display_name TEXT NOT NULL,
      secret_name TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'needs_secret',
      use_cases_json TEXT NOT NULL DEFAULT '[]',
      metadata_json TEXT NOT NULL DEFAULT '{}',
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS cms_ai_models (
      id TEXT PRIMARY KEY,
      provider_key TEXT NOT NULL,
      model_key TEXT NOT NULL,
      display_name TEXT NOT NULL,
      lane TEXT NOT NULL,
      is_enabled INTEGER NOT NULL DEFAULT 1,
      is_blocked INTEGER NOT NULL DEFAULT 0,
      input_price_per_mtok REAL,
      output_price_per_mtok REAL,
      metadata_json TEXT NOT NULL DEFAULT '{}',
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      UNIQUE(provider_key, model_key)
    );

    CREATE TABLE IF NOT EXISTS cms_ai_routing_policy (
      id TEXT PRIMARY KEY,
      policy_key TEXT NOT NULL UNIQUE,
      default_text_model TEXT,
      cheap_text_model TEXT,
      senior_text_model TEXT,
      default_image_model TEXT,
      standard_image_model TEXT,
      review_provider TEXT,
      blocked_models_json TEXT NOT NULL DEFAULT '[]',
      metadata_json TEXT NOT NULL DEFAULT '{}',
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    INSERT OR IGNORE INTO cms_ai_providers (
      id,
      provider_key,
      display_name,
      secret_name,
      use_cases_json
    ) VALUES
      ('provider_openai', 'openai', 'OpenAI', 'OPENAI_API_KEY', json_array('chat','routing','image_generation','evals')),
      ('provider_anthropic', 'anthropic', 'Anthropic', 'ANTHROPIC_API_KEY', json_array('chat','routing','code_review','evals'));

    INSERT OR IGNORE INTO cms_ai_models (
      id,
      provider_key,
      model_key,
      display_name,
      lane,
      is_enabled,
      is_blocked,
      metadata_json
    ) VALUES
      ('openai_gpt_5_4_nano', 'openai', 'gpt-5.4-nano', 'GPT-5.4 Nano', 'cheap_fast_router', 1, 0, '{}'),
      ('openai_gpt_5_4_mini', 'openai', 'gpt-5.4-mini', 'GPT-5.4 Mini', 'default_workhorse', 1, 0, '{}'),
      ('openai_gpt_5_4', 'openai', 'gpt-5.4', 'GPT-5.4', 'senior_reasoning', 1, 0, '{}'),
      ('openai_image_1_mini', 'openai', 'gpt-image-1-mini', 'GPT Image 1 Mini', 'budget_image_generation', 1, 0, '{}'),
      ('openai_image_1_5', 'openai', 'gpt-image-1.5', 'GPT Image 1.5', 'standard_image_generation', 1, 0, '{}'),
      ('openai_gpt_5_5_blocked', 'openai', 'gpt-5.5', 'GPT-5.5', 'blocked', 0, 1, json_object('reason','User policy: do not implement yet')),
      ('openai_gpt_5_5_pro_blocked', 'openai', 'gpt-5.5-pro', 'GPT-5.5 Pro', 'blocked', 0, 1, json_object('reason','User policy: do not implement yet')),
      ('openai_gpt_5_4_pro_blocked', 'openai', 'gpt-5.4-pro', 'GPT-5.4 Pro', 'blocked', 0, 1, json_object('reason','User policy: exclude')),
      ('anthropic_sonnet', 'anthropic', 'claude-sonnet', 'Claude Sonnet', 'standard_senior_review', 1, 0, '{}'),
      ('anthropic_haiku', 'anthropic', 'claude-haiku', 'Claude Haiku', 'cheap_fast_fallback', 1, 0, '{}');

    INSERT OR IGNORE INTO cms_ai_routing_policy (
      id,
      policy_key,
      default_text_model,
      cheap_text_model,
      senior_text_model,
      default_image_model,
      standard_image_model,
      review_provider,
      blocked_models_json,
      metadata_json
    ) VALUES (
      'policy_default',
      'default',
      'gpt-5.4-mini',
      'gpt-5.4-nano',
      'gpt-5.4',
      'gpt-image-1-mini',
      'gpt-image-1.5',
      'anthropic',
      json_array('gpt-5.5','gpt-5.5-pro','gpt-5.4-pro'),
      json_object('router','deterministic_guardrails_then_thompson_sampling')
    );
    ''')

    run(["npm", "install"], check=True)
    run(["npm", "run", "build"], check=True)

    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", "feat: build full CMS dashboard and fix dashboard worker route"], check=False)

    print("\nDashboard buildout complete.")
    print("Next commands:")
    print("npm run deploy")
    print("curl -I https://leadership-legacy.meauxbility.workers.dev/dashboard")
    print("open https://leadership-legacy.meauxbility.workers.dev/dashboard")

if __name__ == "__main__":
    main()
