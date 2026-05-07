# InnerAnimal-Style Dashboard Remaster

This remaster removes the oversized dashboard headers and replaces the experience with a full-height IDE workspace.

## Design Direction

```txt
Activity rail
Explorer sidebar
Cloudflare R2 panel
GitHub/Drive connection cards
Editor tabs
Monaco center editor
Right Agent panel
Bottom terminal drawer
Thin status bar
No fake marketing hero headers inside dashboard
No iframe-style card wrapper
```

## Main Route

```txt
/dashboard
/dashboard/agent
/dashboard/dev
```

## OpenAI

Agent panel calls:

```txt
POST /api/openai/code
```

The OpenAI key remains server-side as:

```txt
OPENAI_API_KEY
```

## Terminal

The terminal is xterm-prepped and command-copy enabled. It does not execute shell commands yet.

Production terminal execution still needs:

```txt
Worker auth
Durable Object session
PTY service
command allowlist
audit logs
secret redaction
```
