# Leadership Legacy Full CMS SQL Logic

This repo now includes full SQL packs for both Cloudflare D1 and Supabase.

## Cloudflare D1

D1 handles runtime CMS state:

```txt
sql/d1/010_full_cms_runtime.sql
sql/d1/011_full_cms_runtime_triggers.sql
sql/d1/012_full_cms_seed_content.sql
```

D1 owns:

```txt
tenants
workspaces
users
brand settings
themes
navigation
templates
pages
sections
components
page versions
R2 buckets/assets
services
case studies
resources
forms
submissions
leads
redirects
SEO audits
publish jobs
activity log
lightweight analytics
AI provider/model/routing metadata
Thompson routing arms
```

## Supabase

Supabase handles heavier analytics, RAG, evals, and telemetry:

```txt
sql/supabase/010_full_cms_analytics_rag.sql
sql/supabase/011_full_cms_functions.sql
sql/supabase/012_full_cms_seed.sql
```

Supabase owns:

```txt
RAG documents
semantic search logs
knowledge edges
site sessions
site events
lead events
model cost snapshots
routing arms
routing decisions
prompt runs
stream events
tool call events
error events
eval suites
eval runs
R2 object events
Design Studio run metrics
codebase snapshots
codebase files
codebase chunks
codebase symbols
```

## Recommended Apply Commands

D1:

```bash
npx wrangler d1 execute <DB_NAME> --remote --file sql/d1/010_full_cms_runtime.sql
npx wrangler d1 execute <DB_NAME> --remote --file sql/d1/011_full_cms_runtime_triggers.sql
npx wrangler d1 execute <DB_NAME> --remote --file sql/d1/012_full_cms_seed_content.sql
```

Supabase:

```bash
supabase db push
```

or paste/run the SQL files in Supabase SQL Editor.

## Fixture Safety

Use IDs prefixed with:

```txt
test_
req_test_
run_test_
ds_test_
snapshot_test_
```

Add metadata:

```json
{
  "fixture": true,
  "created_by": "leadership_legacy_sql_seed"
}
```

## Production Auth Reminder

The current dashboard password gate is concept-only. Production should use:

```txt
Cloudflare Access
Supabase Auth
Worker session cookies
Role checks
```
