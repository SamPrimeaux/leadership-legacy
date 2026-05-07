#!/usr/bin/env bash
set -euo pipefail

files=(
  "docs/TOOLS_README.md"
  "docs/integrations/GITHUB_SETUP_PLAYBOOK.md"
  "docs/integrations/GOOGLE_DRIVE_GMAIL_SETUP_PLAYBOOK.md"
  "docs/integrations/MCP_TOOLS_PLAYBOOK.md"
  "docs/integrations/AI_PROVIDERS_SETUP_PLAYBOOK.md"
  "docs/integrations/AWS_SETUP_PLAYBOOK.md"
  "docs/integrations/RESEND_EMAIL_PLAYBOOK.md"
  "docs/CONNOR_COURSE_STUDY_GUIDE.md"
  "docs/CONNOR_PROGRESS_TRACKER.md"
  "docs/RUBRIC.md"
  "docs/END_TO_END_INTEGRATION_PLAYBOOK.md"
)

for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing $file"
    exit 1
  fi
  echo "OK $file"
done

echo "Tools docs complete."
