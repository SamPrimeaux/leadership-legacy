# Leadership Legacy Digital

Production-ready Vite + React + Cloudflare platform for Connor McNeely and Leadership Legacy Digital.

Leadership Legacy Digital is positioned as an engineering-grade AI systems studio for technical businesses. The platform combines a premium public website, a private dashboard, a Cursor-style AI IDE, CMS/runtime storage, R2 asset management, OpenAI-powered code assistance, and a growing integration layer for GitHub, Google Drive, Gmail, Resend, Supabase, Anthropic, Gemini, MCP-style tools, and Cloudflare services.

## Brand Positioning

```txt
Connor McNeely = Mechanical Engineer × AI Developer
Leadership Legacy Digital = AI systems, automation, CAD workflows, RAG systems, and full-stack applications
Core message = engineering-grade AI systems for technical businesses
Visual tone = dark premium SaaS, engineering blueprint, AI neural systems, industrial precision, founder-led trust
```

## Current Live Site

Public site:

```txt
https://leadership-legacy.meauxbility.workers.dev/
https://leadership-legacy.meauxbility.workers.dev/services
https://leadership-legacy.meauxbility.workers.dev/work
https://leadership-legacy.meauxbility.workers.dev/about
https://leadership-legacy.meauxbility.workers.dev/resources
https://leadership-legacy.meauxbility.workers.dev/contact
```

Dashboard:

```txt
https://leadership-legacy.meauxbility.workers.dev/dashboard
https://leadership-legacy.meauxbility.workers.dev/dashboard/agent
https://leadership-legacy.meauxbility.workers.dev/dashboard/storage
https://leadership-legacy.meauxbility.workers.dev/dashboard/settings
https://leadership-legacy.meauxbility.workers.dev/dashboard/analytics
https://leadership-legacy.meauxbility.workers.dev/dashboard/learn
https://leadership-legacy.meauxbility.workers.dev/dashboard/mail
https://leadership-legacy.meauxbility.workers.dev/dashboard/mcp
```

API health checks:

```txt
https://leadership-legacy.meauxbility.workers.dev/api/health
https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
https://leadership-legacy.meauxbility.workers.dev/api/openai/diagnostics
https://leadership-legacy.meauxbility.workers.dev/api/openai/test
https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=
https://leadership-legacy.meauxbility.workers.dev/api/github/status
```

## What This Repo Contains

```txt
public website
dashboard
Cursor-style IDE
Monaco editor
Agent Connor chat/code panel
xterm terminal prep
R2 object browser
live Worker API
OpenAI server-side integration
Playwright live smoke tests
R2 deploy snapshots
R2 pruning workflow
GitHub Actions deploy workflow
Connor onboarding docs
integrations playbooks
production readiness rubric
```

## Tech Stack

| Layer | Tooling |
|---|---|
| Frontend | Vite, React, React Router |
| Dashboard IDE | Monaco Editor, xterm |
| UI Icons | lucide-react |
| Backend | Cloudflare Workers |
| Static assets | Worker Assets + R2 |
| Object storage | Cloudflare R2 |
| CMS runtime planned | Cloudflare D1 |
| Session/cache planned | Cloudflare KV |
| Realtime planned | Durable Objects |
| AI provider live | OpenAI |
| AI providers planned | Anthropic, Gemini, Workers AI, local Llama/Ollama |
| Email planned | Resend, Gmail OAuth |
| File integrations planned | GitHub App/OAuth, Google Drive OAuth |
| Heavy backend planned | Supabase Postgres, pgvector, analytics, evals |
| Testing | Playwright |
| CI/CD | GitHub Actions + Wrangler |

## File Tree

```txt
leadership-legacy/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docs/
│   ├── TOOLS_README.md
│   ├── END_TO_END_INTEGRATION_PLAYBOOK.md
│   ├── CONNOR_COURSE_STUDY_GUIDE.md
│   ├── CONNOR_PROGRESS_TRACKER.md
│   ├── RUBRIC.md
│   ├── R2_AUTODEPLOY_AND_PRUNE.md
│   └── integrations/
├── scripts/
│   ├── publish-dist-to-r2.mjs
│   ├── prune-r2-deployments.mjs
│   └── *.py helper scripts
├── src/
│   ├── public-app/
│   ├── dashboard/
│   ├── shared/
│   ├── styles/
│   └── worker/
├── tests/
│   └── e2e/
├── dashboard.html
├── index.html
├── package.json
├── playwright.config.js
├── TO-DO.md
├── vite.config.js
└── wrangler config
```

## Important Directories

```txt
src/public-app/      public marketing site
src/dashboard/       private dashboard and IDE shell
src/worker/          Cloudflare Worker API/router
src/shared/          shared brand tokens and components
docs/                operating docs and integration playbooks
scripts/             repo automation, R2 publishing, SQL/helpers
tests/e2e/           Playwright live smoke tests
dist/                generated build output, gitignored
node_modules/        installed dependencies, gitignored
```

## Quick Start

Requirements:

