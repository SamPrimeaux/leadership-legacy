# EMAIL SYSTEM TEMPLATE

**For:** Connor McNeely — connordmcneely@leadershiplegacydigital.com  
**From:** Sam Primeaux / Inner Animal Media  
**Repo:** `SamPrimeaux/leadership-legacy`  
**Reference build (live today):** Companions of CPAS email workspace at `/dashboard/email`  
**Your dashboard route (planned):** `/dashboard/mail`

---

## Brief summary (read this first)

Connor — this doc is your **copy-paste email system template**. You do not need to invent inbound/outbound/automated email from scratch.

We already run a production version for **Companions of CPAS** (`companionscpas` Worker on `companionsofcaddo.org`). That stack is:

| Piece | What it does |
|---|---|
| **Resend (outbound)** | Your app sends emails (contact confirmations, lead replies, password resets, etc.) |
| **Resend (inbound)** | Emails sent *to* your support address arrive in your dashboard inbox via webhook |
| **D1 database** | Stores inbox messages, sent log, drafts, and HTML templates |
| **Dashboard mail UI** | Admin reads, replies, and composes from `/dashboard/email` |
| **Gmail OAuth (optional)** | Sync a personal or work Gmail inbox into the same UI — per user, approval-gated |

**Three ideas, plain English:**

1. **Outbound** — your Worker calls Resend’s API to *send* mail (`POST https://api.resend.com/emails`).
2. **Inbound** — Resend receives mail at your domain and POSTs a webhook to your Worker (`POST /api/email/inbound`). You save it in D1 and show it in the dashboard.
3. **Automated / transactional** — when something happens (contact form, lead signup, deploy), your Worker loads an HTML template from D1, fills in `{{variables}}`, and sends via Resend. No human clicks Send.

Install this on **your own schedule**. Nothing here blocks your current site. Work in small steps and check each box.

**Related docs already in this repo:**

- `docs/integrations/RESEND_EMAIL_PLAYBOOK.md` — Resend account + DNS
- `docs/integrations/GOOGLE_DRIVE_GMAIL_SETUP_PLAYBOOK.md` — Gmail OAuth later
- `docs/email-system/` — SQL + seed templates to run against D1

---

## Architecture (what you are building)

```txt
Public site / contact form
        │
        ▼
Cloudflare Worker (leadership-legacy)
        │
        ├── Outbound ──► Resend API ──► recipient inbox
        │
        ├── Inbound ◄── Resend webhook ◄── mail to hello@ / support@
        │
        ├── Templates ◄── D1 email_templates ({{first_name}}, etc.)
        │
        └── Dashboard ◄── D1 inbound_emails, email_logs, email_drafts
                │
                └── /dashboard/mail (React UI — you wire this up)
```

**Source reference (Sam’s live implementation):**

| File | Purpose |
|---|---|
| `companionscpas/public/dashboard/js/view-email.jsx` | Mail workspace UI |
| `companionscpas/public/dashboard/dash.css` | Mail layout styles (`.mail-app`, compose sheet) |
| `companionscpas/src/api/email_api.js` | Inbox, send, drafts, webhooks, campaigns |
| `companionscpas/src/api/gmail_api.js` | Gmail OAuth + sync (optional phase 2) |
| `companionscpas/db/migrations/20260619_email_inbox.sql` | Core D1 tables |
| `companionscpas/db/seed_002_email_templates.sql` | Branded HTML templates |

You can port files from `companionscpas` or follow the phased plan below.

---

## Phase 0 — Concepts checklist (15 min read)

Before touching code, be comfortable with these terms:

| Term | Meaning |
|---|---|
| **Transactional email** | Automatic email triggered by an event (form submit, payment, invite) |
| **From address** | What recipients see (`Leadership Legacy <hello@leadershiplegacydigital.com>`) |
| **Webhook** | Resend calls your URL when mail arrives; your Worker saves it |
| **Template key** | Stable ID like `contact_form_notify` stored in D1 |
| **`{{variable}}`** | Placeholder replaced at send time (`{{first_name}}` → `Connor`) |
| **API key secret** | `RESEND_API_KEY` lives in Cloudflare secrets — never in git |

---

## Phase 1 — Resend account (outbound only)

**Goal:** Send one test email from your Worker.

### 1. Create Resend account

