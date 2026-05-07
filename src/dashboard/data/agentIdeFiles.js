export const workspaceFiles = {
  "routes/home.jsx": {
    language: "javascript",
    type: "REACT",
    source: "local",
    content: `export function HomePage() {
  return (
    <main className="public-page">
      <section className="hero">
        <p className="eyebrow">Mechanical Engineer × AI Developer</p>
        <h1>Engineering-grade AI systems for technical businesses.</h1>
        <p>
          Connor McNeely builds AI systems, RAG workflows, CAD automations,
          and full-stack applications for technical teams.
        </p>
      </section>
    </main>
  );
}`
  },
  "routes/services.jsx": {
    language: "javascript",
    type: "REACT",
    source: "local",
    content: `export const services = [
  "AI Engineering",
  "RAG Systems",
  "Full-Stack Apps",
  "CAD Automation",
  "CAD-to-Video",
  "Business Automation",
  "Consulting"
];

export function ServicesPage() {
  return (
    <main>
      {services.map((service) => (
        <article key={service}>
          <h2>{service}</h2>
        </article>
      ))}
    </main>
  );
}`
  },
  "worker/index.js": {
    language: "javascript",
    type: "WORKER",
    source: "local",
    content: `export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/health") {
      return Response.json({
        ok: true,
        app: "leadership-legacy",
        openaiConfigured: Boolean(env.OPENAI_API_KEY)
      });
    }

    return env.ASSETS.fetch(request);
  }
};`
  },
  "cms/schema.sql": {
    language: "sql",
    type: "SQL",
    source: "local",
    content: `CREATE TABLE IF NOT EXISTS cms_pages (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  route_path TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'draft',
  draft_json TEXT NOT NULL DEFAULT '{}',
  published_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);`
  },
  "cloudflare/wrangler.jsonc": {
    language: "json",
    type: "CONFIG",
    source: "local",
    content: `{
  "name": "leadership-legacy",
  "main": "src/worker/index.js",
  "compatibility_date": "2026-05-06",
  "assets": {
    "directory": "./dist",
    "binding": "ASSETS"
  },
  "r2_buckets": [
    {
      "binding": "WEBSITE",
      "bucket_name": "leadership-legacy"
    }
  ]
}`
  }
};

export const localTree = [
  {
    name: "routes",
    kind: "folder",
    children: ["home.jsx", "services.jsx", "work.jsx", "contact.jsx"]
  },
  {
    name: "components",
    kind: "folder",
    children: ["Header.jsx", "Footer.jsx", "Hero.jsx", "ServiceCard.jsx"]
  },
  {
    name: "cms",
    kind: "folder",
    children: ["schema.sql", "pages.json", "sections.json"]
  },
  {
    name: "worker",
    kind: "folder",
    children: ["index.js", "openai.js", "r2.js"]
  },
  {
    name: "cloudflare",
    kind: "folder",
    children: ["wrangler.jsonc"]
  }
];

export const commandPresets = [
  "npm install --include=dev",
  "npm run dev",
  "npm run build",
  "npm run test:e2e",
  "npm run deploy",
  "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
  "curl https://leadership-legacy.meauxbility.workers.dev/api/ai/providers",
  "curl https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=cms/",
  "npx wrangler secret put OPENAI_API_KEY",
  "npx wrangler secret put ANTHROPIC_API_KEY"
];

export const dashboardViews = {
  home: {
    label: "Command Center",
    tab: "dashboard",
    title: "Leadership Legacy operating system",
    subtitle: "CMS, code, storage, AI providers, learning, mail, MCP tools, analytics, and deployment workflows."
  },
  agent: {
    label: "Agent",
    tab: "agent",
    title: "Agent Connor",
    subtitle: "Edit Monaco files, call OpenAI, inspect generated code, and prepare GitHub/R2 saves."
  },
  storage: {
    label: "Storage",
    tab: "storage",
    title: "R2 + assets",
    subtitle: "Browse R2 objects, open text assets into Monaco, and prepare uploads/snapshots."
  },
  settings: {
    label: "Settings",
    tab: "settings",
    title: "Provider + integration settings",
    subtitle: "OpenAI, Anthropic, Gemini, GitHub, Google, Resend, Cloudflare, Supabase, and AWS readiness."
  },
  analytics: {
    label: "Analytics",
    tab: "analytics",
    title: "Analytics + telemetry",
    subtitle: "Track page views, leads, agent runs, model costs, tool calls, errors, and deployment health."
  },
  learn: {
    label: "Learn",
    tab: "learn",
    title: "Connor learning path",
    subtitle: "Guided setup modules, CLI/PowerShell practice, integration study guide, and rubric scoring."
  },
  mail: {
    label: "Mail",
    tab: "mail",
    title: "Mail + lead communication",
    subtitle: "Prepare Gmail OAuth, Resend transactional email, lead drafts, and approved outbound workflows."
  },
  mcp: {
    label: "MCP",
    tab: "mcp",
    title: "MCP tools registry",
    subtitle: "Tool registry, permissions, execution logs, approval gates, and provider adapters."
  },
  cms: {
    label: "CMS",
    tab: "cms",
    title: "CMS runtime",
    subtitle: "Pages, sections, services, case studies, resources, navigation, SEO, and publishing."
  }
};
