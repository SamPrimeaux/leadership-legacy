-- Leadership Legacy Digital — email system schema (D1)
-- Run: npx wrangler d1 execute leadership-legacy --remote --file=docs/email-system/001_schema.sql
-- Reference: companionscpas/db/migrations/20260619_email_inbox.sql + schema_payments_email.sql

CREATE TABLE IF NOT EXISTS email_templates (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'tenant_leadership_legacy',
  provider TEXT DEFAULT 'resend',
  template_key TEXT NOT NULL,
  subject TEXT NOT NULL,
  body_text TEXT,
  body_html TEXT,
  status TEXT DEFAULT 'active',
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE(tenant_id, template_key)
);

CREATE TABLE IF NOT EXISTS email_logs (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'tenant_leadership_legacy',
  recipient_email TEXT NOT NULL,
  recipient_name TEXT,
  subject TEXT NOT NULL,
  email_type TEXT NOT NULL,
  from_email TEXT,
  provider TEXT DEFAULT 'resend',
  provider_message_id TEXT,
  status TEXT DEFAULT 'queued',
  related_type TEXT,
  related_id TEXT,
  error_message TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  sent_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_email_logs_tenant ON email_logs(tenant_id, created_at);

CREATE TABLE IF NOT EXISTS inbound_emails (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'tenant_leadership_legacy',
  resend_email_id TEXT,
  provider_event_id TEXT,
  message_id TEXT,
  thread_key TEXT,
  mailbox TEXT NOT NULL,
  from_email TEXT NOT NULL,
  from_name TEXT,
  to_json TEXT DEFAULT '[]',
  cc_json TEXT DEFAULT '[]',
  subject TEXT,
  preview_text TEXT,
  body_html TEXT,
  body_text TEXT,
  attachments_json TEXT DEFAULT '[]',
  status TEXT DEFAULT 'unread',
  source TEXT DEFAULT 'resend',
  folder_id TEXT,
  is_important INTEGER DEFAULT 0,
  is_deleted INTEGER DEFAULT 0,
  in_reply_to TEXT,
  related_type TEXT,
  related_id TEXT,
  raw_event_json TEXT,
  received_at TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_inbound_resend_email
  ON inbound_emails(tenant_id, resend_email_id)
  WHERE resend_email_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_inbound_mailbox
  ON inbound_emails(tenant_id, mailbox, status, received_at);

CREATE TABLE IF NOT EXISTS email_drafts (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'tenant_leadership_legacy',
  to_json TEXT DEFAULT '[]',
  cc_json TEXT DEFAULT '[]',
  subject TEXT,
  body_html TEXT,
  body_text TEXT,
  from_email TEXT,
  folder_id TEXT,
  created_by TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_email_drafts_tenant ON email_drafts(tenant_id, updated_at);

CREATE TABLE IF NOT EXISTS email_folders (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'tenant_leadership_legacy',
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  is_system INTEGER DEFAULT 0,
  sort_order INTEGER DEFAULT 50,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE(tenant_id, slug)
);

INSERT OR IGNORE INTO email_folders (id, tenant_id, name, slug, is_system, sort_order)
VALUES ('fld_leads', 'tenant_leadership_legacy', 'Leads', 'leads', 1, 10);

CREATE TABLE IF NOT EXISTS email_campaigns (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL DEFAULT 'tenant_leadership_legacy',
  name TEXT NOT NULL,
  subject TEXT NOT NULL,
  body_html TEXT,
  body_text TEXT,
  from_email TEXT,
  audience_type TEXT DEFAULT 'manual',
  audience_json TEXT DEFAULT '[]',
  status TEXT DEFAULT 'draft',
  scheduled_at TEXT,
  sent_at TEXT,
  stats_json TEXT DEFAULT '{}',
  created_by TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_email_campaigns_tenant
  ON email_campaigns(tenant_id, status, updated_at);
