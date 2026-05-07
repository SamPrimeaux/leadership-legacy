# Leadership Legacy Digital

Production-ready Vite + React public website and CMS dashboard for Connor McNeely and Leadership Legacy Digital.

This repo is the working foundation for:

- Connor McNeely’s premium technical founder portfolio
- Leadership Legacy Digital’s AI engineering studio website
- A password-protected CMS dashboard
- Cloudflare Worker deployment
- R2-backed assets and code snapshots
- D1-backed CMS runtime
- Supabase-backed analytics, RAG, evals, and model routing telemetry
- AI provider routing across OpenAI, Anthropic, Gemini, Workers AI, local Llama/Ollama, and future tool providers

## Current Positioning

```txt
Connor McNeely
Mechanical Engineer × AI Developer

Leadership Legacy Digital
Engineering-grade AI systems for technical businesses.
```

## Live Development URL

```txt
https://leadership-legacy.meauxbility.workers.dev/
```

Dashboard:

```txt
https://leadership-legacy.meauxbility.workers.dev/dashboard
```

Current concept password:

```txt
1234
```

This password gate is only for demo/concept review. Production should use Cloudflare Access, Supabase Auth, or Worker-backed secure sessions.

## Current Repo Structure

```txt
leadership-legacy/
├── index.html
├── dashboard.html
├── wrangler.jsonc
├── vite.config.js
├── src/
│   ├── public-app/
│   ├── dashboard/
│   ├── worker/
│   ├── shared/
│   ├── styles/
│   ├── components/
│   ├── data/
│   └── config/
├── sql/
│   ├── d1/
│   └── supabase/
├── docs/
└── scripts/
```

## Quick Start

```bash
npm install
npm run dev
```

Public app:

```txt
http://localhost:5173/
```

Dashboard MPA entry:

```txt
http://localhost:5173/dashboard.html
```

Cloudflare Worker route after deploy:

```txt
/dashboard
```

## Build

```bash
npm run build
```

## Deploy

```bash
npm run deploy
```

## Environment Philosophy

Never put API keys in React, public files, dashboard data files, or `.env` files that are committed.

Production secrets belong in:

```txt
Cloudflare Worker secrets
Supabase secrets
Provider dashboards
Local uncommitted .env files
```

Cloudflare secret pattern:

```bash
npx wrangler secret put OPENAI_API_KEY
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put GEMINI_API_KEY
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put GOOGLE_CLIENT_ID
npx wrangler secret put GOOGLE_CLIENT_SECRET
```

## Owner Note

Sam has temporarily installed an OpenAI API key so development can continue until Connor installs his own key.

Once Connor has his own OpenAI account/key, replace the Cloudflare Worker secret:

```bash
npx wrangler secret put OPENAI_API_KEY
npm run deploy
```

Do not commit either Sam’s or Connor’s key.

## Main Setup Guide

Read this first:

```txt
docs/CONNECTORS_SETUP_GUIDE.md
```

## Checklist

Use this checklist during Connor handoff:

```txt
docs/CONNOR_HANDOFF_CHECKLIST.md
```

## Database SQL

D1 CMS runtime:

```txt
sql/d1/010_full_cms_runtime.sql
sql/d1/011_full_cms_runtime_triggers.sql
sql/d1/012_full_cms_seed_content.sql
```

Supabase analytics/RAG/runtime telemetry:

```txt
sql/supabase/010_full_cms_analytics_rag.sql
sql/supabase/011_full_cms_functions.sql
sql/supabase/012_full_cms_seed.sql
```

## R2

Current bucket:

```txt
leadership-legacy
```

Current Worker binding:

```txt
WEBSITE
```

R2 docs:

```txt
docs/R2_BUCKET.md
```

## Scripts

```txt
scripts/build_full_dashboard.py
scripts/collect_python_scripts.py
scripts/generate_full_cms_sql.py
scripts/generate_connor_onboarding_docs.py
scripts/upgrade_header_footer_auth.py
scripts/wire_r2_website_bucket.py
```

Refresh script index:

```bash
python3 scripts/collect_python_scripts.py
```
