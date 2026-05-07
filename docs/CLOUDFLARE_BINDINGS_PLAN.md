# Cloudflare Bindings Plan

This project should eventually use these Cloudflare bindings.

## Static Assets

```json
"assets": {
  "directory": "./dist",
  "binding": "ASSETS"
}
```

## R2

```json
"r2_buckets": [
  {
    "binding": "WEBSITE",
    "bucket_name": "leadership-legacy"
  }
]
```

## D1

```json
"d1_databases": [
  {
    "binding": "DB",
    "database_name": "leadership-legacy-cms",
    "database_id": "PASTE_DATABASE_ID"
  }
]
```

## KV

```json
"kv_namespaces": [
  {
    "binding": "LL_SESSIONS",
    "id": "PASTE_ID"
  },
  {
    "binding": "LL_RATE_LIMITS",
    "id": "PASTE_ID"
  },
  {
    "binding": "LL_CACHE",
    "id": "PASTE_ID"
  },
  {
    "binding": "LL_OAUTH_STATE",
    "id": "PASTE_ID"
  },
  {
    "binding": "LL_FLAGS",
    "id": "PASTE_ID"
  }
]
```

## Durable Objects

```json
"durable_objects": {
  "bindings": [
    {
      "name": "DASHBOARD_SESSION",
      "class_name": "DashboardSession"
    },
    {
      "name": "AGENT_SESSION",
      "class_name": "AgentSession"
    }
  ]
}
```

## Workers AI

```json
"ai": {
  "binding": "AI"
}
```

## Recommended Secrets

```txt
OPENAI_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
RESEND_API_KEY
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI
```