```txt
Node 22+
npm
Wrangler
Cloudflare account access
GitHub repo access
```

Install:

```bash
npm install --include=dev
```

Run local dev server:

```bash
npm run dev
```

Build:

```bash
npm run build
```

Run live Playwright smoke tests:

```bash
npm run test:e2e
```

Run tests against local Vite:

```bash
LOCAL_E2E=1 npm run test:e2e
```

Deploy Worker:

```bash
npm run deploy
```

Full build + R2 upload + prune + deploy:

```bash
npm run deploy:full
```

## NPM Scripts

```txt
npm run dev              start Vite locally
npm run build            production build
npm run preview          preview Vite build
npm run deploy           build and deploy Worker
npm run deploy:full      build, publish to R2, prune old R2 deploys, deploy Worker
npm run r2:publish       upload dist/ to R2 live/ and deployments/<sha>/
npm run r2:prune         prune old deployment snapshots
npm run test:e2e         run live Playwright smoke tests
npm run test:e2e:ui      open Playwright UI
npm run test:e2e:headed  run Playwright headed
npm run test:e2e:report  open Playwright report
```

## Cloudflare Resources

Required:

```txt
Worker: leadership-legacy
R2 bucket: leadership-legacy
Worker Assets binding: ASSETS
R2 binding: WEBSITE -> leadership-legacy
```

Planned or optional:

```txt
D1 database for CMS runtime
KV namespace for OAuth/session/cache
Durable Objects for agent sessions, terminal sessions, realtime CMS editing
Workers AI binding for Cloudflare-native AI utilities
```

Basic checks:

```bash
npx wrangler whoami
npx wrangler r2 bucket list
npx wrangler d1 list
```

Live checks:

```bash
curl -s https://leadership-legacy.meauxbility.workers.dev/api/health
curl -s https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=
```

## R2 Deploy Layout

Built assets are uploaded to R2 in two locations:

```txt
leadership-legacy/
  live/
    index.html
    dashboard.html
    assets/
    manifest.json

  deployments/
    <git-sha>/
      index.html
      dashboard.html
      assets/
      manifest.json

    _latest.json
```

`live/` is the latest build snapshot.

`deployments/<sha>/` keeps versioned snapshots.

The prune script keeps the latest deployment snapshots and deletes older ones under:

```txt
deployments/<old-sha>/
```

It does not delete long-lived data folders:

```txt
live/
cms/
assets/
docs/
analytics/
```

## R2 Pruning Note

Wrangler v4.88.0 does not support this unsupported command form:

```bash
npx wrangler r2 object list leadership-legacy --prefix deployments/ --remote --json
```

The current prune script instead lists objects through the Worker API:

```txt
GET /api/r2/list?prefix=deployments/
```

Then it deletes old objects using supported Wrangler delete calls:

```bash
npx wrangler r2 object delete leadership-legacy/<key> --remote
```

## GitHub Actions Autodeploy

Workflow:

```txt
.github/workflows/deploy.yml
```

On push to `main`, GitHub Actions should:

```txt
install dependencies
run npm audit
build
run live Playwright smoke tests
upload dist to R2
prune old R2 deployments
deploy Worker
```

Required GitHub repo secrets:

```txt
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
```

Cloudflare API token permissions:

```txt
Workers Scripts: Edit
Account R2 Storage: Edit
Account Settings: Read
```

Optional if Cloudflare requests them:

```txt
Workers Routes: Edit
D1: Edit
```

## OpenAI

OpenAI is called server-side from the Worker. The browser never receives the key.

Add or replace the Worker secret:

```bash
npx wrangler secret put OPENAI_API_KEY
```

Paste only the raw key:

```txt
sk-proj-...
```

Do not paste:

```txt
OPENAI_API_KEY=sk-proj-...
```

Verify:

```bash
curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/diagnostics
curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/test
```

Expected:

```txt
startsWithEnvName: false
hasQuotes: false
/api/openai/test returns ok
```

## Agent Connor

Agent Connor has three modes:

```txt
Chat
Code
Auto
```

Chat is default.

Use Chat for:

```txt
normal questions
learning Cloudflare/GitHub/R2/D1/Supabase
explaining repo setup
planning integrations
debugging conceptually
```

Chat calls:

```txt
POST /api/openai/chat
```

Code mode intentionally edits the active Monaco file.

Code calls:

```txt
POST /api/openai/code
```

Auto mode switches to code only for clear edit/refactor/patch/generate-code prompts.

## Model Policy

Enabled OpenAI model lanes:

```txt
gpt-5.4-mini
gpt-5.4-nano
gpt-5.4
```

Blocked by current project policy:

```txt
gpt-5.5
gpt-5.5-pro
gpt-5.4-pro
```

Planned providers:

```txt
Anthropic
Gemini
Workers AI
local Llama/Ollama
```

## Integration Roadmap

GitHub:

```txt
OAuth/App setup
list repos
browse tree
open file into Monaco
AI edit
preview diff
commit to branch
open PR
run tests
deploy after approval
```

