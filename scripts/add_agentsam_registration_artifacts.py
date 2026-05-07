#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()

def run(cmd, check=False):
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result

def write(path, content):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"wrote {path}")

def main():
    write("sql/agentsam/register_connor_workspace_scripts.sql", r'''
    -- Agent Sam registration artifacts for Connor McNeely / Leadership Legacy Digital
    -- Workspace id: ws_connor_mcneely
    --
    -- NOTE:
    -- This SQL intentionally does not use BEGIN TRANSACTION or COMMIT because
    -- Wrangler/D1 remote execution rejects explicit transaction statements.
    --
    -- Apply from the InnerAnimalMedia D1 control repo/context:
    --
    -- npx wrangler d1 execute inneranimalmedia-business --remote --file sql/agentsam/register_connor_workspace_scripts.sql

    INSERT INTO agentsam_workspace (
      id,
      workspace_slug,
      tenant_id,
      project_id,
      project_slug,
      name,
      description,
      root_path,
      r2_bucket,
      status,
      metadata_json,
      r2_prefix,
      github_repo,
      default_model_id,
      primary_subagent_id,
      display_name,
      updated_at
    ) VALUES (
      'ws_connor_mcneely',
      'connor-mcneely',
      'tenant_connor_mcneely',
      'project_leadership_legacy',
      'leadership-legacy',
      'Connor McNeely / Leadership Legacy',
      'Client workspace for Connor McNeely and Leadership Legacy Digital: public site, dashboard, R2 assets, OpenAI Agent Connor, Playwright, GitHub/Google/Resend/Supabase integration roadmap.',
      '~/Downloads/leadership-legacy',
      'leadership-legacy',
      'active',
      '{"client":"Connor McNeely","brand":"Leadership Legacy Digital","live_url":"https://leadership-legacy.meauxbility.workers.dev","stack":["Cloudflare Workers","R2","Vite","React","Monaco","xterm","OpenAI","Playwright"]}',
      'leadership-legacy/',
      'SamPrimeaux/leadership-legacy',
      'gpt-5.4-mini',
      'agentsam_connor',
      'Connor McNeely',
      unixepoch()
    )
    ON CONFLICT(id) DO UPDATE SET
      workspace_slug = excluded.workspace_slug,
      tenant_id = excluded.tenant_id,
      project_id = excluded.project_id,
      project_slug = excluded.project_slug,
      name = excluded.name,
      description = excluded.description,
      root_path = excluded.root_path,
      r2_bucket = excluded.r2_bucket,
      status = excluded.status,
      metadata_json = excluded.metadata_json,
      r2_prefix = excluded.r2_prefix,
      github_repo = excluded.github_repo,
      default_model_id = excluded.default_model_id,
      primary_subagent_id = excluded.primary_subagent_id,
      display_name = excluded.display_name,
      updated_at = unixepoch();

    INSERT INTO workspaces (
      id,
      name,
      domain,
      category,
      status,
      cloudflare_plan,
      dns_records_count,
      workers_pages_count,
      logo_url,
      theme_set,
      created_at,
      handle,
      is_system,
      is_archived,
      owner_tenant_id,
      default_tenant_id,
      updated_at,
      theme_id,
      app_id,
      project_id,
      workspace_id,
      worker_id,
      brand,
      theme,
      user_id,
      tenant_id,
      display_name,
      slug,
      workspace_type,
      r2_prefix,
      github_repo,
      primary_subagent_id,
      default_model_id,
      settings_json,
      description,
      state_json
    ) VALUES (
      'ws_connor_mcneely',
      'Connor McNeely / Leadership Legacy',
      'leadership-legacy.meauxbility.workers.dev',
      'client',
      'active',
      'workers',
      0,
      1,
      NULL,
      'leadership-legacy-dark',
      strftime('%Y-%m-%dT%H:%M:%fZ','now'),
      'connor-mcneely',
      0,
      0,
      'tenant_connor_mcneely',
      'tenant_connor_mcneely',
      strftime('%Y-%m-%dT%H:%M:%fZ','now'),
      'theme_leadership_legacy_dark',
      'app_leadership_legacy',
      'project_leadership_legacy',
      'ws_connor_mcneely',
      'worker_leadership_legacy',
      'Leadership Legacy Digital',
      'dark-premium-engineering',
      'user_connor_mcneely',
      'tenant_connor_mcneely',
      'Connor McNeely',
      'connor-mcneely',
      'project',
      'leadership-legacy/',
      'SamPrimeaux/leadership-legacy',
      'agentsam_connor',
      'gpt-5.4-mini',
      '{"autodeploy":true,"r2_keep_deployments":3,"live_worker_url":"https://leadership-legacy.meauxbility.workers.dev","requires_owner_approval_for_deploy":true,"blocked_models":["gpt-5.5","gpt-5.5-pro","gpt-5.4-pro"]}',
      'Client workspace for Connor McNeely and Leadership Legacy Digital.',
      '{"openai":"configured","r2":"configured","worker":"deployed","anthropic":"pending","gemini":"pending","github":"prepared","google_drive":"prepared","gmail":"prepared","resend":"prepared","supabase":"planned","d1":"planned","mcp":"planned"}'
    )
    ON CONFLICT(id) DO UPDATE SET
      name = excluded.name,
      domain = excluded.domain,
      category = excluded.category,
      status = excluded.status,
      cloudflare_plan = excluded.cloudflare_plan,
      workers_pages_count = excluded.workers_pages_count,
      theme_set = excluded.theme_set,
      handle = excluded.handle,
      is_archived = excluded.is_archived,
      owner_tenant_id = excluded.owner_tenant_id,
      default_tenant_id = excluded.default_tenant_id,
      updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now'),
      theme_id = excluded.theme_id,
      app_id = excluded.app_id,
      project_id = excluded.project_id,
      workspace_id = excluded.workspace_id,
      worker_id = excluded.worker_id,
      brand = excluded.brand,
      theme = excluded.theme,
      user_id = excluded.user_id,
      tenant_id = excluded.tenant_id,
      display_name = excluded.display_name,
      slug = excluded.slug,
      workspace_type = excluded.workspace_type,
      r2_prefix = excluded.r2_prefix,
      github_repo = excluded.github_repo,
      primary_subagent_id = excluded.primary_subagent_id,
      default_model_id = excluded.default_model_id,
      settings_json = excluded.settings_json,
      description = excluded.description,
      state_json = excluded.state_json;

    -- Minimal script registry mirror.
    -- Full source of truth has already been applied to inneranimalmedia-business.
    -- This keeps Connor's repo self-documenting.

    INSERT INTO agentsam_scripts (
      id, workspace_id, name, path, description, purpose, runner,
      requires_env, owner_only, safe_to_run, preferred_for, notes, is_active, updated_at
    ) VALUES
    ('script_connor_build','ws_connor_mcneely','Build production app','npm run build','Build the production Vite assets for the public website and dashboard.','build','npm',0,1,1,'Pre-deploy validation and CI build checks.','Writes dist/. dist/ should remain gitignored.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_test_e2e','ws_connor_mcneely','Run live Playwright smoke tests','npm run test:e2e','Run Playwright smoke tests against the live Worker routes by default.','test','npm',0,1,1,'Validating public routes, dashboard routes, APIs, OpenAI diagnostics, R2 listing, and GitHub status.','Defaults to the deployed Worker unless PLAYWRIGHT_BASE_URL or LOCAL_E2E=1 is set.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_deploy_worker','ws_connor_mcneely','Deploy Worker','npm run deploy','Build and deploy the Leadership Legacy Worker to Cloudflare.','deploy','npm',1,1,0,'Manual production deploy after validation.','Mutates production Worker. Owner approval required.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_deploy_full','ws_connor_mcneely','Full build, R2 publish, prune, and Worker deploy','npm run deploy:full','Run the full release flow: build, publish dist to R2, prune old R2 deployments, and deploy Worker.','deploy','npm',1,1,0,'Owner-approved production release.','Mutates production Worker and R2. Requires explicit approval.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_r2_publish','ws_connor_mcneely','Publish dist to R2','npm run r2:publish','Upload dist/ assets to R2 under live/ and deployments/<git-sha>/.','deploy','npm',1,1,0,'Publishing fresh static assets to R2 for snapshots and live asset storage.','Writes R2 objects. Requires Cloudflare credentials and R2 bucket access.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_r2_prune','ws_connor_mcneely','Prune old R2 deployments','npm run r2:prune','Delete old R2 deployment snapshots under deployments/<old-sha>/ while preserving live/, cms/, assets/, docs/, and analytics/.','maintenance','npm',1,1,0,'Preventing R2 deployment snapshot bloat.','Deletes old deployment objects only. Uses Worker /api/r2/list because Wrangler v4.88 lacks r2 object list.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_health_check','ws_connor_mcneely','Run Worker health check','curl -s https://leadership-legacy.meauxbility.workers.dev/api/health','Check Worker health, OpenAI configured flag, and R2 binding status.','audit','bash',0,1,1,'Post-deploy smoke check.','Read-only.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_openai_test','ws_connor_mcneely','Run OpenAI live test','curl -s https://leadership-legacy.meauxbility.workers.dev/api/openai/test','Run a live Worker-routed OpenAI test and expect text ok.','test','bash',0,1,1,'Verifying OpenAI endpoint after secret changes or deploys.','Costs a tiny number of OpenAI tokens.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_r2_list','ws_connor_mcneely','List R2 objects through Worker','curl -s https://leadership-legacy.meauxbility.workers.dev/api/r2/list?prefix=','List R2 objects through the Worker R2 binding.','audit','bash',0,1,1,'Verifying R2 binding and object browser support.','Read-only.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    ('script_connor_readme_review','ws_connor_mcneely','Review repo README','README.md','Primary repo front door explaining the product, stack, setup, routes, tests, R2 flow, and integration roadmap.','audit','bash',0,0,1,'Repo orientation.','Documentation entry.',1,strftime('%Y-%m-%dT%H:%M:%fZ','now'))
    ON CONFLICT(id) DO UPDATE SET
      workspace_id = excluded.workspace_id,
      name = excluded.name,
      path = excluded.path,
      description = excluded.description,
      purpose = excluded.purpose,
      runner = excluded.runner,
      requires_env = excluded.requires_env,
      owner_only = excluded.owner_only,
      safe_to_run = excluded.safe_to_run,
      preferred_for = excluded.preferred_for,
      notes = excluded.notes,
      is_active = 1,
      updated_at = strftime('%Y-%m-%dT%H:%M:%fZ','now');

    -- Verification:
    -- SELECT id, workspace_slug, name, r2_bucket, r2_prefix, github_repo, default_model_id FROM agentsam_workspace WHERE id='ws_connor_mcneely';
    -- SELECT id, name, domain, category, status, github_repo, r2_prefix, default_model_id FROM workspaces WHERE id='ws_connor_mcneely';
    -- SELECT id,name,path,purpose,runner,safe_to_run,owner_only FROM agentsam_scripts WHERE workspace_id='ws_connor_mcneely' ORDER BY purpose,name;
    ''')

    write("docs/AGENTSAM_WORKSPACE_REGISTRATION.md", r'''
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
    ''')

    run(["git", "add", "sql/agentsam/register_connor_workspace_scripts.sql", "docs/AGENTSAM_WORKSPACE_REGISTRATION.md", "scripts/add_agentsam_registration_artifacts.py"], check=False)
    run(["git", "commit", "-m", "docs: add Agent Sam workspace registration artifacts"], check=False)

    print("\nDone.")
    print("Now push Connor repo:")
    print("git push origin main")

if __name__ == "__main__":
    main()
