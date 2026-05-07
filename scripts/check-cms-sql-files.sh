#!/usr/bin/env bash
set -euo pipefail

echo "D1 SQL files:"
ls -lah sql/d1/010_full_cms_runtime.sql sql/d1/011_full_cms_runtime_triggers.sql sql/d1/012_full_cms_seed_content.sql

echo "Supabase SQL files:"
ls -lah sql/supabase/010_full_cms_analytics_rag.sql sql/supabase/011_full_cms_functions.sql sql/supabase/012_full_cms_seed.sql

echo "CMS SQL docs:"
ls -lah docs/CMS_SQL_LOGIC.md
