# Leadership Legacy Dashboard

The dashboard is served through `dashboard.html` and mapped by the Cloudflare Worker:

```txt
/dashboard
/dashboard/*
```

The Worker must never redirect `/dashboard`; it serves `/dashboard.html` directly to avoid redirect loops.

## AI Provider Prep

The dashboard is prepared for:

```txt
OPENAI_API_KEY
ANTHROPIC_API_KEY
```

These must be stored as Cloudflare secrets:

```bash
npx wrangler secret put OPENAI_API_KEY
npx wrangler secret put ANTHROPIC_API_KEY
```

The browser dashboard must never receive raw provider secrets.

## API Contracts

```txt
GET  /api/health
GET  /api/ai/providers
POST /api/agent/chat
POST /api/agent/route
POST /api/agent/image
POST /api/agent/evals/run
```

## CMS Contracts

```txt
GET   /api/cms/pages
GET   /api/cms/pages/:id
PATCH /api/cms/pages/:id/draft
POST  /api/cms/pages/:id/publish
GET   /api/cms/media
GET   /api/leads
GET   /api/analytics/overview
```
