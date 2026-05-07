# End-to-End Integration Playbook

This is the master implementation path.

## Phase 1: Clean Foundation

```bash
npm install --include=dev
npm audit
npm run build
npm run test:e2e
npm run deploy
```

Must pass:

```txt
no audit vulnerabilities
build passes
Playwright passes
Worker deploys
dashboard loads
OpenAI provider status configured
```

## Phase 2: Cloudflare Resources

Create/verify:

```txt
Worker
R2 bucket
D1 database
KV namespaces
Durable Objects
Workers AI binding
```

Apply D1:

```bash
./scripts/apply-d1-cms-sql.sh leadership-legacy-cms
```

## Phase 3: Supabase

Apply:

```txt
sql/supabase/010_full_cms_analytics_rag.sql
sql/supabase/011_full_cms_functions.sql
sql/supabase/012_full_cms_seed.sql
```

Verify tables:

```txt
ll_documents
ll_site_events
ll_routing_decisions
ll_eval_runs
ll_codebase_chunks
```

## Phase 4: AI Providers

Add:

```bash
npx wrangler secret put OPENAI_API_KEY
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put GEMINI_API_KEY
```

Verify:

```bash
curl -s https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
```

## Phase 5: Email

Add:

```bash
npx wrangler secret put RESEND_API_KEY
```

Build:

```txt
contact form notification
lead confirmation
admin alert
send log
```

## Phase 6: Google

Add:

```bash
npx wrangler secret put GOOGLE_CLIENT_ID
npx wrangler secret put GOOGLE_CLIENT_SECRET
npx wrangler secret put GOOGLE_REDIRECT_URI
```

Build:

```txt
OAuth start route
OAuth callback route
token storage
Drive file list
Drive import
Gmail thread list
Gmail draft creation
```

## Phase 7: GitHub

Add OAuth or GitHub App secrets:

```bash
npx wrangler secret put GITHUB_CLIENT_ID
npx wrangler secret put GITHUB_CLIENT_SECRET
```

Or GitHub App:

```bash
npx wrangler secret put GITHUB_APP_ID
npx wrangler secret put GITHUB_APP_PRIVATE_KEY
npx wrangler secret put GITHUB_WEBHOOK_SECRET
```

Build:

```txt
repo list
tree browser
file read
branch create
commit file
pull request
webhook receive
```

## Phase 8: Tool Registry

Build:

```txt
tools table
tool execution log
risk level
approval gate
rate limit
result renderer
error logger
```

## Phase 9: Monitoring

Track:

```txt
page views
lead submits
agent runs
tool calls
provider costs
errors
deploys
Playwright runs
R2 uploads
D1 writes
Supabase inserts
```

## Phase 10: Handoff

Connor must demonstrate:

```txt
run local dev
run build
run tests
deploy
inspect Cloudflare resources
inspect Supabase logs
connect provider key
use dashboard Agent
identify unsafe tool action
read rubric
update progress tracker
```
