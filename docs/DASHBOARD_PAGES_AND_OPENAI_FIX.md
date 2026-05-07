# Dashboard Pages and OpenAI Fix

This update fixes three issues.

## 1. OpenAI Key Diagnostics

Added:

```txt
GET /api/openai/diagnostics
GET /api/openai/test
```

Diagnostics show only key shape, never the full key.

This helps catch the common mistake of setting the Worker secret as:

```txt
OPENAI_API_KEY=sk-...
```

Instead of only:

```txt
sk-...
```

## 2. Flexfit Drag Direction

The right panel drag math is now natural:

```txt
drag left = agent panel expands
drag right = agent panel shrinks
drag terminal divider up = terminal expands
drag terminal divider down = terminal shrinks
```

## 3. True Dashboard Pages

Monaco is now reserved for:

```txt
/dashboard/agent
/dashboard/dev
/dashboard/dev/editor
/dashboard/dev/terminal
```

Designed dashboard pages now render for:

```txt
/dashboard
/dashboard/storage
/dashboard/settings
/dashboard/analytics
/dashboard/learn
/dashboard/mail
/dashboard/mcp
```

This keeps the interface Cursor-like, but gives Connor actual places to learn, monitor, configure, and operate.
