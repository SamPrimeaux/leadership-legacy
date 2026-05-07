# Connor Handoff Checklist

Use this checklist when Sam and Connor sit down to finish connecting the production accounts.

## Repo

- [ ] Connor has GitHub access to `SamPrimeaux/leadership-legacy`
- [ ] Connor can clone the repo
- [ ] Connor can run `npm install`
- [ ] Connor can run `npm run dev`
- [ ] Connor can run `npm run build`
- [ ] Connor understands public app vs dashboard app

## Cloudflare

- [ ] Connor has Cloudflare account
- [ ] Worker ownership/transfer plan is decided
- [ ] Worker name confirmed: `leadership-legacy`
- [ ] `wrangler.jsonc` reviewed
- [ ] Worker deploy works from local machine
- [ ] Production domain plan chosen

## R2

- [ ] R2 bucket exists
- [ ] Bucket name confirmed: `leadership-legacy`
- [ ] Worker binding confirmed: `WEBSITE`
- [ ] R2 folder structure seeded
- [ ] Custom asset domain planned
- [ ] `/api/r2/status` returns OK
- [ ] `/dashboard/storage` loads

## D1

- [ ] D1 database created
- [ ] D1 binding added as `DB`
- [ ] Full CMS SQL applied
- [ ] Seed content applied
- [ ] `cms_pages` contains homepage/about/services/work/contact
- [ ] Dashboard is ready to read/write CMS content later

## Durable Objects

- [ ] `DashboardSession` planned
- [ ] `AgentSession` planned
- [ ] DO bindings added
- [ ] DO migrations added
- [ ] Live editing/session state design approved

## KV

- [ ] `LL_SESSIONS` created
- [ ] `LL_RATE_LIMITS` created
- [ ] `LL_CACHE` created
- [ ] `LL_OAUTH_STATE` created
- [ ] `LL_FLAGS` created

## Supabase

- [ ] Connor Supabase project created
- [ ] Supabase URL saved
- [ ] Service role key stored securely
- [ ] Supabase SQL files applied
- [ ] RLS strategy reviewed
- [ ] RAG/analytics tables verified

## OpenAI

- [ ] Sam’s temporary key noted
- [ ] Connor creates his own OpenAI API key
- [ ] `OPENAI_API_KEY` replaced in Cloudflare secrets
- [ ] Blocked models policy confirmed
- [ ] Image generation lanes approved

## Anthropic

- [ ] Connor creates Anthropic API key
- [ ] `ANTHROPIC_API_KEY` added to Cloudflare secrets
- [ ] Claude review lane approved

## Gemini

- [ ] Google AI Studio or Vertex setup chosen
- [ ] `GEMINI_API_KEY` added if available
- [ ] Gemini routing role defined

## Workers AI

- [ ] Workers AI binding added as `AI`
- [ ] Embedding/fallback usage agreed
- [ ] Not treated as primary senior reasoning lane without evals

## Resend

- [ ] Resend account created
- [ ] Sending domain verified
- [ ] `RESEND_API_KEY` added to Cloudflare secrets
- [ ] Lead notification email flow planned

## Gmail

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] Client ID/secret created
- [ ] Redirect URI added
- [ ] Token storage strategy approved

## Google Drive

- [ ] Drive API enabled
- [ ] Scopes selected
- [ ] Import-to-RAG flow planned
- [ ] R2 sync flow planned

## OpenSCAD

- [ ] Local OpenSCAD installed
- [ ] CAD folder structure created
- [ ] Sandbox/security strategy approved before production execution

## Llama / Ollama

- [ ] Local Ollama installed if desired
- [ ] Local model chosen
- [ ] Local fallback scope defined
- [ ] Not relied on for production unless hosting is planned

## Spline

- [ ] Spline account confirmed
- [ ] Hero/3D visual direction approved
- [ ] Embed/fallback strategy approved
- [ ] Reduced-motion fallback planned

## Final Production Auth

- [ ] Replace concept password `1234`
- [ ] Choose Cloudflare Access, Supabase Auth, or Worker sessions
- [ ] Add admin roles
- [ ] Add session expiration
- [ ] Add audit logging
