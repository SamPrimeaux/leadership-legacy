PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cms_ai_providers (
  id TEXT PRIMARY KEY,
  provider_key TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  secret_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'needs_secret',
  use_cases_json TEXT NOT NULL DEFAULT '[]',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cms_ai_models (
  id TEXT PRIMARY KEY,
  provider_key TEXT NOT NULL,
  model_key TEXT NOT NULL,
  display_name TEXT NOT NULL,
  lane TEXT NOT NULL,
  is_enabled INTEGER NOT NULL DEFAULT 1,
  is_blocked INTEGER NOT NULL DEFAULT 0,
  input_price_per_mtok REAL,
  output_price_per_mtok REAL,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(provider_key, model_key)
);

CREATE TABLE IF NOT EXISTS cms_ai_routing_policy (
  id TEXT PRIMARY KEY,
  policy_key TEXT NOT NULL UNIQUE,
  default_text_model TEXT,
  cheap_text_model TEXT,
  senior_text_model TEXT,
  default_image_model TEXT,
  standard_image_model TEXT,
  review_provider TEXT,
  blocked_models_json TEXT NOT NULL DEFAULT '[]',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO cms_ai_providers (
  id,
  provider_key,
  display_name,
  secret_name,
  use_cases_json
) VALUES
  ('provider_openai', 'openai', 'OpenAI', 'OPENAI_API_KEY', json_array('chat','routing','image_generation','evals')),
  ('provider_anthropic', 'anthropic', 'Anthropic', 'ANTHROPIC_API_KEY', json_array('chat','routing','code_review','evals'));

INSERT OR IGNORE INTO cms_ai_models (
  id,
  provider_key,
  model_key,
  display_name,
  lane,
  is_enabled,
  is_blocked,
  metadata_json
) VALUES
  ('openai_gpt_5_4_nano', 'openai', 'gpt-5.4-nano', 'GPT-5.4 Nano', 'cheap_fast_router', 1, 0, '{}'),
  ('openai_gpt_5_4_mini', 'openai', 'gpt-5.4-mini', 'GPT-5.4 Mini', 'default_workhorse', 1, 0, '{}'),
  ('openai_gpt_5_4', 'openai', 'gpt-5.4', 'GPT-5.4', 'senior_reasoning', 1, 0, '{}'),
  ('openai_image_1_mini', 'openai', 'gpt-image-1-mini', 'GPT Image 1 Mini', 'budget_image_generation', 1, 0, '{}'),
  ('openai_image_1_5', 'openai', 'gpt-image-1.5', 'GPT Image 1.5', 'standard_image_generation', 1, 0, '{}'),
  ('openai_gpt_5_5_blocked', 'openai', 'gpt-5.5', 'GPT-5.5', 'blocked', 0, 1, json_object('reason','User policy: do not implement yet')),
  ('openai_gpt_5_5_pro_blocked', 'openai', 'gpt-5.5-pro', 'GPT-5.5 Pro', 'blocked', 0, 1, json_object('reason','User policy: do not implement yet')),
  ('openai_gpt_5_4_pro_blocked', 'openai', 'gpt-5.4-pro', 'GPT-5.4 Pro', 'blocked', 0, 1, json_object('reason','User policy: exclude')),
  ('anthropic_sonnet', 'anthropic', 'claude-sonnet', 'Claude Sonnet', 'standard_senior_review', 1, 0, '{}'),
  ('anthropic_haiku', 'anthropic', 'claude-haiku', 'Claude Haiku', 'cheap_fast_fallback', 1, 0, '{}');

INSERT OR IGNORE INTO cms_ai_routing_policy (
  id,
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
  'default',
  'gpt-5.4-mini',
  'gpt-5.4-nano',
  'gpt-5.4',
  'gpt-image-1-mini',
  'gpt-image-1.5',
  'anthropic',
  json_array('gpt-5.5','gpt-5.5-pro','gpt-5.4-pro'),
  json_object('router','deterministic_guardrails_then_thompson_sampling')
);
