-- Leadership Legacy Digital / Connor McNeely
-- Cloudflare D1 Full CMS Runtime Schema
--
-- Purpose:
-- - Public site CMS runtime
-- - /dashboard live editing
-- - Draft/publish/version workflow
-- - Navigation, menus, SEO, redirects
-- - Services, case studies, resources, forms, leads
-- - R2 asset registry
-- - AI provider/model routing metadata
-- - Lightweight analytics/event logging
--
-- D1 notes:
-- - JSON is stored as TEXT.
-- - Use json_valid(...) checks where practical.
-- - Keep operational analytics light in D1.
-- - Supabase should hold heavier analytics, RAG, evals, and code indexing.

PRAGMA foreign_keys = ON;

------------------------------------------------------------
-- 00. System / schema metadata
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_schema_migrations (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  applied_at TEXT NOT NULL DEFAULT (datetime('now')),
  checksum TEXT,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_runtime_settings (
  id TEXT PRIMARY KEY,
  setting_key TEXT NOT NULL UNIQUE,
  setting_value TEXT,
  setting_json TEXT NOT NULL DEFAULT '{}',
  description TEXT,
  is_public INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  CHECK (json_valid(setting_json))
);

------------------------------------------------------------
-- 01. Tenancy / workspace
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_tenants (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'paused', 'archived')),
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_workspaces (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  slug TEXT NOT NULL,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'paused', 'archived')),
  default_locale TEXT NOT NULL DEFAULT 'en',
  timezone TEXT NOT NULL DEFAULT 'America/Chicago',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  UNIQUE (tenant_id, slug),
  CHECK (json_valid(metadata_json))
);

CREATE INDEX IF NOT EXISTS idx_cms_workspaces_tenant
ON cms_workspaces(tenant_id);

CREATE TABLE IF NOT EXISTS cms_users (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  email TEXT NOT NULL,
  display_name TEXT,
  role TEXT NOT NULL DEFAULT 'editor'
    CHECK (role IN ('owner', 'admin', 'editor', 'viewer')),
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'invited', 'disabled')),
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  UNIQUE (tenant_id, email),
  CHECK (json_valid(metadata_json))
);

------------------------------------------------------------
-- 02. Brand / theme / design tokens
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_brand_settings (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  brand_name TEXT NOT NULL,
  founder_name TEXT,
  company_name TEXT,
  tagline TEXT,
  logo_url TEXT,
  mark_url TEXT,
  wordmark_url TEXT,
  favicon_url TEXT,
  og_default_image_url TEXT,
  tokens_json TEXT NOT NULL DEFAULT '{}',
  typography_json TEXT NOT NULL DEFAULT '{}',
  social_links_json TEXT NOT NULL DEFAULT '{}',
  contact_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  CHECK (json_valid(tokens_json)),
  CHECK (json_valid(typography_json)),
  CHECK (json_valid(social_links_json)),
  CHECK (json_valid(contact_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_themes (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  mode TEXT NOT NULL DEFAULT 'auto'
    CHECK (mode IN ('light', 'dark', 'auto')),
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'draft', 'archived')),
  tokens_json TEXT NOT NULL DEFAULT '{}',
  css_vars_json TEXT NOT NULL DEFAULT '{}',
  brand_json TEXT NOT NULL DEFAULT '{}',
  compiled_css TEXT,
  compiled_css_hash TEXT,
  r2_key TEXT,
  public_url TEXT,
  preview_image_url TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, slug),
  CHECK (json_valid(tokens_json)),
  CHECK (json_valid(css_vars_json)),
  CHECK (json_valid(brand_json))
);

------------------------------------------------------------
-- 03. Navigation / menus
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_navigation_menus (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  menu_key TEXT NOT NULL,
  name TEXT NOT NULL,
  location TEXT NOT NULL DEFAULT 'primary',
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'draft', 'archived')),
  items_json TEXT NOT NULL DEFAULT '[]',
  r2_key TEXT,
  public_url TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, menu_key),
  CHECK (json_valid(items_json))
);

------------------------------------------------------------
-- 04. Pages / sections / components
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_templates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  template_key TEXT NOT NULL,
  name TEXT NOT NULL,
  template_type TEXT NOT NULL DEFAULT 'page'
    CHECK (template_type IN ('page', 'post', 'service', 'case_study', 'resource', 'legal', 'system')),
  schema_json TEXT NOT NULL DEFAULT '{}',
  default_sections_json TEXT NOT NULL DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'draft', 'archived')),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, template_key),
  CHECK (json_valid(schema_json)),
  CHECK (json_valid(default_sections_json))
);

