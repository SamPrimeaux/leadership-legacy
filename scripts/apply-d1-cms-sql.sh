#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${1:-leadership-legacy}"

npx wrangler d1 execute "$DB_NAME" --remote --file sql/d1/010_full_cms_runtime.sql
npx wrangler d1 execute "$DB_NAME" --remote --file sql/d1/011_full_cms_runtime_triggers.sql
npx wrangler d1 execute "$DB_NAME" --remote --file sql/d1/012_full_cms_seed_content.sql

echo "Applied D1 CMS SQL to $DB_NAME"
