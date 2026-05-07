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
