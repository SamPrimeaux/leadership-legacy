#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()

def run(cmd, check=False):
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result

def write(path, content):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"wrote {path}")

def main():
    write("README.md", r'''
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
    ''')

    write("docs/CONNECTORS_SETUP_GUIDE.md", r'''
    # Connor + Sam Setup Guide

    This document explains how Connor and Sam should connect every backend, API, AI provider, and storage system required for the Leadership Legacy Digital app.

    The goal is to turn this repo into a real working platform:

    ```txt
    Public website
    CMS dashboard
    AI provider routing
    RAG/document intelligence
    R2 asset storage
    Analytics
    Leads and email
    Google/Gmail/Drive integrations
    CAD/OpenSCAD workflows
    Workers AI/local model fallback
    Spline/3D asset support
    ```

    ## 0. Who owns what?

    During buildout:

    ```txt
    Sam:
    - Initial repo
    - Current Cloudflare deployment
    - Temporary OpenAI API key
    - Initial Worker/R2/D1/Supabase wiring
    - CMS/dashboard architecture

    Connor:
    - Final provider API keys
    - Final Cloudflare account/resources if transferred
    - Final Supabase project
    - Final Resend domain/API key
    - Final Google OAuth credentials
    - Final Anthropic/OpenAI/Gemini keys
    - Brand assets, case studies, content approval
    ```

    ## 1. Required Accounts

    Connor should have or create:

    ```txt
    Cloudflare account
    Supabase account
    OpenAI platform account
    Anthropic account
    Google Cloud project
    Resend account
    Gemini / Google AI Studio or Vertex AI setup
    GitHub account with repo access
    Optional: Spline account
    Optional: local Ollama/Llama setup
    Optional: OpenSCAD installed locally/server-side
    ```

    ## 2. Cloudflare Worker

    Current Worker:

    ```txt
    leadership-legacy
    ```

    Current deployed URL:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/
    ```

    The Worker serves:

    ```txt
    /                         public app
    /about                    public app
    /services/*               public app
    /work/*                   public app
    /resources/*              public app
    /dashboard                dashboard app shell
    /dashboard/*              dashboard app shell
    /api/*                    Worker API
    ```

    Important files:

    ```txt
    wrangler.jsonc
    src/worker/index.js
    ```

    Deploy:

    ```bash
    npm run deploy
    ```

    Verify:

    ```bash
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/health
    curl -I https://leadership-legacy.meauxbility.workers.dev/dashboard
    ```

    ## 3. Cloudflare D1

    D1 is for the lightweight CMS runtime.

    It should store:

    ```txt
    pages
    sections
    components
    page versions
    navigation menus
    brand settings
    themes
    R2 asset registry
    services
    case studies
    resources
    forms
    leads
    publish jobs
    activity log
    lightweight analytics
    AI provider metadata
    AI routing policy
    ```

    ### Create D1 DB

    Choose a DB name, likely:

    ```txt
    leadership-legacy-cms
    ```

    Create:

    ```bash
    npx wrangler d1 create leadership-legacy-cms
    ```

    Wrangler will return a database ID. Add it to `wrangler.jsonc`:

    ```json
    "d1_databases": [
      {
        "binding": "DB",
        "database_name": "leadership-legacy-cms",
        "database_id": "PASTE_DATABASE_ID_HERE"
      }
    ]
    ```

    ### Apply D1 SQL

    ```bash
    npx wrangler d1 execute leadership-legacy-cms --remote --file sql/d1/010_full_cms_runtime.sql
    npx wrangler d1 execute leadership-legacy-cms --remote --file sql/d1/011_full_cms_runtime_triggers.sql
    npx wrangler d1 execute leadership-legacy-cms --remote --file sql/d1/012_full_cms_seed_content.sql
    ```

    Or:

    ```bash
    ./scripts/apply-d1-cms-sql.sh leadership-legacy-cms
    ```

    ### Verify D1

    ```bash
    npx wrangler d1 execute leadership-legacy-cms --remote --command "SELECT id, title, route_path, status FROM cms_pages;"
    ```

    ## 4. Durable Objects

    Durable Objects should be used for live/realtime dashboard and agent sessions.

    Recommended use cases:

    ```txt
    Live CMS editing sessions
    Draft collaboration
    Agent run/session state
    Streaming state
    Terminal-like task sessions
    Multi-step workflow coordination
    ```

    Recommended Durable Object names:

    ```txt
    DashboardSession
    AgentSession
    CMSCollaborationSession
    ```

    Add to `wrangler.jsonc` later:

    ```json
    "durable_objects": {
      "bindings": [
        {
          "name": "DASHBOARD_SESSION",
          "class_name": "DashboardSession"
        },
        {
          "name": "AGENT_SESSION",
          "class_name": "AgentSession"
        }
      ]
    },
    "migrations": [
      {
        "tag": "v1",
        "new_classes": ["DashboardSession", "AgentSession"]
      }
    ]
    ```

    Recommended file path:

    ```txt
    src/worker/durable-objects/
    ```

    ## 5. Cloudflare KV

    KV should be used for low-risk fast lookup/config/cache.

    Recommended KV namespaces:

    ```txt
    LL_SESSIONS
    LL_RATE_LIMITS
    LL_CACHE
    LL_OAUTH_STATE
    LL_FLAGS
    ```

    Create:

    ```bash
    npx wrangler kv namespace create LL_SESSIONS
    npx wrangler kv namespace create LL_RATE_LIMITS
    npx wrangler kv namespace create LL_CACHE
    npx wrangler kv namespace create LL_OAUTH_STATE
    npx wrangler kv namespace create LL_FLAGS
    ```

    Add returned IDs to `wrangler.jsonc`:

    ```json
    "kv_namespaces": [
      {
        "binding": "LL_SESSIONS",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_RATE_LIMITS",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_CACHE",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_OAUTH_STATE",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_FLAGS",
        "id": "PASTE_ID"
      }
    ]
    ```

    ## 6. R2

    Current R2 bucket:

    ```txt
    leadership-legacy
    ```

    Current Worker binding:

    ```txt
    WEBSITE
    ```

    Bucket purpose:

    ```txt
    CMS assets
    generated images
    brand assets
    GLB/model files
    downloads
    page snapshots
    code snapshots
    analytics exports
    docs
    temporary artifacts
    ```

    Current public development URL:

    ```txt
    https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev
    ```

    Production recommendation:

    ```txt
    assets.leadershiplegacydigital.com
    ```

    Seed folder structure:

    ```bash
    ./scripts/seed-r2-structure.sh
    ```

    Verify:

    ```bash
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/status
    curl -s "https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=cms/"
    ```

    ## 7. Supabase

    Supabase is for heavier backend data, analytics, RAG, evals, and long-term telemetry.

    Supabase should store:

    ```txt
    RAG documents
    semantic search logs
    knowledge edges
    site sessions
    site events
    lead events
    model cost snapshots
    routing arms
    routing decisions
    prompt runs
    stream events
    tool call events
    error events
    eval suites
    eval runs
    R2 object events
    Design Studio metrics
    codebase snapshots
    codebase chunks
    codebase symbols
    ```

    ### Create Connor Supabase Project

    In Supabase:

    ```txt
    New project → leadership-legacy
    Region → closest to Connor/users
    Database password → store securely
    ```

    Save:

    ```txt
    SUPABASE_URL
    SUPABASE_ANON_KEY
    SUPABASE_SERVICE_ROLE_KEY
    SUPABASE_DB_URL
    ```

    ### Apply SQL

    Run in Supabase SQL Editor, in this order:

    ```txt
    sql/supabase/010_full_cms_analytics_rag.sql
    sql/supabase/011_full_cms_functions.sql
    sql/supabase/012_full_cms_seed.sql
    ```

    ### Add Worker Secrets

    ```bash
    npx wrangler secret put SUPABASE_URL
    npx wrangler secret put SUPABASE_SERVICE_ROLE_KEY
    ```

    Optional public frontend env only if needed:

    ```txt
    VITE_SUPABASE_URL
    VITE_SUPABASE_ANON_KEY
    ```

    Do not expose the service role key to the browser.

    ## 8. OpenAI API

    Current state:

    ```txt
    Sam has installed an OpenAI API key temporarily.
    Connor should replace it with his own OpenAI API key when ready.
    ```

    Cloudflare secret:

    ```bash
    npx wrangler secret put OPENAI_API_KEY
    ```

    Suggested OpenAI lanes:

    ```txt
    gpt-5.4-nano       cheap routing/classification
    gpt-5.4-mini       default workhorse
    gpt-5.4            senior architecture/reasoning
    gpt-image-1-mini   budget image generation
    gpt-image-1.5      standard image generation
    ```

    Blocked by project policy:

    ```txt
    gpt-5.5
    gpt-5.5-pro
    gpt-5.4-pro
    ```

    Do not hardcode OpenAI keys.

    ## 9. Anthropic API

    Anthropic should be used for:

    ```txt
    code review
    architecture review
    long-form reasoning
    alternate provider evals
    senior review lane
    ```

    Cloudflare secret:

    ```bash
    npx wrangler secret put ANTHROPIC_API_KEY
    ```

    Suggested routing:

    ```txt
    Claude Sonnet → senior review / architecture
    Claude Haiku  → cheaper summaries / validation
    ```

    Store model config in:

    ```txt
    D1: cms_ai_models
    Supabase: ll_routing_arms, ll_model_cost_snapshots
    ```

    ## 10. Gemini / Google AI

    Gemini can be used for:

    ```txt
    provider comparison
    long context reasoning
    alternate model evals
    multimodal workflows
    fallback model routes
    ```

    Cloudflare secret:

    ```bash
    npx wrangler secret put GEMINI_API_KEY
    ```

    Suggested future D1 rows:

    ```txt
    provider_key: google
    model_key: gemini-pro
    model_key: gemini-flash
    ```

    Keep Gemini isolated behind the same routing abstraction as OpenAI/Anthropic.

    ## 11. Workers AI

    Workers AI should be used as Cloudflare-native fallback or utility inference.

    Good use cases:

    ```txt
    embeddings
    image classification
    lightweight summaries
    fallback chat
    low-cost internal utilities
    ```

    Avoid using Workers AI as the primary high-quality reasoning/coding model until evals prove it.

    Wrangler binding pattern:

    ```json
    "ai": {
      "binding": "AI"
    }
    ```

    In Worker code:

    ```js
    await env.AI.run("@cf/baai/bge-large-en-v1.5", {
      text: "content to embed"
    });
    ```

    Recommended Worker binding:

    ```txt
    AI
    ```

    ## 12. Resend

    Resend should handle:

    ```txt
    project intake notifications
    lead confirmation emails
    dashboard/admin notifications
    password reset / magic link later
    publishing notifications
    ```

    Cloudflare secret:

    ```bash
    npx wrangler secret put RESEND_API_KEY
    ```

    Recommended sender domain:

    ```txt
    leadershiplegacydigital.com
    ```

    Until final domain is ready, use a verified Resend sender/domain Connor controls.

    Recommended email routes:

    ```txt
    POST /api/forms/contact
    POST /api/leads/:id/send-followup
    POST /api/admin/invite
    ```

    ## 13. Gmail

    Gmail integration should be OAuth-based, not password-based.

    Use Gmail for:

    ```txt
    reading lead-related inbox threads
    drafting replies
    sending follow-up drafts
    syncing client communication notes
    ```

    Google Cloud setup:

    ```txt
    Google Cloud Console
    Create project
    Enable Gmail API
    Configure OAuth consent screen
    Create OAuth 2.0 Client ID
    Add authorized redirect URI
    ```

    Suggested redirect path:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/google/callback
    ```

    Cloudflare secrets:

    ```bash
    npx wrangler secret put GOOGLE_CLIENT_ID
    npx wrangler secret put GOOGLE_CLIENT_SECRET
    npx wrangler secret put GOOGLE_REDIRECT_URI
    ```

    KV usage:

    ```txt
    LL_OAUTH_STATE      temporary OAuth state
    D1/Supabase table   encrypted or token-managed account records
    ```

    Do not store Gmail refresh tokens in browser storage.

    ## 14. Google Drive

    Google Drive integration should support:

    ```txt
    pulling docs for RAG
    syncing PDFs and docs into R2
    indexing case study assets
    importing Connor’s files
    linking downloadable resources
    ```

    Google Cloud setup:

    ```txt
    Enable Google Drive API
    Use same OAuth consent/client if possible
    Add Drive scopes carefully
    ```

    Recommended scopes:

    ```txt
    drive.metadata.readonly
    drive.readonly
    ```

    Only request broader scopes if the app truly writes to Drive.

    Suggested routes:

    ```txt
    GET  /api/integrations/google-drive/files
    POST /api/integrations/google-drive/import
    POST /api/rag/ingest/drive-file
    ```

    ## 15. OpenSCAD

    OpenSCAD should be treated as a server/local tool, not browser code.

    Good use cases:

    ```txt
    parametric CAD generation
    scripted part generation
    technical product demos
    STL generation
    CAD-to-video asset pipeline
    engineering calculators
    ```

    Local install check:

    ```bash
    openscad --version
    ```

    Suggested repo directories:

    ```txt
    cad/
    cad/openscad/
    cad/outputs/
    cad/templates/
    ```

    Suggested R2 prefixes:

    ```txt
    assets/models/
    snapshots/cad/
    exports/cad/
    ```

    Suggested Worker route design:

    ```txt
    POST /api/cad/jobs
    GET  /api/cad/jobs/:id
    GET  /api/cad/jobs/:id/download
    ```

    For production, do not run untrusted OpenSCAD scripts without sandboxing.

    ## 16. Llama / Local Models / Ollama

    Local Llama/Ollama can be used as:

    ```txt
    low-cost local coding fallback
    offline drafting
    private summarization
    eval comparison
    cheap router fallback
    ```

    Recommended local model server:

    ```txt
    Ollama
    ```

    Local check:

    ```bash
    ollama list
    ollama run llama3.1
    ```

    Example local endpoint:

    ```txt
    http://localhost:11434
    ```

    Recommended env var for local development:

    ```txt
    LOCAL_LLM_BASE_URL=http://localhost:11434
    LOCAL_LLM_MODEL=llama3.1
    ```

    Do not rely on local Llama for production unless Connor has a server/VPS/GPU strategy.

    ## 17. Spline

    Spline can support:

    ```txt
    hero 3D visuals
    engineering/AI visual scenes
    product interaction demos
    interactive homepage sections
    brand motion
    ```

    Store Spline references in CMS as assets:

    ```txt
    asset_type: model
    usage_context: hero_3d
    metadata_json.spline_url
    metadata_json.embed_url
    ```

    Recommended CMS fields:

    ```txt
    visual_type: spline | glb | image | video
    visual_url
    visual_embed_url
    fallback_image_url
    reduced_motion_fallback
    ```

    For performance:

    ```txt
    lazy load Spline
    provide static fallback image
    respect prefers-reduced-motion
    do not load heavy 3D scenes on every page by default
    ```

    ## 18. API Provider Routing Strategy

    The app should route models through a single provider abstraction.

    Recommended provider interface:

    ```txt
    routeTask(task)
    estimateCost(task, model)
    callTextModel(provider, model, messages)
    callImageModel(provider, model, prompt)
    logRoutingDecision()
    logStreamEvent()
    logToolCall()
    logError()
    ```

    D1 stores config:

    ```txt
    cms_ai_providers
    cms_ai_models
    cms_ai_routing_policy
    cms_ai_routing_arms
    ```

    Supabase stores telemetry:

    ```txt
    ll_model_cost_snapshots
    ll_routing_arms
    ll_routing_decisions
    ll_prompt_runs
    ll_stream_events
    ll_tool_call_events
    ll_error_events
    ll_eval_runs
    ```

    ## 19. Immediate Connection Checklist

    Sam and Connor should complete in this order:

    ```txt
    1. Confirm repo access for Connor.
    2. Confirm Cloudflare account ownership / transfer plan.
    3. Create/confirm Connor R2 bucket.
    4. Create/confirm Connor D1 database.
    5. Apply D1 SQL.
    6. Create Connor Supabase project.
    7. Apply Supabase SQL.
    8. Add Connor OpenAI API key to Cloudflare secrets.
    9. Add Anthropic API key to Cloudflare secrets.
    10. Add Gemini API key if available.
    11. Add Resend API key.
    12. Configure Google Cloud OAuth for Gmail and Drive.
    13. Add KV namespaces.
    14. Add Durable Objects.
    15. Add Workers AI binding.
    16. Seed R2 folder structure.
    17. Verify /api/health, /api/r2/status, /api/ai/providers.
    18. Replace concept dashboard auth with production auth.
    ```

    ## 20. Verification Commands

    ```bash
    npm run build
    npm run deploy

    curl -s https://leadership-legacy.meauxbility.workers.dev/api/health
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/status
    curl -s https://leadership-legacy.meauxbility.workers.dev/api/ai/providers
    curl -I https://leadership-legacy.meauxbility.workers.dev/dashboard
    ```

    ## 21. Production Safety Rules

    ```txt
    Never commit secrets.
    Never expose service-role Supabase keys to the browser.
    Never store OAuth refresh tokens in localStorage.
    Never let untrusted CAD/OpenSCAD execute without sandboxing.
    Never route expensive models without cost logging.
    Never let image generation run without user/project quotas.
    Never deploy dashboard auth as only a client-side password in production.
    ```
    ''')

    write("docs/CONNOR_HANDOFF_CHECKLIST.md", r'''
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
    ''')

    write("docs/ENVIRONMENT_VARIABLES.md", r'''
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
    ''')

    write("docs/PROVIDER_ROUTING_PLAN.md", r'''
    # Provider Routing Plan

    Leadership Legacy should use a model/provider router instead of hardcoding one model.

    ## Providers

    ```txt
    OpenAI
    Anthropic
    Gemini
    Workers AI
    Local Llama/Ollama
    ```

    ## OpenAI

    ```txt
    gpt-5.4-nano       cheap router
    gpt-5.4-mini       default workhorse
    gpt-5.4            senior reasoning
    gpt-image-1-mini   budget image generation
    gpt-image-1.5      standard image generation
    ```

    Blocked:

    ```txt
    gpt-5.5
    gpt-5.5-pro
    gpt-5.4-pro
    ```

    ## Anthropic

    ```txt
    Claude Sonnet     senior review / architecture
    Claude Haiku      cheap summaries / validation
    ```

    ## Gemini

    ```txt
    Gemini Pro        alternate long-context reasoning
    Gemini Flash      cheaper/faster fallback
    ```

    ## Workers AI

    ```txt
    embeddings
    classification
    fallback
    utility inference
    ```

    ## Local Llama/Ollama

    ```txt
    offline/local draft work
    cheap local summaries
    local coding experiments
    ```

    ## Routing Strategy

    Recommended:

    ```txt
    deterministic guardrails
    then Thompson Sampling inside safe model pool
    then log all outcomes
    ```

    D1 config tables:

    ```txt
    cms_ai_providers
    cms_ai_models
    cms_ai_routing_policy
    cms_ai_routing_arms
    ```

    Supabase telemetry tables:

    ```txt
    ll_model_cost_snapshots
    ll_routing_arms
    ll_routing_decisions
    ll_prompt_runs
    ll_stream_events
    ll_tool_call_events
    ll_error_events
    ll_eval_runs
    ```
    ''')

    write("docs/GOOGLE_OAUTH_PLAN.md", r'''
    # Google OAuth Plan: Gmail + Google Drive

    Gmail and Drive must be OAuth-based.

    ## Google Cloud Setup

    1. Create Google Cloud project.
    2. Configure OAuth consent screen.
    3. Enable Gmail API.
    4. Enable Google Drive API.
    5. Create OAuth 2.0 Client ID.
    6. Add redirect URI.

    Recommended redirect URI:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/google/callback
    ```

    ## Gmail Use Cases

    ```txt
    read relevant lead/customer threads
    draft replies
    send follow-up drafts after review
    sync communication notes
    ```

    ## Drive Use Cases

    ```txt
    import docs into RAG
    sync PDFs/assets to R2
    organize client files
    map docs to CMS resources
    ```

    ## Token Storage

    Do not store refresh tokens in localStorage.

    Recommended:

    ```txt
    encrypted server-side storage
    D1/Supabase token metadata
    KV only for short-lived OAuth state
    ```

    ## Suggested Routes

    ```txt
    GET  /api/oauth/google/start
    GET  /api/oauth/google/callback
    GET  /api/gmail/threads
    POST /api/gmail/draft
    GET  /api/google-drive/files
    POST /api/google-drive/import
    POST /api/rag/ingest/drive-file
    ```
    ''')

    write("docs/CAD_OPENSCAD_SPLINE_PLAN.md", r'''
    # CAD, OpenSCAD, GLB, and Spline Plan

    Connor’s unique advantage is the overlap between engineering/CAD and AI systems.

    ## OpenSCAD

    Use OpenSCAD for:

    ```txt
    parametric CAD generation
    scripted mechanical parts
    STL generation
    technical demos
    engineering configurators
    CAD-to-video workflows
    ```

    Suggested repo folders:

    ```txt
    cad/
    cad/openscad/
    cad/templates/
    cad/outputs/
    cad/metadata/
    ```

    Suggested R2 prefixes:

    ```txt
    assets/models/
    snapshots/cad/
    exports/cad/
    ```

    Production warning:

    ```txt
    Never execute untrusted OpenSCAD scripts without sandboxing.
    ```

    ## GLB / 3D Models

    Use GLB files for:

    ```txt
    product demos
    technical hero visuals
    dashboard previews
    case study media
    CAD-to-video pipelines
    ```

    Store metadata in CMS:

    ```txt
    cms_assets.asset_type = model
    cms_assets.usage_context = hero_3d | case_study | cad_demo
    ```

    ## Spline

    Spline can be used for:

    ```txt
    homepage hero scene
    AI network visual
    engineering workflow animation
    product demo scene
    ```

    CMS fields:

    ```txt
    visual_type
    visual_url
    visual_embed_url
    fallback_image_url
    reduced_motion_fallback
    ```

    Performance rules:

    ```txt
    lazy-load 3D
    use static fallbacks
    disable heavy animation for reduced motion
    do not load Spline on every route by default
    ```
    ''')

    write("docs/CLOUDFLARE_BINDINGS_PLAN.md", r'''
    # Cloudflare Bindings Plan

    This project should eventually use these Cloudflare bindings.

    ## Static Assets

    ```json
    "assets": {
      "directory": "./dist",
      "binding": "ASSETS"
    }
    ```

    ## R2

    ```json
    "r2_buckets": [
      {
        "binding": "WEBSITE",
        "bucket_name": "leadership-legacy"
      }
    ]
    ```

    ## D1

    ```json
    "d1_databases": [
      {
        "binding": "DB",
        "database_name": "leadership-legacy-cms",
        "database_id": "PASTE_DATABASE_ID"
      }
    ]
    ```

    ## KV

    ```json
    "kv_namespaces": [
      {
        "binding": "LL_SESSIONS",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_RATE_LIMITS",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_CACHE",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_OAUTH_STATE",
        "id": "PASTE_ID"
      },
      {
        "binding": "LL_FLAGS",
        "id": "PASTE_ID"
      }
    ]
    ```

    ## Durable Objects

    ```json
    "durable_objects": {
      "bindings": [
        {
          "name": "DASHBOARD_SESSION",
          "class_name": "DashboardSession"
        },
        {
          "name": "AGENT_SESSION",
          "class_name": "AgentSession"
        }
      ]
    }
    ```

    ## Workers AI

    ```json
    "ai": {
      "binding": "AI"
    }
    ```

    ## Recommended Secrets

    ```txt
    OPENAI_API_KEY
    ANTHROPIC_API_KEY
    GEMINI_API_KEY
    RESEND_API_KEY
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
    GOOGLE_REDIRECT_URI
    ```
    ''')

    write("scripts/check-onboarding-docs.sh", r'''
    #!/usr/bin/env bash
    set -euo pipefail

    echo "Checking onboarding docs..."

    files=(
      "README.md"
      "docs/CONNECTORS_SETUP_GUIDE.md"
      "docs/CONNOR_HANDOFF_CHECKLIST.md"
      "docs/ENVIRONMENT_VARIABLES.md"
      "docs/PROVIDER_ROUTING_PLAN.md"
      "docs/GOOGLE_OAUTH_PLAN.md"
      "docs/CAD_OPENSCAD_SPLINE_PLAN.md"
      "docs/CLOUDFLARE_BINDINGS_PLAN.md"
    )

    for file in "${files[@]}"; do
      if [[ ! -f "$file" ]]; then
        echo "Missing: $file"
        exit 1
      fi
      echo "OK: $file"
    done

    echo "Onboarding docs are present."
    ''')

    run(["chmod", "+x", "scripts/check-onboarding-docs.sh"], check=False)
    run(["./scripts/check-onboarding-docs.sh"], check=True)

    run(["git", "add", "README.md", "docs", "scripts/check-onboarding-docs.sh", "scripts/generate_connor_onboarding_docs.py"], check=False)
    run(["git", "commit", "-m", "docs: add Connor integration onboarding guide"], check=False)

    print("\nOnboarding README/docs generated.")
    print("Next:")
    print("git push origin main")
    print("Open docs/CONNECTORS_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
