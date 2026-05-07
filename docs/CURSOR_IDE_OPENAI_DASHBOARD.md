# Cursor-Style IDE Dashboard + OpenAI

The dashboard has been remastered into a Cursor-style IDE cockpit.

## Routes

```txt
/dashboard
/dashboard/dev
/dashboard/dev/editor
/dashboard/dev/terminal
/dashboard/dev/agent
```

## Features

```txt
Cursor-style shell
Activity bar
Sidebar navigation
Monaco editor
File explorer
xterm terminal dock
PowerShell command presets
OpenAI-backed code generation endpoint
AI result copy/apply-to-editor workflow
Provider settings
R2/CMS/dashboard routes preserved
```

## OpenAI Endpoints

```txt
POST /api/openai/code
POST /api/openai/chat
GET  /api/ai/providers
GET  /api/health
```

## Security

The OpenAI key stays in the Worker as:

```txt
OPENAI_API_KEY
```

The browser never receives the key.

## Example OpenAI Code Request

```json
{
  "model": "gpt-5.4-mini",
  "mode": "refactor",
  "filename": "src/worker/index.js",
  "language": "javascript",
  "instruction": "Add a CMS save draft endpoint.",
  "code": "current file contents"
}
```

## Production Notes

The terminal is xterm-ready, but command execution is intentionally not enabled yet.

Production terminal execution needs:

```txt
Auth
Durable Object session
PTY bridge
command allowlist
audit logs
timeout limits
secret redaction
```
