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
