#!/usr/bin/env bash
set -euo pipefail

echo "Checking onboarding docs..."

files=(
  "README.md"
  "docs/CONNECTORS_SETUP_GUIDE.md"
  "docs/CONNOR_HANDOFF_CHECKLIST.md"
  "docs/ENVIRONMENT_VARIABLES.md"
  "docs/PROVIDER_ROUTING_PLAN.md"
  "docs/GOOGLE_OAUTH_PLAN.md"
  "docs/CAD_OPENSCAD_SPLINE_PLAN.md"
  "docs/CLOUDFLARE_BINDINGS_PLAN.md"
)

for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing: $file"
    exit 1
  fi
  echo "OK: $file"
done

echo "Onboarding docs are present."
