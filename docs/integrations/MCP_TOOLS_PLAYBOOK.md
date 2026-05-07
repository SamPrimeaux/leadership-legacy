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
