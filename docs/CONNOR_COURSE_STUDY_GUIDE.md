# Connor Course and Study Guide

This course teaches Connor how to operate and understand the Leadership Legacy platform.

## Outcome

By the end, Connor should be able to:

```txt
run the app locally
deploy to Cloudflare
connect API providers
use the dashboard
understand the CMS
use R2/D1/Supabase correctly
connect Google/GitHub integrations
understand AI provider routing
run Playwright tests
review tool logs
safely approve agent actions
```

## Module 1: Repo and Local Development

Learn:

```txt
Git basics
npm install
npm run dev
npm run build
npm run deploy
PowerShell equivalents
```

Practice:

```bash
git status
npm install --include=dev
npm run dev
npm run build
```

Completion:

- [ ] Connor can clone repo.
- [ ] Connor can start local dev server.
- [ ] Connor can explain source vs build output.
- [ ] Connor understands why `node_modules/` and `dist/` are gitignored.

## Module 2: Dashboard and CMS

Learn:

```txt
dashboard purpose
Monaco editor
Agent panel
terminal panel
CMS pages
sections
R2 assets
publishing flow
```

Practice:

```txt
Open /dashboard
Sign in
Open Monaco file
Ask Agent to modify file
Apply generated output
Open R2 status
```

Completion:

- [ ] Connor can navigate dashboard.
- [ ] Connor understands CMS data vs hardcoded React.
- [ ] Connor understands draft vs published content.
- [ ] Connor understands why agent edits require approval.

## Module 3: Cloudflare

Learn:

```txt
Workers
R2
D1
KV
Durable Objects
Workers AI
Wrangler
```

Practice:

```bash
npx wrangler whoami
npx wrangler deploy
npx wrangler r2 bucket list
npx wrangler d1 list
```

Completion:

- [ ] Connor understands Worker as backend.
- [ ] Connor understands R2 as object storage.
- [ ] Connor understands D1 as CMS runtime database.
- [ ] Connor understands KV as fast state/cache.
- [ ] Connor understands Durable Objects as realtime session state.

## Module 4: Supabase

Learn:

```txt
Postgres
pgvector
analytics
RAG documents
eval runs
routing logs
service role safety
RLS
```

Practice:

```txt
Open Supabase SQL editor
Review ll_documents
Review ll_site_events
Review ll_routing_decisions
Review ll_eval_runs
```

Completion:

- [ ] Connor knows what belongs in Supabase.
- [ ] Connor knows service role key is server-only.
- [ ] Connor understands why RAG and analytics live there.

## Module 5: AI Providers

Learn:

```txt
OpenAI default lane
Anthropic review lane
Gemini comparison lane
Workers AI utility lane
local Llama experimental lane
blocked models policy
cost logging
```

Completion:

- [ ] Connor can replace OpenAI key.
- [ ] Connor can add Anthropic key.
- [ ] Connor can explain model routing.
- [ ] Connor can explain why 5.5 and 5.4 pro are excluded for now.

## Module 6: GitHub

Learn:

```txt
OAuth app vs GitHub App
repo permissions
branch workflow
PR workflow
commit safety
```

Completion:

- [ ] Connor can connect GitHub.
- [ ] Connor can select a repo.
- [ ] Connor understands file read/write flow.
- [ ] Connor understands PR approval flow.

## Module 7: Google Drive and Gmail

Learn:

```txt
OAuth
scopes
Drive ingestion
Gmail drafts
token safety
```

Completion:

- [ ] Connor can explain OAuth callback.
- [ ] Connor understands Drive scopes.
- [ ] Connor understands Gmail draft approval.
- [ ] Connor knows tokens are never client-side.

## Module 8: Tools and MCP

Learn:

```txt
tool registry
tool execution log
approvals
risk levels
input/output schemas
```

Completion:

- [ ] Connor can describe a tool.
- [ ] Connor can explain approval gates.
- [ ] Connor can inspect tool logs.
- [ ] Connor can identify risky tools.

## Module 9: Testing and Quality

Learn:

```txt
Playwright
smoke tests
dashboard tests
provider tests
rubric scoring
eval runs
```

Practice:

```bash
npm run test:e2e
npm run build
npm run deploy
```

Completion:

- [ ] Connor can run Playwright.
- [ ] Connor can read failures.
- [ ] Connor understands screenshots/traces.
- [ ] Connor understands when to block deploy.

## Module 10: Production Readiness

Learn:

```txt
auth
secrets
logs
monitoring
backups
rate limits
spend controls
approval gates
```

Completion:

- [ ] Dashboard concept auth replaced.
- [ ] Real auth selected.
- [ ] Secrets audited.
- [ ] Rate limits added.
- [ ] Tool approvals enforced.
- [ ] Monitoring dashboards created.
