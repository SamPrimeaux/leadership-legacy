export const workspaceFiles = {
  "routes/home.jsx": {
    language: "javascript",
    type: "REACT",
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
  }
];

export const r2Objects = [
  "cms/pages/home.json",
  "cms/themes/leadership-legacy-dark.css",
  "assets/brand/mark.svg",
  "assets/models/engineering-system.glb",
  "snapshots/code/latest.zip",
  "docs/onboarding.md"
];

export const commandPresets = [
  "npm install",
  "npm run dev",
  "npm run build",
  "npm run deploy",
  "curl https://leadership-legacy.meauxbility.workers.dev/api/health",
  "curl https://leadership-legacy.meauxbility.workers.dev/api/ai/providers",
  "npx wrangler secret put OPENAI_API_KEY",
  "npx wrangler d1 execute leadership-legacy-cms --remote --command \"SELECT id,title FROM cms_pages;\""
];
