#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-HSRT-Knowledge-Vault-Template}"
if [[ ! "$NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "Invalid repository name." >&2
  exit 2
fi
command -v git >/dev/null || { echo "git is required" >&2; exit 2; }
command -v gh >/dev/null || { echo "GitHub CLI (gh) is required" >&2; exit 2; }
command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 2; }
cd "$(dirname "$0")/.."
if [[ -d .git ]]; then
  if git remote | grep -q .; then
    echo "ABORT: Existing Git remote detected. This script only publishes a fresh standalone template." >&2
    exit 2
  fi
  if [[ $(git rev-list --count --all 2>/dev/null || echo 0) -gt 0 ]]; then
    echo "ABORT: Existing Git history. Publish only from a fresh extracted template directory." >&2
    exit 2
  fi
fi
python3 scripts/validate_vault.py .
python3 scripts/audit_public.py .
python3 -m unittest discover -s tests -v
gh auth status >/dev/null
OWNER="$(gh api user --jq '.login')"
TARGET="${OWNER}/${NAME}"
if gh repo view "$TARGET" >/dev/null 2>&1; then
  echo "ABORT: ${TARGET} already exists." >&2
  exit 2
fi
printf '
You are about to publish this directory to a NEW PUBLIC GitHub repository:
  %s
' "$TARGET"
printf 'Type PUBLISH to confirm: '
read -r ACCEPT
[[ "$ACCEPT" == "PUBLISH" ]] || { echo "Cancelled."; exit 1; }
if [[ ! -d .git ]]; then git init -b main; fi
git add .
git commit -m "Initial public source-free knowledge vault template"
gh repo create "$TARGET" --public --source=. --remote=origin --push   --description "Source-linked knowledge vault template with HSRT-inspired admission governance"
gh repo edit "$TARGET" --template
echo "Published: https://github.com/${TARGET}"
