-- Supabase functions for Leadership Legacy analytics/RAG/telemetry.

create or replace function public.ll_touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_ll_tenants_updated_at on public.ll_tenants;
create trigger trg_ll_tenants_updated_at
before update on public.ll_tenants
for each row execute function public.ll_touch_updated_at();

drop trigger if exists trg_ll_workspaces_updated_at on public.ll_workspaces;
create trigger trg_ll_workspaces_updated_at
before update on public.ll_workspaces
for each row execute function public.ll_touch_updated_at();

drop trigger if exists trg_ll_documents_updated_at on public.ll_documents;
create trigger trg_ll_documents_updated_at
before update on public.ll_documents
for each row execute function public.ll_touch_updated_at();

drop trigger if exists trg_ll_routing_arms_updated_at on public.ll_routing_arms;
create trigger trg_ll_routing_arms_updated_at
before update on public.ll_routing_arms
for each row execute function public.ll_touch_updated_at();

create or replace function public.ll_log_site_event(
  p_workspace_id text,
  p_event_name text,
  p_page_path text default null,
  p_session_id text default null,
  p_visitor_id text default null,
  p_metadata jsonb default '{}'::jsonb
)
returns uuid
language plpgsql
security definer
as $$
declare
  v_id uuid;
begin
  insert into public.ll_site_events (
    workspace_id,
    event_name,
    page_path,
    session_id,
    visitor_id,
    metadata
  )
  values (
    p_workspace_id,
    p_event_name,
    p_page_path,
    p_session_id,
    p_visitor_id,
    coalesce(p_metadata, '{}'::jsonb)
  )
  returning id into v_id;

  return v_id;
end;
$$;

create or replace function public.ll_update_routing_arm(
  p_arm_id uuid,
  p_success boolean,
  p_latency_ms numeric default null,
  p_cost_usd numeric default null,
  p_quality_score numeric default null
)
returns void
language plpgsql
security definer
as $$
begin
  update public.ll_routing_arms
  set
    total_runs = total_runs + 1,
    successes = successes + case when p_success then 1 else 0 end,
    failures = failures + case when p_success then 0 else 1 end,
    alpha = alpha + case when p_success then 1 else 0 end,
    beta = beta + case when p_success then 0 else 1 end,
    avg_latency_ms = case
      when p_latency_ms is null then avg_latency_ms
      when total_runs = 0 then p_latency_ms
      else ((avg_latency_ms * total_runs) + p_latency_ms) / (total_runs + 1)
    end,
    avg_cost_usd = case
      when p_cost_usd is null then avg_cost_usd
      when total_runs = 0 then p_cost_usd
      else ((avg_cost_usd * total_runs) + p_cost_usd) / (total_runs + 1)
    end,
    avg_quality_score = case
      when p_quality_score is null then avg_quality_score
      when total_runs = 0 then p_quality_score
      else ((avg_quality_score * total_runs) + p_quality_score) / (total_runs + 1)
    end,
    updated_at = now()
  where id = p_arm_id;
end;
$$;

create or replace function public.ll_match_documents(
  query_embedding vector(1024),
  match_threshold float default 0.72,
  match_count int default 8,
  p_workspace_id text default 'ws_leadership_legacy'
)
returns table (
  id uuid,
  title text,
  content text,
  source text,
  metadata jsonb,
  similarity float
)
language sql
stable
as $$
  select
    d.id,
    d.title,
    d.content,
    d.source,
    d.metadata,
    1 - (d.embedding <=> query_embedding) as similarity
  from public.ll_documents d
  where d.workspace_id = p_workspace_id
    and d.embedding is not null
    and 1 - (d.embedding <=> query_embedding) > match_threshold
  order by d.embedding <=> query_embedding
  limit match_count;
$$;