CREATE TABLE IF NOT EXISTS cms_pages (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  title TEXT NOT NULL,
  slug TEXT NOT NULL,
  route_path TEXT NOT NULL,
  page_type TEXT NOT NULL DEFAULT 'page'
    CHECK (page_type IN ('page', 'landing', 'service', 'case_study', 'resource', 'legal', 'system')),
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'review', 'published', 'archived')),
  visibility TEXT NOT NULL DEFAULT 'public'
    CHECK (visibility IN ('public', 'private', 'unlisted')),
  template_id TEXT,
  theme_id TEXT,
  is_homepage INTEGER NOT NULL DEFAULT 0,
  is_system_page INTEGER NOT NULL DEFAULT 0,
  seo_json TEXT NOT NULL DEFAULT '{}',
  open_graph_json TEXT NOT NULL DEFAULT '{}',
  draft_json TEXT NOT NULL DEFAULT '{}',
  published_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  r2_draft_key TEXT,
  r2_published_key TEXT,
  public_url TEXT,
  created_by TEXT,
  updated_by TEXT,
  published_by TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  published_at TEXT,
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (template_id) REFERENCES cms_templates(id) ON DELETE SET NULL,
  FOREIGN KEY (theme_id) REFERENCES cms_themes(id) ON DELETE SET NULL,
  UNIQUE (workspace_id, route_path),
  CHECK (json_valid(seo_json)),
  CHECK (json_valid(open_graph_json)),
  CHECK (json_valid(draft_json)),
  CHECK (json_valid(published_json)),
  CHECK (json_valid(metadata_json))
);

CREATE INDEX IF NOT EXISTS idx_cms_pages_workspace_status
ON cms_pages(workspace_id, status);

CREATE INDEX IF NOT EXISTS idx_cms_pages_route
ON cms_pages(workspace_id, route_path);

CREATE TABLE IF NOT EXISTS cms_page_sections (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page_id TEXT NOT NULL,
  section_type TEXT NOT NULL,
  section_key TEXT NOT NULL,
  name TEXT,
  order_index INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'hidden', 'archived')),
  props_json TEXT NOT NULL DEFAULT '{}',
  style_json TEXT NOT NULL DEFAULT '{}',
  responsive_json TEXT NOT NULL DEFAULT '{}',
  animation_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (page_id) REFERENCES cms_pages(id) ON DELETE CASCADE,
  UNIQUE (page_id, section_key),
  CHECK (json_valid(props_json)),
  CHECK (json_valid(style_json)),
  CHECK (json_valid(responsive_json)),
  CHECK (json_valid(animation_json)),
  CHECK (json_valid(metadata_json))
);

CREATE INDEX IF NOT EXISTS idx_cms_page_sections_order
ON cms_page_sections(page_id, order_index);

