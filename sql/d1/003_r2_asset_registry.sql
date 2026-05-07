PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cms_r2_buckets (
  id TEXT PRIMARY KEY,
  binding_name TEXT NOT NULL UNIQUE,
  bucket_name TEXT NOT NULL,
  public_dev_url TEXT,
  s3_endpoint TEXT,
  catalog_uri TEXT,
  warehouse_name TEXT,
  location TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cms_r2_objects (
  id TEXT PRIMARY KEY,
  bucket_binding TEXT NOT NULL,
  object_key TEXT NOT NULL,
  object_type TEXT NOT NULL DEFAULT 'asset',
  content_type TEXT,
  size_bytes INTEGER,
  public_url TEXT,
  etag TEXT,
  usage_context TEXT,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(bucket_binding, object_key)
);

INSERT OR IGNORE INTO cms_r2_buckets (
  id,
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
  'WEBSITE',
  'leadership-legacy',
  'https://pub-d426ded97b90451886c5cc7870ae9f17.r2.dev',
  'https://ede6590ac0d2fb7daf155b35653457b2.r2.cloudflarestorage.com/leadership-legacy',
  'https://catalog.cloudflarestorage.com/ede6590ac0d2fb7daf155b35653457b2/leadership-legacy',
  'ede6590ac0d2fb7daf155b35653457b2_leadership-legacy',
  'WNAM',
  json_object('created','2026-05-03','purpose','CMS assets, code snapshots, generated media, docs, exports, analytics')
);
