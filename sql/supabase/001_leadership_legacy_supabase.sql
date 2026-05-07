create extension if not exists "pgcrypto";
create extension if not exists "vector";

create table if not exists public.ll_documents (
  id uuid primary key default gen_random_uuid(),
  project_id text not null default 'leadership_legacy',
  workspace_id text not null default 'ws_leadership_legacy',
  source text not null,
  title text,
  content text not null,
  embedding vector(1024),
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.ll_agentsam_routing_decisions (
  id uuid primary key default gen_random_uuid(),
  tenant_id text,
  workspace_id text,
  session_id text,
  request_id text,
  run_group_id text,
  task_type text,
  mode text,
  intent text,
  requested_model text,
  selected_model text not null,
  provider text,
  routing_strategy text,
  estimated_cost_usd numeric default 0,
  success boolean,
  latency_ms integer,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);
