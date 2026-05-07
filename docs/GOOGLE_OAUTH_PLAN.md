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
