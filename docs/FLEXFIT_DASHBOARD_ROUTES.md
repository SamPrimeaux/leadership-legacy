# Flexfit Dashboard Routes

The dashboard now supports routed IDE views:

```txt
/dashboard
/dashboard/agent
/dashboard/storage
/dashboard/settings
/dashboard/analytics
/dashboard/learn
/dashboard/mail
/dashboard/mcp
```

## Added Capabilities

```txt
Resizable explorer width
Resizable agent panel width
Resizable terminal height
Real R2 object listing
Text/code R2 object open into Monaco
GitHub status endpoint
GitHub OAuth start placeholder
Google OAuth start placeholder
View-specific dashboard panels
Route-aware activity rail
```

## Real R2 Access

The dashboard calls:

```txt
GET /api/r2/list?prefix=
GET /api/r2/text?key=<r2-key>
GET /api/r2/object/<r2-key>
```

Text-like files open into Monaco.

Binary files should be previewed/downloaded through `/api/r2/object/`.

## GitHub

Prepared routes:

```txt
GET /api/github/status
GET /api/oauth/github/start
```

Required secrets:

```txt
GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET
GITHUB_APP_ID
GITHUB_APP_PRIVATE_KEY
GITHUB_WEBHOOK_SECRET
```

## Google Drive / Gmail

Prepared route:

```txt
GET /api/oauth/google/start
```

Required secrets:

```txt
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI
```

## Next Implementation Layer

```txt
GitHub file tree
GitHub file read into Monaco
GitHub branch save
GitHub PR creation
R2 upload from Monaco
R2 binary preview drawer
D1 CMS read/write panels
Gmail drafts
Drive file import
MCP tool execution log
```
