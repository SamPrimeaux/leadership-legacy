# Agent Sam Workspace Registration

Connor's Leadership Legacy workspace is registered in the InnerAnimalMedia D1 database as:

```txt
ws_connor_mcneely
```

## Verified Remote D1 State

Verified in `inneranimalmedia-business`:

```txt
agentsam_workspace.id = ws_connor_mcneely
workspaces.id = ws_connor_mcneely
github_repo = SamPrimeaux/leadership-legacy
r2_bucket = leadership-legacy
r2_prefix = leadership-legacy/
default_model_id = gpt-5.4-mini
```

`agentsam_scripts` has Connor-specific scripts registered for:

```txt
audit
build
deploy
dev
maintenance
test
```

Production-mutating scripts such as deploy, R2 publish, R2 prune, and secret mutation are registered with:

```txt
safe_to_run = 0
owner_only = 1
```

Read-only/build/test scripts are registered with:

```txt
safe_to_run = 1
```

## SQL Artifact

The repo stores a mirror SQL artifact at:

```txt
sql/agentsam/register_connor_workspace_scripts.sql
```

This file is for documentation/replay. It intentionally does not use:

```txt
BEGIN TRANSACTION
COMMIT
SAVEPOINT
```

because Wrangler/D1 remote execution rejects explicit transaction statements.

## Apply Command

Apply from the correct D1 control context:

```bash
npx wrangler d1 execute inneranimalmedia-business --remote --file sql/agentsam/register_connor_workspace_scripts.sql
```

## Verify Commands

```bash
npx wrangler d1 execute inneranimalmedia-business --remote --command "SELECT id, workspace_slug, name, r2_bucket, r2_prefix, github_repo, default_model_id FROM agentsam_workspace WHERE id='ws_connor_mcneely';"

npx wrangler d1 execute inneranimalmedia-business --remote --command "SELECT id, name, domain, category, status, github_repo, r2_prefix, default_model_id FROM workspaces WHERE id='ws_connor_mcneely';"

npx wrangler d1 execute inneranimalmedia-business --remote --command "SELECT id,name,path,purpose,runner,safe_to_run,owner_only FROM agentsam_scripts WHERE workspace_id='ws_connor_mcneely' ORDER BY purpose,name;"
```
