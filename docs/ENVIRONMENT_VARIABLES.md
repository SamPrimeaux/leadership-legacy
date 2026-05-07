# Environment Variables and Secrets

This file documents the expected environment variables and Cloudflare Worker secrets.

Do not commit real values.

## Cloudflare Worker Secrets

```bash
npx wrangler secret put OPENAI_API_KEY
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put GEMINI_API_KEY
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put SUPABASE_URL
npx wrangler secret put SUPABASE_SERVICE_ROLE_KEY
npx wrangler secret put GOOGLE_CLIENT_ID
npx wrangler secret put GOOGLE_CLIENT_SECRET
npx wrangler secret put GOOGLE_REDIRECT_URI
```

## Temporary Note

Sam has installed an OpenAI API key until Connor installs his own.

When Connor is ready:

```bash
npx wrangler secret put OPENAI_API_KEY
npm run deploy
```

## Public Vite Variables

Use only for non-secret public config:

```txt
VITE_PUBLIC_SITE_URL=https://leadership-legacy.meauxbility.workers.dev
VITE_DASHBOARD_BASE=/dashboard
VITE_API_BASE=/api
```

## Never Public

Never expose these in `VITE_` variables:

```txt
OPENAI_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
RESEND_API_KEY
SUPABASE_SERVICE_ROLE_KEY
GOOGLE_CLIENT_SECRET
OAuth refresh tokens
```