CREATE TABLE IF NOT EXISTS cms_section_components (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  section_id TEXT NOT NULL,
  component_type TEXT NOT NULL,
  component_key TEXT NOT NULL,
  order_index INTEGER NOT NULL DEFAULT 0,
  props_json TEXT NOT NULL DEFAULT '{}',
  style_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (section_id) REFERENCES cms_page_sections(id) ON DELETE CASCADE,
  UNIQUE (section_id, component_key),
  CHECK (json_valid(props_json)),
  CHECK (json_valid(style_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_page_versions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page_id TEXT NOT NULL,
  version_number INTEGER NOT NULL,
  version_label TEXT,
  snapshot_json TEXT NOT NULL,
  snapshot_hash TEXT,
  r2_snapshot_key TEXT,
  created_by TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (page_id) REFERENCES cms_pages(id) ON DELETE CASCADE,
  UNIQUE (page_id, version_number),
  CHECK (json_valid(snapshot_json))
);

------------------------------------------------------------
-- 05. Media / R2 object registry
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_r2_buckets (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  binding_name TEXT NOT NULL,
  bucket_name TEXT NOT NULL,
  public_dev_url TEXT,
  custom_domain_url TEXT,
  s3_endpoint TEXT,
  catalog_uri TEXT,
  warehouse_name TEXT,
  location TEXT,
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'disabled', 'archived')),
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, binding_name),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_assets (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  bucket_id TEXT,
  asset_key TEXT NOT NULL,
  object_key TEXT,
  url TEXT,
  filename TEXT NOT NULL,
  original_filename TEXT,
  mime_type TEXT,
  asset_type TEXT NOT NULL DEFAULT 'image'
    CHECK (asset_type IN ('image', 'svg', 'video', 'model', 'pdf', 'download', 'texture', 'audio', 'json', 'code', 'other')),
  size_bytes INTEGER,
  width INTEGER,
  height INTEGER,
  duration_seconds REAL,
  alt_text TEXT,
  caption TEXT,
  usage_context TEXT,
  tags_json TEXT NOT NULL DEFAULT '[]',
  variants_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'ready'
    CHECK (status IN ('uploading', 'ready', 'processing', 'needs_optimization', 'archived', 'failed')),
  created_by TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (bucket_id) REFERENCES cms_r2_buckets(id) ON DELETE SET NULL,
  UNIQUE (workspace_id, asset_key),
  CHECK (json_valid(tags_json)),
  CHECK (json_valid(variants_json)),
  CHECK (json_valid(metadata_json))
);

CREATE INDEX IF NOT EXISTS idx_cms_assets_workspace_type
ON cms_assets(workspace_id, asset_type);

CREATE INDEX IF NOT EXISTS idx_cms_assets_usage
ON cms_assets(workspace_id, usage_context);

------------------------------------------------------------
-- 06. Business content: services, case studies, resources
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_services (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page_id TEXT,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  eyebrow TEXT,
  summary TEXT NOT NULL,
  body_json TEXT NOT NULL DEFAULT '{}',
  starting_at TEXT,
  pricing_json TEXT NOT NULL DEFAULT '{}',
  deliverables_json TEXT NOT NULL DEFAULT '[]',
  use_cases_json TEXT NOT NULL DEFAULT '[]',
  stack_json TEXT NOT NULL DEFAULT '[]',
  cta_json TEXT NOT NULL DEFAULT '{}',
  seo_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'review', 'published', 'archived')),
  order_index INTEGER NOT NULL DEFAULT 0,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (page_id) REFERENCES cms_pages(id) ON DELETE SET NULL,
  UNIQUE (workspace_id, slug),
  CHECK (json_valid(body_json)),
  CHECK (json_valid(pricing_json)),
  CHECK (json_valid(deliverables_json)),
  CHECK (json_valid(use_cases_json)),
  CHECK (json_valid(stack_json)),
  CHECK (json_valid(cta_json)),
  CHECK (json_valid(seo_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_case_studies (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page_id TEXT,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  category TEXT,
  client_name TEXT,
  summary TEXT NOT NULL,
  problem TEXT,
  solution TEXT,
  outcome TEXT,
  body_json TEXT NOT NULL DEFAULT '{}',
  stack_json TEXT NOT NULL DEFAULT '[]',
  metrics_json TEXT NOT NULL DEFAULT '{}',
  gallery_json TEXT NOT NULL DEFAULT '[]',
  testimonial_json TEXT NOT NULL DEFAULT '{}',
  seo_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'review', 'published', 'archived')),
  featured INTEGER NOT NULL DEFAULT 0,
  order_index INTEGER NOT NULL DEFAULT 0,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (page_id) REFERENCES cms_pages(id) ON DELETE SET NULL,
  UNIQUE (workspace_id, slug),
  CHECK (json_valid(body_json)),
  CHECK (json_valid(stack_json)),
  CHECK (json_valid(metrics_json)),
  CHECK (json_valid(gallery_json)),
  CHECK (json_valid(testimonial_json)),
  CHECK (json_valid(seo_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_resources (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page_id TEXT,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  resource_type TEXT NOT NULL DEFAULT 'article'
    CHECK (resource_type IN ('article', 'checklist', 'playbook', 'download', 'guide', 'tool')),
  summary TEXT,
  body_json TEXT NOT NULL DEFAULT '{}',
  download_asset_id TEXT,
  seo_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'review', 'published', 'archived')),
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (page_id) REFERENCES cms_pages(id) ON DELETE SET NULL,
  FOREIGN KEY (download_asset_id) REFERENCES cms_assets(id) ON DELETE SET NULL,
  UNIQUE (workspace_id, slug),
  CHECK (json_valid(body_json)),
  CHECK (json_valid(seo_json)),
  CHECK (json_valid(metadata_json))
);

------------------------------------------------------------
-- 07. Forms / leads / CRM
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_forms (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  form_key TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  fields_json TEXT NOT NULL DEFAULT '[]',
  success_message TEXT,
  notification_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'draft', 'archived')),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, form_key),
  CHECK (json_valid(fields_json)),
  CHECK (json_valid(notification_json))
);