1. Sign up at [resend.com](https://resend.com).
2. Add domain **`leadershiplegacydigital.com`** (or your production domain).
3. Add DNS records Resend gives you (SPF, DKIM, etc.) in Cloudflare DNS.
4. Wait until domain shows **Verified**.

### 2. Create API key

1. Resend → API Keys → Create.
2. Store in Cloudflare (from repo root):

```bash
cd leadership-legacy
npx wrangler secret put RESEND_API_KEY
```

Paste the raw key only (`re_...`), not `RESEND_API_KEY=re_...`.

### 3. Add wrangler vars

Edit `wrangler.jsonc` and add under `"vars"`:

```jsonc
"RESEND_FROM_EMAIL": "Leadership Legacy Digital <hello@leadershiplegacydigital.com>",
"RESEND_SUPPORT_FROM": "Leadership Legacy Digital <hello@leadershiplegacydigital.com>",
"EMAIL_INBOX_MAILBOXES": "hello@leadershiplegacydigital.com",
"ADMIN_EMAIL": "connordmcneely@leadershiplegacydigital.com"
```

### 4. Smoke test (temporary route)

Add a dev-only test handler in `src/worker/index.js` or run from Wrangler dev:

```bash
curl -X POST "https://leadership-legacy.meauxbility.workers.dev/api/email/send" \
  -H "Content-Type: application/json" \
  -d '{"to":"connordmcneely@leadershiplegacydigital.com","subject":"Resend test","html":"<p>Outbound works.</p>"}'
```

**Done when:** You receive the test email in your inbox.

See also: `docs/integrations/RESEND_EMAIL_PLAYBOOK.md`.

---

## Phase 2 — D1 database (storage)

**Goal:** Tables for templates, sent log, and inbox.

### 1. Create D1 database

```bash
npx wrangler d1 create leadership-legacy
```

Copy the `database_id` into `wrangler.jsonc`:

```jsonc
"d1_databases": [
  {
    "binding": "DB",
    "database_name": "leadership-legacy",
    "database_id": "<paste-id-here>"
  }
]
```

### 2. Apply schema + seeds

From repo root:

```bash
npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/001_schema.sql
npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/002_seed_templates.sql
```

### 3. Verify

```bash
npx wrangler d1 execute leadership-legacy --remote --command \
  "SELECT template_key, subject FROM email_templates WHERE status = 'active'"
```

**Done when:** You see rows like `contact_form_notify`, `lead_confirmation`.

---

## Phase 3 — Worker API (send + templates)

**Goal:** `POST /api/email/send` and template-based sends.

### Minimum routes to implement

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/email/send` | Manual / dashboard outbound |
| `POST` | `/api/email/inbound` | Resend inbound webhook (no auth) |
| `GET` | `/api/email/inbox` | List inbound (auth required) |
| `GET` | `/api/email/outbound` | Sent log (auth required) |
| `GET` | `/api/email/templates` | List active templates |
| `POST` | `/api/forms/contact` | Public contact → notify admin + confirm to user |

### Template send helper (copy into Worker)

```javascript
async function sendTemplateEmail(env, { templateKey, to, vars = {}, type }) {
  const tpl = await env.DB.prepare(
    "SELECT subject, body_html, body_text FROM email_templates WHERE template_key = ? AND status = 'active' LIMIT 1"
  ).bind(templateKey).first();

  if (!tpl) return { ok: false, error: "template_not_found" };

  let subject = tpl.subject || "";
  let html = tpl.body_html || "";
  let text = tpl.body_text || "";
  for (const [k, v] of Object.entries(vars)) {
    const token = `{{${k}}}`;
    const val = String(v ?? "");
    subject = subject.replaceAll(token, val);
    html = html.replaceAll(token, val);
    text = text.replaceAll(token, val);
  }

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: env.RESEND_FROM_EMAIL,
      to: [to],
      subject,
      html,
      text,
    }),
  });

  const parsed = await res.json().catch(() => ({}));
  return res.ok ? { ok: true, id: parsed.id } : { ok: false, error: JSON.stringify(parsed) };
}
```

**Port full API from:** `companionscpas/src/api/email_api.js` (rename tenant id to `tenant_leadership_legacy`).

**Done when:** Contact form triggers two emails — one to you, one confirmation to the submitter.

---

## Phase 4 — Inbound webhook (mail arrives in dashboard)

**Goal:** Email sent to `hello@leadershiplegacydigital.com` shows up in D1 + dashboard.

### 1. Resend inbound setup

1. Resend → Domains → your domain → **Inbound** (or Receiving).
2. Configure MX records if prompted.
3. Create inbound route → webhook URL:

```txt
https://leadership-legacy.meauxbility.workers.dev/api/email/inbound
```

4. Copy webhook signing secret:

```bash
npx wrangler secret put RESEND_INBOUND_WEBHOOK_SECRET
```

### 2. Webhook handler

Port `handleInboundWebhook` + `verifyResendWebhook` from `companionscpas/src/api/email_api.js`.

Important: `/api/email/inbound` must **not** require dashboard login — Resend calls it directly.

### 3. Test

Send an email from your personal account to `hello@leadershiplegacydigital.com`.

```bash
npx wrangler d1 execute leadership-legacy --remote --command \
  "SELECT subject, from_email, received_at FROM inbound_emails ORDER BY received_at DESC LIMIT 5"
