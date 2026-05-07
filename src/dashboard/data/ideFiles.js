export const initialFiles = {
  "src/worker/index.js": {
    language: "javascript",
    content: `export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/health") {
      return Response.json({
        ok: true,
        app: "leadership-legacy"
      });
    }

    return new Response("Leadership Legacy Worker online");
  }
};`
  },
  "src/dashboard/components/HeroPanel.jsx": {
    language: "javascript",
    content: `export function HeroPanel() {
  return (
    <section className="hero-panel">
      <p className="eyebrow">Mechanical Engineer × AI Developer</p>
      <h1>Engineering-grade AI systems for technical businesses.</h1>
      <p>
        Connor McNeely builds AI systems, RAG tools, CAD automations,
        and full-stack applications for technical teams.
      </p>
    </section>
  );
}`
  },
  "wrangler.jsonc": {
    language: "json",
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
  },
  "README_TASK.md": {
    language: "markdown",
    content: `# Current Task

Use the AI panel to generate or refactor files.

Good prompts:

- Build a polished CMS page editor component.
- Add a Cloudflare Worker route for saving CMS drafts.
- Generate a D1 query helper for cms_pages.
- Improve accessibility and mobile behavior.
- Create a RAG ingestion endpoint outline.`
  }
};
