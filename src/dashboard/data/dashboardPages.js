import {
  Activity,
  Bot,
  Cloud,
  Code2,
  Database,
  FileText,
  GitBranch,
  GraduationCap,
  HardDrive,
  Inbox,
  KeyRound,
  Mail,
  Rocket,
  Server,
  Settings,
  ShieldCheck,
  Sparkles,
  TestTube2,
  Wrench
} from "lucide-react";

export const dashboardPageConfig = {
  home: {
    eyebrow: "Command Center",
    title: "Leadership Legacy operating system",
    body: "A focused cockpit for Connor to learn, build, test, deploy, and connect the tools behind Leadership Legacy Digital.",
    primaryAction: "Open Agent IDE",
    primaryHref: "/dashboard/agent",
    secondaryAction: "Review playbook",
    secondaryHref: "/dashboard/learn",
    cards: [
      { icon: Bot, label: "Agent IDE", value: "OpenAI live", body: "Use Monaco and Agent Connor for guided code work." },
      { icon: HardDrive, label: "R2 Storage", value: "Connected", body: "Browse real R2 files and open text/code assets." },
      { icon: Wrench, label: "MCP Tools", value: "Prepared", body: "Tool registry, approval gates, and execution logs." },
      { icon: TestTube2, label: "Playwright", value: "Ready", body: "Run smoke tests before deploys." }
    ],
    timeline: [
      "Confirm OpenAI model route and key shape",
      "Connect Connor GitHub OAuth/App",
      "Connect Google Drive and Gmail OAuth",
      "Wire real CMS writes through D1",
      "Add approval-gated GitHub save and PR creation"
    ]
  },
  storage: {
    eyebrow: "Storage",
    title: "R2 assets and snapshots",
    body: "Browse the real leadership-legacy R2 bucket, open text/code objects into Monaco, and prepare uploads, previews, and CMS asset mapping.",
    primaryAction: "Refresh R2",
    primaryActionType: "r2-refresh",
    secondaryAction: "Open Agent",
    secondaryHref: "/dashboard/agent",
    cards: [
      { icon: HardDrive, label: "Bucket", value: "leadership-legacy", body: "Primary object storage for assets, docs, exports, and snapshots." },
      { icon: FileText, label: "Text assets", value: "Monaco-ready", body: "Open code, JSON, markdown, SQL, CSS, and HTML into the editor." },
      { icon: Cloud, label: "Public assets", value: "R2-backed", body: "Use public object routes for previews and downloads." },
      { icon: Database, label: "CMS mapping", value: "Next", body: "Map assets to CMS records and section schemas." }
    ]
  },
  settings: {
    eyebrow: "Settings",
    title: "Integrations and provider readiness",
    body: "Track the secrets, OAuth apps, provider accounts, and Cloudflare resources Connor needs to fully own the platform.",
    primaryAction: "Check providers",
    primaryActionType: "provider-check",
    secondaryAction: "Study guide",
    secondaryHref: "/dashboard/learn",
    cards: [
      { icon: KeyRound, label: "OpenAI", value: "Configured", body: "Server-side Worker secret. Never exposed to the browser." },
      { icon: Sparkles, label: "Anthropic", value: "Pending", body: "Add Connor's Anthropic key when ready." },
      { icon: GitBranch, label: "GitHub", value: "OAuth/App", body: "Prepare repo browsing, branches, commits, and PRs." },
      { icon: Mail, label: "Google", value: "Drive/Gmail", body: "OAuth-driven Drive import and Gmail drafts." },
      { icon: Server, label: "Supabase", value: "Planned", body: "Analytics, RAG, evals, and codebase indexing." },
      { icon: Cloud, label: "Cloudflare", value: "Live", body: "Worker, R2, D1, KV, DO, and Workers AI." }
    ]
  },
  analytics: {
    eyebrow: "Analytics",
    title: "Telemetry and quality signals",
    body: "Track what matters: user activity, R2 access, lead flow, agent runs, model costs, tool calls, errors, and deploy health.",
    primaryAction: "Open tests",
    primaryHref: "/dashboard/learn",
    secondaryAction: "Review tools",
    secondaryHref: "/dashboard/mcp",
    cards: [
      { icon: Activity, label: "Views", value: "2,188", body: "Seed analytics until live event tracking is connected." },
      { icon: Inbox, label: "Leads", value: "1", body: "Project intake queue placeholder." },
      { icon: Bot, label: "Agent runs", value: "Live", body: "OpenAI calls are routed through Worker." },
      { icon: TestTube2, label: "E2E tests", value: "Playwright", body: "Smoke tests for public site and dashboard auth." }
    ]
  },
  learn: {
    eyebrow: "Learning Center",
    title: "Connor setup course",
    body: "A guided course for Connor to learn PowerShell, Cloudflare, GitHub, Google OAuth, AI provider routing, R2, D1, Supabase, MCP tools, and deploy discipline.",
    primaryAction: "Open rubric",
    primaryHref: "/dashboard/mcp",
    secondaryAction: "Open Agent",
    secondaryHref: "/dashboard/agent",
    modules: [
      "Run locally with PowerShell",
      "Understand source vs build output",
      "Deploy with Wrangler",
      "Read and open R2 assets",
      "Use Monaco safely",
      "Ask Agent Connor for code edits",
      "Connect GitHub OAuth/App",
      "Connect Google Drive and Gmail",
      "Add Anthropic and Gemini keys",
      "Run Playwright before deploys",
      "Use the readiness rubric"
    ]
  },
  mail: {
    eyebrow: "Mail",
    title: "Gmail and Resend workflows",
    body: "Prepare lead communication, Gmail drafts, Resend notifications, and approval-gated outbound messages.",
    primaryAction: "Connect Google",
    primaryHref: "/api/oauth/google/start",
    secondaryAction: "Open settings",
    secondaryHref: "/dashboard/settings",
    cards: [
      { icon: Mail, label: "Gmail", value: "OAuth", body: "Read threads and create drafts after user approval." },
      { icon: Inbox, label: "Lead inbox", value: "Planned", body: "Central queue for project inquiries and followups." },
      { icon: Rocket, label: "Resend", value: "Transactional", body: "Contact notifications, confirmations, and admin emails." },
      { icon: ShieldCheck, label: "Approval", value: "Required", body: "No autonomous sending without explicit review." }
    ]
  },
  mcp: {
    eyebrow: "MCP Tools",
    title: "Tool registry and execution layer",
    body: "A governed tool system for repo operations, R2, D1, Supabase, Drive, Gmail, OpenAI, Anthropic, Gemini, Resend, Playwright, and CAD workflows.",
    primaryAction: "Review settings",
    primaryHref: "/dashboard/settings",
    secondaryAction: "Open Agent",
    secondaryHref: "/dashboard/agent",
    tools: [
      { key: "github.listRepos", risk: "low", status: "planned" },
      { key: "github.getFile", risk: "low", status: "planned" },
      { key: "github.commitFile", risk: "approval", status: "planned" },
      { key: "r2.listObjects", risk: "low", status: "live" },
      { key: "r2.getTextObject", risk: "low", status: "live" },
      { key: "d1.query", risk: "approval", status: "planned" },
      { key: "openai.codeAction", risk: "medium", status: "live" },
      { key: "anthropic.review", risk: "medium", status: "pending key" },
      { key: "gmail.createDraft", risk: "approval", status: "planned" },
      { key: "drive.importFile", risk: "medium", status: "planned" },
      { key: "playwright.runSmoke", risk: "low", status: "ready" },
      { key: "resend.sendEmail", risk: "approval", status: "planned" }
    ]
  },
  cms: {
    eyebrow: "CMS",
    title: "Pages, sections, and publishing",
    body: "The CMS layer should manage page routes, section schemas, services, case studies, resources, SEO, navigation, assets, and publish snapshots.",
    primaryAction: "Open storage",
    primaryHref: "/dashboard/storage",
    secondaryAction: "Open Agent",
    secondaryHref: "/dashboard/agent",
    cards: [
      { icon: FileText, label: "Pages", value: "D1 runtime", body: "Draft and published page JSON." },
      { icon: Code2, label: "Sections", value: "Schema-driven", body: "Reusable content blocks." },
      { icon: HardDrive, label: "Assets", value: "R2-backed", body: "Media, models, downloads, and snapshots." },
      { icon: Rocket, label: "Publishing", value: "Snapshot flow", body: "Review, build, test, deploy." }
    ]
  }
};
