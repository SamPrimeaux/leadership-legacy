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
    write("docs/TOOLS_README.md", r'''
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
    ''')

    write("docs/integrations/GITHUB_SETUP_PLAYBOOK.md", r'''
    # GitHub App and OAuth Setup Playbook

    ## Goal

    Connor should be able to connect GitHub so the dashboard and AI agent can eventually:

    ```txt
    read repo files
    create files
    update files
    delete files
    create branches
    open pull requests
    review diffs
    attach commits to AI runs
    save code snapshots to R2
    ```

    ## Option A: GitHub OAuth App

    Use OAuth when the app acts as the signed-in user.

    Best for:

    ```txt
    dashboard login
    user repo browsing
    user-authorized file edits
    user-owned repo access
    ```

    ### GitHub OAuth App Steps

    1. Go to GitHub Developer Settings.
    2. Create a new OAuth App.
    3. Set app name:

    ```txt
    Leadership Legacy Dashboard
    ```

    4. Set homepage URL:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev
    ```

    5. Set authorization callback URL:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/github/callback
    ```

    6. Save:

    ```txt
    GITHUB_CLIENT_ID
    GITHUB_CLIENT_SECRET
    ```

    7. Add secrets:

    ```bash
    npx wrangler secret put GITHUB_CLIENT_ID
    npx wrangler secret put GITHUB_CLIENT_SECRET
    ```

    ## Option B: GitHub App

    Use a GitHub App when the platform itself needs controlled repo installation access.

    Best for:

    ```txt
    repo automation
    PR creation
    code review workflows
    branch-based edits
    organization-level installs
    auditability
    ```

    ### GitHub App Steps

    1. Create GitHub App.
    2. Set callback URL:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/github/callback
    ```

    3. Set webhook URL later:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/webhooks/github
    ```

    4. Permissions:

    ```txt
    Contents: Read and write
    Pull requests: Read and write
    Issues: Read and write
    Metadata: Read-only
    Actions: Read-only initially
    Checks: Read and write later
    ```

    5. Generate private key.
    6. Store private key securely. Do not commit it.

    Cloudflare secret candidates:

    ```bash
    npx wrangler secret put GITHUB_APP_ID
    npx wrangler secret put GITHUB_APP_PRIVATE_KEY
    npx wrangler secret put GITHUB_WEBHOOK_SECRET
    ```

    ## Recommended Dashboard GitHub Features

    ```txt
    Connect GitHub
    Select repository
    Browse file tree
    Open file into Monaco
    Ask AI to edit file
    Preview diff
    Save to branch
    Create pull request
    Run Playwright
    Deploy if approved
    ```

    ## Required Backend Routes

    ```txt
    GET  /api/oauth/github/start
    GET  /api/oauth/github/callback
    GET  /api/github/repos
    GET  /api/github/repos/:owner/:repo/tree
    GET  /api/github/repos/:owner/:repo/file
    POST /api/github/repos/:owner/:repo/file
    POST /api/github/repos/:owner/:repo/branch
    POST /api/github/repos/:owner/:repo/pull-request
    POST /api/webhooks/github
    ```

    ## Progress Checks

    - [ ] Connor can authorize GitHub.
    - [ ] Dashboard can list repos.
    - [ ] Dashboard can read repo tree.
    - [ ] Monaco can open a repo file.
    - [ ] Agent can propose an edit.
    - [ ] Dashboard can show diff before saving.
    - [ ] Dashboard can save to a branch.
    - [ ] Dashboard can open a PR.
    ''')

    write("docs/integrations/GOOGLE_DRIVE_GMAIL_SETUP_PLAYBOOK.md", r'''
    # Google Drive and Gmail Setup Playbook

    ## Goal

    Google integrations allow Connor to connect his work files and communication workflows to the dashboard.

    Drive is for:

    ```txt
    importing docs
    indexing PDFs
    syncing client assets
    sending files to R2
    powering RAG
    ```

    Gmail is for:

    ```txt
    lead followups
    drafting replies
    project communication history
    inbox summaries
    CRM notes
    ```

    ## Google Cloud Setup

    1. Create a Google Cloud project.
    2. Configure OAuth consent screen.
    3. Add app name:

    ```txt
    Leadership Legacy Digital
    ```

    4. Add authorized domain when final domain is ready.
    5. Create OAuth 2.0 Client ID.
    6. Application type:

    ```txt
    Web application
    ```

    7. Authorized redirect URI:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/google/callback
    ```

    ## Enable APIs

    Enable:

    ```txt
    Google Drive API
    Gmail API
    Google People API optional
    ```

    ## Recommended OAuth Scopes

    Start narrow.

    ```txt
    openid
    email
    profile
    https://www.googleapis.com/auth/drive.metadata.readonly
    https://www.googleapis.com/auth/drive.readonly
    https://www.googleapis.com/auth/gmail.readonly
    https://www.googleapis.com/auth/gmail.compose
    ```

    Only request broader scopes after the product needs them.

    ## Cloudflare Secrets

    ```bash
    npx wrangler secret put GOOGLE_CLIENT_ID
    npx wrangler secret put GOOGLE_CLIENT_SECRET
    npx wrangler secret put GOOGLE_REDIRECT_URI
    ```

    `GOOGLE_REDIRECT_URI` should be:

    ```txt
    https://leadership-legacy.meauxbility.workers.dev/api/oauth/google/callback
    ```

    ## Token Storage Rules

    Do not store refresh tokens in:

    ```txt
    browser localStorage
    public R2 objects
    React state
    Git
    ```

    Store token metadata server-side.

    Recommended:

    ```txt
    D1 for token account references
    Supabase for encrypted integration logs
    KV only for temporary OAuth state
    ```

    ## Required Backend Routes

    ```txt
    GET  /api/oauth/google/start
    GET  /api/oauth/google/callback
    POST /api/oauth/google/disconnect

    GET  /api/google-drive/files
    GET  /api/google-drive/files/:id
    POST /api/google-drive/import-to-r2
    POST /api/google-drive/ingest-to-rag

    GET  /api/gmail/threads
    GET  /api/gmail/threads/:id
    POST /api/gmail/drafts
    POST /api/gmail/send-draft
    ```

    ## Drive Workflow

    ```txt
    Connect Google
    Browse Drive folders
    Pick docs/PDFs
    Import metadata
    Download server-side
    Store copy/snapshot in R2
    Chunk text
    Embed
    Save document chunks to Supabase
    Expose source-cited answers in dashboard
    ```

    ## Gmail Workflow

    ```txt
    Connect Google
    Search relevant threads
    Summarize thread
    Draft reply with OpenAI/Anthropic
    User reviews draft
    Send or save
    Log CRM note
    ```

    ## Progress Checks

    - [ ] OAuth consent screen configured.
    - [ ] Drive API enabled.
    - [ ] Gmail API enabled.
    - [ ] Google callback route planned.
    - [ ] Secrets added to Cloudflare.
    - [ ] OAuth state stored in KV.
    - [ ] Dashboard can show connected Google account.
    - [ ] Drive file list works.
    - [ ] Gmail thread list works.
    - [ ] No tokens exposed to browser.
    ''')

    write("docs/integrations/MCP_TOOLS_PLAYBOOK.md", r'''
    # MCP and Tools Playbook

    ## Goal

    MCP-style tool architecture gives the dashboard and Agent Connor a consistent way to call tools safely.

    Tools should not be random one-off functions. They should be registered, permissioned, logged, tested, and monitored.

    ## Tool Categories

    ```txt
    Repo tools
    File tools
    R2 tools
    D1 tools
    Supabase tools
    Google Drive tools
    Gmail tools
    OpenAI tools
    Anthropic tools
    Gemini tools
    Resend tools
    Playwright tools
    CAD/OpenSCAD tools
    AWS tools
    Spline tools
    ```

    ## Tool Registry Fields

    Recommended fields:

    ```txt
    id
    tool_key
    display_name
    provider
    category
    description
    input_schema_json
    output_schema_json
    auth_type
    required_secret_names_json
    allowed_roles_json
    is_enabled
    risk_level
    requires_approval
    rate_limit_json
    created_at
    updated_at
    ```

    ## Tool Execution Log Fields

    ```txt
    id
    tool_key
    provider
    user_id
    session_id
    run_group_id
    input_preview
    output_preview
    input_json
    output_json
    status
    error_message
    duration_ms
    cost_usd
    metadata_json
    created_at
    ```

    ## Approval Rules

    Require approval for:

    ```txt
    sending email
    deleting files
    writing to GitHub main branch
    deploying production
    rotating secrets
    spending high AI cost
    running CAD code from untrusted input
    executing terminal commands
    changing DNS
    ```

    Safe without approval:

    ```txt
    reading public CMS pages
    reading R2 metadata
    generating draft code
    summarizing a document
    suggesting a command
    creating a local draft
    running non-destructive diagnostics
    ```

    ## MCP Server Strategy

    Connor can think of MCP as:

    ```txt
    a standardized tool adapter layer for agents
    ```

    The platform should support:

    ```txt
    internal tools
    remote MCP servers
    provider tools
    user-installed tools
    tenant-isolated tools
    per-role allowlists
    ```

    ## First Tools to Build

    ```txt
    github.listRepos
    github.getFile
    github.createBranch
    github.commitFile
    github.openPullRequest

    r2.listObjects
    r2.getObject
    r2.putObject
    r2.deleteObject

    d1.query
    d1.getPage
    d1.savePageDraft
    d1.publishPage

    openai.codeAction
    openai.chat
    anthropic.review
    gemini.compare

    resend.sendLeadNotification
    gmail.createDraft
    drive.importFile

    playwright.runSmoke
    playwright.captureScreenshot
    ```

    ## Progress Checks

    - [ ] Tool registry exists.
    - [ ] Tool execution log exists.
    - [ ] Tool inputs are validated.
    - [ ] Tool outputs are normalized.
    - [ ] Tool errors are logged.
    - [ ] Risk levels are assigned.
    - [ ] Approval gates are enforced.
    - [ ] Secrets are never returned to browser.
    ''')

    write("docs/integrations/AI_PROVIDERS_SETUP_PLAYBOOK.md", r'''
    # AI Providers Setup Playbook

    ## Goal

    Connor should understand how OpenAI, Anthropic, Gemini, Workers AI, and local Llama/Ollama fit together.

    ## Provider Roles

    | Provider | Best Use |
    |---|---|
    | OpenAI | Default code generation, agent actions, structured outputs, image generation |
    | Anthropic | Review, architecture, long-form critique, second-opinion reasoning |
    | Gemini | Long-context comparison, Google ecosystem workflows, multimodal alternate |
    | Workers AI | Cloudflare-native embeddings, utility inference, fallback |
    | Local Llama/Ollama | Local low-cost experiments and private drafts |

    ## OpenAI

    Current note:

    ```txt
    Sam installed an OpenAI key temporarily.
    Connor should replace it with his own.
    ```

    Add/replace secret:

    ```bash
    npx wrangler secret put OPENAI_API_KEY
    npm run deploy
    ```

    Recommended model lanes:

    ```txt
    gpt-5.4-nano       cheap fast router
    gpt-5.4-mini       default dashboard/code model
    gpt-5.4            deeper architecture/reasoning
    gpt-image-1-mini   budget image generation
    gpt-image-1.5      higher quality image generation
    ```

    Blocked by project policy:

    ```txt
    gpt-5.5
    gpt-5.5-pro
    gpt-5.4-pro
    ```

    ## Anthropic

    Add secret:

    ```bash
    npx wrangler secret put ANTHROPIC_API_KEY
    npm run deploy
    ```

    Use Anthropic for:

    ```txt
    code review
    architecture review
    risk analysis
    prompt critique
    second-opinion evaluation
    ```

    ## Gemini

    Add secret:

    ```bash
    npx wrangler secret put GEMINI_API_KEY
    npm run deploy
    ```

    Use Gemini for:

    ```txt
    long-context document comparison
    multimodal experiments
    alternate provider testing
    cost/quality benchmarking
    ```

    ## Workers AI

    Add binding in `wrangler.jsonc`:

    ```json
    "ai": {
      "binding": "AI"
    }
    ```

    Use Workers AI for:

    ```txt
    embeddings
    classification
    fallback summaries
    cheap internal utilities
    ```

    ## Local Llama/Ollama

    Local setup:

    ```bash
    ollama list
    ollama run llama3.1
    ```

    Suggested local env:

    ```txt
    LOCAL_LLM_BASE_URL=http://localhost:11434
    LOCAL_LLM_MODEL=llama3.1
    ```

    ## Routing Policy

    Use deterministic safety first, then Thompson Sampling for provider/model selection inside safe lanes.

    Deterministic gates:

    ```txt
    blocked model check
    secret availability
    task risk
    max cost
    required modality
    tool support
    context length
    latency budget
    ```

    Thompson Sampling learns from:

    ```txt
    success/failure
    human rating
    latency
    cost
    tool-call reliability
    test pass/fail
    output quality
    ```

    ## Progress Checks

    - [ ] OpenAI secret added.
    - [ ] Anthropic secret added.
    - [ ] Gemini secret added if available.
    - [ ] Workers AI binding added.
    - [ ] Provider status route shows configured providers.
    - [ ] Dashboard can call OpenAI through Worker.
    - [ ] Anthropic review endpoint planned.
    - [ ] Gemini comparison endpoint planned.
    - [ ] Cost logging table is ready.
    - [ ] Blocked model policy enforced.
    ''')

    write("docs/integrations/AWS_SETUP_PLAYBOOK.md", r'''
    # AWS Setup Playbook

    ## Goal

    AWS is optional for this platform, but Connor should understand where it could fit.

    Cloudflare remains the primary runtime. AWS can be used for compatibility, backup, specialized services, or future client needs.

    ## Useful AWS Services

    | AWS Service | Possible Use |
    |---|---|
    | S3 | Backup storage, client compatibility, artifact exports |
    | IAM | Scoped service users and policies |
    | Bedrock | Alternate model provider experiments |
    | Lambda | Specialized server-side tasks if needed |
    | CloudWatch | Logs if AWS services are used |
    | SES | Email alternative to Resend |
    | ECR/ECS | Containerized CAD or heavy processing later |

    ## First AWS Setup

    1. Create AWS account.
    2. Enable MFA.
    3. Create IAM user or role for programmatic access.
    4. Use least privilege.
    5. Never commit AWS keys.

    ## Suggested IAM Permissions

    Start narrow:

    ```txt
    s3:ListBucket
    s3:GetObject
    s3:PutObject
    s3:DeleteObject only if truly needed
    ```

    ## Cloudflare Secrets

    ```bash
    npx wrangler secret put AWS_ACCESS_KEY_ID
    npx wrangler secret put AWS_SECRET_ACCESS_KEY
    npx wrangler secret put AWS_REGION
    npx wrangler secret put AWS_S3_BUCKET
    ```

    ## When to Use AWS Instead of R2

    Use R2 first for this app.

    Use AWS S3 only when:

    ```txt
    client already uses AWS
    a third-party requires S3
    data pipeline already lives in AWS
    Bedrock workflow requires AWS account alignment
    long-term backup strategy requires separate cloud
    ```

    ## AWS Safety Rules

    ```txt
    use IAM least privilege
    rotate keys
    log access
    avoid root keys
    never put AWS keys in browser
    do not duplicate assets without a reason
    prefer R2 for Cloudflare-native workflows
    ```

    ## Progress Checks

    - [ ] AWS account has MFA.
    - [ ] IAM user/role created.
    - [ ] Permissions are scoped.
    - [ ] Keys stored only as secrets.
    - [ ] S3 compatibility decision documented.
    - [ ] Bedrock experiment decision documented.
    ''')

    write("docs/integrations/RESEND_EMAIL_PLAYBOOK.md", r'''
    # Resend Email Setup Playbook

    ## Goal

    Resend handles transactional email.

    Use it for:

    ```txt
    contact form notifications
    lead confirmations
    admin invites
    password reset or magic link later
    publish/deploy notifications
    project status updates
    ```

    ## Setup

    1. Create Resend account.
    2. Add sending domain.
    3. Verify DNS records.
    4. Create API key.
    5. Add Cloudflare secret:

    ```bash
    npx wrangler secret put RESEND_API_KEY
    ```

    ## Recommended Sender Addresses

    ```txt
    hello@leadershiplegacydigital.com
    no-reply@leadershiplegacydigital.com
    admin@leadershiplegacydigital.com
    ```

    ## Required Routes

    ```txt
    POST /api/forms/contact
    POST /api/leads/:id/notify
    POST /api/auth/password-reset
    POST /api/admin/invite
    ```

    ## Email Safety

    ```txt
    validate form input
    rate limit submissions
    log send attempts
    never expose API key
    avoid sending secrets over email
    require approval before agent sends outbound emails
    ```

    ## Progress Checks

    - [ ] Domain added to Resend.
    - [ ] DNS verified.
    - [ ] API key stored in Cloudflare.
    - [ ] Contact form email route built.
    - [ ] Lead confirmation template created.
    - [ ] Send logs saved to D1 or Supabase.
    ''')

    write("docs/CONNOR_COURSE_STUDY_GUIDE.md", r'''
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
    ''')

    write("docs/CONNOR_PROGRESS_TRACKER.md", r'''
    # Connor Progress Tracker

    Use this tracker during onboarding.

    ## Setup Progress

    | Area | Not Started | In Progress | Complete | Notes |
    |---|---:|---:|---:|---|
    | GitHub repo access | [ ] | [ ] | [ ] | |
    | Local npm install | [ ] | [ ] | [ ] | |
    | Local dev server | [ ] | [ ] | [ ] | |
    | Cloudflare login | [ ] | [ ] | [ ] | |
    | Worker deploy | [ ] | [ ] | [ ] | |
    | R2 bucket | [ ] | [ ] | [ ] | |
    | D1 database | [ ] | [ ] | [ ] | |
    | KV namespaces | [ ] | [ ] | [ ] | |
    | Durable Objects | [ ] | [ ] | [ ] | |
    | Supabase project | [ ] | [ ] | [ ] | |
    | OpenAI key | [ ] | [ ] | [ ] | |
    | Anthropic key | [ ] | [ ] | [ ] | |
    | Gemini key | [ ] | [ ] | [ ] | |
    | Resend key/domain | [ ] | [ ] | [ ] | |
    | Google OAuth | [ ] | [ ] | [ ] | |
    | Gmail API | [ ] | [ ] | [ ] | |
    | Drive API | [ ] | [ ] | [ ] | |
    | GitHub OAuth/App | [ ] | [ ] | [ ] | |
    | AWS optional setup | [ ] | [ ] | [ ] | |
    | Playwright tests | [ ] | [ ] | [ ] | |

    ## Skill Progress

    Rate each 1-5.

    | Skill | Score | Evidence |
    |---|---:|---|
    | Can run app locally |  | |
    | Can deploy Worker |  | |
    | Understands R2 |  | |
    | Understands D1 |  | |
    | Understands Supabase |  | |
    | Understands OAuth |  | |
    | Understands API secrets |  | |
    | Can use dashboard IDE |  | |
    | Can run Playwright |  | |
    | Can approve/reject agent actions |  | |
    | Can read tool logs |  | |
    | Can debug failed deploys |  | |

    ## Weekly Review

    ### Week Of

    ```txt
    Date:
    Reviewer:
    ```

    ### Wins

    ```txt
    -
    -
    -
    ```

    ### Blockers

    ```txt
    -
    -
    -
    ```

    ### Next Focus

    ```txt
    -
    -
    -
    ```
    ''')

    write("docs/RUBRIC.md", r'''
    # Leadership Legacy Integration Rubric

    This rubric scores whether Connor and the platform are ready for production-grade tool usage.

    ## Scoring

    ```txt
    0 = Not present
    1 = Started but not usable
    2 = Partially usable with manual work
    3 = Usable for internal testing
    4 = Production-ready with guardrails
    5 = Production-ready, monitored, documented, and tested
    ```

    ## Category A: Integration Setup

    | Score | Definition |
    |---:|---|
    | 0 | No account/API/resource exists |
    | 1 | Account exists but not connected |
    | 2 | Secret/resource added but not verified |
    | 3 | Integration works manually |
    | 4 | Integration works through dashboard/API with safe errors |
    | 5 | Integration is tested, logged, monitored, and documented |

    Applies to:

    ```txt
    GitHub
    Google Drive
    Gmail
    OpenAI
    Anthropic
    Gemini
    Resend
    Supabase
    D1
    R2
    KV
    Durable Objects
    Workers AI
    AWS
    ```

    ## Category B: Secret Safety

    | Score | Definition |
    |---:|---|
    | 0 | Secrets are exposed or committed |
    | 1 | Secrets are manually copied around |
    | 2 | Secrets are stored server-side but undocumented |
    | 3 | Secrets are stored correctly in Worker/provider dashboards |
    | 4 | Secret usage is audited and never returned to browser |
    | 5 | Rotation, least privilege, and incident plan exist |

    Required standard before production:

    ```txt
    4 minimum
    ```

    ## Category C: Dashboard Usability

    | Score | Definition |
    |---:|---|
    | 0 | Dashboard does not load |
    | 1 | Dashboard loads but is confusing or broken |
    | 2 | Dashboard has basic navigation |
    | 3 | Dashboard supports real internal workflows |
    | 4 | Dashboard is clear, fast, and role-aware |
    | 5 | Dashboard is polished, tested, documented, and production-ready |

    Required standard before client-facing demo:

    ```txt
    3 minimum
    ```

    Required standard before real production:

    ```txt
    4 minimum
    ```

    ## Category D: AI Tooling

    | Score | Definition |
    |---:|---|
    | 0 | No AI provider works |
    | 1 | One provider works manually |
    | 2 | One provider works through API |
    | 3 | Multiple providers are configured |
    | 4 | Provider routing, cost logs, and fallbacks work |
    | 5 | Evals, cost controls, human ratings, and automatic routing optimization work |

    Required standard before serious use:

    ```txt
    3 minimum
    ```

    Required standard before automated workflows:

    ```txt
    4 minimum
    ```

    ## Category E: Tool Execution Safety

    | Score | Definition |
    |---:|---|
    | 0 | Tools execute without controls |
    | 1 | Tools are hardcoded and unlogged |
    | 2 | Tools are logged but not permissioned |
    | 3 | Tools have input validation and basic logging |
    | 4 | Tools have risk levels, approval gates, and audit logs |
    | 5 | Tools are fully governed, tested, monitored, and reversible |

    Any destructive tool requires:

    ```txt
    4 minimum
    ```

    Destructive examples:

    ```txt
    delete file
    send email
    deploy production
    write to main branch
    rotate secret
    change DNS
    execute terminal command
    delete R2 object
    delete database row
    ```

    ## Category F: Testing

    | Score | Definition |
    |---:|---|
    | 0 | No tests |
    | 1 | Manual testing only |
    | 2 | Build passes |
    | 3 | Playwright smoke tests pass |
    | 4 | Core dashboard/API workflows are tested |
    | 5 | CI, traces, screenshots, evals, and deployment gates are active |

    Required standard before production:

    ```txt
    4 minimum
    ```

    ## Category G: Connor Readiness

    | Score | Definition |
    |---:|---|
    | 0 | Connor has no access or understanding |
    | 1 | Connor can view the app |
    | 2 | Connor can run basic commands with help |
    | 3 | Connor can run, test, and deploy with a guide |
    | 4 | Connor can diagnose common issues |
    | 5 | Connor can independently operate and improve the platform |

    Required standard before handoff:

    ```txt
    3 minimum
    ```

    Strong handoff target:

    ```txt
    4 minimum
    ```

    ## Final Readiness Matrix

    | Area | Target Score | Actual Score | Pass |
    |---|---:|---:|---|
    | Integration setup | 4 |  | [ ] |
    | Secret safety | 4 |  | [ ] |
    | Dashboard usability | 4 |  | [ ] |
    | AI tooling | 4 |  | [ ] |
    | Tool execution safety | 4 |  | [ ] |
    | Testing | 4 |  | [ ] |
    | Connor readiness | 3 |  | [ ] |

    ## Production Decision

    Production-ready only if:

    ```txt
    no category below target
    no exposed secrets
    no destructive tools without approval
    build passes
    Playwright passes
    health endpoints pass
    dashboard auth is production-grade
    ```
    ''')

    write("docs/END_TO_END_INTEGRATION_PLAYBOOK.md", r'''
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
    ''')

    write("scripts/check-tools-docs.sh", r'''
    #!/usr/bin/env bash
    set -euo pipefail

    files=(
      "docs/TOOLS_README.md"
      "docs/integrations/GITHUB_SETUP_PLAYBOOK.md"
      "docs/integrations/GOOGLE_DRIVE_GMAIL_SETUP_PLAYBOOK.md"
      "docs/integrations/MCP_TOOLS_PLAYBOOK.md"
      "docs/integrations/AI_PROVIDERS_SETUP_PLAYBOOK.md"
      "docs/integrations/AWS_SETUP_PLAYBOOK.md"
      "docs/integrations/RESEND_EMAIL_PLAYBOOK.md"
      "docs/CONNOR_COURSE_STUDY_GUIDE.md"
      "docs/CONNOR_PROGRESS_TRACKER.md"
      "docs/RUBRIC.md"
      "docs/END_TO_END_INTEGRATION_PLAYBOOK.md"
    )

    for file in "${files[@]}"; do
      if [[ ! -f "$file" ]]; then
        echo "Missing $file"
        exit 1
      fi
      echo "OK $file"
    done

    echo "Tools docs complete."
    ''')

    run(["chmod", "+x", "scripts/check-tools-docs.sh"], check=False)
    run(["./scripts/check-tools-docs.sh"], check=True)

    run([
      "git", "add",
      "docs/TOOLS_README.md",
      "docs/integrations",
      "docs/CONNOR_COURSE_STUDY_GUIDE.md",
      "docs/CONNOR_PROGRESS_TRACKER.md",
      "docs/RUBRIC.md",
      "docs/END_TO_END_INTEGRATION_PLAYBOOK.md",
      "scripts/check-tools-docs.sh",
      "scripts/generate_tools_integration_playbook.py"
    ], check=False)

    run(["git", "commit", "-m", "docs: add tools integration playbook and Connor course rubric"], check=False)

    print("\nTools README, integration playbooks, Connor course, tracker, and rubric generated.")
    print("Next:")
    print("git push origin main")
    print("open docs/TOOLS_README.md")
    print("open docs/END_TO_END_INTEGRATION_PLAYBOOK.md")
    print("open docs/RUBRIC.md")

if __name__ == "__main__":
    main()
