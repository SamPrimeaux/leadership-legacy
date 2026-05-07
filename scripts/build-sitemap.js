import fs from "node:fs";

const siteUrl = process.env.SITE_URL || "https://leadershiplegacydigital.com";
const routes = [
  "/",
  "/about",
  "/services",
  "/services/ai-engineering",
  "/services/rag-systems",
  "/services/full-stack-apps",
  "/services/cad-automation",
  "/services/cad-to-video",
  "/services/business-automation",
  "/services/consulting",
  "/work",
  "/work/mechassist-ai",
  "/work/openclaw",
  "/work/evergrow-landscaping",
  "/work/ai-meal-planner",
  "/work/engineercad",
  "/resources",
  "/resources/engineering-ai-playbook",
  "/resources/rag-readiness-checklist",
  "/resources/automation-roi",
  "/contact",
  "/privacy",
  "/terms"
];

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${routes.map((route) => `  <url><loc>${siteUrl}${route}</loc></url>`).join("\n")}
</urlset>`;

fs.mkdirSync("public", { recursive: true });
fs.writeFileSync("public/sitemap.xml", xml);
console.log("sitemap written to public/sitemap.xml");