CREATE TABLE IF NOT EXISTS cms_form_submissions (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  form_id TEXT,
  form_key TEXT,
  source_page TEXT,
  visitor_id TEXT,
  session_id TEXT,
  payload_json TEXT NOT NULL DEFAULT '{}',
  ip_hash TEXT,
  user_agent_hash TEXT,
  spam_score REAL,
  status TEXT NOT NULL DEFAULT 'new'
    CHECK (status IN ('new', 'reviewed', 'spam', 'archived')),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (form_id) REFERENCES cms_forms(id) ON DELETE SET NULL,
  CHECK (json_valid(payload_json))
);

CREATE TABLE IF NOT EXISTS cms_leads (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  submission_id TEXT,
  name TEXT,
  email TEXT,
  company TEXT,
  phone TEXT,
  project_type TEXT,
  budget_range TEXT,
  timeline TEXT,
  message TEXT,
  source_page TEXT,
  status TEXT NOT NULL DEFAULT 'new'
    CHECK (status IN ('new', 'qualified', 'proposal', 'won', 'lost', 'spam', 'archived')),
  priority TEXT NOT NULL DEFAULT 'normal'
    CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
  owner_user_id TEXT,
  notes TEXT,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (submission_id) REFERENCES cms_form_submissions(id) ON DELETE SET NULL,
  FOREIGN KEY (owner_user_id) REFERENCES cms_users(id) ON DELETE SET NULL,
  CHECK (json_valid(metadata_json))
);

CREATE INDEX IF NOT EXISTS idx_cms_leads_workspace_status
ON cms_leads(workspace_id, status);

CREATE INDEX IF NOT EXISTS idx_cms_leads_created_at
ON cms_leads(created_at);

------------------------------------------------------------
-- 08. SEO / redirects / route aliases
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_redirects (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  from_path TEXT NOT NULL,
  to_path TEXT NOT NULL,
  status_code INTEGER NOT NULL DEFAULT 301
    CHECK (status_code IN (301, 302, 307, 308)),
  is_active INTEGER NOT NULL DEFAULT 1,
  hit_count INTEGER NOT NULL DEFAULT 0,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, from_path),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_seo_audits (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  page_id TEXT,
  route_path TEXT,
  score INTEGER CHECK (score BETWEEN 0 AND 100),
  issues_json TEXT NOT NULL DEFAULT '[]',
  recommendations_json TEXT NOT NULL DEFAULT '[]',
  audited_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (page_id) REFERENCES cms_pages(id) ON DELETE CASCADE,
  CHECK (json_valid(issues_json)),
  CHECK (json_valid(recommendations_json))
);

