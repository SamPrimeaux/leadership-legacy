#!/usr/bin/env python3
from pathlib import Path
import subprocess
import textwrap

ROOT = Path.cwd()

def run(cmd, check=True):
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
    write("sql/d1/010_full_cms_runtime.sql", r'''
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
    ''')

    write("sql/d1/011_full_cms_runtime_triggers.sql", r'''
    -- D1 CMS triggers for timestamps and activity.
    PRAGMA foreign_keys = ON;

    CREATE TRIGGER IF NOT EXISTS trg_cms_pages_updated_at
    AFTER UPDATE ON cms_pages
    FOR EACH ROW
    BEGIN
      UPDATE cms_pages SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_cms_page_sections_updated_at
    AFTER UPDATE ON cms_page_sections
    FOR EACH ROW
    BEGIN
      UPDATE cms_page_sections SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_cms_assets_updated_at
    AFTER UPDATE ON cms_assets
    FOR EACH ROW
    BEGIN
      UPDATE cms_assets SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_cms_leads_updated_at
    AFTER UPDATE ON cms_leads
    FOR EACH ROW
    BEGIN
      UPDATE cms_leads SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_cms_services_updated_at
    AFTER UPDATE ON cms_services
    FOR EACH ROW
    BEGIN
      UPDATE cms_services SET updated_at = datetime('now') WHERE id = NEW.id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_cms_case_studies_updated_at
    AFTER UPDATE ON cms_case_studies
    FOR EACH ROW
    BEGIN
      UPDATE cms_case_studies SET updated_at = datetime('now') WHERE id = NEW.id;
    END;
    ''')

    write("sql/d1/012_full_cms_seed_content.sql", r'''
    -- Leadership Legacy starter content seed for D1.
    PRAGMA foreign_keys = ON;

    INSERT OR IGNORE INTO cms_templates (
      id,
      tenant_id,
      workspace_id,
      template_key,
      name,
      template_type,
      schema_json,
      default_sections_json
    ) VALUES
      (
        'template_landing',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'landing',
        'Landing Page',
        'landing',
        json_object('supports_sections', 1),
        json_array('heroConnor', 'servicesGrid', 'caseStudyGrid', 'founderStory', 'contactBand')
      ),
      (
        'template_service',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'service',
        'Service Page',
        'service',
        json_object('supports_sections', 1),
        json_array('serviceHero', 'serviceDeliverables', 'serviceUseCases', 'contactBand')
      ),
      (
        'template_case_study',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'case_study',
        'Case Study Page',
        'case_study',
        json_object('supports_sections', 1),
        json_array('caseStudyHero', 'problemSolution', 'stack', 'outcome', 'contactBand')
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
      template_id,
      seo_json,
      draft_json,
      published_json
    ) VALUES
      (
        'page_about',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'About',
        'about',
        '/about',
        'page',
        'published',
        'template_landing',
        json_object('title','About Connor McNeely','description','Mechanical engineer and AI developer building engineering-grade AI systems.'),
        json_object('sections', json_array()),
        json_object('sections', json_array())
      ),
      (
        'page_services',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'Services',
        'services',
        '/services',
        'page',
        'published',
        'template_landing',
        json_object('title','Services | Leadership Legacy Digital','description','AI engineering, RAG systems, CAD automation, and full-stack app development.'),
        json_object('sections', json_array()),
        json_object('sections', json_array())
      ),
      (
        'page_work',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'Work',
        'work',
        '/work',
        'page',
        'published',
        'template_landing',
        json_object('title','Work | Leadership Legacy Digital','description','Case studies for technical AI systems and automation workflows.'),
        json_object('sections', json_array()),
        json_object('sections', json_array())
      ),
      (
        'page_contact',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'Contact',
        'contact',
        '/contact',
        'page',
        'published',
        'template_landing',
        json_object('title','Contact | Leadership Legacy Digital','description','Start a project with Connor McNeely and Leadership Legacy Digital.'),
        json_object('sections', json_array()),
        json_object('sections', json_array())
      );

    INSERT OR IGNORE INTO cms_services (
      id,
      tenant_id,
      workspace_id,
      slug,
      title,
      eyebrow,
      summary,
      starting_at,
      deliverables_json,
      use_cases_json,
      stack_json,
      status,
      order_index
    ) VALUES
      (
        'service_ai_engineering',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'ai-engineering',
        'AI Engineering',
        'Custom AI Systems',
        'Production-ready AI tools, copilots, and multi-agent workflows designed around real business processes.',
        '$5,000+',
        json_array('LLM integration', 'Agent workflows', 'Prompt systems', 'Tool routing', 'Deployment'),
        json_array('Internal copilots', 'Workflow automation', 'Technical assistants', 'AI-enabled dashboards'),
        json_array('OpenAI', 'Anthropic', 'Cloudflare Workers', 'D1', 'R2'),
        'published',
        10
      ),
      (
        'service_rag_systems',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'rag-systems',
        'RAG Systems',
        'Document Intelligence',
        'Source-cited knowledge systems for engineering documents, SOPs, manuals, support libraries, and standards.',
        '$5,000+',
        json_array('Document ingestion', 'Embeddings', 'Retrieval tuning', 'Source citations', 'Admin UI'),
        json_array('Technical docs', 'Internal knowledge', 'Support automation', 'Standards lookup'),
        json_array('Vector Search', 'Postgres', 'Cloudflare Vectorize', 'OpenAI', 'Anthropic'),
        'published',
        20
      ),
      (
        'service_full_stack_apps',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'full-stack-apps',
        'Full-Stack AI Apps',
        'SaaS & Dashboards',
        'React/Vite apps, dashboards, APIs, auth, database, payments, and AI features packaged into deployable applications.',
        '$8,000+',
        json_array('React app', 'API design', 'Database schema', 'Auth', 'Payments', 'Deployment'),
        json_array('AI SaaS MVPs', 'Admin dashboards', 'Customer portals', 'Internal tools'),
        json_array('React', 'Vite', 'Cloudflare Workers', 'D1', 'R2', 'Stripe', 'Resend'),
        'published',
        30
      ),
      (
        'service_cad_automation',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'cad-automation',
        'CAD Automation',
        'Engineering Workflow Automation',
        'Automate repetitive CAD, drawing, BOM, and engineering documentation workflows.',
        '$75/hr',
        json_array('SolidWorks automation', 'BOM workflows', 'Drawing automation', 'CAD file structure'),
        json_array('Design iteration reduction', 'Drawing generation', 'Engineering calculators', 'Technical configurators'),
        json_array('SolidWorks', 'CAD', 'Python', 'Automation', 'Engineering Docs'),
        'published',
        40
      );

    INSERT OR IGNORE INTO cms_case_studies (
      id,
      tenant_id,
      workspace_id,
      slug,
      title,
      category,
      summary,
      problem,
      solution,
      outcome,
      stack_json,
      metrics_json,
      status,
      featured,
      order_index
    ) VALUES
      (
        'case_mechassist_ai',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'mechassist-ai',
        'MechAssist AI',
        'RAG / Engineering AI',
        'A mechanical engineering assistant designed to retrieve, reason over, and cite technical documentation.',
        'Engineering knowledge is scattered across manuals, standards, docs, and tribal workflows.',
        'A RAG system that retrieves relevant technical content and returns source-backed answers.',
        'Faster access to technical knowledge and a foundation for engineering-specific copilots.',
        json_array('RAG', 'Vector Search', 'LLM', 'Engineering Docs'),
        json_object('status','concept_proof'),
        'published',
        1,
        10
      ),
      (
        'case_openclaw',
        'tenant_leadership_legacy',
        'ws_leadership_legacy',
        'openclaw',
        'OpenClaw',
        'Multi-Agent AI',
        'A live outbound AI agent system for automation, sales workflows, and campaign execution.',
        'Outbound workflows require research, personalization, follow-up, and structured task execution.',
        'A multi-agent workflow foundation for intelligent outreach and campaign execution.',
        'A clearer path toward automated outbound systems with human oversight.',
        json_array('Agents', 'Automation', 'CRM', 'LLM'),
        json_object('status','draft'),
        'draft',
        1,
        20
      );
    ''')

    write("sql/supabase/010_full_cms_analytics_rag.sql", r'''
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
    ''')

    write("sql/supabase/011_full_cms_functions.sql", r'''
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
    ''')

    write("sql/supabase/012_full_cms_seed.sql", r'''
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
    ''')

    write("docs/CMS_SQL_LOGIC.md", r'''
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
    ''')

    write("scripts/apply-d1-cms-sql.sh", r'''
    #!/usr/bin/env bash
    set -euo pipefail

    DB_NAME="${1:-leadership-legacy}"

    npx wrangler d1 execute "$DB_NAME" --remote --file sql/d1/010_full_cms_runtime.sql
    npx wrangler d1 execute "$DB_NAME" --remote --file sql/d1/011_full_cms_runtime_triggers.sql
    npx wrangler d1 execute "$DB_NAME" --remote --file sql/d1/012_full_cms_seed_content.sql

    echo "Applied D1 CMS SQL to $DB_NAME"
    ''')

    write("scripts/check-cms-sql-files.sh", r'''
    #!/usr/bin/env bash
    set -euo pipefail

    echo "D1 SQL files:"
    ls -lah sql/d1/010_full_cms_runtime.sql sql/d1/011_full_cms_runtime_triggers.sql sql/d1/012_full_cms_seed_content.sql

    echo "Supabase SQL files:"
    ls -lah sql/supabase/010_full_cms_analytics_rag.sql sql/supabase/011_full_cms_functions.sql sql/supabase/012_full_cms_seed.sql

    echo "CMS SQL docs:"
    ls -lah docs/CMS_SQL_LOGIC.md
    ''')

    run(["chmod", "+x", "scripts/apply-d1-cms-sql.sh"], check=False)
    run(["chmod", "+x", "scripts/check-cms-sql-files.sh"], check=False)

    run(["./scripts/check-cms-sql-files.sh"], check=True)

    run(["git", "add", "sql/d1", "sql/supabase", "docs/CMS_SQL_LOGIC.md", "scripts/apply-d1-cms-sql.sh", "scripts/check-cms-sql-files.sh"], check=True)
    run(["git", "commit", "-m", "feat: add full CMS SQL logic for D1 and Supabase"], check=False)

    print("\nFull CMS SQL generation complete.")
    print("Next:")
    print("git push origin main")
    print("./scripts/apply-d1-cms-sql.sh <YOUR_D1_DB_NAME>")
    print("Run Supabase SQL files through Supabase SQL Editor or your Supabase migration flow.")

if __name__ == "__main__":
    main()
