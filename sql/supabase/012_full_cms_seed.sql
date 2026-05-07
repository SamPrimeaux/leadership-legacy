-- Supabase seed data for Leadership Legacy.

insert into public.ll_tenants (id, slug, name, metadata)
values (
  'tenant_leadership_legacy',
  'leadership-legacy',
  'Leadership Legacy Digital',
  jsonb_build_object('founder', 'Connor McNeely')
)
on conflict (id) do nothing;

insert into public.ll_workspaces (id, tenant_id, slug, name, site_url, timezone, metadata)
values (
  'ws_leadership_legacy',
  'tenant_leadership_legacy',
  'main',
  'Leadership Legacy Main Site',
  'https://leadership-legacy.meauxbility.workers.dev',
  'America/Chicago',
  jsonb_build_object('bucket', 'leadership-legacy')
)
on conflict (id) do nothing;

insert into public.ll_model_cost_snapshots (
  provider,
  model_key,
  api_platform,
  modality,
  input_rate_per_mtok,
  output_rate_per_mtok,
  cached_input_rate_per_mtok,
  batch_input_rate_per_mtok,
  batch_output_rate_per_mtok,
  pricing_source,
  metadata
)
values
  ('openai', 'gpt-5.4-nano', 'responses', 'text', 0.20, 1.25, 0.02, 0.10, 0.625, 'manual_registry', '{}'::jsonb),
  ('openai', 'gpt-5.4-mini', 'responses', 'text', 0.75, 4.50, 0.075, 0.375, 2.25, 'manual_registry', '{}'::jsonb),
  ('openai', 'gpt-5.4', 'responses', 'text', 2.50, 15.00, 0.25, 1.25, 7.50, 'manual_registry', '{}'::jsonb),
  ('openai', 'gpt-image-1-mini', 'images', 'image', 2.00, 8.00, 0.20, 1.00, 4.00, 'manual_registry', '{}'::jsonb),
  ('openai', 'gpt-image-1.5', 'images', 'image', 5.00, 32.00, 1.25, 2.50, 16.00, 'manual_registry', '{}'::jsonb),
  ('anthropic', 'claude-sonnet', 'messages', 'text', null, null, null, null, null, 'manual_registry', '{}'::jsonb),
  ('anthropic', 'claude-haiku', 'messages', 'text', null, null, null, null, null, 'manual_registry', '{}'::jsonb);

insert into public.ll_routing_arms (
  tenant_id,
  workspace_id,
  provider,
  model_key,
  task_type,
  mode,
  modality,
  is_enabled,
  is_blocked,
  metadata
)
values
  ('tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4-nano', 'routing', 'agent', 'text', true, false, '{}'::jsonb),
  ('tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4-mini', 'cms_editing', 'agent', 'text', true, false, '{}'::jsonb),
  ('tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4', 'architecture', 'agent', 'text', true, false, '{}'::jsonb),
  ('tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-image-1-mini', 'image_generation', 'agent', 'image', true, false, '{}'::jsonb),
  ('tenant_leadership_legacy', 'ws_leadership_legacy', 'anthropic', 'claude-sonnet', 'code_review', 'agent', 'text', true, false, '{}'::jsonb)
on conflict (workspace_id, provider, model_key, task_type, mode) do nothing;

insert into public.ll_documents (
  tenant_id,
  workspace_id,
  project_id,
  source,
  title,
  content,
  metadata
)
values
  (
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'leadership_legacy',
    'seed:brand',
    'Leadership Legacy Positioning',
    'Connor McNeely is a Mechanical Engineer × AI Developer. Leadership Legacy Digital builds engineering-grade AI systems for technical businesses, including RAG systems, CAD automation, full-stack AI apps, and workflow automation.',
    jsonb_build_object('fixture', true, 'seed', 'brand')
  ),
  (
    'tenant_leadership_legacy',
    'ws_leadership_legacy',
    'leadership_legacy',
    'seed:cms',
    'CMS Runtime',
    'The Leadership Legacy CMS uses Cloudflare D1 for runtime content, pages, sections, media registry, leads, and publishing state. Supabase stores analytics, RAG, evals, routing decisions, and codebase indexing.',
    jsonb_build_object('fixture', true, 'seed', 'cms')
  );
