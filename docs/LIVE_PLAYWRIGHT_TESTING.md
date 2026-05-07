# Live Playwright Testing

Playwright now defaults to the deployed Worker:

```txt
https://leadership-legacy.meauxbility.workers.dev
```

## Run live production smoke tests

```bash
npm run test:e2e
```

## Run against another deployed URL

```bash
PLAYWRIGHT_BASE_URL=https://your-url.workers.dev npm run test:e2e
```

## Run against local Vite instead

```bash
LOCAL_E2E=1 npm run test:e2e
```

## Tested routes

Public:

```txt
/
/services
/work
/about
/resources
/contact
```

Dashboard:

```txt
/dashboard
/dashboard/agent
/dashboard/storage
/dashboard/analytics
/dashboard/learn
/dashboard/mail
/dashboard/mcp
/dashboard/settings
```

APIs:

```txt
/api/health
/api/ai/providers
/api/openai/diagnostics
/api/openai/test
/api/r2/list
/api/github/status
```