------------------------------------------------------------
-- 09. Publishing jobs / deployment audit
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_publish_jobs (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  job_type TEXT NOT NULL DEFAULT 'page'
    CHECK (job_type IN ('page', 'site', 'assets', 'theme', 'navigation')),
  status TEXT NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued', 'running', 'success', 'failed', 'cancelled')),
  target_id TEXT,
  requested_by TEXT,
  started_at TEXT,
  completed_at TEXT,
  error_message TEXT,
  result_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  CHECK (json_valid(result_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_activity_log (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  actor_user_id TEXT,
  action TEXT NOT NULL,
  entity_type TEXT,
  entity_id TEXT,
  route_path TEXT,
  before_json TEXT,
  after_json TEXT,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (actor_user_id) REFERENCES cms_users(id) ON DELETE SET NULL,
  CHECK (before_json IS NULL OR json_valid(before_json)),
  CHECK (after_json IS NULL OR json_valid(after_json)),
  CHECK (json_valid(metadata_json))
);

------------------------------------------------------------
-- 10. Lightweight analytics
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_analytics_events (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  event_name TEXT NOT NULL,
  page_path TEXT,
  visitor_id TEXT,
  session_id TEXT,
  lead_id TEXT,
  referrer TEXT,
  utm_json TEXT NOT NULL DEFAULT '{}',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  FOREIGN KEY (lead_id) REFERENCES cms_leads(id) ON DELETE SET NULL,
  CHECK (json_valid(utm_json)),
  CHECK (json_valid(metadata_json))
);

CREATE INDEX IF NOT EXISTS idx_cms_analytics_workspace_created
ON cms_analytics_events(workspace_id, created_at);

CREATE INDEX IF NOT EXISTS idx_cms_analytics_event
ON cms_analytics_events(workspace_id, event_name);

------------------------------------------------------------
-- 11. AI provider / model routing metadata
------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cms_ai_providers (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  provider_key TEXT NOT NULL,
  display_name TEXT NOT NULL,
  secret_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'needs_secret'
    CHECK (status IN ('active', 'needs_secret', 'disabled', 'archived')),
  use_cases_json TEXT NOT NULL DEFAULT '[]',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, provider_key),
  CHECK (json_valid(use_cases_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_ai_models (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  provider_key TEXT NOT NULL,
  model_key TEXT NOT NULL,
  display_name TEXT NOT NULL,
  lane TEXT NOT NULL,
  runtime TEXT NOT NULL DEFAULT 'responses',
  modality TEXT NOT NULL DEFAULT 'text'
    CHECK (modality IN ('text', 'image', 'audio', 'embedding', 'multimodal')),
  is_enabled INTEGER NOT NULL DEFAULT 1,
  is_blocked INTEGER NOT NULL DEFAULT 0,
  input_price_per_mtok REAL,
  output_price_per_mtok REAL,
  cached_input_price_per_mtok REAL,
  batch_input_price_per_mtok REAL,
  batch_output_price_per_mtok REAL,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, provider_key, model_key),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_ai_routing_policy (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  policy_key TEXT NOT NULL,
  default_text_model TEXT,
  cheap_text_model TEXT,
  senior_text_model TEXT,
  default_image_model TEXT,
  standard_image_model TEXT,
  review_provider TEXT,
  router_strategy TEXT NOT NULL DEFAULT 'deterministic_guardrails_then_thompson_sampling',
  blocked_models_json TEXT NOT NULL DEFAULT '[]',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  UNIQUE (workspace_id, policy_key),
  CHECK (json_valid(blocked_models_json)),
  CHECK (json_valid(metadata_json))
);

CREATE TABLE IF NOT EXISTS cms_ai_routing_arms (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workspace_id TEXT NOT NULL,
  provider_key TEXT NOT NULL,
  model_key TEXT NOT NULL,
  task_type TEXT NOT NULL,
  mode TEXT NOT NULL DEFAULT 'agent',
  is_enabled INTEGER NOT NULL DEFAULT 1,
  alpha REAL NOT NULL DEFAULT 1,
  beta REAL NOT NULL DEFAULT 1,
  total_runs INTEGER NOT NULL DEFAULT 0,
  successes INTEGER NOT NULL DEFAULT 0,
  failures INTEGER NOT NULL DEFAULT 0,
  avg_latency_ms REAL DEFAULT 0,
  avg_cost_usd REAL DEFAULT 0,
  avg_quality_score REAL DEFAULT 0,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (tenant_id) REFERENCES cms_tenants(id) ON DELETE CASCADE,
  FOREIGN KEY (workspace_id) REFERENCES cms_workspaces(id) ON DELETE CASCADE,
  CHECK (json_valid(metadata_json))
);

------------------------------------------------------------
-- 12. Views
------------------------------------------------------------

CREATE VIEW IF NOT EXISTS v_cms_page_status AS
SELECT
  workspace_id,
  status,
  COUNT(*) AS page_count
FROM cms_pages
GROUP BY workspace_id, status;

CREATE VIEW IF NOT EXISTS v_cms_recent_activity AS
SELECT
  id,
  workspace_id,
  actor_user_id,
  action,
  entity_type,
  entity_id,
  route_path,
  created_at
FROM cms_activity_log
ORDER BY created_at DESC
LIMIT 100;

CREATE VIEW IF NOT EXISTS v_cms_lead_pipeline AS
SELECT
  workspace_id,
  status,
  COUNT(*) AS lead_count
FROM cms_leads
GROUP BY workspace_id, status;

------------------------------------------------------------
-- 13. Seed data
------------------------------------------------------------

INSERT OR IGNORE INTO cms_schema_migrations (id, name, checksum)
VALUES ('010_full_cms_runtime', 'Full CMS runtime schema', 'manual');

INSERT OR IGNORE INTO cms_tenants (id, slug, name, metadata_json)
VALUES (
  'tenant_leadership_legacy',
  'leadership-legacy',
  'Leadership Legacy Digital',
  json_object('founder', 'Connor McNeely')
);

INSERT OR IGNORE INTO cms_workspaces (id, tenant_id, slug, name, timezone, metadata_json)
VALUES (
  'ws_leadership_legacy',
  'tenant_leadership_legacy',
  'main',
  'Leadership Legacy Main Site',
  'America/Chicago',
  json_object('site_url', 'https://leadership-legacy.meauxbility.workers.dev')
);

INSERT OR IGNORE INTO cms_users (id, tenant_id, email, display_name, role)
VALUES (
  'user_sam_admin',
  'tenant_leadership_legacy',
  'inneranimalclothing@gmail.com',
  'Sam Primeaux',
  'owner'
);

INSERT OR IGNORE INTO cms_brand_settings (
  id,
  tenant_id,
  workspace_id,
  brand_name,
  founder_name,
  company_name,
  tagline,
  tokens_json,
  typography_json,
  social_links_json,
  contact_json
) VALUES (
  'brand_leadership_legacy',
  'tenant_leadership_legacy',
  'ws_leadership_legacy',
  'Leadership Legacy Digital',
  'Connor McNeely',
  'Leadership Legacy Digital',
  'Engineering precision meets AI intelligence.',
  json_object(
    'background', '#070b12',
    'backgroundSoft', '#0d1320',
    'surface', '#111827',
    'surfaceElevated', '#172033',
    'text', '#f5f7fb',
    'textMuted', '#9ca8bd',
    'primary', '#38bdf8',
    'primaryStrong', '#0ea5e9',
    'accent', '#22c55e',
    'accentWarm', '#f59e0b',
    'border', 'rgba(148, 163, 184, 0.18)',
    'glass', 'rgba(15, 23, 42, 0.72)'
  ),
  json_object(
    'display', 'Satoshi, Inter, system-ui, sans-serif',
    'body', 'Inter, system-ui, sans-serif',
    'mono', 'JetBrains Mono, SFMono-Regular, monospace'
  ),
  json_object(),
  json_object('primary_email', null)
);

INSERT OR IGNORE INTO cms_themes (
  id,
  tenant_id,
  workspace_id,
  name,
  slug,
  mode,
  tokens_json,
  css_vars_json,
  status
) VALUES (
  'theme_ll_dark',
  'tenant_leadership_legacy',
  'ws_leadership_legacy',
  'Leadership Legacy Dark',
  'leadership-legacy-dark',
  'auto',
  json_object('primary', '#38bdf8', 'accent', '#22c55e'),
  json_object('--color-primary', '#38bdf8', '--color-accent', '#22c55e'),
  'active'
);

INSERT OR IGNORE INTO cms_r2_buckets (
  id,
  tenant_id,
  workspace_id,
  binding_name,
  bucket_name,
  public_dev_url,
  s3_endpoint,
  catalog_uri,
  warehouse_name,
  location,
  metadata_json
) VALUES (
  'bucket_leadership_legacy',
  'tenant_leadership_legacy',
  'ws_leadership_legacy',
  'WEBSITE',
  'leadership-legacy',
  'https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev',
  'https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy',
  'https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy',
  'ede6590ac0d2fb7daf155b35653457b2_leadership-legacy',
  'WNAM',
  json_object('purpose', 'CMS assets, snapshots, generated media, docs, exports, analytics')
);

INSERT OR IGNORE INTO cms_navigation_menus (
  id,
  tenant_id,
  workspace_id,
  menu_key,
  name,
  location,
  items_json
) VALUES (
  'nav_primary',
  'tenant_leadership_legacy',
  'ws_leadership_legacy',
  'primary',
  'Primary Navigation',
  'header',
  json_array(
    json_object('label', 'Services', 'href', '/services'),
    json_object('label', 'Work', 'href', '/work'),
    json_object('label', 'About', 'href', '/about'),
    json_object('label', 'Resources', 'href', '/resources'),
    json_object('label', 'Contact', 'href', '/contact')
  )
);

INSERT OR IGNORE INTO cms_pages (
  id,
  tenant_id,
  workspace_id,
  title,
  slug,
  route_path,
  page_type,
  status,
  is_homepage,
  seo_json,
  draft_json,
  published_json
) VALUES (
  'page_home',
  'tenant_leadership_legacy',
  'ws_leadership_legacy',
  'Home',
  '/',
  '/',
  'landing',
  'published',
  1,
  json_object(
    'title', 'Connor McNeely | Engineering-Grade AI Systems',
    'description', 'Mechanical engineer and AI developer building RAG systems, automation workflows, CAD tools, and full-stack applications.'
  ),
  json_object('sections', json_array()),
  json_object('sections', json_array())
);

INSERT OR IGNORE INTO cms_ai_providers (
  id,
  tenant_id,
  workspace_id,
  provider_key,
  display_name,
  secret_name,
  status,
  use_cases_json
) VALUES
  ('provider_openai', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'OpenAI', 'OPENAI_API_KEY', 'needs_secret', json_array('chat','routing','image_generation','evals')),
  ('provider_anthropic', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'anthropic', 'Anthropic', 'ANTHROPIC_API_KEY', 'needs_secret', json_array('chat','routing','code_review','evals'));

INSERT OR IGNORE INTO cms_ai_models (
  id,
  tenant_id,
  workspace_id,
  provider_key,
  model_key,
  display_name,
  lane,
  runtime,
  modality,
  is_enabled,
  is_blocked,
  metadata_json
) VALUES
  ('openai_gpt_5_4_nano', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4-nano', 'GPT-5.4 Nano', 'cheap_fast_router', 'responses', 'text', 1, 0, '{}'),
  ('openai_gpt_5_4_mini', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4-mini', 'GPT-5.4 Mini', 'default_workhorse', 'responses', 'text', 1, 0, '{}'),
  ('openai_gpt_5_4', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4', 'GPT-5.4', 'senior_reasoning', 'responses', 'text', 1, 0, '{}'),
  ('openai_image_1_mini', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-image-1-mini', 'GPT Image 1 Mini', 'budget_image_generation', 'images', 'image', 1, 0, '{}'),
  ('openai_image_1_5', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-image-1.5', 'GPT Image 1.5', 'standard_image_generation', 'images', 'image', 1, 0, '{}'),
  ('openai_gpt_5_5_blocked', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.5', 'GPT-5.5', 'blocked', 'responses', 'text', 0, 1, json_object('reason','Do not implement yet')),
  ('openai_gpt_5_5_pro_blocked', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.5-pro', 'GPT-5.5 Pro', 'blocked', 'responses', 'text', 0, 1, json_object('reason','Do not implement yet')),
  ('openai_gpt_5_4_pro_blocked', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'openai', 'gpt-5.4-pro', 'GPT-5.4 Pro', 'blocked', 'responses', 'text', 0, 1, json_object('reason','User policy excluded')),
  ('anthropic_sonnet', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'anthropic', 'claude-sonnet', 'Claude Sonnet', 'standard_senior_review', 'messages', 'text', 1, 0, '{}'),
  ('anthropic_haiku', 'tenant_leadership_legacy', 'ws_leadership_legacy', 'anthropic', 'claude-haiku', 'Claude Haiku', 'cheap_fast_fallback', 'messages', 'text', 1, 0, '{}');

INSERT OR IGNORE INTO cms_ai_routing_policy (
  id,
  tenant_id,
  workspace_id,
  policy_key,
  default_text_model,
  cheap_text_model,
  senior_text_model,
  default_image_model,
  standard_image_model,
  review_provider,
  blocked_models_json,
  metadata_json
) VALUES (
  'policy_default',
  'tenant_leadership_legacy',
  'ws_leadership_legacy',
  'default',
  'gpt-5.4-mini',
  'gpt-5.4-nano',
  'gpt-5.4',
  'gpt-image-1-mini',
  'gpt-image-1.5',
  'anthropic',
  json_array('gpt-5.5','gpt-5.5-pro','gpt-5.4-pro'),
  json_object('router', 'deterministic_guardrails_then_thompson_sampling')
);