```

**Done when:** Row appears in `inbound_emails`.

---

## Phase 5 — Dashboard mail UI

**Goal:** `/dashboard/mail` becomes a real inbox, not a placeholder.

Your repo already has a **Mail** nav item pointing to `/dashboard/mail`. Today it shows prep copy in `AgentIDE`.

### Option A — Port the CPAS mail client (recommended)

1. Copy `companionscpas/public/dashboard/js/view-email.jsx` → adapt for React in `src/dashboard/pages/MailWorkspace.jsx`.
2. Copy relevant `.mail-*` CSS from `companionscpas/public/dashboard/dash.css` into your dashboard styles.
3. Wire API calls to `/api/email/*` (same contract as CPAS — see table in Phase 3).
4. Replace tenant branding (logo, colors, copy).

### Option B — Minimal v1 (inbox list only)

1. Fetch `GET /api/email/inbox`.
2. Render subject, from, date in a table.
3. Add “Reply” that opens `POST /api/email/send` with pre-filled `to` + `subject`.

**Done when:** You can read inbound mail and send a reply from the dashboard.

---

## Phase 6 — Gmail OAuth (optional, later)

**Goal:** Sync Gmail into the same mail UI (read + draft; send still approval-gated).

Follow `docs/integrations/GOOGLE_DRIVE_GMAIL_SETUP_PLAYBOOK.md`, then port:

- `companionscpas/src/api/gmail_api.js`
- `companionscpas/src/api/gmail_scope.js`

Do this **after** Resend outbound + inbound work. Gmail adds OAuth complexity.

---

## Automated email triggers (what to wire when)

| Event | Template key | Send to |
|---|---|---|
| Contact form submit | `contact_form_notify` | `ADMIN_EMAIL` |
| Contact form submit | `lead_confirmation` | submitter email |
| New lead captured | `lead_welcome` | lead email |
| Admin invite (later) | `admin_invite` | invitee |
| Password reset (later) | `password_reset` | user |

All templates live in `docs/email-system/002_seed_templates.sql`. Edit HTML there, re-run the seed, or update rows in D1 directly.

---

## Security rules (non-negotiable)

```txt
Never commit RESEND_API_KEY or webhook secrets
Never expose API keys to the browser
Rate-limit public form endpoints
Verify Resend webhook signatures on /api/email/inbound
Require dashboard auth on inbox/send routes
Require human approval before Agent Connor sends outbound mail
Log every send to email_logs
```

---

## Install checklist (print this)

### Week 1 — Outbound

- [ ] Resend account + domain verified
- [ ] `RESEND_API_KEY` in Cloudflare secrets
- [ ] `wrangler.jsonc` vars added
- [ ] Test send received at connordmcneely@leadershiplegacydigital.com

### Week 2 — Database + templates

- [ ] D1 created + bound as `DB`
- [ ] `001_schema.sql` applied
- [ ] `002_seed_templates.sql` applied
- [ ] Template query returns active rows

### Week 3 — API

- [ ] `/api/email/send` works
- [ ] Contact form sends admin + user emails
- [ ] Sends logged in `email_logs`

### Week 4 — Inbound

- [ ] Resend inbound webhook configured
- [ ] `RESEND_INBOUND_WEBHOOK_SECRET` set
- [ ] Test inbound email stored in `inbound_emails`

### Week 5 — Dashboard

- [ ] `/dashboard/mail` lists inbox
- [ ] Reply flow works
- [ ] Sent tab shows outbound log

### Later

- [ ] Gmail OAuth connected
- [ ] Campaigns / newsletter (optional)
- [ ] Custom domain on production Worker URL

---

## Quick commands reference

```bash
# Secrets
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put RESEND_INBOUND_WEBHOOK_SECRET

# D1 migrations
npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/001_schema.sql
npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/002_seed_templates.sql

# Inspect
npx wrangler d1 execute leadership-legacy --remote --command "SELECT * FROM email_templates"
npx wrangler d1 execute leadership-legacy --remote --command "SELECT subject, from_email FROM inbound_emails ORDER BY received_at DESC LIMIT 10"

# Deploy
npm run build && npm run deploy
```

---

## Questions?

If you get stuck, check in this order:

1. Resend dashboard → Logs (did the send fail? DNS issue?)
2. Cloudflare Worker → Observability logs (webhook errors?)
3. D1 queries above (did the row save?)
4. Compare your route handler to `companionscpas/src/api/email_api.js`

This template is intentionally boring and step-by-step. Email systems fail in predictable places (DNS, secrets, webhook auth, missing D1 binding). Fix one layer at a time.

— Sam
