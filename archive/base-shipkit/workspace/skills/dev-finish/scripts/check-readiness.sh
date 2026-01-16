#!/usr/bin/env bash
# check-readiness.sh - Verify tests pass and present merge options
# Part of shipkit dev-finish skill

set -e

# =============================================================================
# SETUP
# =============================================================================

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# =============================================================================
# CHECK GIT STATUS
# =============================================================================

echo ""
echo -e "${CYAN}Checking git status...${NC}"
echo ""

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo -e "${RED}✗${NC} Not in a git repository"
  exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ -z "$CURRENT_BRANCH" ]]; then
  echo -e "${RED}✗${NC} Not on a branch (detached HEAD)"
  exit 1
fi

echo -e "${GREEN}✓${NC} Current branch: $CURRENT_BRANCH"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo -e "${YELLOW}⚠${NC} Uncommitted changes detected:"
  echo ""
  git status --short
  echo ""
  echo -e "${YELLOW}Please commit or stash changes before finishing.${NC}"
  exit 1
fi

echo -e "${GREEN}✓${NC} No uncommitted changes"

# =============================================================================
# DETERMINE BASE BRANCH
# =============================================================================

echo ""
echo -e "${CYAN}Determining base branch...${NC}"
echo ""

# Try common base branches
BASE_BRANCH=""
for branch in main master develop; do
  if git rev-parse --verify "$branch" > /dev/null 2>&1; then
    if git merge-base HEAD "$branch" > /dev/null 2>&1; then
      BASE_BRANCH="$branch"
      break
    fi
  fi
done

if [[ -z "$BASE_BRANCH" ]]; then
  echo -e "${YELLOW}⚠${NC} Could not determine base branch automatically"
  echo ""
  echo "Available branches:"
  git branch -a | grep -v HEAD
  echo ""
  read -p "Which branch did this split from? " BASE_BRANCH
fi

echo -e "${GREEN}✓${NC} Base branch: $BASE_BRANCH"

# =============================================================================
# RUN TESTS
# =============================================================================

echo ""
echo -e "${CYAN}Running tests...${NC}"
echo ""

# Try to detect test command
TEST_COMMAND=""

if [[ -f "package.json" ]]; then
  TEST_COMMAND="npm test"
elif [[ -f "Cargo.toml" ]]; then
  TEST_COMMAND="cargo test"
elif [[ -f "pytest.ini" ]] || [[ -f "pyproject.toml" ]]; then
  TEST_COMMAND="pytest"
elif [[ -f "go.mod" ]]; then
  TEST_COMMAND="go test ./..."
elif [[ -f "Gemfile" ]]; then
  TEST_COMMAND="bundle exec rspec"
fi

if [[ -z "$TEST_COMMAND" ]]; then
  echo -e "${YELLOW}⚠${NC} Could not detect test command automatically"
  read -p "Enter test command (or press Enter to skip): " TEST_COMMAND
fi

if [[ -n "$TEST_COMMAND" ]]; then
  echo "Running: $TEST_COMMAND"
  echo ""

  if $TEST_COMMAND; then
    echo ""
    echo -e "${GREEN}✓${NC} All tests pass"
  else
    echo ""
    echo -e "${RED}✗${NC} Tests failing"
    echo ""
    echo -e "${YELLOW}Cannot proceed with merge/PR until tests pass.${NC}"
    echo "Fix tests and run this script again."
    exit 1
  fi
else
  echo -e "${YELLOW}⚠${NC} Skipping test verification"
  echo -e "${YELLOW}  Make sure tests pass before merging!${NC}"
fi

# =============================================================================
# PRESENT OPTIONS
# =============================================================================

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}Implementation complete!${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo "What would you like to do?"
echo ""
echo "  1. Merge to $BASE_BRANCH locally"
echo "  2. Keep branch as-is (handle later)"
echo "  3. Discard this work"
echo ""
echo "For Claude: Use merge-branch.sh with --option=1, --option=2, or --option=3"
echo ""

exit 0
