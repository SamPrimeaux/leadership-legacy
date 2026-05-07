#!/usr/bin/env bash
set -euo pipefail

BUCKET="leadership-legacy"

put_text() {
  local key="$1"
  local content="$2"
  local tmp
  tmp="$(mktemp)"
  printf "%s\n" "$content" > "$tmp"
  npx wrangler r2 object put "$BUCKET/$key" --file "$tmp" --remote
  rm -f "$tmp"
}

put_text "README.txt" "Leadership Legacy R2 bucket for CMS assets, snapshots, generated files, docs, exports, and analytics."
put_text "assets/.keep" "reserved for public/CMS assets"
put_text "assets/images/generated/.keep" "reserved for generated images"
put_text "assets/brand/.keep" "reserved for logos, marks, and brand assets"
put_text "assets/models/.keep" "reserved for GLB/3D model assets"
put_text "downloads/.keep" "reserved for PDFs and downloadable files"
put_text "cms/pages/.keep" "reserved for CMS page JSON"
put_text "cms/sections/.keep" "reserved for CMS section JSON"
put_text "cms/themes/.keep" "reserved for theme CSS/tokens"
put_text "cms/navigation/.keep" "reserved for navigation snapshots"
put_text "snapshots/.keep" "reserved for generated snapshots"
put_text "snapshots/code/.keep" "reserved for codebase snapshots"
put_text "snapshots/pages/.keep" "reserved for rendered page snapshots"
put_text "analytics/.keep" "reserved for analytics exports"
put_text "exports/dashboard/.keep" "reserved for dashboard exports"
put_text "docs/.keep" "reserved for docs"
put_text "tmp/.keep" "reserved for temporary generated artifacts"

echo "R2 structure seeded into $BUCKET"
