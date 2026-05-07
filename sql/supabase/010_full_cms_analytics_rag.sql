-- Leadership Legacy Digital / Connor McNeely
-- Supabase Full CMS Analytics + RAG + Agent Telemetry Schema
--
-- Purpose:
-- - Long-term analytics
-- - RAG documents and semantic search logs
-- - Agent/model routing and eval telemetry
-- - Tool calls, stream events, error events
-- - Codebase snapshots
-- - Design Studio / generated asset metrics
--
-- Supabase notes:
-- - Uses pgcrypto for UUID generation.
-- - Uses vector for embeddings.
-- - RLS is enabled; policies should be configured to match your auth model.
-- - Service-role Worker writes can bypass client RLS when using server secrets.

create extension if not exists "pgcrypto";
create extension if not exists "vector";

------------------------------------------------------------
-- 00. Project / tenant mapping
------------------------------------------------------------

create table if not exists public.ll_tenants (
  id text primary key,
  slug text not null unique,
  name text not null,
  status text not null default 'active'
    check (status in ('active', 'paused', 'archived')),
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.ll_workspaces (
  id text primary key,
  tenant_id text not null references public.ll_tenants(id) on delete cascade,
  slug text not null,
  name text not null,
  site_url text,
  timezone text default 'America/Chicago',
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique (tenant_id, slug)
);

------------------------------------------------------------
-- 01. RAG / knowledge
------------------------------------------------------------

create table if not exists public.ll_documents (
  id uuid primary key default gen_random_uuid(),
  tenant_id text default 'tenant_leadership_legacy',
  workspace_id text default 'ws_leadership_legacy',
  project_id text not null default 'leadership_legacy',
  source text not null,
  source_id text,
  title text,
  content text not null,
  content_hash text,
  chunk_index integer default 0,
  embedding vector(1024),
  embed_model text default '@cf/baai/bge-large-en-v1.5',
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index if not exists idx_ll_documents_workspace_source
on public.ll_documents(workspace_id, source);

create index if not exists idx_ll_documents_created
on public.ll_documents(created_at desc);

create table if not exists public.ll_semantic_search_log (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  request_id text,
  run_group_id text,
  search_fn text not null,
  query_preview text,
  query_hash text,
  match_threshold double precision,
  match_count_requested integer,
  match_count_returned integer,
  top_similarity double precision,
  avg_similarity double precision,
  sources_hit jsonb default '[]'::jsonb,
  latency_ms integer,
  success boolean default true,
  error_message text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists public.ll_knowledge_edges (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  entity_a text not null,
  relation text not null,
  entity_b text not null,
  source_type text default 'document'
    check (source_type in ('document', 'memory', 'decision', 'manual', 'code', 'case_study')),
  source_id text,
  confidence double precision default 1.0
    check (confidence >= 0 and confidence <= 1),
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

------------------------------------------------------------
-- 02. Website analytics
------------------------------------------------------------

create table if not exists public.ll_site_sessions (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  visitor_id text,
  session_id text not null,
  first_page text,
  last_page text,
  referrer text,
  user_agent_hash text,
  ip_hash text,
  country text,
  region text,
  city text,
  started_at timestamptz default now(),
  last_seen_at timestamptz default now(),
  metadata jsonb default '{}'::jsonb,
  unique (workspace_id, session_id)
);

create table if not exists public.ll_site_events (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  visitor_id text,
  session_id text,
  event_name text not null,
  page_path text,
  page_title text,
  referrer text,
  utm_source text,
  utm_medium text,
  utm_campaign text,
  utm_content text,
  utm_term text,
  lead_id text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create index if not exists idx_ll_site_events_workspace_created
on public.ll_site_events(workspace_id, created_at desc);

create index if not exists idx_ll_site_events_name
on public.ll_site_events(workspace_id, event_name);

create table if not exists public.ll_lead_events (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  lead_id text,
  session_id text,
  event_name text not null,
  pipeline_status text,
  project_type text,
  budget_range text,
  source_page text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

------------------------------------------------------------
-- 03. AI model costs / routing / Thompson arms
------------------------------------------------------------

create table if not exists public.ll_model_cost_snapshots (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  model_key text not null,
  api_platform text,
  modality text default 'text',
  input_rate_per_mtok numeric,
  output_rate_per_mtok numeric,
  cached_input_rate_per_mtok numeric,
  batch_input_rate_per_mtok numeric,
  batch_output_rate_per_mtok numeric,
  pricing_source text,
  effective_at timestamptz default now(),
  metadata jsonb default '{}'::jsonb
);

create index if not exists idx_ll_model_costs_provider_model
on public.ll_model_cost_snapshots(provider, model_key, effective_at desc);

create table if not exists public.ll_routing_arms (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  provider text not null,
  model_key text not null,
  task_type text not null,
  mode text default 'agent',
  modality text default 'text',
  is_enabled boolean default true,
  is_blocked boolean default false,
  alpha numeric default 1,
  beta numeric default 1,
  total_runs integer default 0,
  successes integer default 0,
  failures integer default 0,
  avg_latency_ms numeric default 0,
  avg_cost_usd numeric default 0,
  avg_quality_score numeric default 0,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique (workspace_id, provider, model_key, task_type, mode)
);

create table if not exists public.ll_routing_decisions (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  conversation_id text,
  request_id text,
  run_group_id text,
  task_type text,
  mode text,
  intent text,
  requested_model text,
  resolved_requested_model text,
  selected_model text not null,
  provider text,
  api_platform text,
  routing_strategy text,
  routing_arm_id uuid references public.ll_routing_arms(id) on delete set null,
  tools_required boolean default false,
  supports_tools_required boolean default false,
  override_happened boolean default false,
  override_reason text,
  fallback_used boolean default false,
  fallback_reason text,
  estimated_input_tokens integer default 0,
  estimated_output_tokens integer default 0,
  estimated_cost_usd numeric default 0,
  actual_input_tokens integer default 0,
  actual_output_tokens integer default 0,
  actual_cost_usd numeric default 0,
  success boolean,
  human_score integer check (human_score between 1 and 5),
  latency_ms integer,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create index if not exists idx_ll_routing_decisions_request
on public.ll_routing_decisions(request_id);

create index if not exists idx_ll_routing_decisions_created
on public.ll_routing_decisions(created_at desc);

------------------------------------------------------------
-- 04. Agent stream / prompt / tool / error telemetry
------------------------------------------------------------

create table if not exists public.ll_prompt_runs (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  conversation_id text,
  request_id text,
  run_group_id text,
  prompt_profile_key text,
  agent_id text,
  mode text,
  intent text,
  system_prompt_hash text,
  system_prompt_chars integer default 0,
  context_block_chars integer default 0,
  total_prompt_chars integer default 0,
  estimated_tokens integer default 0,
  final_input_tokens integer default 0,
  included_prompts jsonb default '[]'::jsonb,
  omitted_prompts jsonb default '[]'::jsonb,
  context_sources jsonb default '[]'::jsonb,
  warnings jsonb default '[]'::jsonb,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists public.ll_stream_events (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  conversation_id text,
  request_id text,
  run_group_id text,
  source text not null default 'dashboard',
  route text default '/api/agent/chat',
  event_type text not null,
  requested_model text,
  selected_model text,
  provider text,
  api_platform text,
  mode text,
  intent text,
  prompt_chars integer default 0,
  input_tokens integer default 0,
  output_tokens integer default 0,
  total_tokens integer default 0,
  cost_usd numeric default 0,
  chunk_index integer default 0,
  chunk_count integer default 0,
  content_chunk_count integer default 0,
  reasoning_chunk_count integer default 0,
  dropped_chunk_count integer default 0,
  raw_sse_line_count integer default 0,
  duration_ms integer,
  first_token_ms integer,
  aborted boolean default false,
  abort_source text,
  success boolean,
  error_message text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create index if not exists idx_ll_stream_events_request
on public.ll_stream_events(request_id);

create table if not exists public.ll_tool_call_events (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  conversation_id text,
  request_id text,
  run_group_id text,
  agent_tool text,
  provider text,
  model_key text,
  tool_name text not null,
  tool_category text,
  tool_source text,
  call_index integer default 0,
  input_tokens integer default 0,
  output_tokens integer default 0,
  cost_usd numeric default 0,
  duration_ms integer,
  success boolean,
  error_message text,
  input_preview text,
  output_preview text,
  input_json jsonb default '{}'::jsonb,
  output_json jsonb default '{}'::jsonb,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists public.ll_error_events (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  conversation_id text,
  request_id text,
  run_group_id text,
  source text not null,
  severity text not null default 'error'
    check (severity in ('debug', 'info', 'warning', 'error', 'critical')),
  error_type text,
  error_code text,
  error_message text not null,
  stack_preview text,
  route text,
  method text,
  provider text,
  model_key text,
  api_platform text,
  tool_name text,
  table_name text,
  retryable boolean,
  resolved boolean default false,
  resolved_at timestamptz,
  resolution_notes text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

------------------------------------------------------------
-- 05. Evals
------------------------------------------------------------

create table if not exists public.ll_eval_suites (
  id uuid primary key default gen_random_uuid(),
  suite_key text not null unique,
  display_name text not null,
  description text,
  task_type text not null default 'general',
  mode text not null default 'agent',
  repo_path text,
  target_repo text,
  prompt text not null,
  acceptance_criteria jsonb default '[]'::jsonb,
  tags jsonb default '[]'::jsonb,
  created_by text default 'sam_primeaux',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.ll_eval_runs (
  id uuid primary key default gen_random_uuid(),
  suite_id uuid references public.ll_eval_suites(id) on delete set null,
  tenant_id text,
  workspace_id text,
  session_id text,
  conversation_id text,
  request_id text,
  run_group_id text,
  run_source text not null default 'manual',
  agent_tool text not null,
  provider text,
  model_key text,
  model_display_name text,
  api_platform text,
  repo_path text,
  branch_name text,
  commit_before text,
  commit_after text,
  status text not null default 'started',
  success boolean,
  failure_reason text,
  error_message text,
  input_tokens integer not null default 0,
  output_tokens integer not null default 0,
  cache_read_tokens integer not null default 0,
  cache_write_tokens integer not null default 0,
  total_tokens integer generated always as
    (input_tokens + output_tokens + cache_read_tokens + cache_write_tokens) stored,
  cost_usd numeric not null default 0,
  duration_ms integer,
  first_token_ms integer,
  tool_call_count integer not null default 0,
  files_changed_count integer not null default 0,
  lines_added integer not null default 0,
  lines_deleted integer not null default 0,
  build_passed boolean,
  tests_passed boolean,
  lint_passed boolean,
  deploy_passed boolean,
  human_score_architecture integer check (human_score_architecture between 1 and 5),
  human_score_quality integer check (human_score_quality between 1 and 5),
  human_score_speed integer check (human_score_speed between 1 and 5),
  human_score_cost integer check (human_score_cost between 1 and 5),
  human_notes text,
  prompt_preview text,
  output_preview text,
  artifacts_json jsonb default '{}'::jsonb,
  metrics_json jsonb default '{}'::jsonb,
  metadata jsonb default '{}'::jsonb,
  started_at timestamptz default now(),
  completed_at timestamptz,
  created_at timestamptz default now()
);

------------------------------------------------------------
-- 06. R2 / generated assets / design studio analytics
------------------------------------------------------------

create table if not exists public.ll_r2_object_events (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  bucket_name text not null,
  binding_name text,
  object_key text not null,
  event_name text not null,
  object_type text,
  size_bytes bigint,
  content_type text,
  etag text,
  public_url text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists public.ll_designstudio_runs (
  id text primary key default ('dsra_' || lower(replace(gen_random_uuid()::text, '-', ''))),
  workflow_run_id text not null unique,
  tenant_id text not null default 'tenant_leadership_legacy',
  workspace_id text not null default 'ws_designstudio',
  status text not null default 'running',
  success boolean default false,
  input_tokens integer not null default 0,
  output_tokens integer not null default 0,
  cost_usd numeric not null default 0,
  duration_ms integer,
  r2_prefix text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz not null default now(),
  completed_at timestamptz
);

create table if not exists public.ll_designstudio_asset_metrics (
  id text primary key default ('dsam_' || lower(replace(gen_random_uuid()::text, '-', ''))),
  workflow_run_id text not null,
  asset_type text not null,
  r2_key text not null,
  size_bytes bigint,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.ll_designstudio_step_metrics (
  id text primary key default ('dssm_' || lower(replace(gen_random_uuid()::text, '-', ''))),
  workflow_run_id text not null,
  step_key text,
  tool_name text,
  duration_ms integer,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz not null default now()
);

------------------------------------------------------------
-- 07. Codebase indexing
------------------------------------------------------------

create table if not exists public.ll_codebase_snapshots (
  id uuid primary key default gen_random_uuid(),
  snapshot_id text not null unique,
  workspace_id text not null,
  tenant_id text not null,
  commit_sha text not null,
  branch text not null default 'main',
  repo_url text,
  file_count integer not null default 0,
  total_lines integer not null default 0,
  total_bytes bigint not null default 0,
  chunk_count integer not null default 0,
  r2_prefix text,
  upload_status text not null default 'uploading'
    check (upload_status in ('uploading', 'complete', 'failed', 'stale')),
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.ll_codebase_files (
  id uuid primary key default gen_random_uuid(),
  snapshot_id text not null references public.ll_codebase_snapshots(snapshot_id) on delete cascade,
  workspace_id text not null,
  tenant_id text not null,
  file_path text not null,
  file_size_bytes integer not null default 0,
  line_count integer,
  language text,
  category text,
  is_priority boolean not null default false,
  last_modified_at timestamptz,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.ll_codebase_chunks (
  id uuid primary key default gen_random_uuid(),
  snapshot_id text not null references public.ll_codebase_snapshots(snapshot_id) on delete cascade,
  file_id uuid references public.ll_codebase_files(id) on delete cascade,
  workspace_id text not null,
  tenant_id text not null,
  file_path text not null,
  chunk_index integer not null default 0,
  chunk_type text not null default 'code'
    check (chunk_type in ('code', 'comment', 'route', 'function', 'class', 'config', 'markdown', 'other')),
  content text not null,
  embedding vector(1024),
  line_start integer,
  line_end integer,
  symbol_name text,
  language text,
  metadata jsonb default '{}'::jsonb,
  embed_model text default '@cf/baai/bge-large-en-v1.5',
  created_at timestamptz not null default now()
);

create table if not exists public.ll_codebase_symbols (
  id uuid primary key default gen_random_uuid(),
  snapshot_id text not null references public.ll_codebase_snapshots(snapshot_id) on delete cascade,
  workspace_id text not null,
  tenant_id text not null,
  file_path text not null,
  symbol_type text not null
    check (symbol_type in ('route', 'function', 'class', 'export', 'constant', 'import', 'other')),
  symbol_name text not null,
  http_method text,
  line_number integer,
  signature text,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz not null default now()
);

------------------------------------------------------------
-- 08. Views
------------------------------------------------------------

create or replace view public.v_ll_site_overview_30d as
select
  workspace_id,
  count(*) filter (where event_name = 'page_view') as page_views,
  count(*) filter (where event_name = 'cta_click') as cta_clicks,
  count(*) filter (where event_name = 'lead_submit') as lead_submits,
  count(distinct session_id) as sessions,
  min(created_at) as first_event_at,
  max(created_at) as last_event_at
from public.ll_site_events
where created_at >= now() - interval '30 days'
group by workspace_id;

create or replace view public.v_ll_page_performance_30d as
select
  workspace_id,
  page_path,
  count(*) filter (where event_name = 'page_view') as views,
  count(*) filter (where event_name = 'cta_click') as cta_clicks,
  count(*) filter (where event_name = 'lead_submit') as leads,
  max(created_at) as last_event_at
from public.ll_site_events
where created_at >= now() - interval '30 days'
group by workspace_id, page_path;

create or replace view public.v_ll_stream_run_summary as
select
  request_id,
  min(created_at) as started_at,
  max(created_at) as last_event_at,
  max(selected_model) as selected_model,
  max(requested_model) as requested_model,
  max(provider) as provider,
  max(api_platform) as api_platform,
  max(tenant_id) as tenant_id,
  max(workspace_id) as workspace_id,
  count(*) as events,
  sum(coalesce(raw_sse_line_count, 0)) as raw_sse_lines,
  sum(coalesce(reasoning_chunk_count, 0)) as reasoning_chunks,
  sum(coalesce(dropped_chunk_count, 0)) as dropped_chunks,
  bool_or(coalesce(aborted, false)) as aborted,
  bool_or(error_message is not null) as had_error,
  max(error_message) filter (where error_message is not null) as last_error,
  max(duration_ms) as duration_ms,
  max(total_tokens) as total_tokens,
  max(cost_usd) as cost_usd
from public.ll_stream_events
where request_id is not null
group by request_id;

create or replace view public.v_ll_recent_errors as
select *
from public.ll_error_events
order by created_at desc
limit 100;

------------------------------------------------------------
-- 09. RLS enablement
------------------------------------------------------------

alter table public.ll_tenants enable row level security;
alter table public.ll_workspaces enable row level security;
alter table public.ll_documents enable row level security;
alter table public.ll_semantic_search_log enable row level security;
alter table public.ll_knowledge_edges enable row level security;
alter table public.ll_site_sessions enable row level security;
alter table public.ll_site_events enable row level security;
alter table public.ll_lead_events enable row level security;
alter table public.ll_model_cost_snapshots enable row level security;
alter table public.ll_routing_arms enable row level security;
alter table public.ll_routing_decisions enable row level security;
alter table public.ll_prompt_runs enable row level security;
alter table public.ll_stream_events enable row level security;
alter table public.ll_tool_call_events enable row level security;
alter table public.ll_error_events enable row level security;
alter table public.ll_eval_suites enable row level security;
alter table public.ll_eval_runs enable row level security;
alter table public.ll_r2_object_events enable row level security;
alter table public.ll_designstudio_runs enable row level security;
alter table public.ll_designstudio_asset_metrics enable row level security;
alter table public.ll_designstudio_step_metrics enable row level security;
alter table public.ll_codebase_snapshots enable row level security;
alter table public.ll_codebase_files enable row level security;
alter table public.ll_codebase_chunks enable row level security;
alter table public.ll_codebase_symbols enable row level security;