Google Drive:

```txt
OAuth setup
browse files
import docs/PDFs
store snapshots in R2
chunk/embed documents
power RAG
```

Gmail:

```txt
OAuth setup
read threads
summarize conversation
draft replies
user approval before send
CRM/project notes
```

Resend:

```txt
contact notifications
lead confirmations
admin invites
password reset/magic link later
deploy notifications
```

Supabase:

```txt
analytics
RAG documents
pgvector embeddings
eval runs
model routing logs
codebase chunks
tool execution logs
long-term telemetry
```

D1:

```txt
pages
sections
navigation
themes
asset metadata
leads
provider config
publishing status
```

MCP tools:

```txt
github.listRepos
github.getFile
github.commitFile
r2.listObjects
r2.getObject
r2.putObject
d1.query
openai.chat
openai.codeAction
anthropic.review
gmail.createDraft
drive.importFile
resend.sendEmail
playwright.runSmoke
```

## Playwright

Playwright defaults to the deployed Worker:

```txt
https://leadership-legacy.meauxbility.workers.dev
```

Run:

```bash
npm run test:e2e
```

Run against another URL:

```bash
PLAYWRIGHT_BASE_URL=https://your-url.workers.dev npm run test:e2e
```

Run locally:

```bash
LOCAL_E2E=1 npm run test:e2e
```

Tested public routes:

```txt
/
/services
/work
/about
/resources
/contact
```

Tested dashboard routes:

```txt
/dashboard
/dashboard/agent
/dashboard/storage
/dashboard/analytics
/dashboard/learn
/dashboard/mail
/dashboard/mcp
/dashboard/settings
```

Tested APIs:

```txt
/api/health
/api/ai/providers
/api/openai/diagnostics
/api/openai/test
/api/r2/list
/api/github/status
```

## Security Rules

Never commit:

```txt
.env
API keys
private keys
OAuth secrets
service role keys
refresh tokens
passwords
```

Browser must never see:

```txt
OPENAI_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
SUPABASE_SERVICE_ROLE_KEY
GITHUB_CLIENT_SECRET
GOOGLE_CLIENT_SECRET
RESEND_API_KEY
AWS_SECRET_ACCESS_KEY
```

Destructive tools must require approval:

```txt
send email
delete file
write to main branch
deploy production
change DNS
rotate secrets
execute terminal command
delete R2 object
delete database row
```

## Connor Onboarding Docs

Start here:

```txt
TO-DO.md
docs/TOOLS_README.md
docs/END_TO_END_INTEGRATION_PLAYBOOK.md
docs/CONNOR_COURSE_STUDY_GUIDE.md
docs/CONNOR_PROGRESS_TRACKER.md
docs/RUBRIC.md
docs/R2_AUTODEPLOY_AND_PRUNE.md
docs/LIVE_PLAYWRIGHT_TESTING.md
docs/AGENT_CHAT_VS_CODE_MODE.md
```

Integration guides:

```txt
docs/integrations/GITHUB_SETUP_PLAYBOOK.md
docs/integrations/GOOGLE_DRIVE_GMAIL_SETUP_PLAYBOOK.md
docs/integrations/MCP_TOOLS_PLAYBOOK.md
docs/integrations/AI_PROVIDERS_SETUP_PLAYBOOK.md
docs/integrations/AWS_SETUP_PLAYBOOK.md
docs/integrations/RESEND_EMAIL_PLAYBOOK.md
```

## Daily Workflow

```bash
git pull origin main
npm install --include=dev
npm run build
npm run test:e2e
npm run deploy
git status --short
```

Ship workflow:

```bash
git add .
git commit -m "describe the change"
git push origin main
```

## Production Readiness Rubric

Scoring:

```txt
0 = Not present
1 = Started but not usable
2 = Partially usable with manual work
3 = Usable for internal testing
4 = Production-ready with guardrails
5 = Production-ready, monitored, documented, and tested
```

Target scores:

| Area | Target |
|---|---:|
| Repo setup | 4 |
| Cloudflare deploy | 4 |
| R2 storage | 4 |
| OpenAI | 4 |
| Anthropic | 3 |
| Gemini | 3 |
| GitHub integration | 4 |
| Google Drive/Gmail | 4 |
| Resend | 4 |
| Supabase | 4 |
| D1 CMS | 4 |
| MCP tools | 4 |
| Playwright | 4 |
| Security/secrets | 5 |
| Connor readiness | 4 |

Production ready only if:

```txt
no exposed secrets
build passes
live Playwright tests pass
Worker deploys
OpenAI test passes
R2 list works
GitHub Actions deploy works
R2 pruning works
destructive tools require approval
```

## Current Status

```txt
Worker live
R2 binding live
OpenAI live
OpenAI diagnostics clean
Dashboard routes live
R2 browser live
R2 publish script live
R2 prune script fixed to use Worker listing
Playwright live tests installed
Connor setup docs generated
GitHub/Google/Anthropic/Gemini/Resend/Supabase integrations prepared but not fully connected
```
