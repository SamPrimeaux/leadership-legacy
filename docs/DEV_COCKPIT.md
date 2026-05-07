# Developer Cockpit

The dashboard now includes a developer cockpit for Connor.

Routes:

```txt
/dashboard/dev
/dashboard/dev/editor
/dashboard/dev/tunnel
```

## Features

```txt
Monaco Editor draft workspace
xterm browser terminal surface
PowerShell command presets
Cloudflare Tunnel setup commands
Local machine onboarding checklist
Worker/DO/PTY preparation notes
```

## Why this exists

Connor is newer to CLI/terminal workflows and uses PowerShell. The cockpit makes commands copyable, visible, and explained inside the dashboard.

## Current limitation

The terminal is currently browser-side and instructional. It does not execute commands yet.

## Production path

Future architecture:

```txt
Dashboard
→ Worker auth
→ Durable Object session
→ PTY/tunnel service
→ PowerShell/local or hosted shell
→ xterm stream
```

## Security

Do not allow arbitrary terminal execution in production without:

```txt
authentication
authorization
command allowlist
audit logging
timeout limits
workspace isolation
secret redaction
```
