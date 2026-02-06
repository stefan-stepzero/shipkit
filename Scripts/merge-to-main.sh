#!/bin/bash
# Merge dev to main, excluding dev/ folder
# Usage: ./Scripts/merge-to-main.sh [commit message]

set -e

MESSAGE="${1:-Merge dev to main}"

echo "📦 Merging dev → main (excluding dev/ folder)..."

# Ensure we're on dev and up to date
git checkout dev
git pull private dev 2>/dev/null || true

# Switch to main
git checkout main
git pull origin main 2>/dev/null || true

# Merge without committing
git merge dev --no-commit --no-ff || {
    echo "⚠️  Merge conflicts detected. Resolve them, then:"
    echo "   git restore --staged --worktree dev/"
    echo "   git commit -m \"$MESSAGE\""
    exit 1
}

# Remove dev/ folder changes (keep main's version)
git restore --staged --worktree dev/ 2>/dev/null || true

# Commit
git commit -m "$MESSAGE

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

echo "✅ Merged to main (dev/ folder excluded)"
echo ""
echo "To push: git push origin main"
echo "To sync dev: git checkout dev && git merge main && git push private dev"
