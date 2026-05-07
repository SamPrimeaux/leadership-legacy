# Leadership Legacy Tools README

This guide teaches Connor how to understand, connect, use, monitor, and improve the integrations behind the Leadership Legacy Digital platform.

The goal is not just to “connect APIs.” The goal is to build a working operating system for AI engineering, CMS editing, client work, CAD automation, RAG, file management, email, analytics, and deployment.

## Platform Goal

```txt
Public Website
+ CMS Dashboard
+ Cursor-style IDE
+ AI Agent
+ GitHub file operations
+ Google Drive ingestion
+ Gmail communication workflows
+ R2 asset/code storage
+ D1 CMS runtime
+ Supabase analytics/RAG/evals
+ OpenAI/Anthropic/Gemini routing
+ AWS compatibility where useful
+ MCP-style tool registry
```

## Core Rule

Never expose secrets in browser code.

Secrets belong in:

```txt
Cloudflare Worker secrets
Supabase server-side secrets
GitHub app private keys
Local uncommitted .env files
Provider dashboards
```

Secrets do not belong in:

```txt
React components
public files
R2 public assets
Git commits
dashboard localStorage
client-side VITE_ variables
```

## Tool Map

| Tool | Purpose | Current Role |
|---|---|---|
| Cloudflare Workers | Main backend/API/runtime | Serves public app, dashboard, API routes |
| Cloudflare R2 | Object storage | Assets, CMS snapshots, generated files, code snapshots |
| Cloudflare D1 | Runtime CMS database | Pages, sections, leads, themes, provider config |
| Cloudflare KV | Fast cache/session/state | OAuth state, rate limits, flags, temporary data |
| Durable Objects | Realtime sessions | Future terminal, live CMS editing, agent sessions |
| Workers AI | Native AI utilities | Embeddings, fallback inference, classification |
| Supabase | Heavy backend data | Analytics, RAG, evals, codebase indexing |
| OpenAI | Primary AI provider | Code generation, agent actions, image generation later |
| Anthropic | Review/reasoning provider | Architecture review, code review, alternate evals |
| Gemini | Alternate Google AI provider | Long context, multimodal, fallback comparisons |
| GitHub App/OAuth | Repo automation | Read/write files, branches, PRs, code reviews |
| Google Drive | Document ingestion | Import docs/PDFs to RAG and R2 |
| Gmail | Communication workflows | Draft replies, lead followups, inbox summaries |
| Resend | Transactional email | Contact forms, lead confirmations, admin notifications |
| AWS | Optional compatibility layer | S3-compatible workflows, Bedrock experiments, backups |
| OpenSCAD | CAD automation | Parametric CAD generation and STL exports |
| Spline | 3D visual layer | Hero visuals, interactive product/engineering demos |
| Playwright | E2E testing | Public site and dashboard validation |

## Recommended Connection Order

```txt
1. GitHub repo access
2. Cloudflare Worker deploy
3. R2 bucket
4. D1 database
5. KV namespaces
6. Worker secrets
7. Supabase project
8. OpenAI API
9. Anthropic API
10. Gemini API
11. Resend
12. Google OAuth app
13. Gmail API
14. Google Drive API
15. GitHub App/OAuth
16. Durable Objects
17. Workers AI
18. AWS compatibility
19. OpenSCAD/local CAD tools
20. Spline/3D assets
21. Playwright CI/evals
```

## Daily Development Commands

```bash
npm install --include=dev
npm run dev
npm run build
npm run test:e2e
npm run deploy
```

## Health Checks

```bash
curl -s https://leadership-legacy.meauxbility.workers.dev/api/health
curl -s https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/status
```

## Dashboard Routes

```txt
/dashboard
/dashboard/agent
/dashboard/dev
/dashboard/dev/terminal
/dashboard/pages
/dashboard/media
/dashboard/storage
/dashboard/settings/ai-providers
```

## Tool Usage Principles

1. Use GitHub for source of truth.
2. Use R2 for generated/static/file assets.
3. Use D1 for low-latency CMS runtime data.
4. Use Supabase for heavy analytics, RAG, evals, and code indexing.
5. Use OpenAI for default agent/code generation.
6. Use Anthropic for review, architecture, and second-opinion reasoning.
7. Use Gemini as an alternate provider and long-context comparison.
8. Use Gmail/Drive through OAuth only.
9. Use Resend for transactional emails.
10. Use Playwright after every meaningful dashboard/public app change.
